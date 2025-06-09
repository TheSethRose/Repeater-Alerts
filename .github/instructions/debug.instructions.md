---
applyTo: "**"
---

# Error Handling & Debugging Instructions

You are a senior debugging specialist focused on systematic problem-solving and error resolution.

Apply the [general coding standards](../prompts/general.instructions.md) when handling errors and debugging code.

## Project-Specific Error Categories

- Audio Processing Errors: Model loading failures, audio format issues, transcription timeout
- Network Errors: Stream connection failures, Broadcastify URL extraction issues, timeout errors
- Browser Automation Errors: Selenium WebDriver failures, Chrome/Chromium not found, headless mode issues
- Performance Errors: Memory leaks from audio buffers, model inference bottlenecks, queue overflow

## Project-Specific Debugging Scenarios

#### Audio Processing Issues

- Verify NVIDIA NeMo model download and loading
- Check audio format compatibility (ensure MP3/MPEG streams)
- Monitor memory usage during model inference
- Validate sample rate conversion (16kHz target)
- Test with different audio chunk sizes

#### Network Issues

- Check Broadcastify stream URL validity and accessibility
- Verify internet connection and proxy settings
- Monitor HTTP response codes and content types
- Test stream continuity and reconnection logic
- Validate SSL/TLS certificate handling

#### Browser Automation Issues

- Ensure Chrome/Chromium browser is installed and accessible
- Check WebDriver compatibility with browser version
- Verify headless mode operation and user agent settings
- Test Selenium element detection and page loading
- Monitor browser process cleanup and resource usage

#### Performance Debugging

- Profile NVIDIA model loading and inference times
- Monitor audio buffer memory allocation and cleanup
- Check for audio queue overflow and threading issues
- Analyze real-time factor (RTF) for transcription speed
- Test with different chunk durations and overlap settings
- Verify lifecycle dependencies and cleanup
- Monitor re-render frequency and performance
- Test with different data states (loading, error, empty)

#### Performance Debugging

- Use browser performance tools and lighthouse
- Monitor database query execution times
- Check for memory leaks with heap snapshots
- Analyze bundle size and code splitting
- Profile framework component render performance

### Debugging Tools

#### Development Tools

- Python Debugger (pdb): Breakpoints and variable inspection for transcription logic
- Chrome DevTools: Network tab for monitoring Broadcastify stream connections
- Python logging: Structured logging with emoji prefixes for operation tracking
- htop/Activity Monitor: Memory and CPU usage monitoring for model inference
- Audio Analysis Tools: librosa for audio format validation and signal analysis

#### Production Debugging

- Exception Logging: Comprehensive error logging with context for stream failures
- Performance Monitoring: Real-time factor (RTF) tracking for transcription speed
- Network Monitoring: Stream connection health and reconnection attempts
- Memory Profiling: Audio buffer usage and model memory consumption tracking

### Error Testing Strategy

#### Audio Processing Testing

```python
# Test audio format compatibility
def test_audio_format_handling():
    transcriber = BroadcastifyTranscriber()
    # Test with different audio formats
    test_audio = generate_test_audio(format='mp3')
    result = transcriber.transcribe_audio(test_audio)
    assert result is not None

# Test network failure scenarios
def test_stream_connection_failure():
    transcriber = BroadcastifyTranscriber()
    with mock.patch('requests.get') as mock_get:
        mock_get.side_effect = requests.ConnectionError()
        result = transcriber.capture_audio_stream("invalid_url")
        assert result is None
```

- Health Checks: Endpoint monitoring and alerting
- User Session Recording: For reproducing user-reported issues

### Error Reporting Standards

#### Log Levels

- ERROR: System errors requiring immediate attention
- WARN: Potential issues that should be monitored
- INFO: General application flow information
- DEBUG: Detailed debugging information (development only)

#### Structured Logging

```typescript
const logger = {
  error: (message: string, error: Error, context?: Record<string, any>) => {
    console.error(
      JSON.stringify({
        level: "ERROR",
        message,
        error: {
          name: error.name,
          message: error.message,
          stack: error.stack,
        },
        context,
        timestamp: new Date().toISOString(),
      })
    );
  },
};
```

### Task Management Integration

#### Bug Tracking

- Create subtasks in Task 18 for all discovered bugs
- Include reproduction steps, expected vs actual behavior
- Add severity level and impact assessment
- Link to related code files and line numbers

#### Network Error Testing

- Mock Broadcastify connection failures and timeouts
- Test stream URL extraction with invalid pages
- Verify graceful handling of audio stream interruptions
- Test browser automation with missing Chrome/Chromium
- Validate retry logic for temporary network issues

#### Model Error Testing

- Test behavior with corrupted or missing model files
- Verify error handling for insufficient memory scenarios
- Test transcription with various audio quality levels
- Mock model loading failures and recovery
- Validate audio format conversion edge cases
