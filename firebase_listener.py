import firebase_admin
from firebase_admin import credentials, db
import threading
import time

class FirebaseListener:
    def __init__(self, key_path, db_url, on_data_callback):
        """
        key_path: path to firebase-key.json
        db_url: your Realtime Database URL
        on_data_callback: function to call when new data arrives (call, sms, notification)
        """
        self.callback = on_data_callback
        self.listening = False
        
        # Initialize Firebase
        cred = credentials.Certificate(key_path)
        firebase_admin.initialize_app(cred, {'databaseURL': db_url})
        self.ref = db.reference('/')
        
    def start_listening(self):
        """Starts a background thread that listens for new data"""
        self.listening = True
        thread = threading.Thread(target=self._listen, daemon=True)
        thread.start()
    
    def _listen(self):
        # We'll use a simple polling mechanism (lightweight, free)
        # For production, you can use stream() but polling is easier for this project
        last_check = {}
        while self.listening:
            try:
                data = self.ref.get()
                if data:
                    # Check for new calls
                    if 'calls' in data:
                        for call_id, call in data['calls'].items():
                            if call_id not in last_check.get('calls', {}):
                                self.callback('call', call)
                                last_check.setdefault('calls', {})[call_id] = True
                    # Check for SMS
                    if 'sms' in data:
                        for sms_id, sms in data['sms'].items():
                            if sms_id not in last_check.get('sms', {}):
                                self.callback('sms', sms)
                                last_check.setdefault('sms', {})[sms_id] = True
                    # Check for notifications
                    if 'notifications' in data:
                        for notif_id, notif in data['notifications'].items():
                            if notif_id not in last_check.get('notifications', {}):
                                self.callback('notification', notif)
                                last_check.setdefault('notifications', {})[notif_id] = True
            except Exception as e:
                print(f"Firebase polling error: {e}")
            time.sleep(2)  # Check every 2 seconds (free tier allows many requests)
    
    def stop_listening(self):
        self.listening = False