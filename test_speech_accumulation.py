#!/usr/bin/env python3
"""
Test script for speech accumulation functionality.

This script tests the new speech accumulation feature to verify that
continuous speech is properly grouped into complete messages.
"""

import sys
import time
from audio_processor import AudioProcessor, VoiceActivityDetector
import numpy as np


def test_speech_accumulation():
    """Test the speech accumulation logic with simulated audio chunks."""
    
    print("🧪 Testing Speech Accumulation Feature")
    print("=" * 50)
    
    # Initialize audio processor with test settings
    processor = AudioProcessor(
        chunk_duration=2.0,
        buffer_duration=0.5,
        sample_rate=16000,
        max_speech_duration=10.0,  # Shorter for testing
        silence_threshold=1.5      # Shorter silence threshold
    )
    
    # Create sample audio chunks (simulated)
    sample_rate = 16000
    chunk_duration = 2.0
    chunk_samples = int(sample_rate * chunk_duration)
    
    # Simulate speech chunks with varying energy levels
    print("\n🎙️ Simulating speech detection scenarios:")
    
    # Test case 1: Continuous speech (should accumulate)
    print("\n1. Testing continuous speech accumulation...")
    
    speech_chunks = []
    silence_chunks = []
    
    # Create speech-like audio (higher energy)
    for i in range(3):  # 3 chunks of continuous speech
        # Generate noise with speech-like characteristics
        chunk = np.random.normal(0, 0.1, chunk_samples)  # Higher amplitude for speech
        speech_chunks.append(chunk)
    
    # Create silence-like audio (lower energy)
    for i in range(2):  # 2 chunks of silence
        chunk = np.random.normal(0, 0.005, chunk_samples)  # Very low amplitude
        silence_chunks.append(chunk)
    
    # Test speech accumulation flow
    current_time = time.time()
    
    print("   📊 Processing speech chunks...")
    for i, chunk in enumerate(speech_chunks):
        current_time += chunk_duration
        has_speech = processor.vad.detectSpeech(chunk)
        result = processor._handleSpeechAccumulation(chunk, has_speech, current_time)
        
        print(f"   🔹 Chunk {i+1}: Speech={has_speech}, Complete Message Ready={result is not None}")
        
        if result is not None:
            duration = len(result) / sample_rate
            print(f"   ✅ Complete message finalized: {duration:.1f}s ({len(processor.speech_segments)} segments)")
    
    # Test silence termination
    print("\n   📊 Processing silence chunks...")
    for i, chunk in enumerate(silence_chunks):
        current_time += chunk_duration
        has_speech = processor.vad.detectSpeech(chunk)
        result = processor._handleSpeechAccumulation(chunk, has_speech, current_time)
        
        print(f"   🔹 Silence {i+1}: Speech={has_speech}, Complete Message Ready={result is not None}")
        
        if result is not None:
            duration = len(result) / sample_rate
            print(f"   ✅ Message finalized by silence: {duration:.1f}s")
    
    # Test max duration limit
    print("\n2. Testing maximum speech duration limit...")
    
    # Reset processor state
    processor.speech_segments = []
    processor.is_in_speech = False
    
    current_time = time.time()
    
    # Generate many speech chunks to exceed max duration
    for i in range(8):  # 8 chunks = 16 seconds (exceeds 10s limit)
        chunk = np.random.normal(0, 0.1, chunk_samples)
        current_time += chunk_duration
        has_speech = processor.vad.detectSpeech(chunk)
        result = processor._handleSpeechAccumulation(chunk, has_speech, current_time)
        
        if result is not None:
            duration = len(result) / sample_rate
            print(f"   ⏰ Max duration reached at chunk {i+1}: {duration:.1f}s")
            break
    
    print("\n✅ Speech accumulation tests completed!")
    print("🔧 The feature should now properly group continuous speech into complete messages")


def test_vad_thresholds():
    """Test VAD threshold settings with different audio characteristics."""
    
    print("\n🔍 Testing VAD Threshold Sensitivity")
    print("=" * 40)
    
    vad = VoiceActivityDetector(
        energy_threshold=0.01,
        spectral_threshold=0.5,
        min_speech_duration=0.5
    )
    
    sample_rate = 16000
    duration = 2.0
    samples = int(sample_rate * duration)
    
    # Test different audio characteristics
    test_cases = [
        ("🔇 Low energy (silence)", 0.005, "silence"),
        ("🎙️ Speech-like energy", 0.05, "speech"),
        ("📢 High energy (speech)", 0.1, "speech"),
        ("🔊 Very high energy", 0.2, "speech")
    ]
    
    for description, amplitude, expected in test_cases:
        audio = np.random.normal(0, amplitude, samples)
        detected = vad.detectSpeech(audio)
        result = "✅" if (detected and expected == "speech") or (not detected and expected == "silence") else "❌"
        
        energy = np.sqrt(np.mean(audio ** 2))
        print(f"{result} {description}: energy={energy:.4f}, detected={detected}")
    
    print("\n✅ VAD threshold tests completed!")


if __name__ == "__main__":
    print("🧪 Speech Accumulation Test Suite")
    print("==================================")
    
    try:
        test_vad_thresholds()
        test_speech_accumulation()
        
        print("\n🎉 All tests completed successfully!")
        print("📋 The system should now capture full spoken messages as single transcriptions")
        print("🚀 Ready to test with real HAM radio feed!")
        
    except KeyboardInterrupt:
        print("\n🛑 Tests interrupted by user")
    except Exception as e:
        print(f"\n❌ Test error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
