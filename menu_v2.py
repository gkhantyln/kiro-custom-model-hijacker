#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Kiro Custom Model Hijacker v2.0 - Interactive Menu
Modern CLI with background process management
"""

import os
import sys
import subprocess
import platform
import time
import psutil

try:
    from colorama import init, Fore, Back, Style
    init(autoreset=True)
except ImportError:
    print("Installing colorama...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "colorama", "psutil"])
    from colorama import init, Fore, Back, Style
    init(autoreset=True)

# Global process tracking
running_processes = {
    'custom_api': None,
    'proxy': None
}

def clear_screen():
    """Clear the terminal screen"""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_logo():
    """Print ASCII art logo"""
    logo = f"""
{Fore.MAGENTA}    ██╗  ██╗ ██╗ ██████╗   ██████╗ 
{Fore.MAGENTA}    ██║ ██╔╝ ██║ ██╔══██╗ ██╔═══██╗
{Fore.LIGHTMAGENTA_EX}    █████╔╝  ██║ ██████╔╝ ██║   ██║
{Fore.LIGHTMAGENTA_EX}    ██╔═██╗  ██║ ██╔══██╗ ██║   ██║
{Fore.CYAN}    ██║  ██╗ ██║ ██║  ██║ ╚██████╔╝
{Fore.CYAN}    ╚═╝  ╚═╝ ╚═╝ ╚═╝  ╚═╝  ╚═════╝ 
    
{Fore.YELLOW}         Custom Model Hijacker {Fore.CYAN}v2.0{Style.RESET_ALL}

