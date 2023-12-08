import deepspeech as ds
import numpy as np
import wave
import soundfile as sf
from TTS.utils.synthesizer import Synthesizer

class AudioTextTransformer:
  # class constructor
  def __new__(cls, *args, **kwargs):
    return super().__new__(cls)

  # initialize

  # set up deepspeech model and enable scorer to improve performance
  def __init__(self, 
               deepspeech_model_filename, 
               deepspeech_scorer_filename, 
               tts_model_path, 
               tts_config_path, 
               tts_vocoder_path, 
               tts_vocoder_config_path,
               text_to_audio_wavefile_name):
    
    self.ds_model = ds.Model(deepspeech_model_filename)
    self.ds_model.enableExternalScorer(deepspeech_scorer_filename)
    self.ttl_synthesizer = Synthesizer(tts_model_path, tts_config_path, tts_vocoder_path, tts_vocoder_config_path)
    self.text_to_audio_wavefile_name = text_to_audio_wavefile_name
    
  # function that transcribes mono-channel, 16kHz wave file into text string output  
  def audio2text(self, audio_file):
    # Load the WAV file
    with wave.open(audio_file, 'rb') as audio:
      # Check the audio format
      if audio.getnchannels() != 1 or audio.getsampwidth() != 2 or audio.getframerate() != 16000:
          raise ValueError("Audio file must be WAV format mono PCM 16-bit 16kHz")
      
      frames = audio.getnframes()
      buffer = audio.readframes(frames)
      buffer = np.frombuffer(buffer, dtype=np.int16)

    # Perform speech-to-text on the audio buffer
    return self.model.stt(buffer)

  # function to convert text to a wave file
  def text2audio(self, text, text_to_audio_file_name):
    # Convert text to speech
    wav, _ = self.ttl_synthesizer.tts(text)

    # Save the output as a WAV file
    sf.write(self.text_to_audio_wavefile_name, wav, 22050, format='WAV', subtype='PCM_16')
    return text_to_audio_file_name
