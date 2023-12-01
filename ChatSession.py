import sounddevice as sd
import wave
import threading
import queue

# Parameters
fs = 44100  # Sample rate
channels = 1  # Number of channels
filename = 'output.wav'  # Filename for the output file
format = sd.default.dtype[1]  # Default data type for sounddevice

# Queue to manage audio frames
q = queue.Queue()

# Function to record audio
def record_audio(stop_event):
  with sd.InputStream(samplerate=fs, channels=channels, dtype=format, callback=callback):
    while not stop_event.is_set():
      sd.sleep(1000)
    while not q.empty():
      wf.writeframes(q.get())

# Callback function to collect data from the stream
def callback(indata, frames, time, status):
  q.put(indata.copy().tobytes())

# Initialize stop event and thread
stop_event = threading.Event()
recording_thread = threading.Thread(target=record_audio, args=(stop_event,))
is_recording = False

# Main loop
while True:
  command = input("Enter 'r' to start, 's' to stop, 'q' to quit: ").lower()

  if command == "r" and not is_recording:
    is_recording = True
    stop_event.clear()
    recording_thread = threading.Thread(target=record_audio, args=(stop_event,))
    recording_thread.start()
    print("Recording started.")

  elif command == "s" and is_recording:
    is_recording = False
    stop_event.set()
    recording_thread.join()
    print("Recording stopped.")

  elif command == "q":
    if is_recording:
      is_recording = False
      stop_event.set()
      recording_thread.join()
    print("Exiting program.")
    break

# Save as WAV file if recording was done
if not q.empty():
  with wave.open(filename, 'wb') as wf:
    wf.setnchannels(channels)
    wf.setsampwidth(sd.default.samplerate // 8)
    wf.setframerate(fs)
    while not q.empty():
      wf.writeframes(q.get())
  print(f"Audio saved as {filename}")
else:
  print("No audio recorded.")
