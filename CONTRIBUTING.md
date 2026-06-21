# Contributing to Tracks API

## Contents

- [Getting started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Development Environment](#development-environment)
  - [Seed database](#seed-database)
  - [Run the APIs](#run-the-apis)

## Getting started

### Prerequisites

Tools used in development:

- docker compose
- uv package manager
- Apidog for documenting the API
- Postman / Newman for running API tests

### Development Environment

Start by cloning the repository:

```bash
# clone the repository using ssh
git clone git@github.com:pj1401/tracks-api.git

# change directory
cd tracks-api

# Copy from .example.env to .env
cp auth-service/.example.env auth-service/.env
cp seed/.example.env seed/.env
cp tracks-api/.example.env tracks-api/.env
```

**Environment variables in seed directory:**

*List the environment variables*

**Set up docker secrets:**

Create the secrets directory and write the secret files:

```powershell
mkdir secrets
echo "admin" > secrets/admin_username.txt
echo "admin@example.com" > secrets/admin_email.txt
echo "very_secure_admin_password" > secrets/admin_password.txt

# Don't add trailing newlines in the POSTGRES secret files
echo -n "tracks-api-postgres" > secrets/db_name.txt
echo -n "db_user" > secrets/db_user.txt
echo -n "db_pass" > secrets/db_password.txt
```

Create a random secret key for Flask:

```bash
openssl rand -hex 16
# Example output: dd5c21f46c93b3956ab256cf120f9e29

# Replace random-string with your output
echo "random-string" > secrets/flask_secret_key.txt
```

The app uses ECDSA for JWT signing.  
To generate the key pair:

```bash
# Generate private key
openssl ecparam -name secp521r1 -genkey -noout -out secrets/tracks-api-jwt-key

# Extract public key
openssl ec -in secrets/tracks-api-jwt-key -pubout -out secrets/tracks-api-jwt-key.pub
```

**Set up .env files:**

Copy the contents of the generated keys the `.env` files in `auth-service` and `tracks-api`.

Replace these in `auth-service/.env`:

```
FLASK_SECRET_KEY={ Random string }
JWT_PRIVATE_KEY={ An EC private key. }
JWT_PUBLIC_KEY={ An EC public key. }
```

Replace `JWT_PUBLIC_KEY` in `tracks-api/.env`:

```
JWT_PUBLIC_KEY={ An EC public key. }
```

### Seed database

*How to seed the database with either the subset or the complete dataset*

Dataset, both `Music Info.csv` and `User Listening History.csv` are used: [Million Song Dataset + Spotify + Last.fm](https://www.kaggle.com/datasets/undefinenull/million-song-dataset-spotify-lastfm)  
Additional information (album names and IDs) is from the Million Song Dataset summary file (msd_summary_file.h5): [millionsongdataset.com/pages/getting-dataset/, (Additional files, 7)](http://millionsongdataset.com/pages/getting-dataset/)

**Files**

Small subsets of the datasets are included in `seed/data-subset/` to test that the seed script works. The subsets includes the 50 first tracks from the `Music Info` file. Unused columns aren't included in the `listening-history-subset.csv` and `msd-summary-subset.h5` files to keep the file size small.

The full dataset files should be placed in the `seed/data/` directory.  
The CSV files (`Music Info.csv` and `User Listening History.csv`) can be downloaded here: [Million Song Dataset + Spotify + Last.fm](https://www.kaggle.com/datasets/undefinenull/million-song-dataset-spotify-lastfm)  
The HDF5 file (`msd_summary_file.h5`) can be downloaded here : [http://millionsongdataset.com/pages/getting-dataset/, (Additional files, 7)](http://millionsongdataset.com/pages/getting-dataset/)

Update the path variables in the `seed/.env` file if using `uv`:

```
CSV_PATH=data/Music Info.csv
CSV_LISTENING_HISTORY_PATH=data/User Listening History.csv
HDF5_PATH=data/msd_summary_file.h5
```

### Run the APIs

**Using docker:**

```powershell
# Start the services in detached mode
docker compose -f docker-compose.subset.yml up -d

# Remove '-f docker-compose.subset.yml' if the full dataset is used:
docker compose up -d
```
tracks-api and auth-service should start once the seed service exits.  
To check the logs:

```powershell
docker compose logs tracks-api
```

If the logs contain `"GET /api/v1/health HTTP/1.1" 200 OK`, that means the tracks-api is running.

```powershell
docker compose logs auth-service
```

The logs should contain:

```
Request: GET /api/v1/health 127.0.0.1
Response: 200 GET /api/v1/health
```

The Tracks API can be reached at [http://localhost:5000](http://127.0.0.1:5000)
The Auth API can be reached at [http://localhost:5010](http://127.0.0.1:5010)

**Using uv:**

Run the seed script first:

```powershell
# change to the seed directory
cd seed

# Set .venv and install dependencies
uv sync --group dev

# Run the script
uv run src/main.py
```

The APIs can be started after the seed script finishes.

To start the tracks-api:

```powershell
# from the root directory change to the tracks-api directory
cd tracks-api

# Set .venv and install dependencies
uv sync --group dev

# Start the API in dev mode
uv run fastapi dev
```

The Tracks API can be reached at [http://localhost:8000](http://127.0.0.1:8000)

Start the auth-service in a separate terminal:

```powershell
# from the root directory change to the auth-service directory
cd auth-service

# Set .venv and install dependencies
uv sync --group dev

# Start the API in dev mode
uv run -- flask --app src/main run --debug
```

The Auth API can be reached at [http://localhost:5000](http://127.0.0.1:5000)
