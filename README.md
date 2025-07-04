# bejoyas

This repository contains a small Flask web app that lets users upload a selfie and get a playful "hotness" rating. The score is calculated from simple facial ratios (eye distance, mouth width, and symmetry) compared against the golden ratio. A random nudge is added so the results stay fun and unpredictable. A caption and short comment are generated from the score and displayed alongside a shareable report image.

## Running Locally

```bash
pip install -r requirements.txt
python app.py
```

The app will start on `http://localhost:5000`. To connect it to a domain such as `howhot.me`, deploy it to a server and configure your DNS records at GoDaddy to point to that server.

### How the rating works

The scoring system is intentionally light‑hearted. We measure distances between key facial landmarks detected by [MediaPipe](https://developers.google.com/mediapipe) and compare a couple of ratios to the famous golden ratio (≈1.618). A small bit of randomness is sprinkled in so the results feel less deterministic. Depending on the score, the app will choose a silly caption and a short comment to display with your result image.
