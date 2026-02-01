# TonalCenter Web GUI

A modern, AI-powered interface to analyze musical harmonics.

## How to use

1.  **Launch the server**:
    ```bash
    ./tonalcenter/bin/python app.py
    ```
2.  **Open your browser**:
    Navigate to `http://127.0.0.1:5001`

3.  **Search**:
    - Enter a song name (e.g., "The Girl From Ipanema").
    - Or paste a Spotify track URL.

4.  **Select Instrument**:
    Choose your instrument (Concert Pitch, Tenor Sax, Alto Sax, etc.) to automatically transpose all results.

## Features
- **Smart Search**: Uses YouTube fallback if song name is provided.
- **Glassmorphic Design**: A premium dark-theme aesthetic for studio environments.
- **Transposition Engine**: Handles complex interval shifts for Bb, Eb, and F instruments.
- **Harmonic Roadmap**: Displays detected tonal center and chord progression summary.
