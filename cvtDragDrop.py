import sys
from ctypes import alignment
from glob import glob
import time
from tkinter import LEFT, TOP, VERTICAL
from turtle import left, right
import logging
import cv2
from PyQt5 import QtCore
from PyQt5.QtCore import QEvent, QObject, Qt, QThread, QTimer, pyqtSignal
from PyQt5.QtGui import QFont, QIcon, QImage, QPalette, QPixmap,QCursor

from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import (QApplication, QGridLayout, QLabel, QMainWindow,
                             QScrollArea, QSizePolicy, QWidget)

from jsonOku import *
from jsonYaz import *
import threading
import cvlog as log
from PyQt5.QtWidgets import QApplication, QHBoxLayout, QWidget, QPushButton
from PyQt5.QtCore import Qt, QMimeData
from PyQt5.QtGui import QDrag, QPixmap
from PyQt5.QtWidgets import QWidget
import webbrowser as wb
from datetime import datetime
import codecs
import resources

Camera_Direct=""
Camera_İp=""
Camera_Name=""
Camera_Model=""

global combo_List
global combo_List2
global lastJsonList

global websiteLink
websiteLink=""
global website1
website1=""
global text_DragDop
text_DragDop=""

global comboboxText1
global comboboxText2
global comboboxText3
global comboboxText4
global comboboxText5
global comboboxText6
global comboboxText7
global comboboxText8
global comboboxText9
global comboboxText10
global comboboxText11
global comboboxText12

global combobox1
global combobox2
global combobox3
global combobox4
global combobox5
global combobox6
global combobox7
global combobox8
global combobox9
global combobox10
global combobox11
global combobox12

class DragButton(QLineEdit):

    def mouseMoveEvent(self, e):

        if e.buttons() == Qt.LeftButton:
            drag = QDrag(self)
            mime = QMimeData()
            drag.setMimeData(mime)
           
            pixmap = QPixmap(self.size())
            self.render(pixmap)
            drag.setPixmap(pixmap)
            
            drag.exec_(Qt.MoveAction)



class CaptureIpCameraFramesWorker(QThread):
    # Signal emitted when a new image or a new frame is ready.
    ImageUpdated = pyqtSignal(QImage)
    simple_format=  '%(asctime)s - %(levelname)s - %(name)s - %(message)s'  
    detail_format ='%(asctime)s - %(levelname)s - %(funcName)s - %(lineno)d - %(message)s'   
    logging.basicConfig(
      filename='file.txt',
      filemode='a',
      format=detail_format,
      level=logging.DEBUG
) 
    
    def __init__(self, url) -> None:
        super(CaptureIpCameraFramesWorker, self).__init__()
        # Declare and initialize instance variables.
        self.url = url
        self.__thread_active = True
        self.fps = 0
        self.__thread_pause = False
        self.thread=QThread()

        
    def run(self) -> None:
        # Capture video from a network stream.
        global Camera_1,Camera_2,Camera_3,Camera_4, Camera_5, Camera_6, Camera_7, Camera_8, Camera_9, Camera_10, Camera_11, Camera_12
        cap = cv2.VideoCapture(self.url, cv2.CAP_ANY)

       
        #cap = cv2.VideoCapture(self.url)
        # log.image(log.Level.ERROR, cap)
        # Get default video FPS.
        self.fps = cap.get(cv2.CAP_PROP_FPS)
        # cap.set(cv2.CV_CAP_PROP_FRAME_WIDTH,640)
        # cap.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT,480)
        # print("FPS",self.url)
        # print("CV_CAP_PROP_FRAME_WIDTH: '{}'".format(cap.get(cv2.CAP_PROP_FRAME_WIDTH)))
        # print("CV_CAP_PROP_FRAME_HEIGHT : '{}'".format(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
        # print("CAP_PROP_FPS : '{}'".format(cap.get(cv2.CAP_PROP_FPS)))
        # print("CAP_PROP_POS_MSEC : '{}'".format(cap.get(cv2.CAP_PROP_POS_MSEC)))
        # print("CAP_PROP_FRAME_COUNT  : '{}'".format(cap.get(cv2.CAP_PROP_FRAME_COUNT)))
        # print("CAP_PROP_BRIGHTNESS : '{}'".format(cap.get(cv2.CAP_PROP_BRIGHTNESS)))
        # print("CAP_PROP_CONTRAST : '{}'".format(cap.get(cv2.CAP_PROP_CONTRAST)))
        # print("CAP_PROP_SATURATION : '{}'".format(cap.get(cv2.CAP_PROP_SATURATION)))
        # print("CAP_PROP_HUE : '{}'".format(cap.get(cv2.CAP_PROP_HUE)))
        # print("CAP_PROP_GAIN  : '{}'".format(cap.get(cv2.CAP_PROP_GAIN)))
        # print("CAP_PROP_CONVERT_RGB : '{}'".format(cap.get(cv2.CAP_PROP_CONVERT_RGB)))

        # If video capturing has been initialized already.q
        try:
            if cap.isOpened():
                # print("CV_CAP_PROP_FRAME_WIDTH: '{}'".format(cap.get(cv2.CAP_PROP_FRAME_WIDTH)))
                # print("CV_CAP_PROP_FRAME_HEIGHT : '{}'".format(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
                # While the thread is active.
                while self.__thread_active:
                    try:
                        if not self.__thread_pause:
                            # Grabs, decodes and returns the next video frame.
                            ret, frame = cap.read()
                            # Get the frame height, width and channels.
                            height, width, channels = frame.shape
                            # Calculate the number of bytes per line.
                            bytes_per_line = width * channels
                            # If frame is read correctly.
                            if ret:
                               
                                # Convert image from BGR (cv2 default color format) to RGB (Qt default color format).
                                cv_rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                                cv2.rectangle(frame, (width-290,0), (width,20), color=(0,0,0), thickness=-1)
                                cv2.putText(frame, datetime.now().strftime('%H:%M:%S'), (width-16,37), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (255,255,255), lineType=cv2.LINE_AA)
                                # Convert the image to Qt format.
                                qt_rgb_image = QImage(cv_rgb_image.data, width, height, bytes_per_line, QImage.Format_RGB888)#Format_RGB888
                                # Scale the image.
                                
                                qt_rgb_image_scaled = qt_rgb_image.scaled(800,405,  Qt.KeepAspectRatio)  # 1280 720p 1080 720
                                # qt_rgb_image_scaled = qt_rgb_image.scaled(1920, 1080, Qt.KeepAspectRatio)
                                # Emit this signal to notify that a new image or frame is available.
                                
                                self.ImageUpdated.emit(qt_rgb_image_scaled)

                            
                            else:
                                cap = cv2.VideoCapture(self.url, cv2.CAP_ANY)


                               
                        else:
                            self.ImageUpdated.emit('stop')
                            logging.error("Kamera Baglantısı Koptuuuu")  
                    
                    except Exception as ex:
                        logging.error(ex,"Hata Basladı, Kamera dondu")

                        self.stop()
                        time.sleep(1)
                        self.start()

                        cap = cv2.VideoCapture(self.url, cv2.CAP_ANY)
                        self.__thread_active=True
                        print("Threadler basladıı")
                        self.__thread_pause=False
                        
                        logging.error("Hataya girdii, Tekrar Basladı")

            else:
                            
                resim = cv2.imread("images/camera1.png")
                (height, width, channels) = resim.shape
                                    
                bytes_per_line = width * channels
                    
                cv_rgb_image = cv2.cvtColor(resim, cv2.COLOR_BGR2RGB)        
                qt_rgb_image = QImage(cv_rgb_image.data, width, height, bytes_per_line, QImage.Format_RGB888)
                                
                qt_rgb_image_scaled = qt_rgb_image.scaled(640, 480, Qt.KeepAspectRatio)  # 1280 720p
                        
                self.ImageUpdated.emit(qt_rgb_image_scaled)
                
               
                

            # When everything done, release the video capture object.
            cap.release()
                # Tells the thread's event loop to exit with return code 0 (success).
            self.quit()
        except:
            print("İlk try girdi")
            resim = cv2.imread("images/camera.png")
            (height, width, channels) = resim.shape
                                
            bytes_per_line = width * channels
                
            cv_rgb_image = cv2.cvtColor(resim, cv2.COLOR_BGR2RGB)
                     
            qt_rgb_image = QImage(cv_rgb_image.data, width, height, bytes_per_line, QImage.Format_RGB888)
                            
            qt_rgb_image_scaled = qt_rgb_image.scaled(640, 480, Qt.KeepAspectRatio)  # 1280 720p
                    
            self.ImageUpdated.emit(qt_rgb_image_scaled)
            
            self.stop()
            time.sleep(1)
            self.start()

            cap = cv2.VideoCapture(self.url, cv2.CAP_ANY)
            self.__thread_active=True
            print("Threadler basladıı")
            self.__thread_pause=False
          
    def update_image(self):
        """Updates the image_label with a new opencv image"""
        
        self.stop()
        time.sleep(2)
        self.start()
        
        cap = cv2.VideoCapture(self.url, cv2.CAP_ANY)
        
        self.__thread_active=True
        print("Tekrar geldilerr")
        self.__thread_pause=False
       

    def stop(self) -> None:
        self.__thread_active = False

    def pause(self) -> None:
        self.__thread_pause = True

    def unpause(self) -> None:
        self.__thread_pause = False


