import cv2
import mediapipe as mp

image = cv2.imread('facehand-board.png')
if image is None:
    raise RuntimeError('找不到 facehand-board.png')
with mp.solutions.face_mesh.FaceMesh(static_image_mode=True, max_num_faces=1) as mesh:
    result = mesh.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
landmarks = result.multi_face_landmarks or []
for face in landmarks:
    mp.solutions.drawing_utils.draw_landmarks(
        image, face, mp.solutions.face_mesh.FACEMESH_CONTOURS,
        landmark_drawing_spec=None,
        connection_drawing_spec=mp.solutions.drawing_styles.get_default_face_mesh_contours_style())
if not cv2.imwrite('supplement4-camera-face-mesh.png', image):
    raise RuntimeError('無法儲存結果')
print('faces found:', len(landmarks))
print('landmark counts:', [len(face.landmark) for face in landmarks])
print('saved: supplement4-camera-face-mesh.png')
