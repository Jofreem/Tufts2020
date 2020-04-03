#!/usr/bin/env python
# coding: utf-8

# In[2]:


import re
class WithFlags:
    #Class variable - table
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
    def __init__(self, para, env, expect, ans):
        self.para = para
        self.env = env
        self.expect = expect
        self.ans = ans
        
        
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
    
    def apply_flags(self, flags):
        if(type(flags) != list):
            return
        if('ELLIPSIS' in flags):
            print('CALLED ELLIPSIS')
        if('NORMALIZE_WHITESPACE' in flags):
            self.ans = self.strip_whitespace(self.ans)
            print('Whitespace has been normalized')
    
    def eval_ans(self):
        self.ans = eval(str(self.para), self.env) #Computes the answer
        self.apply_flags(self.flag_search()) #Checks for flags
        return self.compare_ans() #Compares to see if they match
    
    # Function: run_test
    # Runs the doctest using the Flags object variables.
    def compare_ans(self):
        #print('self.expect: {}'.format(self.expect)) #Debugging
        #print('self.ans: {}'.format(self.ans)) #Debugging
        return (self.expect == self.ans)
    

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




