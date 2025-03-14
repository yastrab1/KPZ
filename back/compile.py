import os
import subprocess
import re
import tempfile
import shutil

# Map module names to pip package names
module_to_pip = {
    'cv2': 'opencv-python',
    'numpy': 'numpy',
    'segno': 'segno',
    'requests': 'requests',
    'datetime': 'datetime',
}

python_std_lib_modules = [
    "__future__", "abc", "aifc", "argparse", "array", "ast", "asynchat", "asyncio", "asyncore", "atexit",
    "audioop", "base64", "bdb", "binascii", "binhex", "bisect", "builtins", "bz2", "calendar", "cgi",
    "cgitb", "chunk", "cmath", "cmd", "code", "codecs", "codeop", "collections", "colorsys", "compileall",
    "concurrent", "configparser", "contextlib", "contextvars", "copy", "copyreg", "crypt", "csv", "ctypes",
    "curses", "dataclasses", "datetime", "dbm", "decimal", "difflib", "dis", "distutils", "doctest",
    "email", "encodings", "ensurepip", "enum", "errno", "faulthandler", "fcntl", "filecmp", "fileinput",
    "fnmatch", "formatter", "fractions", "ftplib", "functools", "gc", "getopt", "getpass", "gettext",
    "glob", "grp", "gzip", "hashlib", "heapq", "hmac", "html", "http", "imaplib", "imghdr", "importlib",
    "inspect", "io", "ipaddress", "itertools", "json", "keyword", "lib2to3", "linecache", "locale",
    "logging", "lzma", "mailbox", "mailcap", "marshal", "math", "mimetypes", "mmap", "modulefinder",
    "multiprocessing", "netrc", "nis", "nntplib", "numbers", "operator", "optparse", "os", "ossaudiodev",
    "pathlib", "pdb", "pickle", "pickletools", "pipes", "pkgutil", "platform", "plistlib", "poplib",
    "posix", "posixpath", "pprint", "profile", "pstats", "pty", "pwd", "py_compile", "pyclbr",
    "pydoc", "queue", "quopri", "random", "re", "readline", "reprlib", "resource", "rlcompleter",
    "runpy", "sched", "secrets", "select", "selectors", "shelve", "shlex", "shutil", "signal", "site",
    "smtpd", "smtplib", "sndhdr", "socket", "socketserver", "sqlite3", "ssl", "stat", "statistics",
    "string", "stringprep", "struct", "subprocess", "sunau", "symbol", "symtable", "sys", "sysconfig",
    "syslog", "tabnanny", "tarfile", "telnetlib", "tempfile", "termios", "textwrap", "threading",
    "time", "timeit", "tkinter", "token", "tokenize", "trace", "traceback", "tracemalloc", "tty",
    "turtle", "turtledemo", "types", "typing", "unicodedata", "unittest", "urllib", "uuid",
    "venv", "warnings", "wave", "weakref", "webbrowser", "winreg", "winsound", "wsgiref", "xdrlib",
    "xml", "xmlrpc", "zipapp", "zipfile", "zipimport", "zlib", "zoneinfo"
]

def detectReqs(path):
    reqs = []
    fileTxt = ""
    with open(path, 'r',encoding="utf-8") as f:
        fileTxt = f.read()
    pattern = re.compile(r"import (.*?)\n")
    for match in re.finditer(pattern, fileTxt):
        name = match.group(1)

        # Handle 'import X as Y' case
        if ' as ' in name:
            name = name.split(' as ')[0]

        topModule = name.split(".")[0]
        if topModule in python_std_lib_modules:
            continue
        reqs.append(topModule)
    return reqs

pkgs = []
for path in os.listdir("./pkgs"):
    pathName = path.split(".")[0]
    absPath = os.path.abspath(os.path.join("./pkgs",path))

    if not absPath.endswith(".py"):
        continue

    # Get required modules
    modules = detectReqs(absPath)

    # Map modules to pip packages
    reqs = []
    for module in modules:
        if module in module_to_pip:
            reqs.append(module_to_pip[module])
        else:
            reqs.append(module)

    # Add PyInstaller
    reqs.append("pyinstaller")

    with tempfile.TemporaryDirectory(delete=True) as venv:
        subprocess.run(["python3", "-m", "venv", venv])

        # Determine the correct paths based on the operating system
        if os.name == 'nt':  # Windows
            pipPath = os.path.join(venv, "Scripts", "pip.exe")
            pythonPath = os.path.join(venv, "Scripts", "python.exe")
        else:  # Linux/Mac
            pipPath = os.path.join(venv, "bin", "pip")
            pythonPath = os.path.join(venv, "bin", "python")

        subprocess.run([pipPath, "install",*reqs])

        print(os.path.abspath(absPath))
        print([pythonPath, "-m", "PyInstaller", absPath, "--onefile"])
        subprocess.run([pythonPath, "-m", "PyInstaller", absPath, "--onefile", "--clean","--target-arch","x86_64"])

        # Remove spec file if it exists
        spec_file = "./"+pathName+".spec"
        if os.path.exists(spec_file):
            os.remove(spec_file)
    pkgs.append(pathName+".exe")

with open("./dist/registry.txt", "w",encoding="utf-8") as f:
    f.write("\n".join(pkgs))
