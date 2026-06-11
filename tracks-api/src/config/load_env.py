"""
Load environment variables.
module: src/config/load_env.py
"""

import os


def get_env_or_secret(
    env_var: str, default: str | int | None = None
) -> str | int | None:
    """
    Get the value of an environment variable or read it from a file if it ends with _FILE.

    :param env_var: The variable name.
    :type env_var: str
    :param default: The default value of the variable.
    :type default: str | int | None
    :return: The variable value from the file or environment variable.
    :rtype: str | int | None
    """
    file_var = f"{env_var}_FILE"
    value = None
    if file_var in os.environ:
        # Read from file
        with open(os.environ[file_var], "r") as f:
            value = f.read().strip()
    else:
        # Read from environment variable
        value = os.getenv(env_var, default)
    return value
