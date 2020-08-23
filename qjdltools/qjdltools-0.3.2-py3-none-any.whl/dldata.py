'''
Tools collection of Data(np.ndarray) processing.

Version 1.0  2018-04-03 15:44:13 by QiJi
Version 1.5  2018-04-07 22:34:53 by QiJi
Version 2.0  2018-04-11 09:43:47 by QiJi
    Add MyData class, rename this model names and some functions name
Version 3.0  2018-10-25 16:59:23 by QiJi
'''
import os
import sys
import cv2
import numpy as np
from tqdm import tqdm
from .fileop import filelist


def get_label_info(file_path):
    """
    Retrieve the class names and label values for the selected dataset.
    Must be in CSV or Txt format!

    Args:
        file_path: The file path of the class dictionairy

    Returns:
        class_names: A list of class names.
        label values: A list per class's color values. [[0,0,0], [255,255,255], ]
    """
    import csv
    filename, exten = os.path.splitext(file_path)
    if not (exten == ".csv" or exten == ".txt"):
        return ValueError("File is not a CSV or TxT!")

    class_names, label_values = [], []
    with open(file_path, 'r') as f:
        file_reader = csv.reader(f, delimiter=',')
        row = next(file_reader)  # skip one line
        for row in file_reader:
            if row != []:
                class_names.append(row[0])
                label_values.append([int(row[1]), int(row[2]), int(row[3])])
    return class_names, label_values


def compute_class_weights(labels_dir, label_values):
    '''
    Arguments:
        labels_dir(list): Directory where the image segmentation labels are
        num_classes(int): the number of classes of pixels in all images

    Returns:
        class_weights(list): a list of class weights where each index represents
            each class label and the element is the class weight for that label.

    '''
    # TODO: need Test and Debug
    image_files = filelist(labels_dir, ifPath=True, extension='.png')
    num_classes = len(label_values)
    class_pixels = np.zeros(num_classes)
    total_pixels = 0.0

    for n in range(len(image_files)):
        image = cv2.imread(image_files[n], -1)
        for index, colour in enumerate(label_values):
            class_map = np.all(np.equal(image, colour), axis=-1)
            class_map = class_map.astype(np.float32)
            class_pixels[index] += np.sum(class_map)

        print("\rProcessing image: " + str(n) + " / " + str(len(image_files)), end="")
        sys.stdout.flush()

    total_pixels = float(np.sum(class_pixels))
    index_to_delete = np.argwhere(class_pixels == 0.0)
    class_pixels = np.delete(class_pixels, index_to_delete)
    class_weights = total_pixels / class_pixels
    class_weights = class_weights / np.sum(class_weights)

    return class_weights


# **********************************************
# *********** Data Post-treatment **************
# **********************************************
def bwmorph(image, kernel_1=None, kernel_2=None):
    '''
    Do BW morphologic pocessing in label.

    Args:
        image: Tnput image, better be [HW].(also support [HW1] and [HWC])
        kernel_1: The kernel for closses

    Returns:
        image: [HW] label

    Notice: If input label is a multiply channel img, will only keep
        its first channel, then do morphologic pocessing.
    '''
    kernel_0 = np.array([[0, 0, 1, 0, 0],
                         [0, 1, 1, 1, 0],
                         [1, 1, 1, 1, 1],
                         [0, 1, 1, 1, 0],
                         [0, 0, 1, 0, 0]],
                        dtype=np.uint8)
    if kernel_1 is None:
        kernel_1 = kernel_0
    if kernel_2 is None:
        kernel_2 = kernel_0

    if len(image.shape) > 2:
        if image.shape[2] == 3:
            image = image[:, :, 0]
        elif image.shape[2] == 1:
            image = image[:, :, 0]
        else:
            ValueError("What a fucking image U choose?")

    # 闭运算-用[5x5](默认)kernel连接细小断裂
    image = cv2.erode(cv2.dilate(image, kernel_1), kernel_1)

    # 开运算-用[5x5]kernel去除细微噪点
    # kernel = np.ones([5, 5], dtype=np.uint8)
    image = cv2.dilate(cv2.erode(image, kernel_2), kernel_2)

    return image


