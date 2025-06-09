#!/usr/bin/env python3
"""
Quick status check for the Broadcastify Transcriber system.

This script verifies that all components are properly installed
and configured before running the main transcriber.
"""

import sys
import importlib
from typing import Dict, Any


def check_dependencies() -> Dict[str, Any]:
    """Check if all required dependencies are available."""
    deps = {}
    
    # Core dependencies
    required_modules = [
        'requests',
        'selenium', 
        'librosa',
        'soundfile',
        'numpy',
        'nemo',
        'torch'
    ]
    
    for module in required_modules:
        try:
            importlib.import_module(module)
            deps[module] = "✅ Installed"
        except ImportError:
            deps[module] = "❌ Missing"
    
    return deps


def check_chrome_driver():
    """Check if Chrome/Chromium is available for Selenium."""
    try:
        from selenium import webdriver
        from selenium.webdriver.chrome.options import Options
        
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        
        driver = webdriver.Chrome(options=options)
        driver.quit()
        return "✅ Chrome WebDriver working"
    except Exception as e:
        return f"❌ Chrome WebDriver error: {str(e)[:50]}..."


def check_model_compatibility():
    """Check if NeMo ASR model can be loaded."""
    try:
        import nemo.collections.asr as nemo_asr
        # Just check if the module structure is correct
        model_class = nemo_asr.models.ASRModel
        return "✅ NeMo ASR structure OK"
    except Exception as e:
        return f"❌ NeMo ASR error: {str(e)[:50]}..."


def check_modules():
    """Check if our custom modules can be imported."""
    modules = {}
    custom_modules = [
        'stream_extractor',
        'audio_processor', 
        'transcription_model'
    ]
    
    for module in custom_modules:
        try:
            importlib.import_module(module)
            modules[module] = "✅ Available"
        except ImportError as e:
            modules[module] = f"❌ Import error: {str(e)[:30]}..."
        except Exception as e:
            modules[module] = f"⚠️ Other error: {str(e)[:30]}..."
    
    return modules


def main():
    """Run complete system status check."""
    print("🔍 Broadcastify Transcriber System Status Check")
    print("=" * 60)
    
    # Check dependencies
    print("\n📦 Dependencies:")
    deps = check_dependencies()
    for module, status in deps.items():
        print(f"  {module:<15} {status}")
    
    # Check Chrome driver
    print(f"\n🌐 Browser:")
    print(f"  {'Chrome WebDriver':<15} {check_chrome_driver()}")
    
    # Check NeMo model
    print(f"\n🧠 AI Model:")
    print(f"  {'NeMo ASR':<15} {check_model_compatibility()}")
    
    # Check custom modules
    print(f"\n🔧 Custom Modules:")
    modules = check_modules()
    for module, status in modules.items():
        print(f"  {module:<15} {status}")
    
    # Overall status
    print(f"\n📊 Overall Status:")
    
    missing_deps = [k for k, v in deps.items() if "❌" in v]
    failing_modules = [k for k, v in modules.items() if "❌" in v]
    
    if missing_deps:
        print(f"  ❌ Missing dependencies: {', '.join(missing_deps)}")
        print(f"  💡 Run: pip install -r requirements.txt")
    
    if failing_modules:
        print(f"  ❌ Module issues: {', '.join(failing_modules)}")
        print(f"  💡 Check file paths and Python imports")
    
    if not missing_deps and not failing_modules:
        print(f"  ✅ System ready for transcription!")
        print(f"  🚀 Run: python transcriber.py")
    else:
        print(f"  ⚠️ System needs attention before use")
    
    print("\n" + "=" * 60)
    
    return len(missing_deps) + len(failing_modules) == 0


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
