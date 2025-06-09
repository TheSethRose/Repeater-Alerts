# Br## Features

- **🎙️ Voice Activity Detection (VAD)**: Automatically detects speech and skips silent periods
- **📋 Speech Accumulation**: Groups continuous speech into complete messages for better transcription
- **⚡ Real-Time Processing**: 2-second chunks with immediate processing when speech is detected
- **🧠 High-Quality Transcription**: NVIDIA Parakeet TDT 0.6B V2 model (6.05% WER vs 10-15% for Whisper)
- **⏰ Word-Level Timestamps**: Precise timing information for each transcribed word
- **🔧 Modular Architecture**: Separate components for maintainability and testing
- **🌐 Automated Stream Extraction**: Headless browser operation via Selenium
- **🔬 Intelligent Analysis**: Energy and spectral analysis for robust speech detectiony Transcriber with Voice Activity Detection

A real-time HAM radio and emergency scanner transcription tool using NVIDIA Parakeet TDT and intelligent voice activity detection to efficiently monitor Broadcastify feeds.

## Features

- **🎙️ Voice Activity Detection (VAD)**: Automatically detects speech and skips silent periods
- **⚡ Real-Time Processing**: 2-second chunks with immediate transcription when speech is detected
- **🧠 High-Quality Transcription**: NVIDIA Parakeet TDT 0.6B V2 model (6.05% WER vs 10-15% for Whisper)
- **⏰ Word-Level Timestamps**: Precise timing information for each transcribed word
- **🔧 Modular Architecture**: Separate components for maintainability and testing
- **🌐 Automated Stream Extraction**: Headless browser operation via Selenium
- **� Intelligent Analysis**: Energy and spectral analysis for robust speech detection

## Architecture

The application is split into focused modules:

- **`transcriber.py`** - Main orchestrator and entry point
- **`stream_extractor.py`** - Broadcastify URL extraction via Selenium
- **`audio_processor.py`** - Real-time audio streaming and VAD
- **`transcription_model.py`** - NVIDIA Parakeet model management
- **`test_transcriber.py`** - Comparison testing tool

## Voice Activity Detection & Speech Accumulation

The system intelligently handles HAM radio communication patterns:

### Voice Activity Detection (VAD)
- **Energy Analysis**: Monitors audio energy levels for voice activity
- **Spectral Analysis**: Analyzes frequency content typical of human speech  
- **Duration Filtering**: Minimum speech duration requirements
- **Configurable Thresholds**: Adjustable sensitivity for different environments

### Speech Accumulation
- **Message Grouping**: Combines continuous speech chunks into complete messages
- **Intelligent Boundaries**: Uses silence detection to determine message endings
- **Flexible Duration**: Handles short confirmations to long weather announcements
- **Complete Transcriptions**: Ensures full spoken messages aren't fragmented

## Key Improvements

- **Complete Message Capture**: Speech accumulation ensures full announcements aren't fragmented
- **Lower latency**: 2-3 seconds from speech start to transcription (vs 30+ seconds legacy)
- **Resource efficiency**: Only processes audio containing speech
- **Better accuracy**: 6.05% WER vs 10-15% with Whisper models
- **Word-level timestamps**: Precise timing for each word
- **Faster inference**: Real-Time Factor of 3380x

## Prerequisites

- Python 3.8+
- Google Chrome browser (for Selenium)
- Internet connection for streaming and model download
- ~2GB RAM minimum for model loading

## Quick Setup

### Automated Setup (Recommended)

```bash
chmod +x setup.sh
./setup.sh
```

### Manual Setup

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Usage

```bash
# Activate environment
source venv/bin/activate

# Default VAD mode (recommended)
python transcriber.py

# Specific feed ID  
python transcriber.py 31880

# Legacy mode (30-second fixed chunks)
python transcriber.py --legacy

# Compare modes
python test_transcriber.py

# Check system status
python status_check.py

# Get help
python transcriber.py --help
```

Stop with `Ctrl+C`

## Configuration

### VAD Sensitivity (audio_processor.py)

```python
VoiceActivityDetector(
    energy_threshold=0.01,      # Audio energy sensitivity
    spectral_threshold=0.5,     # Frequency content threshold  
    min_speech_duration=0.5     # Minimum speech duration (seconds)
)
```

### Audio Processing & Speech Accumulation (audio_processor.py)

```python
AudioProcessor(
    chunk_duration=2.0,         # Process every 2 seconds
    buffer_duration=0.5,        # 0.5-second overlap
    sample_rate=16000,          # Audio sample rate
    max_speech_duration=30.0,   # Max duration for accumulated speech
    silence_threshold=2.0       # Silence duration to end message
)
```

## Sample Output

```
🚀 Initializing BroadcastifyTranscriber for feed 31880
🔄 Loading NVIDIA Parakeet TDT model: nvidia/parakeet-tdt-0.6b-v2...
✅ Parakeet model loaded successfully!
✅ All components initialized successfully!

🚀 Starting continuous transcription with VAD...
🌐 Loading Broadcastify feed 31880...
✅ Audio element found!
📻 Feed Name: Sacramento County Sheriff
🎵 Starting real-time audio streaming...

🎙️ Speech detected! Processing for transcription
✅ Speech #1 transcribed successfully!

🎙️ [2024-06-08 15:30:42] Sacramento County Sheriff (Feed 31880):
📝 TRANSCRIPTION: Unit 23, respond to a 211 in progress at Oak and Main.
⏰ Word-level timestamps (12 words):
    🔹 [0.1s-0.4s] Unit
    🔹 [0.5s-0.9s] 23,
    🔹 [1.0s-1.4s] respond
    🔹 [1.5s-1.7s] to
    🔹 [1.8s-1.9s] a
    🔹 [2.0s-2.4s] 211
    🔹 [2.5s-2.7s] in
    🔹 [2.8s-3.2s] progress
    🔹 [3.3s-3.5s] at
    🔹 [3.6s-3.8s] Oak
    🔹 [3.9s-4.1s] and
    🔹 [4.2s-4.5s] Main.
================================================================================
```

