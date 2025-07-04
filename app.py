from flask import Flask, render_template, request, send_from_directory
import os
from PIL import Image, ImageDraw, ImageFont
import mediapipe as mp
import numpy as np

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
REPORT_FOLDER = 'reports'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(REPORT_FOLDER, exist_ok=True)

mp_face_mesh = mp.solutions.face_mesh


def compute_beauty_score(landmarks):
    # Golden ratio based heuristic using selected landmark points
    # Indices reference mediapipe face mesh landmarks
    key_points = {
        'left_eye_outer': 33,
        'right_eye_outer': 263,
        'nose_tip': 1,
        'mouth_left': 61,
        'mouth_right': 291,
        'chin': 152,
        'forehead': 10,
    }
    pts = {name: np.array([landmarks[idx].x, landmarks[idx].y]) for name, idx in key_points.items()}

    eye_distance = np.linalg.norm(pts['right_eye_outer'] - pts['left_eye_outer'])
    face_height = np.linalg.norm(pts['chin'] - pts['forehead'])
    ratio_eyes_face = eye_distance / face_height

    mouth_width = np.linalg.norm(pts['mouth_right'] - pts['mouth_left'])
    nose_to_mouth = np.linalg.norm(pts['nose_tip'] - (pts['mouth_left'] + pts['mouth_right']) / 2)
    ratio_mouth_nose = mouth_width / nose_to_mouth if nose_to_mouth != 0 else 0

    # Compare ratios to golden ratio ~1.618
    golden = 1.618
    score = 100 - (abs(ratio_eyes_face - golden) + abs(ratio_mouth_nose - golden)) * 50
    score = max(0, min(100, score))
    return score


def analyze_image(image_path):
    image = Image.open(image_path).convert('RGB')
    img_np = np.array(image)
    with mp_face_mesh.FaceMesh(static_image_mode=True) as face_mesh:
        results = face_mesh.process(img_np)
        if not results.multi_face_landmarks:
            return None
        landmarks = results.multi_face_landmarks[0].landmark
        score = compute_beauty_score(landmarks)
    return score


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files.get('photo')
        if not file:
            return render_template('index.html', error='No file uploaded')
        filename = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(filename)
        score = analyze_image(filename)
        if score is None:
            os.remove(filename)
            return render_template('index.html', error='No face detected')
        report_path = os.path.join(REPORT_FOLDER, file.filename)
        generate_report_image(filename, score, report_path)
        return render_template('result.html', score=score, report=file.filename)
    return render_template('index.html')


def generate_report_image(img_path, score, output_path):
    image = Image.open(img_path).convert('RGB')
    draw = ImageDraw.Draw(image)
    try:
        font = ImageFont.truetype('DejaVuSans.ttf', 40)
    except Exception:
        font = ImageFont.load_default()
    text = f"Hotness: {score:.1f}/100"
    draw.rectangle([(0, 0), (image.width, 50)], fill=(0, 0, 0, 128))
    draw.text((10, 5), text, font=font, fill=(255, 255, 255))
    image.save(output_path)


@app.route('/reports/<path:filename>')
def download_report(filename):
    return send_from_directory(REPORT_FOLDER, filename, as_attachment=True)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
