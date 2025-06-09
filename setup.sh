#!/bin/bash

echo "🎙️ Setting up Broadcastify Transcriber with NVIDIA Parakeet TDT..."

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed. Please install Python 3 first."
    exit 1
fi

# Check if Chrome is installed (required for Selenium)
if ! command -v google-chrome &> /dev/null && ! command -v chromium-browser &> /dev/null; then
    echo "⚠️  Warning: Chrome/Chromium not found. Please install Google Chrome for Selenium to work."
fi

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "🐍 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📦 Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo ""
echo "✅ Setup complete! To run the transcriber:"
echo "1. Activate the virtual environment: source venv/bin/activate"
echo "2. Run the script: python transcriber.py"
echo ""
echo "📝 The script will:"
echo "   - Load the NVIDIA Parakeet TDT ASR model (~600MB download on first run)"
echo "   - Connect to Broadcastify feed 31880"
echo "   - Provide real-time transcription with word-level timestamps"
echo "   - Display enhanced accuracy with punctuation and capitalization"
echo ""
echo "⚠️  Note: First run will download the Parakeet model - ensure stable internet!"
echo "🛑 Press Ctrl+C to stop the transcription when running."
