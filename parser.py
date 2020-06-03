import Scanner as s
letter = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
digits = "01234567890"
others = "@#$%_"
operations="+-*/()"
reserved_words = ['if', 'int' ,'float' ,'char']
DataTypes  = ['int' , 'float' , 'double' , 'string' , 'char']
Functions  = ['printf' , 'scanf']
Tokens     = {}

import os
class parser:
    def __init__(self, token_list):
        self.indx = 0
        self.count=0
        token_list.append("EOF")
        self.token_list = token_list
        self.dec = ["int", "float", "char"]
        self.temp_identifier = None

        self.variables = {'x':'int'}
        #IF_ELSE_statement
        self.cond = ['>','<','>=', '<=', '==','!=']
        self.stack = [ ]
        self.if_count = 0
        self.K_B = ['{']

        self.variables = { }
        self.Current_Line = 1
        self.word = self.token_list[self.indx]
        print("###################################################")
        print("Parser result")
        print("###################################################")
        
    def run(self):
        #self.check_index()
        error = 0
        while self.word !="EOF" :
            
            if self.word == "int" or self.word == "float" or self.word == "char" or self.word in self.variables.keys():
                if self.Dec_Syntax() :
                    pass
                else:
                    error = 1
                    print("Expected in Line: ", self.Current_Line)
                    break

            elif self.word in "\n" or self.word in "EOF":
                pass
             
            elif self.word == "if":
                self.if_count +=1
                if self.IF_DEC():
                    pass
                else:
                    error = 1
                    print("Expected in Line: ", self.Current_Line)
                    break
            
            elif self.word == "else" :
                if self.if_count > 0:
                    if self.ELSE_state():
                        self.if_count -=1
                    else:
                        error = 1
                        print("Syntax Error: in 'else' in line: ", str(self.Current_Line))
                        break
                else:
                    error = 1
                    print("Syntax Error: in 'else' in line: ", str(self.Current_Line))
                    break  
            elif self.word == "{":
                self.K_B.append ('{')
            
            elif self.word == "}":
                try:
                    self.K_B.pop()
                except:
                    print("Syntax Error: '}' without '{' in line: ", str(self.Current_Line))
                    error =1 
            else:
                print("Syntax Error: Unknown word: '{}' is not defined, in Line: '{}'".format(self.word,self.Current_Line ))
                error = 1
                break
            self.check_index()

        if error != 1:
            temp = self.token_list[-3]
            if len(self.K_B) == 1 :
                print("Syntax Error: Expected '}' for main" +  " in Line: '{}'.".format(self.Current_Line ))
                error = 1 
            elif len(self.K_B) == 0 and temp != "}" :
                print("Syntax Error: Expected '}' for main" +  " in Line: '{}'.".format(self.Current_Line ))
                error = 1 
            elif len(self.K_B) > 0  :
                print("Syntax Error: Expected '}'" +  " in Line: '{}'.".format(self.Current_Line ))
                error = 1               
        if error != 1:
            print("Compiled successfully. 0 Errors")
            
                    


    #increasing the index and get the next token
    def check_index(self):
        self.indx += 1
        if self.indx >= len(self.token_list) :
            return True
        self.word = self.token_list[self.indx]
        if self.word == "\n":
            self.Current_Line += 1
        
        return False

    def identifyMainFunction(self):
        if self.check_index() :
            print("Expected {")
            return False
        else:   
            if self.word == "{":
               return True
            else:
                print("Missing {, instead " +  self.word)
                return False

    #declearation grammer rule
    def Dec_Syntax(self):
        self.word = self.token_list[self.indx]
        if self.word in self.dec:
            keyword = self.word
            if self.check_index() :
                print("Syntax Error: Expected identifier name.")
                return False
            else:
                #for main
                if self.word in ['main()' ,'main ()']:
                    if self.identifyMainFunction() :
                        return True
                    else:
                        return False
                if self.identifier(self.word) :
                    self.temp_identifier = self.word
                    if self.check_index():
                        print("Syntax Error: Missing Simicolon ';'. ")
                        self.Current_Line -= 1
                        return False
                    else:
                        if self.word == ";": 
                            self.variables[self.temp_identifier] = keyword
                            self.temp_identifier = None
                            #print ("Valid syntax without assignment.") 
                            return True 
                        elif self.word == "=": 
                            if self.check_index() :
                                print("Syntax Error: Expected identifier value. ")
                                return False
                            else:
                                
                                res_value = self.keyword_value_identify(keyword, self.word)
                                if  res_value == "accepted":
                                    self.variables[self.temp_identifier] = keyword
                                    self.temp_identifier = None
                                    #print("Valid syntax and assignment.")
                                    if self.check_index() :
                                        print("Syntax Error: Missing Simicolon ';'.")
                                        self.Current_Line -= 1
                                        return False
                                    else:
                                        if self.word == ";":
                                            return True
                                        else:
                                            print("Syntax Error: Missing Simicolon ';'.")
                                            self.Current_Line -= 1
                                            return False
                                else:
                                    print(res_value)
                                    return False
                        else:
                            print("Syntax Error: Expected simicolon ';'")
                            self.Current_Line -= 1
                            return False
                else:
                    return False

        #Assignment without declearation.
        elif self.word in self.variables.keys() :
            self.temp_identifier = self.word
            if self.check_index() :
                print("Syntax Error: Expected Assignment statement")
                return False
            else:
                if self.word == "=":
                    if self.check_index() :
                        print("Syntax Error: Expected identifier value.")
                        return False
                    else:
                        #assignment with other existing variables.
                        if self.word in self.variables.keys():
                            if self.variables[self.temp_identifier] == self.variables[self.word] :
                                if self.check_index() :
                                    print("Syntax Error: Missing Simicolon ';'.")
                                    self.Current_Line -= 1
                                    return False
                                else:
                                    if self.word == ";":
                                        #print("Accepted operation, two variables have the same datatype.")
                                        return True
                                    else:
                                        print("Syntax Error: Missing Simicolon ';'.")
                                        self.Current_Line -= 1
                                        return False


                            else:
                                print("Semantic Error: Different Datatypes " + self.variables[self.temp_identifier] + " and " + self.variables[self.word])
                                #self.Current_Line  = self.Current_Line +1
                        else:
                            res_value = self.keyword_value_identify(self.variables[self.temp_identifier], self.word)
                            if  res_value == "accepted":
                                if self.check_index() :
                                    print("Syntax Error: Missing Simicolon ';'.")
                                    self.Current_Line -= 1
                                    return False
                                else:
                                    if self.word == ";":
                                        #print("Valid assignment without decleration.")
                                        return True
                                    else:
                                        print("Syntax Error: Missing Simicolon ';'.")
                                        self.Current_Line -= 1
                                        return False
                            else:
                                print(res_value)
                                return False
            
                else:
                    print('Syntax Error: Expected "=".')
                    return False


        else:
            print("Syntax Error: Expected int, float, char.")
            return False
  

        
    def CheckExpresion(self):
        if self.check_index():  
            print("Not Valid Expression")
            return False    
        elif self.word in digits:
            if self.check_index():  
                print("Not Complete Expression")
                return False
            else:
                while(self.word in operations):
                    if self.check_index():  
                        print("Not Valid Expression")
                        return False
                    elif self.word in digits:
                        if self.check_index():
                            break         
               
                print("Valid Expression")
        else:
            print("expression must start with number  ")

    #check ( ) that is right

       
    def CheckPera(self):
        if self.check_index():
            print("not complete expression")
            return False
        elif self.word in "( )":
            while self.word in "( )":
                if self.word=="(":
                    self.count+=self.count
                elif self.word==")":
                    self.count-=self.count
                else:
                    if self.check_index():
                        break
                    
            if self.count==0:
                print("valid parenthes")     
            else:
                print("Not Valid parenthes")
        else:
            CheckPera()
            
            
   
    def check_Expression(self, text):
        text_index = 0 
        for c in text :
            x = c in digits
            if  c.isnumeric()or c in ["+","-","*","/"]:
                pass
            else:
                print("Syntax Error: only numbers and operations allowed, '{}' not allowed in expression.".format(c))
                return False


        current_caracter = text[text_index]
        if current_caracter in ["+","-"]:
            text_index += 1
            if text_index < len(text):
                current_caracter = text[text_index]
                if current_caracter.isnumeric():
                    pass
                else:
                    print("Syntax Error: bad Expression")
                    return False


        if current_caracter.isnumeric() :
            while "+" in text[text_index:] or "-" in text[text_index:] or "*" in text[text_index:] or "/" in text[text_index:]:
                text_index += 1
                if text_index < len(text):
                    current_caracter = text[text_index]
                    if current_caracter in ["+","-","*","/"]:
                        text_index += 1
                        if text_index < len(text):
                            current_caracter = text[text_index]
                            if current_caracter in ["+","-","*","/"]:
                                print("Syntax Error: Expected value instead of '{}'".format(current_caracter))
                                return False
                            elif current_caracter.isnumeric():
                                pass
                            else:
                                print("Syntax Error: two followed operations.")
                                return False
                        else:
                            print("Syntax Error: Expected value after " + current_caracter)
                            return False
                    elif current_caracter.isnumeric():
                        text_index += 1
                    else:
                        print("Syntax Error: Bad expression format.")
                        return False
                else:
                    print("Syntax Error: Expected value.")
                    return False
            return True
        elif current_caracter in ["+", "-"]:

            return False


    #chech that the keyword have its right value. 
    def keyword_value_identify(self, keyword, value):

        if "+" in value or "-" in value or "*" in value or "/" in value:
            if self.check_Expression(value):
                return "accepted"
            else:
                return ""
        elif keyword == "int":
            for digit in value:
                if digit not in digits:
                    return "Semantic Error: Keyword int MUST have only integer values."


            return "accepted"

        elif keyword == "float":
            if value.count(".") > 1 or value.count(".") == 0 :
                return "Expected float number."
            for digit in value:
                if digit not in digits and digit != ".":
                    return "Keyword float MUST have only float numbers."
            return "accepted"

        elif keyword == "char":
            quot = "'\""
            if value[0] in quot and value[len(value) - 1 ] in quot:
                for c in value :
                    if c not in letter and c not in quot and c not in others and  c not in digits:
                        return "Bad string format"
                return "accepted"
            return "Syntax Error: String Must starting and ending with quotation '  or \"."

    #check the variable name 
    def identifier(self, text):
        indx = 0
        current_char = text[indx]
        if current_char in letter  and text not in reserved_words:
            indx = 0
            while (indx < len(text)):
                current_char = text[indx]
                if current_char in letter or current_char in digits or current_char in others :
                    indx +=1
                    if indx < len(text):
                        current_char = text[indx]
                    else:
                        break
                else:
                    print("variable name can only be letters or numbers. can't contain '{}'".format(current_char))
                    return False
        else:
            if text in reserved_words:
                print("'{}' is a reserved word, Identifier can't be from reserved words.".format(text))
                return False

            print("varible must start with letter")
            return False
        return True


    def CheckExpresion(self):
        print("ok")
     #this function for knowing var  
    def EXP_ident (self ):
        if self.word in self.variables.keys() or self.word.isnumeric() :
            if self.check_index() :
                print("Syntax Error: Incomplete if statement.")
                return False
            else :
                return True
        else :
            if self.word not in self.variables.keys():
                print ("Systax Error: Unknow word: '{}' is not defined. ".format(self.word))
                return False
            if self.word.isnumeric():
                pass
            else:
                print ("Systax Error: Expected numeric value istead of '{}'. ".format(self.word))
                return False

	# this function for check number of '( ' ' ) ' right or not     
    def check_bra (self , text):
        for text_i in text :
            if text_i == "(":
                self.stack.append('(')
            elif text_i == ")":
                  if  len(self.stack) != 0:
                      self.stack.pop()
                  else :
                       print ("Syntax Error: Expected ')' .")
                       return False
        if len(self.stack) != 0 :
            print("Syntax Error: Expected ')' .")
            return False
        else :
             return True
    
    #for  If Statement rule 
    def IF_DEC (self):
        self.word = self.token_list[self.indx]
        if self.word == "if" and self.check_bra(self.token_list):
            if self.check_index() :
                print("Error in if statement not complete.")
                return False
            else:
                if self.word == "("  and self.brackets ():
                    if self.check_index() :
                        return True 
                    else :
                        if self.word == '{' :
                            self.K_B.append('{')
                    return True 
                else:
                     return False
        else:
            return False
    # ELSE_statement for else rule 
    def ELSE_state (self) :
        self.word = self.token_list[self.indx]
        if self.word == "else" :
            if self.check_index() :
                return True
            else :
                if self.word == "if" :
                    self.if_count +=1
                    if self.IF_DEC () :
                        if self.check_index() :
                            return True
                        else :
                             if self.word == "{" :
                                 self.K_B.append('{')
                                 return True 
                             else :
                                  return True
                        return True
                    else :
                         return False
                elif self.word == "{" :
                     self.K_B.append('{')
                     return True
                else :
                     return True
        else :
             print ("somthing error in else ")
             return False
    # for check expiration right or not 
    def brackets (self):
        if self.word == "(" :
            if self.check_index():
                print("Syntax Error: Expected ')'.")
                return False
            else :
                 if self.word == "(" :
                    if not self.brackets () :
                        return False 
                 elif self.EXP_ident() :
                      if self.word in self.cond:
                         if self.check_index():
                            print("Syntax Error: Missing Condition.")
                            return False 
                         else :
                              if self.word == "(" :
                                 if not self.brackets () :
                                       return False
                              elif self.EXP_ident():
                                   if self.word == ")" :
                                      return True 
                                   else :
                                        print("Syntax Error: Expected ')'.")
                                        return False 
                              else :
                                   print ("Syntax Error: Missing comparison value.")
                                   return False
                      else :
                            print ("Syntax Error: Missing condition.")
                            return False 
                 else :
                      print ("Syntax Error: Incomplete if statement.")
                      return False
        else : 
             print("Syntax Error: Expected '('. ")
             return False 	
        

