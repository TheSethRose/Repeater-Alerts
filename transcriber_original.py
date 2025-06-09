import requests
import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import nemo.collections.asr as nemo_asr
from nemo.collections.asr.models import ASRModel
import io
import os
import librosa
import soundfile as sf
import tempfile
import threading
import queue
import numpy as np
from typing import Optional, Tuple, List

class BroadcastifyTranscriber:
    def __init__(self, feed_id: str = "31880"):
        self.feed_id = feed_id
        self.feed_url = f"https://www.broadcastify.com/webPlayer/{feed_id}"
        print("🔄 Loading NVIDIA Parakeet TDT model...")
        try:
            # Load the model
            model = nemo_asr.models.ASRModel.from_pretrained(
                model_name="nvidia/parakeet-tdt-0.6b-v2"
            )
            
            # Verify the model has the transcribe method
            if hasattr(model, 'transcribe') and callable(getattr(model, 'transcribe')):
                self.asr_model = model
                print("✅ Parakeet model loaded successfully!")
                print(f"🎯 Model configured for feed: {feed_id}")
                print(f"📊 Model type: {type(self.asr_model)}")
            else:
                raise ValueError("Loaded model does not have transcribe method")
                
        except Exception as e:
            print(f"❌ Error loading model: {e}")
            raise
        
        self.is_running = False
        self.audio_queue = queue.Queue()
        self.sample_rate = 16000
        self.chunk_duration = 3.0  # Process 3-second chunks
        self.buffer_duration = 1.0  # 1-second overlap for context
        self.silence_threshold = 0.01  # Threshold for voice activity detection
        self.audio_buffer = np.array([], dtype=np.float32)
        
        print(f"⚙️ Configuration:")
        print(f"   📏 Chunk duration: {self.chunk_duration}s")
        print(f"   🔄 Buffer overlap: {self.buffer_duration}s")
        print(f"   🔇 Silence threshold: {self.silence_threshold}")
        
    def get_stream_url(self) -> Tuple[Optional[str], Optional[str]]:
        """Extract direct stream URL using Selenium"""
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")
        
        driver = webdriver.Chrome(options=chrome_options)
        
        try:
            print(f"🌐 Loading Broadcastify feed {self.feed_id}...")
            driver.get(self.feed_url)
            
            # Wait for audio element
            print("⏳ Waiting for audio element to load...")
            audio_element = WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.TAG_NAME, "audio"))
            )
            print(f"✅ Audio element found!")
            
            # Get stream URL
            stream_url = driver.execute_script("return document.querySelector('audio').src;")
            print(f"🎯 Raw stream URL: {stream_url}")
            
            # Get feed name
            feed_name = driver.execute_script("""
                const titleSelectors = ['.feed-title', 'h1', '.title', '.feed-name'];
                for (let selector of titleSelectors) {
                    const element = document.querySelector(selector);
                    if (element) return element.textContent.trim();
                }
                return 'Feed 31880';
            """)
            
            # Also try to get some page info for debugging
            page_title = driver.execute_script("return document.title;")
            audio_info = driver.execute_script("""
                const audio = document.querySelector('audio');
                if (audio) {
                    return {
                        src: audio.src,
                        currentSrc: audio.currentSrc,
                        readyState: audio.readyState,
                        networkState: audio.networkState,
                        paused: audio.paused,
                        ended: audio.ended
                    };
                }
                return null;
            """)
            
            print(f"📄 Page title: {page_title}")
            print(f"🎵 Audio element info: {audio_info}")
            print(f"🔗 Stream URL found: {stream_url}")
            print(f"📻 Feed Name: {feed_name}")
            
            return stream_url, feed_name
            
        finally:
            driver.quit()
            print("� Web scraping completed, browser session ended")
    
    def capture_audio_stream(self, stream_url: str, duration: int = 30) -> Optional[io.BytesIO]:
        """Capture audio stream in chunks for transcription"""
        try:
            print(f"🎵 Starting audio capture for {duration} seconds...")
            print(f"🔗 Connecting to: {stream_url}")
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                'Accept': 'audio/*,*/*;q=0.9',
                'Accept-Language': 'en-US,en;q=0.5',
                'Accept-Encoding': 'identity',
                'Connection': 'keep-alive',
            }
            
            response = requests.get(stream_url, stream=True, timeout=10, headers=headers)
            response.raise_for_status()
            
            print(f"✅ Connected! Response status: {response.status_code}")
            print(f"📊 Content-Type: {response.headers.get('Content-Type', 'Unknown')}")
            print(f"📊 Content-Length: {response.headers.get('Content-Length', 'Unknown')}")
            
            audio_buffer = io.BytesIO()
            chunk_size = 1024
            total_size = 0
            max_size = duration * 1024 * 128  # Rough estimate for 30 seconds
            start_time = time.time()
            
            print(f"📡 Streaming audio data (target: {max_size} bytes)...")
            chunk_count = 0
            last_update = time.time()
            
            for chunk in response.iter_content(chunk_size=chunk_size):
                if chunk and self.is_running:
                    audio_buffer.write(chunk)
                    total_size += len(chunk)
                    chunk_count += 1
                    
                    current_time = time.time()
                    # Show progress every 2 seconds or every 200 chunks
                    if current_time - last_update >= 2.0 or chunk_count % 200 == 0:
                        elapsed = current_time - start_time
                        rate = total_size / elapsed if elapsed > 0 else 0
                        print(f"� Progress: {total_size:,} bytes in {elapsed:.1f}s (rate: {rate:.0f} bytes/s)")
                        last_update = current_time
                    
                    if total_size >= max_size:
                        print(f"🎯 Target size reached: {total_size:,} bytes")
                        break
                        
                    # Also break after maximum time to prevent hanging
                    if time.time() - start_time > duration + 5:
                        print(f"⏰ Time limit reached: {time.time() - start_time:.1f}s")
                        break
                        
                elif not self.is_running:
                    print("🛑 Capture stopped by user")
                    break
                else:
                    # Empty chunk - check if stream ended
                    if time.time() - start_time > 5:  # Give it 5 seconds
                        print("⚠️ No more data available from stream")
                        break
            
            elapsed_total = time.time() - start_time
            print(f"✅ Audio capture complete: {total_size:,} bytes, {chunk_count:,} chunks in {elapsed_total:.1f}s")
            
            if total_size == 0:
                print("❌ No audio data captured - stream may be offline or inaccessible")
                return None
                
            audio_buffer.seek(0)
            return audio_buffer
            
        except requests.exceptions.RequestException as e:
            print(f"❌ Network error capturing audio: {e}")
            return None
        except Exception as e:
            print(f"❌ Error capturing audio: {e}")
            return None
    
    def transcribe_audio(self, audio_buffer: io.BytesIO) -> Tuple[Optional[str], Optional[List[str]]]:
        """Transcribe audio using NVIDIA Parakeet TDT"""
        try:
            print("🎤 Processing audio for transcription...")
            # Convert audio buffer to format Parakeet can handle
            audio_data = audio_buffer.read()
            print(f"📊 Audio data size: {len(audio_data)} bytes")
            
            # Create temporary file for audio processing
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_file:
                temp_filename = temp_file.name
                temp_file.write(audio_data)
            
            try:
                print("🔄 Loading and resampling audio to 16kHz...")
                # Load and resample audio to 16kHz if needed
                audio, sample_rate = librosa.load(temp_filename, sr=16000, mono=True)
                print(f"📈 Audio loaded: {len(audio)} samples at {sample_rate}Hz")
                
                # Save resampled audio
                sf.write(temp_filename, audio, 16000)
                print("💾 Resampled audio saved")
                
                print("🧠 Running Parakeet transcription...")
                # Transcribe with timestamps
                output = self.asr_model.transcribe([temp_filename], timestamps=True)  # type: ignore
                print(f"📝 Transcription complete, processing results...")
                
                if output and len(output) > 0:
                    transcription = output[0].text.strip()
                    print(f"📄 Raw transcription: '{transcription}' (length: {len(transcription)})")
                    
                    # Get word-level timestamps if available
                    if hasattr(output[0], 'timestamp') and output[0].timestamp:
                        word_timestamps = output[0].timestamp.get('word', [])
                        if word_timestamps:
                            print(f"⏰ Found {len(word_timestamps)} word timestamps")
                            # Print timestamped transcription
                            timestamped_text = []
                            for word_info in word_timestamps:
                                start = word_info.get('start', 0)
                                end = word_info.get('end', 0)
                                word = word_info.get('word', '')
                                timestamped_text.append(f"[{start:.1f}s-{end:.1f}s] {word}")
                            return transcription, timestamped_text
                    else:
                        print("⚠️ No timestamp data available")
                    
                    return transcription, None
                else:
                    print("⚠️ No transcription output received")
                    return None, None
                    
            finally:
                # Clean up temporary file
                if os.path.exists(temp_filename):
                    os.remove(temp_filename)
                    print("🗑️ Temporary file cleaned up")
            
        except Exception as e:
            print(f"❌ Transcription error: {e}")
            import traceback
            print(f"🔍 Full error trace: {traceback.format_exc()}")
            return None, None
    
    def print_transcription(self, transcription: str, feed_name: str, timestamps: Optional[List[str]] = None) -> None:
        """Print transcription to console with timestamp"""
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        print(f"\n🎙️ [{timestamp}] {feed_name} (Feed {self.feed_id}):")
        print(f"📝 TRANSCRIPTION: {transcription}")
        
        # Print word-level timestamps if available
        if timestamps:
            print(f"⏰ Word-level timestamps ({len(timestamps)} words):")
            for ts in timestamps[:10]:  # Show first 10 words with timestamps
                print(f"    🔹 {ts}")
            if len(timestamps) > 10:
                print(f"    📊 ... and {len(timestamps) - 10} more words")
        else:
            print("⚠️ No timestamp data available")
        
        print("=" * 80)
    
    def run_continuous_transcription(self):
        """Main loop for continuous transcription"""
        print("🚀 Starting continuous transcription...")
        print("❌ Press Ctrl+C to stop\n")
        
        # Get stream URL once
        print("🔍 Getting stream information...")
        stream_url, feed_name = self.get_stream_url()
        
        if not stream_url or not feed_name:
            print("❌ Failed to get stream URL or feed name")
            return
        
        print(f"✅ Stream ready! Starting transcription loop...")
        self.is_running = True
        loop_count = 0
        
        while self.is_running:
            try:
                loop_count += 1
                print(f"\n🔄 Loop #{loop_count} - Capturing audio chunk...")
                audio_buffer = self.capture_audio_stream(stream_url, duration=30)
                
                if audio_buffer:
                    print("🎯 Audio captured, starting transcription...")
                    transcription, timestamps = self.transcribe_audio(audio_buffer)
                    
                    if transcription and len(transcription.strip()) > 0:
                        print("✅ Speech detected! Printing results...")
                        self.print_transcription(transcription, feed_name, timestamps)
                    else:
                        print("🔇 No speech detected in this chunk")
                else:
                    print("⚠️ Failed to capture audio buffer")
                
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
                time.sleep(10)  # Wait before retrying
    
    def stop(self):
        """Stop the transcription process"""
        self.is_running = False

# Usage
if __name__ == "__main__":
    transcriber = BroadcastifyTranscriber(feed_id="31880")
    
    try:
        transcriber.run_continuous_transcription()
    except KeyboardInterrupt:
        transcriber.stop()
        print("Transcription stopped")
