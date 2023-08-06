import requests
import os
import sys
import argparse
import shutil
import patchutils


def clone(url: str, dir: str):
    """
    clones a repository from the upstream named `url` into the
    directory named `dir`. It uses requests library to stream
    the data. Note native http based zip compression is not
    implemented but only rocktree's implementation of data
    compression is implemented.

    .. TODO::
        Data compression is not yet ready and has to be
        implemented for the feature versions.
    """
    # Create the root directory
    os.mkdir(dir)

    # Request for patchfile for getting the names of files to download.
    response = requests.post(
        url + "/v1/get_patch",
        json={"dirinfo": {"files": [], "directories": [], "hash": {}}},
    )
    response.raise_for_status()
    response = response.json()  # Because the data is in json format

    # For all the directories in the response create corresponding local directories
    for x in response["directories_added"]:
        os.makedirs(dir + "/" + x)

    # For all the files download them
    for x in response["files_added"]:
        # Stream files from the api endpoint
        with requests.get(url + f"/v1/download/{x}", stream=True) as r:
            r.raise_for_status()

            # Create a new file and use shutil's method copyfileobj for best
            # speed transfers of data but with the caveat of native http zip
            # being not supported this way.
            with open(dir + "/" + x, "wb") as f:
                shutil.copyfileobj(r.raw, f)

    # Add a .rocktree file
    with open(f"{dir}/.rocktree", "w") as f:
        f.write(url)


def update_from_file(dir: str):
    """
    Same as `update()` but takes the upstream url from the `.rocktree` file inside
    the repository.
    """
    # Read the url from the .rocktree file
    with open(f"{dir}/.rocktree") as f:
        url = f.read().strip()

    # Simply update using the update function.
    update(dir, url)


def update(dir: str, url: str):
    """
    Updates an existing repository inside the directory `dir` from the upstream
    `url`.
    """
    # Request for patchfile for getting the names of files to download against
    # the local copy of directory information
    response = requests.post(
        url + "/v1/get_patch",
        json={"dirinfo": patchutils.create_info_from_directory(dir)},
    )
    response.raise_for_status()
    response = response.json()  # Because the data is in json format

    # For all the new directories in the response create corresponding local directories
    for x in response["directories_added"]:
        os.makedirs(dir + "/" + x)

    # For all the files that are added or modified, download and write them
    for x in response["files_added"] + response["files_modified"]:
        # Stream files from the api endpoint
        with requests.get(url + f"/v1/download/{x}", stream=True) as r:
            r.raise_for_status()

            # Create a new file and use shutil's method copyfileobj for best
            # speed transfers of data but with the caveat of native http zip
            # being not supported this way.
            with open(dir + "/" + x, "wb") as f:
                shutil.copyfileobj(r.raw, f)

    # Remove all the removed files
    for x in response["files_removed"]:
        os.remove(dir + "/" + x)

    # Remove all the directories that were removed
    for x in response["directories_removed"]:
        try:
            shutil.rmtree(dir + "/" + x)
        except FileNotFoundError:
            pass

    # Rewrite the .rocktree to take the current url used
    with open(f"{dir}/.rocktree", "w") as f:
        f.write(url)


def main(args=None):
    """
    CLI Interface to the rocktree.py
    """
    # If args are not provided as function arguments then load from sys.argv
    if args is None:
        args = sys.argv[1:]

    # Create the parser and rest you can understand if you understand argparse.ArgumentParser which
    # is a part of standard library.
    parser = argparse.ArgumentParser(
        "rocktree",
        description="Rock Solid Trees (Directories) completely mirrored byte to byte.",
    )
    commands = parser.add_subparsers(dest="_command")
    # Command `rocktree clone`
    commands_clone = commands.add_parser(
        "clone", help="Download from upstream for the first time to a given directory"
    )
    commands_clone.add_argument(
        "-i", "--source", help="The url of the repository to clone from", required=True
    )
    commands_clone.add_argument(
        "directory", metavar="OUTPUT_DIRECTORY", help="Output directory to store to."
    )

    # Command `rocktree update`
    commands_update = commands.add_parser(
        "update", help="Update a directory from upstream discarding any manual changes"
    )
    commands_update_source = commands_update.add_mutually_exclusive_group(required=True)
    commands_update_source.add_argument(
        "-i",
        "--source",
        help="The url of the repository to update from",
    )
    commands_update_source.add_argument(
        "-r",
        "--rocktreefile",
        help="Read upstream url from .rocktree file",
        action="store_true",
    )
    commands_update.add_argument(
        "directory", metavar="UPDATE_DIRECTORY", help="Directory to update to"
    )

    # Finally parse the argument and move on to the tree of subcommands.
    args = parser.parse_args(args)
    if args._command == "clone":  # On clone
        clone(args.source, args.directory)
    if args._command == "update":  # On update
        if args.rocktreefile:
            update_from_file(args.directory)
        else:
            update(args.directory, args.source)


if __name__ == "__main__":
    main()
