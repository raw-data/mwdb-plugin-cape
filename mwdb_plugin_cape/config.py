# -*- coding: utf-8 -*-

from typedconfig import Config, group_key, key, section
from mwdb.core.config import AppConfig, app_config


@section("cape")
class CAPEPluginConfig(Config):

    cape_url = key(cast=str, required=True)
    metakey_cape_url = key(cast=str, required=False)
    metakey_value = key(cast=str, required=False)
    timeout = key(cast=int, required=False, default=500)
    additional_analysis_options = key(required=False)


class CAPEPluginAppConfig(AppConfig):

    cape = group_key(CAPEPluginConfig)


config = CAPEPluginAppConfig(provider=app_config.provider)