def main_function():
    count    = 0
    fun_counter    = 0
    if_count = 0
    #print(alphabet)
    path = input("Enter The Full Path Of The .txt File : ")
    if(os.path.isfile(path)):
        file = open(path , "r")
        for line in file:
            Words      = []
            x = parser(Words)
            for word in line.split():
                if word == '//' or word == '#' or word == '/*' or word == '*/':
                    break
                elif word in Functions:
                    Tokens.update({'Function' + ' ' + str(fun_counter): word})
                    fun_counter += 1
                    break
                Words.append(word)
            count+=1
            if count > 2 and len(Words) != 0:
               for el in Words :
                   x.token_list = Words
                   x.indx = 0 

                   if el == 'if' :
                      if_count += 1
                      if  x.IF_DEC() :
                          print("if food")
                      else :
                          return False
                   elif el == 'else' :
                        if if_count >0 :
                           if x.ELSE_state() :
                              if_count = if_count - 1
                              print ("Else good ")
                           else :
                                return False
                        else :
                             print("error in else ")
                             return False 
                   elif el == '{' :
                        K_B.append ('{')
                   elif el == '}' :
                        K_B.pop()
                   else :
                        if x.Dec_Syntax():
                            print ("EXpration is good")
                        else :
                            
                            return False
                       
                   break
                 
                   
               
               
    else:
        print("File Not Found , Maybe A Wrong Path")
    if len(K_B) != 0 :
        print ("error in { }")
        return False 
    else :
        return True
        
def main():

     #q = ["x", "=", "y", ";" ]
   # dict = {"x":"float",
    #        "y":"int"
     #       }
    #p = parser(q, dict)
    #x = p.Dec_Syntax()
   # print("Declearation Result is: " , x)
   # print(p.variables)
	
    #exp = input('Please enter the expression: ')
    #Stack.checkExpression(exp)
    
    #x = main_function()
   # print("all is ",x)


    q = ["x", "=", "y",";" ]
    tokens = s.Scanner()
    p = parser(tokens)
    x = p.run()
    '''
    while True:
        text = input("Expression> ")
      #  print(p.CheckPera(text))
        print(p.check_Expression(text))
    '''


    #print(p.variables)
	
  #  exp = input('Please enter the expression: ')
 #   Stack.checkExpression(exp)




if __name__ == "__main__":
    main()