class MainWindow(QMainWindow): 
    global combo_List
    global combo_List2
    global lastJsonList
    lastJsonList=[]
    global text_DragDop
    text_DragDop=""
    
    def __init__(self,) -> None:
        super(MainWindow, self).__init__()
        
        self.comboList1()
        self.comboList2()
        self.comboList3()
        self.comboList4()
        self.comboList5()
        self.comboList6()
        self.comboList7()
        self.comboList8()
        self.comboList9()
        self.comboList10()
        self.comboList11()
        self.comboList12()
        
        self.setAcceptDrops(True)
        
        self._createActions()
           

        
        lastİp_Data=JsonOku("veri.json")
        for i in lastİp_Data:
            lastJsonList.append(i)

        global combo_List
        combo_List=[]
        global combo_List2
        combo_List2=[]
        
        global combo_List3
        combo_List3=[]
     
        global combo_List_rtsp
        global comboLis_All
        combo_List_rtsp=[]
        comboLis_All=[]
        data=JsonOku("cam2.json")
        for i in data:

            btn=DragButton(i["cam_Name"])
            # btn.setText(str(i["cam_Name"][:13]))
            
            comboLis_All.append(i)
            combo_List3.append(i["cam_Name"])
            combo_List.append(btn.text())
            combo_List2.append(i["cam_ip"])
            combo_List_rtsp.append(i["cam_rtsp"])


        self.combobox1.addItems(combo_List3[:13])
        self.combobox2.addItems(combo_List3[:13])
        self.combobox3.addItems(combo_List3[:13])
        self.combobox4.addItems(combo_List3[:13])
        self.combobox5.addItems(combo_List3[:13])
        self.combobox6.addItems(combo_List3[:13])
        self.combobox7.addItems(combo_List3[13:])
        self.combobox8.addItems(combo_List3[13:])
        self.combobox9.addItems(combo_List3[13:])
        self.combobox10.addItems(combo_List3[13:])
        self.combobox11.addItems(combo_List3[13:])
        self.combobox12.addItems(combo_List3[13:])
        
         # Listenin son halini combobox lara atama
        self.combobox1.setCurrentText(lastJsonList[0])
        self.combobox2.setCurrentText(lastJsonList[1])
        self.combobox3.setCurrentText(lastJsonList[2])
        self.combobox4.setCurrentText(lastJsonList[3])
        self.combobox5.setCurrentText(lastJsonList[4])
        self.combobox6.setCurrentText(lastJsonList[5])
        self.combobox7.setCurrentText(lastJsonList[6])
        self.combobox8.setCurrentText(lastJsonList[7])
        self.combobox9.setCurrentText(lastJsonList[8])
        self.combobox10.setCurrentText(lastJsonList[9])
        self.combobox11.setCurrentText(lastJsonList[10])
        self.combobox12.setCurrentText(lastJsonList[11])
        
    
        
        cam_index1=combo_List.index(lastJsonList[0])
        rtsp_index1=combo_List_rtsp[cam_index1]
        
        cam_index2=combo_List.index(lastJsonList[1])
        rtsp_index2=combo_List_rtsp[cam_index2]
        
        cam_index3=combo_List.index(lastJsonList[2])
        rtsp_index3=combo_List_rtsp[cam_index3]
        
        cam_index4=combo_List.index(lastJsonList[3])
        rtsp_index4=combo_List_rtsp[cam_index4]
        
        cam_index5=combo_List.index(lastJsonList[4])
        rtsp_index5=combo_List_rtsp[cam_index5]
        
        cam_index6=combo_List.index(lastJsonList[5])
        rtsp_index6=combo_List_rtsp[cam_index6]
        
        cam_index7=combo_List.index(lastJsonList[6])
        rtsp_index7=combo_List_rtsp[cam_index7]
        
        cam_index8=combo_List.index(lastJsonList[7])
        rtsp_index8=combo_List_rtsp[cam_index8]
        
        cam_index9=combo_List.index(lastJsonList[8])
        rtsp_index9=combo_List_rtsp[cam_index9]
        
        cam_index10=combo_List.index(lastJsonList[9])
        rtsp_index10=combo_List_rtsp[cam_index10]
        
        cam_index11=combo_List.index(lastJsonList[10])
        rtsp_index11=combo_List_rtsp[cam_index11]
        
        cam_index12=combo_List.index(lastJsonList[11])
        rtsp_index12=combo_List_rtsp[cam_index12]
    
        self.url_1 = rtsp_index1
        # self.url_1 = ('rtsp://admin:a741953A@{}:554/udpstream').format(str(lastJsonList[0]),self)
        self.url_2 = rtsp_index2
        self.url_3 = rtsp_index3
        self.url_4 = rtsp_index4
        self.url_5 = rtsp_index5
        self.url_6 = rtsp_index6
        self.url_7 = rtsp_index7
        self.url_8 = rtsp_index8
        self.url_9 = rtsp_index9
        self.url_10 = rtsp_index10
        self.url_11 = rtsp_index11
        self.url_12 = rtsp_index12

        # popup = QMenu(self)
        
        # closeEvent = lambda QMouseEvent: popup.setParent(
        #     self.mousePressEvent_2(QMouseEvent)
        # )

        # Dictionary to keep the state of a camera. The camera state will be: Normal or Maximized.
        self.list_of_cameras_state = {}
        cursor = Qt.OpenHandCursor
        # Create an instance of a QLabel class to show camera 1.
        self.camera_1 = QLabel("METRO İSTANBUL ARGE",self)
        self.camera_1.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        self.camera_1.resize(QtCore.QSize(20,10))
        # self.camera_1.setFixedSize(800,480)
        self.camera_1.setScaledContents(True)
        self.camera_1.installEventFilter(self)
        self.camera_1.setObjectName("Camera_1")
        # self.camera_1.mousePressEvent=closeEvent
        self.list_of_cameras_state["Camera_1"] = "Normal"
        

        # Create an instance of a QScrollArea class to scroll camera 1 image.
        
        
        self.QScrollArea_1 = QScrollArea()
        self.QScrollArea_1.setBackgroundRole(QPalette.Dark)
        self.QScrollArea_1.setWidgetResizable(True)
        self.QScrollArea_1.setWidget(self.camera_1)
        self.QScrollArea_1.setFixedSize(763,265)
        self.QScrollArea_1.setCursor(cursor)
        self.QScrollArea_1.setStyleSheet('border : 1px solid green;')
        # self.QScrollArea_1.mousePressEvent=closeEvent


        

        
        

        # Create an instance of a QLabel class to show camera 2.
        self.camera_2 = QLabel("METRO İSTANBUL ARGE",self)
        self.camera_2.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        self.camera_2.setScaledContents(True)
        self.camera_2.installEventFilter(self)
        self.camera_2.setObjectName("Camera_2")
        self.list_of_cameras_state["Camera_2"] = "Normal"

        # Create an instance of a QScrollArea class to scroll camera 2 image.
        self.QScrollArea_2 = QScrollArea()
        self.QScrollArea_2.setBackgroundRole(QPalette.Dark)
        self.QScrollArea_2.setWidgetResizable(True)
        self.QScrollArea_2.setWidget(self.camera_2)
        self.QScrollArea_2.setFixedSize(762,265)
        self.QScrollArea_2.setCursor(cursor)
        self.QScrollArea_2.setStyleSheet('border : 1px solid green;')
        

        # Create an instance of a QLabel class to show camera 3.
        self.camera_3 = QLabel("METRO İSTANBUL ARGE",self)
        self.camera_3.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        self.camera_3.setScaledContents(True)
        self.camera_3.installEventFilter(self)
        self.camera_3.setObjectName("Camera_3")
        self.list_of_cameras_state["Camera_3"] = "Normal"

        # Create an instance of a QScrollArea class to scroll camera 3 image.
        self.QScrollArea_3 = QScrollArea()
        self.QScrollArea_3.setBackgroundRole(QPalette.Dark)
        self.QScrollArea_3.setWidgetResizable(True)
        self.QScrollArea_3.setWidget(self.camera_3)
        self.QScrollArea_3.setFixedSize(382,260)
        self.QScrollArea_3.setCursor(cursor)
        self.QScrollArea_3.setStyleSheet('border : 1px solid green;')

       

        # Create an instance of a QLabel class to show camera 4.
        self.camera_4 = QLabel("METRO İSTANBUL ARGE",self)
        self.camera_4.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        self.camera_4.setScaledContents(True)
        self.camera_4.installEventFilter(self)
        self.camera_4.setObjectName("Camera_4")
        self.list_of_cameras_state["Camera_4"] = "Normal"

        # Create an instance of a QScrollArea class to scroll camera 4 image.
        self.QScrollArea_4 = QScrollArea()
        self.QScrollArea_4.setBackgroundRole(QPalette.Dark)
        self.QScrollArea_4.setWidgetResizable(True)
        self.QScrollArea_4.setWidget(self.camera_4)
        self.QScrollArea_4.setFixedSize(382,260)
        self.QScrollArea_4.setCursor(cursor)
        self.QScrollArea_4.setStyleSheet('border : 1px solid green;')
    

        # Create an instance of a QLabel class to show camera 5.
        self.camera_5 = QLabel("METRO İSTANBUL ARGE",self)
        self.camera_5.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        self.camera_5.resize(QtCore.QSize(20,10))
        # self.camera_5.setFixedSize(800,480)
        self.camera_5.setScaledContents(True)
        self.camera_5.installEventFilter(self)
        self.camera_5.setObjectName("Camera_5")
        self.list_of_cameras_state["Camera_5"] = "Normal"

        # Create an instance of a QScrollArea class to scroll camera 5 image.
        
        
        self.QScrollArea_5 = QScrollArea()
        self.QScrollArea_5.setBackgroundRole(QPalette.Dark)
        self.QScrollArea_5.setWidgetResizable(True)
        self.QScrollArea_5.setWidget(self.camera_5)
        self.QScrollArea_5.setFixedSize(382,260)
        self.QScrollArea_5.setCursor(cursor)
        self.QScrollArea_5.setStyleSheet('border : 1px solid green;')
    
     

