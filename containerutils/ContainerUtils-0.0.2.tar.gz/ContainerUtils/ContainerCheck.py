ERR_CONTAINER=-1
def convert_container_character(character):
    if character=='A' or character=='a':
        return 10
    if character>='B' and character<='K':
        return (ord(character)-ord('B')+12)
        
    if character>='L' and character<='U':
        return (ord(character)-ord('L')+23)
        
    if character>='V' and character<='Z':
        return (ord(character)-ord('V')+34)
        
    if character>='b' and character<='k':
        return (ord(character)-ord('b')+12)
        
    if character>='l' and character<='u':
        return (ord(character)-ord('l')+23)
        
    if character>='v' and character<='z':
        return (ord(character)-ord('v')+34)
        
    if character>='0' and character<='9':
        return (ord(character)-ord('0'))
    return ERR_CONTAINER   

def convert_container_number(container_number_string):
    container_number_digital=[]
    container_number_string=container_number_string[0:11]
    for i in container_number_string:
        container_number_digital.append(convert_container_character(i))
    return container_number_digital
'''计算箱号最后一位的值'''
def cal_container_check_mark(container_number_string):
    if len(container_number_string)!=11:
        print("container_number_string len error")
        return ERR_CONTAINER 
    container_number_digital=convert_container_number(container_number_string)
    if ERR_CONTAINER in container_number_digital :
        return ERR_CONTAINER
    result=0
    for i in range(10):
        result+=container_number_digital[i]*(2**i)
    result=result%11%10
    return result
'''仅仅判断箱号是否正确'''
def verify_container_number(container_number_string):
    cal_result=cal_container_check_mark(container_number_string)
    if cal_result== ERR_CONTAINER:
        return False
    if cal_result==convert_container_character(container_number_string[10]):
        return True
    else :
        return False
'''根据箱号其他位置信息推测index位可能的数字值，仅支持数字值'''   
def delect_container_number(container_number_string,index):
    if index<4 or index>11 :
        print("index error")
        return
    result=[]
    for i in range(10) :
        container=container_number_string[0:index]+str(i)+container_number_string[index+1:]
        if cal_container_check_mark(container)==convert_container_character(container[10]):    
            result.append(container)
    return result   

def test_number(container):
    dd=[]
    print(container)
    for a in range(10):
        s=container[0:4]+str(a)+container[5:]
        #print(s)
        result=cal_container_check_mark(convert_container_number(s))
        #print(result)
        dd.append((a,result))
    for ss in dd:
        print(ss)
