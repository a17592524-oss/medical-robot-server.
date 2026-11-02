from flask import Flask, request
import openai
import os

app = Flask(__name__)

# هنقرأ المفتاح من إعدادات Render عشان الأمان
openai.api_key = os.environ.get("OPENAI_API_KEY")

@app.route('/voice', methods=['POST'])
def voice():
    audio_data = request.data
    with open("/tmp/temp_audio.wav", "wb") as f:
        f.write(audio_data)
    
    with open("/tmp/temp_audio.wav", "rb") as audio_file:
        transcript = openai.Audio.transcribe("whisper-1", audio_file, language="ar")
    
    text = transcript['text']
    
    if "قدام" in text or "أمام" in text: return "FORWARD"
    if "ورا" in text or "خلف" in text: return "BACKWARD"
    if "شمال" in text or "يسار" in text: return "LEFT"
    if "يمين" in text: return "RIGHT"
    
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": text}]
        )
        return "AI_REPLY:" + response.choices[0].message.content
    except:
        return "AI_REPLY:عذراً، حدث خطأ."

# السطر ده مطلوب عشان Render يعرف يشغل السيرفر
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
