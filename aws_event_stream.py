#!/usr/bin/env python3
"""
AWS Event Stream Format Builder
AWS Q'nun kullandığı binary event stream formatını oluşturur
"""

import struct
import json
import binascii

def _crc32(data):
    """Calculate CRC32 checksum (AWS uses standard CRC32)"""
    return binascii.crc32(data) & 0xFFFFFFFF

def _encode_header(name, value, value_type=7):
    """
    Encode a single header
    value_type: 7 = string
    """
    name_bytes = name.encode('utf-8')
    value_bytes = value.encode('utf-8') if isinstance(value, str) else value
    
    header = bytes([len(name_bytes)])  # Name length (1 byte)
    header += name_bytes
    header += bytes([value_type])  # Value type (1 byte) - 7 for string
    header += struct.pack('>H', len(value_bytes))  # Value length (2 bytes, big-endian)
    header += value_bytes
    
    return header

def create_aws_event(payload):
    """
    AWS Event Stream binary formatında bir event oluştur
    
    Format:
    - Prelude (12 bytes): total_length (4), headers_length (4), prelude_crc (4)
    - Headers: key-value pairs
    - Payload: JSON data
    - Message CRC (4 bytes)
    """
    
    # Payload'ı encode et
    payload_bytes = payload.encode('utf-8') if isinstance(payload, str) else payload
    
    # Headers oluştur
    headers = []
    headers.append(_encode_header(':event-type', 'assistantResponseEvent'))
    headers.append(_encode_header(':content-type', 'application/json'))
    headers.append(_encode_header(':message-type', 'event'))
    
    # Tüm headers'ı birleştir
    headers_bytes = b''.join(headers)
    headers_length = len(headers_bytes)
    
    # Total length = prelude (12) + headers + payload + message_crc (4)
    total_length = 12 + headers_length + len(payload_bytes) + 4
    
    # Prelude oluştur (ilk 8 byte)
    prelude = struct.pack('>I', total_length)  # Total length (4 bytes)
    prelude += struct.pack('>I', headers_length)  # Headers length (4 bytes)
    
    # Prelude CRC hesapla ve ekle
    prelude_crc = _crc32(prelude)
    prelude += struct.pack('>I', prelude_crc)  # Prelude CRC (4 bytes)
    
    # Message oluştur (prelude + headers + payload)
    message = prelude + headers_bytes + payload_bytes
    
    # Message CRC hesapla ve ekle
    message_crc = _crc32(message)
    message += struct.pack('>I', message_crc)  # Message CRC (4 bytes)
    
    return message

def create_aws_event_stream(content):
    """
    Bir text içeriğini AWS Q binary streaming formatına çevir
    Markdown formatını koruyarak chunk'lara böler
    """
    events = []
    
    # Markdown formatını korumak için daha akıllı chunking
    # Satırları koru, ama çok uzun satırları böl
    chunk_size = 100  # Her chunk'ta max 100 karakter
    
    i = 0
    while i < len(content):
        # Chunk al
        chunk = content[i:i+chunk_size]
        
        # Eğer chunk ortasında bir kelimeyi kesiyorsa, son boşluğa kadar al
        if i + chunk_size < len(content) and chunk[-1] != '\n' and chunk[-1] != ' ':
            last_space = chunk.rfind(' ')
            last_newline = chunk.rfind('\n')
            split_point = max(last_space, last_newline)
            
            if split_point > 0:
                chunk = chunk[:split_point + 1]
        
        # Event oluştur
        payload = json.dumps({"content": chunk}, ensure_ascii=False)
        event = create_aws_event(payload)
        events.append(event)
        
        i += len(chunk)
    
    # Tüm eventleri birleştir
    return b''.join(events)

if __name__ == "__main__":
    # Test
    test_content = "Merhaba! Nasılsın?"
    stream = create_aws_event_stream(test_content)
    print(f"Generated {len(stream)} bytes")
    print(f"First 50 bytes: {stream[:50].hex()}")

if __name__ == "__main__":
    # Test
    test_content = "Merhaba! Nasılsın?"
    stream = create_aws_event_stream(test_content)
    print(stream)
