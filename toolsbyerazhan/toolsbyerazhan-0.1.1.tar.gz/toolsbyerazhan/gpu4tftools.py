#一般要用到本函数的,都已经安装了tensorflow
import tensorflow as tf
'''
#可以不用加experimental
gpus = tf.config.experimental.list_physical_devices('GPU')
print(gpus)
for gpu in gpus:
    tf.config.experimental.set_memory_growth(gpu, True)

#查看gpu能否使用
print(tf.test.is_gpu_available())
print(tf.config.list_physical_devices('GPU'))
#命令行查看gpu使用情况
#nvidia-smi

import torch
#查看torch的gpu版本是否安装成功
print(torch.cuda.is_available())
'''

'''
#在主程序中判断是否GPU可用
if tf.test.is_gpu_available():
    from configure_gpu import set_gpu_memory
    set_gpu_memory()
'''

def set_gpu_memory():
    print("set gpu memory")
    gpus = tf.config.experimental.list_physical_devices('GPU')
    
    for gpu in gpus:
        tf.config.experimental.set_memory_growth(gpu, True)

