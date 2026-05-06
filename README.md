# camnithm

# !!! this is currently in WIP and does not work !!!

## Simple chunithm controller with opencv + hand detection

---

### Some Links:

#### install the hand_landmarker.task model from here:
> https://ai.google.dev/edge/mediapipe/solutions/vision/hand_landmarker?hl=zh-tw

#### hand_landmarker documentations:
> https://ai.google.dev/edge/mediapipe/solutions/vision/hand_landmarker/python?hl=zh-tw

#### main code is copied from here:
> https://steam.oxxostudio.tw/category/python/ai/ai-mediapipe-2023-hand.html

#### Umiguri:
> https://umgr.inonote.jp/en/

---

### Installation Steps

#### 1. Install [umiguri](https://umgr.inonote.jp/en/) (Chunithm Simulator)

#### 2. Install dependencies

```
pip install opencv-python mediapipe pydirectinput
```

#### 3. Install [hand_landmarker.task](https://ai.google.dev/edge/mediapipe/solutions/vision/hand_landmarker?hl=zh-tw) and put it in the folder

#### 4. Setup webcam correctly (persumably right above your hands)

#### 5. Change some settings or code if needed

#### 6. Change offset in game to match camera offset (perferably as late as possible to combat the delay)

#### 7. Run main.py

---

### How to Play

#### 1. Press space to initialization, put both your hands where you want the slider to be (with the pinky being the sides of the slider)

#### 2. Wait for 10 seconds, it should automatically start

#### 3. Start playing, press space on the opencv window to stop or start

#### 4. Press esc on the opencv window to quit