import json
from os import listdir
from os.path import abspath
from os.path import join
from pathlib import Path
from typing import Any
from typing import Optional

import progressbar
from dateutil.parser import parse
from git import Repo
from loguru import logger
from progressbar import ProgressBar

from fastapi_web_app.config import get_db_path
from fastapi_web_app.data.db_session import create_session
from fastapi_web_app.data.db_session import global_init
from fastapi_web_app.data.package import Package
from fastapi_web_app.data.release import Release
from fastapi_web_app.data.user import User


def main() -> None:
    init_db()
    session = create_session()
    user_count = session.query(User).count()
    session.close()
    if user_count == 0:
        file_data = do_load_files()
        users = find_users(file_data)

        db_users = do_user_import(users)
        do_import_packages(file_data, db_users)

    do_summary()


def do_summary() -> None:
    session = create_session()

    logger.info("Final numbers:")
    logger.info(f"Users: {session.query(User).count():,}")
    logger.info(f"Packages: {session.query(Package).count():,}")
    logger.info(f"Releases: {session.query(Release).count():,}")


def do_user_import(user_lookup: dict[str, str]) -> dict[str, User]:
    logger.info("Importing users ... ")
    with ProgressBar(max_value=len(user_lookup)) as bar:
        for idx, (email, name) in enumerate(user_lookup.items()):
            session = create_session()
            session.expire_on_commit = False

            user = User()
            user.email = email
            user.name = name
            session.add(user)

            session.commit()
            bar.update(idx)

    session = create_session()
    return {u.email: u for u in session.query(User)}


def do_import_packages(
    file_data: list[dict], user_lookup: dict[str, User]
) -> Any:
    errored_packages = []
    logger.info("Importing packages and releases ... ")
    with ProgressBar(max_value=len(file_data)) as bar:
        for idx, p in enumerate(file_data):
            try:
                load_package(p, user_lookup)
                bar.update(idx)
            except Exception as x:
                errored_packages.append(
                    (
                        p,
                        " *** Errored out for package {}, {}".format(
                            p.get("package_name"), x
                        ),
                    )
                )
                raise
    logger.info(f"Completed packages with {len(errored_packages)} errors.")
    for (_, txt) in errored_packages:
        logger.error(txt)


def do_load_files() -> list[dict]:
    data_path_p = Path(
        Repo(".", search_parent_directories=True).working_tree_dir,
        "official-repo",
        "data",
        "pypi-top-100",
    )
    data_path = str(data_path_p)
    logger.info(f"Loading files from {data_path}")
    files = get_file_names(data_path)
    logger.info(f"Found {len(files):,} files, loading ...")

    file_data = []
    with ProgressBar(max_value=len(files)) as bar:
        for idx, f in enumerate(files):
            file_data.append(load_file_data(f))
            bar.update(idx)

    return file_data


def find_users(data: list[dict]) -> dict:
    logger.info("Discovering users...")
    found_users = {}

    with progressbar.ProgressBar(max_value=len(data)) as bar:
        for idx, p in enumerate(data):
            info = p.get("info")
            found_users.update(
                get_email_and_name_from_text(
                    info.get("author"), info.get("author_email")
                )
            )
            found_users.update(
                get_email_and_name_from_text(
                    info.get("maintainer"), info.get("maintainer_email")
                )
            )
            bar.update(idx)

    logger.info(f"Discovered {len(found_users):,} users")
    return found_users


def get_email_and_name_from_text(name: str, email: str) -> dict:
    data = {}

    if not name or not email:
        return data

    emails = email.strip().lower().split(",")
    names = name
    if len(email) > 1:
        names = name.strip().split(",")

    for n, e in zip(names, emails):
        if not n or not e:
            continue

        data[e.strip()] = n.strip()

    return data


def load_file_data(filename: str) -> dict:
    try:
        with open(filename, encoding="utf-8") as fin:
            data = json.load(fin)
    except Exception as x:
        logger.error(f"ERROR in file: {filename}, details: {x}")
        raise

    return data


def load_package(data: dict, user_lookup: dict[str, User]) -> Any:  # noqa: U100
    try:
        info = data.get("info", {})

        p = Package()
        p.id = data.get("package_name", "").strip()
        if not p.id:
            return

        p.author = info.get("author")
        p.author_email = info.get("author_email")  # type: ignore

        releases = build_releases(p.id, data.get("releases", {}))

        if releases:
            p.created_date = releases[0].created_date

        maintainers = []

        p.summary = info.get("summary")  # type: ignore
        p.description = info.get("description")  # type: ignore

        p.home_page = info.get("home_page")  # type: ignore
        p.docs_url = info.get("docs_url")  # type: ignore
        p.package_url = info.get("package_url")  # type: ignore

        p.author = info.get("author")  # type: ignore
        p.author_email = info.get("author_email")  # type: ignore
        p.license = detect_license(info.get("license"))  # type: ignore

        session = create_session()
        session.add(p)
        session.add_all(releases)
        if maintainers:
            session.add_all(maintainers)
        session.commit()
        session.close()
    except OverflowError:
        # What the heck, people just putting fake data in here
        # Size is terabytes...
        pass
    except Exception:
        raise


def detect_license(license_text: str) -> Optional[str]:
    if not license_text:
        return None

    license_text = license_text.strip()

    if len(license_text) > 100 or "\n" in license_text:
        return "CUSTOM"

    license_text = license_text.replace("Software License", "").replace(
        "License", ""
    )

    if "::" in license_text:
        # E.g. 'License :: OSI Approved :: Apache Software License'
        return license_text.split(":")[-1].replace("  ", " ").strip()

    return license_text.strip()


def build_releases(package_id: str, releases: dict) -> list[Release]:
    db_releases = []
    for k in releases.keys():
        all_releases_for_version = releases.get(k)
        if not all_releases_for_version:
            continue

        v = all_releases_for_version[-1]

        r = Release()
        r.package_id = package_id
        r.major_ver, r.minor_ver, r.build_ver = make_version_num(k)
        r.created_date = parse(v.get("upload_time"))
        r.comment = v.get("comment_text")
        r.url = v.get("url")
        r.size = int(v.get("size", 0))

        db_releases.append(r)

    return db_releases


def make_version_num(version_text: str) -> tuple[int, int, int]:
    major, minor, build = 0, 0, 0
    if version_text:
        version_text = version_text.split("b")[0]
        parts = version_text.split(".")
        if len(parts) == 1:
            major = try_int(parts[0])
        elif len(parts) == 2:
            major = try_int(parts[0])
            minor = try_int(parts[1])
        elif len(parts) == 3:
            major = try_int(parts[0])
            minor = try_int(parts[1])
            build = try_int(parts[2])

    return major, minor, build


def try_int(text: str) -> int:
    try:
        return int(text)
    except (ValueError, TypeError):
        return 0


def init_db() -> None:
    global_init(get_db_path())


def get_file_names(data_path: str) -> list[str]:
    files = []
    for f in listdir(data_path):
        if f.endswith(".json"):
            files.append(abspath(join(data_path, f)))

    files.sort()
    return files


if __name__ == "__main__":
    main()
