import datetime
import json
import os
import pathlib
import secrets
import socket
import string
import subprocess
from typing import Callable, Iterator

import dateutil.tz
import psycopg2
import pytest
import yaml

from pglift import db

PLAYDIR = pathlib.Path(__file__).parent.parent.parent / "docs" / "ansible"


def generate_secret(length: int) -> str:
    return "".join(
        secrets.choice(string.ascii_letters + string.digits) for i in range(length)
    )


@pytest.fixture
def call_playbook(tmp_path: pathlib.Path) -> Iterator[Callable[[pathlib.Path], None]]:
    env = os.environ.copy()
    env["ANSIBLE_COLLECTIONS_PATH"] = str(
        pathlib.Path(__file__).parent.parent.parent / "ansible"
    )
    env["ANSIBLE_VERBOSITY"] = "3"
    settings = {
        "prefix": str(tmp_path),
        "postgresql": {
            "auth": {
                "local": "md5",
                "host": "md5",
                "passfile": str(tmp_path / "pgpass"),
            },
            "surole": {"pgpass": True},
            "root": str(tmp_path / "postgresql"),
        },
    }
    with (tmp_path / "config.json").open("w") as f:
        json.dump(settings, f)
    env["SETTINGS"] = f"@{tmp_path / 'config.json'}"

    with (tmp_path / "vault-pass").open("w") as f:
        f.write(generate_secret(32))
    env["ANSIBLE_VAULT_PASSWORD_FILE"] = str(tmp_path / "vault-pass")

    with (tmp_path / "vars").open("w") as f:
        passwords = {
            "postgresql_surole_password": "supers3kret",
            "prod_bob_password": "s3kret",
        }
        yaml.dump(passwords, f)
    subprocess.check_call(["ansible-vault", "encrypt", str(tmp_path / "vars")], env=env)

    def call(playfile: pathlib.Path) -> None:
        subprocess.check_call(
            [
                "ansible-playbook",
                "--extra-vars",
                f'@{tmp_path / "vars"}',
                str(playfile),
            ],
            env=env,
        )

    yield call
    call(PLAYDIR / "play3.yml")
    assert not (tmp_path / "pgpass").exists()


def cluster_name(dsn: str) -> str:
    with db.connect_dsn(dsn) as cnx:
        with cnx.cursor() as cur:
            cur.execute("SELECT setting FROM pg_settings WHERE name = 'cluster_name'")
            name = cur.fetchall()[0][0]
            assert isinstance(name, str), name
            return name


def test_ansible(
    tmp_path: pathlib.Path, call_playbook: Callable[[pathlib.Path], None]
) -> None:
    call_playbook(PLAYDIR / "play1.yml")

    prod_dsn = "host=/tmp user=postgres password=supers3kret dbname=postgres port=5433"
    assert cluster_name(prod_dsn) == "prod"
    with db.connect_dsn(prod_dsn) as cnx:
        with cnx.cursor() as cur:
            cur.execute(
                "SELECT rolname,rolinherit,rolcanlogin,rolconnlimit,rolpassword,rolvaliduntil FROM pg_roles WHERE rolname = 'bob'"
            )
            assert cur.fetchall() == [
                [
                    "bob",
                    True,
                    True,
                    10,
                    "********",
                    datetime.datetime(2025, 1, 1, tzinfo=dateutil.tz.tzlocal()),
                ]
            ]
            cur.execute(
                "SELECT r.rolname AS role, ARRAY_AGG(m.rolname) AS member_of FROM pg_auth_members JOIN pg_authid m ON pg_auth_members.roleid = m.oid JOIN pg_authid r ON pg_auth_members.member = r.oid GROUP BY r.rolname"
            )
            assert cur.fetchall() == [
                ["bob", ["pg_read_all_stats", "pg_signal_backend"]],
                [
                    "pg_monitor",
                    [
                        "pg_read_all_settings",
                        "pg_read_all_stats",
                        "pg_stat_scan_tables",
                    ],
                ],
            ]

    socket.create_connection(("localhost", 9186), 1)

    # test connection with bob to the db database
    with db.connect_dsn("host=/tmp user=bob password=s3kret dbname=db port=5433"):
        pass

    # check preprod cluster & postgres_exporter
    preprod_dsn = (
        "host=/tmp user=postgres password=supers3kret dbname=postgres port=5434"
    )
    assert cluster_name(preprod_dsn) == "preprod"
    socket.create_connection(("localhost", 9188), 1)

    # check dev cluster & postgres_exporter are stopped
    with pytest.raises(psycopg2.OperationalError, match="No such file or directory"):
        cluster_name(
            "host=/tmp user=postgres password=supers3kret dbname=postgres port=5444"
        )

    # check dev postgres_exporter is stopped
    with pytest.raises(ConnectionRefusedError):
        socket.create_connection(("localhost", 9189), 1)

    call_playbook(PLAYDIR / "play2.yml")

    # prod running
    assert cluster_name(prod_dsn) == "prod"
    # bob user and db database no longer exists
    with pytest.raises(
        psycopg2.OperationalError, match='password authentication failed for user "bob"'
    ):
        with db.connect_dsn(
            "host=/tmp user=bob password=s3kret dbname=template1 port=5433"
        ):
            pass
    with pytest.raises(psycopg2.OperationalError, match='database "db" does not exist'):
        with db.connect_dsn(
            "host=/tmp user=postgres password=supers3kret dbname=db port=5433"
        ):
            pass

    # preprod stopped
    with pytest.raises(psycopg2.OperationalError, match="No such file or directory"):
        assert cluster_name(preprod_dsn) == "preprod"
    with pytest.raises(ConnectionRefusedError):
        socket.create_connection(("localhost", 9188), 1)

    # dev running
    dev_dsn = "host=/tmp user=postgres password=supers3kret dbname=postgres port=5455"
    assert cluster_name(dev_dsn) == "dev"
    socket.create_connection(("localhost", 9189))
