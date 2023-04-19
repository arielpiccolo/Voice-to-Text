import tkinter as tk
import threading
import speech_recognition as sr
import pyperclip

class VoiceToTextApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Voice to Text")
        self.geometry("400x300")
        self.resizable(False, False)
        self.text = ""
        self.recognizer = sr.Recognizer()
        self.caption_label = tk.Label(self, text="", font=("Helvetica", 18), wraplength=350)
        self.caption_label.pack(side=tk.TOP, pady=10)
        self.capture_button = tk.Button(self, text="Capture", font=("Helvetica", 14), command=self.record)
        self.capture_button.pack(side=tk.LEFT, padx=20, pady=10)
        self.copy_button = tk.Button(self, text="Copy", font=("Helvetica", 14), command=self.copy_to_clipboard)
        self.copy_button.pack(side=tk.LEFT, padx=20, pady=10)
        self.clear_button = tk.Button(self, text="Clear", font=("Helvetica", 14), command=self.clear_text)
        self.clear_button.pack(side=tk.LEFT, padx=20, pady=10)
        self._position_copyright()
        
    def record(self):
        def process_audio():
            with sr.Microphone() as source:
                self.recognizer.adjust_for_ambient_noise(source)
                audio = self.recognizer.listen(source)
                try:
                    text = self.recognizer.recognize_google(audio)
                    self.text += text + " "
                    self.caption_label.config(text=self.text)
                except sr.UnknownValueError:
                    print("Could not understand audio")
                except sr.RequestError as e:
                    print("Could not request results; {0}".format(e))
        
        self.capture_button.config(text="Recording...", state=tk.DISABLED)
        self.update()
        self.thread = threading.Thread(target=process_audio)
        self.thread.start()
        self.bind("<ButtonRelease-1>", self.stop_recording)
        
    def stop_recording(self, event):
        self.capture_button.config(text="Capture", state=tk.NORMAL)
        self.update()
        self.unbind("<ButtonRelease-1>")
    
    def copy_to_clipboard(self):
        pyperclip.copy(self.text)
        
    def clear_text(self):
        self.text = ""
        self.caption_label.config(text=self.text)
        
    def _position_copyright(self):
        copyright_label = tk.Label(self, text="© arielpiccolo", font=("Helvetica", 8))
        copyright_label.pack(
            side=tk.RIGHT, padx=5, pady=5, anchor=tk.SE)
    
if __name__ == "__main__":
    app = VoiceToTextApp()
    app.mainloop()

