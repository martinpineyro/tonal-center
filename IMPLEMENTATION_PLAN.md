## Proposed Changes

1.  **Dependency Addition**:
    - Installed `spotipy`, `yt-dlp`, and `python-dotenv`.
    
2.  **Spotify API Integration**:
    - Created `spotify_utils.py` with `SpotifyHandler`.
    - Supports `spotipy` for high-quality metadata and audio features (requires `SPOTIPY_CLIENT_ID` and `SPOTIPY_CLIENT_SECRET`).
    - Includes a scraping fallback to identify track names from URLs (best effort).

3.  **Audio Extraction**:
    - Uses `yt-dlp` to find and download the corresponding audio from YouTube for analysis.
    - Saves temporary files in a `downloads/` directory.

4.  **CLI Enhancement**:
    - Updated `cli.py` to recognize Spotify URLs.
    - Automatically downloads and analyzes tracks when a URL is provided.

## Next Steps
- User needs to provide Spotify API keys in a `.env` file for reliable metadata.
- I will now verify the integration with a dummy test if possible, or wait for the user to try with their keys.

## Success Criteria
- Running `python cli.py https://open.spotify.com/track/...` works.
- Tonal center is correctly identified for Spotify tracks.
- Transposed scales are suggested for the detected key.
