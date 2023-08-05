import copy
import logging
import pathlib
import platform
import shutil
import subprocess
from datetime import datetime
from typing import Any, Iterator, Optional, Set

import pgtoolkit.conf
import port_for
import pydantic
import pytest
from pgtoolkit.ctl import Status
from typing_extensions import Protocol

from pglift import _install
from pglift import instance as instance_mod
from pglift import pm
from pglift.ctx import Context
from pglift.models import interface, system
from pglift.settings import POSTGRESQL_SUPPORTED_VERSIONS, Settings

from . import configure_instance, execute


@pytest.fixture(scope="session")
def redhat() -> bool:
    return pathlib.Path("/etc/redhat-release").exists()


@pytest.fixture(autouse=True)
def journalctl() -> Iterator[None]:
    journalctl = shutil.which("journalctl")
    if journalctl is None:
        yield
        return
    proc = subprocess.Popen([journalctl, "--user", "-f", "-n0"])
    yield
    proc.kill()


@pytest.fixture(scope="session")
def systemd_available() -> bool:
    try:
        subprocess.run(
            ["systemctl", "--user", "status"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=True,
        )
    except (FileNotFoundError, subprocess.CalledProcessError):
        return False
    return True


settings_by_id = {
    "defaults": {},
    "systemd": {
        "service_manager": "systemd",
        "scheduler": "systemd",
    },
    "postgresql_password_auth__surole_use_pgpass": {
        "postgresql": {
            "auth": {
                "local": "password",
                "host": "reject",
            },
            "surole": {
                "pgpass": True,
            },
        },
    },
    "postgresql_password_auth__surole_password_command": {
        "postgresql": {
            "auth": {
                "local": "password",
                "host": "reject",
            },
            "surole": {
                "pgpass": False,
            },
        },
    },
}
ids, params = zip(*settings_by_id.items())
ids = tuple(f"settings:{i}" for i in ids)


@pytest.fixture(scope="session", params=params, ids=ids)
def settings(
    request: Any,
    tmp_path_factory: pytest.TempPathFactory,
    systemd_available: bool,
) -> Settings:
    passfile = tmp_path_factory.mktemp("home") / ".pgpass"
    passfile.touch(mode=0o600)
    passfile.write_text("#hostname:port:database:username:password\n")

    prefix = tmp_path_factory.mktemp("prefix")
    (prefix / "run" / "postgresql").mkdir(parents=True)
    obj = copy.deepcopy(request.param)
    assert "prefix" not in obj
    obj["prefix"] = str(prefix)
    pg_obj = obj.setdefault("postgresql", {})
    assert "root" not in pg_obj
    pg_obj["root"] = str(tmp_path_factory.mktemp("postgres"))
    pgauth_obj = pg_obj.setdefault("auth", {})
    assert "passfile" not in pgauth_obj
    pgauth_obj["passfile"] = str(passfile)

    if pgauth_obj.get("local", "trust") != "trust" and not pg_obj.get("surole", {}).get(
        "pgpass", True
    ):
        assert "password_command" not in pgauth_obj
        pgauth_obj["password_command"] = str(
            tmp_path_factory.mktemp("home") / "passcmd"
        )
    if obj.get("service_manager") == "systemd" and not systemd_available:
        pytest.skip("systemd not functional")
    try:
        return Settings.parse_obj(obj)
    except pydantic.ValidationError as exc:
        pytest.skip(
            "; ".join(
                f"unsupported setting(s) {' '.join(e['loc'])}: {e['msg']}"
                for e in exc.errors()
            )
        )


@pytest.fixture(
    scope="session",
    params=POSTGRESQL_SUPPORTED_VERSIONS,
    ids=lambda v: f"postgresql:{v}",
)
def pg_version(request: Any, settings: Settings) -> str:
    version = request.param
    assert isinstance(version, str)
    if not pathlib.Path(settings.postgresql.bindir.format(version=version)).exists():
        pytest.skip(f"PostgreSQL {version} not available")
    return version


@pytest.fixture(scope="session")
def ctx(settings: Settings) -> Context:
    p = pm.PluginManager.get()
    p.trace.root.setwriter(print)
    p.enable_tracing()
    logger = logging.getLogger("pglift")
    logger.setLevel(logging.DEBUG)
    return Context(plugin_manager=p, settings=settings)


@pytest.fixture(scope="session")
def installed(ctx: Context, tmp_path_factory: pytest.TempPathFactory) -> Iterator[None]:
    tmp_path = tmp_path_factory.mktemp("config")
    settings = ctx.settings
    if settings.service_manager != "systemd":
        yield
        return

    custom_settings = tmp_path / "settings.json"
    custom_settings.write_text(settings.json())
    _install.do(
        ctx,
        env=f"SETTINGS=@{custom_settings}",
        header=f"# ** Test run on {platform.node()} at {datetime.now().isoformat()} **",
    )
    yield
    _install.undo(ctx)


@pytest.fixture(scope="session")
def tmp_port_factory() -> Iterator[int]:
    """Return a generator producing available and distinct TCP ports."""

    def available_ports() -> Iterator[int]:
        used: Set[int] = set()
        while True:
            port = port_for.select_random(exclude_ports=list(used))
            used.add(port)
            yield port

    return available_ports()


@pytest.fixture(scope="session")
def surole_password(settings: Settings) -> Iterator[Optional[str]]:
    if settings.postgresql.auth.local == "trust":
        yield None
        return

    passcmdfile = (
        pathlib.Path(settings.postgresql.auth.password_command)
        if settings.postgresql.auth.password_command
        else None
    )
    if passcmdfile:
        with passcmdfile.open("w") as f:
            f.write("#!/bin/sh\necho s3kret\n")
        passcmdfile.chmod(0o700)

    yield "s3kret"


@pytest.fixture(scope="session")
def instance_manifest(
    pg_version: str,
    settings: Settings,
    surole_password: Optional[str],
    tmp_port_factory: Iterator[int],
) -> interface.Instance:
    return interface.Instance(
        name="test",
        version=pg_version,
        surole_password=surole_password,
    )


@pytest.fixture(scope="session")
def instance_initialized(
    ctx: Context, instance_manifest: interface.Instance, installed: None
) -> system.Instance:
    assert instance_manifest.version is not None
    instance = system.BaseInstance.get(
        instance_manifest.name, instance_manifest.version, ctx
    )
    assert instance_mod.status(ctx, instance) == Status.unspecified_datadir
    instance_mod.init(ctx, instance_manifest)
    assert instance_mod.status(ctx, instance) == Status.not_running
    return system.Instance.system_lookup(ctx, instance)


@pytest.fixture(scope="session")
def log_directory(tmp_path_factory: pytest.TempPathFactory) -> pathlib.Path:
    return tmp_path_factory.mktemp("postgres-logs")


@pytest.fixture(scope="session")
def instance(
    ctx: Context,
    instance_manifest: interface.Instance,
    instance_initialized: system.Instance,
    tmp_port_factory: Iterator[int],
    log_directory: pathlib.Path,
) -> system.Instance:
    port = next(tmp_port_factory)
    configure_instance(
        ctx, instance_manifest, port=port, log_directory=str(log_directory)
    )
    return instance_initialized


@pytest.fixture(scope="session")
def instance_dropped(
    ctx: Context, instance: system.Instance
) -> pgtoolkit.conf.Configuration:
    config = instance.config()
    if instance.exists():
        instance_mod.drop(ctx, instance)
    return config


class RoleFactory(Protocol):
    def __call__(self, name: str, options: str = "") -> None:
        ...


@pytest.fixture(scope="module")
def role_factory(ctx: Context, instance: system.Instance) -> Iterator[RoleFactory]:
    rolnames = set()

    def factory(name: str, options: str = "") -> None:
        if name in rolnames:
            raise ValueError(f"'{name}' name already taken")
        execute(ctx, instance, f"CREATE ROLE {name} {options}", fetch=False)
        rolnames.add(name)

    yield factory

    for name in rolnames:
        execute(ctx, instance, f"DROP ROLE IF EXISTS {name}", fetch=False)


class DatabaseFactory(Protocol):
    def __call__(self, name: str) -> None:
        ...


@pytest.fixture(scope="module")
def database_factory(
    ctx: Context, instance: system.Instance
) -> Iterator[DatabaseFactory]:
    datnames = set()

    def factory(name: str) -> None:
        if name in datnames:
            raise ValueError(f"'{name}' name already taken")
        execute(
            ctx,
            instance,
            f"CREATE DATABASE {name}",
            fetch=False,
            autocommit=True,
        )
        datnames.add(name)

    yield factory

    for name in datnames:
        execute(
            ctx,
            instance,
            f"DROP DATABASE IF EXISTS {name}",
            fetch=False,
            autocommit=True,
        )
