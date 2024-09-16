import os
import sys
import time
import random
import hashlib
from datetime import datetime

class BootcampOS:
    def __init__(self):
        self.current_dir = "/"
        self.file_system = {"/": {"home": {}, "etc": {"passwd": "", "group": ""}, "var": {}, "usr": {"bin": {}}}}
        self.running = True
        self.packages = ["base", "base-devel", "linux", "linux-firmware", "networkmanager", "grub", "vim", "git", "yay"]
        self.installed_packages = ["base", "linux", "networkmanager"]
        self.users = {"root": {"password": self.hash_password("toor"), "groups": ["wheel"]}}
        self.current_user = "root"
        self.hostname = "bootcamp"
        self.init_system = "systemd"
        self.system_time = datetime.now()

    def run(self):
        self.boot_sequence()
        while self.running:
            command = input(f"[{self.current_user}@{self.hostname} {self.current_dir}]$ ").strip().split()
            if not command:
                continue
            
            cmd = command[0]
            args = command[1:]

            if cmd == "exit":
                self.cmd_exit()
            elif cmd == "echo":
                self.cmd_echo(args)
            elif cmd == "ls":
                self.cmd_ls(args)
            elif cmd == "cd":
                self.cmd_cd(args)
            elif cmd == "mkdir":
                self.cmd_mkdir(args)
            elif cmd == "touch":
                self.cmd_touch(args)
            elif cmd == "cat":
                self.cmd_cat(args)
            elif cmd == "rm":
                self.cmd_rm(args)
            elif cmd == "clear":
                self.cmd_clear()
            elif cmd == "pacman":
                self.cmd_pacman(args)
            elif cmd == "makepkg":
                self.cmd_makepkg()
            elif cmd == "useradd":
                self.cmd_useradd(args)
            elif cmd == "userdel":
                self.cmd_userdel(args)
            elif cmd == "passwd":
                self.cmd_passwd(args)
            elif cmd == "su":
                self.cmd_su(args)
            elif cmd == "neofetch":
                self.cmd_neofetch()
            elif cmd == "systemctl":
                self.cmd_systemctl(args)
            elif cmd == "uname":
                self.cmd_uname(args)
            elif cmd == "grep":
                self.cmd_grep(args)
            elif cmd == "nano":
                self.cmd_nano(args)
            elif cmd == "date":
                self.cmd_date(args)
            elif cmd == "timedatectl":
                self.cmd_timedatectl(args)
            elif cmd == "hostnamectl":
                self.cmd_hostnamectl(args)
            elif cmd == "help":
                self.cmd_help()
            else:
                print(f"Command not found: {cmd}. Try 'pacman -S {cmd}' to install it.")

    def boot_sequence(self):
        print("Booting BootcampOS...")
        for i in range(5):
            print(".", end="", flush=True)
            time.sleep(0.5)
        print("\nWelcome to BootcampOS!")
        print("Type 'neofetch' for system info or 'help' for available commands.")

    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def cmd_exit(self):
        print("Shutting down BootcampOS...")
        self.running = False

    def cmd_echo(self, args):
        print(" ".join(args))

    def cmd_ls(self, args):
        path = self.current_dir if not args else args[0]
        current = self.get_dir(path)
        if current is None:
            print(f"Directory not found: {path}")
            return
        for item in current:
            if isinstance(current[item], dict):
                print(f"\033[1;34m{item}/\033[0m")
            else:
                print(item)

    def cmd_cd(self, args):
        if not args:
            self.current_dir = "/"
        elif args[0] == "..":
            if self.current_dir != "/":
                self.current_dir = "/".join(self.current_dir.split("/")[:-1])
                if not self.current_dir:
                    self.current_dir = "/"
        else:
            new_dir = os.path.normpath(os.path.join(self.current_dir, args[0]))
            if self.dir_exists(new_dir):
                self.current_dir = new_dir
            else:
                print(f"Directory not found: {args[0]}")

    def cmd_mkdir(self, args):
        if not args:
            print("Usage: mkdir <directory_name>")
            return
        current = self.get_current_dir()
        if args[0] in current:
            print(f"Directory already exists: {args[0]}")
        else:
            current[args[0]] = {}

    def cmd_touch(self, args):
        if not args:
            print("Usage: touch <file_name>")
            return
        current = self.get_current_dir()
        if args[0] in current:
            print(f"File already exists: {args[0]}")
        else:
            current[args[0]] = ""

    def cmd_cat(self, args):
        if not args:
            print("Usage: cat <file_name>")
            return
        current = self.get_current_dir()
        if args[0] in current and not isinstance(current[args[0]], dict):
            print(current[args[0]])
        else:
            print(f"File not found: {args[0]}")

    def cmd_rm(self, args):
        if not args:
            print("Usage: rm <file_or_directory_name>")
            return
        current = self.get_current_dir()
        if args[0] in current:
            del current[args[0]]
            print(f"Removed: {args[0]}")
        else:
            print(f"File or directory not found: {args[0]}")

    def cmd_clear(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def cmd_pacman(self, args):
        if not args:
            print("Usage: pacman <operation> [...]")
            return
        if args[0] == "-S":
            if len(args) < 2:
                print("Error: No targets specified")
                return
            for pkg in args[1:]:
                if pkg in self.packages:
                    if pkg not in self.installed_packages:
                        print(f"Installing {pkg}...")
                        time.sleep(1)
                        self.installed_packages.append(pkg)
                        print(f"{pkg} installed successfully.")
                    else:
                        print(f"{pkg} is already installed.")
                else:
                    print(f"Package not found: {pkg}")
        elif args[0] == "-Syu":
            print("Updating system...")
            time.sleep(2)
            print("System is up to date.")
        elif args[0] == "-Ss":
            if len(args) < 2:
                print("Error: No search term specified")
                return
            for pkg in self.packages:
                if args[1] in pkg:
                    print(pkg)
        elif args[0] == "-R":
            if len(args) < 2:
                print("Error: No targets specified")
                return
            for pkg in args[1:]:
                if pkg in self.installed_packages:
                    print(f"Removing {pkg}...")
                    time.sleep(1)
                    self.installed_packages.remove(pkg)
                    print(f"{pkg} removed successfully.")
                else:
                    print(f"{pkg} is not installed.")
        else:
            print(f"Unknown operation: {args[0]}")

    def cmd_makepkg(self):
        print("Building package...")
        time.sleep(2)
        print("Package built successfully.")

    def cmd_useradd(self, args):
        if len(args) != 1:
            print("Usage: useradd <username>")
            return
        if args[0] in self.users:
            print(f"User {args[0]} already exists.")
        else:
            password = input(f"Enter password for {args[0]}: ")
            self.users[args[0]] = {"password": self.hash_password(password), "groups": []}
            print(f"User {args[0]} created successfully.")

    def cmd_userdel(self, args):
        if len(args) != 1:
            print("Usage: userdel <username>")
            return
        if args[0] in self.users and args[0] != "root":
            del self.users[args[0]]
            print(f"User {args[0]} deleted successfully.")
        else:
            print(f"User {args[0]} does not exist or cannot be deleted.")

    def cmd_passwd(self, args):
        if not args:
            user = self.current_user
        else:
            user = args[0]
        if user in self.users:
            new_password = input(f"Enter new password for {user}: ")
            self.users[user]["password"] = self.hash_password(new_password)
            print(f"Password updated for {user}.")
        else:
            print(f"User {user} does not exist.")

    def cmd_su(self, args):
        if not args:
            self.current_user = "root"
        elif args[0] in self.users:
            password = input("Password: ")
            if self.users[args[0]]["password"] == self.hash_password(password):
                self.current_user = args[0]
            else:
                print("Incorrect password.")
        else:
            print(f"User {args[0]} does not exist.")

    def cmd_neofetch(self):
        ascii_art = """
         /\\
        /  \\
       /\\   \\
      /  __  \\
     /  (  )  \\
    / __|  |__\\\\
   /.`        `.\\ 
        """
        print(ascii_art)
        print(f"OS: BootcampOS")
        print(f"Kernel: Linux 5.13.13-bootcamp1-1")
        print(f"Uptime: {random.randint(1, 100)} mins")
        print(f"Packages: {len(self.installed_packages)}")
        print(f"Shell: bash 5.1.8")
        print(f"Resolution: 1920x1080")
        print(f"DE: None")
        print(f"WM: i3")
        print(f"Theme: Arc-Dark [GTK2/3]")
        print(f"Terminal: alacritty")
        print(f"CPU: AMD Ryzen 9 5950X (32) @ 3.400GHz")
        print(f"GPU: NVIDIA GeForce RTX 3080")
        print(f"Memory: 1234MiB / 32768MiB")

    def cmd_systemctl(self, args):
        if not args:
            print("Usage: systemctl <command> [service]")
            return
        if args[0] == "start":
            print(f"Starting {args[1]}...")
        elif args[0] == "stop":
            print(f"Stopping {args[1]}...")
        elif args[0] == "restart":
            print(f"Restarting {args[1]}...")
        elif args[0] == "status":
            print(f"{args[1]} is running")
        else:
            print(f"Unknown systemctl command: {args[0]}")

    def cmd_uname(self, args):
        if "-a" in args:
            print(f"Linux {self.hostname} 5.13.13-bootcamp1-1 #1 SMP PREEMPT Thu, 21 Oct 2021 22:50:27 +0000 x86_64 GNU/Linux")
        else:
            print("Linux")

    def cmd_grep(self, args):
        if len(args) < 2:
            print("Usage: grep <pattern> <file>")
            return
        pattern, filename = args[0], args[1]
        current = self.get_current_dir()
        if filename in current and not isinstance(current[filename], dict):
            content = current[filename]
            for line in content.split("\n"):
                if pattern in line:
                    print(line)
        else:
            print(f"File not found: {filename}")

    def cmd_nano(self, args):
        if not args:
            print("Usage: nano <filename>")
            return
        filename = args[0]
        current = self.get_current_dir()
        if filename not in current or isinstance(current[filename], dict):
            current[filename] = ""
        content = current[filename]
        print(f"Editing {filename}. Press Ctrl+C to save and exit.")
        try:
            new_content = input(f"{content}")
            current[filename] = new_content
            print(f"File {filename} saved.")
        except KeyboardInterrupt:
            print("\nFile saved.")

    def cmd_date(self, args):
        print(self.system_time.strftime("%a %b %d %H:%M:%S %Z %Y"))

    def cmd_timedatectl(self, args):
        if not args:
            print(f"               Local time: {self.system_time.strftime('%a %Y-%m-%d %H:%M:%S %Z')}")
            print(f"           Universal time: {self.system_time.strftime('%a %Y-%m-%d %H:%M:%S UTC')}")
            print(f"                 RTC time: {self.system_time.strftime('%a %Y-%m-%d %H:%M:%S')}")
            print(f"                Time zone: UTC (UTC, +0000)")
            print(f"System clock synchronized: yes")
            print(f"              NTP service: active")
            print(f"          RTC in local TZ: no")
        elif args[0] == "set-time":
            try:
                self.system_time = datetime.strptime(args[1], "%Y-%m-%d %H:%M:%S")
                print(f"System time set to: {self.system_time.strftime('%a %Y-%m-%d %H:%M:%S %Z')}")
            except ValueError:
                print("Invalid time format. Use: YYYY-MM-DD HH:MM:SS")

    def cmd_hostnamectl(self, args):
        if not args:
            print(f"   Static hostname: {self.hostname}")
            print(f"         Icon name: computer-vm")
            print(f"           Chassis: vm")
            print(f"        Machine ID: 1234567890abcdef1234567890abcdef")
            print(f"           Boot ID: 1234567890abcdef1234567890abcdef")
            print(f"  Operating System: BootcampOS")
            print(f"       CPE OS Name: cpe:/o:bootcamp:bootcampos:1")
            print(f"            Kernel: Linux 5.13.13-bootcamp1-1")
            print(f"      Architecture: x86-64")
        elif args[0] == "set-hostname":
            if len(args) == 2:
                self.hostname = args[1]
                print(f"Hostname set to: {self.hostname}")
            else:
                print("Usage: hostnamectl set-hostname <new-hostname>")

    def cmd_help(self):
        print("Available commands:")
        print("  cd, ls, mkdir, touch, cat, rm, echo, clear")
        print("  pacman, makepkg, useradd, userdel, passwd, su")
        print("  neofetch, systemctl, uname, grep, nano")
        print("  date, timedatectl, hostnamectl")
        print("  exit")

    def get_current_dir(self):
        return self.get_dir(self.current_dir)

    def get_dir(self, path):
        current = self.file_system
        for dir in path.split("/"):
            if dir:
                if dir in current and isinstance(current[dir], dict):
                    current = current[dir]
                else:
                    return None
        return current

    def dir_exists(self, path):
        return self.get_dir(path) is not None

if __name__ == "__main__":
    BootcampOS().run()
