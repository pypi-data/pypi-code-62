"""
样本生成器
@author HeTongHao
@since 2020/8/25 17:02
"""
import os
import cv2
import time
import shutil
from datetime import datetime
from tools import os_tools
from datasetGenerate.tag_window import TagWindow


class GetSample:

    def get_samples(self, ori_img_path) -> list:
        return []


class Sample:
    def __init__(self, sample_img):
        self.sample_img = sample_img
        self.tag = None

    def save_to(self, save_path):
        img_name = '{}.jpg'.format(str(time.time()))
        try:
            last_save_dir = os.path.join(save_path, self.tag)
            os_tools.ensure_path_exists(last_save_dir)
            cv2.imwrite(os.path.join(last_save_dir, self.tag + '-' + img_name), self.sample_img)
        except Exception as e:
            print(e)


class DataSource:
    def __init__(self, get_sample, source_dir, file_name):
        """
        数据源（可以是一张原图）
        :param get_sample: 获取样本的实例
        :param source_dir:  数据源所在文件夹
        :param file_name:  文件名称
        """
        self.source_dir = source_dir
        self.file_name = file_name
        self.full_path = os.path.join(self.source_dir, self.file_name)
        self.samples = [Sample(sample) for sample in get_sample.get_samples(self.full_path)]

    def tag_samples_to(self, tag):
        """
        标记所有样本
        :return:
        """
        for sample in self.samples:
            sample.tag = tag

    def save_samples(self, save_path):
        """
        保存所有样本
        :param save_path: 保存目录
        :return:
        """
        for sample in self.samples:
            sample.save_to(save_path)

    def move_to(self, marked_dir):
        os_tools.ensure_path_exists(marked_dir)
        shutil.move(self.full_path, os.path.join(marked_dir, self.file_name))


class SampleGenerate:
    def __init__(self, get_sample: GetSample, source_dir, dist_base_path='dataSets'):
        self.get_sample = get_sample
        self.source_dir = source_dir
        self.all_sample_dir = os.path.join(dist_base_path, 'all_sample')
        self.train_dir = os.path.join(dist_base_path, 'train')
        self.validation_dir = os.path.join(dist_base_path, 'validation')
        self.test_dir = os.path.join(dist_base_path, 'test')
        # 标记完毕，将原始图片移动到这个文件夹
        self.marked_dir = os.path.join(dist_base_path, 'marked')
        self.time_sub_marked_dir = os.path.join(self.marked_dir, datetime.now().strftime('%Y-%m-%d_%H_%M_%S'))
        # 确保文件夹已存在
        os_tools.ensure_path_exists(self.all_sample_dir, self.train_dir, self.validation_dir, self.test_dir,
                                    self.marked_dir)
        self.data_source_list = []
        self.tag_window = None

    def gen_all_sample(self):
        file_names = os.listdir(self.source_dir)
        for file_name in file_names:
            self.data_source_list.append(DataSource(self.get_sample, self.source_dir, file_name))
        print('所有样本已生成')

    def assign_sample(self, train_scale=0.35, validation_scale=0.15, test_scale=0.5):
        tag_samples_file_dict = {}
        for root, tag_dirs, files in os.walk(self.all_sample_dir):
            if self.all_sample_dir != root:
                tag = os.path.basename(root)
                tag_samples_file_dict[tag] = [os.path.join(root, file_name) for file_name in files]
        standard = train_scale + validation_scale + test_scale
        train_scale = train_scale / standard
        validation_scale = validation_scale / standard
        for tag, files in tag_samples_file_dict.items():
            # 保证三个文件夹存在
            train_tag_dir = os.path.join(self.train_dir, tag)
            validation_tag_dir = os.path.join(self.validation_dir, tag)
            test_tag_dir = os.path.join(self.test_dir, tag)
            os_tools.ensure_path_exists(train_tag_dir, validation_tag_dir, test_tag_dir)
            # 计算三个数据集分配数量
            file_count = len(files)
            train_count = int(file_count * train_scale)
            validation_count = int(file_count * validation_scale)
            for train_sample_file in files[:train_count]:
                os_tools.copy_file_to_dir(train_sample_file, train_tag_dir)
            for validation_sample_file in files[train_count:train_count + validation_count]:
                os_tools.copy_file_to_dir(validation_sample_file, validation_tag_dir)
            for test_sample_file in files[train_count + validation_count:]:
                os_tools.copy_file_to_dir(test_sample_file, test_tag_dir)
            print('标签为[%s]的%s个样本分配完毕:' % (tag, file_count))
            print('train sample count:', train_count)
            print('validation sample count:', validation_count)
            print('test sample count:', file_count - train_count - validation_count)
            print('--------------------------------------------')

    def start_tag_window(self, tags):
        print('启动手动标定ui线程')
        self.tag_window = TagWindow(tags)
        self.tag_window.mainloop()

    def manually_tag_samples(self, tags):
        """
        手动标定
        :return:
        """
        import _thread
        _thread.start_new_thread(self.start_tag_window, (tags,))
        while self.tag_window is None:
            time.sleep(0.01)
        for data_source in self.data_source_list:
            for sample in data_source.samples:
                self.tag_window.next_sample(sample.sample_img)
                sample.tag = self.tag_window.tag_queue.get()
                print('手动标定：', sample.tag)
                sample.save_to(self.all_sample_dir)
            data_source.move_to(self.time_sub_marked_dir)

    def unite_tag_samples(self, tag):
        """
        统一标定为同一个标签
        :param tag: 统一标定标签
        :return:
        """
        for data_source in self.data_source_list:
            # 全部标记为
            data_source.tag_samples_to(tag)
            # 保存样本
            data_source.save_samples(self.all_sample_dir)
            # 移动数据源到标记完毕的目录
            data_source.move_to(self.time_sub_marked_dir)


# from vision.Vision import Vision
# class GetCeramicsSample(GetSample):
#     def __init__(self):
#         self.v = Vision()
#
#     def get_samples(self, ori_img_path):
#         ori_img = cv2.imread(ori_img_path, 0)
#         self.v.gen_train_data(ori_img)
#         return [ceramics.predict_img for ceramics in self.v.all_exists_ceramics_list]


# if __name__ == '__main__':
#     generate = SampleGenerate(GetSample(), r'E:\project\keraster\datasetGenerate\facade')
#     generate.gen_all_sample()
#     # 手动标定
#     # generate.manually_tag_samples(['facade', 'reverse'])
#     # 统一标定
#     generate.unite_tag_samples('facade')
#     # 分配样本
#     generate.assign_sample(train_scale=0.35, validation_scale=0.15, test_scale=0.5)
