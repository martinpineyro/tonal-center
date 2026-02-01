import os
import re
import yt_dlp
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from dotenv import load_dotenv

load_dotenv()

class SpotifyHandler:
    def __init__(self):
        self.client_id = os.getenv('SPOTIPY_CLIENT_ID')
        self.client_secret = os.getenv('SPOTIPY_CLIENT_SECRET')
        self.sp = None
        
        if self.client_id and self.client_secret:
            try:
                auth_manager = SpotifyClientCredentials(client_id=self.client_id, client_secret=self.client_secret)
                self.sp = spotipy.Spotify(auth_manager=auth_manager)
            except Exception as e:
                print(f"Warning: Spotify authentication failed: {e}")

    def is_spotify_url(self, url):
        return 'open.spotify.com/track/' in url

    def search_track(self, query):
        """
        Searches for a track by name using yt-dlp to get metadata and find audio.
        """
        print(f"Searching for track: {query}")
        with yt_dlp.YoutubeDL({'quiet': True, 'no_warnings': True}) as ydl:
            try:
                # Search on YouTube
                search_results = ydl.extract_info(f"ytsearch1:{query}", download=False)
                if not search_results['entries']:
                    return None
                    
                first_result = search_results['entries'][0]
                return {
                    'title': first_result.get('title'),
                    'artist': first_result.get('uploader') or first_result.get('artist', 'Unknown'),
                    'id': first_result.get('id')
                }
            except Exception as e:
                print(f"Search failed: {e}")
                return None

    def get_track_metadata(self, url):
        if not self.sp:
            # Fallback: Scrape or use yt-dlp to guess
            return self._guess_metadata_from_url(url)
        
        try:
            track_id = url.split('/')[-1].split('?')[0]
            track = self.sp.track(track_id)
            return {
                'title': track['name'],
                'artist': track['artists'][0]['name'],
                'key': track.get('audio_features', {}).get('key'),
                'mode': track.get('audio_features', {}).get('mode')
            }
        except Exception as e:
            print(f"Error fetching Spotify metadata: {e}")
            return self._guess_metadata_from_url(url)

    def _guess_metadata_from_url(self, url):
        # Basic fallback using requests to get title/artist from meta tags
        import requests
        try:
            # Use a more realistic browser User-Agent
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code == 200:
                # More flexible regex to handle attribute order and quotes
                title_match = re.search(r'property="og:title" content="(.*?)"', response.text) or \
                              re.search(r'content="(.*?)" property="og:title"', response.text)
                
                desc_match = re.search(r'property="og:description" content="(.*?)"', response.text) or \
                             re.search(r'content="(.*?)" property="og:description"', response.text)
                
                if title_match:
                    title = title_match.group(1)
                    # Artist is usually the first part of the description before ' · '
                    artist = "Unknown"
                    if desc_match:
                        desc = desc_match.group(1)
                        if ' · ' in desc:
                            artist = desc.split(' · ')[0]
                        else:
                            artist = desc.split(' - ')[0]
                    return {'title': title, 'artist': artist}
        except Exception as e:
            print(f"Metadata scraping failed: {e}")
        return None

    def download_audio(self, metadata):
        if not metadata or not metadata.get('title'):
            print("Could not determine track metadata for download.")
            return None

        search_query = f"{metadata['artist']} {metadata['title']} audio"
        print(f"Searching YouTube for: {search_query}")
        
        os.makedirs('downloads', exist_ok=True)
        out_path = 'downloads/spotify_temp'
        
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'outtmpl': out_path,
            'quiet': True,
            'no_warnings': True,
        }
        
        # Cleanup previous temp file
        if os.path.exists(f"{out_path}.mp3"):
            try:
                os.remove(f"{out_path}.mp3")
            except:
                pass

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            try:
                ydl.download([f"ytsearch:{search_query}"])
                return f"{out_path}.mp3"
            except Exception as e:
                print(f"Download failed: {e}")
                return None
