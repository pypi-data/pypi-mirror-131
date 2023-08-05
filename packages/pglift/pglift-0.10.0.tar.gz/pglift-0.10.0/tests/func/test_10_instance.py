import contextlib
import logging
from pathlib import Path
from typing import Iterator, List, NoReturn
from unittest.mock import patch

import psycopg2
import pytest
from pgtoolkit.ctl import Status
from tenacity import retry
from tenacity.retry import retry_if_exception_type
from tenacity.stop import stop_after_attempt
from tenacity.wait import wait_fixed

from pglift import databases, exceptions
from pglift import instance as instance_mod
from pglift import systemd
from pglift.ctx import Context
from pglift.models import interface, system
from pglift.settings import Settings

from . import configure_instance, execute, reconfigure_instance
from .conftest import DatabaseFactory


def test_init(
    ctx: Context, instance_initialized: system.Instance, monkeypatch: pytest.MonkeyPatch
) -> None:
    i = instance_initialized
    assert i.datadir.exists()
    assert i.waldir.exists()
    postgresql_conf = i.datadir / "postgresql.conf"
    assert postgresql_conf.exists()
    assert (i.waldir / "archive_status").is_dir()
    with postgresql_conf.open() as f:
        for line in f:
            if "lc_messages = 'C'" in line:
                break
        else:
            raise AssertionError("invalid postgresql.conf")

    if ctx.settings.service_manager == "systemd":
        assert systemd.is_enabled(ctx, instance_mod.systemd_unit(i))

    # Instance alread exists, no-op.
    with monkeypatch.context() as m:

        def fail() -> NoReturn:
            raise AssertionError("unexpected called")

        m.setattr(ctx, "pg_ctl", fail)
        instance_mod.init(ctx, interface.Instance(name=i.name, version=i.version))


def test_log_directory(
    ctx: Context, instance: system.Instance, log_directory: Path, redhat: bool
) -> None:
    if redhat:
        pytest.xfail("postgresql.conf on redhat contains 'log_directory' uncommented")
    config = instance.config()
    assert isinstance(config.log_directory, str)
    instance_log_dir = Path(config.log_directory)
    assert instance_log_dir == log_directory
    assert instance_log_dir.exists()


def test_pgpass(
    ctx: Context, instance_manifest: interface.Instance, instance: system.Instance
) -> None:
    port = instance.port
    passfile = ctx.settings.postgresql.auth.passfile
    if instance_manifest.surole_password and ctx.settings.postgresql.surole.pgpass:
        assert passfile.read_text().splitlines()[1:] == [f"*:{port}:*:postgres:s3kret"]

        with reconfigure_instance(ctx, instance, instance_manifest, port=port + 1):
            assert passfile.read_text().splitlines() == [
                "#hostname:port:database:username:password",
                f"*:{port+1}:*:postgres:s3kret",
            ]

        assert passfile.read_text().splitlines()[1:] == [f"*:{port}:*:postgres:s3kret"]


def test_auth(
    ctx: Context, instance_manifest: interface.Instance, instance: system.Instance
) -> None:
    i = instance
    surole = interface.instance_surole(ctx.settings, instance_manifest)
    port = i.port
    connargs = {
        "host": str(i.config().unix_socket_directories),
        "port": port,
        "user": surole.name,
    }

    passfile = ctx.settings.postgresql.auth.passfile

    password = None
    if surole.password:
        password = surole.password.get_secret_value()

    with instance_mod.running(ctx, i):
        if password is not None:
            with pytest.raises(psycopg2.OperationalError, match="no password supplied"):
                with patch.dict("os.environ", clear=True):
                    psycopg2.connect(**connargs).close()
            if password:
                connargs["password"] = password
            else:
                connargs["passfile"] = str(passfile)
        else:
            connargs["passfile"] = str(passfile)
        psycopg2.connect(**connargs).close()

    hba_path = i.datadir / "pg_hba.conf"
    hba = hba_path.read_text().splitlines()
    auth = ctx.settings.postgresql.auth
    assert (
        f"local   all             all                                     {auth.local}"
        in hba
    )
    assert (
        f"host    all             all             127.0.0.1/32            {auth.host}"
        in hba
    )

    ident_path = i.datadir / "pg_ident.conf"
    ident = ident_path.read_text().splitlines()
    assert ident == ["# MAPNAME       SYSTEM-USERNAME         PG-USERNAME"]


