"""
@author HeTongHao
@since 2020/7/23 10:57
"""

import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['Songti SC']


def imgs_pre_handle(imgs):
    imgs = imgs.reshape((imgs.shape[0], imgs.shape[1], imgs.shape[2], 1))
    return imgs.astype('float32') / 255


def evaluate(model, x_test, y_test):
    result = model.evaluate(x_test, y_test)
    print('评估模型:', result)


def show_history(history):
    history_dict = history.history
    loss = history_dict['loss']
    val_loss = history_dict['val_loss']
    binary_accuracy = history_dict['binary_accuracy']
    val_binary_accuracy = history_dict['val_binary_accuracy']

    plt.tick_params(axis='both', labelsize=15)
    plt.title('训练损失')
    plt.ylabel('损失')
    plt.xlabel('轮次')
    plt.plot(loss, label='训练损失')
    plt.plot(val_loss, marker='o', label='验证损失')
    plt.legend()
    plt.show()

    plt.tick_params(axis='both', labelsize=15)
    plt.title('训练精度')
    plt.ylabel('精度')
    plt.xlabel('轮次')
    plt.plot(binary_accuracy, label='训练精度')
    plt.plot(val_binary_accuracy, marker='o', label='验证精度')
    plt.legend()
    plt.show()
