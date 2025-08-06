#!/usr/bin/env python3
"""
Test script to verify environment variables are being loaded correctly
"""

import os
import sys
from app.core.config import settings

def test_env_loading():
    print("🔍 Testing Environment Variable Loading...")
    print("=" * 50)
    
    # Check what the settings object sees (now that we enabled .env loading)
    print("\n1️⃣ What your app's settings object sees:")
    print(f"   openai_api_key: {'✅ SET' if settings.openai_api_key else '❌ NOT SET'}")
    print(f"   openai_model: {settings.openai_model}")
    print(f"   max_tokens: {settings.max_tokens}")
    print(f"   temperature: {settings.temperature}")
    
    # Test if API key is available for summarization
    print("\n2️⃣ Summarization Service Status:")
    try:
        from app.services.summarize import SummarizationService
        service = SummarizationService()
        if service.api_key_available:
            print("   ✅ OpenAI API key is available - AI features ENABLED")
            print(f"   📝 Using model: {service.model}")
            print(f"   🎛️ Max tokens: {service.max_tokens}")
            print(f"   🌡️ Temperature: {service.temperature}")
        else:
            print("   ❌ OpenAI API key NOT available - AI features DISABLED")
    except Exception as e:
        print(f"   ⚠️ Error testing summarization service: {e}")
    
    print("\n" + "=" * 50)
    print("✅ Environment variable test complete!")

if __name__ == "__main__":
    test_env_loading()