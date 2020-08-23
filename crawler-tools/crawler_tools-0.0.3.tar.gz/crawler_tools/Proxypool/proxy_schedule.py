# -*-  coding: utf-8 -*-
# Author: caowang
# Datetime : 2020
# software: PyCharm
import os
from  threading import Thread as td
import warnings
warnings.filterwarnings("ignore")

def proxy_schedule(proxy_module=3):
    """启动代理爬取,默认全部启动"""
    try:
        #print('redis数据库启动成功....................................')
        if proxy_module == 3:
            def cui_proxy():
                os.system('python {}\\proxy_pool_cui\\run.py'.format(os.path.abspath(os.path.dirname(__file__))))

            def schedule():
                os.system('python {}\\proxy_pool_jihao\\Schedule\\ProxyScheduler.py'.format(
                    os.path.abspath(os.path.dirname(__file__))))

            def api():
                print(os.system('python {}\\proxy_pool_jihao\\Api\\ProxyApi.py'.format(os.path.abspath(os.path.dirname(__file__)))))


            thread = []
            thread.append(td(target=schedule))
            thread.append(td(target=api))
            thread.append(td(target=cui_proxy))
            #不知道为什么要去掉 if __name__ =="__main__"，或许是这个语法在被调用时不运行
            for t in thread:
                t.start()
                #print("正在运行中")
        elif proxy_module != 3:
            proxy_module = input('输入需要启动的代理池模块： 输入命令格式为——1（崔）or2（jihao) \n')
            if int(proxy_module) == 1:
                print('代理池cui启动中.............................................................')
                os.system('python {}\\proxy_pool_cui\\run.py'.format(os.path.abspath(os.path.dirname(__file__))))
            elif int(proxy_module) == 2:
                print('代理池jihao启动中.............................................................')

                def schedule():
                    os.system('python {}\\proxy_pool_jihao\\Schedule\\ProxyScheduler.py'.format(
                        os.path.abspath(os.path.dirname(__file__))))

                def api():
                    os.system(
                        'python {}\\proxy_pool_jihao\\Api\\ProxyApi.py'.format(
                            os.path.abspath(os.path.dirname(__file__))))

                thread = []
                thread.append(td(target=schedule))
                thread.append(td(target=api))
                # & F:\\PyCharm项目\\常用设置\\Proxypool\\proxy_pool_jihao\\Api\\ProxyApi.py')

                for t in thread:
                    t.start()
                print('................................................................................')

        else:
            print('退出中...............................')
            exit(0)
    except:
        print("可能redis没有启动....")

#proxy_schedule()