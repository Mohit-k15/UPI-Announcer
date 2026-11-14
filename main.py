import os
import sqlite3
from datetime import datetime

from kivy.app import App
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.utils import platform

KV = """
BoxLayout:
    orientation: "vertical"
    padding: "18dp"
    spacing: "12dp"

    Label:
        text: "UPI PAYMENT ANNOUNCER"
        bold: True
        font_size: "22sp"
        size_hint_y: None
        height: "54dp"

    Label:
        id: status
        text: "Ready — demo mode"
        font_size: "16sp"
        size_hint_y: None
        height: "36dp"

    Label:
        id: last_payment
        text: "Last payment: —"
        font_size: "23sp"
        bold: True

    Spinner:
        id: language
        text: "Hindi"
        values: ["Hindi", "English"]
        size_hint_y: None
        height: "48dp"

    Button:
        text: "TEST ANNOUNCEMENT"
        size_hint_y: None
        height: "52dp"
        on_release: app.test_voice()

    Button:
        text: "ADD DEMO PAYMENT ₹100"
        size_hint_y: None
        height: "52dp"
        on_release: app.add_demo_payment()

    Button:
        text: "VIEW PAYMENT HISTORY"
        size_hint_y: None
        height: "48dp"
        on_release: app.show_history()

    Label:
        id: history
        text: "No demo payments yet."
        halign: "left"
        valign: "top"
        text_size: self.width, None
"""

class UPIAnnouncerApp(App):
    def build(self):
        self.root = Builder.load_string(KV)
        self.tts = None
        self.tts_ready = False
        self.db = sqlite3.connect(
            os.path.join(self.user_data_dir, "payments.db")
        )
        self.db.execute("""
            CREATE TABLE IF NOT EXISTS payments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                amount TEXT NOT NULL,
                source TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
        """)
        self.db.commit()

        if platform == "android":
            self._init_android_tts()
            self.root.ids.status.text = "Ready — voice test available"
        else:
            self.root.ids.status.text = "Preview mode — install APK for Android voice"

        return self.root

    def _init_android_tts(self):
        try:
            from jnius import autoclass
            PythonActivity = autoclass("org.kivy.android.PythonActivity")
            TextToSpeech = autoclass("android.speech.tts.TextToSpeech")
            self.Locale = autoclass("java.util.Locale")
            self.tts = TextToSpeech(PythonActivity.mActivity, None)
            self.TextToSpeech = TextToSpeech
            self.tts_ready = True
        except Exception as exc:
            self.root.ids.status.text = "Voice setup error: " + str(exc)

    def speak(self, amount=None):
        language = self.root.ids.language.text
        if amount is None:
            message = ("भुगतान घोषणा परीक्षण। धन्यवाद।"
                       if language == "Hindi"
                       else "Payment announcement test. Thank you.")
        elif language == "Hindi":
            message = f"{amount} रुपये का भुगतान नोटिफिकेशन मिला है। कृपया भुगतान की पुष्टि करें।"
        else:
            message = f"A payment notification for {amount} rupees was received. Please verify the payment."

        if platform == "android" and self.tts_ready:
            try:
                locale = self.Locale("hi", "IN") if language == "Hindi" else self.Locale("en", "IN")
                self.tts.setLanguage(locale)
                self.tts.speak(message, self.TextToSpeech.QUEUE_FLUSH, None, "upi_announcement")
                return
            except Exception as exc:
                self.root.ids.status.text = "Speech error: " + str(exc)

        self.root.ids.status.text = "Voice is available in the Android APK"

    def test_voice(self):
        self.speak()

    def add_demo_payment(self):
        amount = "100"
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.db.execute(
            "INSERT INTO payments(amount, source, created_at) VALUES (?, ?, ?)",
            (amount, "DEMO ONLY", now)
        )
        self.db.commit()
        self.root.ids.last_payment.text = "Demo payment: ₹100"
        self.root.ids.status.text = "Demo record added — NOT a real payment"
        self.speak(amount)
        self.show_history()

    def show_history(self):
        rows = self.db.execute(
            "SELECT amount, source, created_at FROM payments ORDER BY id DESC LIMIT 8"
        ).fetchall()
        if not rows:
            self.root.ids.history.text = "No payments recorded."
            return
        lines = ["Recent records (demo only):"]
        for amount, source, created_at in rows:
            lines.append(f"₹{amount} | {source} | {created_at}")
        self.root.ids.history.text = "\n".join(lines)

    def on_stop(self):
        try:
            if self.tts:
                self.tts.stop()
                self.tts.shutdown()
        except Exception:
            pass
        self.db.close()

if __name__ == "__main__":
    UPIAnnouncerApp().run()
