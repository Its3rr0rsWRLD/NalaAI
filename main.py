import os
import tempfile
from flask import Flask, request, jsonify
import whisper

model = whisper.load_model("base")

app = Flask(__name__)

@app.route('/transcribe', methods=['POST'])
def transcribe():
    if 'audio' not in request.files:
        return jsonify({'error': 'No audio file provided'}), 400

    audio_file = request.files['audio']
    temp = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
    try:
        audio_file.save(temp.name)
        temp.close()

        result = model.transcribe(temp.name)
        transcription = result.get('text', 'Transcription not available')
        return jsonify({'transcription': transcription})
        
    except Exception as e:
        return jsonify({'error': f'Error during transcription: {str(e)}'}), 500
    finally:
        os.unlink(temp.name)

if __name__ == '__main__':
    app.run(port=5000)
