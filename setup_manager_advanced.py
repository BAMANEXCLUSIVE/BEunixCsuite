#use nano setup_manager_advanced.py

#!/usr/bin/env python3
import os
import subprocess
import logging
import platform
import time
import sys
import yaml
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from rich.console import Console
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn

console = Console()

# ------------------------------------------------------------------------------
# OUTPUT DIRECTORY CONFIGURATION
# ------------------------------------------------------------------------------
current_dir = os.getcwd()
console.print(f"[Debug] Current working directory: {current_dir}", style="cyan")

OUTPUT_DIR = os.path.join(current_dir, "OUTPUT")
console.print(f"[Debug] OUTPUT_DIR set to: {OUTPUT_DIR}", style="cyan")
os.makedirs(OUTPUT_DIR, exist_ok=True)
console.print("[Debug] OUTPUT directory ensured to exist.", style="cyan")

# ------------------------------------------------------------------------------
# Logging Configuration
# ------------------------------------------------------------------------------
LOG_FILE = os.path.join(OUTPUT_DIR, "setup_manager_advanced.log")
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
console.print(f"[Debug] Log file will be saved to: {LOG_FILE}", style="cyan")
logging.info("Logging initialized. This is a test log entry.")

# ------------------------------------------------------------------------------
# Global structures for task progress (thread-safe with lock)
# ------------------------------------------------------------------------------
task_progress = {}  # Format: { task_name: {"status": "", "start": <timestamp> or None, "end": <timestamp> or None, "group": str} }
progress_lock = threading.Lock()

# ------------------------------------------------------------------------------
# Helper Functions
# ------------------------------------------------------------------------------

def sanitize_filename(name):
    """Sanitize a string for safe file names."""
    return "".join(c if c.isalnum() or c in "._-" else "_" for c in name)

def open_file(file_path):
    """Open a file with the default system viewer."""
    try:
        if platform.system() == "Windows":
            os.startfile(file_path)
        else:
            subprocess.Popen(["xdg-open", file_path])
        console.print(f"[Open] Opened file: {file_path}", style="cyan")
    except Exception as e:
        console.print(f"[Open Error] Cannot open file {file_path}: {str(e)}", style="red")

def load_tasks(config_file):
    """Load tasks from YAML and merge all group-defined tasks into one list."""
    if not os.path.exists(config_file):
        console.print(f"[Error] Config file '{config_file}' not found.", style="bold red")
        sys.exit(1)
    with open(config_file, "r") as f:
        config = yaml.safe_load(f)
    tasks = []
    # Iterate over each group (top-level key) and add group info to tasks.
    for group, task_list in config.items():
        for task in task_list:
            if "group" not in task:
                task["group"] = group
            tasks.append(task)
    console.print(f"[Debug] Loaded {len(tasks)} tasks from '{config_file}'.", style="cyan")
    return tasks

def update_gantt_chart(tasks):
    """Generate a live-updating HTML Gantt chart with hyperlinks to task logs."""
    html_lines = []
    html_lines.append("<html><head>")
    html_lines.append('<meta http-equiv="refresh" content="5">')  # auto-refresh every 5 seconds
    html_lines.append("<style>")
    html_lines.append("""
        body { font-family: Arial, sans-serif; }
        table { width: 100%; border-collapse: collapse; }
        th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
        tr:nth-child(even){background-color: #f9f9f9;}
        .progress { position: relative; width: 100%; background-color: #ddd; height: 20px; }
        .progress-bar { height: 20px; background-color: #4CAF50; text-align: center; color: white; }
        a { text-decoration: none; color: #0645AD; }
    """)
    html_lines.append("</style></head><body>")
    html_lines.append("<h2>Gantt Chart – Task Progress</h2>")
    html_lines.append("<table>")
    html_lines.append("<tr><th>Task</th><th>Group</th><th>Start Time</th><th>End Time</th><th>Status</th><th>Progress</th></tr>")
    
    with progress_lock:
        for task in tasks:
            name = task.get("name", "Unnamed Task")
            indent = "&nbsp;&nbsp;&nbsp;&nbsp;" if task.get("dependencies") else ""
            group = task.get("group", "Ungrouped")
            status = task_progress.get(name, {}).get("status", "pending")
            start = task_progress.get(name, {}).get("start")
            end = task_progress.get(name, {}).get("end")
            start_str = time.strftime("%H:%M:%S", time.localtime(start)) if start else "-"
            end_str = time.strftime("%H:%M:%S", time.localtime(end)) if end else "-"
            progress_percent = 0
            if status == "running":
                progress_percent = 50
            elif status == "completed":
                progress_percent = 100

            log_filename = sanitize_filename(name) + ".log"
            log_filepath = os.path.join(OUTPUT_DIR, log_filename)
            if os.path.exists(log_filepath):
                task_display = f'<a href="{log_filename}" target="_blank">{indent}{name}</a>'
            else:
                task_display = indent + name

            progress_bar_html = f'''
            <div class="progress">
                <div class="progress-bar" style="width:{progress_percent}%;">{progress_percent}%</div>
            </div>
            '''
            html_lines.append(f"<tr><td>{task_display}</td><td>{group}</td><td>{start_str}</td><td>{end_str}</td><td>{status}</td><td>{progress_bar_html}</td></tr>")
    html_lines.append("</table>")
    html_lines.append("<h3>Project Management & Frameworks:</h3>")
    html_lines.append("<ul>")
    html_lines.append("<li>Frontend Frameworks: react, vue</li>")
    html_lines.append("<li>Backend Frameworks: nestjs, koa</li>")
    html_lines.append("<li>Project Management Tools: BRM, CPM, CCPM, EVM, Iterative & Incremental, Agile, DSDM, Extreme PM, Innovation Engineering</li>")
    html_lines.append("</ul>")
    html_lines.append("</body></html>")
    
    gantt_file = os.path.join(OUTPUT_DIR, "gantt_chart.html")
    with open(gantt_file, "w") as f:
        f.write("\n".join(html_lines))
    console.print(f"[Gantt] Updated live Gantt chart at '{gantt_file}'", style="cyan")

