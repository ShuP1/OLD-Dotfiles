#!/usr/bin/env python3
# coding=utf-8

"""
Auto-mounter for gvfs.

Automatically mounts specific removable media with uuid in args
Exemple: gvfs_automount.py <uuid> <uuid> ...
"""

import sys

from gi.repository import Gio
from gi.repository import GObject
from gi.repository import Notify

def on_volume_added(vm, volume, _):
    should_automount = volume.should_automount()
    uuid = volume.get_uuid()
    if should_automount:
        if uuid in sys.argv[1:]:
            mount_op = Gio.MountOperation()
            volume.mount(0, mount_op, None, on_volume_mounted, mount_op)

def on_volume_mounted(volume, async_result, mount_op):
    if volume.mount_finish(async_result):
        mount = volume.get_mount()
        label = mount.get_name()
        mount_path = mount.get_root().get_path()

        notification = Notify.Notification.new(
                "Volume mounted",
                "%s mounted at %s" % (label, mount_path),
                "dialog-information")
        notification.show()


class UserError(Exception):
    def __init__(self, message):
        self.message = message

def create_parser():
    description, epilog = __doc__.strip().split('\n', 1)
    parser = argparse.ArgumentParser(description=description, epilog=epilog,
            formatter_class=argparse.RawDescriptionHelpFormatter)
    return parser

if __name__ == '__main__':
    Notify.init ("gvfs-automount")
    vm = Gio.VolumeMonitor.get()
    connections = []
    connections.append(vm.connect("volume-added", on_volume_added, None))
    GObject.MainLoop().run()
