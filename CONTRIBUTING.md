# 🤝 Katkıda Bulunma Rehberi

Kiro Custom Model Hijacker projesine katkıda bulunmak istediğiniz için teşekkürler! 🎉

## 📋 İçindekiler

- [Davranış Kuralları](#davranış-kuralları)
- [Nasıl Katkıda Bulunabilirim?](#nasıl-katkıda-bulunabilirim)
- [Geliştirme Ortamı Kurulumu](#geliştirme-ortamı-kurulumu)
- [Pull Request Süreci](#pull-request-süreci)
- [Kod Standartları](#kod-standartları)
- [Commit Mesajları](#commit-mesajları)

## 🤝 Davranış Kuralları

Bu proje açık kaynak topluluğunun bir parçasıdır. Lütfen:

- ✅ Saygılı ve yapıcı olun
- ✅ Farklı görüşlere açık olun
- ✅ Eleştirileri yapıcı bir şekilde yapın
- ❌ Kaba veya saldırgan dil kullanmayın
- ❌ Spam veya reklam yapmayın

## 💡 Nasıl Katkıda Bulunabilirim?

### 🐛 Bug Bildirimi

Bir hata mı buldunuz? [Issue açın](https://github.com/gkhantyln/kiro-custom-model-hijacker/issues) ve şunları ekleyin:

- Hatanın açıklaması
- Hatayı tekrar etme adımları
- Beklenen davranış
- Gerçek davranış
- Ekran görüntüleri (varsa)
- Sistem bilgileri (OS, Python versiyonu)

### 💡 Özellik Önerisi

Yeni bir özellik mi istiyorsunuz?

1. Önce [Issues](https://github.com/gkhantyln/kiro-custom-model-hijacker/issues) sayfasında benzer bir öneri olup olmadığını kontrol edin
2. Yoksa yeni bir issue açın ve şunları ekleyin:
   - Özelliğin açıklaması
   - Neden gerekli olduğu
   - Nasıl çalışması gerektiği
   - Örnek kullanım senaryoları

### 🔧 Kod Katkısı

1. **Fork edin** - Projeyi kendi hesabınıza fork edin
2. **Clone edin** - Fork'u bilgisayarınıza indirin
   ```bash
   git clone https://github.com/KULLANICI_ADINIZ/kiro-custom-model-hijacker.git
   cd kiro-custom-model-hijacker
   ```
3. **Branch oluşturun** - Yeni bir branch oluşturun
   ```bash
   git checkout -b feature/harika-ozellik
   ```
4. **Değişiklik yapın** - Kodunuzu yazın
5. **Test edin** - Değişikliklerinizi test edin
6. **Commit edin** - Değişikliklerinizi commit edin
   ```bash
   git commit -m "feat: harika özellik eklendi"
   ```
7. **Push edin** - Branch'i GitHub'a gönderin
   ```bash
   git push origin feature/harika-ozellik
   ```
8. **Pull Request açın** - GitHub'da PR oluşturun

## 🛠️ Geliştirme Ortamı Kurulumu

### Gereksinimler

- Python 3.8+
- pip
- Git

### Kurulum

```bash
# Projeyi clone edin
git clone https://github.com/gkhantyln/kiro-custom-model-hijacker.git
cd kiro-custom-model-hijacker

# Virtual environment oluşturun (önerilen)
python -m venv venv
source venv/bin/activate  # Linux/Mac
# veya
venv\Scripts\activate  # Windows

# Bağımlılıkları yükleyin
pip install -r requirements.txt

# Config dosyasını oluşturun
cp config.example.py config.py
# config.py dosyasını düzenleyin
```

### Test Etme

```bash
# Custom API'yi başlatın
python custom_api.py

# Başka bir terminalde proxy'yi başlatın
python advanced_proxy.py

# Test edin
curl http://localhost:20128/health
```

## 📝 Pull Request Süreci

1. **Açıklayıcı başlık** - Ne yaptığınızı açıkça belirtin
2. **Detaylı açıklama** - Değişiklikleri detaylı açıklayın
3. **Issue referansı** - İlgili issue'yu bağlayın (#123)
4. **Ekran görüntüleri** - UI değişiklikleri varsa ekleyin
5. **Test sonuçları** - Testlerin geçtiğini gösterin

### PR Şablonu

```markdown
## Değişiklikler
- [ ] Yeni özellik eklendi
- [ ] Bug düzeltildi
- [ ] Dokümantasyon güncellendi
- [ ] Test eklendi

## Açıklama
Bu PR şunları yapar...

## İlgili Issue
Fixes #123

## Test Edildi
- [ ] Windows 10/11
- [ ] Python 3.8+
- [ ] Tüm testler geçti

## Ekran Görüntüleri
(varsa ekleyin)
```

## 📐 Kod Standartları

### Python Stil Rehberi

- **PEP 8** standartlarına uyun
- **Type hints** kullanın (Python 3.8+)
- **Docstrings** yazın (Google style)
- **Anlamlı değişken isimleri** kullanın

### Örnek

```python
def process_request(message: str, temperature: float = 0.7) -> dict:
    """
    Process incoming chat request and return response.
    
    Args:
        message: User's input message
        temperature: Model temperature (0.0-1.0)
        
    Returns:
        dict: API response with choices and usage
        
    Raises:
        ValueError: If temperature is out of range
    """
    if not 0.0 <= temperature <= 1.0:
        raise ValueError("Temperature must be between 0.0 and 1.0")
    
    # Implementation...
    return response
```

### Dosya Yapısı

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Module description here.
"""

# Standard library imports
import os
import sys

# Third-party imports
from flask import Flask
import requests

# Local imports
from config import API_KEY

# Constants
DEFAULT_TIMEOUT = 30

# Code...
```

## 💬 Commit Mesajları

[Conventional Commits](https://www.conventionalcommits.org/) formatını kullanın:

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Tipler

- `feat`: Yeni özellik
- `fix`: Bug düzeltme
- `docs`: Dokümantasyon
- `style`: Kod formatı (kod davranışını değiştirmez)
- `refactor`: Kod yeniden yapılandırma
- `test`: Test ekleme/düzeltme
- `chore`: Build, CI/CD, bağımlılık güncellemeleri

### Örnekler

```bash
feat(proxy): add request filtering by endpoint
fix(api): handle empty message array
docs(readme): update installation instructions
style(menu): improve color scheme
refactor(proxy): extract message parsing logic
test(api): add unit tests for chat endpoint
chore(deps): update mitmproxy to 10.1.0
```

## 🎨 UI/UX Katkıları

- Renkli terminal çıktıları için `colorama` kullanın
- Tutarlı emoji kullanımı (📡, 🎯, ✅, ❌, vb.)
- Kullanıcı dostu hata mesajları
- İngilizce ve Türkçe dil desteği

## 📚 Dokümantasyon

- README.md güncellemeleri
- Kod içi yorumlar
- Docstrings
- Örnek kullanımlar
- Sorun giderme rehberleri

## 🔒 Güvenlik

Güvenlik açığı bulduysanız:

1. ❌ **Public issue açmayın**
2. ✅ **Doğrudan email gönderin**: tylngkhn@gmail.com
3. ✅ **Detaylı açıklama yapın**
4. ✅ **Proof of concept ekleyin** (varsa)

## 📞 İletişim

Sorularınız mı var?

- 📧 Email: tylngkhn@gmail.com
- 💬 Telegram: [@llcoder](https://t.me/llcoder)
- 🐙 GitHub: [@gkhantylnl](https://github.com/gkhantyln)

## 🙏 Teşekkürler

Katkılarınız için teşekkür ederiz! Her katkı, projeyi daha iyi hale getirir. 🎉

---

**Made with ❤️ by the community**
