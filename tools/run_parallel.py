import json
import subprocess
import time
import os
import sys
import re
import argparse

def send_notification(title, message):
    """
    Sends a Windows system notification using PowerShell.
    """
    try:
        # PowerShell command for a simple MessageBox (Popup)
        # Using WScript.Shell for a slightly more modern look and non-blocking if needed
        ps_cmd = f"$wshell = New-Object -ComObject WScript.Shell; $wshell.Popup('{message}', 0, '{title}', 64)"
        subprocess.Popen(["powershell", "-Command", ps_cmd])
    except:
        pass

def scan_directory(directory):
    tasks = []
    if not os.path.exists(directory):
        print(f"오류: 디렉토리 '{directory}'를 찾을 수 없습니다.")
        return tasks

    print(f"'{directory}' 디렉토리 스캔 중...")
    
    files = os.listdir(directory)

    for filename in files:
        if not filename.lower().endswith(".md"):
            continue
            
        filepath = os.path.join(directory, filename)
        model = None
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                # Read first 5 lines safely
                head = []
                for _ in range(5):
                    line = f.readline()
                    if not line:
                        break
                    head.append(line)
                
                content = "".join(head)
                
                # Look for patterns: <!-- model: gpt-4 --> or # model: gpt-4
                match = re.search(r'<!--\s*model:\s*(.+?)\s*-->', content, re.IGNORECASE)
                if not match:
                    match = re.search(r'#\s*model:\s*(.+)', content, re.IGNORECASE)
                
                if match:
                    model = match.group(1).strip()
        except Exception as e:
            print(f"파일 읽기 오류 ({filename}): {e}")

        if model:
            task_id = os.path.splitext(filename)[0]
            tasks.append({
                "id": task_id,
                "model": model,
                "context": filepath,
                "output_log": f".logs/{task_id}.log"
            })
            print(f"  - 발견: {filename} (모델: {model})")

    return tasks

def run_parallel():
    parser = argparse.ArgumentParser(description="Run codex models in parallel.")
    parser.add_argument("--scan", help="Scan a directory for prompts with model headers.", default=None)
    parser.add_argument("--config", help="Path to JSON config file.", default="conversations.json")
    parser.add_argument("--watch", action="store_true", help="Watch the scan directory for changes and run automatically.")
    parser.add_argument("filter_ids", nargs="*", help="Optional: List of task IDs to run. If omitted, all tasks found will run.")
    args = parser.parse_args()

    if args.watch and not args.scan:
        print("오류: --watch 모드는 --scan과 함께 사용해야 합니다.")
        sys.exit(1)

    if args.watch:
        watch_directory(args.scan)
        return

    all_tasks = []

    if args.scan:
        all_tasks = scan_directory(args.scan)
        if not all_tasks:
            print("실행할 작업이 없습니다. .md 파일 상단에 '<!-- model: 모델명 -->'을 추가했는지 확인하세요.")
            sys.exit(0)
    else:
        config_path = args.config
        if not os.path.exists(config_path):
            print(f"오류: 설정 파일 '{config_path}'를 찾을 수 없습니다.")
            print("사용법: python tools/run_parallel.py --scan prompts/  또는  --config conversations.json")
            sys.exit(1)

        with open(config_path, 'r', encoding='utf-8') as f:
            all_tasks = json.load(f)

    # Filter tasks if specific IDs are provided
    if args.filter_ids:
        tasks = [t for t in all_tasks if any(fid.lower() in t['id'].lower() for fid in args.filter_ids)]
        if not tasks:
            print(f"알림: 지정하신 ID({args.filter_ids})와 일치하는 작업을 찾지 못했습니다.")
            print(f"발견된 작업 가능 목록: {[t['id'] for t in all_tasks]}")
            sys.exit(0)
    else:
        tasks = all_tasks

    if not tasks:
        print("작업 목록이 비어 있습니다.")
        sys.exit(0)

    execute_tasks(tasks)

