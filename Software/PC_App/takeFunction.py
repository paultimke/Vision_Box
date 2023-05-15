import re 

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
        """ Evaulate if function type exists and send correct command.
            Returns tuple of four; first is always a str, for every case second, 
            third and fourth values are None, except when FICON with rgb values input."""
        
        if self.__Status.match(self.name):
            function = self.name.split('TESTSTATUS')
            if function[1] == '(START)': return 'START', None, None, None
            elif function[1] == '(END)': return 'END', None, None, None
            else: print('Error in Function Call. Function only accepts START or END entry.') ; return None, None, None, None 


        elif self.__findImage.match(self.name):
            function = self.name.split('COMPIMAGE')
            if  ( function[1].startswith('(')) and (function[1].endswith(')') ):
                entryTXT = Text = '' ; cnt = 0
                # remove ( ) and spaces
                entryTXT = function[1].translate({ord(i): None for i in '( )'})
                # remove ' "
                if (entryTXT.startswith('"') and entryTXT.endswith('"')): Text = entryTXT.replace('"', '')
                elif (entryTXT.startswith("'") and entryTXT.endswith("'")): Text = entryTXT.replace("'", '')
                else: print('Error in Function Call. Bad use of quotation marks.') ; return None, None, None, None 
                # check if null
                if len(Text) > 0: return Text, None, None, None
                else: print('Error in Function Call. Path is empty.') ; return None, None, None, None 
            else: print('Error in Function Call. Bad use of parentheses.') ; return None, None, None, None 


        elif self.__findText.match(self.name):
            function = self.name.split('FTEXT')
            if ( function[1].startswith('("') and function[1].endswith('")') ) or ( function[1].startswith("('") and (function[1].endswith("')")) ):
                entryTXT = Text = '' ; cnt = 0
                # remove (" ") , (' ')
                for i in function[1]:
                    cnt+=1
                    if (cnt == (len(function[1])-1)): break
                    if (cnt!=1) and (cnt!=2): entryTXT+=i
                # separate words in list
                words = entryTXT.split() ; cnt = 0
                # concatenate text 
                if len(words) > 0:
                    for word in words:
                        cnt+=1
                        if cnt < len(words): Text = Text + word + ' '
                        else: Text += word
                    return Text, None, None, None
                else: print('Error in Function Call. Text is empty.') ; return None, None, None, None 
            else: print('Error in Function Call. Bad use of parentheses or quotation marks.') ; return None, None, None, None 


        elif self.__findIcon.match(self.name):
            function = self.name.split('FICON')
            if ( function[1].startswith('(')) and (function[1].endswith(')') ):
                entryTXT = Text = '' ; cnt = 0
                # remove ( ) and spaces 
                entryTXT = function[1].translate({ord(i): None for i in '( )'})
                #separate words in list 
                words = entryTXT.split(',') ; cnt = 0
                # remove ' " 
                if (words[0].startswith('"') and words[0].endswith('"')): words[0] = words[0].replace('"', '')
                elif (words[0].startswith("'") and words[0].endswith("'")): words[0] = words[0].replace("'", '')
                else: print('Error in Function Call. Bad use of quotation marks.') ; return None, None, None, None 
                if len(words) == 1:
                    return words[0], None, None, None
                elif len(words) == 4:
                    for i in range(1,4):
                        try: int(words[i])
                        except: print('Error in Function Call. Expected int type for RGB values') ; return None, None, None, None 
                    return words[0], int(words[1]), int(words[2]), int(words[3])
                else: print('Error in Function Call. Expected only 3 int type RGB values') ; return None, None, None, None 
            else: print('Error in Function Call. Bad use of parentheses.') ; return None, None, None, None 

        else: print('Error in Function Call') ; return None, None, None, None 


# Example to test class#
func = input("Receive Function: ")

Function = callFunction(func)
if Function.check():
    print(Function.evaluate())


