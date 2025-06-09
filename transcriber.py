"""
Real-time HAM Radio Transcriber for Broadcastify Streams

This module provides real-time transcription of HAM radio communications
with voice activity detection to efficiently handle periods of silence
common in emergency radio feeds.
"""

import time
from typing import Optional, Dict, Any, List
from stream_extractor import StreamExtractor
from audio_processor import AudioProcessor
from transcription_model import TranscriptionModel


class BroadcastifyTranscriber:
    """
    Main orchestrator for real-time HAM radio transcription.
    
    Combines stream extraction, voice activity detection, and ASR transcription
    to provide efficient real-time monitoring of Broadcastify feeds.
    """
    
    def __init__(self, feed_id: str = "31880"):
        """
        Initialize the transcriber for a specific Broadcastify feed.
        
        Args:
            feed_id: Broadcastify feed identifier
        """
        self.feed_id = feed_id
        self.is_running = False
        
        print(f"🚀 Initializing BroadcastifyTranscriber for feed {feed_id}")
        
        # Initialize components
        self.stream_extractor = StreamExtractor(feed_id)
        self.audio_processor = AudioProcessor(
            chunk_duration=2.0,        # 2-second processing chunks
            buffer_duration=0.5,       # 0.5-second overlap
            sample_rate=16000,
            max_speech_duration=30.0,  # Max 30s for complete messages
            silence_threshold=4.0,     # 4s silence ends message (more tolerant)
            min_message_duration=1.0   # Minimum 1s for valid message
        )
        self.transcription_model = TranscriptionModel()
        
        print("✅ All components initialized successfully!")
    
    def _printTranscription(self, 
                          transcription: str, 
                          feed_name: str, 
                          word_timestamps: Optional[List[Dict[str, Any]]] = None) -> None:
        """
        Print transcription results to console with clean formatting.
        
        Args:
            transcription: The transcribed text
            feed_name: Name of the audio feed
            word_timestamps: Optional word-level timestamp data (not displayed)
        """
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        print(f"\n🎙️ [{timestamp}] {feed_name} (Feed {self.feed_id}):")
        print(f"📝 {transcription}")
        print("=" * 80)
    
    def runContinuousTranscription(self) -> None:
        """
        Main loop for continuous real-time transcription with VAD.
        
        Uses voice activity detection to process only audio segments
        containing speech, making it efficient for HAM radio feeds
        with long periods of silence.
        """
        print("🚀 Starting continuous transcription with VAD...")
        print("❌ Press Ctrl+C to stop\n")
        
        # Extract stream information once
        print("🔍 Getting stream information...")
        stream_url, feed_name = self.stream_extractor.extractStreamUrl()
        
        if not stream_url or not feed_name:
            print("❌ Failed to get stream URL or feed name")
            return
        
        print(f"✅ Stream ready! Starting real-time transcription with speech accumulation...")
        print("📋 Complete messages will be transcribed as single units")
        self.is_running = True
        
        message_count = 0
        
        try:
            # Stream complete speech messages with voice activity detection
            for complete_message in self.audio_processor.streamAudioChunks(stream_url):
                if not self.is_running:
                    break
                
                message_count += 1
                
                # Transcribe the complete speech message
                transcription, word_timestamps = self.transcription_model.transcribeAudio(complete_message)
                
                if transcription and len(transcription.strip()) > 0:
                    self._printTranscription(transcription, feed_name, word_timestamps)
                else:
                    print("⚠️ No transcription returned")
                
        except KeyboardInterrupt:
            print("\n🛑 Stopping transcription...")
            self.is_running = False
        except Exception as e:
            print(f"❌ Error in transcription loop: {e}")
            import traceback
            print(f"🔍 Full error trace: {traceback.format_exc()}")
        finally:
            self.stop()
    
    def runLegacyMode(self) -> None:
        """
        Legacy mode with fixed-duration chunks (for comparison/debugging).
        
        Captures 30-second chunks similar to the original implementation,
        but still uses the modular architecture.
        """
        print("🚀 Starting legacy mode transcription...")
        print("❌ Press Ctrl+C to stop\n")
        
        # Get stream information
        stream_url, feed_name = self.stream_extractor.extractStreamUrl()
        
        if not stream_url or not feed_name:
            print("❌ Failed to get stream URL or feed name")
            return
        
        print(f"✅ Stream ready! Starting legacy transcription loop...")
        self.is_running = True
        loop_count = 0
        
        while self.is_running:
            try:
                loop_count += 1
                print(f"\n🔄 Loop #{loop_count} - Capturing 30-second chunk...")
                
                # Use a single chunk from the audio processor
                for audio_chunk in self.audio_processor.streamAudioChunks(stream_url):
                    transcription, word_timestamps = self.transcription_model.transcribeAudio(audio_chunk)
                    
                    if transcription and len(transcription.strip()) > 0:
                        self._printTranscription(transcription, feed_name, word_timestamps)
                    else:
                        print("🔇 No speech detected in this chunk")
                    
                    # Only process one chunk in legacy mode
                    break
                
                # Brief pause before next chunk
                print(f"⏸️ Waiting 5 seconds before next capture...")
                time.sleep(5)
                
            except KeyboardInterrupt:
                print("\n🛑 Stopping transcription...")
                self.is_running = False
                break
            except Exception as e:
                print(f"❌ Error in main loop: {e}")
                print("⏳ Waiting 10 seconds before retrying...")
                time.sleep(10)
    
    def stop(self) -> None:
        """Stop the transcription process and cleanup resources."""
        print("🛑 Stopping transcription...")
        self.is_running = False
        self.audio_processor.stopStreaming()
        print("✅ Transcription stopped")
    
    def getStatus(self) -> Dict[str, Any]:
        """
        Get current status of the transcriber components.
        
        Returns:
            Dictionary with status information
        """
        return {
            'feed_id': self.feed_id,
            'is_running': self.is_running,
            'model_loaded': self.transcription_model.isModelLoaded(),
            'model_info': self.transcription_model.getModelInfo(),
            'audio_processor_streaming': self.audio_processor.is_streaming
        }


def main():
    """Main entry point for the transcriber application."""
    import sys
    
    # Default feed ID
    feed_id = "31880"
    
    # Parse command line arguments
    if len(sys.argv) > 1:
        if sys.argv[1] in ['-h', '--help']:
            print("Usage: python transcriber.py [feed_id] [--legacy]")
            print("  feed_id: Broadcastify feed ID (default: 31880)")
            print("  --legacy: Use legacy mode with fixed 30-second chunks")
            print("  --vad: Use voice activity detection mode (default)")
            return
        
        # Check for mode flags
        legacy_mode = '--legacy' in sys.argv
        if not legacy_mode and len(sys.argv) > 1 and sys.argv[1] != '--vad':
            feed_id = sys.argv[1]
    else:
        legacy_mode = False
    
    # Initialize transcriber
    transcriber = BroadcastifyTranscriber(feed_id=feed_id)
    
    # Print status
    status = transcriber.getStatus()
    print(f"\n📊 Transcriber Status:")
    print(f"   📡 Feed ID: {status['feed_id']}")
    print(f"   🧠 Model loaded: {status['model_loaded']}")
    print(f"   🎵 Model: {status['model_info']['model_name']}")
    
    try:
        if legacy_mode:
            print(f"\n🔄 Starting in LEGACY mode...")
            transcriber.runLegacyMode()
        else:
            print(f"\n🔄 Starting in VAD mode (voice activity detection)...")
            transcriber.runContinuousTranscription()
    except KeyboardInterrupt:
        transcriber.stop()
        print("\n👋 Goodbye!")


if __name__ == "__main__":
    main()
