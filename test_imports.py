import sys
try:
    import librosa
    import numpy
    import music21
    import scipy
    print("Core libraries imported successfully.")
    
    from music_theory import MusicTheoryHelper
    helper = MusicTheoryHelper()
    key = "C major"
    transposed = helper.get_transposed_key(key, 'Bb')
    print(f"Test Transposition: {key} -> Tenor Sax: {transposed}")
    if transposed == "D major":
        print("Transposition logic: PASS")
    else:
        print(f"Transposition logic: FAIL (Expected D major, got {transposed})")
except Exception as e:
    print(f"Test FAILED: {e}")
    sys.exit(1)
