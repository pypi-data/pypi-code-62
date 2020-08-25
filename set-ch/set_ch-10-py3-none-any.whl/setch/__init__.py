# -*-coding:utf-8-*-
'''
汉化功能库
'''


def set_ch():
    '''
    这个可以解决matplotlib的中文问题
    '''
    from pylab import mpl
    mpl.rcParams['font.sans-serif'] = ['FangSong']  # 指定默认字体
    mpl.rcParams['axes.unicode_minus'] = False  # 解决保存图像是负号'-'显示为方块的问题

def demo(d):
    '''
    测试
    '''
    import turtle
    turtle.circle(d)