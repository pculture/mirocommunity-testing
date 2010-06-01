# Module MCLIB.PY
# includes:
#   * function remove_html_tags(data) - strips Python string of HTML tags
#   * subroutine AppendErrorMessage(self,sel,msg) - inserts <msg> error message
#                into verificationErrors list and into output log

import re, testvars

def remove_html_tags(data):
    p = re.compile(r'<.*?>')
    return p.sub('', data)


def AppendErrorMessage(self,sel,msg):
    self.verificationErrors.append(msg)
    print testvars.preE+msg
