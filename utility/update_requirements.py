import subprocess
import platform
import os
from datetime import datetime

# Define essential packages that are needed for both Windows and macOS
ESSENTIAL_PACKAGES = {
    'keyboard',
    'MouseInfo',
    'pendulum',
    'pillow',
    'PyAutoGUI',
    'PyGetWindow',
    'PyMsgBox',
    'pynput',
    'pyperclip',
    'PyRect',
    'PyScreeze',
    'python-dateutil',
    'pytweening',
    'six',
    'toml'
}

# Define OS-specific package prefixes to filter
MACOS_SPECIFIC = {
    'pyobjc',
    'rubicon-objc',
    'macholib'
}

def get_installed_packages():
    """Get list of installed packages with versions"""
    try:
        result = subprocess.run(['pip', 'freeze'], capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Error getting installed packages: {e}")
        return None

def filter_packages(packages_str):
    """Filter packages into essential and OS-specific lists"""
    all_packages = {}
    for line in packages_str.split('\n'):
        if '==' in line:
            name, version = line.split('==')
            all_packages[name.lower()] = line

    # Get essential packages with their versions
    essential_packages = []
    for package in ESSENTIAL_PACKAGES:
        if package.lower() in all_packages:
            essential_packages.append(all_packages[package.lower()])
    
    # Get macOS specific packages
    macos_packages = essential_packages.copy()  # Include essential packages
    for name, line in all_packages.items():
        # Add macOS specific packages
        if any(name.startswith(prefix.lower()) for prefix in MACOS_SPECIFIC):
            macos_packages.append(line)
        # Add development tools like pyinstaller
        elif name.startswith('pyinstaller'):
            macos_packages.append(line)
    
    return sorted(essential_packages), sorted(macos_packages)

def write_requirements(filename, packages, os_type):
    """Write requirements to file with header"""
    try:
        with open(filename, 'w') as f:
            f.write(f"# Requirements for {os_type}\n")
            f.write(f"# Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write('\n'.join(packages))
        print(f"Successfully updated {filename}")
        return True
    except Exception as e:
        print(f"Error writing {filename}: {e}")
        return False

def update_requirements():
    """Update requirements files for both Windows and macOS"""
    packages_str = get_installed_packages()
    if not packages_str:
        return False

    # Filter packages
    essential_packages, macos_packages = filter_packages(packages_str)
    
    # Update Windows requirements (essential packages only)
    write_requirements('requirements_windows.txt', essential_packages, 'Windows')
    
    # Update macOS requirements (all packages)
    write_requirements('requirements.txt', macos_packages, 'macOS')
    
    return True

if __name__ == "__main__":
    update_requirements() 