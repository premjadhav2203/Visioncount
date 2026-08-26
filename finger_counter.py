import cv2
import mediapipe as mp

mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

hands = mp_hands.Hands(static_image_mode=False, 
                       max_num_hands=1, 
                       min_detection_confidence=0.7)

tip_ids = [4, 8, 12, 16, 20]

cap = cv2.VideoCapture(0)

print("AI Finger Counter Started. Press 'q' to exit.")

while True:
    success, img = cap.read()
    if not success:
        print("Camera not found.")
        break

    img = cv2.flip(img, 1)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(img_rgb)
    
    # Initialize total_fingers to 0 every frame
    total_fingers = 0
    fingers_status = []

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(img, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            lm_list = []
            for id, lm in enumerate(hand_landmarks.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                lm_list.append([id, cx, cy])

            if len(lm_list) != 0:
                # --- FIX 1: THUMB LOGIC ---
                # Logic: Is thumb tip (4) to the left of the thumb IP joint (3)?
                # We use [0] for the thumb id index
                if lm_list[tip_ids[0]][1] < lm_list[tip_ids[0] - 1][1]:
                    fingers_status.append(1)
                else:
                    fingers_status.append(0)

                # FINGERS LOGIC
                for id in range(1, 5):
                    # Logic: Is finger tip (8,12,16,20) ABOVE the pip joint (6,10,14,18)?
                    # 'Above' means the Y value is LOWER (closer to 0)
                    if lm_list[tip_ids[id]][2] < lm_list[tip_ids[id] - 2][2]:
                        fingers_status.append(1)
                    else:
                        fingers_status.append(0)

            total_fingers = fingers_status.count(1)

            # --- FIX 2: DRAWING ERROR ---
            # Changed cv2.FILLED to -1 (Works on all versions)
            cv2.rectangle(img, (20, 20), (170, 170), (0, 255, 0), -1)
            
            # Ensure text is drawn cleanly
            cv2.putText(img, str(total_fingers), (45, 145), cv2.FONT_HERSHEY_PLAIN,
                        10, (255, 0, 0), 25)

    cv2.imshow("AI Finger Counter", img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()