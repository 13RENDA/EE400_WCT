# import numpy as np
# from scipy.io import wavfile
# from scipy.signal import resample

# def resample_wav(input_wav, output_wav, target_sample_rate):
#     # Read the original WAV file
#     original_sample_rate, data = wavfile.read(input_wav)

#     # Resample the data to the target sample rate
#     data_resampled = resample(data, int(len(data) * target_sample_rate / original_sample_rate))

#     # Save the resampled data as a new WAV file
#     wavfile.write(output_wav, target_sample_rate, data_resampled)

# # Replace 'your_input_wav.wav' with the path to your input WAV file
# # Replace 'your_output_wav.wav' with the desired output WAV file path
# # Replace 44100 with the target sample rate you want
# resample_wav('t3.wav', 't4.wav', target_sample_rate=16000)

import numpy as np
from scipy.io import wavfile

def wav_to_numpy_int16_and_save(wav_file, output_file):
    # Read the WAV file
    sample_rate, data = wavfile.read(wav_file)

    # Ensure the data is in the correct format (numpy.int16)
    if data.dtype != np.int16:
        data = (data * 32767).astype(np.int16)

    # Save the NumPy array to a binary file
    np.save(output_file, data)

    return sample_rate

# Replace '/path/to/your/your_output_wav.wav' with the path to your WAV file
# Replace '/path/to/your/output_array.npy' with the desired output binary file path
sample_rate = wav_to_numpy_int16_and_save('t3.wav', 't3array.npy')

# Now you can use 'sample_rate' and 'output_array.npy' as needed
