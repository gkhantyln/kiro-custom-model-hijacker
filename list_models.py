#!/usr/bin/env python3
import requests

print("9router - Mevcut modelleri listele")
print("=" * 60)

try:
    response = requests.get("http://localhost:20128/v1/models", timeout=5)
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        import json
        data = response.json()
        
        if "data" in data:
            print(f"\n✅ {len(data['data'])} model bulundu:\n")
            for model in data['data'][:20]:  # İlk 20 model
                model_id = model.get('id', 'unknown')
                print(f"  - {model_id}")
        else:
            print(json.dumps(data, indent=2))
    else:
        print(f"Hata: {response.text}")
        
except Exception as e:
    print(f"Bağlantı hatası: {e}")
