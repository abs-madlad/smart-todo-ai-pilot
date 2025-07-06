#!/usr/bin/env python3
"""
Setup script for Smart Todo AI Application
"""

import os
import subprocess
import sys
from pathlib import Path

def run_command(command, cwd=None):
    """Run a command and return success status."""
    try:
        result = subprocess.run(
            command, 
            shell=True, 
            check=True, 
            cwd=cwd,
            capture_output=True,
            text=True
        )
        print(f"✅ {command}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {command}")
        print(f"Error: {e.stderr}")
        return False

def setup_backend():
    """Set up the Django backend."""
    print("\n🔧 Setting up Django Backend...")
    
    backend_dir = Path("backend")
    if not backend_dir.exists():
        print("❌ Backend directory not found!")
        return False
    
    # Create virtual environment
    if not run_command("python -m venv venv", cwd=backend_dir):
        return False
    
    # Determine activation script based on OS
    if sys.platform == "win32":
        activate_script = "venv\\Scripts\\activate"
        pip_command = "venv\\Scripts\\pip"
        python_command = "venv\\Scripts\\python"
    else:
        activate_script = "venv/bin/activate"
        pip_command = "venv/bin/pip"
        python_command = "venv/bin/python"
    
    # Install requirements
    if not run_command(f"{pip_command} install -r requirements.txt", cwd=backend_dir):
        return False
    
    # Check if .env exists
    env_file = backend_dir / ".env"
    if not env_file.exists():
        print("⚠️  Creating .env file from template...")
        env_example = backend_dir / "env.example"
        if env_example.exists():
            with open(env_example, 'r') as f:
                content = f.read()
            with open(env_file, 'w') as f:
                f.write(content)
            print("📝 Please edit backend/.env with your configuration")
        else:
            print("❌ env.example not found!")
            return False
    
    # Run migrations
    if not run_command(f"{python_command} manage.py makemigrations", cwd=backend_dir):
        return False
    
    if not run_command(f"{python_command} manage.py migrate", cwd=backend_dir):
        return False
    
    print("✅ Backend setup complete!")
    return True

def setup_frontend():
    """Set up the React frontend."""
    print("\n🔧 Setting up React Frontend...")
    
    # Install npm dependencies
    if not run_command("npm install"):
        return False
    
    print("✅ Frontend setup complete!")
    return True

def main():
    """Main setup function."""
    print("🚀 Smart Todo AI Application Setup")
    print("=" * 40)
    
    # Check Python version
    if sys.version_info < (3, 9):
        print("❌ Python 3.9+ required!")
        sys.exit(1)
    
    # Check Node.js
    try:
        result = subprocess.run(["node", "--version"], capture_output=True, text=True)
        if result.returncode != 0:
            print("❌ Node.js not found! Please install Node.js 18+")
            sys.exit(1)
        print(f"✅ Node.js version: {result.stdout.strip()}")
    except FileNotFoundError:
        print("❌ Node.js not found! Please install Node.js 18+")
        sys.exit(1)
    
    # Setup backend
    if not setup_backend():
        print("❌ Backend setup failed!")
        sys.exit(1)
    
    # Setup frontend
    if not setup_frontend():
        print("❌ Frontend setup failed!")
        sys.exit(1)
    
    print("\n🎉 Setup Complete!")
    print("=" * 40)
    print("Next steps:")
    print("1. Edit backend/.env with your configuration")
    print("2. Start backend: cd backend && python manage.py runserver")
    print("3. Start frontend: npm run dev")
    print("4. Visit http://localhost:8080")
    print("\nFor detailed instructions, see README.md")

if __name__ == "__main__":
    main() 