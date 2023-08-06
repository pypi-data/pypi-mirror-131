"""Module with various tools."""
import os
import json
from typing import Any, List, Dict, Literal, Callable, Union, Tuple

import yaml

from .logger import logger


# Yaml loaders types according to https://github.com/yaml/pyyaml/wiki/PyYAML-yaml.load(input)-Deprecation.
YamlLoader = Literal["base", "safe", "full", "unsafe"]


@logger.catch
def join_paths(*args) -> str:
    """Collect given paths and return summary joined absolute path.
    
    Also calculate logic for `./` starting path, consider it as "from me" relative point."""
    summary_path = ""
    for path in args:
        # Check if path starts from slash, to remove it to avoid errors.
        if path[0] == "/": 
            path = path[1:]
        # Check if path given in logical form (starts from "./").
        elif path[:2] == "./":  
            path = path[2:]  # Remove leading "./" to perform proper paths joining.
        # Check if path ends with slash, to remove it to avoid errors.
        if path[len(path)-1] == "/":
            path = path[:len(path)-1]
        summary_path += "/" + path
    return summary_path


@logger.catch
def dump_json_to_environ(environ_key: str, map_to_dump: Union[List, Dict, Tuple]) -> None:
    """Dump given map with converting to json to environment variable by given key."""
    os.environ[environ_key] = json.dumps(map_to_dump)


@logger.catch
def load_json_from_environ(environ_key: str) -> Dict[str, Any]:
    """Load json with converting to Python's map object from environment variable by given key and return data dictionary."""
    return json.loads(os.environ[environ_key])


@logger.catch
def save_yaml(file_path: str, data: dict) -> None:
    """Save given dict to yaml to file on given path.
    
    Args:
        file_path: Path of yaml file to load from.
        data: Dictionary to be converted and saved.
    """
    with open(file_path, "w") as file:
        yaml.dump(data=data, stream=file, allow_unicode=True)


@logger.catch
def load_yaml(file_path: str, *, loader: YamlLoader = "safe") -> Dict[str, Any]:
    """Load yaml from file on given path and return Python dict.
    
    Args:
        file_path: Path of yaml file to load from.
        loader: Loader for yaml according to [load deprecation](https://github.com/yaml/pyyaml/wiki/PyYAML-yaml.load(input)-Deprecation).
        
    Raise:
        ValueError: If given loader is not in yaml loaders list.
    """
    # Define yaml loader according to given argument.
    if loader == "safe":
        yaml_loader = yaml.SafeLoader
    elif loader == "full":
        yaml_loader = yaml.FullLoader
    elif loader == "base":
        yaml_loader = yaml.BaseLoader
    elif loader == "unsafe":
        yaml_loader = yaml.UnsafeLoader
    else:
        message = format_message("Couldn't recognize given loader {}.", loader)
        raise ValueError(message)

    # Open file by given path and load yaml.
    with open(file_path, "r") as file:
        return yaml.load(file, Loader=yaml_loader)


@logger.catch
def format_message(text: str, *args, no_arg_phrase: str = "None", enclosing_char: str = "`") -> str:
    """Construct message from given text with inserting given args to it and return resulting message.
    
    Args:
        text: Main message text with formatting brackets `{}`.
        args: Positional args ordered for according formatting brackets. Given lists will be also unpacked.
        no_arg_phrase: Text to insert to position of arg with `None` value instead it. Defaults to `"None"`.
        enclosing_char: 
            Char to enclose every given argument in text from both sides for differentiation. 
            If set to `None`, don't perform enclosing. 
            Defaults to single backtick.

    Raise:
        ValueError: If given text has different number of braces than amount of given arguments.
    """
    vars_to_format = []
    for arg in args:
        if isinstance(arg, list):
            if not bool(arg): # Empty mapping, no need to unpack.
                vars_to_format.append(no_arg_phrase)
            for _arg in arg:
                if _arg is None or (not bool(_arg) and not isinstance(_arg, int)):
                    vars_to_format.append(no_arg_phrase)
                else:
                    vars_to_format.append(_arg)
        elif arg is None or (not bool(arg) and not isinstance(arg, int)):
            vars_to_format.append(no_arg_phrase)
        else:
            vars_to_format.append(arg)
    
    # Check if text with correct number of braces given.
    if text.count("{}") != len(vars_to_format):
        raise ValueError(f"Text `{text}` has different number of braces than amount of given arguments: `{vars_to_format}`.")

    # Apply enclosing char to every var.
    if enclosing_char is not None:
        enclosed_vars_to_format = []
        for var in vars_to_format:
            enclosed_vars_to_format.append(str(enclosing_char) + str(var) + str(enclosing_char))

    message = text.format(*enclosed_vars_to_format)
    return message


@logger.catch
def get_next_dict_key(dictionary: dict) -> str:
    """Return next key in dictionary by using its iterator."""
    return next(iter(dictionary.keys()))


@logger.catch
def normalize_db_uri(cpas_module_path: str, raw_db_uri: str) -> str:
    """Normalize given db (i.e. convert rel paths to abs and check for errors) uri and return it."""
    if ":memory:" in raw_db_uri:
        return "sqlite:///:memory:"
    db_name, db_rel_path = raw_db_uri.split("://")
    if db_name == "sqlite":
        db_path = join_paths(cpas_module_path, db_rel_path)
        db_uri = db_name + ":///" + db_path  # It is necessary to set ":///" in sqlite3 abs paths
        return db_uri
    elif db_name == "postgresql":
        error_message = format_message("PostgreSQL database temporarily not supported.")
        raise ValueError(error_message)
    else:
        error_message = format_message("Couldn't recognize database name: {}", db_name)
        raise ValueError(error_message)


# Don't use `@logger.catch` at function below, since error should be propagated to caller function and catched there, 
# because errors occured here carries more exceptional sence.
def get_or_error(object_to_return: Any) -> Any:
    """Return given object after checking.
    
    Raise:
        TypeError: If given object is None.
        TypeError: If given object is empty mapping."""
    if object_to_return is None:
        error_message = format_message("Requested object is None.")
        raise TypeError(error_message)
    elif isinstance(object_to_return, (list, dict, tuple, set)) and not object_to_return:
        error_message = format_message("Requested object is empty mapping: {}.", object_to_return)
        raise TypeError(error_message)
    return object_to_return
