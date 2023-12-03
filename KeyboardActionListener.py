# Object class to manage keyboard inputs for manager program
from pynput import keyboard

class KeyActionListener:
  def __init__(self, on_start=None, on_stop=None, on_quit=None):
    self.on_start = on_start
    self.on_stop = on_stop
    self.on_quit = on_quit
    self.stop_output = None  # Attribute to store the output of stop action

    self.listener = keyboard.Listener(
      on_press=self.on_press,
      on_release=self.on_release)

  def on_press(self, key):
    if key == keyboard.Key.space and self.on_start:
      self.on_start()

  def on_release(self, key):
    if key == keyboard.Key.space and self.on_stop:
      self.stop_output = self.on_stop()  # Store the return value of stop action
    elif key.char == 'q' and self.on_quit:
      self.on_quit()
      return False

  def start(self):
    self.listener.start()

  def join(self):
    self.listener.join()
