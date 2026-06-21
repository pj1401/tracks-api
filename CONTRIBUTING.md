# Contributing to Tracks API

## Contents

- [Getting started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Development Environment](#development-environment)

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

*Instructions for docker secrets*

**Set up .env files:**

*Instructions for .env files*

### Seed database

*How to seed the database with either the subset or the complete dataset*

Dataset: [Million Song Dataset + Spotify + Last.fm](https://www.kaggle.com/datasets/undefinenull/million-song-dataset-spotify-lastfm)  
Additional information (album names and IDs) is from the Million Song Dataset summary file: [millionsongdataset.com/pages/getting-dataset/, (Additional files, 7)](http://millionsongdataset.com/pages/getting-dataset/)

**Files**

Small subsets of the datasets are included in `seed/data-subset/` to allow faster testing.

The actual files should be placed in the `seed/data/` directory.  
The CSV files can be downloaded here: [Million Song Dataset + Spotify + Last.fm](https://www.kaggle.com/datasets/undefinenull/million-song-dataset-spotify-lastfm)  
The HDF5 file can be downloaded here: [http://millionsongdataset.com/pages/getting-dataset/, (Additional files, 7)](http://millionsongdataset.com/pages/getting-dataset/)

Update the path variables in the `.env` file:

```
CSV_PATH=data/Music Info.csv
CSV_LISTENING_HISTORY_PATH=data/User Listening History.csv
HDF5_PATH=data/msd_summary_file.h5
```

### Instructions

```powershell
# Copy from .example.env to .env
cp .example.env .env

# Create Secret Files
mkdir secrets
echo "admin" > secrets/admin_username.txt
echo "admin@example.com" > secrets/admin_email.txt
echo "very_secure_admin_password" > secrets/admin_password.txt

# Start container for db and seed script
docker-compose up db seed
docker-compose up db      # Start only database

# Stop container
docker-compose down
docker-compose down -v # Removes volumes
```

## Run dev

### Setup env

The app uses ECDSA for JWT signing.  
To generate the key pair:

```bash
# Generate private key
openssl ecparam -name secp521r1 -genkey -noout -out tracks-rest-api-jwt.pem

# Extract public key
openssl ec -in tracks-rest-api-jwt.pem -pubout -out tracks-rest-api-jwt.public.pem
```

Copy the contents of the key pair files to the `.env` file.

### Run

```powershell
# Change to the api directory
cd api/

# Start the database
docker-compose up db -d

# Run the app
uv run -- flask --app main run --debug

# Stop the database
docker-compose down
```
