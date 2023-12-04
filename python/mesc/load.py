from __future__ import annotations
import json
import os

from .types import mesc_env_vars, RpcConfig
from . import exceptions
from . import overrides


def is_mesc_enabled() -> bool:
    for var in mesc_env_vars:
        if os.environ.get(var) not in [None, ""]:
            return True
    return False


def read_config_data() -> RpcConfig:
    mode = os.environ.get("MESC_CONFIG_MODE")
    if mode == "DISABLE":
        raise exceptions.MescDisabled("MESC disabled, check with is_mesc_enabled()")
    if mode == "PATH":
        config = read_file_config()
    elif mode == "ENV":
        config = read_env_config()
    elif mode not in ["", None]:
        raise Exception("invalid mode: " + str(mode))
    elif os.environ.get("MESC_CONFIG_PATH") not in ["", None]:
        config = read_file_config()
    elif os.environ.get("MESC_CONFIG_JSON") not in ["", None]:
        config = read_env_config()
    else:
        raise Exception("config not specified")

    config = overrides.apply_env_overrides(config)

    return config


def read_env_config() -> RpcConfig:
    return json.loads(os.environ.get("MESC_CONFIG_JSON"))  # type: ignore


def read_file_config() -> RpcConfig:
    with open(os.environ.get("MESC_CONFIG_PATH"), "r") as f:  # type: ignore
        return json.load(f)  # type: ignore