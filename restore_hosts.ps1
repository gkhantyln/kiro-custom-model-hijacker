# Hosts dosyasını geri yükle

$hostsPath = "C:\Windows\System32\drivers\etc\hosts"

# En son backup'ı bul
$backups = Get-ChildItem "C:\Windows\System32\drivers\etc\hosts.backup_*" | Sort-Object LastWriteTime -Descending

if ($backups.Count -eq 0) {
    Write-Host "❌ Backup bulunamadı!" -ForegroundColor Red
    exit
}

$latestBackup = $backups[0]
Write-Host "📦 Backup bulundu: $($latestBackup.Name)" -ForegroundColor Cyan

Copy-Item $latestBackup.FullName $hostsPath -Force
Write-Host "✅ Hosts dosyası geri yüklendi!" -ForegroundColor Green
Write-Host ""
Write-Host "Kiro'yu yeniden başlatın." -ForegroundColor Yellow
