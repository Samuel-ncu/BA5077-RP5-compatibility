import cv2
import mediapipe as mp

image = cv2.imread('facehand-board.png')
if image is None:
    raise RuntimeError('找不到 facehand-board.png')
with mp.solutions.hands.Hands(static_image_mode=True, max_num_hands=1, model_complexity=0) as detector:
    result = detector.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
hands = result.multi_hand_landmarks or []
print('hands found:', len(hands))
if hands:
    hand = hands[0]
    # 僅適用大致朝上的手：影像的 y 座標從上往下增加。
    up = [hand.landmark[tip].y < hand.landmark[pip].y
          for tip, pip in [(8, 6), (12, 10), (16, 14), (20, 18)]]
    if all(up):
        gesture = 'paper'
    elif not any(up):
        gesture = 'rock'
    elif up == [True, True, False, False]:
        gesture = 'scissors'
    else:
        gesture = 'unknown'
    print('index, middle, ring, little:', up)
    print('predicted gesture:', gesture)
    mp.solutions.drawing_utils.draw_landmarks(image, hand, mp.solutions.hands.HAND_CONNECTIONS)
    cv2.putText(image, gesture, (20, 45), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 200, 0), 2)
    if not cv2.imwrite('supplement5-camera-gesture.png', image):
        raise RuntimeError('無法儲存結果')
    print('saved: supplement5-camera-gesture.png')
