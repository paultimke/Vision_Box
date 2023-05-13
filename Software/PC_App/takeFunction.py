import re 

func = input("Receive Function: ")

class callFunction:
    """ Class to receive and evaluate function """
    def __init__(self, name:str):
        self.name = name
        self.__Status = re.compile(r'\bTESTSTATUS\b')
        self.__findImage = re.compile(r'\bCOMPIMAGE\b')
        self.__findText = re.compile(r'\bFTEXT\b')
        self.__findIcon = re.compile(r'\bFICON\b')

    def check(self) -> bool:
        """ Check if function object is correctly created """
        check = False 
        if self.__Status.match(self.name) or self.__findText.match(self.name) or self.__findImage.match(self.name) or self.__findIcon.match(self.name):
            check = True
        return check
    
    def evaluate(self):
        if self.__Status.match(self.name):
            print('Start')
        elif self.__findImage.match(self.name):
            print('Find Image')
        elif self.__findText.match(self.name):
            word = ''
            print('Find Text')
            function = self.name.split('(')
            if ( function[1].startswith('"') or function[1].startswith("'") ) & function[1].endswith(')'):
                word = ''
                for i in function[1]:
                    if (i!="'") & (i!='"') & (i!=')'):
                        word+=i
            else: print('Error in Function Call')
            print(word)
        elif self.__findIcon.match(self.name):
            print('Find icon')
        else: print('Error in Function Call')

        



Function = callFunction(func)
if Function.check():
    Function.evaluate()





