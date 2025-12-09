# 🏗️ MIDI Harmonizer Architecture

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                         User Browser                        │
│                     (React Frontend)                        │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │ FileUpload   │  │ MIDIPlayer   │  │  Download    │     │
│  │  Component   │  │  Component   │  │   Button     │     │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘     │
│         │                  │                  │             │
│         └──────────────────┴──────────────────┘             │
│                            │                                │
│                      Axios HTTP Requests                    │
└────────────────────────────┼────────────────────────────────┘
                             │
                    ─────────┼─────────
                   │    INTERNET     │
                    ─────────┼─────────
                             │
┌────────────────────────────┼────────────────────────────────┐
│                 Flask Backend (Python)                      │
│                   localhost:5000                            │
│  ┌──────────────────────────────────────────────────────┐  │
│  │                  REST API Endpoints                   │  │
│  │  ┌────────────┐  ┌────────────┐  ┌────────────┐     │  │
│  │  │ /upload    │  │ /harmonize │  │ /download  │     │  │
│  │  └─────┬──────┘  └─────┬──────┘  └─────┬──────┘     │  │
│  └────────┼───────────────┼───────────────┼────────────┘  │
│           │               │               │                │
│  ┌────────▼───────────────▼───────────────▼────────────┐  │
│  │           MIDIHarmonizer Class                       │  │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────┐  │  │
│  │  │ Key Analysis │  │   Harmony    │  │   Bass   │  │  │
│  │  │  (music21)   │  │  Generation  │  │ Generator│  │  │
│  │  └──────┬───────┘  └──────┬───────┘  └────┬─────┘  │  │
│  │         │                  │                │        │  │
│  │         └──────────────────┴────────────────┘        │  │
│  │                            │                          │  │
│  │                  ┌─────────▼─────────┐               │  │
│  │                  │  ML Model (LSTM)  │               │  │
│  │                  │   (TensorFlow)    │               │  │
│  │                  └───────────────────┘               │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                             │
│  ┌──────────────────────────────────────────────────────┐  │
│  │              File Storage                             │  │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐           │  │
│  │  │ uploads/ │  │ outputs/ │  │  models/ │           │  │
│  │  └──────────┘  └──────────┘  └──────────┘           │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

## Data Flow

```
1. USER UPLOADS MIDI
   ↓
2. FileUpload Component → POST /api/upload
   ↓
3. Flask saves file to uploads/
   ↓
4. User clicks "Harmonize" → POST /api/harmonize
   ↓
5. MIDIHarmonizer.harmonize() executes:
   │
   ├─→ Parse MIDI (mido)
   ├─→ Analyze key (music21)
   ├─→ Generate harmony notes (ML/Rules)
   ├─→ Generate bass line (Music Theory)
   └─→ Combine tracks and export
   ↓
6. Save harmonized MIDI to outputs/
   ↓
7. Return download URL to frontend
   ↓
8. User downloads harmonized MIDI
```

## Technology Stack

### Frontend Layer
```
React 18.2
├── Axios (HTTP client)
├── Tone.js (Audio playback)
└── Modern CSS (Styling)
```

### Backend Layer
```
Python 3.9+
├── Flask 3.0 (Web framework)
├── Flask-CORS (Cross-origin requests)
├── mido (MIDI parsing)
├── music21 (Music theory)
├── pretty-midi (MIDI processing)
└── TensorFlow 2.15 (ML models)
```

## API Endpoints

### GET /api/health
- **Purpose**: Health check
- **Returns**: `{"status": "healthy", "message": "..."}`

### POST /api/upload
- **Purpose**: Upload MIDI file
- **Input**: FormData with 'file' field
- **Returns**: `{"filename": "...", "filepath": "..."}`
- **Validation**: .mid or .midi extensions only

### POST /api/harmonize
- **Purpose**: Generate harmonized version
- **Input**: `{"filename": "original.mid"}`
- **Returns**: `{"output_filename": "harmonized_...", "download_url": "..."}`
- **Process**:
  1. Load MIDI from uploads/
  2. Analyze musical structure
  3. Generate harmony and bass
  4. Save to outputs/

### GET /api/download/{filename}
- **Purpose**: Download harmonized file
- **Returns**: MIDI file as attachment

