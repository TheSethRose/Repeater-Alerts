# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

### Added
- Initial release of Repeater Alerts monitoring system
- Real-time HAM radio transcription using NVIDIA Parakeet TDT model
- Voice Activity Detection (VAD) for efficient processing
- Intelligent reconnection system with dual exponential backoff
- Support for Broadcastify feed monitoring
- Comprehensive documentation and setup guides
- GitHub CI/CD workflow for automated testing

### Features
- **Advanced Audio Processing**: Real-time VAD with speech accumulation
- **High-Quality Transcription**: NVIDIA Parakeet TDT model (6.05% WER)
- **24/7 Operation**: Robust reconnection handling for continuous monitoring
- **Multiple Feed Support**: Easy switching between repeater feeds
- **Word-Level Timestamps**: Precise timing information for transcriptions

### Documentation
- Complete README with usage examples and configuration
- RECONNECTION_GUIDE.md explaining the intelligent retry system
- MIT License for open source compatibility
- GitHub workflow for continuous integration

### Technical
- Modular architecture with clean separation of concerns
- Comprehensive .gitignore for Python and audio projects
- Automated setup script for easy installation
- Support for both CPU and GPU acceleration

## [1.0.0] - 2024-XX-XX

### Added
- Initial stable release
- Core transcription functionality
- Broadcastify integration
- Documentation and examples
