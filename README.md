# Tracks API

Tracks API is a REST API used for getting information about various music tracks.

**Primary resource:** Tracks (track_id, track_name, duration_ms, genre, year, tags, total_playcount, danceability, mode, valence)

**Secondary resource 1:** Artists (artist_id, artist_name, albums)

**Secondary resource 2:** Albums (album_id, album_name, total_tracks, album_type, release_date, artists, tracks)

## Usage

| | URL |
|---|---|
| **Production API** | [patriciaj.se/tracks-api/](https://patriciaj.se/tracks-api/) |
| **API Documentation** | [patriciaj.se/tracks-api/docs](https://patriciaj.se/tracks-api/docs) |
| **Tracks v1 Docs** | [patriciaj.se/tracks-api/api/v1/docs](https://patriciaj.se/tracks-api/api/v1/docs) |
| **Auth v1 Docs** | [patriciaj.se/tracks-api/auth/api/v1/docs](https://patriciaj.se/tracks-api/auth/api/v1/docs) |

## Acknowledgements

- 1DV027 API Design Assignment
- Dataset on Kaggle: [Million Song Dataset + Spotify + Last.fm](https://www.kaggle.com/datasets/undefinenull/million-song-dataset-spotify-lastfm)  
- Additional information (album names and IDs) is from the Million Song Dataset summary file: [millionsongdataset.com/pages/getting-dataset/, (Additional files, 7)](http://millionsongdataset.com/pages/getting-dataset/)
