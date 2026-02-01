from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
from analyzer import AudioAnalyzer
from music_theory import MusicTheoryHelper
from spotify_utils import SpotifyHandler

app = Flask(__name__, static_folder='static')
CORS(app)

analyzer = AudioAnalyzer()
helper = MusicTheoryHelper()
spotify = SpotifyHandler()

@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

@app.route('/style.css')
def css():
    return send_from_directory('static', 'style.css')

@app.route('/app.js')
def js():
    return send_from_directory('static', 'app.js')

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.json
    query = data.get('query')
    instrument = data.get('instrument', 'Bb') # Default to Tenor Sax

    if not query:
        return jsonify({'error': 'No song name or URL provided'}), 400

    try:
        # 1. Get Metadata
        if spotify.is_spotify_url(query):
            metadata = spotify.get_track_metadata(query)
        else:
            metadata = spotify.search_track(query)

        if not metadata:
            print(f"Error: Could not find track info for {query}")
            return jsonify({'error': 'Could not find track info'}), 404

        print(f"Meta found: {metadata.get('title')} - Downloading...")
        # 2. Download Audio
        audio_path = spotify.download_audio(metadata)
        if not audio_path or not os.path.exists(audio_path):
            print("Error: Audio download failed")
            return jsonify({'error': 'Could not retrieve audio for analysis'}), 500

        # 3. Analyze
        print(f"Analyzing harmonics for {audio_path}...")
        key = analyzer.analyze_key(audio_path)
        progression = analyzer.get_chord_progression(audio_path)
        print(f"Analysis complete: {key}")

        # 4. Get suggestions for the chosen instrument
        suggestions = helper.get_instrument_suggestions(key, instrument)
        concert_suggestions = helper.suggest_scales(key)

        # 5. Build response
        response = {
            'track': {
                'title': metadata.get('title'),
                'artist': metadata.get('artist')
            },
            'tonal_center': key.upper(),
            'progression': progression,
            'instrument': instrument,
            'suggestions': suggestions,
            'concert_pitch': concert_suggestions
        }

        return jsonify(response)

    except Exception as e:
        print(f"Server Error: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    os.makedirs('static', exist_ok=True)
    app.run(debug=True, port=5001)
