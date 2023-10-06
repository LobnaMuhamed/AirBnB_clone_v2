#!/usr/bin/python3
"""
Compress web static package
"""
from fabric import Connection
from datetime import datetime
import os


env = {
    'host_string': '100.25.19.204',
    'user': 'ubuntu',
    'key_filename': '/path/to/private_key.pem'
}


def do_deploy(archive_path):
    """Deploys a web static package to a remote server."""

    if not os.path.isfile(archive_path):
        print("Archive file does not exist.")
        return False

    try:
        # Establish a connection to the remote server
        conn = Connection(env['host_string'],
                          user=env['user'],
                          connect_kwargs={'key_filename': env['key_filename']})

        # Get the current timestamp for the release folder
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")

        # Create the necessary directories
        conn.run('mkdir -p /data/web_static/releases/web_static_{}/'
                 .format(timestamp))
        conn.run('mkdir -p /data/web_static/shared/')

        # Upload the archive to the temporary folder on the server
        remote_archive_path = '/tmp/' + os.path.basename(archive_path)
        conn.put(archive_path, remote=remote_archive_path)

        # Extract the archive into the release folder
        conn.run('tar -xzf {} -C /data/web_static/releases/web_static_{}/'
                 .format(remote_archive_path, timestamp))

        # Remove the temporary archive
        conn.run('rm {}'.format(remote_archive_path))

        # Move the contents of the extracted folder to the release folder
        conn.run('mv /data/web_static/releases/web_static_{}/web_static/* \
/data/web_static/releases/web_static_{}/'.format(timestamp, timestamp))

        # Remove the now empty 'web_static' folder
        conn.run('rm -rf /data/web_static/releases/web_static_{}/web_static'
                 .format(timestamp))

        # Delete the old symbolic link if it exists
        conn.run('rm -rf /data/web_static/current')

        # Create a new symbolic link to the new release folder
        conn.run('ln -s /data/web_static/releases/web_static_{}/ \
/data/web_static/current'.format(timestamp))

        print("Deployment successful.")
        return True

    except Exception as e:
        print("An error occurred during deployment:", str(e))
        return False
