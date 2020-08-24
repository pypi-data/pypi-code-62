import moyan


# from moyan.tools import walkDir2List, cv_read
# from moyan import w2l

# def w2l(win_path):
#     '''
#     windows path to linux
#     '''
#     return '/'.join(win_path.split('\\'))

# @moyan.decorator.time_cost
# def hello():
#     path = r'C:\Users\Moyan\Desktop\demo\demo.jpg'
#     # im = cv_read(path)
#     # print(im.shape)
#     print(path)
#     print(w2l(path))


# for i in range(20):
#     print(hello())  


input_json = r'D:\Dataset\TableBank_data\Detection_data\Word\Word.json'
input_img_dir = r'D:\Dataset\TableBank_data\Detection_data\Word\images'
output_dir = r'D:\Dataset\TableBank_data\Detection_data\Word\voc'


moyan.dettools.coco2voc(input_json, input_img_dir, output_dir)