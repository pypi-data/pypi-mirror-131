# @Time    : 2018/8/8 10:36
# @Author  : Niyoufa
import subprocess

def subprocess_popen(command):
    p = subprocess.Popen(command,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT
    )

    print("command start...")
    for line in p.stdout.readlines():
        print(line.decode())
    print("command end.")

    return p