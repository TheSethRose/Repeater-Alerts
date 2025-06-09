"""
Audio processing module for real-time voice activity detection and streaming.

This mo    def __init__(self, 
                 chunk_duration: float = 3.0,
                 buffer_duration: float = 0.5,
                 sample_rate: int = 16000,
                 max_speech_duration: float = 45.0,
                 silence_threshold: float = 3.5,
                 min_message_duration: float = 1.0):ndles audio stream capture, voice activity detection (VAD),
and efficient audio buffer management for real-time transcription.
"""

import requests
import time
import io
import numpy as np
import librosa
import soundfile as sf
import tempfile
import os
from typing import Optional, Tuple, Generator
from collections import deque


class VoiceActivityDetector:
    """Voice Activity Detection using energy-based and spectral methods."""
    
    def __init__(self, 
                 energy_threshold: float = 0.01,
                 spectral_threshold: float = 0.5,
                 min_speech_duration: float = 0.5):
        """
        Initialize VAD with configurable thresholds.
        
        Args:
            energy_threshold: Minimum energy level to consider as speech
            spectral_threshold: Minimum spectral centroid for speech detection
            min_speech_duration: Minimum duration in seconds to consider as speech
        """
        self.energy_threshold = energy_threshold
        self.spectral_threshold = spectral_threshold
        self.min_speech_duration = min_speech_duration
        self.sample_rate = 16000
    
    def detectSpeech(self, audio: np.ndarray) -> bool:
        """
        Detect if audio contains speech using energy and spectral analysis.
        
        Args:
            audio: Audio signal as numpy array
            
        Returns:
            True if speech is detected, False otherwise
        """
        if len(audio) == 0:
            return False
        
        # Energy-based detection
        energy = np.sqrt(np.mean(audio ** 2))
        
        # Spectral centroid for frequency content analysis
        try:
            spectral_centroids = librosa.feature.spectral_centroid(
                y=audio, sr=self.sample_rate)[0]
            spectral_centroid = np.mean(spectral_centroids)
            
            # Normalize spectral centroid (typical speech range: 500-4000 Hz)
            normalized_centroid = spectral_centroid / 4000.0
            
        except Exception:
            # Fallback if spectral analysis fails
            normalized_centroid = 0.5
        
        # Check if audio duration meets minimum speech requirement
        duration = len(audio) / self.sample_rate
        
        # Combined decision
        has_energy = energy > self.energy_threshold
        has_speech_spectrum = normalized_centroid > self.spectral_threshold
        sufficient_duration = duration >= self.min_speech_duration
        
        is_speech = has_energy and has_speech_spectrum and sufficient_duration
        
        # VAD debugging disabled for clean output
        
        return is_speech


