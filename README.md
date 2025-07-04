# bejoyas

This repository now contains a simple Flask web application that lets users upload a photo and receive a "hotness" score based on a heuristic using face landmarks. A report image with the score is generated so it can be shared on social media.

## Running Locally

```bash
pip install -r requirements.txt
python app.py
```

The app will start on `http://localhost:5000`. To connect it to a domain such as `howhot.me`, deploy it to a server and configure your DNS records at GoDaddy to point to that server.
