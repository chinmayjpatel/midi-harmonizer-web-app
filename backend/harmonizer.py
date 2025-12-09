import mido
import numpy as np
from music21 import converter, note, chord, stream, key
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
        Main harmonization function
        """
        # Load MIDI file
        midi_stream = converter.parse(input_path)
        
        # Analyze key
        detected_key = self.analyze_key(midi_stream)
        print(f"Detected key: {detected_key}")
        
        # Create new streams for harmony and bass
        harmony_stream = stream.Part()
        bass_stream = stream.Part()
        melody_stream = stream.Part()
        
        # Extract melody (assume first part or highest notes)
        parts = midi_stream.parts
        if len(parts) > 0:
            original_melody = parts[0]
        else:
            original_melody = midi_stream.flatten()
        
        # Process each note in the melody
        for element in original_melody.flatten().notesAndRests:
            if isinstance(element, note.Note):
                # Copy original melody note
                melody_note = note.Note(element.pitch)
                melody_note.duration = element.duration
                melody_note.offset = element.offset
                melody_stream.append(melody_note)
                
                # Generate harmony (third above)
                harmony_note = self.generate_harmony_note(element.pitch.nameWithOctave, detected_key, interval=3)
                if harmony_note:
                    harmony_note.duration = element.duration
                    harmony_note.offset = element.offset
                    harmony_stream.append(harmony_note)
                
                # Generate bass (simplified - one per measure)
                if element.offset % 4.0 == 0:  # On downbeats
                    bass_note = self.generate_bass_note([element], detected_key, element.offset)
                    bass_note.duration.quarterLength = 4.0  # Whole note
                    bass_note.offset = element.offset
                    bass_stream.append(bass_note)
            
            elif isinstance(element, note.Rest):
                # Copy rests to all parts
                rest = note.Rest()
                rest.duration = element.duration
                rest.offset = element.offset
                melody_stream.append(rest)
        
        # Combine all parts
        score = stream.Score()
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
