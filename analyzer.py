import librosa
import numpy as np
import scipy.stats

class AudioAnalyzer:
    def __init__(self):
        # Krumhansl-Schmuckler key profiles
        self.major_profile = np.array([6.35, 2.23, 3.48, 2.33, 4.38, 4.09, 2.52, 5.19, 2.39, 3.66, 2.29, 2.88])
        self.minor_profile = np.array([6.33, 2.68, 3.52, 5.38, 2.60, 3.53, 2.54, 4.75, 3.98, 2.69, 3.34, 3.17])
        self.note_names = ['C', 'C#', 'D', 'Eb', 'E', 'F', 'F#', 'G', 'Ab', 'A', 'Bb', 'B']

    def analyze_key(self, audio_path):
        """
        Analyzes the audio file and returns the estimated key (e.g., 'C major').
        """
        # Load only 45s for faster analysis
        y, sr = librosa.load(audio_path, duration=45)
        
        # Compute chromagram
        chroma = librosa.feature.chroma_stft(y=y, sr=sr)
        
        # Mean chroma across time
        mean_chroma = np.mean(chroma, axis=1)
        
        # Correlations with key profiles
        best_score = -1
        best_key = None
        
        for i in range(12):
            # Rotate profiles to check each key
            major_corr = np.corrcoef(mean_chroma, np.roll(self.major_profile, i))[0, 1]
            minor_corr = np.corrcoef(mean_chroma, np.roll(self.minor_profile, i))[0, 1]
            
            if major_corr > best_score:
                best_score = major_corr
                best_key = f"{self.note_names[i]} major"
            
            if minor_corr > best_score:
                best_score = minor_corr
                best_key = f"{self.note_names[i]} minor"
                
        return best_key

    def get_chord_progression(self, audio_path):
        """
        Rough estimation of chord progression using chroma segments.
        This is a simplified version.
        """
        y, sr = librosa.load(audio_path, duration=45)
        chroma = librosa.feature.chroma_stft(y=y, sr=sr)
        
        # Beat tracking to segment chords by beat
        tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr)
        beat_chroma = librosa.util.sync(chroma, beat_frames, aggregate=np.median)
        
        chords = []
        for i in range(beat_chroma.shape[1]):
            frame_chroma = beat_chroma[:, i]
            # Simple heuristic: the most prominent note is the chord root
            root_idx = np.argmax(frame_chroma)
            chords.append(self.note_names[root_idx])
            
        # Group consecutive identical chords
        if not chords:
            return []
            
        summary = []
        current_chord = chords[0]
        for chord in chords[1:]:
            if chord != current_chord:
                summary.append(current_chord)
                current_chord = chord
        summary.append(current_chord)
        
        return summary

if __name__ == "__main__":
    # Test (will fail if no audio file is provided)
    import sys
    if len(sys.argv) > 1:
        analyzer = AudioAnalyzer()
        key = analyzer.analyze_key(sys.argv[1])
        print(f"Detected Key: {key}")
