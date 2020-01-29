import re
from fractions import Fraction
global res
res=[]
def print_rules(): #печатает правила ввода
    rules='''КАЛЬКУЛЯТОР ДРОБЕЙ
Дроби записываются следующим образом:
Смешанные дроби – 5(1/4), правильные – 5/9, неправильные 19/7 или 19/(-7) (ЗАПИСЫВАТЬ переменную в смешанную дробь (a(a/a)) запрещено)
В выражении могут быть простые числа, смешанные, правильные и неправильные дроби
exit - завершить программу
save "name" - сохранить значение в переменную с названием "name"
del "name" - удалить переменную с названием "name"
to double - вывести результат в виде числа с плавающей точкой
'''
    print(rules)
    
def check_bracket(string): #функция проверяет корректность введеных скобок, если все правильно, возвращает True
    fbracket_close=string.find(")")
    fbracket_open=string[:fbracket_close].rfind("(")
    if (-1<fbracket_open<fbracket_close):
        string=string[:fbracket_open]+string[fbracket_close+1:]
        return check_bracket(string)
    elif (fbracket_open==fbracket_close==string.find('(')==-1):
        return True
    else:
        return False
def check_sign(string): #проверка на корректность введеных знаков
    check=not(re.search('([-+/*][-+/*])|([-+/*][)])|([(][-+/*]?[)])',string))
    string=find_mfraction(string)
    return check and not(re.search('\d+[(]',string))
    
def countbyJeka(numb1,between,numb2): #считает числа, которые передаются из calculator()
    if between=='+':
        return numb1+numb2
    elif between=='-':
        return numb1-numb2
    elif between=='*':
        return numb1*numb2
    elif between=='/':
        try:
            return numb1/numb2
        except ZeroDivisionError:
            return 'Деление на ноль запрещено'
    
def arr(string): #превращает введеную строку в массив, разделенный по числам и знакам
    string=string
    a=re.match("(\d+[.]?\d*)|([-+*/()])", string)
    if a!=None:
        res.append(a.group())
        string=string[len(a.group()):]
        return arr(string)
    return (res)

def find_mfraction(mfraction): #находит смешанные числа и преобразует в дробь, также отправляет в reduction, чтобы ее сократить
    ff=re.search(r"\d+[(]\d+[/]\d+[)]", mfraction)
    if (ff==None):
        return mfraction
    else:
        mix_num=mfraction[ff.start():ff.end()]
        mix_num=re.split(r"[(/)]", mix_num)
        mix_num=str(f'{(int(mix_num[0]))*(int(mix_num[2]))+(int(mix_num[1]))}/{int(mix_num[2])}')
        mix_num=reduction(mix_num)
        mfraction=mfraction[:ff.start()]+mix_num+mfraction[ff.end():]
#        print(mfraction)
        return find_mfraction(mfraction)
    
def reduction(mix_num): #сокращает дробь при помощи НОД
    mix_num=mix_num.split('/')
    for i in range(2):
        mix_num[i]=int(mix_num[i])
    a=abs(mix_num[0])
    b=abs(mix_num[1])
    while a!=0 and b!=0:
        if a>b:
            a%=b
        else:
            b%=a
    a+=b
    if mix_num[1]<0:
        mix_num[i]*=-1
    for i in range(2):
        mix_num[i]//=a
    if mix_num[1]<0:
        for i in range(2):
            mix_num[i]*=-1
    mix_num=str(f'{mix_num[0]}/{mix_num[1]}')
    return mix_num

def calculator(arrstring): #калькулятор, реализованный при помощи стаков
    numbers=[]
    sign=[]
    temps=''
    operations={'+':'1', '-':'1', '*':'2', '/':'2', '(':'0',')':'9999'}
    for i in arrstring:
        a=re.match("(\d+[.]?\d*)",i)
        if a:
            numbers.append(float(i))
        else:
            if not sign:
                sign.append(i)  
            elif i=='(':
                sign.append(i)            
            elif i==')':
                while sign[-1]!='(':
                    first=numbers.pop(-2)
                    second=numbers.pop()
                    icon=sign.pop()
                    temps=countbyJeka(first,icon,second)
                    if temps!='Деление на ноль запрещено':
                        numbers.append(temps)
                    else:
                        return 'Деление на ноль запрещено'
                sign.pop(-1)

            elif int(operations.get(i))<=int(operations.get(sign[-1])):
                while sign and (int(operations.get(i))<=int(operations.get(sign[-1]))):
                    first=numbers.pop(-2)
                    second=numbers.pop()
                    icon=sign.pop()
                    temps=countbyJeka(first,icon,second)
                    if temps!='Деление на ноль запрещено':
                        numbers.append(temps)
                    else:
                        return 'Деление на ноль запрещено'
                sign.append(i)
            elif int(operations.get(i))>int(operations.get(sign[-1])):
                sign.append(i)
    if temps=='':
        print('Что-то пошло не так, введите уравнение еще раз.')
        print_rules()
    else:
        return temps

