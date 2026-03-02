#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Configuration File
Tüm API ve proxy ayarlarını buradan yönetin
"""

# ============================================================================
# API YAPILANDIRMASI
# ============================================================================

# Custom API Endpoint Bilgileri
API_ENDPOINT = "http://localhost:port/v1"
API_KEY = "API KEYINIZ"
MODEL_NAME = "provider veya multi provider ismi"

# ============================================================================
# PROXY AYARLARI
# ============================================================================

# Proxy Server Ayarları
PROXY_HOST = "0.0.0.0"
PROXY_PORT = 8080

# Custom API Server Ayarları
CUSTOM_API_HOST = "0.0.0.0"
CUSTOM_API_PORT = 20128

# ============================================================================
# ÖZELLIKLER
# ============================================================================

# Debug Modu
DEBUG = True

# Loglama
LOG_REQUESTS = True
LOG_RESPONSES = True
LOG_LEVEL = "INFO"  # DEBUG, INFO, WARNING, ERROR

# Güvenlik
ALLOWED_HOSTS = ["localhost", "127.0.0.1"]
REQUIRE_API_KEY = True

# AI Özellikleri
ENABLE_STREAMING = True
ENABLE_HISTORY = True
MAX_HISTORY_LENGTH = 50

# Timeout Ayarları (saniye)
REQUEST_TIMEOUT = 30
CONNECTION_TIMEOUT = 10
