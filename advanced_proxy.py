#!/usr/bin/env python3
"""
Kiro Advanced HTTPS Proxy - SSL/TLS isteklerini intercept eder
mitmproxy kullanarak tüm HTTPS trafiğini yakalar
"""

from mitmproxy import http
from mitmproxy.tools.main import mitmdump
import json
import sys

# AWS event stream helper
from aws_event_stream import create_aws_event_stream

# Config dosyasından ayarları yükle
try:
    from config import API_ENDPOINT, API_KEY, MODEL_NAME, PROXY_PORT
    CUSTOM_API_ENDPOINT = API_ENDPOINT
    CUSTOM_API_KEY = API_KEY
    CUSTOM_MODEL = MODEL_NAME
except ImportError:
    print("\n" + "="*70)
    print("❌ HATA: config.py bulunamadı!")
    print("="*70)
    print("\n📝 Lütfen şu adımları takip edin:\n")
    print("1. config.example.py dosyasını config.py olarak kopyalayın:")
    print("   Windows: copy config.example.py config.py")
    print("   Linux/Mac: cp config.example.py config.py\n")
    print("2. config.py dosyasını açın ve API bilgilerinizi girin\n")
    print("3. Bu scripti tekrar çalıştırın\n")
    print("="*70)
    sys.exit(1)

