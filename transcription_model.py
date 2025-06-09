"""
ASR model management module for NVIDIA NeMo Parakeet transcription.

This module handles loading, configuration, and inference of the
NVIDIA Parakeet TDT ASR model for real-time transcription.
"""

import nemo.collections.asr as nemo_asr
from nemo.collections.asr.models import ASRModel
import tempfile
import os
import soundfile as sf
import numpy as np
import logging
from typing import Optional, Tuple, List, Dict, Any

# Suppress NeMo's verbose logging
logging.getLogger('nemo_logger').setLevel(logging.WARNING)
logging.getLogger('pytorch_lightning').setLevel(logging.WARNING)
os.environ['HYDRA_FULL_ERROR'] = '0'


class TranscriptionModel:
    """Manages NVIDIA Parakeet TDT ASR model for real-time transcription."""
    
    def __init__(self, model_name: str = "nvidia/parakeet-tdt-0.6b-v2"):
        """
        Initialize the ASR model.
        
        Args:
            model_name: Name of the NeMo ASR model to load
        """
        self.model_name = model_name
        self.asr_model: Optional[ASRModel] = None
        self.sample_rate = 16000
        self._loadModel()
    
    def _loadModel(self) -> None:
        """Load the NVIDIA Parakeet TDT model."""
        print(f"🔄 Loading NVIDIA Parakeet TDT model...")
        
        try:
            # Temporarily suppress logging during model load
            original_level = logging.getLogger().level
            logging.getLogger().setLevel(logging.ERROR)
            
            # Load the model
            model = nemo_asr.models.ASRModel.from_pretrained(
                model_name=self.model_name
            )
            
            # Restore logging
            logging.getLogger().setLevel(original_level)
            
            # Verify the model has the transcribe method
            if hasattr(model, 'transcribe') and callable(getattr(model, 'transcribe')):
                self.asr_model = model  # type: ignore
                print("✅ Parakeet model loaded successfully!")
            else:
                raise ValueError("Loaded model does not have transcribe method")
                
        except Exception as e:
            print(f"❌ Error loading model: {e}")
            raise
    
    def transcribeAudio(self, audio: np.ndarray) -> Tuple[Optional[str], Optional[List[Dict[str, Any]]]]:
        """
        Transcribe audio using the loaded ASR model.
        
        Args:
            audio: Audio data as numpy array (16kHz, mono)
            
        Returns:
            Tuple of (transcription_text, word_timestamps) or (None, None) if transcription fails
        """
        if self.asr_model is None:
            print("❌ ASR model not loaded")
            return None, None
        
        try:
            print("🎤 Transcribing audio...")
            print(f"📊 Audio: {len(audio)/self.sample_rate:.1f}s duration")
            
            # Create temporary file for audio processing
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_file:
                temp_filename = temp_file.name
                sf.write(temp_filename, audio, self.sample_rate)
            
            try:
                print("🧠 Running ASR model...")
                # Transcribe with timestamps
                output = self.asr_model.transcribe([temp_filename], timestamps=True)  # type: ignore
                
                if output and len(output) > 0:
                    transcription = output[0].text.strip()
                    
                    # Get word-level timestamps if available
                    word_timestamps = None
                    if hasattr(output[0], 'timestamp') and output[0].timestamp:
                        word_data = output[0].timestamp.get('word', [])
                        if word_data:
                            word_timestamps = []
                            for word_info in word_data:
                                timestamp_entry = {
                                    'word': word_info.get('word', ''),
                                    'start': word_info.get('start', 0),
                                    'end': word_info.get('end', 0)
                                }
                                word_timestamps.append(timestamp_entry)
                    
                    return transcription, word_timestamps
                else:
                    return None, None
                    
            finally:
                # Clean up temporary file
                if os.path.exists(temp_filename):
                    os.remove(temp_filename)
                    
        except Exception as e:
            print(f"❌ Transcription error: {e}")
            import traceback
            print(f"🔍 Full error trace: {traceback.format_exc()}")
            return None, None
    
    def transcribeFromFile(self, filepath: str) -> Tuple[Optional[str], Optional[List[Dict[str, Any]]]]:
        """
        Transcribe audio from file path.
        
        Args:
            filepath: Path to audio file
            
        Returns:
            Tuple of (transcription_text, word_timestamps) or (None, None) if transcription fails
        """
        if self.asr_model is None:
            print("❌ ASR model not loaded")
            return None, None
        
        try:
            print(f"🎤 Transcribing audio file: {filepath}")
            
            # Transcribe with timestamps
            output = self.asr_model.transcribe([filepath], timestamps=True)  # type: ignore
            
            if output and len(output) > 0:
                transcription = output[0].text.strip()
                print(f"📄 Transcription: '{transcription}'")
                
                # Process word timestamps
                word_timestamps = None
                if hasattr(output[0], 'timestamp') and output[0].timestamp:
                    word_data = output[0].timestamp.get('word', [])
                    if word_data:
                        word_timestamps = []
                        for word_info in word_data:
                            timestamp_entry = {
                                'word': word_info.get('word', ''),
                                'start': word_info.get('start', 0),
                                'end': word_info.get('end', 0)
                            }
                            word_timestamps.append(timestamp_entry)
                
                return transcription, word_timestamps
            else:
                return None, None
                
        except Exception as e:
            print(f"❌ File transcription error: {e}")
            return None, None
    
    def isModelLoaded(self) -> bool:
        """Check if the ASR model is properly loaded."""
        return self.asr_model is not None
    
    def getModelInfo(self) -> Dict[str, Any]:
        """Get information about the loaded model."""
        return {
            'model_name': self.model_name,
            'sample_rate': self.sample_rate,
            'is_loaded': self.isModelLoaded(),
            'model_type': type(self.asr_model).__name__ if self.asr_model else None
        }
