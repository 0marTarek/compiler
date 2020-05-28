##############################################
import os
##############################################

#E:\lvl 3\Term 2\Compiler\Test The Scanner1(c).txt
#E:\lvl 3\Term 2\Compiler\Test The Scanner2(c).txt
#E:\lvl 3\Term 2\Compiler\Test The Scanner3(c).txt

##############################################
Keywords   = ['if','else','else if','then','while','do while','&&' ,'break'
              ,'continue','for','!' , '||' , 'return' , 'main']
Comparing  = ['<' , '>' , '==' , '<=' , '>=' , '!=']
Operations = ['+' , '-' , '*' , '/' , '%']
Assignment = ['=']
DataTypes  = ['int' , 'float' , 'double' , 'string' , 'char']
alphabet   = ['a' , 'b','c','d','e','f','g','h','i','j','k','l','m','n','o'
             ,'p','q','r','s','t','u','v','w','x','y','z','A','B','C','D'
             ,'E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S'
             ,'T','U','V','W','X','Y','Z','_']
Brackets   = ['[' , ']' , '(' , ')' , '{' , '}']
Functions  = ['printf' , 'scanf']
digits     = ['1' , '2' , '3' , '4' , '5' , '6' , '7' , '8' , '9' , '0']
Words      = []
Tokens     = {}
##############################################
def Scanner():
    count    = 0
    fun_counter    = 0
    #print(alphabet)
    path = input("Enter The Full Path Of The .txt File : ")
    if(os.path.isfile(path)):
        file = open(path , "r")
        #print(path)
        #print(f.read())
        for line in file:
            for word in line.split():
                if word == '//' or word == '#' or word == '/*' or word == '*/':
                    break
                elif word in Functions:
                    Tokens.update({'Function' + ' ' + str(fun_counter): word})
                    fun_counter += 1
                    break
                Words.append(word)
            count+=1
            print("Line {}   : {}".format(count, line.strip()))
    else:
        print("File Not Found , Maybe A Wrong Path")
    print(Words)
    print('##############################################')
    id_counter     = 0
    key_counter    = 0
    Assign_counter = 0
    comp_counter   = 0
    op_counter     = 0
    Brac_counter   = 0
    dig_counter    = 0
    data_counter   = 0
    for word in Words:
        if(Is_identifier(word)):
            Tokens.update({'identifier' + ' ' + str(id_counter)     : word})
            id_counter     += 1
        elif(word in Keywords):
            Tokens.update({'Keyword'    + ' ' + str(key_counter)    : word})
            key_counter    += 1
        elif(word in DataTypes):
            Tokens.update({'DataType'   + ' ' + str(data_counter)  : word})
            data_counter    += 1
        elif(word in Assignment):
            Tokens.update({'Assignment' + ' ' + str(Assign_counter) : word})
            Assign_counter += 1
        elif(word in Comparing):
            Tokens.update({'Comparison' + ' ' + str(comp_counter)   : word})
            comp_counter   += 1
        elif(word in Operations):
            Tokens.update({'Operation'  + ' ' + str(op_counter)     : word})
            op_counter     += 1
        elif(word in Brackets):
            Tokens.update({'Bracket'    + ' ' + str(Brac_counter)   : word})
            Brac_counter   += 1
        #elif(word in Functions):
            #Tokens.update({'Function'   + ' ' + str(fun_counter)    : word})
            #fun_counter    += 1
        elif(word in digits):
            Tokens.update({'digit'      + ' ' + str(dig_counter)    : word})
            dig_counter    += 1
    for keys,values in Tokens.items():
        print(values + ' ' + keys)

    return Words
        

def Is_identifier (word):
    valid = False
    if(word in Keywords or word in Functions or word in DataTypes):  
        valid = False
    else:
        if(word[0] in alphabet):
            valid = True
    return valid
    

Scanner()

