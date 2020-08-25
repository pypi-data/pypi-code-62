import matplotlib.pyplot as plt

def kaun_tha(loud=False):
    if loud:
        print('RASHI BEN')
        img = plt.imread('/disp.jpg')
        plt.imshow(img)
        ax= plt.gca()
        ax.axes.xaxis.set_visible(False)
        ax.axes.yaxis.set_visible(False)
    else:
        print('')