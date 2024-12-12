import whisper

def whisper_transcribe(filename):
    # Whisper modelini yükle
    model = whisper.load_model("base")

    # Ses dosyasını metne çevirme
    result = model.transcribe(filename)

    # Sonucu ekrana yazdırma
    print(result["text"])

# Kayıt edilen ses dosyasını Whisper ile metne çevirme
whisper_transcribe("ornek.wav")
