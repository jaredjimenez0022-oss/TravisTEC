import cv2
from pathlib import Path

CASCADE = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'

def analyze_image_file(path):
    """Simple heuristic: detect faces and smiles using Haar cascades.

    Returns a dict with keys: dominant_emotion, face_count, details
    """
    p = Path(path)
    if not p.exists():
        return {"error": "file_not_found", "path": str(path)}

    img = cv2.imread(str(p))
    if img is None:
        return {"error": "invalid_image"}

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    face_cascade = cv2.CascadeClassifier(CASCADE)
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)

    # Use an extremely simple heuristic: if any face is smiling => happy else neutral
    smile_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_smile.xml')
    smiles = 0
    for (x, y, w, h) in faces:
        roi_gray = gray[y:y+h, x:x+w]
        ss = smile_cascade.detectMultiScale(roi_gray, 1.7, 20)
        smiles += len(ss)

    dominant = 'happy' if smiles > 0 else 'neutral'

    return {
        "dominant_emotion": dominant,
        "face_count": int(len(faces)),
        "details": {"smiles": int(smiles)}
    }
