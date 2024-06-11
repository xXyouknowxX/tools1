#USAGE : python vmenum.py > INFO.txt
import os

def get_system_info():
    os_type = os.popen("uname -a").read()
    hostname = os.popen("hostname").read()
    return os_type, hostname

def list_users():
    return os.popen("cat /etc/passwd | cut -d: -f1").read()

def list_groups():
    return os.popen("cat /etc/group | cut -d: -f1").read()

def find_suid_files():
    return os.popen("find / -type f -perm -4000 -ls 2>/dev/null").read()

def list_cron_jobs():
    return os.popen("ls -la /etc/cron*").read()

def get_installed_software():
    return os.popen("dpkg -l").read()

def get_network_info():
    return os.popen("ifconfig -a").read()

def check_unattended_upgrades():
    '''Check for the presence of auto-upgrades which could be exploited'''
    if os.path.exists("/etc/apt/apt.conf.d/10periodic"):
        with open("/etc/apt/apt.conf.d/10periodic", "r") as file:
            data = file.read()
            if "APT::Periodic::Update-Package-Lists" in data and "APT::Periodic::Download-Upgradeable-Packages" in data:
                return True
    return False

def check_weak_file_permissions():
    '''Check for world-writable files in critical paths, which can be exploited for privilege escalation'''
    results = os.popen("find /etc /var /usr /home -type f -perm -2 ! -perm -a+t 2>/dev/null").read()
    return results.splitlines()

def main():
    if check_unattended_upgrades():
        print("[!] Found potential vulnerability with unattended upgrades!")

    weak_files = check_weak_file_permissions()
    if weak_files:
        print("[!] Found files with weak file permissions:")
        for file in weak_files:
            print(f"    {file}")

    print("[+] System Information:")
    os_type, hostname = get_system_info()
    print(f"OS: {os_type}")
    print(f"Hostname: {hostname}")

    print("\n[+] Users:")
    print(list_users())

    print("\n[+] Groups:")
    print(list_groups())

    print("\n[+] SUID Files:")
    print(find_suid_files())

    print("\n[+] Cron Jobs:")
    print(list_cron_jobs())

    print("\n[+] Installed Software:")
    print(get_installed_software())

    print("\n[+] Network Configuration:")
    print(get_network_info())

if __name__ == "__main__":
    main()