class KiroInterceptor:
    def __init__(self):
        self.request_count = 0
        print("🚀 Kiro Advanced HTTPS Proxy başlatıldı")
        print(f"🎯 Target API: {CUSTOM_API_ENDPOINT}")
        print(f"🔑 Model: {CUSTOM_MODEL}")
        print("=" * 70)
    
    def request(self, flow: http.HTTPFlow) -> None:
        """Giden istekleri yakala - SADECE AI CHAT İSTEKLERİ"""
        
        # Sadece AI chat isteklerini yakala
        is_ai_request = False
        
        # AWS AI endpoint'lerini yakala
        if "amazonaws.com" in flow.request.pretty_host:
            # Sadece AI model invoke istekleri
            if any(keyword in flow.request.path.lower() for keyword in ["invoke", "generateassistantresponse", "chat", "completion"]):
                is_ai_request = True
        
        # GitHub Copilot chat
        elif "github.com" in flow.request.pretty_host or "copilot" in flow.request.path.lower():
            if "completions" in flow.request.path.lower():
                is_ai_request = True
        
        # Telemetri ve diğer istekleri sessizce geçir
        if not is_ai_request:
            return
        
        # AI isteği yakalandı!
        self.request_count += 1
        print(f"\n{'='*70}")
        print(f"🎯 AI CHAT İSTEĞİ YAKALANDI #{self.request_count}")
        print(f"{'='*70}")
        print(f"📡 Host: {flow.request.pretty_host}")
        print(f"📍 Path: {flow.request.path}")
        print(f"🔧 Method: {flow.request.method}")
        
        try:
            # Request body'yi oku
            if flow.request.content:
                body = json.loads(flow.request.content)
                
                # AWS Q formatını OpenAI formatına çevir
                messages = []
                
                # conversationState içinde mesajlar var mı?
                if "conversationState" in body:
                    conv_state = body["conversationState"]
                    
                    if isinstance(conv_state, dict):
                        # History'deki eski mesajları ekle
                        if "history" in conv_state and isinstance(conv_state["history"], list):
                            for msg in conv_state["history"]:
                                if isinstance(msg, dict):
                                    # User mesajı
                                    if "userInputMessage" in msg:
                                        messages.append({
                                            "role": "user",
                                            "content": msg["userInputMessage"].get("content", "")
                                        })
                                    # Assistant mesajı
                                    elif "assistantResponseMessage" in msg:
                                        messages.append({
                                            "role": "assistant", 
                                            "content": msg["assistantResponseMessage"].get("content", "")
                                        })
                        
                        # Şu anki mesajı ekle
                        if "currentMessage" in conv_state:
                            current = conv_state["currentMessage"]
                            if isinstance(current, dict) and "userInputMessage" in current:
                                user_content = current["userInputMessage"].get("content", "")
                                if user_content:
                                    messages.append({
                                        "role": "user",
                                        "content": user_content
                                    })
                
                # Fallback: diğer formatlar
                if not messages:
                    if "messages" in body:
                        messages = body["messages"]
                    elif "prompt" in body:
                        messages = [{"role": "user", "content": body["prompt"]}]
                
                print(f"💬 Toplam Mesaj: {len(messages)}")
                if messages:
                    last_msg = messages[-1].get('content', '')
                    print(f"📝 Son Kullanıcı Mesajı:")
                    print(f"   {last_msg[:200]}{'...' if len(last_msg) > 200 else ''}")
                
                # Custom API'ye yönlendir - OpenAI endpoint'i
                flow.request.scheme = "http"
                flow.request.host = "localhost"
                flow.request.port = 20130
                flow.request.path = "/v1/chat/completions"  # OpenAI endpoint'i
                
                # OpenAI formatında body oluştur
                custom_body = {
                    "model": CUSTOM_MODEL,
                    "messages": messages,
                    "stream": body.get("stream", False),
                    "temperature": body.get("temperature", 0.7),
                    "max_tokens": body.get("max_tokens", body.get("maxTokens", 4096))
                }
                
                # Body'yi encode et
                encoded_body = json.dumps(custom_body).encode('utf-8')
                flow.request.content = encoded_body
                
                # Headers'ı güncelle
                flow.request.headers.clear()
                flow.request.headers["Authorization"] = f"Bearer {CUSTOM_API_KEY}"
                flow.request.headers["Content-Type"] = "application/json"
                flow.request.headers["Content-Length"] = str(len(encoded_body))
                flow.request.headers["Host"] = "localhost:20130"
                flow.request.headers["Connection"] = "close"
                
                print(f"✅ Custom API'ye yönlendirildi: http://localhost:20130/v1/chat/completions")
                print(f"{'='*70}\n")
                
        except Exception as e:
            print(f"❌ Hata: {e}")
            import traceback
            traceback.print_exc()
    
    def response(self, flow: http.HTTPFlow) -> None:
        """Gelen yanıtları yakala ve AWS Q event-stream formatına çevir"""
        
        # Custom API'den gelen yanıtları logla ve event-stream formatına çevir
        if flow.request.host == "localhost" and flow.request.port == 20130:
            print(f"\n✅ Custom API Yanıtı")
            print(f"   Status: {flow.response.status_code}")
            
            try:
                if flow.response.content and flow.response.status_code == 200:
                    openai_response = json.loads(flow.response.content)
                    
                    if "choices" in openai_response:
                        content = openai_response["choices"][0].get("message", {}).get("content", "")
                        preview = content[:100] + "..." if len(content) > 100 else content
                        print(f"   📝 Response Preview: {preview}")
                        
                        # AWS Q binary event-stream formatına çevir
                        event_stream = create_aws_event_stream(content)
                        
                        # Yanıtı değiştir - BINARY
                        flow.response.content = event_stream  # Zaten bytes
                        flow.response.headers["Content-Type"] = "application/vnd.amazon.eventstream"
                        flow.response.headers["Cache-Control"] = "no-cache"
                        flow.response.headers["Connection"] = "keep-alive"
                        # Content-Length kaldır (streaming için)
                        if "Content-Length" in flow.response.headers:
                            del flow.response.headers["Content-Length"]
                        
                        print(f"   ✅ AWS Q binary event-stream formatına çevrildi ({len(event_stream)} bytes)")
                        
            except Exception as e:
                print(f"   ❌ Yanıt parse hatası: {e}")
                import traceback
                traceback.print_exc()

def main():
    print("=" * 70)
    print("🔒 Kiro Advanced HTTPS Proxy")
    print("=" * 70)
    print()
    print("Bu proxy tüm HTTPS trafiğini intercept eder.")
    print("SSL sertifikası oluşturulacak ve Kiro'ya güvenilir olarak eklenmeli.")
    print()
    print("Başlatılıyor...")
    print()
    
    # mitmproxy'yi başlat
    sys.argv = [
        "mitmdump",
        "-s", __file__,
        "--listen-host", "0.0.0.0",
        "--listen-port", str(PROXY_PORT),
        "--ssl-insecure"
    ]
    
    mitmdump()

addons = [KiroInterceptor()]

if __name__ == "__main__":
    main()
