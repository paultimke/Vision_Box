import re

class callFunction:
    """ Class to receive and evaluate function """
    def __init__(self, name:str):
        self.name = name
        self.__Status = re.compile(r'\bTESTSTATUS\b')
        self.__compImage = re.compile(r'\bCOMPIMAGE\b')
        self.__findText = re.compile(r'\bFTEXT\b')
        self.__findIcon = re.compile(r'\bFICON\b')    
        self.__setLight = re.compile(r'\bSETLIGHT\b')
        self.__help = re.compile(r'\bHELPME\b')
        self.__example = re.compile(r'\bEXAMPLE\b')
    def check(self) -> bool:
        """ Check if function is correctly created """
        check = False
        if self.__Status.match(self.name) or self.__compImage.match(self.name) or self.__findText.match(self.name) or self.__findIcon.match(self.name)or self.__setLight.match(self.name) or self.__help.match(self.name) or self.__example.match(self.name):
            check = True
        return check
 

    def evaluate(self) -> str:
        """ Evaluate function """
        if self.__Status.match(self.name):
            function = self.name.split('TESTSTATUS')
            if function[1] == '(START)' : return 'START'
            elif function[1] == '(END)' : return 'END'
            else: print('Error in Function Call. Function only accepts START or END en .'); return None

 
        elif self.__compImage.match(self.name):
            function = self.name.split('COMPIMAGE')
            if ( function[1].startswith('(')) and (function[1].endswith(')')):
                entryTXT = Text = '' 
                # remove ( ) and spaces
                entryTXT = function[1].translate({ord(i): None for i in '( )'})
                # remove ' "
                if (entryTXT.startswith('"') and entryTXT.endswith('"')): Text = entryTXT.replace('"', '')
                elif (entryTXT.startswith("'") and entryTXT.endswith("'")): Text = entryTXT.replace("'", '')
                else: print('Error in Function Call. Bad use of quotation marks.') ; return None
                # check if null
                if len(Text) > 0: return Text
                else: print('Error in Function Call. Path is empty.') ; return None
            else: print('Error in Function Call. Bad use of parentheses.') ; return None



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
                    return Text
                else: print('Error in Function Call. Text is empty.') ; return None
            else: print('Error in Function Call. Bad use of parentheses or quotation marks.') ; return None

 

        elif self.__findIcon.match(self.name):
            function = self.name.split('FICON')
            if ( function[1].startswith('(')) and (function[1].endswith(')') ):
                entryTXT = Text = '' 
                # remove ( ) and spaces
                entryTXT = function[1].translate({ord(i): None for i in '( )'})
                # remove ' "
                if (entryTXT.startswith('"') and entryTXT.endswith('"')): Text = entryTXT.replace('"', '')
                elif (entryTXT.startswith("'") and entryTXT.endswith("'")): Text = entryTXT.replace("'", '')
                else: print('Error in Function Call. Bad use of quotation marks.') ; return None
                # check if null
                if len(Text) > 0: return Text
                else: print('Error in Function Call. Path is empty.') ; return None
            else: print('Error in Function Call. Bad use of parentheses.') ; return None

 

        elif self.__setLight.match(self.name):
            function = self.name.split('SETLIGHT')
            if ( function[1].startswith('(')) and (function[1].endswith(')')):
                entryTXT = '' ; value = 0
                # remove ( ) and spaces
                entryTXT = function[1].translate({ord(i): None for i in '( )'})
                try: value = int(entryTXT)
                except: print('Error in Function Call. Could not get integer from function.') ; return None
                if (value>0) or (value<10000): return value
                else: print('Error in Function Call. Value out of range') ; return None
            else: print('Error in Function Call. Bad use of parenthesis.') ; return None

 

        elif self.__help.match(self.name): 
            print('Help')
            return None


        elif self.__example.match(self.name):
            print('Example')
            return None
        

        else: print('Error in Function Call') ; return None

 
# Example to test class#
func = input("Receive Function: ")

Function = callFunction(func)
if Function.check():
    print(Function.evaluate())