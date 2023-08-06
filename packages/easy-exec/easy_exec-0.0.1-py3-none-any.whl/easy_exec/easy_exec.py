import shlex
import subprocess

def exec(command, cwd=None):
    if isinstance(command, str):
        command = shlex.split(command)
    res = subprocess.run(
        command, 
        cwd=cwd,
        stdout=subprocess.PIPE, 
        stderr=subprocess.PIPE, 
        check=False)
    has_error = res.returncode != 0
    return res.stdout.decode(), res.stderr.decode(), has_error