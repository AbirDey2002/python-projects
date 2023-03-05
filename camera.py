#importing modules

import cv2
import time
import datetime
import smtplib, ssl

# setting up server to send email to designated address as an emergency alert

port = 465  # For SSL
password = #enter your password here, for the account that will send the alert

# Create a secure SSL context
context = ssl.create_default_context()

with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
    server.login("my@gmail.com", password)

sender_email = "my@gmail.com"
receiver_email = "your@gmail.com"
message = """\
Subject: Hi there

This message is an alert sent from Cam1."""

#You can choose the camera you want you use if you have multiple camera modules in your PC
#For Camera option 1 - 0, for Camera option 2 - 1 ...

cap = cv2.VideoCapture(0)   

#face and body detection classifier ...

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
body_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_fullbody.xml")

"""
variables with set values that will change on a certain condition
   - detection will be true if face or body is detected
   - if detection is true, timer_started will be true too
   - detection_stopped_time will be recorded everytime detection stops 
     for saving the mp4 file with the date and time name
"""
# code by Abir Dey

detection = False
detection_stopped_time = None
timer_started = False
SECONDS_TO_RECORD_AFTER_DETECTION = 5

#Video settings - Frame size and file format

frame_size = (int(cap.get(3)), int(cap.get(4)))
fourcc = cv2.VideoWriter_fourcc(*"mp4v")

while True:

    # reading every frame - keep in mind this is a GPU induced program, it may be slow on low end devices

    _, frame = cap.read()

    # converting the frames into grayscale for detection using cascadeClassifier

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    bodies = face_cascade.detectMultiScale(gray, 1.3, 5)

    '''
    Let me explain how this is exactly working -

       - As the classifier works, it just identifies if there is a face or not

       - If there is a face, it returns 1 else 0

       - Same for bodies, 1 for positive and 0 for negative

       - If there is a face or body, timer starts if it was not already

       - If there is neither a face, nor a body, the timer stops if not already 

       - That's it, four conditions :

               * Start if not started

               * Continue if started

               * Stop if not stopped

               * Keep scanning if stopped

    '''
    
    if len(faces) + len(bodies) > 0:
        if detection:
            timer_started = False
        else:
            detection = True

            # current time recorded for saving the mp4 file with the respective name 

            current_time = datetime.datetime.now().strftime("%d-%m-%Y-%H-%M-%S")
            out = cv2.VideoWriter(                                          
                f"{current_time}.mp4", fourcc, 20, frame_size)
            print("Started Recording!") 
    elif detection:
        if timer_started:
            if time.time() - detection_stopped_time >= SECONDS_TO_RECORD_AFTER_DETECTION:
                detection = False
                timer_started = False
                out.release()
                print('Stop Recording!')
        else:
            timer_started = True
            detection_stopped_time = time.time()

    if detection:
        out.write(frame)

    for (x, y, width, height) in faces:
        if (width*height >= 22550):
            cv2.rectangle(frame, (x, y), (x + width, y + height), (255, 0, 0), 3)
            
            ''' using our setup server to send the alert when the face area is more than 22550 pixels
                   - Face area suggests how close the person is to the camera module
                   - The threshold are is upto the user, when used under practical conditions, 
                     we found that 22550 px was the perfect threshold
            
            '''
            
            server.sendmail(sender_email, receiver_email, message)

        else:
            cv2.rectangle(frame, (x, y), (x + width, y + height), (0, 255, 0), 3)


    

    cv2.imshow("Camera", frame)

    # The program runs until q is pressed, this being the exit key
    
    if cv2.waitKey(1) == ord('q'):
        break

#relesing resources and destroying all cv2 windows

out.release()
cap.release()
cv2.destroyAllWindows()


'''

Note - Make sure to use a PC module that has a GPU, preferably dedicated GPU
     - Don't share your mail password with anyone
     - You might not recieve the mail as alert as e-mails like this are most likely get classified into spam or
       get blocked as they are from unreliable source - being the smtp server
     - You need to go into the settings and disable some firewalls and accept e-mails from unreliable sources
       although it is not adviced to do so. make sure to revert back the changes later
     - modules required - cv2, datetime, time, smtplib, ssl
     - hardware - camera module - Prefarably dedicated

'''
