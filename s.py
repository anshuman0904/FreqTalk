import numpy as np
from scipy.io import wavfile

def generate_mfsk_signal(message, output_file="mfsk_output.wav", sample_rate=44100):
    base_freq = 500  # Starting freq in Hz
    step = 60        # Frequency step between characters
    duration = 0.025 # Duration of each char

    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    audio = np.array([])

    for char in message:
        freq = base_freq + step * ord(char)
        tone = np.sin(2 * np.pi * freq * t)
        audio = np.append(audio, tone)

    # Add a bit of silence before and after
    silence = np.zeros(int(sample_rate * 0.1))
    audio = np.concatenate((silence, audio, silence))

    # Normalize to 16-bit PCM
    audio = (audio / np.max(np.abs(audio)) * 32767).astype(np.int16)
    wavfile.write(output_file, sample_rate, audio)

    print(f"Encoded {len(message)} characters to {output_file}")

if __name__ == "__main__":
    msg = input("Enter message to send: ")
    generate_mfsk_signal(msg)
