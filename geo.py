import io
import time
import base64
import requests
import mss
import customtkinter as ctk
from PIL import Image

API_KEY = "YOU_API_KEY_HERE"
MODEL = "gemini-3-flash-preview"
URL = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent?key={API_KEY}"

class GeoSolver(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("GeoGuessr Solver")
        self.geometry("500x450")
        ctk.set_appearance_mode("dark")
        
        self.btn = ctk.CTkButton(self, text="⚡SCAN", command=self.solve, height=70, font=("Impact", 24), fg_color="#d32f2f", hover_color="#b71c1c")
        self.btn.pack(pady=30, padx=20, fill="x")
        
        self.output = ctk.CTkTextbox(self, font=("Consolas", 18), text_color="#00ffcc", fg_color="#000000")
        self.output.pack(pady=10, padx=20, fill="both", expand=True)

    def solve(self):
        self.output.delete("0.0", "end")
        self.output.insert("end", ">> SCANNING...")
        self.update()
        time.sleep(1.5)
        
        with mss.mss() as sct:
            shot = sct.grab(sct.monitors[1])
            img = Image.frombytes("RGB", shot.size, shot.bgra, "raw", "BGRX")
            
            img.thumbnail((1280, 720)) 
            buf = io.BytesIO()
            img.save(buf, format="JPEG", quality=75)
            b64 = base64.b64encode(buf.getvalue()).decode()

        payload = {
            "contents": [{
                "parts": [
                    {"text": "Analyze Google Street View. Focus on: utility poles, road markings, architecture, and vegetation. Be extremely precise. No yapping. \n\nFormat:\nCountry: <name>\nState: <name>\nCity: <name>\nAnswer ONLY in English."},
                    {"inline_data": {"mime_type": "image/jpeg", "data": b64}}
                ]
            }],
            "generationConfig": {
                "temperature": 0.1,
                "topP": 0.8
            }
        }

        try:
            res = requests.post(URL, json=payload, timeout=15)
            data = res.json()
            txt = data["candidates"][0]["content"]["parts"][0]["text"]
            self.output.delete("0.0", "end")
            self.output.insert("end", txt.strip())
        except Exception as e:
            self.output.insert("end", f"Check connection or API Key.")

if __name__ == "__main__":
    GeoSolver().mainloop()


    # Obrigado por ver meu código XD @drakkiosauro_2
