# Repeater Alerts - Real-Time HAM Radio Alert Monitoring

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A real-time HAM radio repeater monitoring system that captures live audio streams from Broadcastify feeds and transcribes them to detect emergency alerts and important communications. Using advanced voice activity detection and NVIDIA's Parakeet TDT model, this system provides 24/7 monitoring of amateur radio repeaters for emergency preparedness and situational awareness.

## 📱 Sample Alert Output

```
🚀 Initializing BroadcastifyTranscriber for feed 20213
⚙️ AudioProcessor Configuration:
   📏 Chunk duration: 2.0s
   🔄 Buffer overlap: 0.5s  
   🎵 Sample rate: 16000Hz
🔄 Loading NVIDIA Parakeet TDT model...
✅ Parakeet model loaded successfully!
✅ All components initialized successfully!

📊 Transcriber Status:
   📡 Feed ID: 20213 (Sherman Repeater)
   🧠 Model loaded: True
   🎵 Model: nvidia/parakeet-tdt-0.6b-v2

🔄 Starting in VAD mode (voice activity detection)...
🔄 24/7 operation with intelligent reconnection enabled
📡 Network issues: 10s → 5min exponential backoff
📻 Feed outages: 1min → 30min exponential backoff
❌ Press Ctrl+C to stop

🌐 Loading Broadcastify feed 20213...
✅ Audio element found!
🎯 Raw stream URL: https://broadcastify.cdnstream1.com/20213
📄 Page title: Sherman Texas Amateur Radio Emergency Service
🔗 Stream URL found: https://broadcastify.cdnstream1.com/20213
📻 Feed Name: Sherman ARES Repeater
✅ Stream ready! Starting real-time transcription with speech accumulation...

🎙️ [2025-06-08 15:30:42] Sherman ARES Repeater (Feed 20213):
📝 Emergency net activation. All stations standby for priority traffic.
================================================================================

🎙️ [2025-06-08 15:31:15] Sherman ARES Repeater (Feed 20213):
📝 Severe thunderstorm warning issued for Grayson County until 4 PM.
================================================================================

🎙️ [2025-06-08 15:32:03] Sherman ARES Repeater (Feed 20213):
📝 Unit 7 reporting power lines down on Highway 82 near mile marker 15.
================================================================================
```

## 🎯 Use Cases

### Emergency Preparedness
- **Weather Alerts**: Monitor severe weather communications and warnings
- **Emergency Traffic**: Catch emergency activations and priority communications  
- **Net Operations**: Track emergency nets and disaster communications
- **Situational Awareness**: Stay informed when away from radio equipment

### HAM Radio Operations
- **Repeater Monitoring**: Track activity on local repeater networks
- **Event Support**: Monitor communications during races, festivals, and public events
- **Training**: Record and analyze emergency exercises and drills
- **Documentation**: Maintain logs of important communications

### Emergency Services Coordination
- **ARES/RACES**: Monitor amateur radio emergency service communications
- **Storm Spotting**: Track severe weather reports and spotter activations
- **Disaster Response**: Monitor relief communications during emergencies
- **Interoperability**: Bridge between different communication systems

## 🚀 Quick Start

### Automated Setup (Recommended)

```bash
git clone https://github.com/TheSethRose/Repeater-Alerts.git
cd Repeater-Alerts
chmod +x setup.sh
./setup.sh
```

### Manual Setup

```bash
git clone https://github.com/TheSethRose/Repeater-Alerts.git
cd Repeater-Alerts
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Configuration

1. Copy the example environment file:
```bash
cp .env.example .env
```

2. Edit `.env` to set your default feed ID:
```bash
# Default Broadcastify Feed ID to monitor
BROADCASTIFY_FEED_ID=20213
```

3. Common feed IDs for reference:
   - **Plano Repeater**: 31880
   - **Sherman Repeater**: 20213

## 📻 Usage

### Basic Alert Monitoring

```bash
# Activate environment
source venv/bin/activate

# Start monitoring default repeater (from .env)
python transcriber.py

# Monitor specific repeater feed
python transcriber.py 31880

# Show help
python transcriber.py --help
```

### Finding Feed IDs
1. Visit [Broadcastify.com](https://www.broadcastify.com)
2. Search for your local repeater or emergency services
3. The feed ID is in the URL: `broadcastify.com/listen/feed/XXXXX`
4. Use that number: `python transcriber.py XXXXX` or set in `.env`

### Continuous Operation
The system is designed for 24/7 operation:
- **Automatic Recovery**: Handles feed outages and network issues
- **Resource Efficient**: Only processes when speech is detected  
- **Clean Shutdown**: Stop anytime with `Ctrl+C`

## ⚙️ Configuration

### Environment Variables (.env)

The system uses environment variables for configuration. Copy `.env.example` to `.env` and customize:

```bash
# Default feed to monitor
BROADCASTIFY_FEED_ID=20213

# Optional browser settings
CHROME_HEADLESS=true
CHROME_USER_AGENT="Mozilla/5.0 (compatible; RepeaterAlerts/1.0)"

# Optional audio processing settings
CHUNK_DURATION=2.0
BUFFER_OVERLAP=0.5
SAMPLE_RATE=16000
```

### Audio Processing Parameters

You can fine-tune audio processing in `audio_processor.py`:

```python
# Voice Activity Detection sensitivity
VoiceActivityDetector(
    energy_threshold=0.01,      # Speech detection sensitivity
    spectral_threshold=0.5,     # Frequency analysis threshold  
    min_speech_duration=0.5     # Minimum speech duration (seconds)
)

# Audio chunk processing
AudioProcessor(
    chunk_duration=2.0,         # Process every 2 seconds
    buffer_duration=0.5,        # 0.5-second overlap for accuracy
    sample_rate=16000,          # Audio sample rate (16kHz)
    max_speech_duration=30.0,   # Max single message duration
    silence_threshold=4.0       # Silence duration to end message
)
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

### Development Setup
1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes and test thoroughly
4. Commit your changes: `git commit -am 'Add some feature'`
5. Push to the branch: `git push origin feature-name`
6. Submit a pull request

### Code Style
- Follow PEP 8 for Python code
- Add docstrings to new functions and classes
- Include tests for new features
- Update documentation as needed

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **NVIDIA NeMo Team** for the excellent Parakeet TDT ASR model
- **Broadcastify.com** for providing public access to radio feeds
- **HAM Radio Community** for emergency communications and public service

## 📞 Support

If you encounter any issues or have questions:
1. Check the [RECONNECTION_GUIDE.md](docs/RECONNECTION_GUIDE.md) for troubleshooting
2. Search existing [GitHub Issues](https://github.com/TheSethRose/Repeater-Alerts/issues)
3. Open a new issue with detailed information about your problem

---

**⚠️ Legal Notice**: This tool is intended for monitoring publicly available radio communications only. Always comply with local laws and regulations regarding radio monitoring. Respect privacy and emergency services protocols.
