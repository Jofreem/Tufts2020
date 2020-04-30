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
    

    #Inputs: self and para
    #Purpose: Initializes class variables
    def __init__(self, para, expect = None, ans = None, flags = None):
        self.para = para
        self.expect = expect
        self.ans = ans
        self.flags = None
        

    #Purpose: Returns flags in input string
    def get_flags(self):
        self.flag_search()
        return(self.flags)
    

    #Purpose: Searches the .py file for flags
    #Effects: Will add/remove flags, or throw error if they aren't recognized.
    def flag_search(self):
        docsplit = self.para.split("#doctest:")
        if(len(docsplit) <= 1):
            return -1
        wSplit = docsplit[1].split(",")
        
        flags = set([]) #TODO: Default flags set here

        pattern = re.compile(r'(\s?)([+-]{1})+(./*)')
        for i in range(len(wSplit)):
            results = pattern.finditer(wSplit[i])
            for result in results:
                #print('result: {}'.format(result)) #NOTE: Uncomment to view the registered flags.
                if("+" in result.string[:]):
                    flags.add(wSplit[i].strip().strip("+"))
                elif("-" in result.string[:]):
                    flags.discard(wSplit[i].strip().strip("-"))
                else:
                    print('Error flag {} not recognized'.format(result))
        self.flags = self.validate_flags(flags)
        #TODO: Fix the flag search to make spaces between commas optional
    

    #Input: 'flags' - set of flags 
    #Purpose: Checks the flags to see if they exist in the "keys" list
    #Effects: Removes the non-valid flags
    def validate_flags(self,flags):
        flags.intersection_update(set(self.keys))
        print('flgs: {}'.format(flags))
        return flags
    
    
    #Purpose: Searches and applies for flags then returns outcome
    #Effects: Calls compare_ans, returns True/False
    def decide_correct(self):
        self.apply_flags()
        if(self.compare_ans()["passed"] is 1):
            return True
        else:
            return False
        
        
    #Purpose: Getter to replace the answer
    def get_output(self):
        return self.ans
        
        
    #Input: 'flags' - the set of desired flags
    #Purpose: Applies the desired flags, or will print out an error if they have not been implemented
    #Effects: Can call ellipsis(), strip_whitespace(), and/or lock the question.
    def apply_flags(self):
        if(type(self.flags) != set):
            return
        if('ELLIPSIS' in self.flags):
            self.ellipsis()
        if('NORMALIZE_WHITESPACE' in self.flags):
            self.ans = self.strip_whitespace(self.ans)
            self.expect = self.strip_whitespace(self.expect)
        if('SKIP' in self.flags):
            self.locked = True
        for i in self.flags:
            if(i in self.keys and i not in self.implemented_keys):
                print("Error: flag {} not implemented".format(i))
    

    #Purpose, to implement the ELLIPSIS function 
    #Inputs: 'looking' - the result that this is looking for
    #       'words' - the body of the answer that this is searching
    def ellipsis(self):
        first = self.encode(self.expect)
        second = first.replace(r"\.\.\.", r".*")
        toMatch = re.compile(second)
        result = re.search(toMatch, self.ans)
        if(result.group() == self.ans):
            self.expect = self.ans
            

    # Inputs: 'words' - string to encode (self.para)
    # Returns: The encoded version of the words input
    # NOTE: Weird behavior for the \,\\,\t,\n etc.
    def encode(self, words):
        assert type(words) != "str", "Invalid type."
        for word, initial in self.table.items():
            words = words.replace(word, initial)
        return words


    # Purpose: Replaces extra spaces, tabs, and new lines with single spaces
    def strip_whitespace(self, words):
        if(not words is None):
            words = " ".join(words.split())
        return words    


    # Purpose: Returns a list with the passed and failed tests
    def compare_ans(self):
        results = {"passed":0, "failed":0,"locked":0}
        if(str(self.expect) == str(self.ans)):
            results["passed"] += 1
        else:
            results["failed"] += 1
        return results