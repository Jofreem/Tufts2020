#!/usr/bin/env python
# coding: utf-8

# In[2]:


import re
class Flags:
    #Class variable - table
    #Purpose: is the encoding hash table
    table = {".":"\.",
           "^":"\^",
           "*":"\*",
            "$":"\$",
           "+":"\+",
           "?":"\?",
           "{":"\{",
           "}":"\}",
           "[":"\[",
           "]":"\]",
           "\ ":"\\",
           "|":"\|",
           ")":"\)",
           "(":"\(",
            "\n":"\\n"#,
           # "\t":"\s\s"
          }
    keys = ["DONT_ACCEPT_TRUE_FOR_1","DONT_ACCEPT_BLANKLINE", "NORMALIZE_WHITESPACE","ELLIPSIS",
            "IGNORE_EXCEPTION_DETAIL","SKIP","COMPARISON_FLAGS","REPORT_UDIFF","REPORT_CDIFF","REPORT_NDIFF",
            "REPORT_ONLY_FIRST_FAILURE","REPORTING_FLAGS","register_optionflag"]
    
    
    
    #Function: __init__
    #Inputs: self and para
    #Purpose: sets the self.para variable equal to the provided string
    def __init__(self, para, env, expect):
        self.para = para
        self.env = env
        self.expect = expect
        
        
    #Function: Ellipsis
    #Purpose, to implement the ELLIPSIS function 
    #Inputs: 'looking' - the result that this is looking for
    #       'words' - the body of the answer that this is searching
    def ellipsis(self, looking, words):
        return -1 #This function isn't working yet
        obj = Flags(looking)
        matched = looking.encode(obj.para)
        #Need to match the "..." with "./*" ?
        
        
    # Function: strip_whitespace
    # Purpose: Replaces extra spaces, tabs, and new lines with single spaces
    def strip_whitespace(self, words):
        words = " ".join(words.split())
        return words
        #Split on comments.
        #Split on spaces.
        #Search for keywords.
        #\s* doesn't match 
        # Match with doctest
        
        #doctest +ELLIPSIS
        #split on #doctest:
    

    def flag_search(self):
        docsplit = self.para.split("#doctest:")
        if(len(docsplit) <= 1):
            return -1
        wSplit = docsplit[1].split()
        flags = []
        for i in range (len(wSplit)):
            if(wSplit[i][0] is "+"):
                wSplit[i] = wSplit[i].strip("+")
                if(wSplit[i] in self.keys):
                    flags.append(wSplit[i])
        return flags
    
    
    # Function: run_test
    # Runs the doctest using the Flags object variables.
    def run_test(self):
        '''
        >>> run_test(self.para,self.env,self.expect)
        True
    
        '''
        #If this isn't true I could output a debug message
        return (self.expect == eval(str(self.para),self.env))
    

    # Function: encode
    # Inputs: self, and words (self.para) which should be a string
    # Returns: The encoded version of the words input
    # NOTE: Weird behavior for the \,\\,\t,\n etc.
    def encode(self, words):
        assert type(words) != "str", "Invalid type."
        for word, initial in self.table.items():
            words = words.replace(word, initial)
        return words


# In[ ]:




