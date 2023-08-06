# Git Workspace

This script is intended to ease the development in multirepo environment. By defining a workspace file
that contains all the repositories one can easily share the environment setup without the need for manual
git clones. With git configuration user and host can also be set for the repositories. This allows one
to use e.g. multiple bitbucket repositories with different SSH keys easily without altering the host in
each git clone command.

This script also provides a command to check the overall state of the workspace (branches, untracked files etc.).
Few commands are overridden, but most are plain passthroughs to git and are run in all of the workspace
repositories.

### Installation:

```shell
pip install --user git-workspace
```
or
```shell
pip3 install git-workspace
```

### Usage

At first, create a new directory where the workspace will be initialized. There, run `git ws init` which creates a blank configuration. Fill in at least the remote configuration (examples later in this README).

For the repositories, fill those either by hand or if using Gitlab, you can use `git ws gitlab-sync` to automatically create a repository list either for a single group (and its subgroups) or for all that you have access to. `gitlab-sync` requires you to create a personal access token with Gitlab REST API access rights and supports only v4 API. The token can be saved to the systems secret storage (for details see Keyring python package documentation, but at least KWallet in KDE and Keychain in MacOS are supported). If stored, then the API TOKEN does not need to be filled in later on.

> NOTICE: Right now, only a single token can be used. Support for multiple different tokens coming soon-ish.

#### Command helps
```
Usage: git-ws [OPTIONS] COMMAND [ARGS]...

  Git Workspace

  Copyright 2021 Aki Mäkinen
  https://gitlab.com/blissfulreboot/python/git-workspace
  Licensed under MIT license

Options:
  --help  Show this message and exit.

Commands:
  clone               Clone the repositories listed in the workspace...
  command             Run a command in each workspace git directory
  default-and-update  Stash potential changes, switch to the default...
  gitlab-sync         Sync the workspace to match the state of the gitlab...
  graphops            Graphops commands
  init                Initialize a new blank workspace
  state               Print the state of the repositories in the workspace

```

```
Usage: git ws graphops [OPTIONS] COMMAND [ARGS]...

  Graphops commands

Options:
  --help  Show this message and exit.

Commands:
  list-operations  List all available graphops operations
  run
  simulate         Run simulation of the operation pipeline
  visualize

```

#### Configuration

In contrast to the first version of this tool, the configuration resides now in a single YAML file. The format is:

```yaml
repositories: []
remote:
  gituser: ''
  githost: ''
  api_url: ''
  insecure: false
```
where the repository entries are

```yaml
- path: some/repository/path.git 
  directory: some/repository/path
  default_branch: main
```

If the directory is defined for the repository entry, then the repository will be cloned there, otherwise the structure will be flattened. The default branch is used for the `git ws state` currently and defaults to `main` if not defined.

Example:

```yaml
# The remote configuration for gitlab.com using ssh (which is the only officially supported right now)
repositories: []
remote:
  gituser: git
  githost: gitlab.com
  api_url: https://gitlab.com/api/v4/
  insecure: false
```

### Graphops

This is an experimental feature. 

Graphops in this context are executable graphs. These graphs are defined by creating `.graphops` files into repository roots and defining operations there. These operations are connected by the name, e.g. all `deploy` operations would define together a single `deploy` graphops pipeline. Requirements are that the script in the configuration is an executable script file and that the graph ia a directed acyclic graph.

Example:

```      
{
  "deploy": {
    "script": "foobar3.sh",
    "requires": ["a", "b"],
    "environment": {
      "somekey": "somevalue"
    }
  }
}
```

In the future, YAML support will be added for the .graphops files and likely the JSON format is phased out. The reason for this is that YAML is friendlier for humans.