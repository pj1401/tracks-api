# Tracks API

Tracks API is a REST API used for getting information about various music tracks.

**Main resources:**

**Primary resource (CRUD):** Tracks (id, name, duration_ms, genre, year, tags, total_playcount, danceability, mode, valence)

**Secondary resource 1 (read-only):** Artists (id, name, albums, tracks)

**Secondary resource 2 (read-only):** Albums (id, name, year (not implemented), artists, tracks)

## Usage

| | URL |
|---|---|
| **Production API** | [patriciaj.se/tracks-api/](https://patriciaj.se/tracks-api/) |
| **API Documentation** | [patriciaj.se/tracks-api/docs](https://patriciaj.se/tracks-api/docs) |
| **Tracks v1 Docs** | [patriciaj.se/tracks-api/api/v1/docs](https://patriciaj.se/tracks-api/api/v1/docs) |
| **Auth v1 Docs** | [patriciaj.se/tracks-api/auth/api/v1/docs](https://patriciaj.se/tracks-api/auth/api/v1/docs) |

**HTTP methods**

Tracks API:

| Resource | POST | GET | PUT | DELETE |
|----------|------|-----|-----|--------|
| /tracks | Create a new track | Retrieve all tracks | ❌ (Error) | ❌ |
| /tracks/1 | ❌ | Retrieve details of track 1 | Update details of track 1 if it exists | Delete track 1 |
| /artists | ❌ | Retrieve all artists | ❌ | ❌ |
| /artists/1 | ❌ | Retrieve details of artist 1 | ❌ | ❌ |
| /albums | ❌ | Retrieve all albums | ❌ | ❌ |
| /albums/1 | ❌ | Retrieve details of album 1 | ❌ | ❌ |

A Method Not Allowed error (405) is returned for undefined methods. But currently my error module incorrectly maps the status code in the response body to 500.

Auth API:

| Action / Resource | POST | GET | PUT | DELETE |
|----------|------|-----|-----|--------|
| /register | Register a new user | ❌ | ❌ | ❌ |
| /login | Log in a user | ❌ | ❌ | ❌ |
| /users/1 | ❌ | ❌ | ❌ | Delete user 1 |


## Acknowledgements

- 1DV027 API Design Assignment
- Dataset on Kaggle: [Million Song Dataset + Spotify + Last.fm](https://www.kaggle.com/datasets/undefinenull/million-song-dataset-spotify-lastfm)  
- Additional information (album names and IDs) is from the Million Song Dataset summary file: [millionsongdataset.com/pages/getting-dataset/, (Additional files, 7)](http://millionsongdataset.com/pages/getting-dataset/)
