from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import os
from werkzeug.utils import secure_filename
from harmonizer import MIDIHarmonizer

app = Flask(__name__)
CORS(app)

# Configuration
UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'outputs'
ALLOWED_EXTENSIONS = {'mid', 'midi'}

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Initialize harmonizer
harmonizer = MIDIHarmonizer()

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy', 'message': 'MIDI Harmonizer API is running'})

@app.route('/api/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        return jsonify({
            'message': 'File uploaded successfully',
            'filename': filename,
            'filepath': filepath
        }), 200
    
    return jsonify({'error': 'Invalid file type. Please upload a MIDI file'}), 400

@app.route('/api/harmonize', methods=['POST'])
def harmonize():
    data = request.get_json()
    
    if not data or 'filename' not in data:
        return jsonify({'error': 'No filename provided'}), 400
    
    filename = secure_filename(data['filename'])
    input_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    
    if not os.path.exists(input_path):
        return jsonify({'error': 'File not found'}), 404
    
    try:
        # Generate harmonized MIDI
        output_filename = f"harmonized_{filename}"
        output_path = os.path.join(app.config['OUTPUT_FOLDER'], output_filename)
        
        harmonizer.harmonize(input_path, output_path)
        
        return jsonify({
            'message': 'Harmonization successful',
            'output_filename': output_filename,
            'download_url': f'/api/download/{output_filename}'
        }), 200
    
    except Exception as e:
        return jsonify({'error': f'Harmonization failed: {str(e)}'}), 500

@app.route('/api/download/<filename>', methods=['GET'])
def download_file(filename):
    try:
        filepath = os.path.join(app.config['OUTPUT_FOLDER'], secure_filename(filename))
        return send_file(filepath, as_attachment=True)
    except Exception as e:
        return jsonify({'error': f'Download failed: {str(e)}'}), 404

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