def conversion(string,variables): # вытаскивает переменные из словаря, где ключ - название переменной, значение - значение
    if variables!=None:
        for i in list(variables.keys()):
            if i in string:
                string=re.sub(i,'('+variables[i]+')',string)
    return string
def mfraction(string): #преобразует дробь в смешанную дробь
    sign=''
    if string[0]=='-':
        sign='-'
    string=re.split('/',string)
    numerator=abs(int(string[0]))
    denumerator=int(string[1])
    if numerator%denumerator==0:
        string=str(numerator//denumerator)
    elif numerator<denumerator:
        string=str(numerator)+'/'+str(denumerator)
    else:
        string=str(numerator//denumerator)+'('+str(numerator%denumerator)+'/'+str(denumerator)+')'
    return sign+string
def double(string): #делает число из дроби типа float
    string=re.split('/',string)
    return int(string[0])/int(string[1])
def negative(string): # если в строке первое число с минусом(-2), то делает его вида 0-2, если в скобке первое число с минусом((-2), то делает его вида (0-2 для корректной работы calculator())
    string=re.sub('[(][-]','(0-',string)
    string=re.sub('\A[-]','0-',string)
    return string
def main(): #проверяет, что ввел пользователь, и в зависимости от введеной строки, выполняет действия
    variables={}
    print_rules()
    temp=''
    dbb=''
    while True:
        string=input('Введите уравнение или команду: \n')
        if string=='exit':
            print('Выходим из программы....Успешно')
            break
        elif re.match('save \w+', string)!=None:
            name_variables=re.findall('save (\w+)',string)[0]
            if re.search('\d+',name_variables)==None and name_variables!='exit' and name_variables!='save' and name_variables!='del' and name_variables!='to double':
                for k in variables.keys():
                    if name_variables==k:
                        print('такое имя уже есть')
                        break
                else:
                    if temp=='':
                        print('нечего сохранять')
                    else:
                        if len(variables)<10:
                            variables[name_variables]=temp
                            print(f'значение \"{temp}\" сохранено в переменную {name_variables}')
                        else:
                            del variables[list(variables.keys())[0]]
                            variables[name_variables]=temp
            else:
                print('переменная может содержать только буквы/вы использовали команду как имя переменной')
        elif re.match('del \w+', string)!=None:
            name_variables=re.findall('del (\w+)',string)[0]
            if name_variables in list(variables.keys()):
                del variables[name_variables]
                print(f'значение "{name_variables}" удалено')
            else:
                print('Значение с таким именем не было сохранено')
        elif string=='to double':
            if dbb=='':
                print("нельзя преобразовать пустое значение")
            else:
                print(double(dbb))
        else:
            if string=='+' or string=='-' or string=='*' or string=='/'  or re.match('[+*/]\d+',string) or re.search('\d+[+*/]\Z',string) or re.search('\w+[+*/]\Z',string):
                print('Что-то пошло не так, введите уравнение еще раз.')
                print_rules()
            else:
                if string.isdigit() or re.search('\A\d+[.]\d+\Z',string):
                    dbb=string
                    temp=string
                    print(string)
                else:
                    string=conversion(string,variables)
                    if (re.match(r'\A[0-9()*/+-.]+\Z',string)!=None)and(check_bracket(string))and(check_sign(string)):
                        string=find_mfraction(string)
                        if re.search('[)]\d',string)==None and re.search('\d+[)][(]',string)==None and re.search('[)][(]',string)==None:
                            string=negative(string)
                            string=arr('('+string+')')
                            calculator(string)
                            string=calculator(string)
                            if string!='Деление на ноль запрещено':
                                string=str(Fraction(float(string)).limit_denominator())
                                dbb=string
                                if '/' in string:
                                    string=mfraction(string)
                                temp=string
                                print(string)
                            else:
                                print('\nДеление на ноль запрещено!\n')
                                print_rules()
                                pass
                        else:
                            print('Что-то пошло не так, введите уравнение еще раз.')
                            print_rules()
                    else:
                     print('Что-то пошло не так, введите уравнение еще раз.')
                     print_rules()
        

main()