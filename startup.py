import os
import subprocess
import sys
import platform

def run_command(command):
    """Helper function to run a shell command."""
    print(f"Running: {command}")
    result = subprocess.run(command, shell=True, check=True)
    result.check_returncode()

def get_python_command():
    """Determine whether to use 'python' or 'python3'."""
    try:
        # Check if python3 is available
        subprocess.run(["python3", "--version"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return "python3"
    except subprocess.CalledProcessError:
        # If python3 is not found, check for python
        try:
            subprocess.run(["python", "--version"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            return "python"
        except subprocess.CalledProcessError:
            # If neither python nor python3 is found, ask the user to install Python
            print("Error: Python is not installed on your system. Please install Python from:")
            print("https://www.python.org/downloads/")
            sys.exit(1)

def activate_virtualenv():
    """Activate the virtual environment based on the operating system."""
    os_type = platform.system()

    print("Activating virtualenv...")

    if os_type == "Windows":
        activate_command = ".\\.venv\\Scripts\\activate"
    elif os_type == "Darwin" or os_type == "Linux":  # macOS and Linux
        activate_command = "source ./.venv/bin/activate"
    else:
        print(f"Unsupported operating system: {os_type}")
        sys.exit(1)

    run_command(activate_command)

def create_virtualenv():
    """Create a virtual environment if it doesn't exist."""
    if not os.path.exists(".venv"):
        print("Creating virtual environment...")
        run_command("python -m venv .venv")
    else:
        print("Virtual environment already exists.")

def install_requirements():
    """Install py-graspi in the virtual environment."""
    print("Installing py-graspi in the virtual environment...")

    # Activate the virtual environment
    activate_virtualenv()

    # Change to the py-graspi directory
    if os.path.exists("py-graspi"):
        os.chdir("py-graspi")
        print("Changed directory to 'py-graspi'.")
    else:
        print("The 'py-graspi' directory does not exist. Please clone the repository first.")
        sys.exit(1)

    run_command("pip install py-graspi")

def main():
    """Main setup function."""
    print("Starting setup...")

    # Ensure Python is installed
    try:
        subprocess.run(["python", "--version"], check=True)
    except subprocess.CalledProcessError:
        print("Python is not installed. Please install Python first.")
        sys.exit(1)

    # Create the virtual environment if it doesn't exist
    create_virtualenv()

    # Install requirements in the virtual environment
    install_requirements()

    print("Setup complete!")

if __name__ == "__main__":
    main()
