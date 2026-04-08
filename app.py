import customtkinter as ctk
from datetime import datetime
from firebase_listener import FirebaseListener
import threading
import os

# --- UI Settings ---
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class OmniSyncApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("OmniSync Pro - Open Source Bridge")
        self.geometry("950x650")
        self.minsize(800, 500)
        
        # Set window icon
        try:
            if os.path.exists("assets/omnisync.ico"):
                self.iconbitmap("assets/omnisync.ico")
        except:
            pass  # Icon not found, continue without it
        
        # --- Data storage (to keep history) ---
        self.call_history = []   # list of dicts
        self.message_history = [] # sms + notifications
        
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        
        # --- Sidebar ---
        self.sidebar = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.grid_rowconfigure(5, weight=1)
        
        self.logo = ctk.CTkLabel(self.sidebar, text="OmniSync OSOS", font=ctk.CTkFont(size=22, weight="bold"))
        self.logo.grid(row=0, column=0, padx=20, pady=(20,30))
        
        self.btn_live = ctk.CTkButton(self.sidebar, text="Live Dashboard", command=lambda: self.show_frame("live"))
        self.btn_live.grid(row=1, column=0, padx=20, pady=10)
        
        self.btn_calls = ctk.CTkButton(self.sidebar, text="Call History", command=lambda: self.show_frame("calls"))
        self.btn_calls.grid(row=2, column=0, padx=20, pady=10)
        
        self.btn_sms = ctk.CTkButton(self.sidebar, text="Messages & Alerts", command=lambda: self.show_frame("sms"))
        self.btn_sms.grid(row=3, column=0, padx=20, pady=10)
        
        self.status_label = ctk.CTkLabel(self.sidebar, text="🔴 Waiting for Firebase...", text_color="#E74C3C", font=ctk.CTkFont(weight="bold"))
        self.status_label.grid(row=6, column=0, padx=20, pady=20, sticky="s")
        
        # --- Frames (same as before) ---
        self.frames = {}
        self.frames["live"] = ctk.CTkScrollableFrame(self, corner_radius=0, fg_color="transparent")
        ctk.CTkLabel(self.frames["live"], text="Live Activity Feed", font=ctk.CTkFont(size=20, weight="bold")).pack(anchor="w", padx=20, pady=20)
        
        self.frames["calls"] = ctk.CTkScrollableFrame(self, corner_radius=0, fg_color="transparent")
        ctk.CTkLabel(self.frames["calls"], text="Call Logs", font=ctk.CTkFont(size=20, weight="bold")).pack(anchor="w", padx=20, pady=20)
        
        self.frames["sms"] = ctk.CTkScrollableFrame(self, corner_radius=0, fg_color="transparent")
        ctk.CTkLabel(self.frames["sms"], text="Messages & Notifications", font=ctk.CTkFont(size=20, weight="bold")).pack(anchor="w", padx=20, pady=20)
        
        self.show_frame("live")
        
        # --- Start Firebase listener (if key exists) ---
        self.start_firebase_listener()
        
        # Optional: load mock data for testing without Firebase
        # self.load_mock_data()
    
    def start_firebase_listener(self):
        try:
            key_path = "firebase-key.json"
            if not os.path.exists(key_path):
                key_path = "firebase-key.json.json"

            if not os.path.exists(key_path):
                raise FileNotFoundError(
                    "Firebase service account key not found. "
                    "Rename firebase-key.json.json to firebase-key.json or update app.py to the correct file name."
                )

            listener = FirebaseListener(
                key_path=key_path,
                db_url="https://omnisync-78f1e-default-rtdb.firebaseio.com/",  # REPLACE with your URL if needed
                on_data_callback=self.on_new_data
            )
            listener.start_listening()
            self.status_label.configure(text="🟢 Phone Online (Firebase)", text_color="#2ECC71")
        except Exception as e:
            print(f"Firebase init error: {e}")
            self.status_label.configure(text="⚠️ Firebase not configured", text_color="#F1C40F")
    
    def on_new_data(self, data_type, data):
        """Called when Firebase receives new data from phone"""
        timestamp = data.get('timestamp', datetime.now().strftime("%H:%M"))
        if data_type == 'call':
            number = data.get('number', 'Unknown')
            call_type = data.get('type', 'incoming')  # incoming, outgoing, missed
            title = f"{call_type.capitalize()} Call"
            message = number
            category = f"call_{call_type}"
            # Save to call history
            self.call_history.append(data)
            # Add to live feed and call history frame
            self.add_card("live", title, message, category, timestamp)
            self.add_card("calls", title, message, category, timestamp)
        
        elif data_type == 'sms':
            sender = data.get('sender', 'Unknown')
            msg = data.get('message', '')
            title = f"SMS from {sender}"
            self.message_history.append(data)
            self.add_card("live", title, msg, "sms", timestamp)
            self.add_card("sms", title, msg, "sms", timestamp)
        
        elif data_type == 'notification':
            app = data.get('app_name', 'App')
            title_text = data.get('title', '')
            content = data.get('content', '')
            title = f"{app} - {title_text}"
            self.message_history.append(data)
            self.add_card("live", title, content, "whatsapp", timestamp)
            self.add_card("sms", title, content, "whatsapp", timestamp)
    
    def add_card(self, target_frame, title, message, category, timestamp):
        """Adds a card to the specified frame"""
        color_map = {
            "call_missed": "#4A1515",
            "call_incoming": "#1A3A1A",
            "call_outgoing": "#2C3E50",
            "whatsapp": "#153A2D",
            "sms": "#2B2B2B"
        }
        card_color = color_map.get(category, "#2B2B2B")
        
        card = ctk.CTkFrame(self.frames[target_frame], fg_color=card_color, corner_radius=8)
        card.pack(fill="x", padx=20, pady=5)
        
        lbl_title = ctk.CTkLabel(card, text=title, font=ctk.CTkFont(weight="bold", size=14), width=180, anchor="w")
        lbl_title.pack(side="left", padx=15, pady=15)
        
        lbl_msg = ctk.CTkLabel(card, text=message, anchor="w", wraplength=400)
        lbl_msg.pack(side="left", fill="x", expand=True, padx=10, pady=15)
        
        lbl_time = ctk.CTkLabel(card, text=timestamp, text_color="gray", width=80)
        lbl_time.pack(side="right", padx=15, pady=15)
    
    def show_frame(self, frame_name):
        for frame in self.frames.values():
            frame.grid_forget()
        self.frames[frame_name].grid(row=0, column=1, sticky="nsew")
    
    def load_mock_data(self):
        """For testing without Firebase"""
        now = datetime.now().strftime("%H:%M")
        self.add_card("live", "Incoming Call", "+254712345678", "call_incoming", now)
        self.add_card("live", "WhatsApp - John", "Hey, are we meeting?", "whatsapp", now)
        self.add_card("calls", "Missed Call", "+254799888777", "call_missed", "10:30 AM")
        self.add_card("calls", "Outgoing Call", "Mom", "call_outgoing", "09:15 AM")
        self.add_card("sms", "Safaricom", "Your bundle renewed.", "sms", "Yesterday")
        self.status_label.configure(text="🟡 Mock Mode (No Firebase)", text_color="#F1C40F")

if __name__ == "__main__":
    app = OmniSyncApp()
    app.mainloop()