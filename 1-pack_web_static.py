#!/usr/bin/python3
"""Generates a .tgz archive from the contents of the web_static folder."""
from fabric.api import local
from datetime import datetime


def do_pack():
    """Generates a .tgz archive from the contents of the web_static folder."""

    # Get the current timestamp
    now = datetime.now()
    timestamp = now.strftime("%Y%m%d%H%M%S")

    try:
        local("mkdir -p versions")

        archive_name = "web_static_{}.tgz".format(timestamp)
        local("tar -czvf versions/{} web_static".format(archive_name))

        return "versions/{}".format(archive_name)

    except Exception as e:
        return None
