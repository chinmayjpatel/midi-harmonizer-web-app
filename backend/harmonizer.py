"""
MIDI Harmonizer v2.0 - Enhanced Rule-Based System
==================================================
Phase 1 improvements:
- Markov chain chord progressions
- Proper voice leading (avoids parallel 5ths/octaves)
- Phrase boundary detection with cadences
- Chord-tone based harmony generation
- Smooth bass line movement

Author: Trixx (Chinmay Patel)
"""

import mido
import numpy as np
from music21 import converter, note, chord, stream, key, instrument, pitch, interval, roman
import pretty_midi
import os
import random
from collections import defaultdict

class ChordProgressionGenerator:
    """
    Markov chain-based chord progression generator using functional harmony.
    Probabilities based on common practice period music theory.
    """
    
    def __init__(self):
        # Transition probabilities: from_chord -> {to_chord: probability}
        # Based on functional harmony analysis of classical music
        self.major_transitions = {
            'I': {'I': 0.05, 'ii': 0.15, 'iii': 0.05, 'IV': 0.25, 'V': 0.30, 'vi': 0.15, 'viio': 0.05},
            'ii': {'I': 0.05, 'ii': 0.05, 'iii': 0.05, 'IV': 0.10, 'V': 0.60, 'vi': 0.05, 'viio': 0.10},
            'iii': {'I': 0.05, 'ii': 0.10, 'iii': 0.05, 'IV': 0.30, 'V': 0.10, 'vi': 0.35, 'viio': 0.05},
            'IV': {'I': 0.20, 'ii': 0.15, 'iii': 0.05, 'IV': 0.05, 'V': 0.40, 'vi': 0.05, 'viio': 0.10},
            'V': {'I': 0.55, 'ii': 0.05, 'iii': 0.05, 'IV': 0.10, 'V': 0.05, 'vi': 0.15, 'viio': 0.05},
            'vi': {'I': 0.10, 'ii': 0.25, 'iii': 0.10, 'IV': 0.30, 'V': 0.15, 'vi': 0.05, 'viio': 0.05},
            'viio': {'I': 0.70, 'ii': 0.05, 'iii': 0.05, 'IV': 0.05, 'V': 0.05, 'vi': 0.05, 'viio': 0.05},
        }
        
        self.minor_transitions = {
            'i': {'i': 0.05, 'iio': 0.10, 'III': 0.10, 'iv': 0.25, 'V': 0.30, 'VI': 0.15, 'viio': 0.05},
            'iio': {'i': 0.05, 'iio': 0.05, 'III': 0.05, 'iv': 0.10, 'V': 0.60, 'VI': 0.05, 'viio': 0.10},
            'III': {'i': 0.10, 'iio': 0.05, 'III': 0.05, 'iv': 0.30, 'V': 0.10, 'VI': 0.35, 'viio': 0.05},
            'iv': {'i': 0.20, 'iio': 0.10, 'III': 0.05, 'iv': 0.05, 'V': 0.45, 'VI': 0.05, 'viio': 0.10},
            'V': {'i': 0.55, 'iio': 0.05, 'III': 0.05, 'iv': 0.10, 'V': 0.05, 'VI': 0.15, 'viio': 0.05},
            'VI': {'i': 0.10, 'iio': 0.20, 'III': 0.10, 'iv': 0.30, 'V': 0.20, 'VI': 0.05, 'viio': 0.05},
            'viio': {'i': 0.70, 'iio': 0.05, 'III': 0.05, 'iv': 0.05, 'V': 0.05, 'VI': 0.05, 'viio': 0.05},
        }
    
    def get_next_chord(self, current_chord, mode='major'):
        """Select next chord based on Markov transition probabilities."""
        transitions = self.major_transitions if mode == 'major' else self.minor_transitions
        
        if current_chord not in transitions:
            current_chord = 'I' if mode == 'major' else 'i'
        
        probs = transitions[current_chord]
        chords = list(probs.keys())
        weights = list(probs.values())
        
        return random.choices(chords, weights=weights)[0]
    
    def get_cadence_chords(self, mode='major'):
        """Return authentic cadence: V -> I (or V -> i in minor)."""
        if mode == 'major':
            return ['V', 'I']
        else:
            return ['V', 'i']


