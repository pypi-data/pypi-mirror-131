def help():
    print("""주의사항
1.이어폰과 마이크가 모두 연결되어있어야함
2.끝

도움말
'AL.rai_ready()'=기본 설정
'AL.speak('[하고싶은말]')'=하고싶은말을 음성,텍스트로 출력해줌
""")

def rai_ready():
    from typing import Text
    import win32com.client
    import time
    import os
    import pyaudio
    import keyboard
    import clipboard
    import speech_recognition as sr
    import googletrans
    from gtts import gTTS
    import playsound
    voice_data = 0
    args = 0
    Text = 0
    Text2 = 0
    translator = googletrans.Translator()
    r = Recognizer()
    m = Microphone()

def speak(text):
    tts = gTTS(text=text, lang='en')
    filename='voice.mp3'
    tts.save(filename)
    playsound.playsound(filename)