## Harmonization Algorithm

### Current Implementation (Rule-Based)
```python
for each note in melody:
    1. Determine scale position
    2. Generate harmony note (interval: third)
    3. Adjust octave for voice leading
    4. Add to harmony track
    
for each measure (downbeat):
    1. Identify chord context
    2. Use root note for bass
    3. Set duration (whole note)
    4. Add to bass track
```

### Future ML Implementation
```python
Input: Melody sequence (MIDI notes)
       ↓
[Embedding Layer]
       ↓
[LSTM Layers] ← Context from previous notes
       ↓
[Dense Layer] → Predict harmony note probability
       ↓
Output: Harmony + Bass sequences
```

## File Structure

```
midi-harmonizer-web-app/
│
├── backend/
│   ├── app.py                 # Flask application & routes
│   ├── harmonizer.py          # Core harmonization logic
│   ├── requirements.txt       # Python dependencies
│   │
│   ├── uploads/              # Uploaded MIDI files (gitignored)
│   ├── outputs/              # Harmonized outputs (gitignored)
│   └── models/               # Trained ML models
│
├── frontend/
│   ├── public/
│   │   └── index.html        # HTML entry
│   │
│   ├── src/
│   │   ├── App.js            # Main app component
│   │   ├── App.css           # Main styles
│   │   ├── index.js          # React entry
│   │   ├── index.css         # Global styles
│   │   │
│   │   └── components/
│   │       ├── FileUpload.js      # Upload UI
│   │       ├── FileUpload.css
│   │       ├── MIDIPlayer.js      # Playback UI
│   │       └── MIDIPlayer.css
│   │
│   └── package.json          # Node dependencies
│
├── README.md                 # Main documentation
├── SETUP.md                  # Setup instructions
├── QUICK_REFERENCE.md        # Command reference
├── PROJECT_SUMMARY.md        # Project overview
├── ARCHITECTURE.md           # This file
└── .gitignore                # Git ignore rules
```

## Component Interaction

### FileUpload Component
```
State: [dragActive, selectedFile]
       ↓
User drags/drops or browses MIDI file
       ↓
Validates file type
       ↓
Calls onFileUpload(file) prop
       ↓
Parent (App) uploads to backend
```

### App Component
```
State: [uploadedFile, harmonizedFile, loading, error]
       ↓
Manages entire application flow
       ↓
Coordinates API calls
       ↓
Passes data to child components
```

### MIDIPlayer Component
```
Props: [filename]
       ↓
Initializes Tone.js synth
       ↓
Provides play/pause/stop controls
       ↓
[Future] Loads and plays MIDI via Tone.js
```

## Security Considerations

1. **File Upload Validation**
   - Extension checking (.mid, .midi)
   - MIME type validation
   - File size limits (16MB)

2. **Path Security**
   - `secure_filename()` for all uploads
   - Restricted to designated folders

3. **CORS Configuration**
   - Enabled only for development
   - Should restrict in production

4. **Error Handling**
   - Try-catch blocks in all routes
   - Sanitized error messages

## Performance Considerations

- Async file processing (future enhancement)
- Client-side file size validation
- Server-side timeout limits
- Efficient MIDI parsing with mido
- Lazy loading of ML models

## Deployment Architecture (Future)

```
Production:
  Frontend → Vercel/Netlify (Static hosting)
  Backend → Heroku/AWS/DigitalOcean (Python app)
  Models → Cloud storage (S3)
  Database → PostgreSQL (for user data)
```

## Extension Points

1. **Add New Harmony Styles**
   - Create style classes in harmonizer.py
   - Pass style parameter from frontend

2. **Train ML Model**
   - Collect MIDI dataset
   - Implement training loop
   - Save model to models/

3. **Add Audio Export**
   - Integrate synthesizer
   - Generate WAV/MP3 files

4. **Add User Accounts**
   - Add authentication (JWT)
   - Store user projects in database
   - Track usage analytics

---

This architecture is designed to be:
✅ Modular - Easy to replace components
✅ Scalable - Can handle increased load
✅ Maintainable - Clear separation of concerns
✅ Extensible - Easy to add new features