class VoiceLeadingChecker:
    """
    Checks and enforces voice leading rules from classical music theory.
    """
    
    @staticmethod
    def get_interval_semitones(pitch1, pitch2):
        """Get interval in semitones between two pitches."""
        return abs(pitch1.midi - pitch2.midi) % 12
    
    @staticmethod
    def is_parallel_fifth(prev_voice1, prev_voice2, curr_voice1, curr_voice2):
        """Check for parallel perfect fifths (forbidden in classical harmony)."""
        if prev_voice1 is None or prev_voice2 is None:
            return False
        
        prev_interval = VoiceLeadingChecker.get_interval_semitones(prev_voice1, prev_voice2)
        curr_interval = VoiceLeadingChecker.get_interval_semitones(curr_voice1, curr_voice2)
        
        # Perfect fifth = 7 semitones
        if prev_interval == 7 and curr_interval == 7:
            # Check if both voices moved in the same direction
            voice1_direction = curr_voice1.midi - prev_voice1.midi
            voice2_direction = curr_voice2.midi - prev_voice2.midi
            if voice1_direction * voice2_direction > 0:  # Same direction
                return True
        return False
    
    @staticmethod
    def is_parallel_octave(prev_voice1, prev_voice2, curr_voice1, curr_voice2):
        """Check for parallel octaves (forbidden in classical harmony)."""
        if prev_voice1 is None or prev_voice2 is None:
            return False
        
        prev_interval = VoiceLeadingChecker.get_interval_semitones(prev_voice1, prev_voice2)
        curr_interval = VoiceLeadingChecker.get_interval_semitones(curr_voice1, curr_voice2)
        
        # Perfect octave/unison = 0 semitones
        if prev_interval == 0 and curr_interval == 0:
            voice1_direction = curr_voice1.midi - prev_voice1.midi
            voice2_direction = curr_voice2.midi - prev_voice2.midi
            if voice1_direction * voice2_direction > 0:
                return True
        return False
    
    @staticmethod
    def calculate_voice_leading_cost(prev_pitch, curr_pitch):
        """
        Calculate cost of voice movement. Lower is better.
        Stepwise motion (1-2 semitones) is preferred.
        """
        if prev_pitch is None:
            return 0
        
        movement = abs(curr_pitch.midi - prev_pitch.midi)
        
        if movement == 0:
            return 0.5  # Repeated note - okay but not ideal
        elif movement <= 2:
            return 0  # Stepwise - ideal
        elif movement <= 4:
            return 1  # Third - acceptable
        elif movement <= 7:
            return 2  # Fourth/Fifth - less ideal
        else:
            return 4  # Large leap - avoid if possible


class PhraseDetector:
    """
    Detects phrase boundaries in melodies for cadence placement.
    """
    
    @staticmethod
    def detect_boundaries(melody_notes):
        """
        Detect phrase boundaries based on musical cues:
        - Long notes (relative to context)
        - Notes before rests
        - Melodic peaks/valleys
        - Regular intervals (every 4 or 8 measures)
        """
        boundaries = []
        
        if len(melody_notes) < 4:
            return boundaries
        
        # Calculate average duration
        durations = [n.duration.quarterLength for n in melody_notes if hasattr(n, 'duration')]
        avg_duration = np.mean(durations) if durations else 1.0
        
        for i, element in enumerate(melody_notes):
            is_boundary = False
            
            # Check for long notes (1.5x average or longer)
            if hasattr(element, 'duration') and element.duration.quarterLength >= avg_duration * 1.5:
                is_boundary = True
            
            # Check if next element is a rest
            if i < len(melody_notes) - 1:
                next_elem = melody_notes[i + 1]
                if isinstance(next_elem, note.Rest):
                    is_boundary = True
            
            # Check for melodic peaks (higher than neighbors)
            if isinstance(element, note.Note) and i > 0 and i < len(melody_notes) - 1:
                prev_elem = melody_notes[i - 1]
                next_elem = melody_notes[i + 1]
                if isinstance(prev_elem, note.Note) and isinstance(next_elem, note.Note):
                    if element.pitch.midi > prev_elem.pitch.midi and element.pitch.midi > next_elem.pitch.midi:
                        is_boundary = True
            
            if is_boundary:
                boundaries.append(i)
        
        # Also add boundaries every ~8 beats if none detected nearby
        if hasattr(melody_notes[0], 'offset'):
            current_offset = 0
            for i, elem in enumerate(melody_notes):
                if hasattr(elem, 'offset'):
                    current_offset = elem.offset
                    # Every 8 quarter notes, check if we need a boundary
                    if current_offset > 0 and current_offset % 8.0 < 1.0:
                        # Check if there's already a boundary nearby
                        nearby = any(abs(b - i) <= 2 for b in boundaries)
                        if not nearby and i not in boundaries:
                            boundaries.append(i)
        
        return sorted(set(boundaries))


