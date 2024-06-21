import sys
import tkinter as tk                       
from tkinter import messagebox             
import cv2                                 
import os                                  
from PIL import Image                      
import numpy as np                         
import mysql.connector
import time
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QProgressBar, QLabel, QFrame, QHBoxLayout, QVBoxLayout
from PyQt5.QtCore import Qt, QTimer

class SplashScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Spash Screen Example')
        self.setFixedSize(1100, 500)
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.counter = 0
        self.n = 300 # total instance

        self.initUI()

        self.timer = QTimer()
        self.timer.timeout.connect(self.loading)
        self.timer.start(30)

    def initUI(self):
        layout = QVBoxLayout()
        self.setLayout(layout)

        self.frame = QFrame()
        layout.addWidget(self.frame)

        self.labelTitle = QLabel(self.frame)
        self.labelTitle.setObjectName('LabelTitle')

        # center labels
        self.labelTitle.resize(self.width() - 10, 150)
        self.labelTitle.move(0, 40) # x, y
        self.labelTitle.setText('Face Recognition System')
        self.labelTitle.setAlignment(Qt.AlignCenter)

        self.labelDescription = QLabel(self.frame)
        self.labelDescription.resize(self.width() - 10, 50)
        self.labelDescription.move(0, self.labelTitle.height())
        self.labelDescription.setObjectName('LabelDesc')
        self.labelDescription.setText('<strong>Loading...</strong>')
        self.labelDescription.setAlignment(Qt.AlignCenter)

        self.progressBar = QProgressBar(self.frame)
        self.progressBar.resize(self.width() - 200 - 10, 50)
        self.progressBar.move(100, self.labelDescription.y() + 130)
        self.progressBar.setAlignment(Qt.AlignCenter)
        self.progressBar.setFormat('%p%')
        self.progressBar.setTextVisible(True)
        self.progressBar.setRange(0, self.n)
        self.progressBar.setValue(20)

        self.labelLoading = QLabel(self.frame)
        self.labelLoading.resize(self.width() - 10, 50)
        self.labelLoading.move(0, self.progressBar.y() + 70)
        self.labelLoading.setObjectName('LabelLoading')
        self.labelLoading.setAlignment(Qt.AlignCenter)
        self.labelLoading.setText('By:- ASHISH☺...')

    def loading(self):
        self.progressBar.setValue(self.counter)

        if self.counter == int(self.n * 0.3):
            self.labelDescription.setText('<strong>Loading Modules...</strong>')
        elif self.counter == int(self.n * 0.6):
            self.labelDescription.setText('<strong>Launching Application...</strong>')
        elif self.counter >= self.n:
            self.timer.stop()
            self.close()

            time.sleep(1)

            self.myApp = MyApp()
            self.myApp.show()

        self.counter += 1

class MyApp(QWidget):
    def __init__(self):
        window = tk.Tk()
        window.title("Face Recognition system")

        window.config(background= "gray")

        l1 = tk.Label(window, text="Name",bg="gray", font=("Algerian",20),fg="white")
        l1.grid(column=0, row=0)
        t1 = tk.Entry(window, width=50, bd=5)
        t1.grid(column=1, row=0)

        l2 = tk.Label(window, text="Age", font=("Algerian",20),fg="white",bg="gray")
        l2.grid(column=0, row=1)
        t2 = tk.Entry(window, width=50, bd=5)
        t2.grid(column=1, row=1)

        l3 = tk.Label(window, text="Address", font=("Algerian",20),fg="white",bg="gray")
        l3.grid(column=0, row=2)
        t3 = tk.Entry(window, width=50, bd=5)
        t3.grid(column=1, row=2)

        def train_classifier():
            mydb=mysql.connector.connect(host="localhost", user="root", passwd="", database="face_reco_user")
            mycursor=mydb.cursor()
            mycursor.execute("SELECT * from user_Table")
            myresult=mycursor.fetchall()
            id1=0
            for x in myresult:
                id1+=1
            if(id1==0):
                    messagebox.showinfo('Result',"Please Generate Dataset Before Training!!")
            else:
                data_dir="C:/Users/Lenovo/OneDrive/Desktop/FRS/data/"
                path = [os.path.join(data_dir, f) for f in os.listdir(data_dir)]
        
                faces = []
                ids = []
        
                for image in path:
                    img = Image.open(image).convert('L')#convert to grayscale
                    imageNp = np.array(img, 'uint8')
                    id = int(os.path.split(image)[1].split(".")[1])
                    
                    faces.append(imageNp)
                    ids.append(id)
                    
                ids = np.array(ids)
                
                # Train and save classifier
                clf = cv2.face.LBPHFaceRecognizer_create()
                clf.train(faces,ids)
                clf.write("classifier.xml")
                messagebox.showinfo('Result','Training Dataset Completed')
##############################################################################
        b1 = tk.Button(window, text="Training", font=("Algerian",20),bg="orange",fg="black",command=train_classifier)
        b1.grid(column=0, row=4)