def gantt_updater_loop(tasks):
    """Continuously update the Gantt chart until all tasks finish."""
    total_tasks = len(tasks)
    while True:
        with progress_lock:
            completed = sum(1 for t in task_progress.values() if t["status"] in ["completed", "failed"])
        update_gantt_chart(tasks)
        if completed >= total_tasks:
            break
        time.sleep(5)

def execute_task(task):
    """Execute a task, update progress, and print a waiting message if >5 seconds."""
    name = task.get("name", "Unnamed Task")
    path = task.get("path", "")
    task_type = task.get("type", "").lower()
    log_filename = sanitize_filename(name) + ".log"
    task_log_path = os.path.join(OUTPUT_DIR, log_filename)
    
    # Create/clear the task log file.
    with open(task_log_path, "w") as task_log:
        task_log.write("")
    
    # Update task progress to 'running' and record start time.
    with progress_lock:
        task_progress[name]["status"] = "running"
        task_progress[name]["start"] = time.time()
    
    # Start a timer: if task runs for more than 5 seconds, print a wait message.
    def delayed_message():
        time.sleep(5)
        with progress_lock:
            if task_progress[name]["status"] == "running":
                console.print(f"[Info] {name}: please wait, the installation is in progress...", style="yellow")
    threading.Thread(target=delayed_message, daemon=True).start()

    logging.info(f"Starting task: {name}")
    console.print(f"[Task] Starting: {name}", style="green")
    try:
        if task_type == "py":
            result = subprocess.run([sys.executable, path], capture_output=True, text=True)
        elif task_type == "bat":
            if platform.system() == "Windows":
                result = subprocess.run(["cmd", "/c", path], capture_output=True, text=True)
            else:
                result = subprocess.run([path], shell=True, capture_output=True, text=True)
        elif task_type == "sh":
            result = subprocess.run(["bash", path], capture_output=True, text=True)
        elif task_type == "exe":
            result = subprocess.run([path], capture_output=True, text=True)
        elif task_type == "doc":
            logging.info(f"Document task '{name}' requires no execution.")
            console.print(f"[Doc] Document reference: {name}", style="blue")
            with progress_lock:
                task_progress[name]["status"] = "completed"
                task_progress[name]["end"] = time.time()
            return True
        else:
            logging.warning(f"Unknown task type for '{name}': {task_type}")
            console.print(f"[Warning] Unknown task type for {name}: {task_type}", style="yellow")
            with progress_lock:
                task_progress[name]["status"] = "failed"
                task_progress[name]["end"] = time.time()
            return False

        with open(task_log_path, "w") as task_log:
            task_log.write(result.stdout)
            if result.stderr:
                task_log.write("\n--- STDERR ---\n")
                task_log.write(result.stderr)
        
        if result.returncode != 0:
            message = f"Task '{name}' failed (rc={result.returncode}): {result.stderr}"
            logging.error(message)
            console.print(f"[Error] {name} failed: {result.stderr}", style="red")
            with progress_lock:
                task_progress[name]["status"] = "failed"
                task_progress[name]["end"] = time.time()
            return False

        logging.info(f"Completed task: {name}")
        console.print(f"[Task] Completed: {name}", style="green")
        with progress_lock:
            task_progress[name]["status"] = "completed"
            task_progress[name]["end"] = time.time()
        return True

    except Exception as e:
        logging.error(f"Exception during task '{name}': {str(e)}")
        console.print(f"[Exception] {name} - {str(e)}", style="red")
        with progress_lock:
            task_progress[name]["status"] = "failed"
            task_progress[name]["end"] = time.time()
        return False

