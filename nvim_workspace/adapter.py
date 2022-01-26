from glob import glob, iglob
from os import remove
from os.path import isdir
from pathlib import Path
from typing import List, Tuple

from pynvim import attach
from pynvim.api.nvim import Nvim


def get_nvim_sockets():
    sockets: List[str] = []
    for path in iglob("/tmp/nvim*"):
        if isdir(path):
            sockets += glob(path + "/*")
            continue
        sockets.append(path)

    return sockets


def connect_or_clear(sockets: List[str]):
    nvim_instances: List[Nvim] = []

    for socket in sockets:
        try:
            nvim = attach("socket", path=socket)
            nvim_instances.append(nvim)
            print(f"Connection succesful at {socket}")
        except:
            print(f"Couldn't connect to socket at {socket}, deleting.")
            remove(socket)

    return nvim_instances


def get_instances_working_directory(instances: List[Nvim]):
    instances_tuples: List[Tuple[Nvim, Path]] = []

    for instance in instances:
        instances_tuples.append((instance, Path(instance.funcs.getcwd()).absolute()))

    return instances_tuples