class MIDIHarmonizer:
    """
    Enhanced MIDI Harmonizer with:
    - Markov chain chord progressions
    - Voice leading rules
    - Phrase detection and cadences
    - Chord-tone based harmony
    """
    
    def __init__(self, model_path=None):
        """Initialize the MIDI Harmonizer."""
        self.model = None
        self.chord_generator = ChordProgressionGenerator()
        self.voice_checker = VoiceLeadingChecker()
        self.phrase_detector = PhraseDetector()
        
        # Chord definitions (scale degrees for each chord in major)
        # Scale degrees: 1=tonic, 2=supertonic, etc. (0-indexed: 0, 1, 2, 3, 4, 5, 6)
        self.major_chord_tones = {
            'I': [0, 2, 4],      # 1, 3, 5
            'ii': [1, 3, 5],     # 2, 4, 6
            'iii': [2, 4, 6],    # 3, 5, 7
            'IV': [3, 5, 0],     # 4, 6, 1
            'V': [4, 6, 1],      # 5, 7, 2
            'vi': [5, 0, 2],     # 6, 1, 3
            'viio': [6, 1, 3],   # 7, 2, 4
        }
        
        self.minor_chord_tones = {
            'i': [0, 2, 4],
            'iio': [1, 3, 5],
            'III': [2, 4, 6],
            'iv': [3, 5, 0],
            'V': [4, 6, 1],      # Raised 7th for dominant
            'VI': [5, 0, 2],
            'viio': [6, 1, 3],
        }
        
        if model_path and os.path.exists(model_path):
            self.load_model(model_path)
        else:
            print("Using enhanced rule-based harmonization (Phase 1).")
    
    def analyze_key(self, midi_stream):
        """Analyze the key of the MIDI file using music21."""
        analyzed_key = midi_stream.analyze('key')
        return analyzed_key
    
    def get_scale_pitches(self, detected_key):
        """Get all pitches in the scale."""
        scale = detected_key.getScale()
        return scale.pitches
    
    def get_chord_from_melody(self, melody_notes, detected_key, current_chord_numeral):
        """
        Determine which chord best fits the current melody notes.
        Returns chord tones as pitch objects.
        """
        scale_pitches = self.get_scale_pitches(detected_key)
        mode = 'major' if detected_key.mode == 'major' else 'minor'
        chord_tones_map = self.major_chord_tones if mode == 'major' else self.minor_chord_tones
        
        if current_chord_numeral not in chord_tones_map:
            current_chord_numeral = 'I' if mode == 'major' else 'i'
        
        scale_degree_indices = chord_tones_map[current_chord_numeral]
        chord_pitches = []
        
        for idx in scale_degree_indices:
            if idx < len(scale_pitches):
                chord_pitches.append(scale_pitches[idx])
        
        return chord_pitches
    
    def find_best_chord_for_melody(self, melody_pitch, detected_key, prev_chord):
        """
        Find the best chord that contains the melody note.
        Uses Markov chain probabilities weighted by whether chord contains melody.
        """
        mode = 'major' if detected_key.mode == 'major' else 'minor'
        chord_tones_map = self.major_chord_tones if mode == 'major' else self.minor_chord_tones
        transitions = self.chord_generator.major_transitions if mode == 'major' else self.chord_generator.minor_transitions
        
        scale_pitches = self.get_scale_pitches(detected_key)
        scale_names = [p.name for p in scale_pitches]
        
        # Find which scale degree the melody note is
        melody_name = melody_pitch.name
        melody_scale_degree = None
        for i, name in enumerate(scale_names):
            if name == melody_name:
                melody_scale_degree = i
                break
        
        if melody_scale_degree is None:
            # Non-diatonic note, keep current chord
            return prev_chord
        
        # Score each possible chord
        chord_scores = {}
        
        if prev_chord not in transitions:
            prev_chord = 'I' if mode == 'major' else 'i'
        
        for next_chord, transition_prob in transitions[prev_chord].items():
            chord_degrees = chord_tones_map.get(next_chord, [0, 2, 4])
            
            # Check if melody note is in this chord
            if melody_scale_degree in chord_degrees:
                # Melody fits chord - high score
                chord_scores[next_chord] = transition_prob * 2.0
            else:
                # Melody doesn't fit - lower score but still possible (passing tone)
                chord_scores[next_chord] = transition_prob * 0.3
        
        # Normalize and select
        total = sum(chord_scores.values())
        if total == 0:
            return prev_chord
        
        chords = list(chord_scores.keys())
        weights = [chord_scores[c] / total for c in chords]
        
        return random.choices(chords, weights=weights)[0]
    
    def generate_harmony_note(self, melody_pitch, chord_pitches, detected_key, prev_harmony_pitch):
        """
        Generate a harmony note from the current chord.
        Prefers notes that create good voice leading.
        """
        if not chord_pitches:
            return None
        
        # Target range: below melody, within an octave
        target_octave = melody_pitch.octave - 1
        
        candidates = []
        
        for chord_pitch in chord_pitches:
            # Create candidate at different octaves
            for oct_adjust in [-1, 0, 1]:
                candidate = note.Note(chord_pitch.name)
                candidate.octave = target_octave + oct_adjust
                
                # Skip if too close to or above melody
                if candidate.pitch.midi >= melody_pitch.midi - 2:
                    continue
                
                # Skip if too low
                if candidate.pitch.midi < 48:  # Below C3
                    continue
                
                # Calculate voice leading cost
                vl_cost = self.voice_checker.calculate_voice_leading_cost(
                    prev_harmony_pitch, candidate.pitch
                )
                
                # Check for parallel fifths/octaves with melody
                parallel_penalty = 0
                if prev_harmony_pitch:
                    # We need previous melody note too - approximate check
                    pass  # Full check would need melody history
                
                # Prefer thirds and sixths with melody
                interval_with_melody = (melody_pitch.midi - candidate.pitch.midi) % 12
                if interval_with_melody in [3, 4, 8, 9]:  # thirds and sixths
                    interval_bonus = -1
                else:
                    interval_bonus = 0
                
                total_cost = vl_cost + parallel_penalty + interval_bonus
                candidates.append((candidate, total_cost))
        
        if not candidates:
            # Fallback: create a third below melody
            fallback = note.Note()
            fallback.pitch.midi = melody_pitch.midi - 4  # Major third below
            return fallback
        
        # Sort by cost and pick best (with some randomness for variety)
        candidates.sort(key=lambda x: x[1])
        
        # Pick from top 3 candidates with weighted probability
        top_candidates = candidates[:3]
        weights = [1.0 / (c[1] + 1) for c in top_candidates]
        total_weight = sum(weights)
        weights = [w / total_weight for w in weights]
        
        selected = random.choices(top_candidates, weights=weights)[0]
        return selected[0]
    
    def generate_bass_note(self, chord_numeral, detected_key, prev_bass_pitch):
        """
        Generate bass note (chord root) with smooth voice leading.
        """
        scale_pitches = self.get_scale_pitches(detected_key)
        mode = 'major' if detected_key.mode == 'major' else 'minor'
        chord_tones_map = self.major_chord_tones if mode == 'major' else self.minor_chord_tones
        
        if chord_numeral not in chord_tones_map:
            chord_numeral = 'I' if mode == 'major' else 'i'
        
        # Get root of chord (first scale degree in chord)
        root_degree = chord_tones_map[chord_numeral][0]
        root_pitch = scale_pitches[root_degree]
        
        # Create bass note
        bass = note.Note(root_pitch.name)
        bass.octave = 2  # Bass range
        
        # Apply voice leading - prefer stepwise motion
        if prev_bass_pitch:
            # Try different octaves to minimize movement
            best_bass = bass
            best_movement = abs(bass.pitch.midi - prev_bass_pitch.midi)
            
            for oct in [2, 3]:
                candidate = note.Note(root_pitch.name)
                candidate.octave = oct
                movement = abs(candidate.pitch.midi - prev_bass_pitch.midi)
                if movement < best_movement and candidate.pitch.midi >= 36:  # Above C2
                    best_movement = movement
                    best_bass = candidate
            
            bass = best_bass
        
        return bass
    
    def harmonize(self, input_path, output_path):
        """
        Main harmonization function with Markov chains and voice leading.
        """
        # Load MIDI file
        midi_stream = converter.parse(input_path)
        
        # Analyze key
        detected_key = self.analyze_key(midi_stream)
        mode = 'major' if detected_key.mode == 'major' else 'minor'
        print(f"Detected key: {detected_key} ({mode})")
        
        # Create streams for each voice
        melody_stream = stream.Part()
        melody_stream.id = 'Melody'
        
        harmony_stream = stream.Part()
        harmony_stream.id = 'Harmony'
        
        bass_stream = stream.Part()
        bass_stream.id = 'Bass'
        
        # Extract melody
        parts = midi_stream.parts
        if len(parts) > 0:
            original_melody = parts[0]
        else:
            original_melody = midi_stream.flatten()
        
        # Get all melody notes for phrase detection
        melody_elements = list(original_melody.flatten().notesAndRests)
        melody_notes_only = [e for e in melody_elements if isinstance(e, note.Note)]
        
        # Detect phrase boundaries
        phrase_boundaries = self.phrase_detector.detect_boundaries(melody_elements)
        print(f"Detected {len(phrase_boundaries)} phrase boundaries")
        
        # Initialize chord progression
        current_chord = 'I' if mode == 'major' else 'i'
        
        # Track previous notes for voice leading
        prev_harmony_pitch = None
        prev_bass_pitch = None
        prev_melody_pitch = None
        
        # Track timing for chord changes
        last_chord_change = -2.0
        last_bass_offset = -2.0
        
        # Process each element
        for i, element in enumerate(melody_elements):
            if isinstance(element, note.Note):
                current_offset = element.offset
                
                # === MELODY ===
                melody_note = note.Note(element.pitch)
                melody_note.duration = element.duration
                melody_stream.insert(current_offset, melody_note)
                
                # === CHORD PROGRESSION ===
                # Change chord every 2 beats or at phrase boundaries
                should_change_chord = (current_offset - last_chord_change) >= 2.0
                is_phrase_end = i in phrase_boundaries
                
                if should_change_chord:
                    if is_phrase_end:
                        # Use cadence at phrase boundaries
                        cadence = self.chord_generator.get_cadence_chords(mode)
                        # If we're at phrase end, use V (will resolve to I next)
                        current_chord = cadence[0]  # V
                    else:
                        # Normal Markov progression weighted by melody fit
                        current_chord = self.find_best_chord_for_melody(
                            element.pitch, detected_key, current_chord
                        )
                    last_chord_change = current_offset
                
                # If previous was V at phrase end, now resolve to I
                if i > 0 and (i - 1) in phrase_boundaries:
                    current_chord = 'I' if mode == 'major' else 'i'
                
                # Get chord tones for current chord
                chord_pitches = self.get_chord_from_melody(
                    [element], detected_key, current_chord
                )
                
                # === HARMONY ===
                harmony_note = self.generate_harmony_note(
                    element.pitch, chord_pitches, detected_key, prev_harmony_pitch
                )
                
                if harmony_note:
                    # Check for parallel fifths/octaves with melody
                    has_parallel_violation = False
                    if prev_harmony_pitch and prev_melody_pitch:
                        if self.voice_checker.is_parallel_fifth(
                            prev_melody_pitch, prev_harmony_pitch,
                            element.pitch, harmony_note.pitch
                        ):
                            has_parallel_violation = True
                        if self.voice_checker.is_parallel_octave(
                            prev_melody_pitch, prev_harmony_pitch,
                            element.pitch, harmony_note.pitch
                        ):
                            has_parallel_violation = True
                    
                    if has_parallel_violation:
                        # Try to find an alternative harmony note
                        for alt_pitch in chord_pitches:
                            alt_note = note.Note(alt_pitch.name)
                            alt_note.octave = element.pitch.octave - 1
                            if not self.voice_checker.is_parallel_fifth(
                                prev_melody_pitch, prev_harmony_pitch,
                                element.pitch, alt_note.pitch
                            ):
                                harmony_note = alt_note
                                break
                    
                    harmony_note.duration = element.duration
                    harmony_stream.insert(current_offset, harmony_note)
                    prev_harmony_pitch = harmony_note.pitch
                
                # === BASS ===
                # Bass changes on strong beats (every 2 quarter notes)
                if (current_offset - last_bass_offset) >= 2.0 or last_bass_offset < 0:
                    bass_note = self.generate_bass_note(
                        current_chord, detected_key, prev_bass_pitch
                    )
                    
                    # Duration: until next bass note (default 2 beats)
                    bass_note.duration.quarterLength = 2.0
                    bass_stream.insert(current_offset, bass_note)
                    
                    prev_bass_pitch = bass_note.pitch
                    last_bass_offset = current_offset
                
                prev_melody_pitch = element.pitch
            
            elif isinstance(element, note.Rest):
                # Add rest to melody
                rest = note.Rest()
                rest.duration = element.duration
                melody_stream.insert(element.offset, rest)
        
        # === ASSEMBLE SCORE ===
        score = stream.Score()
        
        # Add instruments
        melody_stream.insert(0, instrument.Piano())
        harmony_stream.insert(0, instrument.Piano())
        bass_stream.insert(0, instrument.AcousticBass())
        
        score.insert(0, melody_stream)
        score.insert(0, harmony_stream)
        score.insert(0, bass_stream)
        
        # Add key signature
        score.insert(0, detected_key)
        
        # Write output
        score.write('midi', fp=output_path)
        print(f"Harmonized MIDI saved to: {output_path}")
        
        # Print statistics
        print(f"\n=== Harmonization Statistics ===")
        print(f"Total melody notes: {len(melody_notes_only)}")
        print(f"Phrase boundaries detected: {len(phrase_boundaries)}")
        print(f"Key: {detected_key}")
        
        return output_path
    
    def train_model(self, training_data_path):
        """Placeholder for ML training (Phase 2)."""
        print("ML training not yet implemented. Using rule-based system.")
        pass
    
    def load_model(self, model_path):
        """Load pre-trained model."""
        try:
            from tensorflow import keras
            self.model = keras.models.load_model(model_path)
            print(f"Model loaded from {model_path}")
        except Exception as e:
            print(f"Error loading model: {e}")
            print("Falling back to rule-based harmonization.")
    
    def save_model(self, model_path):
        """Save trained model."""
        if self.model:
            self.model.save(model_path)
            print(f"Model saved to {model_path}")


# === TESTING ===
if __name__ == "__main__":
    # Quick test
    harmonizer = MIDIHarmonizer()
    
    # Test chord progression generator
    print("\n=== Testing Chord Progression Generator ===")
    prog_gen = ChordProgressionGenerator()
    chord = 'I'
    progression = [chord]
    for _ in range(7):
        chord = prog_gen.get_next_chord(chord, 'major')
        progression.append(chord)
    print(f"Sample progression: {' -> '.join(progression)}")
    
    # Test phrase detector
    print("\n=== Testing Phrase Detector ===")
    print("Phrase detector ready for melody input.")
    
    print("\n=== Harmonizer Ready ===")
    print("Usage: harmonizer.harmonize('input.mid', 'output.mid')")