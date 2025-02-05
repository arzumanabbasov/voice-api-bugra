import os
import numpy as np
from flask import Flask, request, jsonify
from pathlib import Path
import librosa
import soundfile as sf
import whisper
from datetime import timedelta
from werkzeug.utils import secure_filename
from pydub import AudioSegment
from io import BytesIO
import torch

app = Flask(__name__)

print("Loading Whisper model...")
model = whisper.load_model("tiny")
print("Whisper model loaded.")

UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'splitted_voices'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

device = 'cuda' if torch.cuda.is_available() else 'cpu'
print(f"Using device: {device}")

if device != 'cuda':
    print("Warning: GPU is not available. The application will run on the CPU, which may result in slower performance.")

def seconds_to_time_format(seconds):
    return str(timedelta(seconds=seconds))

def split_and_transcribe_audio(file_path, target_duration=15):
    print(f"Processing file: {file_path}")
    audio, sr = librosa.load(file_path, sr=16000)
    total_duration = librosa.get_duration(y=audio, sr=sr)
    print(f"Total duration of the audio: {total_duration:.2f} seconds")

    print("Transcribing audio using Whisper...")
    result = model.transcribe(file_path, language="en", word_timestamps=True)
    print(f"Transcription completed with {len(result['segments'])} segments.")

    segments = []
    current_segment = []
    current_duration = 0
    segment_count = 0

    original_title = Path(file_path).stem

    for segment in result["segments"]:
        start = segment["start"]
        end = segment["end"]
        duration = end - start
        print(f"Processing segment {segment_count + 1}: Start = {start:.2f}, End = {end:.2f}, Duration = {duration:.2f} seconds")

        if current_duration + duration > target_duration and current_segment:
            segment_count += 1
            output_filename = f"{original_title}_part_{segment_count:03d}.wav"
            output_path = Path(OUTPUT_FOLDER) / output_filename

            start_sample = int(current_segment[0]["start"] * sr)
            end_sample = int(current_segment[-1]["end"] * sr)
            audio_segment = audio[start_sample:end_sample]
            sf.write(str(output_path), audio_segment, sr)
            print(f"Saved segment {segment_count} to {output_filename}")

            segment_text = " ".join([seg["text"] for seg in current_segment])
            segments.append({
                'part_file': output_filename,
                'whisper_text': segment_text.strip(),
                'start_time': seconds_to_time_format(current_segment[0]["start"]),
                'end_time': seconds_to_time_format(current_segment[-1]["end"]),
                'duration': current_segment[-1]["end"] - current_segment[0]["start"],
                'part_number': segment_count,
            })

            current_segment = [segment]
            current_duration = duration
        else:
            current_segment.append(segment)
            current_duration += duration

    if current_segment:
        segment_count += 1
        output_filename = f"{original_title}_part_{segment_count:03d}.wav"
        output_path = Path(OUTPUT_FOLDER) / output_filename

        start_sample = int(current_segment[0]["start"] * sr)
        end_sample = int(current_segment[-1]["end"] * sr)
        audio_segment = audio[start_sample:end_sample]
        sf.write(str(output_path), audio_segment, sr)
        print(f"Saved final segment {segment_count} to {output_filename}")

        segment_text = " ".join([seg["text"] for seg in current_segment])
        segments.append({
            'part_file': output_filename,
            'whisper_text': segment_text.strip(),
            'start_time': seconds_to_time_format(current_segment[0]["start"]),
            'end_time': seconds_to_time_format(current_segment[-1]["end"]),
            'duration': current_segment[-1]["end"] - current_segment[0]["start"],
            'part_number': segment_count,
        })

    print(f"Total segments created: {len(segments)}")
    return segments

@app.route('/upload', methods=['POST'])
def upload_audio():
    print("Received upload request...")
    if 'file' not in request.files:
        print("No file part in the request.")
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        print("No selected file.")
        return jsonify({'error': 'No selected file'}), 400

    filename = secure_filename(file.filename)
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    print(f"Saving file to: {file_path}")
    file.save(file_path)

    try:
        segments = split_and_transcribe_audio(file_path)
        print("Returning segments information.")
        return jsonify(segments)
    except Exception as e:
        print(f"Error processing the file: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == "__main__":
    print("Starting Flask app...")
    app.run(debug=True, host='0.0.0.0', port=5000)