###############################################################################
        def detect_face():
            mydb=mysql.connector.connect(host="localhost", user="root", passwd="", database="face_reco_user")
            mycursor=mydb.cursor()
            mycursor.execute("SELECT * from user_Table")
            myresult=mycursor.fetchall()
            id1=0
            for x in myresult:
                id1+=1
            if(id1==0):
                    messagebox.showinfo('Result',"Please Generate and Train Dataset Before Detection!!")
            else:
                messagebox.showinfo('Result',"Starting Face Detection, to exit press Enter(once you are in detection screen)!!")
                def draw_boundary(img, classifier, scaleFactor, minNeighbors, color, text, clf):
                    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                    features = classifier.detectMultiScale(gray_img, scaleFactor, minNeighbors)
                    for (x,y,w,h) in features:
                        cv2.rectangle(img, (x,y), (x+w,y+h), color, 2 )

                        id, pred = clf.predict(gray_img[y:y+h,x:x+w])
                        confidence = int(100*(1-pred/300))

                        mydb= mysql.connector.connect(host="localhost", user="root", passwd="",database="face_reco_user")
                        mycursor = mydb.cursor()

                        mycursor.execute("select name from user_Table where id="+str(id))
                        s=mycursor.fetchone()
                        s=''+''.join(s)

                        if confidence>80:
                            cv2.putText(img, s, (x,y-5), cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 1, cv2.LINE_AA)
                        else:
                            cv2.putText(img, "UNKNOWN", (x,y-5), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,0,255), 1, cv2.LINE_AA)
                    return img
                # loading classifier

                faceCascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

                clf = cv2.face.LBPHFaceRecognizer_create()
                clf.read("classifier.xml")

                video_capture = cv2.VideoCapture(0)
                while True:
                    ret, img = video_capture.read()
                    img = draw_boundary(img, faceCascade, 1.3, 6, (255,255,255), "Face", clf)
                    cv2.imshow("face Detection", img)
        
                    if cv2.waitKey(1)==13:
                        break
                video_capture.release()
                cv2.destroyAllWindows()

                        
#######################################################################################
        b2 = tk.Button(window, text="Detect the faces", font=("Algerian",20), bg="green", fg="white",command=detect_face)
        b2.grid(column=1, row=4)
#######################################################################################
        def generate_dataset():
            if(t1.get()=="" or t2.get()=="" or t3.get()==""):
                messagebox.showinfo('Result',"Please fill all three fields !!XOX!!")
            else:
                messagebox.showinfo('Result',"Initiating Dataset Generation, place your face in front of camera to get started!!")
                mydb=mysql.connector.connect(host="localhost", user="root", passwd="", database="face_reco_user")
                mycursor=mydb.cursor()
                mycursor.execute("SELECT * from user_Table")
                myresult=mycursor.fetchall()
                id=1
                for x in myresult:
                    id+=1
                sql="insert into user_Table(id,Name,Age,Address) values(%s, %s, %s, %s)"
                val= (id, t1.get(), t2.get(), t3.get())
                mycursor.execute(sql,val)
                mydb.commit()

                face_classifier = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
                def face_cropped(img):
                    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
                    faces = face_classifier.detectMultiScale(gray, 1.3, 5)
                    # scaling factor = 1.3
                    # minimum neighbor = 5
                    if faces is ():
                        return None
                    for (x,y,w,h) in faces:
                        cropped_face = img[y:y+h,x:x+w]
                    return cropped_face
                cap = cv2.VideoCapture(0)
                img_id = 0
                while True:
                    ret, frame = cap.read()
                    if face_cropped(frame) is not None:
                        img_id+=1
                        face = cv2.resize(face_cropped(frame), (300,300))
                        face = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)
                        file_name_path = "data/user."+str(id)+"."+str(img_id)+".jpg"
                        cv2.imwrite(file_name_path, face)
                        cv2.putText(face, str(img_id), (50,50), cv2.FONT_HERSHEY_COMPLEX, 1, (0,255,0), 2)
                        
                        cv2.imshow("Cropped face", face)
                    if cv2.waitKey(1)==13 or int(img_id)==200: #13 is the ASCII character of Enter
                        break
                cap.release()
                cv2.destroyAllWindows()
                messagebox.showinfo('Result','Generating Dataset Completed..!!')
###################################################################################

        b3 = tk.Button(window, text="Generate dataset", font=("Algerian",20), bg="orange", fg="black", command=generate_dataset)
        b3.grid(column=2, row=4)

###################################################################################

        window.geometry("800x200")
        window.mainloop()

######################################################################################

if __name__ == '__main__':
    # don't auto scale when drag app to a different monitor.
    # QApplication.setAttribute(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    
    app = QApplication(sys.argv)
    app.setStyleSheet('''
        #LabelTitle {
            font-size: 60px;
            color: #93deed;
        }

        #LabelDesc {
            font-size: 30px;
            color: #c2ced1;
        }

        #LabelLoading {
            font-size: 30px;
            color: #e8e8eb;
        }

        QFrame {
            background-color: #2F4454;
            color: rgb(220, 220, 220);
        }

        QProgressBar {
            background-color: #DA7B93;
            color: rgb(200, 200, 200);
            border-style: none;
            border-radius: 10px;
            text-align: center;
            font-size: 30px;
        }

        QProgressBar::chunk {
            border-radius: 10px;
            background-color: qlineargradient(spread:pad x1:0, x2:1, y1:0.511364, y2:0.523, stop:0 #1C3334, stop:1 #376E6F);
        }
    ''')
    
    splash = SplashScreen()
    splash.show()

    try:
        sys.exit(app.exec_())
    except SystemExit:
        print('Closing Window...')

###################################################################################
