#!/usr/bin/python3
"""This script is used to create an archive file and deploy it to a
remote server using Fabric.
"""

# Import required modules.
from fabric.api import local
from datetime import datetime
from fabric.api import run, env, put
import os.path

# Define the remote server details.
env.hosts = ['18.207.234.171', '35.153.226.243']
env.key_filename = '~/.ssh/school'
env.user = 'ubuntu'


def do_pack():
    """
    Compress a file and return its path.
    """
    try:
        # Save the current timestamp and create a filename.
        time_now = datetime.now().strftime("%Y%m%d%H%M%S")
        file_path = "versions/web_static_{}.tgz".format(time_now)

        # Create a directory called versions.
        local("mkdir -p versions")

        # Create an archive file.
        local("tar -cvzf {} web_static/".format(file_path))

        # Return the path to the archive file created.
        return "{}".format(file_path)

    except Exception as e:
        # Return None if an error occurs.
        return None


def do_deploy(archive_path):
    """
    Deploy code and decompress it.
    """
    if not os.path.isfile(archive_path):
        # Return False if the file does not exist.
        return False

    # Get the filename and extension of the compressed file.
    compressed_file = archive_path.split("/")[-1]
    no_extension = compressed_file.split(".")[0]

    try:
        # Define the remote path and symbolic link.
        remote_path = "/data/web_static/releases/{}/".format(no_extension)
        sym_link = "/data/web_static/current"

        # Copy the archive to the remote server.
        put(archive_path, "/tmp/")

        # Create the remote directory.
        run("sudo mkdir -p {}".format(remote_path))

        # Extract the contents of the archive to the remote directory.
        run("sudo tar -xvzf /tmp/{} -C {}".format(compressed_file,
                                                  remote_path))

        # Remove the archive file from the remote server.
        run("sudo rm /tmp/{}".format(compressed_file))

        # Move the contents of the web_static directory to remote directory.
        run("sudo mv {}/web_static/* {}".format(remote_path, remote_path))

        # Remove the web_static directory from the remote directory.
        run("sudo rm -rf {}/web_static".format(remote_path))

        # Remove the symbolic link to the current version.
        run("sudo rm -rf /data/web_static/current")

        # Create a new symbolic link to the current version.
        run("sudo ln -sf {} {}".format(remote_path, sym_link))

        # Return True if successful.
        return True

    except Exception as e:
        # Return False if an error occurs.
        return False


def deploy():
    """
    Create and deploy an archive to a web server.
    """
    # Create the archive.
    file_path = do_pack()

    if file_path is None:
        # Return False if the archive creation fails.
        return False

    # Deploy the archive to the remote server.
    return do_deploy(file_path)
