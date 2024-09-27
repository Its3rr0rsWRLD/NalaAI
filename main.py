import os
from flask import Flask, request, jsonify
import whisper
import tempfile

app = Flask(__name__)

model = whisper.load_model("base")

@app.route('/transcribe', methods=['POST'])
def transcribe():
    if 'audio' not in request.files:
        return jsonify({'error': 'No audio file provided'}), 400

    audio_file = request.files['audio']
    with tempfile.NamedTemporaryFile(delete=False) as temp:
        audio_file.save(temp.name)
        result = model.transcribe(temp.name)
        transcription = result['text']
    os.unlink(temp.name)
    return jsonify({'transcription': transcription})

if __name__ == '__main__':
    app.run(port=5000)