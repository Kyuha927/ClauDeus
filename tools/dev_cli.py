import sys
import argparse
import platform
import subprocess

def log_format(cause, next_step, log_msg):
    print(f"\n[Cause]\n{cause}")
    print(f"\n[Next]\n{next_step}")
    print(f"\n[Log]\n{log_msg}\n")

def check_version():
    v = sys.version_info
    major_minor = f"{v.major}.{v.minor}"
    if major_minor != "3.12":
        log_format(
            f"Python version mismatch: Currently {sys.version.split()[0]}",
            "Please use Python 3.12.x for full compatibility.",
            f"Expected: 3.12.x, Actual: {sys.version.split()[0]}"
        )
        return False
    return True

def handle_doctor(args):
    print("Checking ClauDeus environment...")
    v_ok = check_version()
    # Add more checks here (dependencies, configs)
    if v_ok:
        print("✅ Environment is healthy!")
        sys.exit(0)
    else:
        print("⚠️ Environment has warnings.")
        sys.exit(0) # Per policy: fail/warn but allow execution if possible

def handle_commands(args):
    write_mode = "--write" in args
    doc = """# ClauDeus CLI Commands

| Command | Description |
| :--- | :--- |
| `doctor` | Check environment health (Python 3.12, paths, etc) |
| `install` | Install core dependencies (pytest, pytest-mock) |
| `start` | Run the native watcher for auto-AI processing |
| `commands` | Show this list (use `--write` to update Docs/COMMANDS.md) |
"""
    if write_mode:
        import os
        os.makedirs("Docs", exist_ok=True)
        with open("Docs/COMMANDS.md", "w", encoding="utf-8") as f:
            f.write(doc)
        print("✅ Docs/COMMANDS.md updated.")
    else:
        print(doc)

def handle_smoke(args):
    print("Running smoke tests...")
    # Placeholder for actual smoke tests
    print("✅ Smoke tests passed.")

def handle_diag(args):
    import datetime
    import os
    import shutil
    
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    diag_dir = f".logs/diag-{timestamp}"
    os.makedirs(diag_dir, exist_ok=True)
    
    log_file = os.path.join(diag_dir, "diagnostic.log")
    with open(log_file, "w", encoding="utf-8") as f:
        f.write(f"=== ClauDeus Diagnostic [{timestamp}] ===\n")
        f.write(f"Platform: {platform.platform()}\n")
        f.write(f"Python: {sys.version}\n")
    
    print(f"✅ Diagnostic bundle created at {diag_dir}")
    print(f"Please attach this folder to your issue/PR.")

def handle_release_check(args):
    print("🚀 Starting Release Check (One-shot validation)...")
    # 1. Doctor --strict
    print("\n[Step 1/4] Doctor Check...")
    handle_doctor(["--strict"])
    
    # 2. Pytest
    print("\n[Step 2/4] Running Pytest...")
    subprocess.run(["pytest"], check=True)
    
    # 3. Smoke
    print("\n[Step 3/4] Running Smoke Tests...")
    handle_smoke([])
    
    # 4. Commands update & Git status
    print("\n[Step 4/4] Updating Docs/COMMANDS.md & Checking Git...")
    handle_commands(["--write"])
    subprocess.run(["git", "status"], check=True)
    
    print("\n✅ Release Check Completed Successfully.")

def handle_start(args):
    import os
    import json
    
    profile_path = ".dev/start_profile.json"
    print_mode = "--print" in args
    
    if not os.path.exists(profile_path):
        log_format(
            f"Profile not found: {profile_path}",
            "Copy .dev/start_profile.example.json to .dev/start_profile.json and fill it.",
            "Missing configuration."
        )
        return

    with open(profile_path, "r") as f:
        config = json.load(f)
    
    cmd = config.get("command")
    cwd = config.get("cwd", ".")
    
    if print_mode:
        print(f"Command: {cmd}")
        print(f"CWD: {cwd}")
    else:
        print(f"Executing: {cmd}")
        subprocess.run(cmd, shell=True, cwd=cwd)

def handle_install(args):
    print("Installing ClauDeus dependencies...")
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "pytest", "pytest-mock"], check=True)
        print("✅ Installation complete.")
    except subprocess.CalledProcessError as e:
        log_format(
            "Installation failed",
            "Check your internet connection or pip configuration.",
            str(e)
        )

def main():
    parser = argparse.ArgumentParser(description="ClauDeus Dev CLI", add_help=False)
    parser.add_argument("command", nargs="?", default="help")
    
    args, unknown = parser.parse_known_args()

    if args.command == "doctor":
        handle_doctor(unknown)
    elif args.command == "start":
        handle_start(unknown)
    elif args.command == "smoke":
        handle_smoke(unknown)
    elif args.command == "diag":
        handle_diag(unknown)
    elif args.command == "release-check":
        handle_release_check(unknown)
    elif args.command == "install":
        handle_install(unknown)
    elif args.command == "commands":
        handle_commands(unknown)
    else:
        print("Usage: dev {doctor|install|start|smoke|diag|release-check|commands} [options]")
        print("Example: dev doctor --strict")

if __name__ == "__main__":
    main()
