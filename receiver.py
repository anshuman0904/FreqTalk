import numpy as np
import sounddevice as sd

# MFSK Parameters
base_freq = 500  # Starting frequency in Hz
step = 60        # Frequency step between characters
duration = 0.025 # Duration of each character in seconds
sample_rate = 44100  # Audio sample rate

def decode_mfsk_signal(record_duration):
    """Record and decode MFSK signal from the microphone."""
    print("Listening...")
    recording = sd.rec(int(record_duration * sample_rate), samplerate=sample_rate, channels=1, dtype='float32')
    sd.wait()

    data = recording.flatten()

    # Skip initial and final silence
    data = data[int(sample_rate * 0.1):-int(sample_rate * 0.1)]

    window_size = int(sample_rate * duration)
    message = ""

    for i in range(0, len(data), window_size):
        chunk = data[i:i + window_size]
        if len(chunk) < window_size:
            break

        # Apply a window to smooth edges
        windowed = chunk * np.hanning(len(chunk))
        spectrum = np.fft.fft(windowed)
        freqs = np.fft.fftfreq(len(spectrum), 1 / sample_rate)

        # Find the peak frequency
        peak_index = np.argmax(np.abs(spectrum[:len(spectrum)//2]))
        peak_freq = freqs[peak_index]

        # Convert frequency to ASCII character
        char_code = int(round((peak_freq - base_freq) / step))
        if 0 <= char_code <= 127:
            message += chr(char_code)
        else:
            message += '?'  # fallback if out of range

    return message

if __name__ == "__main__":
    # Duration to record (add silence and buffer)
    record_duration = float(input("Enter record duration (in seconds): "))
    decoded = decode_mfsk_signal(record_duration)
    print(f"Decoded message: {decoded}")
