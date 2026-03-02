#!/usr/bin/env python3
"""
Kiro Extension Patcher - GitHub Copilot API endpoint'ini değiştirir
"""

import os
import shutil
import re
from pathlib import Path

KIRO_EXTENSION_PATH = r"C:\Users\user\AppData\Local\Programs\Kiro\resources\app\extensions\kiro.kiro-agent"
CUSTOM_API_ENDPOINT = "http://localhost:8080"  # Proxy endpoint

def backup_file(file_path):
    """Dosyayı yedekle"""
    backup_path = f"{file_path}.backup"
    if not os.path.exists(backup_path):
        shutil.copy2(file_path, backup_path)
        print(f"✅ Backup: {backup_path}")
    return backup_path

def patch_product_json():
    """product.json dosyasını patch'le"""
    product_json_path = r"C:\Users\user\AppData\Local\Programs\Kiro\resources\app\product.json"
    
    backup_file(product_json_path)
    
    with open(product_json_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # GitHub API URL'lerini değiştir
    content = content.replace(
        'https://api.github.com',
        CUSTOM_API_ENDPOINT
    )
    
    with open(product_json_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ product.json patched: {product_json_path}")

def patch_extension_files():
    """Extension JS dosyalarını patch'le"""
    dist_path = Path(KIRO_EXTENSION_PATH) / "dist"
    
    if not dist_path.exists():
        print(f"❌ Dist klasörü bulunamadı: {dist_path}")
        return
    
    # Tüm JS dosyalarını tara
    for js_file in dist_path.rglob("*.js"):
        try:
            backup_file(str(js_file))
            
            with open(js_file, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            # GitHub API URL'lerini değiştir
            original_content = content
            content = content.replace(
                'https://api.github.com',
                CUSTOM_API_ENDPOINT
            )
            content = content.replace(
                'api.github.com',
                'localhost:8080'
            )
            
            if content != original_content:
                with open(js_file, 'w', encoding='utf-8', errors='ignore') as f:
                    f.write(content)
                print(f"✅ Patched: {js_file.name}")
        
        except Exception as e:
            print(f"⚠️  Hata ({js_file.name}): {e}")

def main():
    print("🔧 Kiro Extension Patcher")
    print("=" * 50)
    print(f"📁 Extension Path: {KIRO_EXTENSION_PATH}")
    print(f"🎯 Custom Endpoint: {CUSTOM_API_ENDPOINT}")
    print("=" * 50)
    print()
    
    confirm = input("⚠️  Kiro dosyalarını değiştirmek istediğinizden emin misiniz? (Y/N): ")
    if confirm.lower() != 'y':
        print("❌ İptal edildi.")
        return
    
    print("\n🔄 Patching başlıyor...\n")
    
    # product.json'u patch'le
    patch_product_json()
    
    # Extension dosyalarını patch'le
    patch_extension_files()
    
    print("\n✅ Patching tamamlandı!")
    print("\n📝 Sonraki adımlar:")
    print("1. Proxy sunucusunu başlatın: python kiro_proxy/proxy_server.py")
    print("2. Kiro'yu yeniden başlatın")
    print("3. Test edin!")
    print("\n⚠️  Geri almak için .backup dosyalarını geri yükleyin")

if __name__ == "__main__":
    main()
