import sys, getopt
import cv2
import numpy as np

def dodgeV2(image,mask):
  return cv2.divide(image,255-mask,scale=256)

def main(argv):
   inputfile = ''
   outputfile = ''
   try:
      opts, args = getopt.getopt(argv,"hi:o:",["ifile=","ofile="])
   except getopt.GetoptError:
      print ('img2sketch -i <inputfile> -o <outputfile>')
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
         print ('img2sketch -i <inputfile> -o <outputfile>')
         sys.exit()
      elif opt in ("-i", "--ifile"):
         inputfile = arg
      elif opt in ("-o", "--ofile"):
         outputfile = arg
   #print ('Input file is "', inputfile)
   #print ('Output file is "', outputfile)
   source_photo = cv2.imread(inputfile)
   scale_percent = 0.60

   width = int(source_photo.shape[1]*scale_percent)
   height = int(source_photo.shape[0]*scale_percent)

   dim = (width,height)

   resized = cv2.resize(source_photo,dim,interpolation = cv2.INTER_AREA)
    
   kernel_sharpening = np.array([[-1,-1,-1],[-1, 9,-1],[-1,-1,-1]])
    
   sharpened = cv2.filter2D(resized,-1,kernel_sharpening)
    
   gray = cv2.cvtColor(sharpened , cv2.COLOR_BGR2GRAY)

   inv = 255-gray
    
   gauss = cv2.GaussianBlur(inv,ksize=(15,15),sigmaX=0,sigmaY=0)
    
    
   pencil_photo = dodgeV2(gray,gauss)
    
   cv2.imwrite(outputfile,pencil_photo)

if __name__ == "__main__":
   main(sys.argv[0:]) #for using as a pypi package
   #main(sys.argv[1:]) for downloading .py file and executing
