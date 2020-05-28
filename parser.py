import Scanner as s
letter = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
digits = "01234567890"
others = "@#$%_"
reserved_words = "if int float char"
DataTypes  = ['int' , 'float' , 'double' , 'string' , 'char']
Functions  = ['printf' , 'scanf']
Tokens     = {}
K_B = ['{']
import os
class parser:
    def __init__(self, token_list):
        self.indx = 0
        
        token_list.append("EOF")
        self.token_list = token_list
        self.dec = ["int", "float", "char"]
        self.temp_identifier = None

        self.variables = {'x':'int'}
        #IF_ELSE_statement
        self.cond = ['>','<','>=', '<=', '==','!=']
        self.stack = [ ]

        self.variables = { }
        self.Current_Line = 0
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

            elif self.word in "\n}" or self.word in "EOF":
                pass
             
            else:
                print("Unknown word: '{}' in Line: '{}'".format(self.word,self.Current_Line +1))
                error = 1
                break
            self.check_index()

        if error != 1:
            temp = self.token_list[-3]
            if temp != "}" :
                print("Expected '}' for main" +  " Expected in Line: '{}'.".format(self.Current_Line ))
                error = 1
            else:
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
                print("Missing {")
                return False

    #declearation grammer rule
    def Dec_Syntax(self):
        self.word = self.token_list[self.indx]
        if self.word in self.dec:
            keyword = self.word
            if self.check_index() :
                print("Expected variable name.")
                return False
            else:
                #for main
                if self.word in "main() main ()":
                    if self.identifyMainFunction() :
                        return True
                    else:
                        return False
                if self.identifier(self.word) :
                    self.temp_identifier = self.word
                    if self.check_index():
                        print("Miss ing Simicolon ';'. ")
                        return False
                    else:
                        if self.word == ";": 
                            self.variables[self.temp_identifier] = keyword
                            self.temp_identifier = None
                            #print ("Valid syntax without assignment.") 
                            return True 
                        elif self.word == "=": 
                            if self.check_index() :
                                print("Bad syntax expected value. ")
                                return False
                            else:
                                res_value = self.keyword_value_identify(keyword, self.word)
                                if  res_value == "accepted":
                                    self.variables[self.temp_identifier] = keyword
                                    self.temp_identifier = None
                                    #print("Valid syntax and assignment.")
                                    if self.check_index() :
                                        print("Missing Simicolon ';'.")
                                        return False
                                    else:
                                        if self.word == ";":
                                            return True
                                        else:
                                            print("Missing Simicolon ';'.")
                                            return False
                                else:
                                    print(res_value)
                                    return False
                        else:
                            print("Bad syntax expected ';' or '=' ")
                            return False
                else:
                    return False

        #Assignment without declearation.
        elif self.word in self.variables.keys() :
            self.temp_identifier = self.word
            if self.check_index() :
                print("Expected Assignment statement")
                return False
            else:
                if self.word == "=":
                    if self.check_index() :
                        print("Bad Syntax, Expected value.")
                        return False
                    else:
                        #assignment with other existing variables.
                        if self.word in self.variables.keys():
                            if self.variables[self.temp_identifier] == self.variables[self.word] :
                                if self.check_index() :
                                    print("Missing Simicolon ';'.")
                                    return False
                                else:
                                    if self.word == ";":
                                        #print("Accepted operation, two variables have the same datatype.")
                                        return True
                                    else:
                                        print("Missing Simicolon ';'.")
                                        return False


                            else:
                                print("Different Datatypes " + self.variables[self.temp_identifier] + " and " + self.variables[self.word])
                        else:
                            res_value = self.keyword_value_identify(self.variables[self.temp_identifier], self.word)
                            if  res_value == "accepted":
                                if self.check_index() :
                                    print("Missing Simicolon ';'.")
                                    return False
                                else:
                                    if self.word == ";":
                                        #print("Valid assignment without decleration.")
                                        return True
                                    else:
                                        print("Missing Simicolon ';'.")
                                        return False
                            else:
                                print(res_value)
                                return False
                else:
                    print('Expected "=".')
                    return False


        else:
            print("Expected int, float, char.")
            return False    

    #chech that the keyword have its right value. 
    def keyword_value_identify(self, keyword, value):
        if keyword == "int":
            for digit in value:
                if digit not in digits:
                    return "Keyword int MUST have only integer values."
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
                    if c not in letter and c not in quot and c not in others:
                        return "Bad string format"
                return "accepted"
            return "Expected String starting or ending with \" or '."

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
        if self.word in self.variables.keys() or self.word in digits :
            print("variables good .")
            if self.check_index() :
                print("Error in if statement not complete.")
                return False
            else :
                return True
        else :
            print ("no expiration ")
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
                       print ("error in ')' .")
                       return False
        if len(self.stack) != 0 :
            print("error in ')' .")
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
                            K_B.append('{')
                    return True 
                else:
                     print("somthing missed  in if statement.")
                     return False
        else:
            print("missing 'if'is ronge .")
            return False
    # ELSE_statement for else rule 
    def ELSE_state (self) :
        self.word = self.token_list[self.indx]
        if self.word == "else" :
            if self.check_index() :
                return True
            else :
                if self.word == "if" :
                    if self.IF_DEC () :
                        if self.check_index() :
                            return True
                        else :
                             if self.word == "{" :
                                 K_B.append('{')
                                 return True 
                             else :
                                  return True
                        return True
                    else :
                         return False
                elif self.word == "{" :
                     K_B.append('{')
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
                print("error ')' complete .")
                return False
            else :
                 if self.word == "(" :
                    if not self.brackets () :
                        return False 
                 elif self.EXP_ident() :
                      if self.word in self.cond:
                         if self.check_index():
                            print("if statement not complete ")
                            return False 
                         else :
                              if self.word == "(" :
                                 if not self.brackets () :
                                       return False
                              elif self.EXP_ident():
                                   if self.word == ")" :
                                      print("good job")
                                      return True 
                                   else :
                                        print("error in ')'")
                                        return False 
                              else :
                                   print ("error in expiration")
                                   return False
                      else :
                            print ("error in condition")
                            return False 
                 else :
                      print ("error in expiration")
                      return False
        else : 
             print("error in '('")
             return False 	
class Stack:
    def __init__(self):
        self.items = []
 
    def is_empty(self):
        return self.items == []
 
    def push(self, data):
        self.items.append(data)
 
    def pop(self):
        return self.items.pop()
    
    def checkExpression(exp):
        s = Stack()
        for c in exp:
            if c == '(':
                s.push(1)
            elif c == ')':
                if s.is_empty():
                    is_balanced = False
                    break
                s.pop()    
        else:
            if s.is_empty():
                is_balanced = True
            else:
                is_balanced = False
        
     
        if is_balanced:
            print('Expression is correctly parenthesized.')
        else:
            print('Expression is not correctly parenthesized.')		
    

        

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
                   #print(el)
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
    
    x = main_function()
    print("all is ",x)

   # q = ["x", "=", "y",";" ]
   # dict = {}
   # tokens = s.Scanner()
   # p = parser(tokens, dict)
  #  x = p.run()

    #print(p.variables)
	
  #  exp = input('Please enter the expression: ')
 #   Stack.checkExpression(exp)




if __name__ == "__main__":
    main()
