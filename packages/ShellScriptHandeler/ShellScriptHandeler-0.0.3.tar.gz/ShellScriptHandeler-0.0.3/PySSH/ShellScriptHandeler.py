import subprocess, os

class Basic():
    def __init__(self) -> None:
        pass

    def open(self, displayPath):
        shellscript = subprocess.Popen([displayPath], shell=True, stdin=subprocess.PIPE )
        shellscript.stdin.write('yes\n'.encode("utf-8"))
        shellscript.stdin.close()
        returncode = shellscript.wait()