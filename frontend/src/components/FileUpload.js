import React, { useRef, useState } from 'react';
import './FileUpload.css';

function FileUpload({ onFileUpload, disabled }) {
  const [dragActive, setDragActive] = useState(false);
  const [selectedFile, setSelectedFile] = useState(null);
  const inputRef = useRef(null);

  const handleDrag = (e) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === "dragenter" || e.type === "dragover") {
      setDragActive(true);
    } else if (e.type === "dragleave") {
      setDragActive(false);
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);

    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      handleFile(e.dataTransfer.files[0]);
    }
  };

  const handleChange = (e) => {
    e.preventDefault();
    if (e.target.files && e.target.files[0]) {
      handleFile(e.target.files[0]);
    }
  };

  const handleFile = (file) => {
    // Check if file is MIDI
    const validTypes = ['audio/midi', 'audio/x-midi', 'application/x-midi'];
    const validExtensions = ['.mid', '.midi'];
    const fileExtension = file.name.toLowerCase().slice(file.name.lastIndexOf('.'));

    if (!validTypes.includes(file.type) && !validExtensions.includes(fileExtension)) {
      alert('Please upload a valid MIDI file (.mid or .midi)');
      return;
    }

    setSelectedFile(file);
    onFileUpload(file);
  };

  const onButtonClick = () => {
    inputRef.current.click();
  };

  return (
    <div className="file-upload-container">
      <form 
        className={`upload-form ${dragActive ? 'drag-active' : ''}`}
        onDragEnter={handleDrag}
        onDragLeave={handleDrag}
        onDragOver={handleDrag}
        onDrop={handleDrop}
        onSubmit={(e) => e.preventDefault()}
      >
        <input
          ref={inputRef}
          type="file"
          className="file-input"
          accept=".mid,.midi"
          onChange={handleChange}
          disabled={disabled}
        />
        
        <div className="upload-content">
          <div className="upload-icon">🎹</div>
          <p className="upload-text">
            {selectedFile ? (
              <>Selected: <strong>{selectedFile.name}</strong></>
            ) : (
              <>Drag and drop your MIDI file here</>
            )}
          </p>
          <p className="upload-subtext">or</p>
          <button
            type="button"
            className="browse-btn"
            onClick={onButtonClick}
            disabled={disabled}
          >
            Browse Files
          </button>
          <p className="file-types">Accepted formats: .mid, .midi</p>
        </div>
      </form>
    </div>
  );
}

export default FileUpload;
