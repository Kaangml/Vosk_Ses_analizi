import pyaudio
import wave

def record_audio(duration=5, filename="output.wav"):
    # Ses kaydı parametreleri
    chunk = 1024  # Her seferde okunan veri miktarı
    sample_format = pyaudio.paInt16  # 16-bit
    channels = 1  # Mono kayıt
    fs = 44100  # Örnekleme hızı (Hz)
    seconds = duration  # Kayıt süresi

    p = pyaudio.PyAudio()  

    print("Kayıt başlatıldı...")

    # Mikrofonu başlatma
    stream = p.open(format=sample_format,
                    channels=channels,
                    rate=fs,
                    frames_per_buffer=chunk,
                    input=True)

    frames = []  

    # Kayıt süresince mikrofon verisini okuma
    for _ in range(0, int(fs / chunk * seconds)):
        data = stream.read(chunk)
        frames.append(data)

    # Kaydı sonlandırma
    stream.stop_stream()
    stream.close()
    p.terminate()

    print("Kayıt tamamlandı.")

    # Kayıt edilen veriyi bir dosyaya yazma
    wf = wave.open(filename, 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(p.get_sample_size(sample_format))
    wf.setframerate(fs)
    wf.writeframes(b''.join(frames))
    wf.close()

# 5 saniyelik bir ses kaydı alalım
record_audio(duration=10)
