import argparse
import os
import sys
import requests
import subprocess
import shutil

# Constants
SERVER_URL = "http://localhost:8080"
BIN_DIR = os.path.abspath("./bin")
REGISTRY_FILE = os.path.join(BIN_DIR, "registry.txt")

def ensure_bin_directory():
    """Ensure the bin directory exists and is in PATH."""
    if not os.path.exists(BIN_DIR):
        print(f"Creating directory: {BIN_DIR}")
        os.makedirs(BIN_DIR, exist_ok=True)

    # Add bin directory to PATH if not already there
    if BIN_DIR not in os.environ.get("PATH", ""):
        print(f"Adding {BIN_DIR} to PATH")
        new_path = os.environ.get("PATH", "") + os.pathsep + BIN_DIR

        # Update PATH based on OS
        if os.name == 'nt':  # Windows
            subprocess.run(f"setx PATH \"{new_path}\"", shell=True)
        else:  # Linux/Unix
            bashrc_path = os.path.expanduser("~/.bashrc")
            export_line = f'\n# Added by KPZ\nexport PATH="$PATH{os.pathsep}{BIN_DIR}"\n'

            # Check if the export line already exists in .bashrc
            if os.path.exists(bashrc_path):
                with open(bashrc_path, 'r') as f:
                    if BIN_DIR not in f.read():
                        with open(bashrc_path, 'a') as f:
                            f.write(export_line)
                            print(f"Added PATH export to {bashrc_path}")
            else:
                with open(bashrc_path, 'w') as f:
                    f.write(export_line)
                    print(f"Created {bashrc_path} with PATH export")

            print("Please run 'source ~/.bashrc' or restart your terminal to apply the PATH changes")

        # Also update current session PATH
        os.environ["PATH"] = new_path

def get_remote_registry():
    """Get the registry from the server."""
    try:
        response = requests.get(f"{SERVER_URL}/registry.txt")
        response.raise_for_status()
        return response.text.splitlines()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching registry: {e}")
        return []

def get_local_registry():
    """Get the list of locally installed packages."""
    if not os.path.exists(REGISTRY_FILE):
        return []

    with open(REGISTRY_FILE, 'r') as f:
        return [line.strip() for line in f if line.strip()]

def save_local_registry(packages):
    """Save the list of installed packages to the registry file."""
    with open(REGISTRY_FILE, 'w') as f:
        f.write("\n".join(packages))

def update():
    """Update the package registry."""
    ensure_bin_directory()
    print("Updating package registry...")
    remote_registry = get_remote_registry()

    if remote_registry:
        print(f"Found {len(remote_registry)} packages on the server.")
        # Save the remote registry locally
        with open(REGISTRY_FILE, 'w') as f:
            f.write("\n".join(remote_registry))
        print("Package registry updated successfully.")
    else:
        print("No packages found or unable to connect to server.")

def list_packages():
    """List available packages."""
    ensure_bin_directory()
    remote_registry = get_remote_registry()

    # Get locally installed packages based on OS
    if os.name == 'nt':  # Windows
        local_registry = [os.path.basename(f) for f in os.listdir(BIN_DIR) if os.path.isfile(os.path.join(BIN_DIR, f)) and f.endswith('.exe')]
    else:  # Linux/Unix
        # On Linux, executables don't have .exe extension but should have executable permission
        local_registry = []
        for f in os.listdir(BIN_DIR):
            file_path = os.path.join(BIN_DIR, f)
            if os.path.isfile(file_path) and os.access(file_path, os.X_OK):
                local_registry.append(f)

    if not remote_registry:
        print("No packages available on the server or unable to connect.")
        return

    print("Available packages:")
    for package in remote_registry:
        status = "[installed]" if package in local_registry else "[not installed]"
        print(f"  {package} {status}")

def install(packages):
    """Install specified packages."""
    ensure_bin_directory()
    remote_registry = get_remote_registry()

    if not remote_registry:
        print("No packages available on the server or unable to connect.")
        return

    if not packages:
        print("No packages specified for installation.")
        return

    # If 'all' is specified, install all packages
    if len(packages) == 1 and packages[0] == 'all':
        packages = remote_registry

    for package in packages:
        if package not in remote_registry:
            print(f"Package '{package}' not found on the server.")
            continue

        print(f"Downloading {package}...")
        try:
            response = requests.get(f"{SERVER_URL}/{package}")
            response.raise_for_status()

            package_path = os.path.join(BIN_DIR, package)
            with open(package_path, 'wb') as f:
                f.write(response.content)

            # Make the file executable (for Unix-like systems)
            if os.name != 'nt':
                os.chmod(package_path, 0o755)

            print(f"Successfully installed {package}")
        except requests.exceptions.RequestException as e:
            print(f"Error downloading {package}: {e}")

