import os
import subprocess
import sys
import time
import socket

# Kill existing electron processes
if sys.platform == "win32":
    os.system("taskkill /f /im electron.exe >nul 2>&1")
else:
    os.system("pkill -9 electron >/dev/null 2>&1")

time.sleep(1)

# Get current environment
env = os.environ.copy()

# Ensure System32 is in PATH
system32 = os.path.join(os.environ.get('SystemRoot', 'C:\\Windows'), 'System32')
if system32 not in env.get('PATH', ''):
    env['PATH'] = system32 + os.pathsep + env.get('PATH', '')

# Ensure the problematic variable is GONE
env.pop('ELECTRON_RUN_AS_NODE', None)
env['ELECTRON_NO_ATTACH_CONSOLE'] = '1'

# Path to electron
electron_path = os.path.abspath('node_modules/electron/dist/electron.exe')
app_path = os.path.abspath('.')

print(f"Launching Electron from: {electron_path}")
print(f"App path: {app_path}")

# Check if frontend is running to prevent blank screen
def is_port_open(port):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(0.5)
            return s.connect_ex(('127.0.0.1', port)) == 0
    except:
        return False

print("Waiting for Frontend (Vite) to start on port 5173...")
max_retries = 60 # Wait up to 30 seconds
server_started = False
for i in range(max_retries):
    if is_port_open(5173):
        print("Frontend is ready!")
        server_started = True
        break
    time.sleep(0.5)
    if i % 10 == 0:
        print(f"Waiting... ({i/2}s)")

if not server_started:
    print("\n[WARNING] Port 5173 is closed! The frontend (React/Vite) failed to start.")
    print("          You will see a BLANK SCREEN. Please run 'npm run dev' manually.\n")

try:
    # Launch electron and stream output to a log file
    log_file = open("electron_log_new.txt", "w")
    process = subprocess.Popen([electron_path, app_path, "--disable-gpu"], env=env, cwd=app_path, stdout=log_file, stderr=log_file)
    print(f"Electron process started with PID {process.pid}.")
    print("Check electron_log_new.txt for detailed startup logs.")
except Exception as e:
    print(f"Failed to start Electron: {e}")
