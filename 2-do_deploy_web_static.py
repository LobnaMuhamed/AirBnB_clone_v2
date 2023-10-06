#!/usr/bin/python3
"""
Compress web static package
"""
from fabric.api import env, put, run
import os

# Define the web server IP addresses
env.hosts = ['<IP web-01>', '<IP web-02>']


def do_deploy(archive_path):

    if not os.path.exists(archive_path):
        print("Archive file does not exist.")
        return False

    try:
        put(archive_path, "/tmp/")

        archive_filename = os.path.basename(archive_path)
        release_folder = "/data/web_static/releases/\
{}".format(os.path.splitext(archive_filename)[0])
        run("mkdir -p {}".format(release_folder))
        run("tar -xzf /tmp/{} -C {}".format(archive_filename, release_folder))
        run("rm /tmp/{}".format(archive_filename))

        run("mv {}/web_static/* {}/".format(release_folder, release_folder))
        run("rm -rf {}/web_static".format(release_folder))

        run("rm -rf /data/web_static/current")

        run("ln -s {} /data/web_static/current".format(release_folder))

        print("New version deployed!")
        return True

    except Exception as e:
        print("An error occurred during deployment:", str(e))
        return False
