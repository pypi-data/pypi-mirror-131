###############################################################################
# (c) Copyright 2021 CERN for the benefit of the LHCb Collaboration           #
#                                                                             #
# This software is distributed under the terms of the GNU General Public      #
# Licence version 3 (GPL Version 3), copied verbatim in the file "LICENSE".   #
#                                                                             #
# In applying this licence, CERN does not waive the privileges and immunities #
# granted to it by virtue of its status as an Intergovernmental Organization  #
# or submit itself to any jurisdiction.                                       #
###############################################################################
import json
from io import BytesIO
from itertools import chain
from typing import Any, BinaryIO, Optional, Union
from zipfile import ZipFile, ZipInfo

import requests
from lb.nightly.configuration import Project, Slot, lbnightly_settings


def _make_dir_zipinfo(dirname) -> ZipInfo:
    """
    Creates a ZipInfo object for a directory.
    """
    if not dirname.endswith("/"):
        dirname += "/"
    info = ZipInfo(dirname)
    info.external_attr = 0o40775 << 16  # this is a directory
    info.external_attr |= 0x10  # MS-DOS directory flag
    info.file_size = 0
    return info


def make_slot_deployment_dir(
    slot: Slot, file_object: Optional[BinaryIO] = None
) -> BinaryIO:
    """
    Creates a zip file with the contents of the deployment directory
    for the given slot, either in the specified file_object or in an in-memory
    BytesIO buffer.
    In either case the file_object is returned.
    """
    if file_object is None:
        file_object = BytesIO()

    with ZipFile(file_object, "w") as zip_file:
        # dump slot configuration in JSON format
        info = ZipInfo("slot-config.json")
        info.external_attr = 0o644 << 16  # we want the file world readable
        zip_file.writestr(info, json.dumps(slot.toDict(), indent=2, sort_keys=True))

        # create target directories
        for path in chain.from_iterable(
            (project.name, f"{project.name}/InstallArea/{platform}")
            for project in slot.projects
            for platform in slot.platforms
        ):
            zip_file.writestr(_make_dir_zipinfo(path), b"")

    file_object.seek(0)
    return file_object


def trigger_deployment(
    item: Union[Project, Slot],
    platform: Optional[str] = None,
) -> Any:
    """
    Makes a request to lbtask infrastructure to trigger installation
    of the deployment directory, sources or binaries.
    Returns json reponse content with the task id.
    """
    try:
        hook = lbnightly_settings().lbtask.hook
        token = lbnightly_settings().lbtask.token
        repo = lbnightly_settings().artifacts.uri
    except AttributeError as exc:
        raise RuntimeError(
            f"cannot trigger cache installation due to missing settings: {exc}"
        )
    if isinstance(item, Slot):
        # installing slot deployment directory
        req = requests.put(
            f"{hook}/{item.id()}/",
            params={"url": f"{repo}/{item.artifacts('deployment_dir')}"},
            headers={"Authorization": f"Bearer {token}"},
        )
    elif isinstance(item, Project):
        if platform:
            # which implies installing binaries
            req = requests.put(
                f"{hook}/{item.id()}/{platform}/",
                params={"url": f"{repo}/{item.artifacts('build', platform)}"},
                headers={"Authorization": f"Bearer {token}"},
            )
        else:
            # installing sources
            req = requests.put(
                f"{hook}/{item.id()}/",
                params={"url": f"{repo}/{item.artifacts('checkout')}"},
                headers={"Authorization": f"Bearer {token}"},
            )
    else:
        raise ValueError(
            f"Cannot trigger cache installation for {item} (of type: {type(item)}), which is neither Project nor Slot"
        )
    req.raise_for_status()
    return req.json()