def vote_combine(label, crop_params, crop_info, mode, scale=False):
    '''
    Combine small scale predicted label into a big one,
    for 1.classification or 2.semantic segmantation.
    Args:
        label: One_hot label(may be tensor). 1.[NC]; 2.[NHWC]
        crop_params: [sub_h, sub_w, crop_stride]
        crop_info: [rows, cols]
            rows: Num of images in the row direction.
            cols: Num of images in the col direction.
        mode: 1-classification, 2-semantic segmantation.
        scale: If do adaptive normalize.
    Returns:
        out_label: [HWC] one hot array, uint8.
    '''
    rows, cols = crop_info
    h, w, stride = crop_params
    label = np.array(label)  # Tensor -> Array
    if mode == 1:
        # 1. For classification
        if len(label.shape) == 3:  # list转array后会多出一维
            label = np.squeeze()
    elif mode == 2:
        # 2. For semantic segmantation
        if len(label.shape) == 5:  # in case of label is [1NHWC]
            label = label[0]
    else:
        return ValueError('Incorrect mode!')
    out_h, out_w = (rows-1)*stride+h, (cols-1)*stride+w
    out_label = np.zeros([out_h, out_w, label.shape[-1]], dtype=label.dtype)  # [HWC]

    y = 0  # y=h=row
    for i in range(rows):
        x = 0  # x=w=col
        for j in range(cols):
            out_label[y:y+h, x:x+w] += label[i*cols+j]  # 此处融合用加法
            x += stride
        y += stride

    # 自适应归一化
    if scale:
        m = np.max(out_label, axis=-1, keepdims=True).repeat(2, -1)
        n = np.min(out_label, axis=-1, keepdims=True).repeat(2, -1)
        out_label = out_label / (m - n)
    return out_label  # np.uint8(out_label)


def modefilter(label):
    '''找到label matrix中所有的无类别值(0)，用8连通区的众数给其赋值'''
    # TODO:How to solve the problem of boundary.
    newlabel = label.copy()
    indlist = np.argwhere(label == 0)
    for [r, c] in indlist:  # ind - [r, c]
        try:
            connected = label[r-1:r+1, c-1:c+1]
            mode = np.argmax(np.bincount(connected))
        except Exception:
            mode = 0
        newlabel[r, c] = mode
    return newlabel


def classifydataset_init(root, category, ratio=[0.5, 0.3, 0.2], full_train=False, mode=0, seed=0):
    '''
    分类数据初始化， 即获得训练(测试)集的所有文件路径及其标签
    Args:
        root - The dir of the train(test) dataset folder.
        ratio - [train, val, test] or [train, val]
            Note: 在2、3种模式下, ratio[0]默认为0,
                若为1则表示train_set包含train/val/test所有数据
        mode - 文件的组织结构不同
            1: 不同类别分文件夹放置
            2: 预测划分了train/val/test
        full_train - wether return all the images for train
    '''
    init_dataset = {k: {} for k in ['train', 'val', 'test']}
    cls_table = category.table

    if mode == 1:
        # loop floders
        for f in sorted(os.listdir(root)):
            cls = cls_table[f]
            img_names = sorted(os.listdir(root + '/' + f))
            samples = [(root+'/'+f+'/'+x, cls) for x in img_names]
            n = len(img_names)
            train_num, val_num = int(n * ratio[0]), int(n * ratio[1])
            if full_train:
                init_dataset['train'].update({f: samples[:]})
            else:
                init_dataset['train'].update({f: samples[: train_num]})
            init_dataset['val'].update({f: samples[train_num: train_num + val_num]})
            init_dataset['test'].update({f: samples[train_num + val_num:]})

    elif mode == 2:
        for split in ['train', 'val', 'test']:
            data_dir = root + '/' + split
            if os.path.exists(data_dir):
                for f in sorted(os.listdir(data_dir)):
                    cls = cls_table[f]
                    img_names = sorted(os.listdir(data_dir + '/' + f))
                    samples = [(data_dir+'/'+f+'/'+x, cls) for x in img_names]
                    init_dataset[split].update({f: samples})
                    if full_train and split != 'train':
                        if len(samples) == 0:
                            continue
                        init_dataset['train'][f].extend(samples)
            else:
                print('No %sing set found at: %s.' % (split, data_dir))

    return init_dataset


