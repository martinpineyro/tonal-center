# TonalCenter Agent

An AI-powered agent to analyze audio files, identify the tonal center (key), and suggest scales for improvisation, specifically for Tenor Saxophone (Bb) and Alto Saxophone (Eb).

## Features
- **Key Detection**: Uses the Krumhansl-Schmuckler algorithm to identify the most likely musical key.
- **Chord Progression**: Basic estimation of the chord sequence.
- **Scale Suggestions**: Recommends Major, Minor, Pentatonic, and Blues scales.
- **Transposition**: Automatically transposes suggestions for Bb (Tenor) and Eb (Alto) instruments.

## Installation

1. Ensure you have Python 3.13+ installed.
2. The virtual environment `tonalcenter` is already set up in this directory.
3. Activate the environment:
   ```bash
   source tonalcenter/bin/activate
   ```
4. Install dependencies (already done):
   ```bash
   pip install librosa numpy soundfile music21 scipy
   ```

## Usage

Run the analysis on any audio file (wav, mp3, etc.):

```bash
./tonalcenter/bin/python cli.py path/to/your/song.mp3
```

## Project Structure
- `analyzer.py`: Audio analysis and key detection logic.
- `music_theory.py`: Music theory helper for scales and transposition.
- `cli.py`: Command-line interface.
- `IMPLEMENTATION_PLAN.md`: Roadmap for the project.
