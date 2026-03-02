#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Custom API Server for Kiro
Bu basit API, Kiro'dan gelen istekleri kabul eder ve yanıt verir
"""

from flask import Flask, request, jsonify
import json

# Config dosyasından ayarları yükle
try:
    from config import API_ENDPOINT, API_KEY, MODEL_NAME, CUSTOM_API_HOST, CUSTOM_API_PORT
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
    input("\nDevam etmek için Enter'a basın...")
    sys.exit(1)

app = Flask(__name__)

@app.route('/generateAssistantResponse', methods=['POST'])
def generate_assistant_response():
    """AWS Q formatında istek al, OpenAI formatında yanıt ver"""
    try:
        # AWS Q formatındaki isteği al
        if not request.data:
            return jsonify({"error": "Request body is empty"}), 400
        
        data = json.loads(request.data.decode('utf-8'))
        
        print("\n" + "="*60)
        print("📨 AWS Q İsteği Alındı!")
        print("="*60)
        
        # AWS Q formatından mesajları çıkar
        messages = []
        if "conversationState" in data:
            conv_state = data["conversationState"]
            
            # History'deki mesajları ekle
            if "history" in conv_state:
                for msg in conv_state["history"]:
                    if "userInputMessage" in msg:
                        messages.append({
                            "role": "user",
                            "content": msg["userInputMessage"].get("content", "")
                        })
                    elif "assistantResponseMessage" in msg:
                        messages.append({
                            "role": "assistant",
                            "content": msg["assistantResponseMessage"].get("content", "")
                        })
            
            # Şu anki mesajı ekle
            if "currentMessage" in conv_state and "userInputMessage" in conv_state["currentMessage"]:
                user_content = conv_state["currentMessage"]["userInputMessage"].get("content", "")
                if user_content:
                    messages.append({
                        "role": "user",
                        "content": user_content
                    })
        
        if not messages:
            return jsonify({"error": "No messages found"}), 400
        
        last_message = messages[-1].get('content', '')
        print(f"💬 Kullanıcı Mesajı: {last_message[:100]}...")
        
        # Gerçek endpoint'e yönlendir
        import requests
        
        real_endpoint = "http://localhost:20128/v1/chat/completions"
        print(f"🔄 Gerçek endpoint'e yönlendiriliyor: {real_endpoint}")
        
        openai_request = {
            "model": MODEL_NAME,
            "messages": messages,
            "stream": False
        }
        
        response = requests.post(
            real_endpoint,
            json=openai_request,
            headers={
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json"
            },
            timeout=30
        )
        
        if response.status_code == 200:
            response_data = response.json()
            
            # OpenAI yanıtından content'i çıkar
            if "choices" in response_data and len(response_data["choices"]) > 0:
                content = response_data["choices"][0].get("message", {}).get("content", "")
                
                print(f"✅ Yanıt alındı: {content[:100]}...")
                
                # AWS Q formatında yanıt döndür
                aws_response = {
                    "conversationId": "custom-conv-123",
                    "assistantResponseMessage": content
                }
                
                return jsonify(aws_response)
        
        return jsonify({"error": "Failed to get response"}), 500
        
    except Exception as e:
        print(f"❌ Hata: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500


@app.route('/v1/chat/completions', methods=['POST'])
def chat_completions():
    """Kiro'dan gelen chat isteklerini işle ve gerçek endpoint'e yönlendir"""
    try:
        # Request body'yi kontrol et
        if not request.data:
            print("❌ Hata: Request body boş!")
            return jsonify({"error": "Request body is empty"}), 400
        
        # JSON parse et
        try:
            data = json.loads(request.data.decode('utf-8'))
        except Exception as e:
            print(f"❌ JSON Parse Hatası: {e}")
            print(f"Raw data: {request.data[:500]}")
            return jsonify({"error": f"Invalid JSON: {str(e)}"}), 400
        
        print("\n" + "="*60)
        print("📨 Yeni İstek Alındı!")
        print("="*60)
        
        # Mesajları al
        messages = data.get('messages', [])
        if not messages:
            print("❌ Hata: Messages array boş!")
            return jsonify({"error": "Messages array is empty"}), 400
            
        last_message = messages[-1].get('content', '') if messages else "Merhaba"
        print(f"💬 Kullanıcı Mesajı: {last_message[:100]}...")
        
        # Gerçek endpoint'e yönlendir (20128)
        import requests
        
        real_endpoint = "http://localhost:20128/v1/chat/completions"
        print(f"🔄 Gerçek endpoint'e yönlendiriliyor: {real_endpoint}")
        
        try:
            response = requests.post(
                real_endpoint,
                json=data,
                headers={
                    "Authorization": f"Bearer {API_KEY}",
                    "Content-Type": "application/json"
                },
                timeout=30
            )
            
            print(f"✅ Gerçek endpoint yanıtı: {response.status_code}")
            
            # Yanıtı kontrol et
            if response.status_code == 200:
                try:
                    response_data = response.json()
                    print(f"📦 Yanıt içeriği: {response_data}")
                    
                    # Eğer OpenAI formatında değilse, dönüştür
                    if "choices" not in response_data:
                        print("⚠️ Yanıt OpenAI formatında değil, dönüştürülüyor...")
                        
                        # Yanıtı string'e çevir
                        content = json.dumps(response_data, ensure_ascii=False, indent=2)
                        
                        # OpenAI formatına çevir
                        openai_response = {
                            "id": "custom-response-1",
                            "object": "chat.completion",
                            "created": 1234567890,
                            "model": MODEL_NAME,
                            "choices": [{
                                "index": 0,
                                "message": {
                                    "role": "assistant",
                                    "content": content
                                },
                                "finish_reason": "stop"
                            }],
                            "usage": {
                                "prompt_tokens": 10,
                                "completion_tokens": 20,
                                "total_tokens": 30
                            }
                        }
                        
                        return jsonify(openai_response)
                    else:
                        # Zaten OpenAI formatında
                        # Content'i kontrol et ve gerekirse düzelt
                        if "choices" in response_data and len(response_data["choices"]) > 0:
                            choice = response_data["choices"][0]
                            if "message" in choice and "content" in choice["message"]:
                                # Content'i olduğu gibi bırak, markdown formatını koru
                                pass
                        
                        return response.content, response.status_code, {'Content-Type': 'application/json; charset=utf-8'}
                        
                except json.JSONDecodeError:
                    # JSON değilse, text olarak döndür
                    content = response.text
                    openai_response = {
                        "id": "custom-response-1",
                        "object": "chat.completion",
                        "created": 1234567890,
                        "model": MODEL_NAME,
                        "choices": [{
                            "index": 0,
                            "message": {
                                "role": "assistant",
                                "content": content
                            },
                            "finish_reason": "stop"
                        }],
                        "usage": {
                            "prompt_tokens": 10,
                            "completion_tokens": 20,
                            "total_tokens": 30
                        }
                    }
                    return jsonify(openai_response)
            else:
                # Hata durumu
                print(f"❌ Endpoint hata döndü: {response.status_code}")
                raise Exception(f"Endpoint returned {response.status_code}")
            
        except requests.exceptions.RequestException as e:
            print(f"❌ Gerçek endpoint hatası: {e}")
            
            # Fallback: Basit yanıt
            response = {
                "id": "custom-response-1",
                "object": "chat.completion",
                "created": 1234567890,
                "model": MODEL_NAME,
                "choices": [{
                    "index": 0,
                    "message": {
                        "role": "assistant",
                        "content": f"Merhaba! Gerçek endpoint'e ulaşılamadı. Test mesajı: '{last_message}'"
                    },
                    "finish_reason": "stop"
                }],
                "usage": {
                    "prompt_tokens": 10,
                    "completion_tokens": 20,
                    "total_tokens": 30
                }
            }
            
            print(f"⚠️ Fallback yanıt gönderildi")
            return jsonify(response)
        
    except Exception as e:
        print(f"\n❌ Hata: {e}\n")
        return jsonify({"error": str(e)}), 500


@app.route('/v1/models', methods=['GET'])
def list_models():
    """Mevcut modelleri listele"""
    return jsonify({
        "object": "list",
        "data": [
            {
                "id": MODEL_NAME,
                "object": "model",
                "created": 1234567890,
                "owned_by": "ayzdev"
            }
        ]
    })


@app.route('/health', methods=['GET'])
def health():
    """Sağlık kontrolü"""
    return jsonify({"status": "ok", "message": "Custom API çalışıyor!"})


if __name__ == '__main__':
    print("\n" + "="*60)
    print("🚀 Custom API Server Başlatılıyor...")
    print("="*60)
    print(f"📍 Adres: {API_ENDPOINT}")
    print(f"🤖 Model: {MODEL_NAME}")
    print(f"🔑 API Key: {API_KEY[:20]}...")
    print(f"📡 Endpoint: /v1/chat/completions")
    print(f"🔧 Test: http://localhost:{CUSTOM_API_PORT}/health")
    print("="*60 + "\n")
    
    # threaded=True ekleyerek concurrent istekleri destekle
    app.run(host=CUSTOM_API_HOST, port=CUSTOM_API_PORT, debug=False, threaded=True)
