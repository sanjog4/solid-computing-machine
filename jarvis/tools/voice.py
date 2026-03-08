from __future__ import annotations

try:
    import pyttsx3
    import speech_recognition as sr
except Exception:  # pragma: no cover - optional dependency
    pyttsx3 = None  # type: ignore
    sr = None  # type: ignore


class VoiceAssistant:
    def __init__(self) -> None:
        if sr is None or pyttsx3 is None:
            raise RuntimeError("Voice dependencies are missing. Install speechrecognition and pyttsx3.")
        self.recognizer = sr.Recognizer()
        self.tts_engine = pyttsx3.init()
        self.tts_engine.setProperty("rate", 175)

    def speak(self, text: str) -> None:
        self.tts_engine.say(text)
        self.tts_engine.runAndWait()

    def listen(self, timeout: int = 5, phrase_time_limit: int = 10) -> str:
        with sr.Microphone() as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=0.8)
            audio = self.recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
        return self.recognizer.recognize_google(audio)