# Create an instance of a QLabel class to show camera 6.
        self.camera_6 = QLabel("METRO İSTANBUL ARGE",self)
        self.camera_6.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        self.camera_6.resize(QtCore.QSize(20,10))
        # self.camera_6.setFixedSize(800,480)
        self.camera_6.setScaledContents(True)
        self.camera_6.installEventFilter(self)
        self.camera_6.setObjectName("Camera_6")
        self.list_of_cameras_state["Camera_6"] = "Normal"

        # Create an instance of a QScrollArea class to scroll camera 6 image.        
        
        self.QScrollArea_6 = QScrollArea()
        self.QScrollArea_6.setBackgroundRole(QPalette.Dark)
        self.QScrollArea_6.setWidgetResizable(True)
        self.QScrollArea_6.setWidget(self.camera_6)
        self.QScrollArea_6.setFixedSize(380,260)
        self.QScrollArea_6.setCursor(cursor)
        self.QScrollArea_6.setStyleSheet('border : 1px solid green;')
      
      
        # Create an instance of a QLabel class to show camera 7.
        self.camera_7 = QLabel("METRO İSTANBUL ARGE",self)
        self.camera_7.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        self.camera_7.resize(QtCore.QSize(20,10))
        # self.camera_7.setFixedSize(800,480)
        self.camera_7.setScaledContents(True)
        self.camera_7.installEventFilter(self)
        self.camera_7.setObjectName("Camera_7")
        self.list_of_cameras_state["Camera_7"] = "Normal"

        # Create an instance of a QScrollArea class to scroll camera 7 image.
        
        
        self.QScrollArea_7 = QScrollArea()
        self.QScrollArea_7.setBackgroundRole(QPalette.Dark)
        self.QScrollArea_7.setWidgetResizable(True)
        self.QScrollArea_7.setWidget(self.camera_7)
        self.QScrollArea_7.setFixedSize(382,260)
        self.QScrollArea_7.setCursor(cursor)
        self.QScrollArea_7.setStyleSheet('border : 1px solid green;')
   
       
        # Create an instance of a QLabel class to show camera 8.
        self.camera_8 = QLabel("METRO İSTANBUL ARGE",self)
        self.camera_8.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        self.camera_8.resize(QtCore.QSize(20,10))
        # self.camera_8.setFixedSize(800,480)
        self.camera_8.setScaledContents(True)
        self.camera_8.installEventFilter(self)
        self.camera_8.setObjectName("Camera_8")
        self.list_of_cameras_state["Camera_8"] = "Normal"

         # Create an instance of a QScrollArea class to scroll camera 8 image.      
        self.QScrollArea_8 = QScrollArea()
        self.QScrollArea_8.setBackgroundRole(QPalette.Dark)
        self.QScrollArea_8.setWidgetResizable(True)
        self.QScrollArea_8.setWidget(self.camera_8)
        self.QScrollArea_8.setFixedSize(382,260)
        self.QScrollArea_8.setCursor(cursor)
        self.QScrollArea_8.setStyleSheet('border : 1px solid green;')
 
        self.camera_9 = QLabel("METRO İSTANBUL ARGE",self)
        self.camera_9.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        self.camera_9.resize(QtCore.QSize(20,10))
        # self.camera_8.setFixedSize(800,480)
        self.camera_9.setScaledContents(True)
        self.camera_9.installEventFilter(self)
        self.camera_9.setObjectName("Camera_9")
        self.list_of_cameras_state["Camera_9"] = "Normal"

         # Create an instance of a QScrollArea class to scroll camera 8 image.      
        self.QScrollArea_9 = QScrollArea()
        self.QScrollArea_9.setBackgroundRole(QPalette.Dark)
        self.QScrollArea_9.setWidgetResizable(True)
        self.QScrollArea_9.setWidget(self.camera_9)
        self.QScrollArea_9.setFixedSize(382,260)
        self.QScrollArea_9.setCursor(cursor)
        self.QScrollArea_9.setStyleSheet('border : 1px solid green;')
 
      
        self.camera_10 = QLabel("METRO İSTANBUL ARGE",self)
        self.camera_10.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        self.camera_10.resize(QtCore.QSize(20,10))
        # self.camera_8.setFixedSize(800,480)
        self.camera_10.setScaledContents(True)
        self.camera_10.installEventFilter(self)
        self.camera_10.setObjectName("Camera_10")
        self.list_of_cameras_state["Camera_10"] = "Normal"

         # Create an instance of a QScrollArea class to scroll camera 8 image.      
        self.QScrollArea_10 = QScrollArea()
        self.QScrollArea_10.setBackgroundRole(QPalette.Dark)
        self.QScrollArea_10.setWidgetResizable(True)
        self.QScrollArea_10.setWidget(self.camera_10)
        self.QScrollArea_10.setFixedSize(380,260)
        self.QScrollArea_10.setCursor(cursor)
        self.QScrollArea_10.setStyleSheet('border : 1px solid green;')
  
        self.camera_11 = QLabel("METRO İSTANBUL ARGE",self)
        self.camera_11.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        self.camera_11.resize(QtCore.QSize(20,10))
        # self.camera_8.setFixedSize(800,480)
        self.camera_11.setScaledContents(True)
        self.camera_11.installEventFilter(self)
        self.camera_11.setObjectName("Camera_11")
        self.list_of_cameras_state["Camera_11"] = "Normal"

         # Create an instance of a QScrollArea class to scroll camera 8 image.      
        self.QScrollArea_11 = QScrollArea()
        self.QScrollArea_11.setBackgroundRole(QPalette.Dark)
        self.QScrollArea_11.setWidgetResizable(True)
        self.QScrollArea_11.setWidget(self.camera_11)
        self.QScrollArea_11.setFixedSize(763,270)
        self.QScrollArea_11.setCursor(cursor)
        self.QScrollArea_11.setStyleSheet('border : 1px solid green;')
    
        self.camera_12 = QLabel("METRO İSTANBUL ARGE",self)
        self.camera_12.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        self.camera_12.resize(QtCore.QSize(20,10))
        # self.camera_8.setFixedSize(800,480)
        self.camera_12.setScaledContents(True)
        self.camera_12.installEventFilter(self)
        self.camera_12.setObjectName("Camera_12")
        self.list_of_cameras_state["Camera_12"] = "Normal"

         # Create an instance of a QScrollArea class to scroll camera 8 image.      
        self.QScrollArea_12 = QScrollArea()
        self.QScrollArea_12.setBackgroundRole(QPalette.Dark)
        self.QScrollArea_12.setWidgetResizable(True)
        self.QScrollArea_12.setWidget(self.camera_12)
        self.QScrollArea_12.setFixedSize(762,270)
        self.QScrollArea_12.setCursor(cursor)
        self.QScrollArea_12.setStyleSheet('border : 1px solid green;')
    
       
        self.combobox1.activated[str].connect(self.combobox1Selected)
        self.combobox2.activated[str].connect(self.combobox2Selected)
        self.combobox3.activated[str].connect(self.combobox3Selected)
        self.combobox4.activated[str].connect(self.combobox4Selected)
        self.combobox5.activated[str].connect(self.combobox5Selected)
        self.combobox6.activated[str].connect(self.combobox6Selected)
        self.combobox7.activated[str].connect(self.combobox7Selected)
        self.combobox8.activated[str].connect(self.combobox8Selected)
        self.combobox9.activated[str].connect(self.combobox9Selected)
        self.combobox10.activated[str].connect(self.combobox10Selected)
        self.combobox11.activated[str].connect(self.combobox11Selected)
        self.combobox12.activated[str].connect(self.combobox12Selected)
        

        
        self.degisken_Layout=QVBoxLayout()
        self.degisken_Layout.setGeometry(QtCore.QRect(500,250,220,200))
        self.degisken_Layout.setSpacing(0)
        self.degisken_Layout.setStretch(2,20)

        self.degisken_Layout2=QVBoxLayout()
        self.degisken_Layout2.setGeometry(QtCore.QRect(500,250,220,200))
        self.degisken_Layout2.setSpacing(0)
        self.degisken_Layout2.setStretch(2,20)
       
       
        self.degisken_Layout.addWidget(self.combobox1)
        self.degisken_Layout.addWidget(self.combobox2)
        self.degisken_Layout.addWidget(self.combobox3)
        self.degisken_Layout.addWidget(self.combobox4)
        self.degisken_Layout.addWidget(self.combobox5)
        self.degisken_Layout.addWidget(self.combobox6)

        self.degisken_Layout2.addWidget(self.combobox7)
        self.degisken_Layout2.addWidget(self.combobox8)
        self.degisken_Layout2.addWidget(self.combobox9)
        self.degisken_Layout2.addWidget(self.combobox10)
        self.degisken_Layout2.addWidget(self.combobox11)
        self.degisken_Layout2.addWidget(self.combobox12)
        
        
        # Set the UI elements for this Widget class.
        self.__SetupUI()

        
        menuBar = self.menuBar()
        fileMenu = QMenu("&MultiPage", self)
        # fileMenu = menuBar.addMenu(QIcon('camico.png'),'&MultiPage')
        menuBar.setStyleSheet('border : 1px solid orange;')
        menuBar.addMenu(fileMenu)
        helpMenu=menuBar.addMenu(QIcon('images/info.png'),'&Help')
        aboutMenu=menuBar.addMenu(QIcon('images/help.png'),'Yardım...')
       
        fileMenu.setIcon(QIcon('images/focus2.png'))
        fileMenu.addAction(self.newAction)
        fileMenu.addAction(self.openAction )
        fileMenu.addAction(self.saveAction )
        fileMenu.addAction(self.exitAction )
        
        helpMenu.addAction(self.helpContentAction)
        
        aboutMenu.addAction(self.aboutAction)
        

        # Create an instance of CaptureIpCameraFramesWorker.
        self.CaptureIpCameraFramesWorker_1 = CaptureIpCameraFramesWorker(self.url_1)
        self.CaptureIpCameraFramesWorker_1.ImageUpdated.connect(lambda image: self.ShowCamera1(image))

        # Create an instance of CaptureIpCameraFramesWorker.
        self.CaptureIpCameraFramesWorker_3 = CaptureIpCameraFramesWorker(self.url_2)
        self.CaptureIpCameraFramesWorker_3.ImageUpdated.connect(lambda image: self.ShowCamera3(image))

        # Create an instance of CaptureIpCameraFramesWorker.
        self.CaptureIpCameraFramesWorker_4 = CaptureIpCameraFramesWorker(self.url_3)
        self.CaptureIpCameraFramesWorker_4.ImageUpdated.connect(lambda image: self.ShowCamera4(image))

        # Create an instance of CaptureIpCameraFramesWorker.
        self.CaptureIpCameraFramesWorker_7 = CaptureIpCameraFramesWorker(self.url_4)
        self.CaptureIpCameraFramesWorker_7.ImageUpdated.connect(lambda image: self.ShowCamera7(image))
        
        # Create an instance of CaptureIpCameraFramesWorker.
        self.CaptureIpCameraFramesWorker_8 = CaptureIpCameraFramesWorker(self.url_5)
        self.CaptureIpCameraFramesWorker_8.ImageUpdated.connect(lambda image: self.ShowCamera8(image))

        # Create an instance of CaptureIpCameraFramesWorker.
        self.CaptureIpCameraFramesWorker_11 = CaptureIpCameraFramesWorker(self.url_6)
        self.CaptureIpCameraFramesWorker_11.ImageUpdated.connect(lambda image: self.ShowCamera11(image))

        # Create an instance of CaptureIpCameraFramesWorker.
        self.CaptureIpCameraFramesWorker_2 = CaptureIpCameraFramesWorker(self.url_7)
        self.CaptureIpCameraFramesWorker_2.ImageUpdated.connect(lambda image: self.ShowCamera2(image))

        # Create an instance of CaptureIpCameraFramesWorker.
        self.CaptureIpCameraFramesWorker_6 = CaptureIpCameraFramesWorker(self.url_8)
        self.CaptureIpCameraFramesWorker_6.ImageUpdated.connect(lambda image: self.ShowCamera6(image))

        # Create an instance of CaptureIpCameraFramesWorker.
        self.CaptureIpCameraFramesWorker_5 = CaptureIpCameraFramesWorker(self.url_9)
        self.CaptureIpCameraFramesWorker_5.ImageUpdated.connect(lambda image: self.ShowCamera5(image))

        # Create an instance of CaptureIpCameraFramesWorker.
        self.CaptureIpCameraFramesWorker_10 = CaptureIpCameraFramesWorker(self.url_10)
        self.CaptureIpCameraFramesWorker_10.ImageUpdated.connect(lambda image: self.ShowCamera10(image))

        # Create an instance of CaptureIpCameraFramesWorker.
        self.CaptureIpCameraFramesWorker_9 = CaptureIpCameraFramesWorker(self.url_11)
        self.CaptureIpCameraFramesWorker_9.ImageUpdated.connect(lambda image: self.ShowCamera9(image))

        # Create an instance of CaptureIpCameraFramesWorker.
        self.CaptureIpCameraFramesWorker_12 = CaptureIpCameraFramesWorker(self.url_12)
        self.CaptureIpCameraFramesWorker_12.ImageUpdated.connect(lambda image: self.ShowCamera12(image))

        # Start the thread getIpCameraFrameWorker_1.
        self.CaptureIpCameraFramesWorker_1.start()
       # self.CaptureIpCameraFramesWorker_1.sleep(1)

        # Start the thread getIpCameraFrameWorker_2.
        self.CaptureIpCameraFramesWorker_2.start()
       # self.CaptureIpCameraFramesWorker_2.sleep(1)

        # Start the thread getIpCameraFrameWorker_3.
        self.CaptureIpCameraFramesWorker_3.start()
       # self.CaptureIpCameraFramesWorker_3.sleep(1)

        # Start the thread getIpCameraFrameWorker_4.
        self.CaptureIpCameraFramesWorker_4.start()
       # self.CaptureIpCameraFramesWorker_4.sleep(1)

        # Start the thread getIpCameraFrameWorker_4.
        self.CaptureIpCameraFramesWorker_5.start()
       # self.CaptureIpCameraFramesWorker_5.sleep(1)

        # Start the thread getIpCameraFrameWorker_4.
        self.CaptureIpCameraFramesWorker_6.start()
        #self.CaptureIpCameraFramesWorker_6.sleep(1)

        # Start the thread getIpCameraFrameWorker_4.
        self.CaptureIpCameraFramesWorker_7.start()
       # self.CaptureIpCameraFramesWorker_7.sleep(1)

        # Start the thread getIpCameraFrameWorker_4.
        self.CaptureIpCameraFramesWorker_8.start()
       # self.CaptureIpCameraFramesWorker_8.sleep(1)
        
        self.CaptureIpCameraFramesWorker_9.start()
       # self.CaptureIpCameraFramesWorker_9.sleep(1)
        self.CaptureIpCameraFramesWorker_10.start()
        #self.CaptureIpCameraFramesWorker_10.sleep(1)
        self.CaptureIpCameraFramesWorker_11.start()
        #self.CaptureIpCameraFramesWorker_11.sleep(1)
        self.CaptureIpCameraFramesWorker_12.start()
        #self.CaptureIpCameraFramesWorker_12.sleep(1)
        

    def _createActions(self):
        self.newAction = QAction(QIcon('images/camico.png'),"&4 lü İzleme",self)
        self.openAction = QAction(QIcon('images/camico.png'),"&8 li İzleme", self)
        self.saveAction = QAction(QIcon('images/camico.png'),"&12 li İzleme", self)
        self.exitAction = QAction(QIcon('images/focus1.png'),"&Özel", self)
        self.helpContentAction = QAction(QIcon('images/info.png'),"&Hakkında", self)
        self.aboutAction = QAction(QIcon('images/info1.png'),"&Yardım...", self)
        
        self.newAction.triggered.connect(self.openCall_dortlu)
        self.openAction.triggered.connect(self.openCall_sekizli)
        self.saveAction.triggered.connect(self.openCall_onikili)
        self.helpContentAction.triggered.connect(self.helpShow)
        self.aboutAction.triggered.connect(self.aboutShow)
        

        
    def openCall_dortlu(self):     #  4 lü Camera View
        
        self.QScrollArea_1.setFixedSize(762,480)
        self.QScrollArea_2.setFixedSize(762,480)
        self.QScrollArea_11.setFixedSize(762,480)
        self.QScrollArea_12.setFixedSize(762,480)
        self.QScrollArea_3.hide()
        self.QScrollArea_4.hide()
        self.QScrollArea_5.hide()
        self.QScrollArea_6.hide()
        self.QScrollArea_7.hide()
        self.QScrollArea_9.hide()
        self.QScrollArea_10.hide()
        self.QScrollArea_8.hide()
        
    def openCall_sekizli(self):    # 8 li Camera View
        self.QScrollArea_3.show()
        self.QScrollArea_5.show()
        self.QScrollArea_7.show()
        self.QScrollArea_9.show()
        
       
       
        self.QScrollArea_1.setFixedSize(763,265)
        self.QScrollArea_2.setFixedSize(763,265)
        self.QScrollArea_3.setFixedSize(763,265)
        self.QScrollArea_5.setFixedSize(763,265)
        self.QScrollArea_7.setFixedSize(763,265)
        self.QScrollArea_9.setFixedSize(763,265)
        self.QScrollArea_11.setFixedSize(763,265)
        self.QScrollArea_12.setFixedSize(763,265)
        self.QScrollArea_4.hide()
        self.QScrollArea_6.hide()
        self.QScrollArea_10.hide()
        self.QScrollArea_8.hide()
    
    def openCall_onikili(self):    # 12 li Camera View
        self.QScrollArea_2.show()
        self.QScrollArea_3.show()
        self.QScrollArea_4.show()
        self.QScrollArea_5.show()
        self.QScrollArea_6.show()
        self.QScrollArea_7.show()
        self.QScrollArea_8.show()
        self.QScrollArea_9.show()
        self.QScrollArea_10.show()
        self.QScrollArea_11.show()
        self.QScrollArea_12.show()
        
        self.combobox1.show()
        self.combobox2.show()
        self.combobox3.show()
        self.combobox4.show()
        self.combobox5.show()
        self.combobox6.show()
        self.combobox7.show()
        self.combobox8.show()
        self.combobox9.show()
        self.combobox10.show()
        self.combobox11.show()
        self.combobox12.show()   
    
    def helpShow(self):
        
        dlg1 = QMessageBox(self)
        dlg1.setFont(QFont('Arial Black',10))
        dlg1.setWindowTitle("Bilgilendirme !!!")
        dlg1.setText( """---------------------------------
F1 FÜNİKÜLER IP KAMERA SİSTEMİ
                     
            Versiyon 1.0.3
                    
            METRO AŞ 
                    
            ARGE ELOSİS
                    
UĞUR BARAN , SERDAR ASLAN
---------------------------------
ugur.baran@metro.istanbul , serdar.aslan@metro.istanbul""")
        button = dlg1.exec()
        dlg1.show()
        
        #if button == QMessageBox.Ok:
           
    def aboutShow(self):
        dlg1 = QMessageBox(self)
        dlg1.setFont(QFont('Arial Black',12))
        dlg1.setWindowTitle("Nasıl Çalışır !!!")
        dlg1.setText( """---------------------------------
Sistem ip tabanlı olup metro istanbul ağında olan kameraların görüntüsünü almaktadır.

Yeni kamera eklenmek istendiğinde 'cam.json' dosyasını açıp içerisine yeni kamera bilgilerini ekleyebiliriz.

Combobox lardan seçilen kameralar sırası ile görüntü vermektedir. Sürükle-Bırak yöntemi ile istenen kamera istenen çerçevede açılabilir.
                     
Menübar daki(en sol üst seçenek) farklı izleme seçeneklerinden değişim yapılabilir 

---------------------------------""")
        button = dlg1.exec()
        
        dlg1.show()

    def Keept(self):
        self.QScrollArea_Test.hide()
        self.combo_Cam.hide()
        self.cmb_Camera1.hide()
        self.button1.show()
    def on_combobox_changed(self, value):
        global text_DragDop
        text_DragDop=value
        print(text_DragDop)

        

    
    
        # do your code    
    def comboList1(self)->None:
        
        self.combobox1 =QComboBox(self)
        # self.combobox1.setGeometry(QtCore.QRect(840, 10, 100, 31))
        self.combobox1.setGeometry(QtCore.QRect(840, 10, 10, 31))
        self.combobox1.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        self.combobox1.setAutoFillBackground(True)
        self.combobox1.setStyleSheet("background-color: rgb(0, 206, 215);")
        self.combobox1.setCurrentText("Kamera Seciniz")
        self.combobox1.setInsertPolicy(QComboBox.InsertAtCurrent)
        self.combobox1.setObjectName("combobox1")
        self.combobox1.setVisible(True)
        self.combobox1.setFixedSize(190,30)
        self.combobox1.setFont(QFont('Arial Black',9))
        # self.combobox1.setStyleSheet(("QComboBox::hover"
        #                              "{"
        #                              "background-color: rgb(0, 206, 215);"
        #                              "border : 3px solid black;"
        #                              "}"))
        self.combobox1.setStyleSheet('background-color:orange')
        self.combobox1.view().setDragDropMode(QAbstractItemView.DragOnly)
       
        
     
        
        

 
    def comboList2(self)->None:
     
        self.combobox2 =QComboBox(self)
        # self.combobox2.setGeometry(QtCore.QRect(840, 10, 100, 31))
        self.combobox2.setGeometry(QtCore.QRect(840, 10, 10, 31))
        self.combobox2.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        self.combobox2.setAutoFillBackground(True)
        self.combobox2.setStyleSheet("background-color: rgb(0, 206, 215);")
        self.combobox2.setCurrentText("Kamera Seciniz")
        self.combobox2.setInsertPolicy(QComboBox.InsertAtCurrent)
        self.combobox2.setObjectName("combobox2")
        self.combobox2.setVisible(True)
        self.combobox2.setFixedSize(190,30)
        self.combobox2.setFont(QFont('Arial Black',9)) 
        self.combobox2.setStyleSheet("background-color:orange")  
        self.combobox2.view().setDragDropMode(QAbstractItemView.DragOnly) 
        
        
   

    def comboList3(self)->None:
        self.combobox3 =QComboBox(self)
        # self.combo_Cam.setGeometry(QtCore.QRect(840, 10, 100, 31))
        self.combobox3.setGeometry(QtCore.QRect(840, 10, 10, 31))
        self.combobox3.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        self.combobox3.setAutoFillBackground(True)
        self.combobox3.setStyleSheet("background-color: rgb(0, 206, 215);")
        self.combobox3.setCurrentText("Kamera Seciniz")
        self.combobox3.setInsertPolicy(QComboBox.InsertAtCurrent)
        self.combobox3.setObjectName("combobox3")
        self.combobox3.setVisible(True)
        self.combobox3.setFixedSize(190,30)
        self.combobox3.setFont(QFont('Arial Black',9)) 
        self.combobox3.setStyleSheet("background-color:orange")
        self.combobox3.view().setDragDropMode(QAbstractItemView.DragOnly)
        # self.combobox3.currentTextChanged.connect(self.on_combobox_changed)

    def comboList4(self)->None:
        self.combobox4 =QComboBox(self)
        # self.combobox4.setGeometry(QtCore.QRect(840, 10, 100, 31))
        self.combobox4.setGeometry(QtCore.QRect(840, 10, 10, 31))
        self.combobox4.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        self.combobox4.setAutoFillBackground(True)
        self.combobox4.setStyleSheet("background-color: rgb(0, 206, 215);")
        self.combobox4.setCurrentText("Kamera Seciniz")
        self.combobox4.setInsertPolicy(QComboBox.InsertAtCurrent)
        self.combobox4.setObjectName("combobox4")
        self.combobox4.setVisible(True)
        self.combobox4.setFixedSize(190,30)
        self.combobox4.setFont(QFont('Arial Black',9)) 
        self.combobox4.setStyleSheet("background-color:orange") 
        self.combobox4.view().setDragDropMode(QAbstractItemView.DragOnly)

    def comboList5(self)->None:
        self.combobox5 =QComboBox(self)
        # self.combobox5.setGeometry(QtCore.QRect(840, 10, 100, 31))
        self.combobox5.setGeometry(QtCore.QRect(840, 10, 10, 31))
        self.combobox5.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        self.combobox5.setAutoFillBackground(True)
        self.combobox5.setStyleSheet("background-color: rgb(0, 206, 215);")
        self.combobox5.setCurrentText("Kamera Seciniz")
        self.combobox5.setInsertPolicy(QComboBox.InsertAtCurrent)
        self.combobox5.setObjectName("combobox5")
        self.combobox5.setVisible(True)
        self.combobox5.setFixedSize(190,30)
        self.combobox5.setFont(QFont('Arial Black',9)) 
        self.combobox5.setStyleSheet("background-color:orange")   
        self.combobox5.view().setDragDropMode(QAbstractItemView.DragOnly) 

    def comboList6(self)->None:
        self.combobox6 =QComboBox(self)
        # self.combobox5.setGeometry(QtCore.QRect(840, 10, 100, 31))
        self.combobox6.setGeometry(QtCore.QRect(840, 10, 10, 31))
        self.combobox6.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        self.combobox6.setAutoFillBackground(True)
        self.combobox6.setStyleSheet("background-color: rgb(0, 206, 215);")
        self.combobox6.setCurrentText("Kamera Seciniz")
        self.combobox6.setInsertPolicy(QComboBox.InsertAtCurrent)
        self.combobox6.setObjectName("combobox6")
        self.combobox6.setVisible(True)
        self.combobox6.setFixedSize(190,30)
        self.combobox6.setFont(QFont('Arial Black',9)) 
        self.combobox6.setStyleSheet("background-color:orange") 
        self.combobox6.view().setDragDropMode(QAbstractItemView.DragOnly)

    def comboList7(self)->None:
        self.combobox7 =QComboBox(self)
        # self.combobox5.setGeometry(QtCore.QRect(840, 10, 100, 31))
        self.combobox7.setGeometry(QtCore.QRect(840, 10, 10, 31))
        self.combobox7.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        self.combobox7.setAutoFillBackground(True)
        self.combobox7.setStyleSheet("background-color: rgb(0, 206, 215);")
        self.combobox7.setCurrentText("Kamera Seciniz")
        self.combobox7.setInsertPolicy(QComboBox.InsertAtCurrent)
        self.combobox7.setObjectName("combobox7")
        self.combobox7.setVisible(True)
        self.combobox7.setFixedSize(190,30)
        self.combobox7.setFont(QFont('Arial Black',9)) 
        self.combobox7.setStyleSheet("background-color:orange") 
        self.combobox7.view().setDragDropMode(QAbstractItemView.DragOnly)

    def comboList8(self)->None:
        self.combobox8 =QComboBox(self)
        # self.combobox5.setGeometry(QtCore.QRect(840, 10, 100, 31))
        self.combobox8.setGeometry(QtCore.QRect(840, 10, 10, 31))
        self.combobox8.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        self.combobox8.setAutoFillBackground(True)
        self.combobox8.setStyleSheet("background-color: rgb(0, 206, 215);")
        self.combobox8.setCurrentText("Kamera Seciniz")
        self.combobox8.setInsertPolicy(QComboBox.InsertAtCurrent)
        self.combobox8.setObjectName("combobox8")
        self.combobox8.setVisible(True)
        self.combobox8.setFixedSize(190,30)
        self.combobox8.setFont(QFont('Arial Black',9)) 
        self.combobox8.setStyleSheet("background-color:orange")  
        self.combobox8.view().setDragDropMode(QAbstractItemView.DragOnly)

    def comboList9(self)->None:
        self.combobox9 =QComboBox(self)
        # self.combobox5.setGeometry(QtCore.QRect(840, 10, 100, 31))
        self.combobox9.setGeometry(QtCore.QRect(840, 10, 10, 31))
        self.combobox9.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        self.combobox9.setAutoFillBackground(True)
        self.combobox9.setStyleSheet("background-color: rgb(0, 206, 215);")
        self.combobox9.setCurrentText("Kamera Seciniz")
        self.combobox9.setInsertPolicy(QComboBox.InsertAtCurrent)
        self.combobox9.setObjectName("combobox9")
        self.combobox9.setVisible(True)
        self.combobox9.setFixedSize(190,30)
        self.combobox9.setFont(QFont('Arial Black',9)) 
        self.combobox9.setStyleSheet("background-color:orange") 
        self.combobox9.view().setDragDropMode(QAbstractItemView.DragOnly)

    def comboList10(self)->None:
        self.combobox10 =QComboBox(self)
        # self.combobox5.setGeometry(QtCore.QRect(840, 10, 100, 31))
        self.combobox10.setGeometry(QtCore.QRect(840, 10, 10, 31))
        self.combobox10.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        self.combobox10.setAutoFillBackground(True)
        self.combobox10.setStyleSheet("background-color: rgb(0, 206, 215);")
        self.combobox10.setCurrentText("Kamera Seciniz")
        self.combobox10.setInsertPolicy(QComboBox.InsertAtCurrent)
        self.combobox10.setObjectName("combobox10")
        self.combobox10.setVisible(True)
        self.combobox10.setFixedSize(190,30)
        self.combobox10.setFont(QFont('Arial Black',9)) 
        self.combobox10.setStyleSheet("background-color:orange")   
        self.combobox10.view().setDragDropMode(QAbstractItemView.DragOnly)

    def comboList11(self)->None:
        self.combobox11 =QComboBox(self)
        # self.combobox5.setGeometry(QtCore.QRect(840, 10, 100, 31))
        self.combobox11.setGeometry(QtCore.QRect(840, 10, 10, 31))
        self.combobox11.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        self.combobox11.setAutoFillBackground(True)
        self.combobox11.setStyleSheet("background-color: rgb(0, 206, 215);")
        self.combobox11.setCurrentText("Kamera Seciniz")
        self.combobox11.setInsertPolicy(QComboBox.InsertAtCurrent)
        self.combobox11.setObjectName("combobox11")
        self.combobox11.setVisible(True)
        self.combobox11.setFixedSize(190,30)
        self.combobox11.setFont(QFont('Arial Black',9)) 
        self.combobox11.setStyleSheet("background-color:orange")  
        self.combobox11.view().setDragDropMode(QAbstractItemView.DragOnly)

    def comboList12(self)->None:
        self.combobox12 =QComboBox(self)
        # self.combobox5.setGeometry(QtCore.QRect(840, 10, 100, 31))
        self.combobox12.setGeometry(QtCore.QRect(840, 10, 10, 31))
        self.combobox12.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        self.combobox12.setAutoFillBackground(True)
        self.combobox12.setStyleSheet("background-color: rgb(0, 206, 215);")
        self.combobox12.setCurrentText("Kamera Seciniz")
        self.combobox12.setInsertPolicy(QComboBox.InsertAtCurrent)
        self.combobox12.setObjectName("combobox12")
        self.combobox12.setVisible(True)
        self.combobox12.setFixedSize(190,30)
        self.combobox12.setFont(QFont('Arial Black',9)) 
        self.combobox12.setStyleSheet("background-color:orange")  
        self.combobox12.view().setDragDropMode(QAbstractItemView.DragOnly)                                       


    def Cam_Yaz(self): # New List write to Json
        
        #json1=combo_List2[:12]
        json1=lastJsonList
        
        sonuc=json.dumps(json1)
    
        jsonfile= open('veri.json','w')
        jsonfile.write(sonuc)
        jsonfile.close()
    
    def return_Rtsp_Protocol(self, cam_index):  # indeksinin buldugumuz kameranın rtsp protokolunu buluyoruz
        global combo_List
        global combo_List_rtsp
        global comboLis_All

        rtsp_index=combo_List_rtsp[cam_index]
        return rtsp_index
        
    def combobox1Selected(self, txtVal):
        global combo_List 
        global combo_List2 
        global lastJsonList
        global combo_List_rtsp
        global text_DragDop
       
        
        cam_index1=combo_List.index(txtVal)
        #combo_List2[0]=txtVal
        lastJsonList[0]=txtVal
        # text_DragDop=txtVal
        
        self.Cam_Yaz()

        _rtsp=MainWindow.return_Rtsp_Protocol(self,cam_index1)
        self.CaptureIpCameraFramesWorker_1.stop()
        self.url_1=_rtsp
        self.CaptureIpCameraFramesWorker_1 = CaptureIpCameraFramesWorker(self.url_1)
        self.CaptureIpCameraFramesWorker_1.ImageUpdated.connect(lambda image: self.ShowCamera1(image))
        self.CaptureIpCameraFramesWorker_1.start()
        self.CaptureIpCameraFramesWorker_1.sleep(1)
        
        self.combobox1.setCurrentText(txtVal)
        
    def combobox2Selected(self, txtVal):
        global text_DragDop
        
        cam_index2=combo_List.index(txtVal)
        lastJsonList[1]=txtVal
        # text_DragDop=txtVal
       
        self.Cam_Yaz()
        _rtsp=MainWindow.return_Rtsp_Protocol(self,cam_index2)

        
        self.CaptureIpCameraFramesWorker_3.stop()
        self.url_2 = _rtsp
        self.CaptureIpCameraFramesWorker_3 = CaptureIpCameraFramesWorker(self.url_2)
        self.CaptureIpCameraFramesWorker_3.ImageUpdated.connect(lambda image: self.ShowCamera3(image))
        self.CaptureIpCameraFramesWorker_3.start()
        self.CaptureIpCameraFramesWorker_3.sleep(1)
        self.combobox2.setCurrentText(txtVal)

    def combobox3Selected(self, txtVal):
        global text_DragDop
       
        cam_index3=combo_List.index(txtVal)
        lastJsonList[2]=txtVal
        # text_DragDop=txtVal
       
        self.Cam_Yaz()
        _rtsp=MainWindow.return_Rtsp_Protocol(self,cam_index3)
        
        self.CaptureIpCameraFramesWorker_4.stop()
        self.url_3 = _rtsp
        self.CaptureIpCameraFramesWorker_4 = CaptureIpCameraFramesWorker(self.url_3)
        self.CaptureIpCameraFramesWorker_4.ImageUpdated.connect(lambda image: self.ShowCamera4(image))
        self.CaptureIpCameraFramesWorker_4.start()
        self.CaptureIpCameraFramesWorker_4.sleep(1)
        self.combobox3.setCurrentText(txtVal)
               
        
    def combobox4Selected(self, txtVal):
        global text_DragDop
        
        cam_index4=combo_List.index(txtVal)
        lastJsonList[3]=txtVal
        # text_DragDop=txtVal
       
        self.Cam_Yaz()  
        _rtsp=MainWindow.return_Rtsp_Protocol(self,cam_index4)
        
        self.CaptureIpCameraFramesWorker_7.stop()
        self.url_4 = _rtsp
        self.CaptureIpCameraFramesWorker_7 = CaptureIpCameraFramesWorker(self.url_4)
        self.CaptureIpCameraFramesWorker_7.ImageUpdated.connect(lambda image: self.ShowCamera7(image))
        self.CaptureIpCameraFramesWorker_7.start() 
        self.CaptureIpCameraFramesWorker_7.sleep(1)
        self.combobox4.setCurrentText(txtVal)

    def combobox5Selected(self, txtVal):
        
        cam_index5=combo_List.index(txtVal)
        lastJsonList[4]=txtVal
        self.Cam_Yaz()
        _rtsp=MainWindow.return_Rtsp_Protocol(self,cam_index5)

        self.CaptureIpCameraFramesWorker_8.stop()
        self.url_5 = _rtsp
        self.CaptureIpCameraFramesWorker_8 = CaptureIpCameraFramesWorker(self.url_5)
        self.CaptureIpCameraFramesWorker_8.ImageUpdated.connect(lambda image: self.ShowCamera8(image))
        self.CaptureIpCameraFramesWorker_8.start() 
        self.CaptureIpCameraFramesWorker_8.sleep(1)

    def combobox6Selected(self, txtVal):
        cam_index6=combo_List.index(txtVal)
        lastJsonList[5]=txtVal
        self.Cam_Yaz()
        _rtsp=MainWindow.return_Rtsp_Protocol(self,cam_index6)
       
        self.CaptureIpCameraFramesWorker_11.stop()
        self.url_6 = _rtsp
        self.CaptureIpCameraFramesWorker_11 = CaptureIpCameraFramesWorker(self.url_6)
        self.CaptureIpCameraFramesWorker_11.ImageUpdated.connect(lambda image: self.ShowCamera11(image))
        self.CaptureIpCameraFramesWorker_11.start()
        self.CaptureIpCameraFramesWorker_11.sleep(1)

    def combobox7Selected(self, txtVal):
        
        cam_index7=combo_List.index(txtVal)
        lastJsonList[6]=txtVal
        self.Cam_Yaz()
        _rtsp=MainWindow.return_Rtsp_Protocol(self,cam_index7)
        self.CaptureIpCameraFramesWorker_2.stop()
        self.url_7 = _rtsp
        self.CaptureIpCameraFramesWorker_2 = CaptureIpCameraFramesWorker(self.url_7)
        self.CaptureIpCameraFramesWorker_2.ImageUpdated.connect(lambda image: self.ShowCamera2(image))
        self.CaptureIpCameraFramesWorker_2.start()
        self.CaptureIpCameraFramesWorker_2.sleep(1)

    def combobox8Selected(self, txtVal):
        cam_index8=combo_List.index(txtVal)
        lastJsonList[7]=txtVal
        self.Cam_Yaz()
        _rtsp=MainWindow.return_Rtsp_Protocol(self,cam_index8)
        self.CaptureIpCameraFramesWorker_6.stop()
        self.url_8 = _rtsp
        self.CaptureIpCameraFramesWorker_6 = CaptureIpCameraFramesWorker(self.url_8)
        self.CaptureIpCameraFramesWorker_6.ImageUpdated.connect(lambda image: self.ShowCamera6(image))
        self.CaptureIpCameraFramesWorker_6.start()
        self.CaptureIpCameraFramesWorker_6.sleep(1)

    def combobox9Selected(self, txtVal):
        cam_index9=combo_List.index(txtVal)
        lastJsonList[8]=txtVal
        self.Cam_Yaz()
        _rtsp=MainWindow.return_Rtsp_Protocol(self,cam_index9)
        self.CaptureIpCameraFramesWorker_5.stop()
        self.url_9 = _rtsp
        self.CaptureIpCameraFramesWorker_5 = CaptureIpCameraFramesWorker(self.url_9)
        self.CaptureIpCameraFramesWorker_5.ImageUpdated.connect(lambda image: self.ShowCamera5(image))
        self.CaptureIpCameraFramesWorker_5.start()
        self.CaptureIpCameraFramesWorker_5.sleep(1)

    def combobox10Selected(self, txtVal):
        cam_index10=combo_List.index(txtVal)
        lastJsonList[9]=txtVal
        self.Cam_Yaz()
        _rtsp=MainWindow.return_Rtsp_Protocol(self,cam_index10)
        
        self.CaptureIpCameraFramesWorker_10.stop()
        self.url_10 = _rtsp
        self.CaptureIpCameraFramesWorker_10 = CaptureIpCameraFramesWorker(self.url_10)
        self.CaptureIpCameraFramesWorker_10.ImageUpdated.connect(lambda image: self.ShowCamera10(image))
        self.CaptureIpCameraFramesWorker_10.start()
        self.CaptureIpCameraFramesWorker_10.sleep(1)
     

    def combobox11Selected(self, txtVal):
        cam_index11=combo_List.index(txtVal)
        lastJsonList[10]=txtVal
        self.Cam_Yaz()
        _rtsp=MainWindow.return_Rtsp_Protocol(self,cam_index11)
        
        self.CaptureIpCameraFramesWorker_9.stop()
        self.url_11 = _rtsp
        self.CaptureIpCameraFramesWorker_9 = CaptureIpCameraFramesWorker(self.url_11)
        self.CaptureIpCameraFramesWorker_9.ImageUpdated.connect(lambda image: self.ShowCamera9(image))
        self.CaptureIpCameraFramesWorker_9.start()
        self.CaptureIpCameraFramesWorker_9.sleep(1)


    def combobox12Selected(self, txtVal):
        cam_index12=combo_List.index(txtVal)
        lastJsonList[11]=txtVal
        self.Cam_Yaz()
        _rtsp=MainWindow.return_Rtsp_Protocol(self,cam_index12)
       
        self.CaptureIpCameraFramesWorker_12.stop()
        self.url_12 = _rtsp
        self.CaptureIpCameraFramesWorker_12 = CaptureIpCameraFramesWorker(self.url_12)
        self.CaptureIpCameraFramesWorker_12.ImageUpdated.connect(lambda image: self.ShowCamera12(image))
        self.CaptureIpCameraFramesWorker_12.start()    
        self.CaptureIpCameraFramesWorker_12.sleep(1)                                                                                                                            
   

   
    def __SetupUI(self) -> None:
        # Create an instance of a QGridLayout layout.
        grid_layout = QGridLayout()
        grid_layout.setContentsMargins(200, 0, 200, 0)
               
        
        grid_layout.addWidget(self.QScrollArea_1, 0, 0)
        grid_layout.addWidget(self.QScrollArea_2, 0, 2)
        grid_layout.addWidget(self.QScrollArea_3, 1, 0)
        grid_layout.addWidget(self.QScrollArea_4, 1, 1)
        grid_layout.addWidget(self.QScrollArea_5, 1, 2)
        grid_layout.addWidget(self.QScrollArea_6, 1, 3)
        grid_layout.addWidget(self.QScrollArea_7, 2, 0)
        grid_layout.addWidget(self.QScrollArea_8, 2, 1)
        grid_layout.addWidget(self.QScrollArea_9, 2, 2)
        grid_layout.addWidget(self.QScrollArea_10,2, 3)
        grid_layout.addWidget(self.QScrollArea_11,3, 0)
        grid_layout.addWidget(self.QScrollArea_12,3, 2)
        
       

        
        # Create a widget instance.
        self.widget = QWidget(self)
        self.widget.setLayout(grid_layout)
        
           
        self.widget2=QWidget(self)
        #self.widget2.setGeometry(1720,30,200,1000)
        self.widget2.setGeometry(2,0,200,1000)
        self.widget2.setLayout(self.degisken_Layout)

        self.widget3=QWidget(self)
        self.widget3.setGeometry(1720,0,200,1000)
        #self.widget3.setGeometry(2,0,200,1000)
        self.widget3.setLayout(self.degisken_Layout2)
        
        
       

        # Set the central widget.
        self.setCentralWidget(self.widget)
        self.setMinimumSize(800, 600)
        self.showMaximized()
        self.setStyleSheet("QMainWindow {background: 'lightgray';}")
        self.setWindowIcon(QIcon(QPixmap("images/iconn.ico")))
        # Set window title.
        self.setWindowTitle("FÜNİKÜLER IP KAMERA SİSTEMİ                                                                                                                                                          METRO İSTANBUL ARGE MÜDÜRLÜĞÜ ELEKTRONİK SİSTEMLER KOORDİNATÖRLÜĞÜ (ELOSİS)")
        
  
        
    @QtCore.pyqtSlot()
    def ShowCamera1(self, frame: QImage.Format_RGB888) -> None:
        self.camera_1.setPixmap(QPixmap.fromImage(frame))

        
    @QtCore.pyqtSlot()
    def ShowCamera2(self, frame: QImage.Format_RGB888) -> None:
        self.camera_2.setPixmap(QPixmap.fromImage(frame))
        
        
    @QtCore.pyqtSlot()
    def ShowCamera3(self, frame: QImage.Format_RGB888) -> None:
        self.camera_3.setPixmap(QPixmap.fromImage(frame))
        
       
    @QtCore.pyqtSlot()
    def ShowCamera4(self, frame: QImage.Format_RGB888) -> None:
        self.camera_4.setPixmap(QPixmap.fromImage(frame))
        
       
    @QtCore.pyqtSlot()
    def ShowCamera5(self, frame: QImage.Format_RGB888) -> None:
        self.camera_5.setPixmap(QPixmap.fromImage(frame))
       

    @QtCore.pyqtSlot()
    def ShowCamera6(self, frame: QImage) -> None:
        self.camera_6.setPixmap(QPixmap.fromImage(frame))
        

    @QtCore.pyqtSlot()
    def ShowCamera7(self, frame: QImage) -> None:
        self.camera_7.setPixmap(QPixmap.fromImage(frame))
        

    @QtCore.pyqtSlot()
    def ShowCamera8(self, frame: QImage) -> None:
        self.camera_8.setPixmap(QPixmap.fromImage(frame))
       
    @QtCore.pyqtSlot()
    def ShowCamera9(self, frame: QImage) -> None:
        self.camera_9.setPixmap(QPixmap.fromImage(frame))    
        
    @QtCore.pyqtSlot()
    def ShowCamera10(self, frame: QImage) -> None:
        self.camera_10.setPixmap(QPixmap.fromImage(frame))
        
    @QtCore.pyqtSlot()
    def ShowCamera11(self, frame: QImage) -> None:
        self.camera_11.setPixmap(QPixmap.fromImage(frame))
        
    @QtCore.pyqtSlot()
    def ShowCamera12(self, frame: QImage) -> None:
        self.camera_12.setPixmap(QPixmap.fromImage(frame))  
        

    # Override method for class MainWindow.
    def eventFilter(self, source: QObject, event: QEvent) -> bool:
        """
        Method to capture the events for objects with an event filter installed.
        :param source: The object for whom an event took place.
        :param event: The event that took place.
        :return: True if event is handled.
        """
        #
        if event.type() == QtCore.QEvent.MouseButtonDblClick:
           if source.objectName() == 'Camera_1':
                #
                if self.list_of_cameras_state["Camera_1"] == "Normal":
                    self.QScrollArea_2.hide()
                    self.QScrollArea_3.hide()
                    self.QScrollArea_4.hide()
                    self.QScrollArea_5.hide()
                    self.QScrollArea_6.hide()
                    self.QScrollArea_7.hide()
                    self.QScrollArea_8.hide()
                    self.QScrollArea_9.hide()
                    self.QScrollArea_10.hide()
                    self.QScrollArea_11.hide()
                    self.QScrollArea_12.hide()
                    self.combobox1.hide()
                    self.combobox2.hide()
                    self.combobox3.hide()
                    self.combobox4.hide()
                    self.combobox5.hide()
                    self.combobox6.hide()
                    self.combobox7.hide()
                    self.combobox8.hide()
                    self.combobox9.hide()
                    self.combobox10.hide()
                    self.combobox11.hide()
                    self.combobox12.hide()
                    self.QScrollArea_1.setStyleSheet('border : 1px solid red;')
                    self.list_of_cameras_state["Camera_1"] = "Maximized"
                    self.QScrollArea_1.setFixedSize(1520,1000)
                else:
                    self.QScrollArea_2.show()
                    self.QScrollArea_3.show()
                    self.QScrollArea_4.show()
                    self.QScrollArea_5.show()
                    self.QScrollArea_6.show()
                    self.QScrollArea_7.show()
                    self.QScrollArea_8.show()
                    self.QScrollArea_9.show()
                    self.QScrollArea_10.show()
                    self.QScrollArea_11.show()
                    self.QScrollArea_12.show()
                    
                    self.combobox1.show()
                    self.combobox2.show()
                    self.combobox3.show()
                    self.combobox4.show()
                    self.combobox5.show()
                    self.combobox6.show()
                    self.combobox7.show()
                    self.combobox8.show()
                    self.combobox9.show()
                    self.combobox10.show()
                    self.combobox11.show()
                    self.combobox12.show()
                    self.QScrollArea_1.setStyleSheet('border : 1px solid green;')
                    self.list_of_cameras_state["Camera_1"] = "Normal"
                    self.QScrollArea_1.setFixedSize(763,265)
           elif source.objectName() == 'Camera_2':
                #
                if self.list_of_cameras_state["Camera_2"] == "Normal":
                    self.QScrollArea_1.hide()
                    self.QScrollArea_3.hide()
                    self.QScrollArea_4.hide()
                    self.QScrollArea_5.hide()
                    self.QScrollArea_6.hide()
                    self.QScrollArea_7.hide()
                    self.QScrollArea_8.hide()
                    self.QScrollArea_9.hide()
                    self.QScrollArea_10.hide()
                    self.QScrollArea_11.hide()
                    self.QScrollArea_12.hide()
                    self.combobox1.hide()
                    self.combobox2.hide()
                    self.combobox3.hide()
                    self.combobox4.hide()
                    self.combobox5.hide()
                    self.combobox6.hide()
                    self.combobox7.hide()
                    self.combobox8.hide()
                    self.combobox9.hide()
                    self.combobox10.hide()
                    self.combobox11.hide()
                    self.combobox12.hide()
                    self.QScrollArea_2.setStyleSheet('border : 1px solid red;')
                    self.list_of_cameras_state["Camera_2"] = "Maximized"
                    self.QScrollArea_2.setFixedSize(1520,1000)
                else:
                    self.QScrollArea_1.show()
                    self.QScrollArea_3.show()
                    self.QScrollArea_4.show()
                    self.QScrollArea_5.show()
                    self.QScrollArea_6.show()
                    self.QScrollArea_7.show()
                    self.QScrollArea_8.show()
                    self.QScrollArea_9.show()
                    self.QScrollArea_10.show()
                    self.QScrollArea_11.show()
                    self.QScrollArea_12.show()
                    
                    self.combobox1.show()
                    self.combobox2.show()
                    self.combobox3.show()
                    self.combobox4.show()
                    self.combobox5.show()
                    self.combobox6.show()
                    self.combobox7.show()
                    self.combobox8.show()
                    self.combobox9.show()
                    self.combobox10.show()
                    self.combobox11.show()
                    self.combobox12.show()
                    self.QScrollArea_2.setStyleSheet('border : 1px solid green;')
                    self.list_of_cameras_state["Camera_2"] = "Normal"
                    self.QScrollArea_2.setFixedSize(762,265)
           elif source.objectName() == 'Camera_3':
                #
                if self.list_of_cameras_state["Camera_3"] == "Normal":
                    self.QScrollArea_1.hide()
                    self.QScrollArea_2.hide()
                    self.QScrollArea_4.hide()
                    self.QScrollArea_5.hide()
                    self.QScrollArea_6.hide()
                    self.QScrollArea_7.hide()
                    self.QScrollArea_8.hide()
                    self.QScrollArea_9.hide()
                    self.QScrollArea_10.hide()
                    self.QScrollArea_11.hide()
                    self.QScrollArea_12.hide()
                    self.combobox1.hide()
                    self.combobox2.hide()
                    self.combobox3.hide()
                    self.combobox4.hide()
                    self.combobox5.hide()
                    self.combobox6.hide()
                    self.combobox7.hide()
                    self.combobox8.hide()
                    self.combobox9.hide()
                    self.combobox10.hide()
                    self.combobox11.hide()
                    self.combobox12.hide()
                    self.QScrollArea_3.setStyleSheet('border : 1px solid red;')
                    self.list_of_cameras_state["Camera_3"] = "Maximized"
                    self.QScrollArea_3.setFixedSize(1520,1000)
                else:
                    self.QScrollArea_1.show()
                    self.QScrollArea_2.show()
                    self.QScrollArea_4.show()
                    self.QScrollArea_5.show()
                    self.QScrollArea_6.show()
                    self.QScrollArea_7.show()
                    self.QScrollArea_8.show()
                    self.QScrollArea_9.show()
                    self.QScrollArea_10.show()
                    self.QScrollArea_11.show()
                    self.QScrollArea_12.show()
                    
                    self.combobox1.show()
                    self.combobox2.show()
                    self.combobox3.show()
                    self.combobox4.show()
                    self.combobox5.show()
                    self.combobox6.show()
                    self.combobox7.show()
                    self.combobox8.show()
                    self.combobox9.show()
                    self.combobox10.show()
                    self.combobox11.show()
                    self.combobox12.show()
                    self.QScrollArea_3.setStyleSheet('border : 1px solid green;')
                    self.list_of_cameras_state["Camera_3"] = "Normal"
                    self.QScrollArea_3.setFixedSize(382,260)
           elif source.objectName() == 'Camera_4':
                #
                if self.list_of_cameras_state["Camera_4"] == "Normal":
                    self.QScrollArea_1.hide()
                    self.QScrollArea_2.hide()
                    self.QScrollArea_3.hide()
                    self.QScrollArea_5.hide()
                    self.QScrollArea_6.hide()
                    self.QScrollArea_7.hide()
                    self.QScrollArea_8.hide()
                    self.QScrollArea_9.hide()
                    self.QScrollArea_10.hide()
                    self.QScrollArea_11.hide()
                    self.QScrollArea_12.hide()
                    self.combobox1.hide()
                    self.combobox2.hide()
                    self.combobox3.hide()
                    self.combobox4.hide()
                    self.combobox5.hide()
                    self.combobox6.hide()
                    self.combobox7.hide()
                    self.combobox8.hide()
                    self.combobox9.hide()
                    self.combobox10.hide()
                    self.combobox11.hide()
                    self.combobox12.hide()
                    self.QScrollArea_4.setStyleSheet('border : 1px solid red;')
                    self.list_of_cameras_state["Camera_4"] = "Maximized"
                    self.QScrollArea_4.setFixedSize(1520,1000)
                else:
                    self.QScrollArea_1.show()
                    self.QScrollArea_2.show()
                    self.QScrollArea_3.show()
                    self.QScrollArea_5.show()
                    self.QScrollArea_6.show()
                    self.QScrollArea_7.show()
                    self.QScrollArea_8.show()
                    self.QScrollArea_9.show()
                    self.QScrollArea_10.show()
                    self.QScrollArea_11.show()
                    self.QScrollArea_12.show()
                    
                    self.combobox1.show()
                    self.combobox2.show()
                    self.combobox3.show()
                    self.combobox4.show()
                    self.combobox5.show()
                    self.combobox6.show()
                    self.combobox7.show()
                    self.combobox8.show()
                    self.combobox9.show()
                    self.combobox10.show()
                    self.combobox11.show()
                    self.combobox12.show()
                    self.list_of_cameras_state["Camera_4"] = "Normal"
                    self.QScrollArea_4.setFixedSize(382,260)
                    self.QScrollArea_4.setStyleSheet('border : 1px solid green;')
           elif source.objectName() == 'Camera_5':
                #
                if self.list_of_cameras_state["Camera_5"] == "Normal":
                    self.QScrollArea_1.hide()
                    self.QScrollArea_2.hide()
                    self.QScrollArea_3.hide()
                    self.QScrollArea_4.hide()
                    self.QScrollArea_6.hide()
                    self.QScrollArea_7.hide()
                    self.QScrollArea_8.hide()
                    self.QScrollArea_9.hide()
                    self.QScrollArea_10.hide()
                    self.QScrollArea_11.hide()
                    self.QScrollArea_12.hide()
                    self.combobox1.hide()
                    self.combobox2.hide()
                    self.combobox3.hide()
                    self.combobox4.hide()
                    self.combobox5.hide()
                    self.combobox6.hide()
                    self.combobox7.hide()
                    self.combobox8.hide()
                    self.combobox9.hide()
                    self.combobox10.hide()
                    self.combobox11.hide()
                    self.combobox12.hide()
                    self.list_of_cameras_state["Camera_5"] = "Maximized"
                    self.QScrollArea_5.setFixedSize(1520,1000)
                    self.QScrollArea_5.setStyleSheet('border : 1px solid red;')
                else:
                    self.QScrollArea_1.show()
                    self.QScrollArea_2.show()
                    self.QScrollArea_3.show()
                    self.QScrollArea_4.show()
                    self.QScrollArea_6.show()
                    self.QScrollArea_7.show()
                    self.QScrollArea_8.show()
                    self.QScrollArea_9.show()
                    self.QScrollArea_10.show()
                    self.QScrollArea_11.show()
                    self.QScrollArea_12.show()
                    
                    self.combobox1.show()
                    self.combobox2.show()
                    self.combobox3.show()
                    self.combobox4.show()
                    self.combobox5.show()
                    self.combobox6.show()
                    self.combobox7.show()
                    self.combobox8.show()
                    self.combobox9.show()
                    self.combobox10.show()
                    self.combobox11.show()
                    self.combobox12.show()
                    self.list_of_cameras_state["Camera_5"] = "Normal"
                    self.QScrollArea_5.setFixedSize(382,260)
                    self.QScrollArea_5.setStyleSheet('border : 1px solid green;')
           elif source.objectName() == 'Camera_6':
                #
                if self.list_of_cameras_state["Camera_6"] == "Normal":
                    self.QScrollArea_1.hide()
                    self.QScrollArea_2.hide()
                    self.QScrollArea_3.hide()
                    self.QScrollArea_4.hide()
                    self.QScrollArea_5.hide()
                    self.QScrollArea_7.hide()
                    self.QScrollArea_8.hide()
                    self.QScrollArea_9.hide()
                    self.QScrollArea_10.hide()
                    self.QScrollArea_11.hide()
                    self.QScrollArea_12.hide()
                    self.combobox1.hide()
                    self.combobox2.hide()
                    self.combobox3.hide()
                    self.combobox4.hide()
                    self.combobox5.hide()
                    self.combobox6.hide()
                    self.combobox7.hide()
                    self.combobox8.hide()
                    self.combobox9.hide()
                    self.combobox10.hide()
                    self.combobox11.hide()
                    self.combobox12.hide()
                    self.list_of_cameras_state["Camera_6"] = "Maximized"
                    self.QScrollArea_6.setFixedSize(1520,1000)
                    self.QScrollArea_6.setStyleSheet('border : 1px solid red;')
                else:
                    self.QScrollArea_1.show()
                    self.QScrollArea_2.show()
                    self.QScrollArea_3.show()
                    self.QScrollArea_4.show()
                    self.QScrollArea_5.show()
                    self.QScrollArea_7.show()
                    self.QScrollArea_8.show()
                    self.QScrollArea_9.show()
                    self.QScrollArea_10.show()
                    self.QScrollArea_11.show()
                    self.QScrollArea_12.show()
                    
                    self.combobox1.show()
                    self.combobox2.show()
                    self.combobox3.show()
                    self.combobox4.show()
                    self.combobox5.show()
                    self.combobox6.show()
                    self.combobox7.show()
                    self.combobox8.show()
                    self.combobox9.show()
                    self.combobox10.show()
                    self.combobox11.show()
                    self.combobox12.show()
                    self.list_of_cameras_state["Camera_6"] = "Normal"
                    self.QScrollArea_6.setFixedSize(380,260)
                    self.QScrollArea_6.setStyleSheet('border : 1px solid green;')

           elif source.objectName() == 'Camera_7':
                
                if self.list_of_cameras_state["Camera_7"] == "Normal":
                    self.QScrollArea_1.hide()
                    self.QScrollArea_2.hide()
                    self.QScrollArea_3.hide()
                    self.QScrollArea_4.hide()
                    self.QScrollArea_5.hide()
                    self.QScrollArea_6.hide()
                    self.QScrollArea_8.hide()
                    self.QScrollArea_9.hide()
                    self.QScrollArea_10.hide()
                    self.QScrollArea_11.hide()
                    self.QScrollArea_12.hide()
                    self.combobox1.hide()
                    self.combobox2.hide()
                    self.combobox3.hide()
                    self.combobox4.hide()
                    self.combobox5.hide()
                    self.combobox6.hide()
                    self.combobox7.hide()
                    self.combobox8.hide()
                    self.combobox9.hide()
                    self.combobox10.hide()
                    self.combobox11.hide()
                    self.combobox12.hide()
                    self.list_of_cameras_state["Camera_7"] = "Maximized"
                    self.QScrollArea_7.setFixedSize(1520,1000)
                    self.QScrollArea_7.setStyleSheet('border : 1px solid red;')
                else:
                    self.QScrollArea_1.show()
                    self.QScrollArea_2.show()
                    self.QScrollArea_3.show()
                    self.QScrollArea_4.show()
                    self.QScrollArea_5.show()
                    self.QScrollArea_6.show()
                    self.QScrollArea_8.show()
                    self.QScrollArea_9.show()
                    self.QScrollArea_10.show()
                    self.QScrollArea_11.show()
                    self.QScrollArea_12.show()
                    
                    self.combobox1.show()
                    self.combobox2.show()
                    self.combobox3.show()
                    self.combobox4.show()
                    self.combobox5.show()
                    self.combobox6.show()
                    self.combobox7.show()
                    self.combobox8.show()
                    self.combobox9.show()
                    self.combobox10.show()
                    self.combobox11.show()
                    self.combobox12.show()
                    self.list_of_cameras_state["Camera_7"] = "Normal"
                    self.QScrollArea_7.setFixedSize(382,260)
                    self.QScrollArea_7.setStyleSheet('border : 1px solid green;')

           elif source.objectName() == 'Camera_8':
                #
                if self.list_of_cameras_state["Camera_8"] == "Normal":
                    self.QScrollArea_1.hide()
                    self.QScrollArea_2.hide()
                    self.QScrollArea_3.hide()
                    self.QScrollArea_4.hide()
                    self.QScrollArea_5.hide()
                    self.QScrollArea_6.hide()
                    self.QScrollArea_7.hide()
                    self.QScrollArea_9.hide()
                    self.QScrollArea_10.hide()
                    self.QScrollArea_11.hide()
                    self.QScrollArea_12.hide()
                    self.combobox1.hide()
                    self.combobox2.hide()
                    self.combobox3.hide()
                    self.combobox4.hide()
                    self.combobox5.hide()
                    self.combobox6.hide()
                    self.combobox7.hide()
                    self.combobox8.hide()
                    self.combobox9.hide()
                    self.combobox10.hide()
                    self.combobox11.hide()
                    self.combobox12.hide()
                    self.list_of_cameras_state["Camera_8"] = "Maximized"
                    self.QScrollArea_8.setFixedSize(1520,1000)
                    self.QScrollArea_8.setStyleSheet('border : 1px solid red;')
                else:
                    self.QScrollArea_1.show()
                    self.QScrollArea_2.show()
                    self.QScrollArea_3.show()
                    self.QScrollArea_4.show()
                    self.QScrollArea_5.show()
                    self.QScrollArea_6.show()
                    self.QScrollArea_7.show()
                    self.QScrollArea_9.show()
                    self.QScrollArea_10.show()
                    self.QScrollArea_11.show()
                    self.QScrollArea_12.show()
                    
                    self.combobox1.show()
                    self.combobox2.show()
                    self.combobox3.show()
                    self.combobox4.show()
                    self.combobox5.show()
                    self.combobox6.show()
                    self.combobox7.show()
                    self.combobox8.show()
                    self.combobox9.show()
                    self.combobox10.show()
                    self.combobox11.show()
                    self.combobox12.show()
                    self.list_of_cameras_state["Camera_8"] = "Normal"
                    self.QScrollArea_8.setFixedSize(382,260)
                    self.QScrollArea_8.setStyleSheet('border : 1px solid green;')

           elif source.objectName() == 'Camera_9':
                #
                if self.list_of_cameras_state["Camera_9"] == "Normal":
                    self.QScrollArea_1.hide()
                    self.QScrollArea_2.hide()
                    self.QScrollArea_3.hide()
                    self.QScrollArea_4.hide()
                    self.QScrollArea_5.hide()
                    self.QScrollArea_6.hide()
                    self.QScrollArea_7.hide()
                    self.QScrollArea_8.hide()
                    self.QScrollArea_10.hide()
                    self.QScrollArea_11.hide()
                    self.QScrollArea_12.hide()
                    self.combobox1.hide()
                    self.combobox2.hide()
                    self.combobox3.hide()
                    self.combobox4.hide()
                    self.combobox5.hide()
                    self.combobox6.hide()
                    self.combobox7.hide()
                    self.combobox8.hide()
                    self.combobox9.hide()
                    self.combobox10.hide()
                    self.combobox11.hide()
                    self.combobox12.hide()
                    self.list_of_cameras_state["Camera_9"] = "Maximized"
                    self.QScrollArea_9.setFixedSize(1520,1000)
                    self.QScrollArea_9.setStyleSheet('border : 1px solid red;')
                else:
                    self.QScrollArea_1.show()
                    self.QScrollArea_2.show()
                    self.QScrollArea_3.show()
                    self.QScrollArea_4.show()
                    self.QScrollArea_5.show()
                    self.QScrollArea_6.show()
                    self.QScrollArea_7.show()
                    self.QScrollArea_8.show()
                    self.QScrollArea_10.show()
                    self.QScrollArea_11.show()
                    self.QScrollArea_12.show()
                    
                    self.combobox1.show()
                    self.combobox2.show()
                    self.combobox3.show()
                    self.combobox4.show()
                    self.combobox5.show()
                    self.combobox6.show()
                    self.combobox7.show()
                    self.combobox8.show()
                    self.combobox9.show()
                    self.combobox10.show()
                    self.combobox11.show()
                    self.combobox12.show()
                    self.list_of_cameras_state["Camera_9"] = "Normal"   
                    self.QScrollArea_9.setFixedSize(382,260)
                    self.QScrollArea_9.setStyleSheet('border : 1px solid green;')
           elif source.objectName() == 'Camera_10':
                #
                if self.list_of_cameras_state["Camera_10"] == "Normal":
                    self.QScrollArea_1.hide()
                    self.QScrollArea_2.hide()
                    self.QScrollArea_3.hide()
                    self.QScrollArea_4.hide()
                    self.QScrollArea_5.hide()
                    self.QScrollArea_6.hide()
                    self.QScrollArea_7.hide()
                    self.QScrollArea_8.hide()
                    self.QScrollArea_9.hide()
                    self.QScrollArea_11.hide()
                    self.QScrollArea_12.hide()
                    self.combobox1.hide()
                    self.combobox2.hide()
                    self.combobox3.hide()
                    self.combobox4.hide()
                    self.combobox5.hide()
                    self.combobox6.hide()
                    self.combobox7.hide()
                    self.combobox8.hide()
                    self.combobox9.hide()
                    self.combobox10.hide()
                    self.combobox11.hide()
                    self.combobox12.hide()
                    self.list_of_cameras_state["Camera_10"] = "Maximized"
                    self.QScrollArea_10.setFixedSize(1520,1000)
                    self.QScrollArea_10.setStyleSheet('border : 1px solid red;')
                else:
                    self.QScrollArea_1.show()
                    self.QScrollArea_2.show()
                    self.QScrollArea_3.show()
                    self.QScrollArea_4.show()
                    self.QScrollArea_5.show()
                    self.QScrollArea_6.show()
                    self.QScrollArea_7.show()
                    self.QScrollArea_8.show()
                    self.QScrollArea_9.show()
                    self.QScrollArea_11.show()
                    self.QScrollArea_12.show()
                    
                    self.combobox1.show()
                    self.combobox2.show()
                    self.combobox3.show()
                    self.combobox4.show()
                    self.combobox5.show()
                    self.combobox6.show()
                    self.combobox7.show()
                    self.combobox8.show()
                    self.combobox9.show()
                    self.combobox10.show()
                    self.combobox11.show()
                    self.combobox12.show()
                    self.list_of_cameras_state["Camera_10"] = "Normal"                     
                    self.QScrollArea_10.setFixedSize(380,260)
                    self.QScrollArea_10.setStyleSheet('border : 1px solid green;')
           elif source.objectName() == 'Camera_11':
                #
                if self.list_of_cameras_state["Camera_11"] == "Normal":
                    self.QScrollArea_1.hide()
                    self.QScrollArea_2.hide()
                    self.QScrollArea_3.hide()
                    self.QScrollArea_4.hide()
                    self.QScrollArea_5.hide()
                    self.QScrollArea_6.hide()
                    self.QScrollArea_7.hide()
                    self.QScrollArea_8.hide()
                    self.QScrollArea_9.hide()
                    self.QScrollArea_10.hide()
                    self.QScrollArea_12.hide()
                    self.combobox1.hide()
                    self.combobox2.hide()
                    self.combobox3.hide()
                    self.combobox4.hide()
                    self.combobox5.hide()
                    self.combobox6.hide()
                    self.combobox7.hide()
                    self.combobox8.hide()
                    self.combobox9.hide()
                    self.combobox10.hide()
                    self.combobox11.hide()
                    self.combobox12.hide()
                    self.list_of_cameras_state["Camera_11"] = "Maximized"
                    self.QScrollArea_11.setFixedSize(1520,1000)
                    self.QScrollArea_11.setStyleSheet('border : 1px solid red;')
                else:
                    self.QScrollArea_1.show()
                    self.QScrollArea_2.show()
                    self.QScrollArea_3.show()
                    self.QScrollArea_4.show()
                    self.QScrollArea_5.show()
                    self.QScrollArea_6.show()
                    self.QScrollArea_7.show()
                    self.QScrollArea_8.show()
                    self.QScrollArea_9.show()
                    self.QScrollArea_10.show()
                    self.QScrollArea_12.show()
                    
                    self.combobox1.show()
                    self.combobox2.show()
                    self.combobox3.show()
                    self.combobox4.show()
                    self.combobox5.show()
                    self.combobox6.show()
                    self.combobox7.show()
                    self.combobox8.show()
                    self.combobox9.show()
                    self.combobox10.show()
                    self.combobox11.show()
                    self.combobox12.show()
                    self.list_of_cameras_state["Camera_11"] = "Normal" 
                    self.QScrollArea_11.setFixedSize(763,270) 
                    self.QScrollArea_11.setStyleSheet('border : 1px solid green;')
           elif source.objectName() == 'Camera_12':
                #
                if self.list_of_cameras_state["Camera_12"] == "Normal":
                    self.QScrollArea_1.hide()
                    self.QScrollArea_2.hide()
                    self.QScrollArea_3.hide()
                    self.QScrollArea_4.hide()
                    self.QScrollArea_5.hide()
                    self.QScrollArea_6.hide()
                    self.QScrollArea_7.hide()
                    self.QScrollArea_8.hide()
                    self.QScrollArea_9.hide()
                    self.QScrollArea_10.hide()
                    self.QScrollArea_11.hide()
                    self.combobox1.hide()
                    self.combobox2.hide()
                    self.combobox3.hide()
                    self.combobox4.hide()
                    self.combobox5.hide()
                    self.combobox6.hide()
                    self.combobox7.hide()
                    self.combobox8.hide()
                    self.combobox9.hide()
                    self.combobox10.hide()
                    self.combobox11.hide()
                    self.combobox12.hide()
                    self.list_of_cameras_state["Camera_12"] = "Maximized"
                    self.QScrollArea_12.setFixedSize(1520,1000)
                    self.QScrollArea_12.setStyleSheet('border : 1px solid red;')
                else:
                    self.QScrollArea_1.show()
                    self.QScrollArea_2.show()
                    self.QScrollArea_3.show()
                    self.QScrollArea_4.show()
                    self.QScrollArea_5.show()
                    self.QScrollArea_6.show()
                    self.QScrollArea_7.show()
                    self.QScrollArea_8.show()
                    self.QScrollArea_9.show()
                    self.QScrollArea_10.show()
                    self.QScrollArea_11.show()
                    
                    self.combobox1.show()
                    self.combobox2.show()
                    self.combobox3.show()
                    self.combobox4.show()
                    self.combobox5.show()
                    self.combobox6.show()
                    self.combobox7.show()
                    self.combobox8.show()
                    self.combobox9.show()
                    self.combobox10.show()
                    self.combobox11.show()
                    self.combobox12.show()
                    self.list_of_cameras_state["Camera_12"] = "Normal"
                    self.QScrollArea_12.setFixedSize(762,270)   
                    self.QScrollArea_12.setStyleSheet('border : 1px solid green;')                          
           else:
                return super(MainWindow, self).eventFilter(source, event)
           return True
        
        elif event.type() == QtCore.QEvent.MouseButtonPress:
            if event.button() == QtCore.Qt.RightButton:
                            #do what you want here

                if source.objectName() == 'Camera_1':
                    website1 = combo_List.index(lastJsonList[0])
                    website=comboLis_All[website1]["cam_ip"]
                
                
                elif source.objectName() == 'Camera_2':
                    website1 = combo_List.index(lastJsonList[6])
                    website=comboLis_All[website1]["cam_ip"]                
                
                elif source.objectName() == 'Camera_3':
                    website1 = combo_List.index(lastJsonList[1])
                    website=comboLis_All[website1]["cam_ip"]                
                    
                elif source.objectName() == 'Camera_4':
                    website1 = combo_List.index(lastJsonList[2])
                    website=comboLis_All[website1]["cam_ip"]                
                   
                elif source.objectName() == 'Camera_5':
                    website1 = combo_List.index(lastJsonList[8])
                    website=comboLis_All[website1]["cam_ip"]                
                    
                elif source.objectName() == 'Camera_6':
                    website1 = combo_List.index(lastJsonList[7])
                    website=comboLis_All[website1]["cam_ip"]                
                   
                elif source.objectName() == 'Camera_7':
                    website1 = combo_List.index(lastJsonList[3])
                    website=comboLis_All[website1]["cam_ip"]                
                    
                elif source.objectName() == 'Camera_8':
                    website1 = combo_List.index(lastJsonList[4])
                    website=comboLis_All[website1]["cam_ip"]                
                    
                elif source.objectName() == 'Camera_9':
                    website1 = combo_List.index(lastJsonList[10])
                    website=comboLis_All[website1]["cam_ip"]                
                     
                elif source.objectName() == 'Camera_10':
                    website1 = combo_List.index(lastJsonList[9])
                    website=comboLis_All[website1]["cam_ip"]                
                     
                elif source.objectName() == 'Camera_11':
                    website1 = combo_List.index(lastJsonList[5])
                    website=comboLis_All[website1]["cam_ip"]                
                    
                elif source.objectName() == 'Camera_12':
                    website1 = combo_List.index(lastJsonList[11])
                    website=comboLis_All[website1]["cam_ip"]                
                                  
                
                dlg = QMessageBox(self)
                dlg.setWindowTitle("Metro İstanbul(Admin)")
                dlg.setText("WebBrowser Aç!\nKamera Paneline Git")
                dlg.setIcon(QMessageBox.Information)
                dlg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
                pos = QCursor.pos()
                dlg.setStyleSheet("background-color: green")
                dlg.move(int(pos.x()), int(pos.y())) # Mouse tıkladıgımız yerde popup cıkarmak
                button = dlg.exec()
                
                
                if button==QMessageBox.Ok:
                    wb.open(website)
     
            else:
                return super(MainWindow, self).eventFilter(source, event)
            return True
        else:
            
            
            return super(MainWindow, self).eventFilter(source, event) 
    # Overwrite method closeEvent from class QMainWindow.
    def closeEvent(self, event) -> None:
        # If thread getIpCameraFrameWorker_1 is running, then exit it.
        if self.CaptureIpCameraFramesWorker_1.isRunning():
            self.CaptureIpCameraFramesWorker_1.quit()
        # If thread getIpCameraFrameWorker_2 is running, then exit it.
        if self.CaptureIpCameraFramesWorker_2.isRunning():
            self.CaptureIpCameraFramesWorker_2.quit()
        # If thread getIpCameraFrameWorker_3 is running, then exit it.
        if self.CaptureIpCameraFramesWorker_3.isRunning():
            self.CaptureIpCameraFramesWorker_3.quit()
        if self.CaptureIpCameraFramesWorker_4.isRunning():
            self.CaptureIpCameraFramesWorker_4.quit()
        if self.CaptureIpCameraFramesWorker_5.isRunning():
            self.CaptureIpCameraFramesWorker_5.quit()  
        if self.CaptureIpCameraFramesWorker_6.isRunning():
            self.CaptureIpCameraFramesWorker_6.quit()  
        if self.CaptureIpCameraFramesWorker_7.isRunning():
            self.CaptureIpCameraFramesWorker_7.quit()  
        if self.CaptureIpCameraFramesWorker_8.isRunning():
            self.CaptureIpCameraFramesWorker_8.quit()
        if self.CaptureIpCameraFramesWorker_9.isRunning():
            self.CaptureIpCameraFramesWorker_9.quit()
        if self.CaptureIpCameraFramesWorker_10.isRunning():
            self.CaptureIpCameraFramesWorker_10.quit()
        if self.CaptureIpCameraFramesWorker_11.isRunning():
            self.CaptureIpCameraFramesWorker_11.quit()
        if self.CaptureIpCameraFramesWorker_12.isRunning():
            self.CaptureIpCameraFramesWorker_12.quit()                          
        # Accept the event
        event.accept()
    
    



    def dragEnterEvent(self, event):
        mimeData = QtCore.QMimeData()
        if mimeData.hasText:

            event.accept()
        else:
            event.ignore()
            
    def dragMoveEvent(self, event):
        mimeData = QtCore.QMimeData()
        
        if mimeData.hasText:
            event.setDropAction(Qt.CopyAction)

            event.accept()
        else:
            event.ignore()    
     
           
    def dropEvent(self, event):   # Drag and Drop in Camera View
        
        mimeData = QtCore.QMimeData()

        format = 'application/x-qabstractitemmodeldatalist'
        data=event.mimeData().data(format)     # Sürükle bırak ile veriyi alıyoruz.
    
        name_str = codecs.decode(data,'utf-8')
        # text = name_str[0][Qt.DisplayRole].
        mimeData.setText(name_str)
        # print(name_str[26:].replace('\x00','').strip(""))
        
        if mimeData.hasText:
            # self.dumpObjectTree()
            source_widget = event.source()
            new_Camera=(name_str[26:].replace('\x00','')).strip("")
            
            # print("new data==",new_Camera.strip(' '))
            destination = self.childAt(event.pos())     # Mouse bırakılan pozisyondaki children alıyoruz
            
            if destination.objectName()=='Camera_1':     # Mouse bırakılan pozisyondaki children adını alıyoruz
                # print(destination.objectName())
                self.camera_1.setText(new_Camera)
                self.combobox1Selected(new_Camera)
            elif destination.objectName()=="Camera_2":
                  
                self.camera_2.setText(new_Camera)
                self.combobox7Selected(new_Camera)
            elif destination.objectName()=='Camera_3':
                
                self.camera_3.setText(new_Camera)
                self.combobox2Selected(new_Camera)
            elif destination.objectName()=="Camera_4":
                  
                self.camera_4.setText(new_Camera)
                self.combobox3Selected(new_Camera)
            elif destination.objectName()=='Camera_5':
               
                self.camera_5.setText(new_Camera)
                self.combobox9Selected(new_Camera)
            elif destination.objectName()=="Camera_6":
             
                self.camera_6.setText(new_Camera)
                self.combobox8Selected(new_Camera)
            elif destination.objectName()=='Camera_7':
                
                self.camera_7.setText(new_Camera)
                self.combobox4Selected(new_Camera)
            elif destination.objectName()=="Camera_8":
                
                self.camera_8.setText(new_Camera)
                self.combobox5Selected(new_Camera)
            elif destination.objectName()=='Camera_9':
                
                self.camera_9.setText(new_Camera)
                self.combobox11Selected(new_Camera)
            elif destination.objectName()=="Camera_10":
                
                self.camera_10.setText(new_Camera)
                self.combobox10Selected(new_Camera)
            elif destination.objectName()=='Camera_11':
               
                self.camera_11.setText(new_Camera)
                self.combobox6Selected(new_Camera)
            elif destination.objectName()=="Camera_12":
                            
                self.camera_12.setText(new_Camera)
                self.combobox12Selected(new_Camera)
            # event.setDropAction(QtCore.Qt.CopyAction)
           
           
            event.accept()   
            
        else:
            event.ignore()  
            
def main() -> None:
    # Create a QApplication object. It manages the GUI application's control flow and main settings.
    # It handles widget specific initialization, finalization.
    # For any GUI application using Qt, there is precisely one QApplication object
    app = QApplication(sys.argv)
    # Create an instance of the class MainWindow.
    window = MainWindow()
    # Show the window.
    window.show()
    # Start Qt event loop.
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
 
 

   

 
