
import subprocess
import time
import os
import signal
import sys
import psutil
import webbrowser
import requests

def kill_process_on_port(port):
    """Finds and kills any process listening on the specified port."""
    for proc in psutil.process_iter(['pid', 'name']):
        try:
            for conn in proc.connections(kind='inet'):
                if conn.laddr.port == port:
                    print(f"[{port}] Killing conflicting process: {proc.info['name']} (PID: {proc.info['pid']})")
                    proc.send_signal(signal.SIGTERM)
                    return
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass

def check_server_ready(url, timeout=30):
    """Polls a URL until it returns 200 OK or timeout."""
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            response = requests.get(url, timeout=1)
            if response.status_code == 200:
                return True
        except requests.ConnectionError:
            pass
        time.sleep(1)
    return False

def main():
    print("==========================================")
    print("      ADA V2 - INTELLIGENT LAUNCHER       ")
    print("==========================================")

    # 1. CLEANUP
    print("\n[1/4] Cleaning up ports and capabilities...")
    kill_process_on_port(8000) # Backend
    kill_process_on_port(5173) # Frontend
    
    # 2. FRONTEND
    print("[2/4] Starting Frontend (Vite)...")
    frontend_process = subprocess.Popen(
        ["npx.cmd", "vite", "--port", "5173"], 
        cwd=os.getcwd(),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    
    # Wait for Vite port to be active
    if check_server_ready("http://localhost:5173", timeout=20):
        print(" -> Frontend is UP (http://localhost:5173)")
    else:
        print(" -> [WARN] Frontend might be slow, proceeding...")

    # 3. BACKEND
    print("[3/4] Starting Backend (Python)...")
    backend_env = os.environ.copy()
    backend_process = subprocess.Popen(
        [os.path.join("venv", "Scripts", "python.exe"), "backend/server.py"],
        cwd=os.getcwd(),
        env=backend_env
    )
    
    # Wait for Backend Health Check
    print(" -> Waiting for Backend initialization...")
    if check_server_ready("http://localhost:8000/status", timeout=20):
         print(" -> Backend is UP (http://localhost:8000)")
    else:
         print(" -> [WARN] Backend didn't respond to status check yet.")

    # 4. LAUNCH
    print("\n[4/4] Launching Interface...")
    print(" -> Opening Chrome...")
    webbrowser.open("http://localhost:5173")
    
    print("\n[SUCCESS] Ada is running.")
    print("Press Ctrl+C to stop servers.")
    
    try:
        while True:
            time.sleep(1)
            if backend_process.poll() is not None:
                print("[ERR] Backend crashed!")
                break
    except KeyboardInterrupt:
        print("\nStopping servers...")
        backend_process.terminate()
        frontend_process.terminate()
        sys.exit(0)

if __name__ == "__main__":
    main()
