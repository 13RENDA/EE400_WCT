# Audio to Text tranlation object. Wrapper object for Deepspeech operations
import deepspeech as ds
import numpy as np
import wave

class AudioTextTransformer:
  # class constructor
  def __new__(cls, *args, **kwargs):
    return super().__new__(cls)

  # initializer
  # set up deepspeech model and enable scorer to improve performance
  def __init__(self, deepspeech_model_filename, deepspeech_scorer_filename):
    self.model = ds.Model(deepspeech_model_filename)
    self.model.enableExternalScorer(deepspeech_scorer_filename)
    
  # function that transcribed mono-channel, 16kHz wave file into text string output  
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