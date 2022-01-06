import cv2 #0.8.7
from cvzone.HandTrackingModule import HandDetector #1.4.1
import time
import pyautogui
# ---------------------------------------------------------

cap= cv2.VideoCapture(0)
cap.set(3,1280)
cap.set(4,720)

# -----------------------------------------------------------

detector = HandDetector(detectionCon=0.8)
previousTime=0
currentTime=0
keys = [["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P"],
        ["A", "S", "D", "F", "G", "H", "J", "K", "L", ";"],
        ["Z", "X", "C", "V", "B", "N", "M", ",", ".", "/"]]

finaltext=""

# ------------------------------------------------------------
    
def drawALL(img,buttonList):
    for button in buttonList:
        x,y=button.pos
        w,h=button.size
        cv2.rectangle(img,button.pos,(x+w,y+h),(255,0,255),cv2.FILLED)
        cv2.putText(img,button.text,(x+20,y+65),cv2.FONT_HERSHEY_PLAIN,4,(255,255,255),4)
    return img
    

class Button():
    def __init__(self, pos,text,size=[85,85]):
        self.pos=pos
        self.size=size
        self.text=text
        
    
        # return img
buttonList=[]
# print(len(keys))       
for i in range(len(keys)):
    for x, key in enumerate(keys[i]):
        buttonList.append(Button([100 * x + 50, 100*i+50],key))       
        
   
while True:
    _,img= cap.read()
    
    img = detector.findHands(img)
    lmList,bboxInfo = detector.findPosition(img)
    # img = cv2.flip(img,1)
    img= drawALL(img,buttonList)
   
    if lmList:
        for button in buttonList:
            x,y=button.pos
            w,h=button.size
            
            if x<lmList[8][0]<x+w and y<lmList[8][1]<y+h:
                cv2.rectangle(img,button.pos,(x+w,y+h),(255,140,255),cv2.FILLED)
                cv2.putText(img,button.text,(x+20,y+65),cv2.FONT_HERSHEY_PLAIN,4,(255,255,255),4)
            
                l, _, _= detector.findDistance(8,12,img,draw=False)
                print(l)
                
                if l<60:
                    pyautogui.press(button.text)
                    time.sleep(0.15)
                    cv2.rectangle(img,button.pos,(x+w,y+h),(0,255,0),cv2.FILLED)
                    cv2.putText(img,button.text,(x+20,y+65),cv2.FONT_HERSHEY_PLAIN,4,(255,255,255),4)
                    finaltext += button.text
    cv2.rectangle(img,(50,350),(700,450),(175,0,175),cv2.FILLED)
    cv2.putText(img,finaltext,(60,425),cv2.FONT_HERSHEY_PLAIN,4,(255,255,255),4)
    
                
        
    
    # Calculating the FPS
    currentTime = time.time()
    fps = 1 / (currentTime-previousTime)
    previousTime = currentTime
    
    # Displaying FPS on the image
    cv2.putText(img, str(int(fps))+" FPS", (10, 70), cv2.FONT_HERSHEY_COMPLEX, 1, (0,255,0), 2)
    cv2.imshow("Image",img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()     