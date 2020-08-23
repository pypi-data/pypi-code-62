from ContainerUtils.ContainerCheck import convert_container_character
from ContainerUtils.ContainerCheck import verify_container_number
from ContainerUtils.ContainerCheck import delect_container_number
from ContainerUtils.ContainerCheck import convert_container_number
from ContainerUtils.ContainerCheck import cal_container_check_mark
ERR_CONTAINER=-1
import sys
def parse_cmd():
    l=len(sys.argv)
    print(sys.argv)
    if l==1 :
        print('命令提示：')
        print('-c container_number :cal_container_check_mark')
        print('-v container_number :verify_container_numbe')
        print('-d container_number :delect_container_number from index4 to 10')
        print('-d container_number index:delect_container_number index')
    pass
    if l==3 :
        if sys.argv[1]=="-v" :
            r=verify_container_number(sys.argv[2])
            print('校验集装箱是否正确：',r)
        if sys.argv[1]=="-c" :
            r=cal_container_check_mark(sys.argv[2])
            print('计算结果：',r)
        if sys.argv[1]=="-d" :
            container=sys.argv[2]
            for i in range(4,11):
                print("**start:**")
                print("if change the index[",i,"] ,then valid container number list:",delect_container_number(container,i))
                print("----------------")
    if l==4  :
        container=sys.argv[2]
        i=int(sys.argv[3])
        if sys.argv[1]=="-d" :
            print("**start:**")
            print("if change the index[",i,"] ,then valid container number list:",delect_container_number(container,i))
            print("----------------")
            
            
if __name__=='__main__'    :
        parse_cmd()