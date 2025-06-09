#!/usr/bin/env python3
"""
Test script to compare legacy vs VAD transcription approaches.

This script allows testing both the original fixed-chunk approach
and the new voice activity detection approach side by side.
"""

import sys
import time
from transcriber_new import BroadcastifyTranscriber


def test_vad_mode(feed_id: str, duration: int = 60):
    """Test the new VAD-based transcription mode."""
    print("🧪 Testing VAD Mode (Voice Activity Detection)")
    print("=" * 60)
    
    transcriber = BroadcastifyTranscriber(feed_id=feed_id)
    
    print(f"⏱️ Running VAD test for {duration} seconds...")
    start_time = time.time()
    
    try:
        transcriber.runContinuousTranscription()
    except KeyboardInterrupt:
        print("\n🛑 VAD test stopped by user")
    
    elapsed = time.time() - start_time
    print(f"✅ VAD test completed in {elapsed:.1f} seconds")
    
    return transcriber.getStatus()


def test_legacy_mode(feed_id: str, cycles: int = 3):
    """Test the legacy fixed-chunk transcription mode."""
    print("🧪 Testing Legacy Mode (Fixed 30s chunks)")
    print("=" * 60)
    
    transcriber = BroadcastifyTranscriber(feed_id=feed_id)
    
    print(f"⏱️ Running legacy test for {cycles} cycles...")
    
    # Override the continuous mode to stop after specified cycles
    original_run = transcriber.runLegacyMode
    cycle_count = 0
    
    def limited_legacy():
        nonlocal cycle_count
        transcriber.is_running = True
        
        # Get stream information
        stream_url, feed_name = transcriber.stream_extractor.extractStreamUrl()
        
        if not stream_url or not feed_name:
            print("❌ Failed to get stream URL or feed name")
            return
        
        while transcriber.is_running and cycle_count < cycles:
            cycle_count += 1
            print(f"\n🔄 Cycle {cycle_count}/{cycles}")
            
            try:
                for audio_chunk in transcriber.audio_processor.streamAudioChunks(stream_url):
                    transcription, word_timestamps = transcriber.transcription_model.transcribeAudio(audio_chunk)
                    
                    if transcription and len(transcription.strip()) > 0:
                        transcriber._printTranscription(transcription, feed_name, word_timestamps)
                    else:
                        print("🔇 No speech detected in this chunk")
                    break
                
                if cycle_count < cycles:
                    print(f"⏸️ Waiting 5 seconds before next cycle...")
                    time.sleep(5)
                    
            except Exception as e:
                print(f"❌ Error in cycle {cycle_count}: {e}")
                break
    
    start_time = time.time()
    
    try:
        limited_legacy()
    except KeyboardInterrupt:
        print("\n🛑 Legacy test stopped by user")
    
    elapsed = time.time() - start_time
    print(f"✅ Legacy test completed in {elapsed:.1f} seconds ({cycle_count} cycles)")
    
    return transcriber.getStatus()


def main():
    """Main test runner."""
    print("🧪 Broadcastify Transcriber Comparison Test")
    print("=" * 80)
    
    feed_id = "31880"
    
    if len(sys.argv) > 1:
        if sys.argv[1] in ['-h', '--help']:
            print("Usage: python test_transcriber.py [feed_id] [mode]")
            print("  feed_id: Broadcastify feed ID (default: 31880)")
            print("  mode: 'vad', 'legacy', or 'both' (default: both)")
            return
        
        feed_id = sys.argv[1]
        mode = sys.argv[2] if len(sys.argv) > 2 else 'both'
    else:
        mode = 'both'
    
    print(f"📡 Testing feed: {feed_id}")
    print(f"🎯 Test mode: {mode}")
    print()
    
    if mode in ['vad', 'both']:
        print("🚀 Starting VAD Mode Test...")
        vad_status = test_vad_mode(feed_id, duration=60)
        print(f"📊 VAD Status: {vad_status}")
        
        if mode == 'both':
            print("\n" + "="*80)
            time.sleep(2)
    
    if mode in ['legacy', 'both']:
        print("🚀 Starting Legacy Mode Test...")
        legacy_status = test_legacy_mode(feed_id, cycles=3)
        print(f"📊 Legacy Status: {legacy_status}")
    
    print("\n✅ All tests completed!")


if __name__ == "__main__":
    main()
