# -*- coding: UTF-8 -*-
__author__ = 'Aki Mäkinen'
import logging
import os

from ruamel.yaml import YAML
from shutil import copyfile
from copy import deepcopy
yaml = YAML()

__WORKSPACE_FILE = ".workspace"
__WORKSPACE_GIT_CONFIGURATION = ".workspace-git-config"

__WORKSPACE_FILE_TEMPLATE = {
        "repositories": [],
        "remote": {
            "gituser": "",
            "githost": "",
            "api_url": "",
            "insecure": False
        }
    }

def migrate_to_v2():
    v2_configuration = deepcopy(__WORKSPACE_FILE_TEMPLATE)

    wsdir = search_workspace()

    original = os.path.join(wsdir, __WORKSPACE_FILE)
    backup = original + ".backup"
    copyfile(original, backup)

    with open(original, "r") as file:
        lines = file.readlines()

        for line in lines:
            cleaned = line.strip()
            v2_configuration["repositories"].append({
                "path": cleaned
            })

    with open(os.path.join(wsdir, __WORKSPACE_GIT_CONFIGURATION), "r") as file:
        lines = file.readlines()

        for line in lines:
            parts = line.strip().split("=")
            if parts[0] == "GITUSER":
                v2_configuration["remote"]["gituser"] = parts[1]
            elif parts[0] == "GITHOST":
                v2_configuration["remote"]["githost"] = parts[1]

    write_configuration(v2_configuration)

def search_workspace():
    directory = os.getcwd()
    while directory != "/":
        logging.debug(directory)
        if __WORKSPACE_FILE in os.listdir(directory):
            return directory
        directory = os.path.realpath(os.path.join(directory, ".."))
    return None

def init_workspace():
    workspacedir = search_workspace()
    if workspacedir is not None:
        print(f"Found a workspace from {workspacedir}, "
              f"will not continue as nested workspaces are not supported at the moment.")
        exit(1)
    empty_configuration = deepcopy(__WORKSPACE_FILE_TEMPLATE)
    write_configuration(empty_configuration)

def read_configuration():
    wsdir = search_workspace()
    with open(os.path.join(wsdir, __WORKSPACE_FILE), "r") as file:
        return yaml.load(file)

def write_configuration(conf):
    with open(__WORKSPACE_FILE, "w+") as configuration_file:
        yaml.indent(mapping=2, sequence=4, offset=2)
        yaml.dump(conf, configuration_file)