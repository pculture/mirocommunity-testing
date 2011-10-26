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
#   * subroutine LogInAsFacebookUser(self,sel,username,email,password) - logs in
#            to MC site as a Facebook user with <email>-<password> credentials
#            The user becomes known to the system as <username>
#   * subroutine LogInToFacebook(self,sel) - logs in to Facebook with the use
#            of PCF test account
#   * subroutine LogInToTwitter(self,sel) - logs in to Twitter with the use
#            of PCF test account

from selenium import selenium

import unittest, time, re, testvars, mclib

# ===================================
# =          LOG IN BASIC           =
# ===================================

# This subroutine logs in to MC site with <username>-<password> credentials

def LogInBasic(self,sel,username,password):
    sel.set_timeout(testvars.MCTestVariables["TimeOut"])
    sel.open(testvars.MCTestVariables["LoginPage"])
    sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])
    sel.window_maximize()
    time.sleep(1)
    sel.click("id_username")
    sel.type("id_username", username)
    time.sleep(1)
    sel.click("id_password")
    sel.type("id_password", password)
    time.sleep(1)
    sel.click("//input[@value='Log In']")
    time.sleep(7)
#    sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])
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


# ===================================
# =    LOG IN AS FACEBOOK USER      =
# ===================================

# This subroutine logs in to MC site as a Facebook user with <email>-<password> credentials
# The user becomes known to the system as <username>

def LogInAsFacebookUser(self,sel,username,email,password):
    sel.open(testvars.MCTestVariables["LoginPage"])
    sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])
    sel.window_maximize()
    time.sleep(1)
    tabFacebook = "link=Facebook"
    if sel.is_element_present(tabFacebook)==False:
        self.fail("Facebook tab not found")
#    sel.click(tabFacebook)
#    time.sleep(3)
    sel.open(testvars.MCTestVariables["FacebookLoginPage"])
    sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])
    if sel.is_text_present("Facebook Login"):
        #buttonLogin = "//img[@alt='Sign In with Twitter']"
        #if sel.is_element_present(buttonLogin)==False:
        #    mclib.AppendErrorMessage(self,sel,"Login button on Facebook tab not found")
        #else:
        #    sel.click(buttonLogin)
        #    sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])
        # Enter Facebook user's email address
        if sel.is_element_present("email")==False:
            mclib.AppendErrorMessage(self,sel,"Entry field for Facebook user's EMAIL not found")
        else:
            sel.type("email", email)
        # Enter Facebook user's password
        if sel.is_element_present("pass")==False:
            mclib.AppendErrorMessage(self,sel,"Entry field for Facebook user's password not found")
        else:
            sel.type("pass", password)
        # Click Login button
        if sel.is_element_present("u041464_1")==False:
            mclib.AppendErrorMessage(self,sel,"Login button on Facebook user's credentials entry form not found")
        else:
            sel.click("u041464_1")
            sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])
            # Should be at Home page and logged in now
            # Check that "Logout <username>" link is present at the bottom of the page
            linkLogout = "link=Logout "+username
            if sel.is_element_present(linkLogout)==False:
                mclib.AppendErrorMessage(self,sel,"'Logout "+username+"' link on Home page not found")
            # Navigating to user profile to check the user's account parameters
            linkYourProfile = "link=Your Profile"
            if sel.is_element_present(linkYourProfile)==False:
                mclib.AppendErrorMessage(self,sel,"'Your profile' link on Home page not found")
            else:
                sel.click("link=Your Profile")
                sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])
                print "Checking Facebook user's name on Profile page..."
                if sel.is_element_present("id_name")==False:
                    mclib.AppendErrorMessage(self,sel,"User Name field on Profile page not found")
                else:
                    if sel.get_value("id_name")!=username:
                        mclib.AppendErrorMessage(self,sel,"Unexpected user name found")
                        print "Expected user name: "+username
                        print "- Actual user name: "+sel.get_value("id_name")
                    else:
                        print "OK"



# ===================================
# =    LOG IN TO FACEBOOK SITE      =
# ===================================

# This subroutine logs in to Facebook with the use of PCF test account

def LogInToFacebook(self,sel):
    sel.open("http://www.facebook.com")
    sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])
    sel.window_maximize()
    time.sleep(1)
    sel.type("id=email", testvars.MCTestVariables["FBLogin"])
    sel.type("id=pass", testvars.MCTestVariables["FBPassword"].decode('base64'))
    sel.click("css=input[value='Log In']")
    sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])


# ===================================
# =     LOG IN TO TWITTER SITE      =
# ===================================

# This subroutine logs in to Twitter with the use of PCF test account

def LogInToTwitter(self,sel):
    sel.open("http://www.twitter.com")
    sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])
    sel.window_maximize()
    time.sleep(1)
#    sel.click("css=div.username > span.holder")
#    sel.type("css=div.username > span.holder", testvars.MCTestVariables["TwitterLogin"])
#    sel.type("css=div.password > span.holder", testvars.MCTestVariables["TwitterPassword"])
    sel.type("css=div.username > input", testvars.MCTestVariables["TwitterLogin"])
    sel.type("css=div.password > input", testvars.MCTestVariables["TwitterPassword"].decode('base64'))
    sel.click("css=div.front-signin > form.signin > fieldset.subchck > button.submit.button")
    sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])

