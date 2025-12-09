# 🎵 MIDI Harmonizer Web App

An ML-powered web application that automatically generates harmonies and bass lines for MIDI melodies. Upload your melody, and let machine learning create beautiful multi-voice arrangements!

![MIDI Harmonizer](https://img.shields.io/badge/Status-In%20Development-yellow)
![Python](https://img.shields.io/badge/Python-3.9+-blue)
![React](https://img.shields.io/badge/React-18.2-blue)
![TensorFlow](https://img.shields.io/badge/TensorFlow-2.15-orange)

## ✨ Features

- **🎹 MIDI Upload**: Drag-and-drop or browse to upload your melody
- **🤖 ML-Powered Harmonization**: Intelligent harmony generation based on music theory and machine learning
- **🎼 Multi-Voice Generation**: Creates harmony parts and bass lines automatically
- **🎧 In-Browser Playback**: Listen to your original and harmonized versions (coming soon)
- **📥 Download**: Export your harmonized MIDI file

## 🛠️ Tech Stack

### Backend
- **Python 3.9+**
- **Flask** - REST API
- **TensorFlow/Keras** - Machine learning models
- **music21** - Music theory analysis
- **mido** - MIDI file manipulation
- **pretty-midi** - MIDI processing

### Frontend
- **React 18**
- **Tone.js** - Audio playback
- **Axios** - API communication
- **Modern CSS** - Responsive design

## 🚀 Getting Started

### Prerequisites

- Python 3.9 or higher
- Node.js 16+ and npm
- Git

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/chinmayjpatel/midi-harmonizer-web-app.git
cd midi-harmonizer-web-app
```

2. **Set up the backend**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. **Set up the frontend**
```bash
cd ../frontend
npm install
```

### Running the Application

1. **Start the backend server** (in `backend/` directory)
```bash
python app.py
```
The API will run on `http://localhost:5000`

2. **Start the frontend** (in `frontend/` directory)
```bash
npm start
```
The app will open at `http://localhost:3000`

## 📖 How It Works

1. **Upload**: User uploads a MIDI file containing a melody
2. **Analysis**: The system analyzes the melody to determine key, scale, and musical structure
3. **ML Processing**: Machine learning model predicts optimal harmony notes and bass progression
4. **Generation**: Creates new MIDI tracks with harmonies and bass
5. **Output**: Combines all parts into a single harmonized MIDI file

## 🎯 Roadmap

- [x] Basic MIDI upload and parsing
- [x] Rule-based harmonization
- [ ] LSTM model training on Bach chorales
- [ ] Advanced harmony patterns (jazz, classical styles)
- [ ] Real-time playback with Tone.js
- [ ] User preferences (harmony style, density)
- [ ] Batch processing
- [ ] Audio export (MP3/WAV)

## 🧠 Machine Learning Approach

The harmonizer uses a combination of:
- **Rule-based system**: Music theory rules for basic harmonization
- **LSTM Neural Network**: Trained on classical music datasets to predict contextual harmony
- **Attention mechanisms**: For capturing long-range musical dependencies (future enhancement)

### Training Data
- Bach Chorales
- Classical piano arrangements
- Jazz standards
- User-contributed MIDI files (future)

## 📁 Project Structure

```
midi-harmonizer-web-app/
├── backend/
│   ├── app.py              # Flask API
│   ├── harmonizer.py       # Core harmonization logic
│   ├── requirements.txt    # Python dependencies
│   ├── models/            # Trained ML models
│   ├── uploads/           # Uploaded MIDI files
│   └── outputs/           # Generated harmonized files
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── components/    # React components
│   │   ├── App.js        # Main application
│   │   └── App.css       # Styles
│   └── package.json      # Node dependencies
└── README.md
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the project
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👨‍💻 Author

**Trixx** (Chinmay Patel)
- GitHub: [@chinmayjpatel](https://github.com/chinmayjpatel)
- Passionate about bridging music and technology through code

## 🙏 Acknowledgments

- Music21 library for music theory analysis
- TensorFlow team for ML framework
- Tone.js for web audio capabilities
- The open-source community

## 📧 Contact

Have questions or suggestions? Open an issue or reach out!

---

⭐ If you find this project interesting, please consider giving it a star!
