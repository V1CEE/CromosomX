import os


def InsidePath(insidePath):
    return os.getcwd() + "\\" + insidePath


def FileDetect(insidePath):
    path = InsidePath(insidePath)
    return os.path.exists(path)


def FileDelete(insidePath):
    ip = InsidePath(insidePath)
    os.remove(ip)


def FileRename(old_ip, new_ip):
    os.rename(InsidePath(old_ip), InsidePath(new_ip))
