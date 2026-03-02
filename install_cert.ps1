# mitmproxy SSL Sertifikasını Windows'a Yükle
# Bu script mitmproxy'nin oluşturduğu sertifikayı güvenilir sertifikalar arasına ekler

Write-Host "🔒 mitmproxy SSL Sertifikası Kurulumu" -ForegroundColor Cyan
Write-Host "=" * 70
Write-Host ""

# mitmproxy sertifika yolu
$certPath = "$env:USERPROFILE\.mitmproxy\mitmproxy-ca-cert.cer"

# Sertifika var mı kontrol et
if (-not (Test-Path $certPath)) {
    Write-Host "❌ Sertifika bulunamadı!" -ForegroundColor Red
    Write-Host "Önce advanced proxy'yi bir kez çalıştırın:" -ForegroundColor Yellow
    Write-Host "  python kiro_proxy/advanced_proxy.py" -ForegroundColor White
    Write-Host ""
    Write-Host "Proxy başladıktan sonra Ctrl+C ile durdurun ve bu scripti tekrar çalıştırın." -ForegroundColor Yellow
    pause
    exit
}

Write-Host "✅ Sertifika bulundu: $certPath" -ForegroundColor Green
Write-Host ""

# Sertifikayı yükle
Write-Host "📥 Sertifika yükleniyor..." -ForegroundColor Cyan

try {
    # Sertifikayı oku
    $cert = New-Object System.Security.Cryptography.X509Certificates.X509Certificate2($certPath)
    
    # Trusted Root Certification Authorities'e ekle
    $store = New-Object System.Security.Cryptography.X509Certificates.X509Store("Root", "CurrentUser")
    $store.Open("ReadWrite")
    $store.Add($cert)
    $store.Close()
    
    Write-Host "✅ Sertifika başarıyla yüklendi!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Artık Kiro, mitmproxy üzerinden HTTPS trafiğini kabul edecek." -ForegroundColor Green
    Write-Host ""
    Write-Host "Sonraki adımlar:" -ForegroundColor Cyan
    Write-Host "1. Advanced proxy'yi başlatın: python kiro_proxy/advanced_proxy.py" -ForegroundColor White
    Write-Host "2. Kiro'yu proxy ile başlatın:" -ForegroundColor White
    Write-Host "   `$env:HTTPS_PROXY='http://localhost:8080'" -ForegroundColor White
    Write-Host "   `$env:HTTP_PROXY='http://localhost:8080'" -ForegroundColor White
    Write-Host "   & 'C:\Users\user\AppData\Local\Programs\Kiro\Kiro.exe'" -ForegroundColor White
    
} catch {
    Write-Host "❌ Hata: $_" -ForegroundColor Red
    Write-Host ""
    Write-Host "Yönetici olarak çalıştırmayı deneyin:" -ForegroundColor Yellow
    Write-Host "  Start-Process powershell -ArgumentList '-ExecutionPolicy Bypass -File install_cert.ps1' -Verb RunAs" -ForegroundColor White
}

Write-Host ""
pause
