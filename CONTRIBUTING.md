# Contributing to Tracks API

## Contents

- [Getting started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Development Environment](#development-environment)
  - [Seed database](#seed-database)

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

Create the secrets directory and write the secret files:

```powershell
mkdir secrets
echo "admin" > secrets/admin_username.txt
echo "admin@example.com" > secrets/admin_email.txt
echo "very_secure_admin_password" > secrets/admin_password.txt

# Don't add trailing newlines in the POSTGRES secret files
echo -n "library-postgres" > secrets/db_name.txt
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

*Instructions for .env files*

Copy the contents of the key pair files to the `.env` file.

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

**Run the seed script:**

### Instructions


