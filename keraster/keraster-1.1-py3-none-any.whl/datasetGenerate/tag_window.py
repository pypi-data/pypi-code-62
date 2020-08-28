from tkinter import *
from PIL import Image, ImageTk
import queue


class TagWindow:
    def __init__(self, tags):
        self.tag_queue = queue.Queue(maxsize=0)
        self.current_view_img = None
        # 构建ui组件
        self.window = Tk()
        self.window.title("样本标定工具")
        self.image_view_frame = Frame(self.window, width=100, height=80)
        self.image_view_frame.pack()
        self.button_frame = Frame(self.window, width=100, height=80)
        self.button_frame.pack()

        self.imgView = Label(self.image_view_frame)
        self.imgView.grid(row=0)

        self.gen_all_tag_button(tags)

    def mainloop(self):
        self.window.mainloop()

    def show_image_path(self, img_path):
        img_open = Image.open(img_path)
        self.current_view_img = ImageTk.PhotoImage(img_open)
        self.imgView.config(image=self.current_view_img)

    def gen_all_tag_button(self, tags):
        for i, tag in enumerate(tags):
            self.gen_tag_button(tag, i)

    def gen_tag_button(self, tag, column):
        """
        生成单个按钮
        遍历生成时必须要提取方法才能正确执行command，否则所有按钮传入的tag始终是遍历的最后一个tag
        :param tag: 按钮对应标签
        :param column: 列
        :return:
        """
        btn = Button(self.button_frame, height=2, width=8, text=tag, command=lambda: self.tag(tag))
        btn.grid(row=2, column=column)

    def tag(self, tag):
        self.tag_queue.put(tag)

    def next_sample(self, nd_img):
        pil_img = Image.fromarray(nd_img)
        self.current_view_img = ImageTk.PhotoImage(pil_img)
        self.imgView.config(image=self.current_view_img)