def segdataset_init(root, dtype, full_train=False, mode=0, seed=0):
    '''
    Initilize the segmentation dataset dict:
        {'train': {'image': {'RGB': [img_pths], 'SAR': [img_pths], ...},
                   'label': [lbl_pths]},
         'val': {'image': {'RGB': [img_pths], 'SAR': [img_pths]},
                 'label': [lbl_pths]},
        }
    Args:
        root - The dir of the train(test) dataset folder.
        dtype - The type of data, ['RGB', 'SAR']
        mode - 文件的组织结构不同
            0: 预测划分了train/val/test but only RGB data
            1: 预测划分了train/val/test and have multi-datatype
        full_train - wether return all the images for train
    '''
    init_dataset = {k: {'image': {}, 'label': []} for k in ['train', 'val', 'test']}
    lbl_dir_suffix = ''
    for suffix in ['_lbl', '_label', '_labels']:
        for sp in ['train', 'val', 'test']:
            test_pth = root + '/' + sp + suffix
            if os.path.exists(test_pth):
                lbl_dir_suffix = suffix
                break

    if mode == 0:
        for sp in ['train', 'val', 'test']:
            lbl_dir = root + '/' + sp + lbl_dir_suffix
            if os.path.exists(lbl_dir):
                lbl_pths = filelist(lbl_dir, ifPath=True)
                init_dataset[sp]['label'] = lbl_pths
                if full_train and sp != 'train':
                    init_dataset['train']['label'] += lbl_pths
            else:
                print('No %sing set label found at: %s.' % (sp, lbl_dir))
            img_dir = root + '/' + sp
            if os.path.exists(img_dir):
                img_pths = filelist(img_dir, ifPath=True)
                init_dataset[sp]['image']['RGB'] = img_pths
                if full_train and sp != 'train':
                    init_dataset['train']['image']['RGB'] += img_pths
            else:
                print('No %sing set image found at: %s.' % (sp, img_dir))

    elif mode == 1:
        for sp in ['train', 'val', 'test']:
            lbl_dir = root + '/' + sp + lbl_dir_suffix
            if os.path.exists(lbl_dir):
                lbl_pths = filelist(lbl_dir, ifPath=True)
                init_dataset[sp]['label'] = lbl_pths
                if full_train and sp != 'train':
                    init_dataset['train']['label'] += lbl_pths
            else:
                print('No %sing set label found at: %s.' % (sp, lbl_dir))
            for dt in dtype:
                img_dir = root + '/%s_%s' % (sp, dt)
                if os.path.exists(img_dir):
                    img_pths = filelist(img_dir, ifPath=True)
                    init_dataset[sp]['image'][dt] = img_pths
                    if full_train and sp != 'train':
                        init_dataset['train']['image'][dt] += img_pths
                else:
                    print('No %sing set image type of %s found at: %s.' % (sp, dt, img_dir))
    return init_dataset


# **********************************************
# ************ Main functions ******************
# **********************************************
def data_statistics():
    ''' Count (pixel-level) mean and variance of dataset. '''
    dir_list = [
        '/home/tao/Data/RBDD/train',
    ]  # list of data folder dir.

    mean = np.array([0, 0, 0], np.float32)  # BGR
    # std = np.array([0, 0, 0],  np.float32)  # BGR
    total_image = 0
    # Statisify mean and std
    for folder in dir_list:
        image_paths = filelist(folder, ifPath=True)
        for path in tqdm(image_paths):
            img = cv2.imread(path, cv2.IMREAD_COLOR)  # BGR
            img = np.float32(img) / 255.0
            # images.append(np.expand_dims(img))
            mean += np.mean(np.mean(img, 0), 0)
            total_image += 1
    mean /= total_image  # get pixel-level BGR mean
    # Statisify std
    # for folder in dir_list:
    #     image_paths = filelist(folder, ifPath=True)
    #     for path in tqdm(image_paths):
    #         img = cv2.imread(path, cv2.IMREAD_COLOR)  # BGR
    #         img = np.float32(img) / 255.0
    #         X = img-mean
    #         X = X*X
    #         std += np.sum(np.sum(X, axis=0), axis=0)
    # std /= total_image
    print('mean=', mean)
    # print('std=', std)
    print('Careful: BGR!')
    # return mean, std


def spilt_dataset(in_floders, out_floders, rate=0.025, max_num=None):
    '''Spilt images(maybe with labels)
    Args:
        in_floders - list of input floders
        out_floders - list of output floders
            for example:
                in_floders = [
                    'dataset_dir/train',
                    'dataset_dir/train_labels'
                ]
                out_floders = [
                    'dataset_dir/val',
                    'dataset_dir/val_labels'
                ]
    '''
    from shutil import move
    # from sklearn.model_selection import train_test_split

    name_list = []
    for d in in_floders:
        names = filelist(d)
        name_list.append(names)
    file_num = len(name_list[0])  # 文件总数
    max_num = file_num if max_num is None else max_num

    # 按比例抽取
    index = np.random.permutation(file_num)
    index = index[:int(file_num*rate)]

    for d, names in zip(range(len(in_floders)), name_list):
        print(in_floders[d])
        cnt = 0
        for i in index:
            # 针对文件的操作
            # os.remove(d+'/'+names[i])
            move(in_floders[d]+'/'+names[i], out_floders[d]+'/'+names[i])
            cnt += 1
            if cnt >= max_num:
                break  # if set max_num, prioritize the max_num

    print('Finished!')


def MorphologicPostTreate(input_dir, output_dir):
    '''
    形态学后处理
    '''
    image_names = filelist(input_dir)
    kernel = np.ones([7, 7], dtype=np.uint8)
    kernel[0, 0], kernel[-1, -1], kernel[0, -1], kernel[-1, 0] = 0, 0, 0, 0
    # print(kernel)

    for i in tqdm(range(len(image_names))):
        img = cv2.imread(input_dir + "/" + image_names[i], -1)
        img = bwmorph(img, kernel_1=kernel)  # 输出[HW]label
        img = np.repeat(np.expand_dims(img, axis=2), 3, axis=2)
        cv2.imwrite(output_dir + "/" + image_names[i], img)


def main():
    pass


if __name__ == '__main__':
    # main()
    data_statistics()
    # spilt_dataset(max_num=1000)
    pass