def remove(packages):
    """Remove specified packages."""
    ensure_bin_directory()

    # Get locally installed packages based on OS
    if os.name == 'nt':  # Windows
        local_registry = [os.path.basename(f) for f in os.listdir(BIN_DIR) if os.path.isfile(os.path.join(BIN_DIR, f)) and f.endswith('.exe')]
    else:  # Linux/Unix
        # On Linux, executables don't have .exe extension but should have executable permission
        local_registry = []
        for f in os.listdir(BIN_DIR):
            file_path = os.path.join(BIN_DIR, f)
            if os.path.isfile(file_path) and os.access(file_path, os.X_OK):
                local_registry.append(f)

    if not packages:
        print("No packages specified for removal.")
        return

    # If 'all' is specified, remove all packages
    if len(packages) == 1 and packages[0] == 'all':
        packages = local_registry

    for package in packages:
        package_path = os.path.join(BIN_DIR, package)
        if os.path.exists(package_path):
            try:
                os.remove(package_path)
                print(f"Successfully removed {package}")
            except OSError as e:
                print(f"Error removing {package}: {e}")
        else:
            print(f"Package '{package}' is not installed.")

def upgrade():
    """Upgrade all installed packages."""
    ensure_bin_directory()
    remote_registry = get_remote_registry()

    # Get locally installed packages based on OS
    if os.name == 'nt':  # Windows
        local_registry = [os.path.basename(f) for f in os.listdir(BIN_DIR) if os.path.isfile(os.path.join(BIN_DIR, f)) and f.endswith('.exe')]
    else:  # Linux/Unix
        # On Linux, executables don't have .exe extension but should have executable permission
        local_registry = []
        for f in os.listdir(BIN_DIR):
            file_path = os.path.join(BIN_DIR, f)
            if os.path.isfile(file_path) and os.access(file_path, os.X_OK):
                local_registry.append(f)

    if not remote_registry:
        print("No packages available on the server or unable to connect.")
        return

    if not local_registry:
        print("No packages are currently installed.")
        return

    print("Upgrading installed packages...")
    for package in local_registry:
        if package in remote_registry:
            print(f"Upgrading {package}...")
            try:
                response = requests.get(f"{SERVER_URL}/{package}")
                response.raise_for_status()

                package_path = os.path.join(BIN_DIR, package)
                with open(package_path, 'wb') as f:
                    f.write(response.content)

                # Make the file executable (for Unix-like systems)
                if os.name != 'nt':
                    os.chmod(package_path, 0o755)

                print(f"Successfully upgraded {package}")
            except requests.exceptions.RequestException as e:
                print(f"Error upgrading {package}: {e}")
        else:
            print(f"Package '{package}' is no longer available on the server.")

def main():
    parser = argparse.ArgumentParser(description='KPZ Package manager for downloading and managing executables')
    subparsers = parser.add_subparsers(dest='command', help='Command to execute')

    # Update command
    update_parser = subparsers.add_parser('update', help='Update package registry')

    # List command
    list_parser = subparsers.add_parser('list', help='List available packages')

    # Install command
    install_parser = subparsers.add_parser('install', help='Install packages')
    install_parser.add_argument('packages', nargs='+', help='Packages to install (use "all" to install all packages)')

    # Remove command
    remove_parser = subparsers.add_parser('remove', help='Remove packages')
    remove_parser.add_argument('packages', nargs='+', help='Packages to remove (use "all" to remove all packages)')

    # Upgrade command
    upgrade_parser = subparsers.add_parser('upgrade', help='Upgrade all installed packages')

    args = parser.parse_args()

    if args.command == 'update':
        update()
    elif args.command == 'list':
        list_packages()
    elif args.command == 'install':
        install(args.packages)
    elif args.command == 'remove':
        remove(args.packages)
    elif args.command == 'upgrade':
        upgrade()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
