import AudioHandler as ah
import AudioTextTransformer as att

def main():
    sys_audio = ah.AudioHandler(":2")
    a2t = att.AudioTextTransformer("model","score") # deepsppech model
    sys_audio.start_recording("audio_file.wav")
    sys_audio.stop_recording()
    text = a2t.audio2file("audio_file.wav")
    print(text)
