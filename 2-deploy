#!/usr/bin/python3
"""A fabric script to send an archive file to a remote server
and decompress it
"""
import os.path
from fabric.api import env, put, run

env.hosts = ["18.207.234.171", "35.153.226.243"]


def do_deploy(archive_path):
    """
    Distributes an archive to a web server.

    Args:
        archive_path (str): The path of the archive to distribute.

    Returns:
        bool: True if successful, False otherwise.
    """

    # Check if the file exists at the specified path.
    if os.path.isfile(archive_path) is False:
        return False

    # Extract the file name and the name of the project from the file path.
    file = archive_path.split("/")[-1]
    name = file.split(".")[0]

    # Copy the archive to the web server's /tmp/ directory.
    if put(archive_path, "/tmp/{}".format(file)).failed is True:
        return False

    # Remove the previous release of the project.
    if run("rm -rf /data/web_static/releases/{}/".format(name)).failed is True:
        return False

    # Create a new directory for the new release of the project.
    if run("mkdir -p /data/web_static/releases/{}/".format(name)).failed is True:
        return False

    # Extract the archive to the new directory.
    if run("tar -xzf /tmp/{} -C /data/web_static/releases/{}/".format(file, name)).failed is True:
        return False

    # Remove the archive from the /tmp/ directory.
    if run("rm /tmp/{}".format(file)).failed is True:
        return False

    # Move the project files from the subdirectory to the main directory.
    if run("mv /data/web_static/releases/{}/web_static/* /data/web_static/releases/{}/".format(name, name)).failed is True:
        return False

    # Remove the subdirectory.
    if run("rm -rf /data/web_static/releases/{}/web_static".format(name)).failed is True:
        return False

    # Remove the symbolic link /data/web_static/current.
    if run("rm -rf /data/web_static/current").failed is True:
        return False

    # Create a new symbolic link pointing to the new release of the project.
    if run("ln -s /data/web_static/releases/{}/ /data/web_static/current".format(name)).failed is True:
        return False

    # If all the above operations succeed, return True.
    return True
