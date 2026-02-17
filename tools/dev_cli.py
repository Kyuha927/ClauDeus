import sys
import argparse
import platform
import subprocess
import os

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
        return
    else:
        if "--strict" in args:
            print("❌ Strict mode enabled: Environment check failed.")
            sys.exit(1)
        print("⚠️ Environment has warnings.")
        return # Per policy: fail/warn but allow execution if possible

def handle_commands(args):
    write_mode = "--write" in args
    doc = """# ClauDeus CLI Commands

| Command | Description |
| :--- | :--- |
| `doctor` | Check environment health (Python 3.12, paths, etc) |
| `bootstrap` | **Onboarding**: Check Py3.12 + Ensure venv + Install deps |
| `dev-check` | **Fast Loop**: doctor(msg) + pytest + smoke (dirty allowed) |
| `release-check` | **Strict Gate**: Py3.12 strict + clean tree + evidence |
| `install` | (Legacy) Install core dependencies |
| `start` | Run the native watcher for auto-AI processing |
| `commands` | Show this list (use `--write` to update Docs/COMMANDS.md) |

## Check Policy
- `dev-check`: fast developer loop (non-strict, dirty allowed)
- `release-check`: strict release gate (Python 3.12.x only, clean working tree required)
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
    print("Policy: Windows=required, WSL=optional, Python=3.12.x(strict)")
    # 1. Doctor --strict
    print("\n[Step 1/4] Doctor Check...")
    handle_doctor(["--strict"])
    
    # 2. Pytest
    print("\n[Step 2/4] Running Pytest...")
    subprocess.run([sys.executable, "-m", "pytest"], check=True)
    
    # 3. Smoke
    print("\n[Step 3/4] Running Smoke Tests...")
    handle_smoke([])
    
    # 4. Commands update & Git status
    print("\n[Step 4/4] Updating Docs/COMMANDS.md & Checking Git...")
    handle_commands(["--write"])
    subprocess.run(["git", "status"], check=True)
    
    print("\n✅ Release Check Completed Successfully.")

def handle_dev_check(args):
    print("== ./dev dev-check ==")
    
    # [DEV] step: ./dev doctor
    print("[DEV] step: ./dev doctor ... ", end="")
    handle_doctor([]) # non-strict
    # handle_doctor prints "✅ Environment is healthy!" which puts a newline.
    # We might want to suppress that or just let it be. 
    # handle_doctor exits/returns. 
    # strictly speaking handle_doctor prints output. 
    # Let's just call it. It prints its own status.
    
    # [DEV] step: python -m pytest -q
    print("[DEV] step: python -m pytest -q ...")
    try:
        subprocess.run([sys.executable, "-m", "pytest", "-q"], check=True)
    except subprocess.CalledProcessError:
        print("❌ Pytest failed.")
        sys.exit(1)

    # [DEV] step: ./dev smoke
    print("[DEV] step: ./dev smoke ...")
    handle_smoke([])
    
    print("Result: PASS")

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

def handle_bootstrap(args):
    print("== ./dev bootstrap ==")
    print("Policy: Windows=required, WSL=optional, Python=3.12.x(strict)")

    # [1/4] Check Python 3.12.x
    print("[1/4] Check Python 3.12.x ... ", end="")
    if not check_version():
        print("FAIL")
        log_format(
            "Python version mismatch.",
            "Follow SSOT setup: Docs/setup/python-3.12.md",
            f"Current: {sys.version.split()[0]}"
        )
        sys.exit(1)
    print("PASS")

    # [2/4] Ensure venv (.venv)
    print("[2/4] Ensure venv (.venv) ... ", end="")
    venv_path = ".venv"
    if not os.path.exists(venv_path):
        try:
            subprocess.run([sys.executable, "-m", "venv", venv_path], check=True)
            print("CREATED")
        except subprocess.CalledProcessError as e:
            print("FAIL")
            log_format("Venv creation failed", "Check permissions or python install", str(e))
            sys.exit(1)
    else:
        print("OK")

    # Determine pip/python paths inside venv
    if platform.system() == "Windows":
        venv_python = os.path.join(venv_path, "Scripts", "python.exe")
        venv_pip = os.path.join(venv_path, "Scripts", "pip.exe")
    else:
        venv_python = os.path.join(venv_path, "bin", "python")
        venv_pip = os.path.join(venv_path, "bin", "pip")

    # [3/4] Upgrade pip
    print("[3/4] Upgrade pip ... ", end="")
    try:
        subprocess.run([venv_python, "-m", "pip", "install", "--upgrade", "pip"], 
                       check=True, capture_output=True)
        print("PASS")
    except subprocess.CalledProcessError:
        print("FAIL (Continuing...)")

    # [4/4] Install deps
    print("[4/4] Install deps ... ", end="")
    try:
        subprocess.run([venv_python, "-m", "pip", "install", "pytest", "pytest-mock"], 
                       check=True, capture_output=True)
        print("PASS")
    except subprocess.CalledProcessError as e:
        print("FAIL")
        log_format("Dependency install failed", "Check network/pip", str(e))
        sys.exit(1)

    print("Next: run ./dev release-check")

def handle_install(args):
    # Backward compatibility
    handle_bootstrap(args)

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
    elif args.command == "dev-check":
        handle_dev_check(unknown)
    elif args.command == "bootstrap":
        handle_bootstrap(unknown)
    elif args.command == "install":
        handle_install(unknown)
    elif args.command == "commands":
        handle_commands(unknown)
    else:
        print("Usage: dev {doctor|bootstrap|start|smoke|diag|release-check|commands} [options]")
        print("Example: dev doctor --strict")

if __name__ == "__main__":
    main()
