import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

import pydirectinput as pyautogui
import time
import math

pyautogui.PAUSE = 0
pyautogui.FAILSAFE = False

#init - initializing the position of the slider
#play - key presses are active
#pause - pausing the key presses and init
status = "pause"
curinit = True

#- model path, change if needed -#
model_path = './hand_landmarker.task'


h = 1280
w = 720

#- change if initializing needs longer -#
init_time = 100

#positions for the sliders
sliderz = 0
sliderx1 = 0
sliderx2 = 0
deltaz = 0.025 #the window for detecting presses

init_cnt = 0

tmp_cnt = 0

current_keys_pressed = set([])

#options
BaseOptions = mp.tasks.BaseOptions
HandLandmarker = mp.tasks.vision.HandLandmarker
HandLandmarkerOptions = mp.tasks.vision.HandLandmarkerOptions
VisionRunningMode = mp.tasks.vision.RunningMode

options = HandLandmarkerOptions(
    num_hands=2,
    base_options=BaseOptions(model_asset_path=model_path),
    running_mode=VisionRunningMode.IMAGE,
    min_hand_detection_confidence = 0.3,
    min_tracking_confidence = 0.3)
detector = vision.HandLandmarker.create_from_options(options)


class point:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

# gets the positions of all the points
def get_pos(result):
    arr = []

    if len(result.hand_landmarks) >= 1:
        for i in result.hand_landmarks[0]:
            #print(f"{i.x} {i.y} {i.z}")
            current_point = point(i.x, i.y, i.z)
            arr.append(current_point)

    if len(result.hand_landmarks) >= 2:
        for i in result.hand_landmarks[1]:
            #print(f"{i.x} {i.y} {i.z}")
            current_point = point(i.x, i.y, i.z)
            arr.append(current_point)

    return arr


#initializes the position of the slider
def init_slider(result):
    global sliderz, sliderx1, sliderx2

    pos = get_pos(result)
    if len(pos) == 0:
        return
    
    average_z = 0
    average_x1 = 0
    average_x2 = 0
    idx = 0
    for i in pos:
        average_z += i.z

        if idx == 17 or idx == 18 or idx == 19 or idx == 20:
            average_x1 += i.x

        if idx == 38 or idx == 39 or idx == 40 or idx == 41:
            average_x2 += i.x

        idx += 1

    average_z /= len(pos)
    average_x1 /= 4
    average_x2 /= 4
    
    if sliderz == 0:
        sliderz = average_z
    else:
        sliderz = (sliderz + average_z)/2

    if sliderx1 == 0:
        sliderx1 = average_x1
    else:
        sliderx1 = (sliderx1 + average_x1)/2

    if len(pos) == 42:
        if sliderx2 == 0:
            sliderx2 = average_x2
        else:
            sliderx2 = (sliderx2 + average_x2)/2


#presses the keys
def press_keys(result):
    global sliderz, sliderx1, sliderx2, current_keys_pressed, tmp_cnt

    pos = get_pos(result)

    tmp_cnt += 1
    
    temp_keys_pressed = set([])

    for i in pos:
        if i.z > sliderz + 1*deltaz:
            if i.x < sliderx1 or i.x > sliderx2:
                continue

            back_slider = "9kmjnhbgvfcdxsza"
            temp_keys_pressed.add(back_slider[math.floor((i.x-sliderx1) / (sliderx2-sliderx1)*16)])
        elif i.z > sliderz:
            temp_keys_pressed.add('0')
        elif i.z > sliderz - deltaz:
            temp_keys_pressed.add('o')
        elif i.z > sliderz - 2*deltaz:
            temp_keys_pressed.add('l')
        elif i.z > sliderz - 3*deltaz:
            temp_keys_pressed.add('p')
        elif i.z > sliderz - 4*deltaz:
            temp_keys_pressed.add(',')
        elif i.z > sliderz - 5*deltaz:
            temp_keys_pressed.add('.')

    if tmp_cnt % 8 == 0:
        for i in current_keys_pressed:
            pyautogui.keyUp(i)

        current_keys_pressed = set([])
        tmp_cnt = 0

    for i in temp_keys_pressed:
        if i not in current_keys_pressed:
            pyautogui.keyDown(i)
            current_keys_pressed.add(i)


with HandLandmarker.create_from_options(options) as landmarker:
    cap = cv2.VideoCapture(0) 
    #cap.set(cv2.CAP_PROP_FRAME_WIDTH, h)
    #cap.set(cv2.CAP_PROP_FRAME_HEIGHT, w)  
    print("Press Space to initialize the slider:")

    if not cap.isOpened():
        print("Cannot open camera")
        exit()
    while True:
        if cv2.waitKey(1) == 27: #stops if esc is pressed
            break

        if cv2.waitKey(1) == 32: #toggles key presses if space is pressed
            if status == 'play':
                status = 'pause'
            elif curinit:
                status = 'init'
            else:
                status = 'play'

        ret, frame = cap.read()
        if not ret:
            print("Cannot receive frame")
            break
        
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame)
        hand_landmarker_result = detector.detect(mp_image)
        
        #print(hand_landmarker_result.handedness)
        #print(hand_landmarker_result)

        cv2.imshow('Camnithm', frame)

        if status == 'pause':
            continue
        elif status == 'init':
            if init_cnt == 0:
                print("Starting initialization...")
                time.sleep(3)

            if init_cnt % 10 == 0:
                print(f"{(init_time - init_cnt)/10}...")

            init_cnt += 1
            init_slider(hand_landmarker_result)

            if init_cnt >= init_time:
                status = 'play'
                curinit = False

                if sliderx1 > sliderx2:
                    sliderx1, sliderx2 = sliderx2, sliderx1
        else:
            press_keys(hand_landmarker_result)

cap.release()
cv2.destroyAllWindows()