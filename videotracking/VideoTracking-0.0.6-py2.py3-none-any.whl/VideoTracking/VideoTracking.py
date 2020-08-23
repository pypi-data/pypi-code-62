# PyQt5 Video player
#!/usr/bin/env python

import argparse
import logging
from datetime import datetime, timedelta

__version_info__ = ('0', '0', '6')
__version__ = '.'.join(__version_info__)

# from VideoTrackingWindowWindow import Ui_VideoTrackingWindowWindow
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtCore import QDir, Qt, QUrl, pyqtSignal, QPoint, QRect, QObject
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer, QVideoFrame, QAbstractVideoSurface, QAbstractVideoBuffer, QVideoSurfaceFormat, QVideoProbe
from PyQt5.QtMultimediaWidgets import QVideoWidget, QGraphicsVideoItem
from PyQt5.QtWidgets import (QApplication, QFileDialog, QHBoxLayout, QLabel,
                             QPushButton, QSizePolicy, QSlider, QStyle, QVBoxLayout, QWidget,
                             QMainWindow, QPushButton, QAction, QListWidget, QListWidgetItem)
from PyQt5.QtGui import QIcon, QPainter, QImage, QPen, QPixmap, QColor
import sys
import os
import os.path as osp
import numpy as np
import cv2


class VideoTrackingWindow(QMainWindow):

    def __init__(self, parent=None):
        super(VideoTrackingWindow, self).__init__(parent)
        # Load UI
        uic.loadUi('VideoTrackingWindow.ui', self)

        # setup media player
        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        self.videoProbe = QVideoProbe()
        self.videoFrame = QVideoFrame()

        #set Icon for buttons
        self.playButton.setIcon(
            self.style().standardIcon(QStyle.SP_MediaPlay))
        self.nextButton.setIcon(
            self.style().standardIcon(QStyle.SP_MediaSkipForward))
        self.prevButton.setIcon(
            self.style().standardIcon(QStyle.SP_MediaSkipBackward))
        self.fastButton.setIcon(
            self.style().standardIcon(QStyle.SP_MediaSeekForward))
        self.slowButton.setIcon(
            self.style().standardIcon(QStyle.SP_MediaSeekBackward))

        # setup connection
        self.playButton.clicked.connect(self.playPause)
        self.nextButton.clicked.connect(self.nextFrame)
        self.prevButton.clicked.connect(self.prevFrame)
        self.fastButton.clicked.connect(self.fastPlayback)
        self.slowButton.clicked.connect(self.slowPlayback)
        self.positionSlider.sliderMoved.connect(self.setPosition)
        self.actionOpen_Video.triggered.connect(self.openVideo)
        self.actionSave_Annotation.triggered.connect(self.saveAnnotations)
        self.actionExit.triggered.connect(self.exitCall)

        # Setup the Media Player
        self.mediaPlayer.setVideoOutput(self.videoWidget)
        self.videoProbe.setSource(self.mediaPlayer)
        self.videoProbe.videoFrameProbed.connect(self.probeFrame)
        self.mediaPlayer.stateChanged.connect(self.mediaStateChanged)
        self.mediaPlayer.positionChanged.connect(self.positionChanged)
        self.mediaPlayer.durationChanged.connect(self.durationChanged)
        self.mediaPlayer.error.connect(self.handleError)

        # Set Tracking
        # self.listTracker=[]
        self.addTracker.clicked.connect(self.addTrackerClicked)
        self.stopTracker.clicked.connect(self.stopTrackerClicked)
        self.runTracker.clicked.connect(self.runTrackerClicked)
        self.currentlyTracking = False
        self.FPS=30

        # print("set rectangle color and thickness")
        self.penRectangle = QPen(QtCore.Qt.red)
        self.penRectangle.setWidth(10)

        self.logging("Application initialized")


    @property
    def DeltaT(self):
        return 1000/self.FPS

    def playPause(self):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.mediaPlayer.pause()
        else:
            self.mediaPlayer.play()

    def mediaStateChanged(self, state):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.playButton.setIcon(
                self.style().standardIcon(QStyle.SP_MediaPause))
        else:
            self.playButton.setIcon(
                self.style().standardIcon(QStyle.SP_MediaPlay))

    def positionChanged(self, position):
        self.positionSlider.setValue(position)
        self.checkIfTracking.setChecked(self.isTracking())
        self.centralwidget.setEnabled(not self.isTracking())
        strPosition = str(timedelta(seconds=int(self.mediaPlayer.position()/1000)))
        strDuration = str(timedelta(seconds=int(self.mediaPlayer.duration()/1000)))
        self.timeLabel.setText(f"{strPosition}/{strDuration}")

    def durationChanged(self, duration):
        self.positionSlider.setRange(0, duration)

    def setPosition(self, position):
        self.mediaPlayer.setPosition(int(position/self.DeltaT)*self.DeltaT)
        self.logging(f"Position set at time: {self.mediaPlayer.position()/1000:.3f} s")

    def nextFrame(self):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.mediaPlayer.pause()

        self.mediaPlayer.setPosition(
            int(self.mediaPlayer.position()+self.DeltaT))
        self.mediaPlayer.play()
        self.mediaPlayer.pause()
        self.logging(
            f"Position set at time: {self.mediaPlayer.position()/1000:.3f} s")

    def prevFrame(self):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.mediaPlayer.pause()

        self.mediaPlayer.setPosition(
            int(self.mediaPlayer.position()-self.DeltaT))
        self.mediaPlayer.play()
        self.mediaPlayer.pause()
        self.logging(
            f"Position set at time: {self.mediaPlayer.position()/1000:.3f} s")

    def fastPlayback(self):
        self.mediaPlayer.setPlaybackRate(self.mediaPlayer.playbackRate()*2.0)
        self.logging(
            f"Playback speed set to {self.mediaPlayer.playbackRate()}x")

    def slowPlayback(self):
        self.mediaPlayer.setPlaybackRate(self.mediaPlayer.playbackRate()/2.0)
        self.logging(
            f"Playback speed set to {self.mediaPlayer.playbackRate()}x")

    def handleError(self):
        self.centralwidget.setEnabled(False)
        self.logging("Error: " + self.mediaPlayer.errorString())

    def logging(self, message):
        logging.info(message)
        self.statusBar.showMessage(message)

    def openVideo(self, filename=False):
        if not filename:
            filename, _ = QFileDialog.getOpenFileName(self, "Open Video",
                                                      QDir.homePath())
        self.path = osp.dirname(str(filename))
        if filename != '':
            self.filename = filename
            # read FPS
            cap = cv2.VideoCapture(filename)
            self.FPS = cap.get(cv2.CAP_PROP_FPS)
            self.logging(f"FPS read: {self.FPS} fps")
            # read Media
            self.mediaPlayer.setMedia(
                QMediaContent(QUrl.fromLocalFile(filename)))
            self.centralwidget.setEnabled(True)
            self.logging(f"Video {filename} opened")

            # self.mediaPlayer.play()
            self.mediaPlayer.pause()

    def saveAnnotations(self, filename=False):
        filename = os.path.splitext(self.filename)[0]+".txt"

        # if not filename:
        #     filename, _ = QFileDialog.getOpenFileName(self, "Where to save",
        #                                               QDir.homePath())

        if filename == '':
            self.logging("Please select a path to save the annotations")
            return
        with open(filename, "w") as file_object:

            for i in range(self.listTracker.count()):
                this_item = self.listTracker.item(i)
                this_tracker = self.listTracker.itemWidget(this_item)
                this_tracker.boxes
                for k, box in this_tracker.boxes.items():
                    lineBB = f"{int(k):016d}, {box.x()}, {box.y()}, {box.width()}, {box.height()} \n"
                    print(lineBB)
                    file_object.write(lineBB)



    def exitCall(self):
        self.logging("Exiting the application")
        sys.exit(app.exec_())

    def probeFrame(self, frame):
        self.videoFrame = frame
        self.videoFrame.map(QAbstractVideoBuffer.ReadOnly)

        if self.currentlyTracking:
            self.showThumbNail()

    # def processFrame(self):
    #     # https://stackoverflow.com/questions/27829830/convert-qvideoframe-to-qimage/63403295#63403295?newreg=72d00ff1bb8a480883ac4d573cec801a

    #     self.image = QVideoFrame(self.videoFrame).image().convertToFormat(4)
    #     # ret = self.image.save(f'frame_pos{self.mediaPlayer.position()}.jpg')

    #     ptr = self.image.bits()
    #     ptr.setsize(self.image.byteCount())
    #     img_np = np.array(ptr).reshape(
    #         self.image.height(), self.image.width(), 4)  # Copies the data

    #     cv2.imwrite(f'framecv_pos{self.mediaPlayer.position()}.jpg', img_np)

    def showThumbNail(self):

        myQImage = QVideoFrame(self.videoFrame).image().convertToFormat(4)
        # myPixMap = QPixmap.fromImage(myQImage)
        # myPixMap = myPixMap.scaled(1200, 1200, QtCore.Qt.KeepAspectRatio)

        # painterInstance = QPainter(myPixMap)

        # pos = self.mediaPlayer.position()

        # print("draw rectangle on painter")
        # painterInstance.setPen(self.penRectangle)
        # for i in range(self.listTracker.count()):
        #     this_item = self.listTracker.item(i)
        #     this_tracker = self.listTracker.itemWidget(this_item)
            
        #     if str(pos) in this_tracker.boxes:
        #         box = this_tracker.boxes[str(pos)]
        #         print("   Tracker", i, box)

        #         painterInstance.drawRect(box)

        # print("scaled")
        # # self.ui.label_imageDisplay.setPixmap(self.pixmap_image)
        # # self.ui.label_imageDisplay.show()


        # print("set pixmap onto the label widget")
        # self.boxLabel.setPixmap(myPixMap)
        # print("done Thumbnail")

    def isTracking(self, pos = None):
        if pos is None:
            pos = self.mediaPlayer.position()

        for i in range(self.listTracker.count()):
            this_item = self.listTracker.item(i)
            this_tracker = self.listTracker.itemWidget(this_item)
            if this_tracker.isTracking(pos):
                return True
        return False

    def runTrackerClicked(self):
        previousPos = self.mediaPlayer.position()
        self.mediaPlayer.setPosition(
            int(self.mediaPlayer.position()+self.DeltaT))
        currentPos = self.mediaPlayer.position()


        for i in range(self.listTracker.count()):
            this_item = self.listTracker.item(i)
            this_tracker = self.listTracker.itemWidget(this_item)
            if this_tracker.isTracking(currentPos):


                qimage = self.videoFrame.image().convertToFormat(4)
                ptr = qimage.bits()
                ptr.setsize(qimage.byteCount())
                img = np.array(ptr).reshape(
                    qimage.height(), qimage.width(), 4)  # Copies the data
                img = img[:,:,:3]
                print(img.shape)
                cv2.imwrite(f'framecv_pos{currentPos}.jpg', img)

                (success, box) = this_tracker.tracker.update(img)
                print("success", success)

                new_frame = qimage.copy()
                new_box = QRect(this_tracker.box2rect(box)) #QRect(this_tracker.boxes[str(previousPos)])

                this_tracker.boxes[str(currentPos)] = new_box
                this_tracker.frames[str(currentPos)] = new_frame


    def stopTrackerClicked(self):
        current_item = self.listTracker.currentItem()
        current_tracker = self.listTracker.itemWidget(current_item)
        if current_tracker.isTracking(self.mediaPlayer.position()):
            current_tracker.time_stop = self.mediaPlayer.position()
            current_tracker.updateItem()
            self.centralwidget.setEnabled(not self.isTracking())
        else:
            self.logging("Tracker already done")
        # print(current_tracker)


    def addTrackerClicked(self):
        self.currentlyTracking = True

        qimage = self.videoFrame.image().convertToFormat(4)
        ptr = qimage.bits()
        ptr.setsize(qimage.byteCount())
        img = np.array(ptr).reshape(
            qimage.height(), qimage.width(), 4)  # Copies the data

        display_name = f'Display: Draw Initial Bounding Box'
        cv2.imshow(display_name, img)
        valid_selection = False
        init_state = [0, 0, 0, 0]

        while not valid_selection:
            frame_disp = img.copy()

            cv2.putText(frame_disp, 'Select target ROI and press ENTER [ESC to use previous BB]', (20, 30), cv2.FONT_HERSHEY_COMPLEX_SMALL,
                        1.5, (0, 0, 0), 1)

            x, y, w, h = cv2.selectROI(
                display_name, frame_disp, fromCenter=False)
            init_state = [x, y, w, h]
            valid_selection = np.sum(init_state)
            if cv2.waitKey(0) == 27:
                cv2.destroyAllWindows()
                break
        cv2.destroyAllWindows()
        print("annot", init_state)


        new_tracker = Tracker(time_start=self.mediaPlayer.position(),
                              time_stop=self.mediaPlayer.duration(),
                              init_QImage=qimage,
                              init_box=init_state,
                              FPS=self.FPS)


        item = QListWidgetItem(self.listTracker)
        item.setSizeHint(new_tracker.minimumSizeHint())


        self.listTracker.addItem(item)

        self.listTracker.setItemWidget(item, new_tracker)
        self.listTracker.setCurrentItem(item)

        self.stopTracker.setEnabled(self.listTracker.count() > 0)
        print(self.isTracking())
        self.centralwidget.setEnabled(not self.isTracking())

        self.showThumbNail()


