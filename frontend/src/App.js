import React, { useState } from 'react';
import './App.css';
import FileUpload from './components/FileUpload';
import MIDIPlayer from './components/MIDIPlayer';
import axios from 'axios';

const API_URL = 'http://localhost:5000/api';

function App() {
  const [uploadedFile, setUploadedFile] = useState(null);
  const [harmonizedFile, setHarmonizedFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleFileUpload = async (file) => {
    setError(null);
    setLoading(true);

    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await axios.post(`${API_URL}/upload`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      setUploadedFile(response.data);
      setLoading(false);
    } catch (err) {
      setError('Failed to upload file. Please try again.');
      setLoading(false);
      console.error(err);
    }
  };

  const handleHarmonize = async () => {
    if (!uploadedFile) return;

    setError(null);
    setLoading(true);

    try {
      const response = await axios.post(`${API_URL}/harmonize`, {
        filename: uploadedFile.filename,
      });

      setHarmonizedFile(response.data);
      setLoading(false);
    } catch (err) {
      setError('Failed to harmonize file. Please try again.');
      setLoading(false);
      console.error(err);
    }
  };

  const handleDownload = () => {
    if (harmonizedFile) {
      window.open(`http://localhost:5000${harmonizedFile.download_url}`, '_blank');
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>🎵 MIDI Harmonizer</h1>
        <p className="subtitle">Upload your melody, get beautiful harmonies powered by ML</p>
      </header>

      <main className="App-main">
        <div className="container">
          {error && (
            <div className="error-message">
              {error}
            </div>
          )}

          <div className="upload-section">
            <FileUpload onFileUpload={handleFileUpload} disabled={loading} />
          </div>

          {uploadedFile && (
            <div className="actions-section">
              <div className="file-info">
                <p>✅ File uploaded: <strong>{uploadedFile.filename}</strong></p>
              </div>
              
              <button 
                className="harmonize-btn"
                onClick={handleHarmonize}
                disabled={loading}
              >
                {loading ? 'Harmonizing...' : '✨ Generate Harmonies'}
              </button>
            </div>
          )}

          {harmonizedFile && (
            <div className="results-section">
              <h2>🎉 Harmonization Complete!</h2>
              
              <div className="player-section">
                <h3>Original Melody</h3>
                <MIDIPlayer filename={uploadedFile.filename} />
              </div>

              <div className="player-section">
                <h3>Harmonized Version</h3>
                <MIDIPlayer filename={harmonizedFile.output_filename} />
              </div>

              <button 
                className="download-btn"
                onClick={handleDownload}
              >
                📥 Download Harmonized MIDI
              </button>
            </div>
          )}

          {loading && (
            <div className="loading-spinner">
              <div className="spinner"></div>
              <p>Processing your music...</p>
            </div>
          )}
        </div>
      </main>

      <footer className="App-footer">
        <p>Built with ❤️ by Trixx | Powered by Machine Learning</p>
      </footer>
    </div>
  );
}

export default App;
