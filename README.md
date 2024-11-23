# hackathon-openconf-2024

## How to run locally
- RUN `export GEMINI_API_KEY="your_gemini_api_key"`
- RUN `pip install --no-cache-dir -r requirements.txt`
- RUN `python3 app.py`

## How to run with Docker
- RUN `docker build -t ecobyte .`

## How to push a new image to Artifact Registry
- RUN `gcloud auth login`
- RUN `gcloud auth configure-docker europe-west1-docker.pkg.dev`
- RUN `docker tag ecobyte:latest europe-west1-docker.pkg.dev/openhack24ath-704/ecobyte/ecobyte:latest`
- RUN `docker push europe-west1-docker.pkg.dev/openhack24ath-704/ecobyte/ecobyte:latest`
