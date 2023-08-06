# -*- coding: utf-8 -*-
import subprocess
import sys


def subprocess_check_output(cmd, cwd="."):
    print(f"")
    print(f"{cmd}")
    res = subprocess.check_output(args=cmd, cwd=cwd, shell=True, stdin=subprocess.PIPE).decode("utf-8").strip('\n')
    print(f"{res}")
    print(f"")
    return res


if __name__ == "__main__":
    print("")
