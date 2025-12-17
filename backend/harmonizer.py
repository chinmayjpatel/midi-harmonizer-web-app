import mido
import numpy as np
from music21 import converter, note, chord, stream, key, instrument
import pretty_midi
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import os

class MIDIHarmonizer:
    def __init__(self, model_path=None):
        """
        Initialize the MIDI Harmonizer with optional pre-trained model
        """
        self.model = None
        self.note_to_int = {}
        self.int_to_note = {}
        
        if model_path and os.path.exists(model_path):
            self.load_model(model_path)
        else:
            # Will use rule-based harmonization until model is trained
            print("No model loaded. Using rule-based harmonization.")
    
    def analyze_key(self, midi_stream):
        """
        Analyze the key of the MIDI file using music21
        """
        analyzed_key = midi_stream.analyze('key')
        return analyzed_key
    
    def get_scale_notes(self, detected_key):
        """
        Get all notes in the scale of the detected key
        """
        scale = detected_key.getScale()
        return [p.name for p in scale.pitches]
    
    def generate_harmony_note(self, melody_note, detected_key, interval=3):
        """
        Generate a harmony note based on the melody note and key
        interval: 3 for third, 5 for fifth, etc.
        """
        scale_notes = self.get_scale_notes(detected_key)
        
        try:
            melody_pitch = note.Note(melody_note).pitch
            melody_name = melody_pitch.name
            
            # Find position in scale
            if melody_name in scale_notes:
                idx = scale_notes.index(melody_name)
                # Get harmony note (third above)
                harmony_idx = (idx + interval - 1) % len(scale_notes)
                harmony_name = scale_notes[harmony_idx]
                
                # Create harmony note with similar octave
                harmony_note = note.Note(harmony_name)
                harmony_note.octave = melody_pitch.octave
                
                # Adjust octave if needed to keep harmony close
                if harmony_note.pitch.midi < melody_pitch.midi:
                    harmony_note.octave += 1
                
                return harmony_note
        except:
            return None
        
        return None
    
    def generate_bass_note(self, melody_notes, detected_key, measure_start_time):
        """
        Generate bass note based on chord progression
        """
        # Simple approach: use root of the key or chord tones
        scale_notes = self.get_scale_notes(detected_key)
        
        # Get tonic (root) of the key
        tonic = detected_key.tonic.name
        
        # Create bass note (two octaves below middle C)
        bass = note.Note(tonic)
        bass.octave = 3
        
        return bass
    
    def harmonize(self, input_path, output_path):
        """
        Main harmonization function with improved timing and voice leading
        """
        # Load MIDI file
        midi_stream = converter.parse(input_path)
        
        # Analyze key
        detected_key = self.analyze_key(midi_stream)
        print(f"Detected key: {detected_key}")
        
        # Create new streams for harmony and bass
        harmony_stream = stream.Part()
        harmony_stream.insert(0, detected_key)
        
        bass_stream = stream.Part()
        bass_stream.insert(0, detected_key)
        
        melody_stream = stream.Part()
        melody_stream.insert(0, detected_key)
        
        # Extract melody (assume first part or highest notes)
        parts = midi_stream.parts
        if len(parts) > 0:
            original_melody = parts[0]
        else:
            original_melody = midi_stream.flatten()
        
        # Track previous harmony note for smooth voice leading
        prev_harmony_pitch = None
        last_bass_offset = -4.0  # Track when we last added bass
        
        # Process each note in the melody
        for element in original_melody.flatten().notesAndRests:
            if isinstance(element, note.Note):
                # Copy original melody note
                melody_note = note.Note(element.pitch)
                melody_note.duration = element.duration
                melody_note.offset = element.offset
                melody_stream.append(melody_note)
                
                # Generate harmony (third below for better sound)
                harmony_note = self.generate_harmony_note(
                    element.pitch.nameWithOctave, 
                    detected_key, 
                    interval=3
                )
                
                if harmony_note:
                    # Match duration exactly
                    harmony_note.duration = element.duration
                    harmony_note.offset = element.offset
                    
                    # Smooth voice leading - keep harmony notes close together
                    if prev_harmony_pitch:
                        # If new harmony is too far, adjust octave
                        interval_distance = abs(harmony_note.pitch.midi - prev_harmony_pitch.midi)
                        if interval_distance > 7:  # More than a fifth
                            if harmony_note.pitch.midi > prev_harmony_pitch.midi:
                                harmony_note.octave -= 1
                            else:
                                harmony_note.octave += 1
                    
                    harmony_stream.append(harmony_note)
                    prev_harmony_pitch = harmony_note.pitch
                
                # Generate bass on strong beats (every 2 quarter notes)
                current_beat = element.offset % 4.0
                if current_beat == 0 or (element.offset - last_bass_offset) >= 2.0:
                    bass_note = self.generate_bass_note([element], detected_key, element.offset)
                    
                    # Calculate duration until next bass note
                    duration_to_next = 2.0  # Default: half note
                    bass_note.duration.quarterLength = duration_to_next
                    bass_note.offset = element.offset
                    bass_stream.append(bass_note)
                    last_bass_offset = element.offset
            
            elif isinstance(element, note.Rest):
                # Copy rests to melody only
                rest = note.Rest()
                rest.duration = element.duration
                rest.offset = element.offset
                melody_stream.append(rest)
        
        # Combine all parts with proper MIDI channels
        score = stream.Score()
        
        # Set instruments for each part
        melody_stream.insert(0, instrument.Piano())
        harmony_stream.insert(0, instrument.Piano())
        bass_stream.insert(0, instrument.Piano())
        
        score.insert(0, melody_stream)
        score.insert(0, harmony_stream)
        score.insert(0, bass_stream)
        
        # Write output
        score.write('midi', fp=output_path)
        print(f"Harmonized MIDI saved to: {output_path}")
        
        return output_path
    
    def train_model(self, training_data_path):
        """
        Train the LSTM model on MIDI data (future enhancement)
        """
        # TODO: Implement LSTM training
        pass
    
    def load_model(self, model_path):
        """
        Load pre-trained model
        """
        try:
            self.model = keras.models.load_model(model_path)
            print(f"Model loaded from {model_path}")
        except Exception as e:
            print(f"Error loading model: {e}")
    
    def save_model(self, model_path):
        """
        Save trained model
        """
        if self.model:
            self.model.save(model_path)
            print(f"Model saved to {model_path}")
