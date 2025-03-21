import numpy as np
import sounddevice as sd

# MFSK Parameters
base_freq = 500  # Starting frequency in Hz
step = 60        # Frequency step between characters
duration = 0.025 # Duration of each character in seconds
sample_rate = 44100  # Audio sample rate

def generate_mfsk_signal(message):
    """Generate MFSK audio signal for the given message."""
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    audio = np.array([])

    for char in message:
        freq = base_freq + step * ord(char)
        tone = np.sin(2 * np.pi * freq * t)
        audio = np.append(audio, tone)

    # Add silence before and after to avoid clipping
    silence = np.zeros(int(sample_rate * 0.1))
    audio = np.concatenate((silence, audio, silence))

    # Normalize to 16-bit PCM format
    audio = (audio / np.max(np.abs(audio)) * 0.8).astype(np.float32)
    return audio

def play_mfsk_signal(message):
    """Play the generated MFSK signal through the speaker."""
    audio = generate_mfsk_signal(message)
    sd.play(audio, sample_rate)
    sd.wait()
    print(f"Transmitted: {message}")

if __name__ == "__main__":
    msg = input("Enter message to send: ")
    play_mfsk_signal(msg)
