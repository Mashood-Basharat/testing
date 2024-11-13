from flask import Flask, render_template, request, jsonify, send_from_directory
import os
import requests
from werkzeug.utils import secure_filename

# Initialize Flask app
app = Flask(__name__)

# Configuration
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['PROCESSED_FOLDER'] = 'processed'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['PROCESSED_FOLDER'], exist_ok=True)

@app.route('/')
def index():
    return render_template('dashboard.html')

@app.route('/dashboard', methods=['POST'])
def dashboard():
    # Check if files are uploaded
    if 'audio' not in request.files or 'video' not in request.files:
        return jsonify({'success': False, 'message': 'Missing audio or video file'}), 400

    # Save uploaded files
    audio_file = request.files['audio']
    video_file = request.files['video']
    audio_path = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(audio_file.filename))
    video_path = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(video_file.filename))
    audio_file.save(audio_path)
    video_file.save(video_path)

    # Send files to Colab
    colab_url = 'YOUR_COLAB_URL'  # Replace with your ngrok URL
    files = {'audio': open(audio_path, 'rb'), 'video': open(video_path, 'rb')}
    try:
        colab_response = requests.post(colab_url, files=files)
        colab_response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return jsonify({'success': False, 'message': 'Error processing files'}), 500
    finally:
        files['audio'].close()
        files['video'].close()

    # Save processed file from Colab
    if 'content-type' in colab_response.headers and 'application/octet-stream' in colab_response.headers['content-type']:
        processed_file_path = os.path.join(app.config['PROCESSED_FOLDER'], 'output.mp4')
        with open(processed_file_path, 'wb') as f:
            f.write(colab_response.content)
        file_url = f'/processed/output.mp4'
        return jsonify({'success': True, 'file_url': file_url}), 200
    else:
        return jsonify({'success': False, 'message': 'Error in response from Colab'}), 500

@app.route('/processed/<filename>')
def download_file(filename):
    return send_from_directory(app.config['PROCESSED_FOLDER'], filename)

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
