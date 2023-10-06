#!/usr/bin/python3

from fabric.api import *
from fabric.contrib.files import exists

env.hosts = ['100.25.19.204', '54.157.159.85']
"""
Delete out-of-date archives.
"""


def do_clean(number=0):
    number = int(number)
    keep = number if number > 0 else 1

    with lcd("versions"):
        local_archives = sorted(os.listdir("."))
        local_archives_to_delete = local_archives[:-keep]
        local("rm -f {}".format(" ".join(local_archives_to_delete)))

    with cd("/data/web_static/releases"):
        remote_archives = run("ls -t | grep web_static_").split()
        remote_archives_to_delete = remote_archives[:-keep]
        [run("rm -rf {}"
             .format(arch)) for arch in remote_archives_to_delete]

    if number <= 0:
        with cd("/data/web_static"):
            if exists("current") and not run("ls -l current").failed:
                run("rm current")
                run("ln -s releases/{}/ web_static"
                    .format(remote_archives[-1]))
