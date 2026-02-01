import sys
import os
from analyzer import AudioAnalyzer
from music_theory import MusicTheoryHelper
from spotify_utils import SpotifyHandler

def main():
    if len(sys.argv) < 2:
        print("Usage: python cli.py <path_to_audio_file_or_spotify_url>")
        sys.exit(1)
        
    input_path = sys.argv[1]
    spotify = SpotifyHandler()
    
    audio_path = input_path
    is_spotify = spotify.is_spotify_url(input_path)
    
    if is_spotify:
        print(f"--- Spotify Input Detected ---")
        metadata = spotify.get_track_metadata(input_path)
        if metadata:
            print(f"Track: {metadata.get('title')} by {metadata.get('artist')}")
            audio_path = spotify.download_audio(metadata)
        else:
            print("Error: Could not retrieve Spotify metadata.")
            sys.exit(1)
            
    if not audio_path or not os.path.exists(audio_path):
        print(f"Error: File {audio_path} not found.")
        sys.exit(1)

    print(f"--- Analyzing: {os.path.basename(audio_path)} ---")
    
    analyzer = AudioAnalyzer()
    helper = MusicTheoryHelper()
    
    # 1. Detect Tonal Center
    print("Finding tonal center...")
    key = analyzer.analyze_key(audio_path)
    print(f"Detected Tonal Center: {key.upper()}")
    
    # 2. Get Chord Progression
    print("Estimating chord progression (simplified)...")
    progression = analyzer.get_chord_progression(audio_path)
    print(f"Chord Sequence: {' -> '.join(progression[:16])} {'...' if len(progression) > 16 else ''}")
    
    # 3. Suggestions
    print("\nScales and Melodies to play:")
    
    print("\n[ Concert Pitch ]")
    concert_suggestions = helper.suggest_scales(key)
    for name, scale in concert_suggestions.items():
        print(f"  - {name}: {scale}")
        
    print("\n[ Tenor Saxophone (Bb) ]")
    tenor_suggestions = helper.get_instrument_suggestions(key, 'Bb')
    for name, scale in tenor_suggestions.items():
        print(f"  - {name}: {scale}")
        
    print("\n[ Alto Saxophone (Eb) ]")
    alto_suggestions = helper.get_instrument_suggestions(key, 'Eb')
    for name, scale in alto_suggestions.items():
        print(f"  - {name}: {scale}")

    # Cleanup temporary spotify download
    if is_spotify and audio_path.startswith('downloads/'):
        # Optional: remove the temp file
        # os.remove(audio_path)
        pass

    print("\n-------------------------------------------")

if __name__ == "__main__":
    main()

