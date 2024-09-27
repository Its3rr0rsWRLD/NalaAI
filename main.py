import os
import sys
import subprocess

# Ensure required packages are installed
def install_requirements():
    try:
        import flask
    except ImportError:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'flask'])
    
    try:
        import whisper
    except ImportError:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'whisper'])

install_requirements()

# After installation check, import the necessary libraries
from flask import Flask, request, jsonify
import whisper
import tempfile

# Load the Whisper model
model = whisper.load_model("base")

app = Flask(__name__)

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
