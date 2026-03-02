#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Kiro Custom Model Hijacker - Interactive Menu
Modern CLI interface with colors and ASCII art
"""

import os
import sys
import subprocess
import platform
import time
import signal

try:
    from colorama import init, Fore, Back, Style
    init(autoreset=True)
except ImportError:
    print("Installing colorama...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "colorama"])
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
    """Print the main menu"""
    print(f"\n{Fore.CYAN}{'─' * 79}{Style.RESET_ALL}\n")
    
    menu_items = [
        (1, "Start Basic Proxy Server", "Simple HTTP proxy - May not work with HTTPS", Fore.GREEN, ""),
        (2, "Start Advanced HTTPS Proxy", "Intercepts HTTPS traffic - Requires certificate", Fore.YELLOW, f"{Back.YELLOW}{Fore.BLACK}RECOMMENDED{Style.RESET_ALL}"),
        (3, "Install SSL Certificate", "Required for HTTPS interception", Fore.BLUE, ""),
        (4, "Setup Hosts File Redirect", "Redirects api.github.com to localhost", Fore.YELLOW, f"{Fore.YELLOW}[MEDIUM RISK]{Style.RESET_ALL}"),
        (5, "Patch Kiro Files", "Directly modifies Kiro installation", Fore.RED, f"{Fore.RED}[HIGH RISK]{Style.RESET_ALL}"),
        (6, "Restore Hosts File", "Restore from backup", Fore.GREEN, ""),
        (7, "Install Dependencies", "Install required Python packages", Fore.BLUE, ""),
        (8, "Test Custom API", "Check if your API is running", Fore.MAGENTA, ""),
        (9, "View Logs", "Display proxy server logs", Fore.CYAN, ""),
        (0, "Exit", "Close the application", Fore.RED, ""),
    ]
    
    for num, title, desc, color, badge in menu_items:
        if badge:
            print(f"  {color}[{num}]{Style.RESET_ALL}  {Fore.WHITE}{title}{Style.RESET_ALL} {badge}")
        else:
            print(f"  {color}[{num}]{Style.RESET_ALL}  {Fore.WHITE}{title}{Style.RESET_ALL}")
        print(f"       {Fore.LIGHTBLACK_EX}{desc}{Style.RESET_ALL}\n")
    
    print(f"{Fore.CYAN}{'─' * 79}{Style.RESET_ALL}\n")


def print_header(title, color=Fore.CYAN):
    """Print a section header"""
    clear_screen()
    print(f"\n{color}{'═' * 79}{Style.RESET_ALL}")
    print(f"{color}{title.center(79)}{Style.RESET_ALL}")
    print(f"{color}{'═' * 79}{Style.RESET_ALL}\n")


def print_info(message, lang="EN"):
    """Print an info message"""
    icon = "ℹ" if lang == "EN" else "ℹ"
    print(f"{Fore.CYAN}[{icon} INFO]{Style.RESET_ALL} {message}")


def print_success(message):
    """Print a success message"""
    print(f"{Fore.GREEN}[✓ SUCCESS]{Style.RESET_ALL} {message}")


def print_warning(message):
    """Print a warning message"""
    print(f"{Fore.YELLOW}[⚠ WARNING]{Style.RESET_ALL} {message}")


def print_error(message):
    """Print an error message"""
    print(f"{Fore.RED}[✗ ERROR]{Style.RESET_ALL} {message}")


def print_tip(message):
    """Print a tip message"""
    print(f"{Fore.MAGENTA}[💡 TIP]{Style.RESET_ALL} {message}")


def run_command(command, shell=True):
    """Run a shell command"""
    try:
        result = subprocess.run(command, shell=shell, check=True)
        return result.returncode == 0
    except subprocess.CalledProcessError:
        return False


def option_basic_proxy():
    """Start basic proxy server"""
    print_header("PROXY SERVER MODE", Fore.GREEN)
    
    print_info("[EN] Starting proxy server on http://localhost:8080")
    print_info("[TR] Proxy sunucusu http://localhost:8080 adresinde başlatılıyor")
    print()
    
    print_info("[EN] This will intercept Kiro's API requests")
    print_info("[TR] Bu, Kiro'nun API isteklerini yakalayacak")
    print()
    
    print(f"{Fore.MAGENTA}[API]{Style.RESET_ALL} Your custom API: {Fore.BLUE}http://localhost:20128/v1{Style.RESET_ALL}")
    print()
    
    print_tip("[EN] Press Ctrl+C to stop the proxy server")
    print_tip("[TR] Proxy sunucusunu durdurmak için Ctrl+C basın")
    print()
    
    print(f"{Fore.CYAN}{'─' * 79}{Style.RESET_ALL}\n")
    
    print_warning("[EN] After starting proxy, run Kiro with these environment variables:")
    print_warning("[TR] Proxy'yi başlattıktan sonra Kiro'yu şu ortam değişkenleriyle çalıştırın:")
    print()
    print(f'{Fore.BLUE}  $env:HTTPS_PROXY="http://localhost:8080"{Style.RESET_ALL}')
    print(f'{Fore.BLUE}  $env:HTTP_PROXY="http://localhost:8080"{Style.RESET_ALL}')
    print(f'{Fore.BLUE}  & "C:\\Users\\user\\AppData\\Local\\Programs\\Kiro\\Kiro.exe"{Style.RESET_ALL}')
    print()
    
    input(f"{Fore.YELLOW}Press Enter to start...{Style.RESET_ALL}")
    
    try:
        subprocess.run([sys.executable, "proxy_server.py"])
    except KeyboardInterrupt:
        print_info("\n[EN] Proxy server stopped")
        print_info("[TR] Proxy sunucusu durduruldu")
    
    input(f"\n{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")


def option_advanced_proxy():
    """Start advanced HTTPS proxy"""
    print_header("ADVANCED HTTPS PROXY MODE", Fore.YELLOW)
    
    print_info("[EN] Starting advanced HTTPS proxy with SSL interception")
    print_info("[TR] SSL yakalama ile gelişmiş HTTPS proxy başlatılıyor")
    print()
    
    print_info("[EN] This proxy can intercept HTTPS traffic (including AWS requests)")
    print_info("[TR] Bu proxy HTTPS trafiğini yakalayabilir (AWS istekleri dahil)")
    print()
    
    print_warning("[EN] You must install SSL certificate first (Option 3)")
    print_warning("[TR] Önce SSL sertifikasını kurmalısınız (Seçenek 3)")
    print()
    
    print(f"{Fore.MAGENTA}[API]{Style.RESET_ALL} Your custom API: {Fore.BLUE}http://localhost:20128/v1{Style.RESET_ALL}")
    print()
    
    print_tip("[EN] Press Ctrl+C to stop the proxy server")
    print_tip("[TR] Proxy sunucusunu durdurmak için Ctrl+C basın")
    print()
    
    print(f"{Fore.CYAN}{'─' * 79}{Style.RESET_ALL}\n")
    
    input(f"{Fore.YELLOW}Press Enter to start...{Style.RESET_ALL}")
    
    try:
        subprocess.run([sys.executable, "advanced_proxy.py"])
    except KeyboardInterrupt:
        print_info("\n[EN] Proxy server stopped")
        print_info("[TR] Proxy sunucusu durduruldu")
    
    input(f"\n{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")


def option_install_cert():
    """Install SSL certificate"""
    print_header("INSTALL SSL CERTIFICATE", Fore.BLUE)
    
    print_info("[EN] Installing mitmproxy SSL certificate...")
    print_info("[TR] mitmproxy SSL sertifikası kuruluyor...")
    print()
    
    print_info("[EN] This allows the proxy to intercept HTTPS traffic")
    print_info("[TR] Bu, proxy'nin HTTPS trafiğini yakalamasını sağlar")
    print()
    
    print(f"{Fore.YELLOW}[STEPS]{Style.RESET_ALL}")
    print(f"  {Fore.MAGENTA}1.{Style.RESET_ALL} Run advanced proxy once to generate certificate")
    print(f"  {Fore.MAGENTA}1.{Style.RESET_ALL} Sertifika oluşturmak için advanced proxy'yi bir kez çalıştırın")
    print()
    print(f"  {Fore.MAGENTA}2.{Style.RESET_ALL} Install certificate to Windows trusted store")
    print(f"  {Fore.MAGENTA}2.{Style.RESET_ALL} Sertifikayı Windows güvenilir deposuna yükleyin")
    print()
    
    print(f"{Fore.CYAN}{'─' * 79}{Style.RESET_ALL}\n")
    
    input(f"{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")
    
    if platform.system() == "Windows":
        subprocess.run([
            "powershell", "-Command",
            "Start-Process powershell -ArgumentList '-ExecutionPolicy Bypass -File install_cert.ps1' -Verb RunAs"
        ])
    
    input(f"\n{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")


def option_hosts_redirect():
    """Setup hosts file redirect"""
    print_header("HOSTS FILE REDIRECT MODE", Fore.YELLOW)
    
    print_warning("[EN] This will modify your Windows hosts file!")
    print_warning("[TR] Bu, Windows hosts dosyanızı değiştirecek!")
    print()
    
    print_info("[EN] What it does:")
    print_info("[TR] Ne yapar:")
    print(f"  {Fore.MAGENTA}•{Style.RESET_ALL} Redirects api.github.com to localhost")
    print(f"  {Fore.MAGENTA}•{Style.RESET_ALL} Creates backup before modification")
    print(f"  {Fore.MAGENTA}•{Style.RESET_ALL} Requires administrator privileges")
    print()
    
    print_warning("[EN] After this, ALL GitHub API requests will go to localhost:8080")
    print_warning("[TR] Bundan sonra TÜM GitHub API istekleri localhost:8080'e gidecek")
    print()
    
    print(f"{Fore.CYAN}{'─' * 79}{Style.RESET_ALL}\n")
    
    confirm = input(f"{Fore.YELLOW}Continue? (Y/N) / Devam? (E/H): {Style.RESET_ALL}").strip().upper()
    
    if confirm in ['Y', 'E']:
        print_info("[EN] Running with administrator privileges...")
        print_info("[TR] Yönetici yetkileriyle çalıştırılıyor...")
        
        if platform.system() == "Windows":
            subprocess.run([
                "powershell", "-Command",
                "Start-Process powershell -ArgumentList '-ExecutionPolicy Bypass -File setup_hosts.ps1' -Verb RunAs"
            ])
        
        print()
        print_success("[EN] Hosts file updated! Now start the proxy server (Option 1)")
        print_success("[TR] Hosts dosyası güncellendi! Şimdi proxy sunucusunu başlatın (Seçenek 1)")
    
    input(f"\n{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")


def option_patch_kiro():
    """Patch Kiro files"""
    print_header("PATCH KIRO FILES MODE", Fore.RED)
    
    print_warning("[EN] HIGH RISK WARNING")
    print_warning("[TR] YÜKSEK RİSK UYARISI")
    print()
    
    print_warning("[EN] This will DIRECTLY MODIFY Kiro installation files!")
    print_warning("[TR] Bu, Kiro kurulum dosyalarını DOĞRUDAN DEĞİŞTİRECEK!")
    print()
    
    print_info("[EN] What it does:")
    print_info("[TR] Ne yapar:")
    print(f"  {Fore.MAGENTA}•{Style.RESET_ALL} Modifies product.json")
    print(f"  {Fore.MAGENTA}•{Style.RESET_ALL} Patches extension JavaScript files")
    print(f"  {Fore.MAGENTA}•{Style.RESET_ALL} Creates .backup files before modification")
    print(f"  {Fore.MAGENTA}•{Style.RESET_ALL} May break Kiro updates")
    print()
    
    print_warning("[EN] Use this ONLY if proxy method doesn't work!")
    print_warning("[TR] Bunu SADECE proxy yöntemi çalışmazsa kullanın!")
    print()
    
    print(f"{Fore.CYAN}{'─' * 79}{Style.RESET_ALL}\n")
    
    confirm = input(f"{Fore.RED}Are you SURE? (Y/N) / EMİN misiniz? (E/H): {Style.RESET_ALL}").strip().upper()
    
    if confirm in ['Y', 'E']:
        print_info("[EN] Patching Kiro files...")
        print_info("[TR] Kiro dosyaları yamalanıyor...")
        
        if run_command([sys.executable, "patch_kiro.py"], shell=False):
            print()
            print_success("[EN] Done! Now start the proxy server and restart Kiro")
            print_success("[TR] Tamamlandı! Şimdi proxy sunucusunu başlatın ve Kiro'yu yeniden başlatın")
        else:
            print_error("[EN] Failed to patch Kiro files")
            print_error("[TR] Kiro dosyaları yamalanırken hata oluştu")
    
    input(f"\n{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")


def option_restore_hosts():
    """Restore hosts file"""
    print_header("RESTORE HOSTS FILE", Fore.GREEN)
    
    print_info("[EN] Restoring hosts file from backup...")
    print_info("[TR] Hosts dosyası yedekten geri yükleniyor...")
    print()
    
    if platform.system() == "Windows":
        subprocess.run([
            "powershell", "-Command",
            "Start-Process powershell -ArgumentList '-ExecutionPolicy Bypass -File restore_hosts.ps1' -Verb RunAs"
        ])
    
    print()
    print_success("[EN] Hosts file restored! Restart Kiro to apply changes.")
    print_success("[TR] Hosts dosyası geri yüklendi! Değişiklikleri uygulamak için Kiro'yu yeniden başlatın.")
    
    input(f"\n{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")


def option_install_deps():
    """Install dependencies"""
    print_header("INSTALL DEPENDENCIES", Fore.BLUE)
    
    print_info("[EN] Installing required Python packages...")
    print_info("[TR] Gerekli Python paketleri yükleniyor...")
    print()
    
    print_info("[EN] Packages: flask, requests, mitmproxy, colorama")
    print_info("[TR] Paketler: flask, requests, mitmproxy, colorama")
    print()
    
    print(f"{Fore.CYAN}{'─' * 79}{Style.RESET_ALL}\n")
    
    if run_command([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], shell=False):
        print()
        print_success("[EN] Installation complete!")
        print_success("[TR] Kurulum tamamlandı!")
    else:
        print_error("[EN] Installation failed")
        print_error("[TR] Kurulum başarısız")
    
    input(f"\n{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")


def option_test_api():
    """Test custom API"""
    print_header("TEST CUSTOM API", Fore.MAGENTA)
    
    print_info(f"[EN] Testing your custom API at {Fore.BLUE}http://localhost:20128/v1{Style.RESET_ALL}")
    print_info(f"[TR] Özel API'niz test ediliyor: {Fore.BLUE}http://localhost:20128/v1{Style.RESET_ALL}")
    print()
    
    print(f"{Fore.CYAN}{'─' * 79}{Style.RESET_ALL}\n")
    
    try:
        result = subprocess.run(
            ['curl', '-X', 'GET', 'http://localhost:20128/v1/models',
             '-H', 'Authorization: Bearer sk-c2cfde71bf830c3f-jh40ri-38f2a287'],
            capture_output=True,
            timeout=5
        )
        
        if result.returncode == 0:
            print_success("[EN] API is running!")
            print_success("[TR] API çalışıyor!")
        else:
            print_error("[EN] API is not responding. Make sure it's running on port 20128")
            print_error("[TR] API yanıt vermiyor. Port 20128'de çalıştığından emin olun")
    except Exception as e:
        print_error(f"[EN] Error testing API: {e}")
        print_error(f"[TR] API test edilirken hata: {e}")
    
    input(f"\n{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")


def option_view_logs():
    """View logs"""
    print_header("PROXY SERVER LOGS", Fore.CYAN)
    
    print_info("[EN] Proxy server logs will appear here when running...")
    print_info("[TR] Proxy sunucusu çalışırken loglar burada görünecek...")
    print()
    
    print_tip("[EN] Start proxy server first (Option 1 or 2)")
    print_tip("[TR] Önce proxy sunucusunu başlatın (Seçenek 1 veya 2)")
    print()
    
    input(f"\n{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")


def main():
    """Main menu loop"""
    options = {
        '1': option_basic_proxy,
        '2': option_advanced_proxy,
        '3': option_install_cert,
        '4': option_hosts_redirect,
        '5': option_patch_kiro,
        '6': option_restore_hosts,
        '7': option_install_deps,
        '8': option_test_api,
        '9': option_view_logs,
    }
    
    while True:
        clear_screen()
        print_logo()
        print_menu()
        
        choice = input(f"{Fore.YELLOW}  > Select option: {Style.RESET_ALL}").strip()
        
        if choice == '0':
            clear_screen()
            print(f"\n{Fore.CYAN}{'═' * 79}{Style.RESET_ALL}")
            print(f"{Fore.MAGENTA}{'THANK YOU / TEŞEKKÜRLER'.center(79)}{Style.RESET_ALL}")
            print(f"{Fore.CYAN}{'═' * 79}{Style.RESET_ALL}\n")
            print_success("[EN] Thank you for using Kiro Custom Model Hijacker!")
            print_success("[TR] Kiro Özel Model Yönlendirici'yi kullandığınız için teşekkürler!")
            print()
            print_tip("[EN] Remember to restore hosts file if you used Option 4")
            print_tip("[TR] Seçenek 4'ü kullandıysanız hosts dosyasını geri yüklemeyi unutmayın")
            print()
            break
        
        if choice in options:
            try:
                options[choice]()
            except Exception as e:
                print_error(f"[EN] An error occurred: {e}")
                print_error(f"[TR] Bir hata oluştu: {e}")
                input(f"\n{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")
        else:
            print_error("[EN] Invalid option!")
            print_error("[TR] Geçersiz seçenek!")
            input(f"\n{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{Fore.YELLOW}[EN] Exiting...{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}[TR] Çıkılıyor...{Style.RESET_ALL}")
        sys.exit(0)