# def cropQImage()

OPENCV_OBJECT_TRACKERS = {
    "csrt": cv2.TrackerCSRT_create,
    "kcf": cv2.TrackerKCF_create,
    "boosting": cv2.TrackerBoosting_create,
    "mil": cv2.TrackerMIL_create,
    "tld": cv2.TrackerTLD_create,
    "medianflow": cv2.TrackerMedianFlow_create,
    "mosse": cv2.TrackerMOSSE_create
}


class Tracker(QWidget):
    def __init__(self, time_start, time_stop, init_box, init_QImage, FPS, parent=None):
        super(Tracker, self).__init__(parent)
        self.time_start = time_start
        print(time_start)
        self.time_stop = time_stop
        print(time_stop)
        self.FPS = FPS
        self.trackingAlgorithm = None
        self.boxes = {f"{self.time_start}": self.box2rect(init_box)}
        self.frames = {f"{self.time_start}": init_QImage}

        pixmap = QPixmap.fromImage(init_QImage)
        pixmap = pixmap.copy(self.boxes[str(self.time_start)])
        pixmap = pixmap.scaled(20, 20, QtCore.Qt.KeepAspectRatio)        
        self.iconQLabel = QLabel()
        self.iconQLabel.setPixmap(pixmap)

        self.nameQLabel = QLabel()
        self.nameQLabel.setText(self.getName())

        self.row = QHBoxLayout()
        self.row.addWidget(self.iconQLabel)
        self.row.addWidget(self.nameQLabel)
        self.setLayout(self.row)

        self.tracker = OPENCV_OBJECT_TRACKERS["kcf"]()

        # self.image = QVideoFrame(self.videoFrame).image().convertToFormat(4)
        # ret = self.image.save(f'frame_pos{self.mediaPlayer.position()}.jpg')

        ptr = init_QImage.bits()
        ptr.setsize(init_QImage.byteCount())
        CVImage = np.array(ptr).reshape(init_QImage.height(), init_QImage.width(), 4) 

        cv2.imwrite(f'framecv_pos{self.time_start}.jpg', CVImage)
        print(tuple(init_box))
        self.tracker.init(CVImage, tuple(init_box))


    @property
    def DeltaT(self):
        return 1000/self.FPS

    def __getitem__(self,i):
        key = int(self.time_start + i*self.DeltaT)
        box = self.boxes[key]
        frame = self.frames[key]
        return box, frame


    def isTracking(self, pos): 
        return not self.afterTracking(pos) and not self.beforeTracking(pos)

    def afterTracking(self, pos): 
        return pos >= self.time_stop

    def beforeTracking(self, pos):
        return pos < self.time_start


    def updateItem(self):
        self.nameQLabel.setText(self.getName())

    def box2rect(self, box):
        return QRect(box[0], box[1], box[2], box[3])

    def printRect(self, rect):
        return f"X:{rect.center().x()}/Y:{rect.center().y()}"


    def getName(self):
        return f"From {self.time_start/1000}s to {self.time_stop/1000}s centered in {self.printRect(self.boxes[str(self.time_start)])}"

    def addBox(self, box):
        self.boxes.append(box)

    def processNextFrame(self, frame):
        if len(self.boxes) == 0:
            print("Initialize the first BB!")
            return

        # no tracking
        if self.trackingAlgorithm is None:
            new_box = self.boxes[-1].copy()

        self.addBox(new_box)


