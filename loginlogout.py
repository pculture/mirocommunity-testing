# Module LOGINLOGOUT.PY
# includes:
#   * function LogInBasic(self,sel,username,password) - logs in to MC site 
#            with <username>-<password> credentials. Returns True if successfully
#            logged in (or could not check) and False if check failed
#   * subroutine LogInAsAdmin(self,sel) - logs in to MC site with AdminLogin
#            and AdminPassword
#   * subroutine LogInAsUser(self,sel) - logs in to MC site with UserLogin
#            and UserPassword
#   * subroutine LogOut(self,sel) - logs out from MC site

from selenium import selenium

import unittest, time, re, testvars, mclib

# ===================================
# =          LOG IN BASIC           =
# ===================================

# This subroutine logs in to MC site with <username>-<password> credentials

def LogInBasic(self,sel,username,password):
    sel.open(testvars.MCTestVariables["LoginPage"])
    sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])
    sel.window_maximize()
    sel.click("id_username")
    sel.type("id_username", username)
    sel.click("id_password")
    sel.type("id_password", password)
    sel.click("//input[@value='Log In']")
    sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])
    if sel.is_element_present(testvars.MCTestVariables["LogoutFootlink"])==True:
        currentUser = sel.get_text(testvars.MCTestVariables["LogoutFootlink"])
        if currentUser.find(username)!=-1:
            print "Logged in as "+username
            return True
        else:
            mclib.AppendErrorMessage(self,sel,"Attempted to login as "+username+". Could not verify successful logon")
            return False
    else:
        mclib.AppendErrorMessage(self,sel,"Could not find Logout link on page.")
        return True


# ===================================
# =        LOG IN AS ADMIN          =
# ===================================

# This subroutine logs in to MC site with AdminLogin and AdminPassword

def LogInAsAdmin(self,sel):
    LogInBasic(self,sel,testvars.MCTestVariables["AdminLogin"],testvars.MCTestVariables["AdminPassword"])
#    self.assertTrue(sel.is_text_present("View Admin"))
    try: self.failUnless(sel.is_text_present("View Admin"))
    except AssertionError, e:
        self.verificationErrors.append("Not logged in as Selenium Test Administrator")
        self.failIf(True)
#        try: self.failUnless(sel.is_text_present("View Admin"))
#        except AssertionError, e: self.verificationErrors.append(str(e))


# ===================================
# =         LOG IN AS USER          =
# ===================================

# This subroutine logs in to MC site with UserLogin and UserPassword

def LogInAsUser(self,sel):
    bLoggedIn = LogInBasic(self,sel,testvars.MCTestVariables["UserLogin"],testvars.MCTestVariables["UserPassword"])
#    self.assertTrue(sel.is_text_present("View Admin"))
    try: self.failUnless(bLoggedIn==True)
    except AssertionError, e:
#        self.verificationErrors.append("Not logged in as Selenium Test User")
#        self.failIf(True)
        self.fail("Not logged in as Selenium Test User")



# ===================================
# =              LOG OUT            =
# ===================================
 
# This subroutine logs out of MC site 

def LogOut(self,sel):
    sel.open(testvars.MCTestVariables["LogoutPage"])
    sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])
    self.assertFalse(sel.is_text_present("View Admin"))