def test_start_stop_restart_running_stopped(
    ctx: Context,
    instance: system.Instance,
    tmp_path: Path,
    caplog: pytest.LogCaptureFixture,
) -> None:
    i = instance
    use_systemd = ctx.settings.service_manager == "systemd"
    if use_systemd:
        assert not systemd.is_active(ctx, instance_mod.systemd_unit(i))

    instance_mod.start(ctx, i)
    try:
        assert instance_mod.status(ctx, i) == Status.running
        if use_systemd:
            assert systemd.is_active(ctx, instance_mod.systemd_unit(i))
    finally:
        instance_mod.stop(ctx, i)

        # Stopping a non-running instance is a no-op.
        caplog.clear()
        with caplog.at_level(logging.WARNING, logger="pglift"):
            instance_mod.stop(ctx, i)
        assert f"instance {instance} is already stopped" in caplog.records[0].message

    assert instance_mod.status(ctx, i) == Status.not_running
    if use_systemd:
        assert not systemd.is_active(ctx, instance_mod.systemd_unit(i))

    instance_mod.start(ctx, i, logfile=tmp_path / "log", run_hooks=False)
    try:
        assert instance_mod.status(ctx, i) == Status.running
        if not use_systemd:
            # FIXME: systemctl restart would fail with:
            #   Start request repeated too quickly.
            #   Failed with result 'start-limit-hit'.
            instance_mod.restart(ctx, i)
            assert instance_mod.status(ctx, i) == Status.running
        instance_mod.reload(ctx, i)
        assert instance_mod.status(ctx, i) == Status.running
    finally:
        instance_mod.stop(ctx, i, mode="immediate", run_hooks=False)

    assert instance_mod.status(ctx, i) == Status.not_running
    with instance_mod.stopped(ctx, i):
        assert instance_mod.status(ctx, i) == Status.not_running
        with instance_mod.stopped(ctx, i):
            assert instance_mod.status(ctx, i) == Status.not_running
        with instance_mod.running(ctx, i):
            assert instance_mod.status(ctx, i) == Status.running
            with instance_mod.running(ctx, i):
                assert instance_mod.status(ctx, i) == Status.running
            with instance_mod.stopped(ctx, i):
                assert instance_mod.status(ctx, i) == Status.not_running
            assert instance_mod.status(ctx, i) == Status.running
        assert instance_mod.status(ctx, i) == Status.not_running
    assert instance_mod.status(ctx, i) == Status.not_running


def test_apply(
    ctx: Context, installed: None, tmp_path: Path, tmp_port_factory: Iterator[int]
) -> None:
    port = next(tmp_port_factory)
    prometheus_port = next(tmp_port_factory)
    im = interface.Instance(
        name="test_apply",
        port=port,
        ssl=True,
        state=interface.InstanceState.stopped,
        configuration={"unix_socket_directories": str(tmp_path)},
        prometheus={"port": prometheus_port},
    )
    r = instance_mod.apply(ctx, im)
    assert r is not None
    i, changes = r
    assert i is not None
    assert i.exists()
    assert i.port == port
    assert changes["port"] == (None, port)
    pgconfig = i.config()
    assert pgconfig
    assert pgconfig.ssl

    assert instance_mod.status(ctx, i) == Status.not_running
    im.state = interface.InstanceState.started
    r = instance_mod.apply(ctx, im)
    assert r is not None
    i, changes = r
    assert not changes
    assert instance_mod.status(ctx, i) == Status.running

    im.configuration["bonjour"] = False
    r = instance_mod.apply(ctx, im)
    assert r is not None
    i, changes = r
    assert changes == {"bonjour": (None, False)}
    assert instance_mod.status(ctx, i) == Status.running

    im.state = interface.InstanceState.stopped
    instance_mod.apply(ctx, im)
    assert instance_mod.status(ctx, i) == Status.not_running

    im.state = interface.InstanceState.absent
    r = instance_mod.apply(ctx, im)
    assert r is None
    with pytest.raises(exceptions.InstanceNotFound):
        i.exists()
    assert instance_mod.status(ctx, i) == Status.unspecified_datadir


def test_describe(
    ctx: Context, instance: system.Instance, log_directory: Path, redhat: bool
) -> None:
    im = instance_mod.describe(ctx, instance.name, instance.version)
    assert im is not None
    assert im.name == "test"
    config = im.configuration
    assert im.port == instance.port
    if "log_directory" in config:
        logdir = config.pop("log_directory")
        if not redhat:
            assert logdir == str(log_directory)
    assert config == {}
    assert im.state.name == "stopped"