class AudioProcessor:
    """Handles real-time audio streaming and processing for HAM radio feeds."""
    
    def __init__(self,
                 chunk_duration: float = 2.0,
                 buffer_duration: float = 0.5,
                 sample_rate: int = 16000,
                 max_speech_duration: float = 30.0,
                 silence_threshold: float = 4.0,
                 min_message_duration: float = 1.0):
        """
        Initialize audio processor with optimized settings for HAM radio.
        
        Args:
            chunk_duration: Duration of each audio chunk to process (seconds)
            buffer_duration: Overlap duration between chunks (seconds)  
            sample_rate: Target sample rate for processing
            max_speech_duration: Maximum duration to accumulate speech (seconds)
            silence_threshold: Duration of silence to end speech accumulation (seconds)
            min_message_duration: Minimum duration to consider a valid message (seconds)
        """
        self.chunk_duration = chunk_duration
        self.buffer_duration = buffer_duration
        self.sample_rate = sample_rate
        self.max_speech_duration = max_speech_duration
        self.silence_threshold = silence_threshold
        self.min_message_duration = min_message_duration
        
        self.audio_buffer = deque(maxlen=int(sample_rate * 10))  # 10-second circular buffer
        self.vad = VoiceActivityDetector(
            energy_threshold=0.003,      # Even lower threshold for better sensitivity
            spectral_threshold=0.25,     # Lower threshold for better detection
            min_speech_duration=0.2      # Shorter minimum for responsiveness
        )
        self.is_streaming = False
        
        # Speech accumulation state
        self.speech_segments = []
        self.last_speech_time = 0
        self.speech_start_time = 0
        self.is_in_speech = False
        self.consecutive_silence_count = 0
        self.speech_chunk_count = 0
        
        print(f"⚙️ AudioProcessor Configuration:")
        print(f"   📏 Chunk duration: {chunk_duration}s")
        print(f"   🔄 Buffer overlap: {buffer_duration}s") 
        print(f"   🎵 Sample rate: {sample_rate}Hz")
    
    def _createHeaders(self) -> dict:
        """Create HTTP headers for audio stream requests."""
        return {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'audio/*,*/*;q=0.9',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'identity',
            'Connection': 'keep-alive',
        }
    
    def streamAudioChunks(self, stream_url: str) -> Generator[np.ndarray, None, None]:
        """
        Stream audio in real-time chunks with voice activity detection and speech accumulation.
        
        Args:
            stream_url: Direct URL to audio stream
            
        Yields:
            Complete speech segments (full messages) rather than individual chunks
        """
        print(f"🎵 Starting real-time audio streaming...")
        print(f"🔗 Connecting to: {stream_url}")
        
        headers = self._createHeaders()
        self.is_streaming = True
        
        try:
            response = requests.get(stream_url, stream=True, timeout=10, headers=headers)
            response.raise_for_status()
            
            print(f"✅ Connected! Response status: {response.status_code}")
            
            audio_data = io.BytesIO()
            chunk_size = 1024
            bytes_collected = 0
            last_process_time = time.time()
            
            print(f"📡 Streaming audio data...")
            
            for chunk in response.iter_content(chunk_size=chunk_size):
                if not self.is_streaming:
                    print("🛑 Streaming stopped by user")
                    break
                    
                if chunk:
                    audio_data.write(chunk)
                    bytes_collected += len(chunk)
                    
                    current_time = time.time()
                    
                    # Process audio every chunk_duration seconds
                    if current_time - last_process_time >= self.chunk_duration:
                        audio_chunk = self._processAudioBuffer(audio_data)
                        
                        if audio_chunk is not None:
                            # Check for speech activity in this chunk
                            has_speech = self.vad.detectSpeech(audio_chunk)
                            
                            # Handle speech accumulation logic
                            complete_message = self._handleSpeechAccumulation(audio_chunk, has_speech, current_time)
                            
                            # Yield complete speech message if ready
                            if complete_message is not None:
                                print(f"📝 Speech message ready ({len(complete_message)/self.sample_rate:.1f}s)")
                                yield complete_message
                        
                        # Reset for next chunk with overlap
                        overlap_bytes = int(bytes_collected * (self.buffer_duration / self.chunk_duration))
                        audio_data.seek(max(0, bytes_collected - overlap_bytes))
                        remaining_data = audio_data.read()
                        audio_data = io.BytesIO()
                        audio_data.write(remaining_data)
                        bytes_collected = len(remaining_data)
                        last_process_time = current_time
                    
        except requests.exceptions.RequestException as e:
            print(f"❌ Network error during streaming: {e}")
        except Exception as e:
            print(f"❌ Error during audio streaming: {e}")
        finally:
            # Finalize any remaining speech message before stopping
            if self.is_in_speech and self.speech_segments:
                print("🏁 Finalizing speech...")
                final_message = self._finalizeSpeechMessage()
                if final_message is not None:
                    yield final_message
            
            self.is_streaming = False
    
    def _processAudioBuffer(self, audio_data: io.BytesIO) -> Optional[np.ndarray]:
        """
        Process raw audio data into numpy array for analysis.
        
        Args:
            audio_data: Raw audio bytes from stream
            
        Returns:
            Processed audio as numpy array or None if processing fails
        """
        try:
            # Create temporary file for audio processing
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_file:
                temp_filename = temp_file.name
                audio_data.seek(0)
                temp_file.write(audio_data.read())
            
            try:
                # Load and resample audio to target sample rate
                audio, _ = librosa.load(temp_filename, sr=self.sample_rate, mono=True)
                return audio
                
            finally:
                # Clean up temporary file
                if os.path.exists(temp_filename):
                    os.remove(temp_filename)
                    
        except Exception as e:
            print(f"⚠️ Error processing audio buffer: {e}")
            return None
    
    def saveAudioChunk(self, audio: np.ndarray, filename: str) -> str:
        """
        Save audio chunk to file for transcription.
        
        Args:
            audio: Audio data as numpy array
            filename: Output filename
            
        Returns:
            Path to saved audio file
        """
        sf.write(filename, audio, self.sample_rate)
        return filename
    
    def stopStreaming(self):
        """Stop the audio streaming process."""
        self.is_streaming = False
        print("🛑 Audio streaming stopped")
    
    def _handleSpeechAccumulation(self, audio_chunk: np.ndarray, has_speech: bool, current_time: float) -> Optional[np.ndarray]:
        """
        Handle accumulation of speech segments into complete messages.
        Uses intelligent speech boundary detection to avoid cutting off natural speech patterns.
        
        Args:
            audio_chunk: Current audio chunk
            has_speech: Whether speech was detected in this chunk
            current_time: Current timestamp
            
        Returns:
            Complete speech message if ready, None otherwise
        """
        if has_speech:
            if not self.is_in_speech:
                # Start new speech segment
                self.is_in_speech = True
                self.speech_start_time = current_time
                self.speech_segments = [audio_chunk]
                self.speech_chunk_count = 1
                self.consecutive_silence_count = 0
            else:
                # Continue accumulating speech
                self.speech_segments.append(audio_chunk)
                self.speech_chunk_count += 1
                self.consecutive_silence_count = 0  # Reset silence counter
                
                speech_duration = current_time - self.speech_start_time
                
                # Check if we've reached maximum speech duration
                if speech_duration >= self.max_speech_duration:
                    return self._finalizeSpeechMessage()
            
            self.last_speech_time = current_time
            
        else:
            # No speech detected in this chunk
            if self.is_in_speech:
                self.consecutive_silence_count += 1
                silence_duration = current_time - self.last_speech_time
                
                # Add chunk to maintain audio continuity (important for natural speech gaps)
                self.speech_segments.append(audio_chunk)
                
                # More intelligent silence detection:
                # - Require longer silence for longer messages
                # - Account for natural speech patterns
                # - Be more tolerant if we might be mid-sentence
                effective_silence_threshold = self.silence_threshold
                
                # For longer messages, allow much more silence tolerance
                speech_duration = current_time - self.speech_start_time
                if speech_duration > 15.0:
                    effective_silence_threshold = self.silence_threshold + 2.0  # Up to 5.5s
                elif speech_duration > 8.0:
                    effective_silence_threshold = self.silence_threshold + 1.5  # Up to 5.0s
                elif speech_duration > 4.0:
                    effective_silence_threshold = self.silence_threshold + 1.0  # Up to 4.5s
                else:
                    effective_silence_threshold = self.silence_threshold + 0.5  # Up to 4.0s
                
                # Additional context: if we have very few speech chunks relative to duration,
                # we might be in a slow/deliberate speech pattern - be more tolerant
                speech_density = self.speech_chunk_count / max(1, speech_duration)
                if speech_density < 0.8:  # Less than 0.8 speech chunks per second
                    effective_silence_threshold += 1.0
                
                # Only finalize if we have enough speech content and sufficient silence
                has_sufficient_content = (
                    self.speech_chunk_count >= 2 and  # At least 2 speech chunks
                    (current_time - self.speech_start_time) >= self.min_message_duration
                )
                
                if silence_duration >= effective_silence_threshold and has_sufficient_content:
                    return self._finalizeSpeechMessage()
                elif silence_duration >= self.silence_threshold * 3:
                    # Force finalization after very long silence (10.5s+), even for short messages
                    return self._finalizeSpeechMessage()
        
        return None
    
    def _finalizeSpeechMessage(self) -> Optional[np.ndarray]:
        """
        Finalize accumulated speech segments into a complete message.
        
        Returns:
            Complete speech message as single audio array
        """
        if not self.speech_segments:
            return None
        
        try:
            # Concatenate all speech segments
            complete_message = np.concatenate(self.speech_segments)
            
            # Calculate message duration
            duration = len(complete_message) / self.sample_rate
            
            # Reset accumulation state
            self.speech_segments = []
            self.is_in_speech = False
            self.speech_start_time = 0
            self.last_speech_time = 0
            self.consecutive_silence_count = 0
            self.speech_chunk_count = 0
            
            return complete_message
            
        except Exception as e:
            print(f"⚠️ Error finalizing speech message: {e}")
            # Reset state on error
            self.speech_segments = []
            self.is_in_speech = False
            self.consecutive_silence_count = 0
            self.speech_chunk_count = 0
            return None
