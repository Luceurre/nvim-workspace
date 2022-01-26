from pathlib import Path
from typing import List, Tuple

from pynvim.api.nvim import Nvim

from .adapter import (connect_or_clear, get_instances_working_directory,
                      get_nvim_sockets)
from .cli import parser


def get_targeted_nvim_client(nvim_workspaces: List[Tuple[Nvim, Path]], target: Path):
    for nvim_workspace in nvim_workspaces:
        if str(target).startswith(str(nvim_workspace[1])):
            return nvim_workspace


def open():
    args = parser.parse_args()
    absolute_file_path = Path(args.file).absolute()

    nvim_sockets = get_nvim_sockets()
    nvim_clients = connect_or_clear(nvim_sockets)
    nvim_workspaces = get_instances_working_directory(nvim_clients)
    target_client = get_targeted_nvim_client(nvim_workspaces, absolute_file_path)

    if not target_client:
        print(f"No suitable client found for {args.file}")
        exit(1)

    target_client[0].funcs.execute(f"edit {str(absolute_file_path)}")


if __name__ == "__main__":
    open()
