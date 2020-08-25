class System:
    def __init__(self,alphabet="01"): #конструктор класса
        if len(set(alphabet))!=len(alphabet):
            raise Exception("Error: the alphabet contains repeating elements")
        elif "." in alphabet:
            raise Exception("Error: invalid character .")
        else:
            self.alphabet=list(alphabet)
            self.power=len(alphabet)
            self.zero=alphabet[0]
            self.one=alphabet[1]
    def Format(self,x,y): #приведение чисел к стандартному виду
        if "." not in x:
            x+="."+self.zero
        if "." not in y:
            y+="."+self.zero
        x1=x.split(".")[0]
        x2=x.split(".")[1]
        y1=y.split(".")[0]
        y2=y.split(".")[1]
        if len(x1)<len(y1):
            x1=self.zero*(len(y1)-len(x1))+x1
        elif len(x1)>len(y1):
            y1=self.zero*(len(x1)-len(y1))+y1
        if len(x2)>len(y2):
            y2+=self.zero*(len(x2)-len(y2))
        elif len(y2)>len(x2):
            x2+=self.zero*(len(y2)-len(x2))
        x=x1+"."+x2
        y=y1+"."+y2
        return x,y
    def Format_out(self,x): #удаление нулей в начале и конце
        while x[0]==self.zero:
            x=x[1:]
        while x[-1]==self.zero:
            x=x[:-1]
        if x[-1]==".":
            x=x[:-1]
        return x
    def Is_number(self,x): #проверка, является ли строка числом
        if x[0]=="-":
            x=x[1:]
        if x.count(".")>1 or x.find(".")==0 or x.find(".")==len(x)-1:
            return False
        for i in x:
            if i not in self.alphabet+["."]:
                return False
        return True
    def To_10_int(self,x): #перевод натурального числа в десятичную систему
        result=0
        for i in range(len(x)):
            result+=self.alphabet.index(x[i])*pow(self.power,len(x)-i-1)
        return result
    def To_system_int(self,x): #перевод натурального числа в пользовательскую систему
        result=""
        while x>=self.power:
            result=self.alphabet[x%self.power]+result
            x=x//self.power
        result=self.alphabet[x]+result
        return result
    def Proc_sum(self,x,y): #суммирование
        result=""
        x,y=self.Format(x,y)
        cache=0
        for i in range(-1,-len(x)-1,-1):
            if x[i]!=".":
                s=self.alphabet.index(x[i])+self.alphabet.index(y[i])+cache
                cache=s//self.power
                result=self.alphabet[s%self.power]+result
            else:
                result="."+result
        if cache!=0:
            result=self.alphabet[cache]+result
        result=self.Format_out(result)
        return result
    def Proc_dif(self,x,y): #вычитание
        result=""
        x,y=self.Format(x,y)
        cache=False
        for i in range(-1,-len(x)-1,-1):
            if x[i]==".":
                result="."+result
            else:
                if cache==False:
                    if x[i]==self.zero:
                        if y[i]==self.zero:
                            result=self.zero+result
                        else:
                            cache=True
                            result=self.alphabet[self.power-self.alphabet.index(y[i])]+result
                    else:
                        if self.alphabet.index(x[i])<self.alphabet.index(y[i]):
                            cache=True
                            result=self.alphabet[self.power+self.alphabet.index(x[i])-self.alphabet.index(y[i])]+result
                        else:
                            result=self.alphabet[self.alphabet.index(x[i])-self.alphabet.index(y[i])]+result
                else:
                    if x[i]==self.zero:
                        result=self.alphabet[self.power-1-self.alphabet.index(y[i])]+result
                    else:
                        if self.alphabet.index(x[i])-1<self.alphabet.index(y[i]):
                            result=self.alphabet[self.power+self.alphabet.index(x[i])-1-self.alphabet.index(y[i])]+result
                        else:
                            cache=False
                            result=self.alphabet[self.alphabet.index(x[i])-1-self.alphabet.index(y[i])]+result
        result=self.Format_out(result)
        return result
    def Proc_mul(self,x,y): #произведение
        x,y=self.Format(x,y)
        x=list(x)
        y=list(y)
        punkt=(len(x)-x.index(".")-1)*2
        x.remove(".")
        y.remove(".")
        for i in range(len(x)):
            x[i]=self.alphabet.index(x[i])
            y[i]=self.alphabet.index(y[i])
        result=[0]*(len(x)*2+1)
        for i in range(-1,-len(y)-1,-1):
            for k in range(-1,-len(x)-1,-1):
                result[i+k+1]+=x[k]*y[i]
        result2=""
        for i in range(-1,-len(result),-1):
            result[i-1]+=result[i]//self.power
            result2=self.alphabet[result[i]%self.power]+result2
        result2=result2[:len(result2)-punkt]+"."+result2[len(result2)-punkt:]
        result2=self.Format_out(result2)
        return result2
    def Proc_div(self,x,y,accuracy): #деление
        x,y=self.Format(x,y)
        x=list(x)
        y=list(y)
        while x[0]==self.zero:
            x=x[1:]
        while y[0]==self.zero:
            y=y[1:]
        x.remove(".")
        y.remove(".")
        result=self.To_system_int(self.To_10_int(x)//self.To_10_int(y))
        cache=self.To_system_int(self.To_10_int(x)%self.To_10_int(y))
        if accuracy>0 and cache!=self.zero:
            result+="."
        while accuracy>0 and cache!=self.zero:
            accuracy-=1
            cache+=self.zero
            result+=self.To_system_int(self.To_10_int(cache)//self.To_10_int(y))
            cache=self.To_system_int(self.To_10_int(cache)%self.To_10_int(y))
        return result
    #========== сверху системные функции, снизу те, что для пользователей
    def To_10(self,x,accuracy=3):
        if x[0]=="-":
            status="negativ"
            x=x[1:]
        else:
            status="positiv"
        if "." not in x:
            x+="."+self.zero
        x1=x.split(".")[0]
        x2=x.split(".")[1]
        result=self.To_10_int(x1)+round(self.To_10_int(x2)/self.To_10_int(self.one+self.zero*len(x2)),accuracy)
        if status=="positiv":
            return result
        else:
            return -result
    def To_system(self,x,accuracy=3):
        if x<0:
            status="negativ"
            x=-x
        else:
            status="positiv"
        x=float(x)
        x1=int(str(x).split(".")[0])
        x2=int(str(x).split(".")[1])
        result=self.To_system_int(x1)+self.Proc_div(self.To_system_int(x2),self.To_system_int(int("1"+"0"*len(str(x2)))),accuracy)[1:]
        if status=="positiv":
            return result
        else:
            return "-"+result
    def Compare(self,x,y): #сравнение чисел
        if self.Is_number(x)==False:
            raise Exception("Error: invalid number "+x)
        if self.Is_number(y)==False:
            raise Exception("Error: invalid number "+y)
        if x==y:
            return "="
        elif x[0]=="-" and y[0]=="-":
            x,y=self.Format(x[1:],y[1:])
            while x[0]==y[0]:
                x=x[1:]
                y=y[1:]
            if self.alphabet.index(x[0])>self.alphabet.index(y[0]):
                return "<"
            else:
                return ">"
        elif x[0]=="-" and y[0]!="-":
            return "<"
        elif x[0]!="-" and y[0]=="-":
            return ">"
        else:
            x,y=self.Format(x,y)
            while x[0]==y[0]:
                x=x[1:]
                y=y[1:]
            if self.alphabet.index(x[0])>self.alphabet.index(y[0]):
                return ">"
            else:
                return "<"
    def Calc(self,x,y,a,accuracy=3): #функция математических вычислений
        if self.Is_number(x)==False:
            raise Exception("Error: invalid number "+x)
        if self.Is_number(y)==False:
            raise Exception("Error: invalid number "+y)
        if a=="+":
            if x[0]=="-" and y[0]=="-":
                return "-"+self.Proc_sum(x[1:],y[1:])
            elif x[0]!="-" and y[0]=="-":
                if self.Compare(x,y[1:])=="<":
                    return "-"+self.Proc_dif(y[1:],x)
                else:
                    return self.Proc_dif(x,y[1:])
            elif x[0]=="-" and y[0]!="-":
                if self.Compare(x[1:],y)=="<":
                    return self.Proc_dif(y,x[1:])
                else:
                    return "-"+self.Proc_dif(x[1:],y)
            else:
                return self.Proc_sum(x,y)
        elif a=="-":
            if x[0]=="-" and y[0]=="-":
                if self.Compare(x[1:],y[1:])=="<":
                    return self.Proc_dif(y[1:],x[1:])
                else:
                    return "-"+self.Proc_dif(x[1:],y[1:])
            elif x[0]!="-" and y[0]=="-":
                return self.Proc_sum(x,y[1:])
            elif x[0]=="-" and y[0]!="-":
                return "-"+self.Proc_sum(x[1:],y)
            else:
                if self.Compare(x,y)=="<":
                    return "-"+self.Proc_dif(y,x)
                else:
                    return self.Proc_dif(x,y)
        elif a=="*":
            if x[0]=="-" and y[0]=="-":
                return self.Proc_mul(y[1:],x[1:])
            elif x[0]!="-" and y[0]=="-":
                return "-"+self.Proc_mul(x,y[1:])
            elif x[0]=="-" and y[0]!="-":
                return "-"+self.Proc_mul(x[1:],y)
            else:
                return self.Proc_mul(x,y)
        elif a=="/":
            if x[0]=="-" and y[0]=="-":
                return self.Proc_div(y[1:],x[1:],accuracy)
            elif x[0]!="-" and y[0]=="-":
                return "-"+self.Proc_div(x,y[1:],accuracy)
            elif x[0]=="-" and y[0]!="-":
                return "-"+self.Proc_div(x[1:],y,accuracy)
            else:
                return self.Proc_div(x,y,accuracy)
        else:
            raise Exception("Error: unknow operator "+a)

