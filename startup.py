import os
import subprocess
import sys

def run_command(command):
    """Helper function to run a shell command."""
    print(f"Running: {command}")
    result = subprocess.run(command, shell=True, check=True)
    result.check_returncode()

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
    run_command(".\\.venv\\Scripts\\activate")
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
