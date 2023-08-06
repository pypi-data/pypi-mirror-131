# -*- coding: UTF-8 -*-
__author__ = 'Aki Mäkinen'

import sys
import logging
import urllib.parse
import requests
import json
import keyring
from keyring.errors import KeyringError, KeyringLocked, NoKeyringError
from copy import deepcopy
from ruamel.yaml import YAML
from git_workspace.configuration import read_configuration, write_configuration

yaml = YAML()

__SERVICE_NAME = "gitworkspace+gitlab"
__SECRET_NAME = "Personal Access Token"

def get_all_projects_in_a_group(gitlab_api_url, group_name="", include_subgroups=True, verify=False):
    page = 1
    projects = []

    if not group_name:
        url = f"{gitlab_api_url}/projects"
    else:
        url_encoded_group_name = urllib.parse.quote_plus(group_name)
        url = f"{gitlab_api_url}/groups/{url_encoded_group_name}/projects"

    try:
        api_token = keyring.get_password(__SERVICE_NAME, __SECRET_NAME)

    except (KeyringError, KeyringLocked, NoKeyringError):
        logging.info("Could not get the personal access token from the keyring.")

    if not api_token:
        api_token = input("Please insert the personal access token: ")
        while True:
            answer = input("Store the token to the keyring? (y or n): ")
            if answer in ["y", "Y"]:
                keyring.set_password(__SERVICE_NAME, __SECRET_NAME, api_token)
            elif answer in ["n", "N"]:
                pass
            else:
                continue
            break

    headers = {
        "Authorization": f"Bearer {api_token}"
    }
    while True:
        r = requests.get(f"{url}?page={page}&include_subgroups={include_subgroups}", headers=headers, verify=verify)
        logging.debug(f"Response status code: {r.status_code}")
        logging.debug("Response headers:")
        logging.debug(r.headers)
        if r.status_code == 200:
            logging.debug(f"Received {len(json.loads(r.content))} projects")
            projects += json.loads(r.content)
        elif r.status_code >= 400:
            logging.error(f"Received status code {r.status_code} from the server.")
            exit(1)
        else:
            logging.error(f"Received status code {r.status_code} from the server and I have no idea what to do, so... pass?")

        if not r.headers["X-Next-Page"]:
            break
        else:
            page = r.headers["X-Next-Page"]

    return projects

def sync_repositories(group_name, do_not_include_subgroups, flatten):
    conf = read_configuration()
    remote_conf = conf.get("remote", {})
    # if the remote is to use insecure, then the verification will be turned off
    verify = not remote_conf.get("insecure", False)
    api_url = remote_conf.get("api_url")
    if not api_url:
        logging.error("API URL is not set, unable to continue.")
        exit(1)
    include_subgroups = not do_not_include_subgroups
    projects = get_all_projects_in_a_group(api_url, group_name, include_subgroups, verify)
    new_configuration = deepcopy(conf)
    new_configuration["repositories"] = []
    for item in projects:
        if flatten:
            new_item = {
                "path": f"{item['path_with_namespace']}.git",
            }
        else:
            new_item = {
                "path": f"{item['path_with_namespace']}.git" ,
                "directory": item['path_with_namespace'],
            }

        new_item["default_branch"] = item["default_branch"]

        new_configuration["repositories"].append(new_item)

    print("\n\nThe new configuration: \n")
    yaml.indent(mapping=2, sequence=4, offset=2)
    yaml.dump(new_configuration, sys.stdout)
    print("\n")

    while True:
        answer = input("Save the new configuration? (y or n): ")
        if answer in ["y", "Y"]:
            write_configuration(new_configuration)
            print("New configuration saved")
        elif answer in ["n", "N"]:
            pass
        else:
            continue
        break
