import numpy as np
from scipy.io import wavfile

def decode_mfsk_signal(filename, sample_rate=44100):
    base_freq = 500
    step = 60
    duration = 0.025  # Must match sender
    window_size = int(sample_rate * duration)

    rate, data = wavfile.read(filename)
    if rate != sample_rate:
        print(f"Warning: sample rate mismatch ({rate} != {sample_rate})")

    data = data.astype(np.float32) / 32767.0

    # Skip the initial and final silence
    data = data[int(sample_rate * 0.1):-int(sample_rate * 0.1)]

    message = ""
    for i in range(0, len(data), window_size):
        chunk = data[i:i + window_size]
        if len(chunk) < window_size:
            break

        # Apply a window to smooth edges
        windowed = chunk * np.hanning(len(chunk))
        spectrum = np.fft.fft(windowed)
        freqs = np.fft.fftfreq(len(spectrum), 1 / sample_rate)

        peak_index = np.argmax(np.abs(spectrum[:len(spectrum)//2]))
        peak_freq = freqs[peak_index]

        # Convert frequency to ASCII char
        char_code = int(round((peak_freq - base_freq) / step))
        if 0 <= char_code <= 127:
            message += chr(char_code)
        else:
            message += '?'  # fallback

    return message

if __name__ == "__main__":
    filename = input("Enter filename to decode (default: mfsk_output.wav): ") or "mfsk_output.wav"
    decoded = decode_mfsk_signal(filename)
    print(f"Decoded message: {decoded}")
