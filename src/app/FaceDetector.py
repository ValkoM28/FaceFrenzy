import cv2
from dataclasses import dataclass, field


@dataclass
class DetectionResult:
    face_count: int
    faces: list
    eyes: dict = field(default_factory=dict)


class FaceDetector:
    def __init__(self, cascade_path, scale_factor=1.3, min_neighbors=5, min_size=(30, 30), detect_eyes=False):
        self.scale_factor = scale_factor
        self.min_neighbors = min_neighbors
        self.min_size = min_size
        self.detect_eyes = detect_eyes

        self.face_cascade = cv2.CascadeClassifier(cascade_path)
        if detect_eyes:
            eye_cascade_path = cascade_path.replace('frontalface_default', 'eye')
            self.eye_cascade = cv2.CascadeClassifier(eye_cascade_path)

    def detect(self, frame) -> DetectionResult:
        # --- offload candidate: grayscale conversion ---
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # --- offload candidate: Haar cascade sliding-window search ---
        faces = self.face_cascade.detectMultiScale(
            gray,
            scaleFactor=self.scale_factor,
            minNeighbors=self.min_neighbors,
            minSize=self.min_size,
        )

        if len(faces) == 0:
            return DetectionResult(face_count=0, faces=[])

        eyes = {}
        if self.detect_eyes:
            for i, (x, y, w, h) in enumerate(faces):
                roi_gray = gray[y:y + h, x:x + w]
                # --- offload candidate: eye detection within each face ROI ---
                detected = self.eye_cascade.detectMultiScale(roi_gray)
                eyes[i] = list(detected) if len(detected) > 0 else []

        return DetectionResult(face_count=len(faces), faces=list(faces), eyes=eyes)

    def draw_detections(self, frame, result: DetectionResult):
        annotated = frame.copy()

        for i, (x, y, w, h) in enumerate(result.faces):
            cv2.rectangle(annotated, (x, y), (x + w, y + h), (255, 0, 0), 2)

            for (ex, ey, ew, eh) in result.eyes.get(i, []):
                cv2.rectangle(
                    annotated,
                    (x + ex, y + ey),
                    (x + ex + ew, y + ey + eh),
                    (0, 255, 0), 2
                )

        return annotated
