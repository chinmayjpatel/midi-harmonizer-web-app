import React, { useState, useEffect } from 'react';
import * as Tone from 'tone';
import './MIDIPlayer.css';

function MIDIPlayer({ filename }) {
  const [isPlaying, setIsPlaying] = useState(false);
  const [currentTime, setCurrentTime] = useState(0);
  const [duration, setDuration] = useState(0);

  useEffect(() => {
    // Initialize Tone.js synth
    const synth = new Tone.PolySynth(Tone.Synth).toDestination();
    
    return () => {
      synth.dispose();
    };
  }, []);

  const handlePlay = async () => {
    if (!isPlaying) {
      await Tone.start();
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
    Tone.Transport.pause();
  };

  const handleStop = () => {
    setIsPlaying(false);
    setCurrentTime(0);
    Tone.Transport.stop();
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