def execute_tasks(tasks):
    if not tasks:
        return

    processes = []
    print(f"\n{len(tasks)}개의 작업을 시작합니다...")

    for task in tasks:
        task_id = task.get("id")
        model = task.get("model")
        context = task.get("context")
        output_log = task.get("output_log")

        if output_log:
            log_dir = os.path.dirname(output_log)
            if log_dir and not os.path.exists(log_dir):
                os.makedirs(log_dir)

        # Using 'exec' instead of 'run' which doesn't exist in newer Codex CLI versions.
        # We'll use stdin redirection to pass the prompt file content.
        cmd = f"type \"{context}\" | codex exec -m {model} --full-auto --skip-git-repo-check"
        print(f"[{task_id}] 실행 중...")
        
        try:
            # Using shell=True for the pipe command in Windows
            log_file = open(output_log, "w", encoding='utf-8') if output_log else subprocess.PIPE
            p = subprocess.Popen(cmd, stdout=log_file, stderr=subprocess.STDOUT, shell=True, text=True)
            processes.append((task_id, p, log_file))
        except Exception as e:
            print(f"[{task_id}] 오류: {e}")

    # Wait and report
    print("\n" + "="*50)
    print("작업 완료 리포트")
    print("-"*50)

    for task_id, p, log_file in processes:
        p.wait()
        if log_file and log_file != subprocess.PIPE:
            log_file.close()
        
        status = "성공" if p.returncode == 0 else f"실패 (코드 {p.returncode})"
        print(f"[{task_id}] 상태: {status}")

    print("-"*50)
    send_notification("msw-vampser 알림", "작업이 완료되었습니다!")
    generate_markdown_summary(tasks)

def watch_directory(directory):
    print(f"'{directory}' 폴더 감시 중... (파일을 수정하고 저장하면 자동으로 실행됩니다.)")
    print("중단하려면 Ctrl+C를 누르세요.")
    
    last_mtimes = {}
    
    # Initial scan
    initial_tasks = scan_directory(directory)
    for t in initial_tasks:
        last_mtimes[t['context']] = os.path.getmtime(t['context'])

    try:
        while True:
            time.sleep(1)
            current_tasks = scan_directory(directory)
            for t in current_tasks:
                path = t['context']
                if not os.path.exists(path): continue
                current_mtime = os.path.getmtime(path)
                
                if path not in last_mtimes or current_mtime > last_mtimes[path]:
                    task_id = t['id']
                    print(f"\n[변경 감지] {task_id} 수정됨. 작업을 시작합니다.")
                    
                    # Notify and update summary with 'running' status
                    send_notification("msw-vampser 작업 시작", f"{task_id} 모델의 답변을 생성하는 중입니다...")
                    generate_markdown_summary(current_tasks, running_task_id=task_id)
                    
                    execute_tasks([t])
                    last_mtimes[path] = current_mtime
                    
                    # Refresh all tasks summary after completion
                    generate_markdown_summary(current_tasks)
    except KeyboardInterrupt:
        print("\n감시를 중단합니다.")

def generate_markdown_summary(tasks, running_task_id=None):
    """
    Consolidates all result logs into a single Markdown file for easy preview.
    If running_task_id is provided, show that task as 'running'.
    """
    summary_path = "RESULTS_SUMMARY.md"
    try:
        with open(summary_path, "w", encoding="utf-8") as out:
            out.write("# 작업 결과 요약 (Multi-Model Results)\n\n")
            out.write(f"**최근 업데이트**: {time.strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            out.write("---\n\n")

            for task in tasks:
                task_id = task['id']
                log_path = task['output_log']
                model = task['model']

                if task_id == running_task_id:
                    out.write(f"## 🤖 {task_id} (Model: {model}) <span style='color: #ff9800;'>🕒 실행 중...</span>\n\n")
                    out.write("> 현재 모델이 답변을 생성하고 있습니다. 잠시만 기다려 주세요...\n\n")
                else:
                    out.write(f"## 🤖 {task_id} (Model: {model})\n\n")
                    
                    if os.path.exists(log_path):
                        with open(log_path, "r", encoding="utf-8") as f:
                            content = f.read()
                            if content.strip():
                                out.write(content + "\n\n")
                            else:
                                out.write("*내용이 없습니다.*\n\n")
                    else:
                        out.write("*로그 파일을 찾을 수 없습니다.*\n\n")
                
                out.write("---\n\n")
        
        print(f"마크다운 요약본이 생성되었습니다: {summary_path}")
    except Exception as e:
        print(f"요약본 생성 중 오류 발생: {e}")

if __name__ == "__main__":
    run_parallel()
