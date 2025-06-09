# Project Structure

```
broadcast/
├── README.md                     # Main project documentation
├── requirements.txt              # Python dependencies
├── setup.sh                     # Automated setup script
├── .gitignore                   # Git ignore patterns
│
├── transcriber.py               # Main application entry point
├── audio_processor.py           # Audio streaming, VAD, and speech accumulation
├── stream_extractor.py          # Broadcastify URL extraction via Selenium
├── transcription_model.py       # NVIDIA Parakeet model management
│
├── docs/                        # Documentation
│   └── RECONNECTION_GUIDE.md    # Detailed reconnection system guide
│
└── .github/                     # GitHub configuration
    ├── instructions/            # Copilot instructions
    └── prompts/                 # Code generation prompts
```

## Core Components

### Main Application
- **`transcriber.py`**: CLI entry point and main orchestration
- **`audio_processor.py`**: Real-time audio processing with VAD
- **`stream_extractor.py`**: Browser automation for stream URL extraction
- **`transcription_model.py`**: NVIDIA NeMo model wrapper

### Configuration
- **`requirements.txt`**: All Python dependencies
- **`setup.sh`**: Automated environment setup
- **`.gitignore`**: Standard Python/audio project ignores

### Documentation
- **`README.md`**: Quick start and usage guide
- **`docs/RECONNECTION_GUIDE.md`**: Detailed reconnection system documentation

## Removed Files

During cleanup, the following obsolete files were removed:
- `transcriber_original.py` - Legacy implementation
- `test_transcriber.py` - Broken test referencing non-existent files
- `test_speech_accumulation.py` - Development test, not production-ready
- `status_check.py` - Redundant functionality
- `__pycache__/` - Python cache files
