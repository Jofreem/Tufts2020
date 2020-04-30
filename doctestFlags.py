""" 
Additional class for implementing flags to the okpy autograder 
Implemented through existing code system through: 

- sources/common/interpreter.py

- sources.ok_test/doctest.py
- sources/ok_test/models.py
- sources/common/interpreter.py

Instance Variables:
para - The input command & any flags*
env - Environment to execute code in
expect - The expected output*
ans - The evaluated answer from the exec function
* = Declared in q*.py file
"""

import re
class WithFlags:
    #table - dict of Python special characters with their replacements
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
            "\n":"\\n"
          }
    
    #keys - list of known doctest keys
    keys = ["DONT_ACCEPT_TRUE_FOR_1","DONT_ACCEPT_BLANKLINE", "NORMALIZE_WHITESPACE","ELLIPSIS",
            "IGNORE_EXCEPTION_DETAIL","SKIP","COMPARISON_FLAGS","REPORT_UDIFF","REPORT_CDIFF","REPORT_NDIFF",
            "REPORT_ONLY_FIRST_FAILURE","REPORTING_FLAGS","register_optionflag"]
    
    #implemented_keys - list of implemented keys in this file
    implemented_keys = ["NORMALIZE_WHITESPACE", "SKIP", "ELLIPSIS"]
    
    #Locked - can be turned on to lock a question
    locked = False
    
    #Function: __init__
    #Inputs: self and para
    #Purpose: Initializes class variables
    def __init__(self, para, env = None, expect = None, ans = None ):
        self.para = para
        self.env = env
        self.expect = expect
        self.ans = ans
        
        
    #Function: Ellipsis
    #Purpose, to implement the ELLIPSIS function 
    #Inputs: 'looking' - the result that this is looking for
    #       'words' - the body of the answer that this is searching
    def ellipsis(self):
        print('inside ellipsis')
        first = self.encode(self.expect)
        first = self.expect.replace(r"...",r"/././.")
        second = first.replace(r"/././.", r".*")
        toMatch = re.compile(second)
        
        result = re.search(toMatch, self.ans)
        if(result.group() == self.ans):
            self.expect = self.ans

        
        
    # Function: strip_whitespace
    # Purpose: Replaces extra spaces, tabs, and new lines with single spaces
    def strip_whitespace(self, words):
        if(not words is None):
            words = " ".join(words.split())
        return words
    

    #Function: flag_search
    #Purpose: Searches the .py file for flags
    #Effects: Will add/remove flags, or throw error if they aren't recognized.
    def flag_search(self):
        docsplit = self.para.split("#doctest:")
        if(len(docsplit) <= 1):
            return -1
        wSplit = docsplit[1].split()
        
        flags = set([]) #TODO: Incorporate provided flags, which would be set here.

        pattern = re.compile(r'([+-]{1})(./*)+(.,?)')
        for i in range(len(wSplit)):
            results = pattern.finditer(wSplit[i])
            for result in results:
                #print('result: {}'.format(result)) #NOTE: Uncomment to view the registered flags.
                if(result.string[0] is "+"):
                    flags.add(wSplit[i].strip("+").strip(","))
                elif(result.string[0] is "-"):
                    flags.discard(wSplit[i].strip("-").strip(","))
                else:
                    print('Error flag {} not recognized'.format(result))
        return self.validate_flags(flags)
    
    
    #Function: validate_flags
    #Input: 'flags' - set of flags 
    #Purpose: Checks the flags to see if they exist in the "keys" list
    #Effects: Removes the non-valid flags
    def validate_flags(self,flags):                         
        for flag in flags:
            if(flag not in self.keys):
                flags.discard(flag)
        return flags
    
    
    #Function: apply_flags
    #Input: 'flags' - the set of desired flags
    #Purpose: Applies the desired flags, or will print out an error if they have not been implemented
    #Effects: Can call ellipsis(), strip_whitespace(), and/or lock the question.
    def apply_flags(self, flags):
        if(type(flags) != set):
            return
        if('ELLIPSIS' in flags):
            self.ellipsis()
        if('NORMALIZE_WHITESPACE' in flags):
            self.ans = self.strip_whitespace(self.ans)
            self.expect = self.strip_whitespace(self.expect)
        if('SKIP' in flags):
            self.locked = True
        for i in flags:
            if(i in self.keys and i not in self.implemented_keys):
                print("Error: flag {} not implemented".format(i))
    
    #Function: eval_ans
    #Purpose: Evaluates the answer, searches for flags that might change the answer, then
    #compares the expected and evaluated answers.
    #Effects: Calls flag_search, apply_flags, and compare_ans
    #Returns: The compare_ans list
    #NOTE: This behaves similar to a 'main,' by calling most of the member functions
    def eval_ans(self):
        self.ans = eval(str(self.para), self.env)
        self.apply_flags(self.flag_search())
        if(self.locked):
            return {"passed":0, "failed":0,"locked":1}
        return self.compare_ans()
    
    
    #Function: get_output
    #Purpose: For getting the new output after flags have been applied
    #NOTE: This is only accurate if decide_correct() has already been called.
    #Effects: Returns a string
    def get_output(self):
        return self.ans
    
    
    def get_flags(self):
        return(self.flag_search())
    
    
    #Function: decide_correct
    #Purpose: Searches and applies for flags then returns outcome
    #Effects: Calls compare_ans, returns True/False
    def decide_correct(self):
        self.apply_flags(self.flag_search())
        if(self.compare_ans()["passed"] is 1):
            return True
        else:
            return False
    
    
    # Function: compare_ans
    # Purpose: Returns a list with the passed and failed tests
    def compare_ans(self):
        results = {"passed":0, "failed":0,"locked":0}
        if(str(self.expect) == str(self.ans)):
            results["passed"] += 1
        else:
            results["failed"] += 1
        return results
    

    # Function: encode
    # Inputs: 'words' - string to encode (self.para)
    # Returns: The encoded version of the words input
    # NOTE: Weird behavior for the \,\\,\t,\n etc.
    def encode(self, words):
        assert type(words) != "str", "Invalid type."
        for word, initial in self.table.items():
            words = words.replace(word, initial)
        return words
