# Kiro API Hijack - Hosts dosyasını düzenle
# UYARI: Bu yöntem tüm GitHub API isteklerini etkiler!

Write-Host "⚠️  UYARI: Bu script hosts dosyasını değiştirecek!" -ForegroundColor Yellow
Write-Host "GitHub API istekleri localhost:8080'e yönlendirilecek" -ForegroundColor Yellow
Write-Host ""
$confirm = Read-Host "Devam etmek istiyor musunuz? (Y/N)"

if ($confirm -ne 'Y' -and $confirm -ne 'y') {
    Write-Host "İptal edildi." -ForegroundColor Red
    exit
}

# Hosts dosyası yolu
$hostsPath = "C:\Windows\System32\drivers\etc\hosts"

# Backup oluştur
$backupPath = "C:\Windows\System32\drivers\etc\hosts.backup_$(Get-Date -Format 'yyyyMMdd_HHmmss')"
Copy-Item $hostsPath $backupPath
Write-Host "✅ Backup oluşturuldu: $backupPath" -ForegroundColor Green

# Hosts dosyasına ekle
$hostsEntry = "`n# Kiro API Hijack`n127.0.0.1 api.github.com`n"
Add-Content -Path $hostsPath -Value $hostsEntry

Write-Host "✅ Hosts dosyası güncellendi!" -ForegroundColor Green
Write-Host ""
Write-Host "Şimdi proxy sunucusunu başlatın:" -ForegroundColor Cyan
Write-Host "  python kiro_proxy/proxy_server.py" -ForegroundColor White
Write-Host ""
Write-Host "Geri almak için:" -ForegroundColor Yellow
Write-Host "  .\kiro_proxy\restore_hosts.ps1" -ForegroundColor White
