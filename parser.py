letter = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
digits = "0123456789"
others = "@#$%_"
reserved_words = "if int float char"
class parser:
    def __init__(self, token_list, dict):
        self.indx = 0
        self.word = None
        self.token_list = token_list
        self.dec = "int float char"
        self.temp_identifier = None
        self.variables = dict

    #increasing the index and get the next token
    def check_index(self):
        self.indx += 1
        if self.indx >= len(self.token_list) :
            return True
        self.word = self.token_list[self.indx]
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
                if self.identifier(self.word) :
                    self.temp_identifier = self.word
                    if self.check_index():
                        print("Missing Simicolon ';'. ")
                        return False
                    else:
                        if self.word == ";": 
                            self.variables[self.temp_identifier] = keyword
                            self.temp_identifier = None
                            print ("Valid syntax without assignment.") 
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
                                    print("Valid syntax and assignment.")
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
                            print("Bad syntax expected simicolon or '=' " )
                            return False
                else:
                    print("Bad variable name.")
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
                                        print("Accepted operation, two variables have the same datatype.")
                                        return True
                                    else:
                                        print("Missing Simicolon ';'.")
                                        return False


                            else:
                                print("Error, Different Datatypes " + self.variables[self.temp_identifier] + " and " + self.variables[self.word])
                        else:
                            res_value = self.keyword_value_identify(self.variables[self.temp_identifier], self.word)
                            if  res_value == "accepted":
                                if self.check_index() :
                                    print("Missing Simicolon ';'.")
                                    return False
                                else:
                                    if self.word == ";":
                                        print("Valid assignment without decleration.")
                                        return True
                                    else:
                                        print("Missing Simicolon ';'.")
                                        return False
                            else:
                                print(res_value)
                                return False
                else:
                    print('expected assignment operator"=".')
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
                    return True
                else:
                    print("variable name can only be letters or numbers.")
                    return False
        else:
            if text in reserved_words:
                print("identifier name can't from reserved words.")
                return False

            print("varible must start with letter")
            return False


    def CheckExpresion(self):
        print("ok")
		
		
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
    
        

def main():
    q = ["x", "=", "y", ";" ]
    dict = {"x":"float",
            "y":"int"
            }
    p = parser(q, dict)
    x = p.Dec_Syntax()
    print("Declearation Result is: " , x)
    print(p.variables)
	
    exp = input('Please enter the expression: ')
    Stack.checkExpression(exp)



if __name__ == "__main__":
    main()
