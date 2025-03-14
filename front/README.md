# KPZ Package Manager for Executables

This is a command-line tool for downloading and managing executables from the backend server. It provides a similar syntax to the Debian apt command.

## Installation

No installation is required. Simply run the script using Python:

```
python3 kpz.py [command] [options]
```

## Commands

### update

Update the package registry from the server.

```
python3 kpz.py update
```

### list

List available packages and their installation status.

```
python3 kpz.py list
```

### install

Install one or more packages.

```
python3 kpz.py install [package1] [package2] ...
```

To install all available packages:

```
python3 kpz.py install all
```

### remove

Remove one or more installed packages.

```
python3 kpz.py remove [package1] [package2] ...
```

To remove all installed packages:

```
python3 kpz.py remove all
```

### upgrade

Upgrade all installed packages to their latest versions.

```
python3 kpz.py upgrade
```

## Examples

Update the package registry:
```
python3 kpz.py update
```

List available packages:
```
python3 kpz.py list
```

Install the QR code generator:
```
python3 kpz.py install qr.exe
```

Install multiple packages:
```
python3 kpz.py install qr.exe yt.exe
```

Remove a package:
```
python3 kpz.py remove qr.exe
```

Upgrade all installed packages:
```
python3 kpz.py upgrade
```

## Notes

- The tool requires an internet connection to communicate with the backend server.
- The backend server must be running at http://localhost:8080.
- Installed executables are stored in the `./bin` directory, which is added to the system PATH.
- You can run the installed executables directly from the command line after installation.