{Fore.WHITE}    Redirects Kiro AI requests to your custom endpoint
{Fore.LIGHTBLACK_EX}    Kiro AI isteklerini özel endpoint'inize yönlendirir{Style.RESET_ALL}
"""
    print(logo)

def print_menu():
    """Print the main menu with server status"""
    print(f"\n{Fore.CYAN}{'─' * 79}{Style.RESET_ALL}\n")
    
    # Quick Start
    print(f"  {Back.GREEN}{Fore.BLACK} Q {Style.RESET_ALL}  {Fore.WHITE}Quick Start - Auto Setup{Style.RESET_ALL} {Fore.GREEN}★ ONE-CLICK{Style.RESET_ALL}")
    print(f"       {Fore.LIGHTBLACK_EX}Start Custom API + Proxy + Show Kiro launch command{Style.RESET_ALL}\n")
    
    print(f"{Fore.CYAN}{'─' * 79}{Style.RESET_ALL}\n")
    
    # Server Status
    api_status = f"{Fore.GREEN}●{Style.RESET_ALL} RUNNING" if is_process_running('custom_api') else f"{Fore.RED}●{Style.RESET_ALL} STOPPED"
    proxy_status = f"{Fore.GREEN}●{Style.RESET_ALL} RUNNING" if is_process_running('proxy') else f"{Fore.RED}●{Style.RESET_ALL} STOPPED"
    
    print(f"  {Fore.YELLOW}SERVER MANAGEMENT{Style.RESET_ALL}\n")
    
    print(f"  {Fore.CYAN}[10]{Style.RESET_ALL}  {Fore.WHITE}Start Custom API{Style.RESET_ALL} {api_status}")
    print(f"       {Fore.LIGHTBLACK_EX}Background server on port 20130{Style.RESET_ALL}\n")
    
    print(f"  {Fore.YELLOW}[2]{Style.RESET_ALL}  {Fore.WHITE}Start HTTPS Proxy{Style.RESET_ALL} {proxy_status} {Fore.YELLOW}[RECOMMENDED]{Style.RESET_ALL}")
    print(f"       {Fore.LIGHTBLACK_EX}Background proxy on port 8082{Style.RESET_ALL}\n")
    
    print(f"  {Fore.RED}[11]{Style.RESET_ALL}  {Fore.WHITE}Stop All Servers{Style.RESET_ALL}")
    print(f"       {Fore.LIGHTBLACK_EX}Terminate all background processes{Style.RESET_ALL}\n")
    
    print(f"  {Fore.RED}[12]{Style.RESET_ALL}  {Fore.WHITE}Kill All Python Processes{Style.RESET_ALL} {Fore.RED}[EMERGENCY]{Style.RESET_ALL}")
    print(f"       {Fore.LIGHTBLACK_EX}Force kill all Python - Use if servers are stuck{Style.RESET_ALL}\n")
    
    print(f"{Fore.CYAN}{'─' * 79}{Style.RESET_ALL}\n")
    
    # Other options
    menu_items = [
        (1, "Start Basic Proxy", "Foreground HTTP proxy", Fore.GREEN),
        (3, "Install SSL Certificate", "Required for HTTPS", Fore.BLUE),
        (4, "Launch Kiro with Proxy", "Auto-launch Kiro IDE", Fore.MAGENTA),
        (7, "Install Dependencies", "Python packages", Fore.BLUE),
        (8, "Test Custom API", "Health check", Fore.MAGENTA),
        (9, "View Server Status", "Show logs & status", Fore.CYAN),
        (0, "Exit", "Close application", Fore.RED),
    ]
    
    for num, title, desc, color in menu_items:
        print(f"  {color}[{num}]{Style.RESET_ALL}  {Fore.WHITE}{title}{Style.RESET_ALL}")
        print(f"       {Fore.LIGHTBLACK_EX}{desc}{Style.RESET_ALL}\n")
    
    print(f"{Fore.CYAN}{'─' * 79}{Style.RESET_ALL}\n")

def is_process_running(process_name):
    """Check if a process is running"""
    if running_processes[process_name] is None:
        return False
    try:
        process = psutil.Process(running_processes[process_name].pid)
        return process.is_running()
    except:
        return False

def start_custom_api():
    """Start Custom API in background"""
    if is_process_running('custom_api'):
        print(f"{Fore.YELLOW}[WARNING]{Style.RESET_ALL} Custom API is already running!")
        return True
    
    print(f"{Fore.CYAN}[INFO]{Style.RESET_ALL} Starting Custom API server...")
    try:
        # Check if custom_api.py exists
        if not os.path.exists("custom_api.py"):
            print(f"{Fore.RED}[ERROR]{Style.RESET_ALL} custom_api.py not found!")
            return False
        
        # Start process
        if os.name == 'nt':  # Windows
            process = subprocess.Popen(
                [sys.executable, "custom_api.py"],
                creationflags=subprocess.CREATE_NEW_CONSOLE
            )
        else:  # Linux/Mac
            process = subprocess.Popen(
                [sys.executable, "custom_api.py"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
        
        running_processes['custom_api'] = process
        time.sleep(3)  # Wait for startup
        
        if is_process_running('custom_api'):
            print(f"{Fore.GREEN}[SUCCESS]{Style.RESET_ALL} Custom API started on port 20128")
            print(f"{Fore.LIGHTBLACK_EX}           Check the new console window for logs{Style.RESET_ALL}")
            return True
        else:
            print(f"{Fore.RED}[ERROR]{Style.RESET_ALL} Process started but not responding")
            print(f"{Fore.YELLOW}[TIP]{Style.RESET_ALL} Try running manually: python custom_api.py")
            return False
    except Exception as e:
        print(f"{Fore.RED}[ERROR]{Style.RESET_ALL} {e}")
        import traceback
        print(f"{Fore.LIGHTBLACK_EX}{traceback.format_exc()}{Style.RESET_ALL}")
        return False

def start_proxy():
    """Start Proxy in background"""
    if is_process_running('proxy'):
        print(f"{Fore.YELLOW}[WARNING]{Style.RESET_ALL} Proxy is already running!")
        return True
    
    print(f"{Fore.CYAN}[INFO]{Style.RESET_ALL} Starting Advanced HTTPS Proxy...")
    try:
        # Check if advanced_proxy.py exists
        if not os.path.exists("advanced_proxy.py"):
            print(f"{Fore.RED}[ERROR]{Style.RESET_ALL} advanced_proxy.py not found!")
            return False
        
        # Start process
        if os.name == 'nt':  # Windows
            process = subprocess.Popen(
                [sys.executable, "advanced_proxy.py"],
                creationflags=subprocess.CREATE_NEW_CONSOLE
            )
        else:  # Linux/Mac
            process = subprocess.Popen(
                [sys.executable, "advanced_proxy.py"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
        
        running_processes['proxy'] = process
        time.sleep(3)  # Wait for startup
        
        if is_process_running('proxy'):
            print(f"{Fore.GREEN}[SUCCESS]{Style.RESET_ALL} Proxy started on port 8082")
            print(f"{Fore.LIGHTBLACK_EX}           Check the new console window for logs{Style.RESET_ALL}")
            return True
        else:
            print(f"{Fore.RED}[ERROR]{Style.RESET_ALL} Process started but not responding")
            print(f"{Fore.YELLOW}[TIP]{Style.RESET_ALL} Try running manually: python advanced_proxy.py")
            return False
    except Exception as e:
        print(f"{Fore.RED}[ERROR]{Style.RESET_ALL} {e}")
        import traceback
        print(f"{Fore.LIGHTBLACK_EX}{traceback.format_exc()}{Style.RESET_ALL}")
        return False

def stop_all_servers():
    """Stop all running servers"""
    print(f"{Fore.CYAN}[INFO]{Style.RESET_ALL} Stopping all servers...")
    
    stopped = 0
    for name, process in running_processes.items():
        if process and is_process_running(name):
            try:
                parent = psutil.Process(process.pid)
                for child in parent.children(recursive=True):
                    child.terminate()
                parent.terminate()
                parent.wait(timeout=3)
                print(f"{Fore.GREEN}[SUCCESS]{Style.RESET_ALL} Stopped {name}")
                stopped += 1
            except:
                try:
                    parent.kill()
                except:
                    pass
            running_processes[name] = None
    
    if stopped == 0:
        print(f"{Fore.YELLOW}[INFO]{Style.RESET_ALL} No servers were running")
    else:
        print(f"{Fore.GREEN}[SUCCESS]{Style.RESET_ALL} Stopped {stopped} server(s)")

def kill_all_python():
    """Emergency: Kill all Python processes"""
    print(f"{Fore.RED}[WARNING]{Style.RESET_ALL} This will kill ALL Python processes!")
    print(f"{Fore.YELLOW}[INFO]{Style.RESET_ALL} Including this menu (it will close)")
    print()
    
    confirm = input(f"{Fore.RED}Are you sure? (yes/no): {Style.RESET_ALL}").strip().lower()
    
    if confirm == 'yes':
        print(f"\n{Fore.CYAN}[INFO]{Style.RESET_ALL} Killing all Python processes...")
        
        try:
            if os.name == 'nt':  # Windows
                result = subprocess.run(['taskkill', '/F', '/IM', 'python.exe'], 
                                      capture_output=True, text=True)
                print(result.stdout)
                if result.returncode == 0:
                    print(f"{Fore.GREEN}[SUCCESS]{Style.RESET_ALL} All Python processes killed")
                else:
                    print(f"{Fore.YELLOW}[INFO]{Style.RESET_ALL} No Python processes found or already killed")
            else:  # Linux/Mac
                subprocess.run(['pkill', '-9', 'python'])
                print(f"{Fore.GREEN}[SUCCESS]{Style.RESET_ALL} All Python processes killed")
            
            # Clear our tracking
            running_processes['custom_api'] = None
            running_processes['proxy'] = None
            
            time.sleep(2)
            sys.exit(0)  # Exit this menu too
            
        except Exception as e:
            print(f"{Fore.RED}[ERROR]{Style.RESET_ALL} {e}")
    else:
        print(f"{Fore.YELLOW}[INFO]{Style.RESET_ALL} Cancelled")

def quick_start():
    """Quick start - Auto setup everything"""
    clear_screen()
    print(f"\n{Fore.GREEN}{'═' * 79}{Style.RESET_ALL}")
    print(f"{Fore.GREEN}{'QUICK START - AUTOMATIC SETUP'.center(79)}{Style.RESET_ALL}")
    print(f"{Fore.GREEN}{'═' * 79}{Style.RESET_ALL}\n")
    
    # Step 1: Start Custom API
    print(f"{Fore.CYAN}[1/3]{Style.RESET_ALL} Starting Custom API...")
    if start_custom_api():
        print(f"      {Fore.GREEN}✓{Style.RESET_ALL} Custom API is ready\n")
    else:
        print(f"      {Fore.RED}✗{Style.RESET_ALL} Failed to start Custom API\n")
        input(f"{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")
        return
    
    # Step 2: Start Proxy
    print(f"{Fore.CYAN}[2/3]{Style.RESET_ALL} Starting HTTPS Proxy...")
    if start_proxy():
        print(f"      {Fore.GREEN}✓{Style.RESET_ALL} Proxy is ready\n")
    else:
        print(f"      {Fore.RED}✗{Style.RESET_ALL} Failed to start Proxy\n")
        input(f"{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")
        return
    
    # Step 3: Launch Kiro
    print(f"{Fore.CYAN}[3/3]{Style.RESET_ALL} Launching Kiro with proxy...")
    if launch_kiro_with_proxy():
        print(f"      {Fore.GREEN}✓{Style.RESET_ALL} Kiro launched successfully\n")
    else:
        print(f"      {Fore.YELLOW}⚠{Style.RESET_ALL} Could not auto-launch Kiro\n")
    
    # Success!
    print(f"\n{Fore.GREEN}{'═' * 79}{Style.RESET_ALL}")
    print(f"{Fore.GREEN}{'✓ ALL SYSTEMS READY!'.center(79)}{Style.RESET_ALL}")
    print(f"{Fore.GREEN}{'═' * 79}{Style.RESET_ALL}\n")
    
    print(f"{Fore.LIGHTBLACK_EX}If Kiro didn't launch automatically, use this command:{Style.RESET_ALL}\n")
    print(f"{Fore.CYAN}PowerShell:{Style.RESET_ALL}")
    
    # Get username
    username = os.environ.get('USERNAME', 'YOUR_USERNAME')
    kiro_path = f'C:\\Users\\{username}\\AppData\\Local\\Programs\\Kiro\\Kiro.exe'
    
    print(f'{Fore.WHITE}  $env:HTTPS_PROXY="http://localhost:8080"{Style.RESET_ALL}')
    print(f'{Fore.WHITE}  $env:HTTP_PROXY="http://localhost:8080"{Style.RESET_ALL}')
    print(f'{Fore.WHITE}  $env:NODE_TLS_REJECT_UNAUTHORIZED="0"{Style.RESET_ALL}')
    print(f'{Fore.WHITE}  & "{kiro_path}"{Style.RESET_ALL}\n')
    
    input(f"{Fore.YELLOW}Press Enter to return to menu...{Style.RESET_ALL}")

def launch_kiro_with_proxy():
    """Launch Kiro with proxy environment variables"""
    try:
        # Get username
        username = os.environ.get('USERNAME', None)
        if not username:
            print(f"{Fore.YELLOW}[WARNING]{Style.RESET_ALL} Could not detect username")
            return False
        
        # Kiro path
        kiro_path = f'C:\\Users\\{username}\\AppData\\Local\\Programs\\Kiro\\Kiro.exe'
        
        # Check if Kiro exists
        if not os.path.exists(kiro_path):
            print(f"{Fore.YELLOW}[WARNING]{Style.RESET_ALL} Kiro not found at: {kiro_path}")
            return False
        
        # Set environment variables and launch
        env = os.environ.copy()
        env['HTTPS_PROXY'] = 'http://localhost:8080'
        env['HTTP_PROXY'] = 'http://localhost:8080'
        env['NODE_TLS_REJECT_UNAUTHORIZED'] = '0'
        
        # Launch Kiro
        subprocess.Popen([kiro_path], env=env)
        
        print(f"{Fore.GREEN}[SUCCESS]{Style.RESET_ALL} Kiro launched with proxy settings")
        time.sleep(2)
        return True
        
    except Exception as e:
        print(f"{Fore.RED}[ERROR]{Style.RESET_ALL} Failed to launch Kiro: {e}")
        return False

def view_status():
    """View server status and logs"""
    clear_screen()
    print(f"\n{Fore.CYAN}{'═' * 79}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'SERVER STATUS'.center(79)}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'═' * 79}{Style.RESET_ALL}\n")
    
    # Custom API Status
    if is_process_running('custom_api'):
        print(f"{Fore.GREEN}● Custom API{Style.RESET_ALL}")
        print(f"  Status: {Fore.GREEN}RUNNING{Style.RESET_ALL}")
        print(f"  Port: 20128")
        print(f"  PID: {running_processes['custom_api'].pid}")
    else:
        print(f"{Fore.RED}● Custom API{Style.RESET_ALL}")
        print(f"  Status: {Fore.RED}STOPPED{Style.RESET_ALL}")
    
    print()
    
    # Proxy Status
    if is_process_running('proxy'):
        print(f"{Fore.GREEN}● HTTPS Proxy{Style.RESET_ALL}")
        print(f"  Status: {Fore.GREEN}RUNNING{Style.RESET_ALL}")
        print(f"  Port: 8082")
        print(f"  PID: {running_processes['proxy'].pid}")
    else:
        print(f"{Fore.RED}● HTTPS Proxy{Style.RESET_ALL}")
        print(f"  Status: {Fore.RED}STOPPED{Style.RESET_ALL}")
    
    print(f"\n{Fore.CYAN}{'─' * 79}{Style.RESET_ALL}\n")
    input(f"{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")

def main():
    """Main menu loop"""
    while True:
        clear_screen()
        print_logo()
        print_menu()
        
        choice = input(f"{Fore.YELLOW}  > Select option: {Style.RESET_ALL}").strip().upper()
        
        if choice == 'Q':
            quick_start()
        elif choice == '10':
            clear_screen()
            print(f"\n{Fore.CYAN}Starting Custom API...{Style.RESET_ALL}\n")
            start_custom_api()
            input(f"\n{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")
        elif choice == '2':
            clear_screen()
            print(f"\n{Fore.CYAN}Starting HTTPS Proxy...{Style.RESET_ALL}\n")
            start_proxy()
            input(f"\n{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")
        elif choice == '11':
            clear_screen()
            print(f"\n{Fore.RED}Stopping all servers...{Style.RESET_ALL}\n")
            stop_all_servers()
            input(f"\n{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")
        elif choice == '12':
            clear_screen()
            print(f"\n{Fore.RED}{'═' * 79}{Style.RESET_ALL}")
            print(f"{Fore.RED}{'EMERGENCY: KILL ALL PYTHON'.center(79)}{Style.RESET_ALL}")
            print(f"{Fore.RED}{'═' * 79}{Style.RESET_ALL}\n")
            kill_all_python()
            input(f"\n{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")
        elif choice == '9':
            view_status()
        elif choice == '4':
            clear_screen()
            print(f"\n{Fore.MAGENTA}Launching Kiro with Proxy...{Style.RESET_ALL}\n")
            launch_kiro_with_proxy()
            input(f"\n{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")
        elif choice == '0':
            clear_screen()
            print(f"\n{Fore.CYAN}{'═' * 79}{Style.RESET_ALL}")
            print(f"{Fore.MAGENTA}{'THANK YOU / TEŞEKKÜRLER'.center(79)}{Style.RESET_ALL}")
            print(f"{Fore.CYAN}{'═' * 79}{Style.RESET_ALL}\n")
            
            # Stop all servers before exit
            if is_process_running('custom_api') or is_process_running('proxy'):
                print(f"{Fore.YELLOW}[INFO]{Style.RESET_ALL} Stopping running servers...\n")
                stop_all_servers()
                print()
            
            print(f"{Fore.GREEN}Thank you for using Kiro Custom Model Hijacker!{Style.RESET_ALL}")
            print(f"{Fore.GREEN}Kiro Özel Model Yönlendirici'yi kullandığınız için teşekkürler!{Style.RESET_ALL}\n")
            break
        else:
            print(f"{Fore.RED}[ERROR]{Style.RESET_ALL} Invalid option!")
            time.sleep(1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{Fore.YELLOW}[INFO]{Style.RESET_ALL} Interrupted by user")
        stop_all_servers()
        sys.exit(0)
