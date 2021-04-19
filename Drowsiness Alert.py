import cv2
import playsound
import winsound
from twilio.rest import Client


def drowsiness_alert():
    eye_cascade = cv2.CascadeClassifier("haarcascade_eye.xml")
    video = cv2.VideoCapture(0)
    a = 0
    frame_counter = 0
    while True:
        a += 1
        check, frame = video.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        eyes = eye_cascade.detectMultiScale(gray, scaleFactor=1.100009,  minNeighbors=10)
        for x, y, w, h in eyes:
            frame = cv2.rectangle(gray, (x, y), (x+w, y+h), (0, 255, 0), 3)

        if gray.all() < 0.3:
            cv2.putText(frame, "Driving", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        else:
            frame_counter += 1
            if frame_counter > 30:
                cv2.putText(frame, "Sleeping", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                playsound.playsound("danger.mp3")
                winsound.Beep(1000, 2000)
                frame_counter = 0
                cv2.imwrite('sleeping.png', frame)
                send_msg()
        cv2.imshow("Drowsiness Detector", frame)
        key = cv2.waitKey(30)
        if key == ord("q"):
            break
        print(frame)

    print(a)


def send_msg():
    account_sid = "Twilio account sid"
    auth_token = "Twilio account auth token"
    client = Client(account_sid, auth_token)
    client.messages.create(
        body="Driver is Sleeping",
        to="Number to which you want to send messages",
        from_="Twilio number generated for your account")

drowsiness_alert()
cv2.destroyAllWindows()
