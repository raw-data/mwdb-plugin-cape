# -*- coding: utf-8 -*-

from mwdb.core.plugins import PluginAppContext, PluginHookHandler
from mwdb.model import db, File, MetakeyDefinition
from .config import config
from typing import Type
import logging
import requests
import json

logger = logging.getLogger("mwdb.plugin.cape")


class CAPEHookHandler(PluginHookHandler):
    def on_created_file(self, file: File) -> None:
        """Send file to CAPEv2 for analysis

        Args:
            file (File): path to file being uploaded
        """

        contents_path = file.get_path()

        data = {"timeout": config.cape.timeout}

        if opt := config.cape.additional_analysis_options:
            try:
                json.loads(opt)
            except Exception:
                logger.error(
                    f"'additional_analysis_options' is invalid {config.cape.additional_analysis_options}, dictionary expected"
                )
                return
            else:
                data.update(json.loads(opt))

        res = requests.post(
            f"{config.cape.cape_url}/apiv2/tasks/create/file/",
            files={"file": (file.sha256, open(contents_path, "rb"))},
            data=data,
        )

        res.raise_for_status()

        if not res.json()["error"]:
            task_id = res.json()["data"]["task_ids"][0]
            logger.info(f"New task submitted to CAPEv2, task_id:{task_id}")

            if (
                config.cape.metakey_value
                and config.cape.metakey_value == "file_sha1"
            ):
                file.add_metakey(
                    "cape", str(file.sha1), check_permissions=False
                )
            else:
                file.add_metakey(
                    "cape", str(task_id), check_permissions=False
                )
        else:
            logger.error(
                "Error while creating CAPE task: %s" % res.json()["errors"]
            )


def entrypoint(app_context: PluginAppContext):
    """
    Register plugin hook handler.

    This will be called on app load.
    """
    app_context.register_hook_handler(CAPEHookHandler)


def configure():
    """
    Configure 'cape' attribute key in MWDB.

    This will be called by 'mwdb configure' command.
    """

    cape_url = config.cape.cape_url
    if config.cape.metakey_cape_url:
        cape_url = config.cape.metakey_cape_url
        
    url_template = (f"{cape_url}/submit/status/$value",)

    if (
        config.cape.metakey_value
        and config.cape.metakey_value == "file_sha1"
    ):
        url_template = (
            f"{cape_url}/analysis/search/$value",
        )

    logger.info("Configuring 'CAPEv2' attribute key.")
    attribute = MetakeyDefinition(
        key="cape",
        url_template=url_template,
        label="CAPEv2 analysis",
        description="Reference to the CAPEv2 file analysis",
    )
    db.session.merge(attribute)
    db.session.commit()