def main():
    app = QApplication(sys.argv)

    parser = argparse.ArgumentParser(
        description="Image Labeler based on Active Learning")

    parser.add_argument("--videopath",
                        default=None,
                        type=str,
                        help="video to open")

    parser.add_argument("--logdir",
                        default="log",
                        type=str,
                        help="diretory for logging")

    parser.add_argument("--loglevel",
                        default="INFO",
                        type=str,
                        help="diretory for logging")
    args = parser.parse_args()

    numeric_level = getattr(logging, args.loglevel.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError('Invalid log level: %s' % args.loglevel)

    # set up logging configuration
    log_file = os.path.join(
        args.logdir, datetime.now().strftime('%Y-%m-%d %H-%M-%S.log'))
    os.makedirs(os.path.dirname(log_file), exist_ok=True)
    logging.basicConfig(
        level=numeric_level,  # INFO
        format="%(asctime)s [%(levelname)-5.5s]  %(message)s",
        handlers=[
            # file handler
            logging.FileHandler(log_file),
            # stream handler
            logging.StreamHandler()
        ])
    logging.info(f"Start logging on {log_file}")
    logging.info(f"Starting Videotracking version {__version__}")

    player = VideoTrackingWindow()
    player.resize(720, 480)
    player.showMaximized()

    if args.videopath is not None:
        player.openVideo(filename=args.videopath)

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()