import os.path
import sys
from pascal_voc_io import XML_EXT
from pascal_voc_io import PascalVocWriter
from pascal_voc_io import PascalVocReader
from yolo_io import YoloReader
from yolo_io import YOLOWriter


try:
    from PyQt5.QtGui import QImage
except ImportError:
    from PyQt4.QtGui import QImage


#imgFolderPath = sys.argv[1]
#imgFolderPath = "/home/oem/Downloads/Data/yolo_txt"
#directory = "ConvertedPascalVOCFiles"
#path = os.path.join(imgFolderPath, directory)
#os.mkdir(path)

def yolo_to_voc(imgFolderPath):
	directory = "ConvertedPascalVOCFiles"
	path = os.path.join(imgFolderPath, directory)
	os.mkdir(path)
	
# Search all yolo annotation (txt files) in the folder path

# Add image files, classes.txt file to the annotation folder (containing txt files)

	for file in os.listdir(imgFolderPath):
    		if file.endswith(".txt") and file != "classes.txt":
        		print("Converting", file)

        		annotation_txt = os.path.splitext(file)[0]

        		imgPath = imgFolderPath + "/" + annotation_txt + ".jpg"

        		image = QImage()
        		image.load(imgPath)
        		imageShape = [image.height(), image.width(), 1 if image.isGrayscale() else 3]
        		imgFolderName = os.path.basename(imgFolderPath)
        		imgFileName = os.path.basename(imgPath)

        		writer = PascalVocWriter(imgFolderName, imgFileName, imageShape, localImgPath=imgPath)


        		# Read YOLO files
        		txt_path = imgFolderPath + "/" + file
        		Yolo_reader = YoloReader(txt_path, image)
        		shapes = Yolo_reader.getShapes()
        		num_of_box = len(shapes)

        		for i in range(num_of_box):
            			label = shapes[i][0]
            			xmin = shapes[i][1][0][0]
            			ymin = shapes[i][1][0][1]
            			x_max = shapes[i][1][2][0]
            			y_max = shapes[i][1][2][1]

            			writer.addBndBox(xmin, ymin, x_max, y_max, label, 0)

        	# Write the converted PascalVOC xml files into a new Directory
        		writer.save(targetFile= path + "/" + annotation_txt + ".xml")
        		

def voc_to_yolo(imgFolderPath):
	directory = "ConverterdYolotxtFiles"
	path = os.path.join(imgFolderPath, directory)
	os.mkdir(path)


	# Search all pascal annotation (xml files) in this folder
	for file in os.listdir(imgFolderPath):
    		if file.endswith(".xml"):
    			print("Converting", file)
        		annotation_xml = os.path.splitext(file)[0]
			
        		imagePath = imgFolderPath + "/" + annotation_xml + ".jpg"

        		image = QImage()
        		image.load(imagePath)
        		imageShape = [image.height(), image.width(), 1 if image.isGrayscale() else 3]
        		imgFolderName = os.path.basename(imgFolderPath)
        		imgFileName = os.path.basename(imagePath)
			
        		writer = YOLOWriter(imgFolderName, imgFileName, imageShape, localImgPath=imagePath)

        		# Read classes.txt
        		classListPath = imgFolderPath + "/" + "classes.txt"
        		classesFile = open(classListPath, 'r')
        		classes = classesFile.read().strip('\n').split('\n')
        		classesFile.close()

        		# Read VOC file
        		filePath = imgFolderPath + "/" + file
        		Voc_Reader = PascalVocReader(filePath, image)
        		shapes = Voc_Reader.getShapes()
        		num_boxes = len(shapes)

        		for i in range(num_boxes):
            			label = classes.index(shapes[i][0])
            			xmin = shapes[i][1][0][0]
            			ymin = shapes[i][1][0][1]
            			x_max = shapes[i][1][2][0]
            			y_max = shapes[i][1][2][1]

            			writer.addBndBox(xmin, ymin, x_max, y_max, label, 0)

        		writer.save(targetFile= path + "/" + annotation_xml + ".txt")
