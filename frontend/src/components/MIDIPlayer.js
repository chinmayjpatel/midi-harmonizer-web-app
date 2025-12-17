import React, { useState } from 'react';
import './MIDIPlayer.css';

function MIDIPlayer({ filename }) {
  const [isPlaying, setIsPlaying] = useState(false);
  const [currentTime, setCurrentTime] = useState(0);
  const [duration] = useState(0);

  const handlePlay = () => {
    if (!isPlaying) {
      setIsPlaying(true);
      
      // TODO: Load and play MIDI file using Tone.js
      // This is a placeholder - full MIDI parsing would be needed
      console.log(`Playing: ${filename}`);
      
      // Simulate playback
      setTimeout(() => {
        setIsPlaying(false);
      }, 5000);
    }
  };

  const handlePause = () => {
    setIsPlaying(false);
    // TODO: Implement pause functionality with Tone.js
  };

  const handleStop = () => {
    setIsPlaying(false);
    setCurrentTime(0);
    // TODO: Implement stop functionality with Tone.js
  };

  const formatTime = (seconds) => {
    const mins = Math.floor(seconds / 60);
    const secs = Math.floor(seconds % 60);
    return `${mins}:${secs.toString().padStart(2, '0')}`;
  };

  return (
    <div className="midi-player">
      <div className="player-controls">
        {!isPlaying ? (
          <button className="control-btn play-btn" onClick={handlePlay}>
            ▶️ Play
          </button>
        ) : (
          <button className="control-btn pause-btn" onClick={handlePause}>
            ⏸️ Pause
          </button>
        )}
        <button className="control-btn stop-btn" onClick={handleStop}>
          ⏹️ Stop
        </button>
      </div>

      <div className="player-info">
        <div className="time-display">
          <span>{formatTime(currentTime)}</span>
          <span> / </span>
          <span>{formatTime(duration)}</span>
        </div>
        <div className="progress-bar">
          <div 
            className="progress-fill" 
            style={{ width: duration > 0 ? `${(currentTime / duration) * 100}%` : '0%' }}
          ></div>
        </div>
      </div>

      <div className="player-note">
        <small>Note: Full MIDI playback coming soon! Download to hear the full harmonization.</small>
      </div>
    </div>
  );
}

export default MIDIPlayer;
