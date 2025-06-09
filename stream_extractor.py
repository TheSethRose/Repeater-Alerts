"""
Stream URL extraction module for Broadcastify feeds using Selenium WebDriver.

This module handles browser automation to extract direct audio stream URLs
from Broadcastify web player pages.
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from typing import Optional, Tuple


class StreamExtractor:
    """Handles extraction of audio stream URLs from Broadcastify web pages."""
    
    def __init__(self, feed_id: str):
        """
        Initialize the stream extractor.
        
        Args:
            feed_id: Broadcastify feed identifier
        """
        self.feed_id = feed_id
        self.feed_url = f"https://www.broadcastify.com/webPlayer/{feed_id}"
    
    def _createChromeOptions(self) -> Options:
        """Create Chrome options for headless browser automation."""
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")
        return chrome_options
    
    def extractStreamUrl(self) -> Tuple[Optional[str], Optional[str]]:
        """
        Extract direct stream URL and feed name using Selenium.
        
        Returns:
            Tuple of (stream_url, feed_name) or (None, None) if extraction fails
        """
        chrome_options = self._createChromeOptions()
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
                return 'Feed """ + self.feed_id + """';
            """)
            
            # Get page info for debugging
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
            
        except Exception as e:
            print(f"❌ Error extracting stream URL: {e}")
            return None, None
            
        finally:
            driver.quit()
            print("🌐 Web scraping completed, browser session ended")
