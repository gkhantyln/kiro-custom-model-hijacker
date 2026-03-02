#!/usr/bin/env python3
"""
Kiro API Proxy - GitHub Copilot isteklerini custom endpoint'e yönlendirir
"""

from flask import Flask, request, Response
import requests
import json

# Config dosyasından ayarları yükle
try:
    from config import API_ENDPOINT, API_KEY, MODEL_NAME, PROXY_HOST, PROXY_PORT
    CUSTOM_API_ENDPOINT = API_ENDPOINT
    CUSTOM_API_KEY = API_KEY
    CUSTOM_MODEL = MODEL_NAME
except ImportError:
    print("\n" + "="*60)
    print("❌ HATA: config.py bulunamadı!")
    print("="*60)
    print("\n📝 Lütfen şu adımları takip edin:\n")
    print("1. config.example.py dosyasını config.py olarak kopyalayın:")
    print("   Windows: copy config.example.py config.py")
    print("   Linux/Mac: cp config.example.py config.py\n")
    print("2. config.py dosyasını açın ve API bilgilerinizi girin\n")
    print("3. Bu scripti tekrar çalıştırın\n")
    print("="*60)
    sys.exit(1)

app = Flask(__name__)

# HTTPS CONNECT tunnel handler
@app.route('/', defaults={'path': ''}, methods=['CONNECT'])
@app.route('/<path:path>', methods=['CONNECT'])
def handle_connect(path):
    """HTTPS CONNECT isteklerini handle et"""
    print(f"🔒 HTTPS CONNECT: {request.host}")
    
    # AWS AI endpoint'lerini yakala
    if 'amazonaws.com' in request.host or 'kiro.dev' in request.host:
        # Şimdilik geçir, ileride intercept edebiliriz
        return Response("Connection established", status=200)
    
    return Response("Method not allowed", status=405)

@app.route('/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH'])
def proxy(path):
    """Tüm istekleri yakala ve custom API'ye yönlendir"""
    
    # GitHub Copilot chat completion isteği mi?
    if 'chat/completions' in path or 'completions' in path:
        try:
            data = request.get_json()
            
            # OpenAI formatına çevir
            custom_request = {
                "model": CUSTOM_MODEL,
                "messages": data.get("messages", []),
                "stream": data.get("stream", False),
                "temperature": data.get("temperature", 0.7),
                "max_tokens": data.get("max_tokens", 4096)
            }
            
            # Custom API'ye istek gönder
            response = requests.post(
                f"{CUSTOM_API_ENDPOINT}/chat/completions",
                json=custom_request,
                headers={
                    "Authorization": f"Bearer {CUSTOM_API_KEY}",
                    "Content-Type": "application/json"
                },
                stream=custom_request["stream"]
            )
            
            # Yanıtı döndür
            return Response(
                response.content,
                status=response.status_code,
                headers=dict(response.headers)
            )
            
        except Exception as e:
            return {"error": str(e)}, 500
    
    # Diğer istekleri GitHub'a yönlendir (authentication vb.)
    else:
        url = f"https://api.github.com/{path}"
        resp = requests.request(
            method=request.method,
            url=url,
            headers={key: value for (key, value) in request.headers if key != 'Host'},
            data=request.get_data(),
            cookies=request.cookies,
            allow_redirects=False
        )
        
        return Response(
            resp.content,
            status=resp.status_code,
            headers=dict(resp.headers)
        )

if __name__ == '__main__':
    print("🚀 Kiro Proxy Server başlatılıyor...")
    print("📡 GitHub Copilot istekleri yakalanacak ve custom API'ye yönlendirilecek")
    print(f"🔗 Proxy: http://localhost:{PROXY_PORT}")
    print("🎯 Target: " + CUSTOM_API_ENDPOINT)
    app.run(host=PROXY_HOST, port=PROXY_PORT, debug=True)
