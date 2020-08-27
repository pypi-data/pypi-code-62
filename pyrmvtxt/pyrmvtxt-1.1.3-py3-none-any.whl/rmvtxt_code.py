# -*- coding: utf-8 -*-
"""
Created on Thu Aug 27 2020

@author: supakrni
"""
#  Import libary
#  Main function to detect and remove text in the  images
def removetxt(Images):
    import gc
    import cv2
    import pandas as pd
    import keras_ocr # keras need gpu for computation
    from keras import backend as bek
    # Split Image into smaller part and do Text detect
    def additional_cropping_img(img, x1, x2, y1, y2, num, show=None):
        cropped_image = img[y1:y2, x1:x2]
        return cropped_image

    def Split_Img(img):
       # img_path = original_image_path
        splitted_img=[]
        splitted_img_name=[]
        #img = cv2.imread(img_path)
        # height, width, number of channels in image
        height = img.shape[0]
        width = img.shape[1]
        start_row, start_col = 0, 0
        i = 0
        j=0
        img_size=pd.DataFrame(columns=['Img_name','start_h','end_h','start_w','end_w'])
        for h in range(1, 3):
            if h > 1:
                start_row = end_row
                start_col = 0
            for w in range(1, 4):
                end_row, end_col = int(h*height/2), int(w*width/3)
                file_name="Original_" + '_' + str(i)
                splitted_img_name.append(file_name)
                cropped_image = img[start_row:end_row , start_col:end_col]
                img_size.loc[j]=[file_name,start_row,end_row,start_col,end_col]
                start_col = end_col
                splitted_img.append(cropped_image)
                i += 1
                j += 1
        # /*-------------------------- Crop additional images for replacing potential lost objects. ---------------------------*/
        # x = left to right  , y = top to bottom
            # 1. 
        x1 = int(width/4)
        x2 = int(5*width/12)
        y1 = 0
        y2 = int(height)
        file_name="Original_"+ '_add_' + str(0)
        splitted_img.append(additional_cropping_img(img, x1, x2, y1, y2, 0))
        img_size.loc[j]=[file_name,y1,y2,x1,x2]
        splitted_img_name.append(file_name)
        j += 1
        # 2. 
        x1 = int(7*width/12)
        x2 = int(3*width/4)
        y1 = 0
        y2 = int(height)
        file_name="Original_"+ '_add_' + str(1)
        splitted_img.append(additional_cropping_img(img, x1, x2, y1, y2, 1))
        img_size.loc[j]=[file_name,y1,y2,x1,x2]
        splitted_img_name.append(file_name)
        j += 1
        # 3.
        x1 = 0
        x2 = int(width)
        y1 = int(3*height/8)
        y2 = int(5*height/8)
        file_name="Original_"+ '_add_' + str(2)
        splitted_img.append(additional_cropping_img(img, x1, x2, y1, y2, 2))
        img_size.loc[j]=[file_name,y1,y2,x1,x2]
        splitted_img_name.append(file_name) 
        j += 1
#        print('***Split image succuess')
        return splitted_img,img_size,splitted_img_name

    # Main functions
    print("***** Start processing..")
    pipeline = keras_ocr.pipeline.Pipeline()
    #original_img = keras_ocr.tools.read(Images)
    original_img = Images
    splitted_img,img_size,splitted_img_name=Split_Img(Images)
    
    for i in range(len(splitted_img)):
        gc.collect()
        print("*** Start splitting ",i+1,"/",len(splitted_img))
        start_h=img_size[img_size.Img_name==splitted_img_name[i]].iloc[0,1]
        end_h=img_size[img_size.Img_name==splitted_img_name[i]].iloc[0,2]
        start_w=img_size[img_size.Img_name==splitted_img_name[i]].iloc[0,3]
        end_w=img_size[img_size.Img_name==splitted_img_name[i]].iloc[0,4]
        split_image =keras_ocr.tools.read(splitted_img[i])
        split_image_prediction_groups=pipeline.recognize([split_image])
#        print("***Detecting text in : ",splitted_img_name[i],)
        for j in range(len(split_image_prediction_groups[0])):
#            print("***",splitted_img_name[i],"detect box : ",j+1,"/",len(split_image_prediction_groups[0]))
            box=split_image_prediction_groups[0][j][1]
            # find Min X [0], Min Y [1], Max X[2] , Max Y[3]
            bbox_resize = [min([x[0] for x in box]), min([x[1] for x in box]),max([x[0] for x in box]), max([x[1] for x in box])]
            # convert into box size (x, y, w, h), img[y:y+h, x:x+w]
            location=[int(bbox_resize[1]),int(bbox_resize[3]), int(bbox_resize[0]),int(bbox_resize[2])]
            original_img[int(start_h+int(bbox_resize[1])):int(start_h+int(bbox_resize[3])),int(start_w+int(bbox_resize[0])):int(start_w+int(bbox_resize[2]))]=[255,255,255]
#        print('****Export result from : ',splitted_img_name[i])
    print('** Remove text success!!')
    del pipeline,splitted_img,img_size,splitted_img_name,start_h,end_h,start_w,end_w,split_image,split_image_prediction_groups,box,bbox_resize,location
    bek.clear_session()
    gc.collect()
    return  original_img
