import tkinter as tk
import threading
import wave
import pyaudio
from vosk import Model, KaldiRecognizer

class VoiceAnalyzerApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Voice Analyzer")

        # Modelin yolu
        self.model = Model("C:/Users/gumel/Desktop/vosk-model-small-tr-0.3")
        self.rec = KaldiRecognizer(self.model, 16000)

        self.text_frame = tk.Frame(master)
        self.text_frame.pack(pady=10)

        self.text_output = tk.Text(self.text_frame, height=10, width=50)
        self.text_output.pack(side=tk.LEFT)

        self.category_output = tk.Text(self.text_frame, height=10, width=20)
        self.category_output.pack(side=tk.RIGHT)

        # Başlatma ve durdurma
        self.start_button = tk.Button(master, text="Analizi Başlat", command=self.start_analysis)
        self.start_button.pack(pady=5)

        self.stop_button = tk.Button(master, text="Durdur", command=self.stop_analysis)
        self.stop_button.pack(pady=5)

        self.running = False  
        self.thread = None

    def start_analysis(self):
        self.running = True
        self.text_output.delete(1.0, tk.END)
        self.category_output.delete(1.0, tk.END)
        self.thread = threading.Thread(target=self.analyze_voice)
        self.thread.start()

    def stop_analysis(self):
        self.running = False
        if self.thread is not None:
            self.thread.join()  

    def analyze_voice(self):
        # Mikrofonu ayarlayın
        p = pyaudio.PyAudio()
        stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8000)
        stream.start_stream()

        print("Dinliyorum...")
        while self.running:
            data = stream.read(4000)
            if self.rec.AcceptWaveform(data):
                result = self.rec.Result()
                result_text = result.split('"')[3] if '"' in result else ""
                if result_text:
                    self.text_output.insert(tk.END, f"Sesi Yakaladım: {result_text}\n")
                    category, cleaned_question = self.analyze_question(result_text)
                    self.category_output.insert(tk.END, f"Kategori: {category}\n")
            else:
                print(self.rec.PartialResult())

        # Temizleme
        stream.stop_stream()
        stream.close()
        p.terminate()

    def analyze_question(self, question):
        personal_keywords = ["isim", "yaş", "hobi"]
        work_keywords = ["proje", "iş", "görev"]
        cleaned_question = question.strip().lower()

        # Kategorileri belirle
        if any(keyword in cleaned_question for keyword in personal_keywords):
            category = "personal"
        elif any(keyword in cleaned_question for keyword in work_keywords):
            category = "work"
        
        else:
            category = "other"

        return category, cleaned_question

if __name__ == "__main__":
    root = tk.Tk()
    app = VoiceAnalyzerApp(root)
    root.mainloop()
