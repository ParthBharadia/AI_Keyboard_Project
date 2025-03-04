from cvzone.HandTrackingModule import HandDetector
import cv2
from time import sleep
from pynput.keyboard import Controller

cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

detector = HandDetector(detectionCon=0.8)

keys = [["Q","W","E","R","T","Y","U","I","O","P"],
        ["A","S","D","F","G","H","J","K","L",";"],
        ["Z","X","C","V","B","N","M",",",".","/"]]

finalText = ""

keyboard = Controller()

def drawALL(img,buttonList):
    for button in buttonList:
        x, y = button.pos
        w,h = button.size
        cv2.rectangle(img,button.pos,(x+w,y+h), (255, 255, 0), cv2.FILLED)
        cv2.putText(img, button.text, (x + 20, y + 65), cv2.FONT_HERSHEY_PLAIN,
                    2, (255, 255, 255), 3)
    return img


class Button:
    def __init__(self,pos,text,size=[85,85]):
        self.pos = pos
        self.size = size
        self.text = text


buttonList = []
for i in range(len(keys)):
    for j, key in enumerate(keys[i]):
        buttonList.append(Button([100 * j + 50, 100 * i + 50], key))

while True:
    success, img = cap.read()
    hands, img = detector.findHands(img, draw=True)  # Returns a list of hands

    lmList = []

    if hands:
        for hand in hands:
            lmList = hand["lmList"]  # List of 21 landmark points
            bbox = hand["bbox"]  # Bounding box info (x, y, w, h)
            center = hand["center"]  # Center of the hand

            print(f"Landmarks: {lmList}")
            print(f"BBox: {bbox}, Center: {center}")

    img = drawALL(img, buttonList)

    if lmList:
        for button in buttonList:
            x,y = button.pos
            w,h = button.size

            if x < lmList[8][0] < x+w and y < lmList[8][1] < y+h:
                cv2.rectangle(img,(x-5,y-5), (x + w+5, y + h+5), (175, 175,0), cv2.FILLED)
                cv2.putText(img, button.text, (x + 20, y + 65), cv2.FONT_HERSHEY_PLAIN,
                            4, (255, 255, 255), 4)

                if len(lmList) > 12:
                    x1, y1 = lmList[8][:2]  # Extract only (x, y)
                    x2, y2 = lmList[12][:2]  # Extract only (x, y)

                    l,_,_ = detector.findDistance((x1,y1),(x2,y2),img)
                    print(l)

                    if l < 40:
                        keyboard.press(button.text)
                        cv2.rectangle(img, button.pos, (x + w, y + h), (0, 255, 0), cv2.FILLED)
                        cv2.putText(img, button.text, (x + 20, y + 65), cv2.FONT_HERSHEY_PLAIN,
                                    4, (255, 255, 255), 4)
                        finalText += button.text
                        sleep(0.15)

    cv2.rectangle(img,(50,350), (900,450), (175, 0, 175), cv2.FILLED)
    cv2.putText(img,finalText, (60,430), cv2.FONT_HERSHEY_PLAIN,
                5, (255, 255, 255), 5)


    cv2.imshow("Image", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break