## Performance Improvements

### VAD Mode vs Legacy Mode

**VAD Mode with Speech Accumulation (Recommended)**:
- ✅ **Complete message capture**: Groups continuous speech into full messages
- ✅ **Real-time responsiveness**: 2-second processing chunks with immediate speech detection
- ✅ **Efficient resource usage**: Only processes audio containing speech
- ✅ **Perfect for HAM radio**: Handles both short confirmations and long announcements
- ✅ **Lower latency**: ~2-3 seconds from speech start to transcription
- ✅ **Adaptive processing**: Automatically adjusts to speech patterns and durations

**Legacy Mode**:
- ⚠️ **Fixed 30-second chunks**: Always waits 30 seconds regardless of content
- ⚠️ **Higher latency**: Up to 30+ seconds from speech to transcription
- ⚠️ **Resource waste**: Processes long periods of silence
- ⚠️ **Poor for sporadic speech**: Not optimized for emergency radio patterns

### Expected Performance

- **Model loading**: 10-30 seconds (first run only)
- **Speech detection**: <100ms per chunk
- **Transcription**: 1-3 seconds per speech segment
- **Total latency**: 2-5 seconds from speech start to text output
- **Memory usage**: ~2-4GB during operation
- **CPU usage**: Moderate during speech processing, minimal during silence

## Sample Output

```
🚀 Initializing BroadcastifyTranscriber for feed 31880
⚙️ AudioProcessor Configuration:
   📏 Chunk duration: 2.0s
   🔄 Buffer overlap: 0.5s
   🎵 Sample rate: 16000Hz
   🔇 VAD energy threshold: 0.01
🔄 Loading NVIDIA Parakeet TDT model: nvidia/parakeet-tdt-0.6b-v2...
✅ Parakeet model loaded successfully!
✅ All components initialized successfully!

🚀 Starting continuous transcription with VAD...
🌐 Loading Broadcastify feed 31880...
✅ Audio element found!
📻 Feed Name: Sacramento County Sheriff
🎵 Starting real-time audio streaming...
📡 Streaming audio data with real-time VAD...

🔍 VAD Analysis: energy=0.003 spectral=0.421 duration=2.0s → SILENCE
🔍 VAD Analysis: energy=0.045 spectral=0.678 duration=2.0s → SPEECH
🎙️ Speech detected! Yielding audio chunk for transcription

🔄 Processing speech chunk #1...
🧠 Running Parakeet transcription...
✅ Transcription successful!

🎙️ [2025-06-08 15:30:42] Sacramento County Sheriff (Feed 31880):
📝 TRANSCRIPTION: Unit 23, respond to a 211 in progress at Oak and Main.
⏰ Word-level timestamps (11 words):
    🔹 [0.1s-0.4s] Unit
    🔹 [0.5s-0.9s] 23,
    🔹 [1.0s-1.4s] respond
    🔹 [1.5s-1.7s] to
    🔹 [1.8s-1.9s] a
    🔹 [2.0s-2.4s] 211
    🔹 [2.5s-2.7s] in
    🔹 [2.8s-3.2s] progress
    🔹 [3.3s-3.5s] at
    🔹 [3.6s-3.8s] Oak
    🔹 [3.9s-4.1s] and
    🔹 [4.2s-4.5s] Main.
================================================================================
```

## How It Works

1. **Model Loading**: Downloads and loads NVIDIA's Parakeet TDT 0.6B model (~600MB on first run)
2. **Stream Extraction**: Uses Selenium to extract direct audio stream URL from Broadcastify
3. **Audio Processing**: Captures 30-second chunks and resamples to 16kHz mono
4. **ASR Transcription**: Processes audio with Parakeet TDT for high-accuracy speech recognition
5. **Timestamp Extraction**: Provides word-level timing information
6. **Output Display**: Shows timestamped transcriptions with enhanced punctuation/capitalization

## Model Performance

- **Word Error Rate**: 6.05% average (significantly better than Whisper's ~10-15%)
- **Inference Speed**: RTFx 3380 with batch processing
- **Language**: Optimized for English speech recognition
- **Audio Quality**: Robust to noise and various audio conditions

## Troubleshooting

- **Chrome not found**: Install Google Chrome browser
- **Import errors**: Make sure virtual environment is activated and dependencies are installed
- **NeMo toolkit issues**: Ensure PyTorch is compatible with your system
- **CUDA errors**: GPU acceleration is optional; CPU inference will work but be slower
- **Stream URL not found**: The feed might be offline or the page structure changed
- **Audio capture fails**: Check internet connection and feed availability
- **Model download fails**: Ensure stable internet connection for initial 600MB download

## Dependencies

- `requests`: HTTP library for audio streaming
- `selenium`: Web automation for stream URL extraction
- `nemo_toolkit[asr]`: NVIDIA NeMo toolkit with ASR capabilities
- `torch` & `torchaudio`: PyTorch framework for deep learning
- `librosa`: Audio processing library
- `soundfile`: Audio file I/O operations
- `webdriver-manager`: Automatic ChromeDriver management

## Notes

- **First run**: Downloads Parakeet TDT model (~600MB) - ensure stable internet
- **Performance**: GPU acceleration recommended but not required
- **Audio quality**: 16kHz mono audio provides best results
- **Licensing**: Model available under CC-BY-4.0 license for commercial/non-commercial use
- **Temporary files**: Audio files are created and cleaned up automatically
- **Feed availability**: Some feeds may require authentication or have geographic restrictions