def test_list(ctx: Context, instance: system.Instance) -> None:
    not_instance_dir = ctx.settings.postgresql.root / "12" / "notAnInstanceDir"
    not_instance_dir.mkdir(parents=True)
    try:
        instances = list(instance_mod.list(ctx))

        for i in instances:
            assert i.status == Status.not_running.name
            # this also ensure instance name is not notAnInstanceDir
            assert i.name == "test"

        for i in instances:
            if (i.version, i.name) == (instance.version, instance.name):
                break
        else:
            assert False, f"Instance {instance.version}/{instance.name} not found"

        with pytest.raises(ValueError, match="unknown version '7'"):
            next(instance_mod.list(ctx, version="7"))

        iv = next(instance_mod.list(ctx, version=instance.version))
        assert iv == i
    finally:
        not_instance_dir.rmdir()


@pytest.mark.parametrize("slot", ["standby", None], ids=["with-slot", "no-slot"])
def test_standby(
    ctx: Context,
    instance: system.Instance,
    instance_manifest: interface.Instance,
    settings: Settings,
    tmp_port_factory: Iterator[int],
    tmp_path_factory: pytest.TempPathFactory,
    pg_version: str,
    slot: str,
) -> None:
    socket_directory = instance.settings.postgresql.socket_directory
    surole = interface.instance_surole(settings, instance_manifest)
    standby_for = f"host={socket_directory} port={instance.port} user={surole.name}"
    if surole.password:
        standby_for += f" password={surole.password.get_secret_value()}"
    else:
        standby_for += f" passfile={settings.postgresql.auth.passfile}"
    standby_manifest = interface.Instance(
        name="standby",
        version=pg_version,
        standby=interface.Instance.Standby(**{"for": standby_for, "slot": slot}),
        surole_password=surole.password,
    )

    @contextlib.contextmanager
    def instance_running_with_table() -> Iterator[None]:
        with instance_mod.running(ctx, instance):
            execute(ctx, instance, "CREATE TABLE t AS (SELECT 1 AS i)", fetch=False)
            try:
                yield
            finally:
                execute(ctx, instance, "DROP TABLE t", fetch=False)

    def pg_replication_slots() -> List[List[str]]:
        return execute(ctx, instance, "SELECT slot_name FROM pg_replication_slots")

    with instance_running_with_table():
        assert not pg_replication_slots()
        instance_mod.init(ctx, standby_manifest)
        if slot:
            assert pg_replication_slots() == [[slot]]
        else:
            assert not pg_replication_slots()
        configure_instance(
            ctx,
            standby_manifest,
            port=next(tmp_port_factory),
            log_directory=str(tmp_path_factory.mktemp("postgres-standby-logs")),
        )
        standby_instance = system.Instance.system_lookup(ctx, ("standby", pg_version))
        assert standby_instance.standby
        assert standby_instance.standby.for_
        assert standby_instance.standby.slot == slot
        try:
            with instance_mod.running(ctx, standby_instance):
                assert execute(
                    ctx, standby_instance, "SELECT * FROM pg_is_in_recovery()"
                ) == [[True]]
                assert execute(ctx, standby_instance, "SELECT * FROM t") == [[1]]
                execute(ctx, instance, "UPDATE t SET i = 42", fetch=False)

                @retry(
                    retry=retry_if_exception_type(AssertionError),
                    wait=wait_fixed(1),
                    stop=stop_after_attempt(4),
                )
                def assert_replicated() -> None:
                    assert execute(ctx, standby_instance, "SELECT * FROM t") == [[42]]

                assert_replicated()

                instance_mod.promote(ctx, standby_instance)
                assert not standby_instance.standby
                assert execute(
                    ctx, standby_instance, "SELECT * FROM pg_is_in_recovery()"
                ) == [[False]]
        finally:
            if slot:
                execute(
                    ctx,
                    instance,
                    f"SELECT true FROM pg_drop_replication_slot('{slot}')",
                )
            assert not pg_replication_slots()
            instance_mod.drop(ctx, standby_instance)


def test_instance_upgrade(
    ctx: Context,
    instance: system.Instance,
    tmp_port_factory: Iterator[int],
    database_factory: DatabaseFactory,
) -> None:
    database_factory("present")
    port = next(tmp_port_factory)
    newinstance = instance_mod.upgrade(
        ctx,
        instance,
        name="test_upgrade",
        version=instance.version,
        port=port,
    )
    try:
        assert newinstance.name == "test_upgrade"
        assert newinstance.version == instance.version
        assert newinstance.port == port
        assert instance_mod.status(ctx, newinstance) == Status.not_running
        with instance_mod.running(ctx, newinstance):
            assert databases.exists(ctx, newinstance, "present")
    finally:
        instance_mod.drop(ctx, newinstance)
