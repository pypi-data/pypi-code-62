__version__="0.0.1"
__method__=u'''
class cmd_argv():
    method define here:
    argv_to_dict
    argv_only_key
    argv_only_value
class create_cmd_argv();
    method define here:
    add_argv
    
    show_help_message
    '''
__all__=["argv_to_dict","argv_only_key","argv_only_value","add_argv","create_help_message"]
def help():
    print("%s\n%s"%("请打开源代码查看注释以获得帮助！",__import__("os").getcwd()))
    print("%s\n%s"%("Check the comments section in the source code for help",__import__("os").getcwd()))

#@author:Bo Wei 韦博
#19801379165
#_________________________________________________________________________
class cmd_argv(object):
    
    def __init__(self,argv_list):
        #@parse:argv_list(sys.argv) 参数列表，从sys.argv获取
        #@return:None               无返回值
        self.list=argv_list
    def argv_to_dict(self):
        #@return:dict of argv       返回参数字典，例如{"-a":"a"}
        re_di={}
        for i in range(len(self.list)):
            try:
                if self.list[i][0:1]=="-" or self.list[i][0:1]=="--":
                    if self.list[i+1][0:1] != "-" or self.list[i+1][0:1] != "--":
                        re_di[self.list[i]]=self.list[i+1]
                    elif self.list[1+1][0:1] =="-" or self.list[i+1][0:1]=="--":
                        re_di[self.list[i]]=""
            except IndexError:
                pass #list end 列表结束

        #排除掉值为键的可能性 replace same value which maybe is key
        key=list(re_di.keys())#以列表形式返回所有键 get all keys in list
        for j in key:
            print(re_di[j])
            if re_di[j][0:1] is "-" or "--" == True:
                print(re_di[j][0:1])
                re_di[j]=""
        self.dict=re_di
        return re_di
    def argv_only_key(self):
       #@parse:None
        #@return:keys 返回键(keys)
        return list(self.dict.keys())
    def argv_only_value(self):
        #@return:value 返回"值"(value)
        return list(self.dict.values())
    #end class
class create_cmd_argv(object):
    def __init__(*project_name):
        if project_name:
            self.name=project_name
        else:
            self.name=""
        self.string="usage for this application :%s\n关于此程序的用法:%s\n"%(self.name,self.name)
        self.list=[]
    def add_argv(self,usage,introduce,long_usage):
        #usage:keys,like(-f),introduce:full_word,like(filename),long_usage,like(get the filename from this dir)
        #add a string like "-f,<filename>,get the filename from this dir"in self.list as help message
        #用法：usage：参数，比如(-f),introduce:全称，如(filename),long_uasge:简介，如(get the filename from this dir)
        #向self.list添加一行字符，如"-f,<filename>,get the filename from this dir"
        string="%s,<%s>,%s\n"%(usage,introduce,long_usage)
        self.list.append(string)
    def create_help_message(self,usage):
        #usage:uasge:print help message when get argv == usage,usually be -h,--help,-?
        #用法：usage:打印帮助当第一个参数为usage时,常为-h ,--help,-?
        try:
            if __import__("sys").argv[1] == usage:#第一个参数是usage？ if first argv is usage?(sys.argv[0])是绝对路径 is abs path
                print(self.string)
                for i in self.list:
                    print(i)
        except IndexError:
            __import__("warnings").warn("Warning:No Argv Given!")
        #end class
#2020-8-26 19:53
#Chinese and English support
#中英双语支持
        
        










        
        
