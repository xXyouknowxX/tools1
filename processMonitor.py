import psutil
import getpass

def list_system_processes():
    system_processes = []

    for proc in psutil.process_iter(['pid', 'name', 'username', 'exe']):
        try:
            if proc.info['username'] == 'NT AUTHORITY\\SYSTEM':
                system_processes.append((proc.info['pid'], proc.info['name'], proc.info['exe']))
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass

    return system_processes

def list_user_processes():
    user_processes = []
    current_user = getpass.getuser()

    for proc in psutil.process_iter(['pid', 'name', 'username', 'exe']):
        try:
            if proc.info['username'] == current_user:
                user_processes.append((proc.info['pid'], proc.info['name'], proc.info['exe']))
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass

    return user_processes

if __name__ == '__main__':
    system_procs = list_system_processes()
    user_procs = list_user_processes()

    if system_procs:
        print("\nProcesses running as SYSTEM:")
        for pid, name, path in system_procs:
            print(f"PID: {pid}, Name: {name}, Path: {path}")
    else:
        print("No processes running as SYSTEM found.")
    
    if user_procs:
        print("\nProcesses running as current user:")
        for pid, name, path in user_procs:
            print(f"PID: {pid} | Name: {name} | Path: {path}")
    else:
        print("No processes running as the current user found.")