def schedule_tasks(tasks):
    """Schedule and execute tasks based on dependencies using a ThreadPoolExecutor."""
    task_dict = {task["name"]: task for task in tasks}
    dependency_count = {}
    dependents = {}
    for task in tasks:
        name = task["name"]
        deps = task.get("dependencies", [])
        dependency_count[name] = len(deps)
        for dep in deps:
            dependents.setdefault(dep, []).append(name)
    ready_tasks = [name for name, count in dependency_count.items() if count == 0]
    
    results = {}
    futures = {}
    with ThreadPoolExecutor(max_workers=os.cpu_count()) as executor:
        progress_rich = Progress(
            SpinnerColumn(),
            "[progress.description]{task.description}",
            BarColumn(),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%")
        )
        overall_task = progress_rich.add_task("[bold green]Executing Tasks...", total=len(tasks))
        with progress_rich:
            for name in ready_tasks:
                task_item = task_dict[name]
                fut = executor.submit(execute_task, task_item)
                futures[fut] = name
            while futures:
                for fut in as_completed(list(futures.keys())):
                    task_name = futures[fut]
                    try:
                        success = fut.result()
                        results[task_name] = success
                    except Exception as e:
                        logging.error(f"Task '{task_name}' raised exception: {e}")
                        results[task_name] = False
                    progress_rich.advance(overall_task)
                    for dependent in dependents.get(task_name, []):
                        dependency_count[dependent] -= 1
                        if dependency_count[dependent] == 0:
                            dep_task = task_dict[dependent]
                            new_future = executor.submit(execute_task, dep_task)
                            futures[new_future] = dependent
                    del futures[fut]
        progress_rich.update(overall_task, completed=len(tasks))
    return results

# ------------------------------------------------------------------------------
# Main Execution
# ------------------------------------------------------------------------------
def main():
    console.print("[Info] Loading tasks from configuration...", style="cyan")
    CONFIG_FILE = "tasks.yaml"   # Ensure this file exists
    tasks = load_tasks(CONFIG_FILE)
    
    # Initialize task progress for each task.
    for task in tasks:
        name = task.get("name", "Unnamed Task")
        with progress_lock:
            task_progress[name] = {
                "status": "pending",
                "start": None,
                "end": None,
                "group": task.get("group", "Ungrouped"),
                "dependencies": task.get("dependencies", [])
            }
    
    console.print("[Info] Validating base directories...", style="cyan")
    base_dir = "/mnt/c/Users/ACER/Documents/BEunixUb - Setup Standard"
    if not os.path.exists(base_dir):
        console.print(f"[Error] Base directory {base_dir} not found.", style="bold red")
        logging.error(f"Base directory {base_dir} not found.")
        sys.exit(1)
    
    console.print("[Info] Starting task execution...", style="cyan")
    start_time = time.time()
    
    # Start live Gantt chart updater thread.
    gantt_thread = threading.Thread(target=gantt_updater_loop, args=(tasks,), daemon=True)
    gantt_thread.start()
    
    results = schedule_tasks(tasks)
    gantt_thread.join()
    
    duration = time.time() - start_time
    summary_table = Table(title="Task Execution Summary")
    summary_table.add_column("Task Name", justify="left", style="bold")
    summary_table.add_column("Status", justify="center")
    for name, status in results.items():
        summary_table.add_row(name, "[green]Success" if status else "[red]Failed")
    console.print(summary_table)
    
    console.print(f"[Info] Total execution time: {duration:.2f} seconds", style="cyan")
    logging.info(f"Total execution time: {duration:.2f} seconds")
    
    console.print("\n[Info] Consider further enhancements using these frameworks and methodologies:", style="cyan")
    console.print(" - Frontend: react, vue")
    console.print(" - Backend: nestjs, koa")
    console.print(" - Project Management: BRM, CPM, CCPM, EVM, Iterative & Incremental, Agile, DSDM, Extreme PM, Innovation Engineering", style="cyan")
    
    gantt_chart_file = os.path.join(OUTPUT_DIR, "gantt_chart.html")
    open_file(gantt_chart_file)

if __name__ == "__main__":
    main()
