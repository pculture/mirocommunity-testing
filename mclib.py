# Module MCLIB.PY
# includes:
#   * function remove_html_tags(data) - strips Python string of HTML tags
#   * function remove_punctuation(data) - removes punctuation signs and other
#              meta characters from a string
#   * function remove_digits(data) - removes digits from a string
#   * function split_by_punctuation_char(data) - truncates the string argument
#              by the first punctuation character
#   * subroutine AppendErrorMessage(self,sel,msg) - inserts <msg> error message
#                into verificationErrors list and into output log

import re, testvars

def remove_html_tags(data):
    p = re.compile(r'<.*?>')
    return p.sub('', data)

def remove_punctuation(data):
    p = re.compile(r'(\W+)')
    return p.sub(' ',data)    # A punctuation sign is replaced with a whitespace

def remove_digits(data):
    p = re.compile(r'(\d)')
    return p.sub('',data)    # Digits are eliminated without replacement

def split_by_punctuation_char(data):
    # Split the argument string by:
    # period, comma, semicolon, colon, opening bracket, closing bracket,
    # opening square bracket, closing square bracket, hyphen, underscore,
    # slash, backslash
    # DO NOT split by whitespace
    p = re.split(r'[.,;:\(\)\[\]\-\_/\\]+', data)
    return p[0]


def AppendErrorMessage(self,sel,msg):
    self.verificationErrors.append(msg)
    print testvars.preE+msg


def wait_for_element_present(self, sel, input_field):
    """
    Description: Waits 60 seconds for element to present itself.
    Requires: valid element identifier, can be css, xpath
    """
    
    for i in range(30):
        
        try:
            if sel.is_element_present(input_field): break
        except: pass
        time.sleep(1)
    else:
        self.fail("time out waiting 30s for element " +input_field)
