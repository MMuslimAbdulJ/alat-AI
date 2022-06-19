import cv2
from cvzone.FaceMeshModule import FaceMeshDetector
import pyfirmata


# Menangkap visualisasi dari webcam
cap = cv2.VideoCapture(3)

# Inisialisasi class FaceMeshDetector
detector = FaceMeshDetector(maxFaces=1)

# Inisialisasi breakcount_s, breakcount_y, counter_s, counter_y, state_s, state_y
breakcount_s, breakcount_y = 0, 0
counter_s, counter_y = 0, 0
state_s, state_y = False, False

# Inisisalisasi Arduino PIN 2
pin = 2
port = "/dev/ttyUSB0"
board = pyfirmata.Arduino(port)
board.digital[pin].write(1)

def peringatan(param1):
    if param1 == 1:
        board.digital[pin].write(0)
        board.pass_time(.1)
        board.digital[pin].write(1)
        board.pass_time(.1)
        board.digital[pin].write(0)
        board.pass_time(.1)
        board.digital[pin].write(1)
        board.pass_time(.1)
    else:
        board.digital[pin].write(1)


def alert1():
    cv2.rectangle(img, (700, 20), (1250, 80), (0, 0, 255), cv2.FILLED)
    cv2.putText(img, "AWAS MENGANTUK!!!", (710, 60),
                cv2.FONT_HERSHEY_PLAIN, 3, (255, 255, 255), 2)

def alert2():
    cv2.rectangle(img, (700, 20), (1250, 80), (0, 0, 255), cv2.FILLED)
    cv2.putText(img, "INDIKASI MENGANTUK!!!", (710, 60),
                cv2.FONT_HERSHEY_PLAIN, 3, (255, 255, 255), 2)

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)

    img, faces = detector.findFaceMesh(img, draw=False)

    if faces:
        face = faces[0]
        eyeLeft = [27, 23, 130, 243]  # up, down, left, right
        eyeRight = [257, 253, 463, 359]  # up, down, left, right
        mouth = [11, 16, 57, 287]  # up, down, left, right
        faceId = [27, 23, 130, 243, 257, 253, 463, 359, 11, 16, 57, 287]

        # menghitung rasio mata kiri
        eyeLeft_ver, _ = detector.findDistance(face[eyeLeft[0]], face[eyeLeft[1]])
        eyeLeft_hor, _ = detector.findDistance(face[eyeLeft[2]], face[eyeLeft[3]])
        eyeLeft_ratio = int((eyeLeft_ver/eyeLeft_hor)*100)
        # menghitung rasio mata kanan
        eyeRight_ver, _ = detector.findDistance(face[eyeRight[0]], face[eyeRight[1]])
        eyeRight_hor, _ = detector.findDistance(face[eyeRight[2]], face[eyeRight[3]])
        eyeRight_ratio = int((eyeRight_ver / eyeRight_hor) * 100)
        #menghitung rasio mulut
        mouth_ver, _ = detector.findDistance(face[mouth[0]], face[mouth[1]])
        mouth_hor, _ = detector.findDistance(face[mouth[2]], face[mouth[3]])
        mouth_ratio = int((mouth_ver / mouth_hor) * 100)

        #menampilkan drawing
        cv2.rectangle(img, (30,20), (400,150), (255,0,0), cv2.FILLED)
        cv2.putText(img, f'UNPI Cianjur', (50, 60),
                    cv2.FONT_HERSHEY_PLAIN, 2, (255,255,255), 2)
        cv2.putText(img, f'Teknik Informatika', (50, 100),
                    cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 2)
        cv2.putText(img, f'Kelompok 5', (50, 140),
                    cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 2)

        cv2.rectangle(img, (30, 200), (350, 300), (0,0,255), cv2.FILLED)
        cv2.putText(img, f'Mengantuk: {counter_s}', (40, 240),
                    cv2.FONT_HERSHEY_PLAIN, 2, (0,0,0), 2)
        cv2.putText(img, f'Menguap: {counter_y}', (40, 280),
                    cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 0), 2)


        #pengkondisian mata
        if eyeLeft_ratio <= 50 and eyeRight_ratio <= 50:
            breakcount_s += 1
            if breakcount_s >= 30:
                alert1()
                if state_s == False:
                    counter_s += 1
                    board.digital[pin].write(0)
                    state_s = not state_s
        else:
            breakcount_s = 0
            if state_s:
                board.pass_time(1)
                board.digital[pin].write(1)
                state_s = not state_s

        #pengkondisian mulut
        if mouth_ratio > 50:
            breakcount_y += 1
            if breakcount_y >= 20:
                alert2()
                if state_y == False:
                    counter_y += 1
                    # board.digital[pin].write(0)
                    peringatan(1)
                    state_y = not state_y
        else:
            breakcount_y = 0
            if state_y:
                peringatan(0)
                # board.pass_time(1)
                # board.digital[pin].write(1)
                state_y = not state_y

        for id in faceId:
            cv2.circle(img,face[id], 5, (0,255,0), cv2.FILLED)


    cv2.imshow("Pengantar A.I -- M Muslim Abdul J", img)
    cv2.waitKey(1)