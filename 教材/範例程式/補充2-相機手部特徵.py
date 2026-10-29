import cv2
import mediapipe as mp

image = cv2.imread('facehand-board.png')
if image is None:
    raise RuntimeError('找不到 facehand-board.png')
with mp.solutions.hands.Hands(static_image_mode=True, max_num_hands=1, model_complexity=0) as hands:
    result = hands.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
landmarks = result.multi_hand_landmarks or []
for hand in landmarks:
    mp.solutions.drawing_utils.draw_landmarks(image, hand, mp.solutions.hands.HAND_CONNECTIONS)
if not cv2.imwrite('supplement2-camera-hand.png', image):
    raise RuntimeError('無法儲存結果')
print('hands found:', len(landmarks))
print('landmark counts:', [len(hand.landmark) for hand in landmarks])
print('saved: supplement2-camera-hand.png')
