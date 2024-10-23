from flask import Flask, render_template, Response
import cv2
import mediapipe as mp
import pandas as pd
import os

app = Flask(__name__)

# Initialize MediaPipe Face Mesh
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(static_image_mode=False, max_num_faces=1, refine_landmarks=True)
mp_drawing = mp.solutions.drawing_utils
drawing_spec = mp_drawing.DrawingSpec(thickness=1, circle_radius=1)

# Prepare output directory
output_dir = os.path.join(os.getcwd(), 'output')
os.makedirs(output_dir, exist_ok=True)

# Global variables
frame_count = 0
all_landmarks = []

# Initialize video capture
camera = cv2.VideoCapture(0)

@app.route('/')
def index():
    return render_template('index.html')

def gen_frames():
    global frame_count, all_landmarks
    while frame_count < 900:
        success, frame = camera.read()  # Read frame from camera
        if not success:
            break
        else:
            # Convert the BGR image to RGB
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Process the frame for face landmarks
            results = face_mesh.process(rgb_frame)

            if results.multi_face_landmarks:
                for face_landmarks in results.multi_face_landmarks:
                    frame_landmarks = []
                    for lm in face_landmarks.landmark:
                        x, y = int(lm.x * frame.shape[1]), int(lm.y * frame.shape[0])
                        # Get RGB values at the landmark points
                        if 0 <= x < frame.shape[1] and 0 <= y < frame.shape[0]:
                            r, g, b = rgb_frame[y, x]
                            frame_landmarks.append([frame_count, x, y, r, g, b])

                    all_landmarks.extend(frame_landmarks)

                    # Draw face mesh on the frame
                    mp_drawing.draw_landmarks(
                        image=frame,
                        landmark_list=face_landmarks,
                        connections=mp_face_mesh.FACEMESH_TESSELATION,
                        landmark_drawing_spec=drawing_spec,
                        connection_drawing_spec=drawing_spec
                    )

            # Display the frame count on the video
            cv2.putText(frame, f"Frame: {frame_count}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

            # Encode the frame back to bytes for Flask to stream
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            frame_count += 1

            print(f"Frame: {frame_count}, Faces detected: {len(results.multi_face_landmarks) if results.multi_face_landmarks else 0}")

            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    # Once 900 frames are processed, save landmarks to CSV
    if frame_count >= 900:
        save_to_csv()

def save_to_csv():
    csv_path = os.path.join(output_dir, 'landmarks.csv')
    df = pd.DataFrame(all_landmarks, columns=['Frame', 'X', 'Y', 'R', 'G', 'B'])
    df.to_csv(csv_path, index=False)

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(debug=True)
