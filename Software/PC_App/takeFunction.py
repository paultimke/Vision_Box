import re 

class callFunction:
    """ Class to receive and evaluate function """
    def __init__(self, name:str):
        self.name = name
        self.__Status = re.compile(r'\bTESTSTATUS\b')
        self.__findImage = re.compile(r'\bCOMPIMAGE\b')
        self.__findText = re.compile(r'\bFTEXT\b')
        self.__findIcon = re.compile(r'\bFICON\b')
        self.__setLight = re.compile(r'\bSETLIGHT\b')
        self.__helpMe = re.compile(r'\bHELPME\b')
        self.__Example = re.compile(r'\bEXAMPLE\b')

    def check(self) -> bool:
        """ Check if function object is correctly created """
        check = False 
        if self.__Status.match(self.name) or self.__findText.match(self.name) or self.__findImage.match(self.name) or self.__findIcon.match(self.name) or self.__setLight.match(self.name) or self.__helpMe.match(self.name) or self.__Example.match(self.name):
            check = True
        return check
    
    def parse(self):
        """ Evaulate if function type exists and send correct command.
            Returns tuple of four; first is always a str, for every case second, 
            third and fourth values are None, except when FICON with rgb values input."""
        ret_val = (None, None)

        if self.__Status.match(self.name):
            command_name = 'TESTSTATUS'
            function = self.name.split(command_name)
            if function[1] == '(START)': 
                ret_val =  (command_name, 'START')
            elif function[1] == '(END)': 
                ret_val =  (command_name, 'END')
            else: 
                print('Error in Function Call. Function only accepts START or END entry.')
            return ret_val

        elif self.__findImage.match(self.name):
            command_name = 'COMPIMAGE'
            function = self.name.split('COMPIMAGE')
            if  ( function[1].startswith('(')) and (function[1].endswith(')') ):
                entryTXT = Text = '' ; cnt = 0
                # remove ( ) and spaces
                entryTXT = function[1].translate({ord(i): None for i in '( )'})
                # remove ' "
                if (entryTXT.startswith('"') and entryTXT.endswith('"')): 
                    Text = entryTXT.replace('"', '')
                elif (entryTXT.startswith("'") and entryTXT.endswith("'")): 
                    Text = entryTXT.replace("'", '')
                else: 
                    Text = entryTXT

                # check if null
                if len(Text) > 0: 
                    ret_val = (command_name, Text)
                else: 
                    print('Error in Function Call. Path is empty.')
            else: 
                print('Error in Function Call. Bad use of parentheses.')
            return ret_val

        elif self.__findText.match(self.name):
            ret_val = (None, None)

            command_name = 'FTEXT'
            function = self.name.split(command_name)
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
                    ret_val = (command_name, Text)
                else: 
                    print('Error in Function Call. Text is empty.') 
            else: 
                print('Error in Function Call. Bad use of parentheses or quotation marks.') 
    
            return ret_val


        elif self.__findIcon.match(self.name):
            ret_val = (None, None)

            command_name = 'FICON'
            function = self.name.split(command_name)
            if ( function[1].startswith('(')) and (function[1].endswith(')') ):
                entryTXT = Text = '' ; cnt = 0
                # remove ( ) and spaces 
                entryTXT = function[1].translate({ord(i): None for i in '( )'})
                #separate words in list 
                words = entryTXT.split(',') ; cnt = 0
                # remove ' " 
                if (words[0].startswith('"') and words[0].endswith('"')): 
                    words[0] = words[0].replace('"', '')
                elif (words[0].startswith("'") and words[0].endswith("'")): 
                    words[0] = words[0].replace("'", '')

                if len(words) == 1:
                    ret_val = (command_name, words[0])
                else: 
                    print('Error in Function Call. Expected only one path to image') 
            else: 
                print('Error in Function Call. Bad use of parentheses.') 

        elif self.__setLight.match(self.name):
            ret_val = (None, None)

            command_name = 'SETLIGHT'
            function = self.name.split(command_name)
            if ( function[1].startswith('(')) and (function[1].endswith(')')):
                entryTXT = Text = ''; cnt = 0
                # remove ( ) and spaces
                entryTXT = function[1].translate({ord(i): None for i in '( )'})
                # separate words in list
                words = entryTXT.split(',') ; cnt = 0
                # concatenate text 
                if len(words) > 0:
                    for word in words:
                        cnt+=1
                        if cnt < len(words): 
                            Text = Text + word + ' '
                        else: 
                            Text += word
                    try:
                        lux_val = int(Text)
                        ret_val = (command_name, lux_val)
                    except:
                        print("Error in Function Call. SETLIGHT Argument must be integer")
                else: 
                    print('Error in Function Call. Text is empty.') 
            else:
                print('Error in Function Call. Bad use of parentheses')

        elif self.__helpMe.match(self.name):
            ret_val = (None, None)

            command_name = 'HELPME'
            function = self.name.split(command_name)
            if (function[1].startswith('(')) or (function[1].endswith(')')):
                print("Error in Function Call. HELPME takes no arguments")
            else:
                ret_val = (command_name, None)
            return ret_val
        
        elif self.__Example.match(self.name):
            ret_val = (None, None)

            command_name = 'EXAMPLE'
            function = self.name.split(command_name)
            if (function[1].startswith('(')) or (function[1].endswith(')')):
                print("Error in Function Call. EXAMPLE takes no arguments")
            else:
                ret_val = (command_name, None)
            return ret_val


        else:
            ret_val = (None, None) 
            print(f'Error in Function Call. Unknown {self.name}') 

        return ret_val


# Example to test class#
if __name__ == '__main__':
    # TODO: Throw error message on unrecognized command
    func = input("Receive Function: ")

    Function = callFunction(func)
    if Function.check():
        print(Function.parse())
