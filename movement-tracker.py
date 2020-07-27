import cv2
import keyboard

def detect_nose(img, face_cascade):
    gray_img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    features = face_cascade.detectMultiScale(gray_img, 1.1, 8)
    nose_cords = []
    for (x, y ,w, h) in features:
        #cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
        #cv2. circle(img, ((2*x+w)//2, (2*y+h)//2), 10, (0, 255, 0), 2)
        nose_cords = ((2*x+w)//2, (2*y+h)//2)
    return img, nose_cords

def draw_controller(img, cords):
    size = 30
    x1 = cords[0] - size
    y1 = cords[1] - size
    x2 = cords[0] + size
    y2 = cords[1] + size
    cv2.circle(img, cords, size, (255, 0, 0), 2)
    return [(x1, y1), (x2, y2)]

def keyboard_events(nose_cords, cords, cmd):
    try:
        [(x1, y1), (x2, y2)] = cords
        xc, yc = nose_cords
    except Exception as e:
        print(e)
        return
    if xc < x1:
        cmd = "left"
    elif xc > x2:
        cmd = "right"
    elif yc < y1:
        cmd = "up"
    elif yc > y2:
        cmd = "down"
    if cmd:
        print(cmd, "\n")
        keyboard.press_and_release(cmd)
    return img, cmd

def reset_press_flag(nose_cords, cords, cmd):
    try:
        [(x1, y1), (x2, y2)] = cords
        xc, yc = nose_cords
    except:
        return True, cmd
    if x1<xc<x2 and y1<yc<y2:
        return True, None
    return False, cmd

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
cap = cv2.VideoCapture(0 + cv2.CAP_DSHOW)
fourcc = cv2.VideoWriter_fourcc(*'XVID')
width = cap.get(3)
height = cap.get(4)
press_flag = False
cmd = ""
while cap.isOpened():
    _, img = cap.read()
    img = cv2.flip(img, 1)
    img, nose_cords = detect_nose(img, face_cascade)
    cv2.putText(img, cmd, (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 1, cv2.LINE_AA)
    cords = draw_controller(img, (int(width/2), int(height/2)))
    if press_flag and len(nose_cords):
        img, cmd = keyboard_events(nose_cords, cords, cmd)
    press_flag, cmd = reset_press_flag(nose_cords, cords, cmd)
    cv2.imshow("something", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()