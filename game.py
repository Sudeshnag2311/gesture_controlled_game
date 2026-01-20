import cv2
import pyautogui
import mediapipe as mp
import time
pyautogui.FAILSAFE=True
cap=cv2.VideoCapture(0)
mphands=mp.solutions.hands
hands=mphands.Hands(max_num_hands=1)
mpdraw=mp.solutions.drawing_utils
cv2.namedWindow("image", cv2.WINDOW_NORMAL)
cv2.resizeWindow("image", 320, 240)
cv2.moveWindow("image", 20, 80)
DEAD_ZONE = 0.15
ACTION_THRESHOLD = 0.05
COOLDOWN = 0.6
last_action_time = 0
def can_act():
    global last_action_time
    now = time.time()
    if now - last_action_time > COOLDOWN:
        last_action_time = now
        return True
    return False
while True:
    ret,img=cap.read()
    h,w,c=img.shape
    img = cv2.flip(img, 1)
    imgrgb=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    result=hands.process(imgrgb)
    if result.multi_hand_landmarks:
        for handlms in result.multi_hand_landmarks:
            mpdraw.draw_landmarks(img,handlms,mphands.HAND_CONNECTIONS)
            thumb_tip = handlms.landmark[4]
            thumb_base = handlms.landmark[2]
            dy = thumb_tip.y - thumb_base.y
            if dy < -(DEAD_ZONE + ACTION_THRESHOLD) and can_act():
                pyautogui.press('up')
                print("JUMP")
            elif dy > (DEAD_ZONE + ACTION_THRESHOLD) and can_act():
                pyautogui.press('down')
                print("DOWN")
            index_tip = handlms.landmark[8]
            index_base = handlms.landmark[5]
            dx = index_tip.x - index_base.x
            if dx < -(DEAD_ZONE + ACTION_THRESHOLD) and can_act():
                pyautogui.press('left')
                print("LEFT")
            elif dx > (DEAD_ZONE + ACTION_THRESHOLD) and can_act():
                pyautogui.press('right')
                print("RIGHT")      
    cv2.imshow("image",img)
    if cv2.waitKey(1)&0xff==ord('q'):
       break
cap.release()
cv2.destroyAllWindows()    



