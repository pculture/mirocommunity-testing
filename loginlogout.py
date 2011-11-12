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
    print "Checking that Facebook tab on Login page exists..."
    if sel.is_element_present(tabFacebook)==False:
        self.fail("Facebook tab not found")
    else:
        print "OK"
        sel.click(tabFacebook)
        time.sleep(7)
        buttonFacebookLogin = "css=div#login_tab_facebook.inactive div.left a"
        if sel.is_element_present(buttonFacebookLogin)==False:
            mclib.AppendErrorMessage(self,sel,"Could not find Login with Facebook button")
        else:
            print "Clicking Log in to Facebook button..."
            sel.click(buttonFacebookLogin)
            time.sleep(5)
        # Enter Facebook user's email address
            if sel.is_element_present("css=input#email.inputtext")==False:
                mclib.AppendErrorMessage(self,sel,"Entry field for Facebook user's EMAIL not found")
            else:
                print "Entering the Facebook user credentials"
                sel.type("css=input#email.inputtext", email)
        # Enter Facebook user's password
            if sel.is_element_present("css=input#pass.inputpassword")==False:
                mclib.AppendErrorMessage(self,sel,"Entry field for Facebook user's password not found")
            else:
                sel.type("css=input#pass.inputpassword", password)
            # Click Login button
            if sel.is_element_present("css=div#login_button_inline label.uiButton input")==False:
                mclib.AppendErrorMessage(self,sel,"Login button on Facebook user's credentials entry form not found")
            else:
                sel.click("css=div#login_button_inline label.uiButton input")
                sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])
                print "Done"
                # Should be at Home page and logged in now
                # Check that "Logout <username>" link is present at the bottom of the page
                print "Checking that user "+username+" is logged on"
                linkLogout = "link=Logout "+username
                if sel.is_element_present(linkLogout)==False:
                    mclib.AppendErrorMessage(self,sel,"'Logout "+username+"' link on Home page not found")
                # Navigating to user profile to check the user's account parameters
                print "Checking the user's profile"
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
# =     LOG IN AS TWITTER USER      =
# ===================================

# This subroutine logs in to MC site as a Twitter user with <username>-<password> credentials

def LogInAsTwitterUser(self,sel,username,password):
    sel.open(testvars.MCTestVariables["LoginPage"])
    sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])
    sel.window_maximize()
    time.sleep(1)
    tabTwitter = "link=Twitter"
    print "Checking that Twitter tab on Login page exists..."
    if sel.is_element_present(tabTwitter)==False:
        self.fail("Twitter tab not found")
    else:
        print "OK"
        sel.click(tabTwitter)
        time.sleep(7)
        buttonTwitterLogin = "css=div#login_tab_twitter.inactive div.left a"
        if sel.is_element_present(buttonTwitterLogin)==False:
            mclib.AppendErrorMessage(self,sel,"Could not find Sign in with Twitter button")
        else:
            print "Clicking Sign in to Twitter button..."
            sel.click(buttonTwitterLogin)
            time.sleep(5)
        # Enter Twitter username address
            if sel.is_element_present("css=input#username_or_email.text")==False:
                mclib.AppendErrorMessage(self,sel,"Entry field for Twitter user's USERNAME not found")
            else:
                print "Entering the Twitter user credentials"
                sel.type("css=input#username_or_email.text", username)
        # Enter Twitter user's password
            if sel.is_element_present("css=input#password.password")==False:
                mclib.AppendErrorMessage(self,sel,"Entry field for Twitter user's password not found")
            else:
                sel.type("css=input#password.password", password)
            # Click Login button
            if sel.is_element_present("css=input#allow.submit")==False:
                mclib.AppendErrorMessage(self,sel,"Login button on Twitter user's credentials entry form not found")
            else:
                sel.click("css=input#allow.submit")
                sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])
                print "Done"
                time.sleep(15)
                # Should be at Home page and logged in now
                # Check that "Logout <username>" link is present at the bottom of the page
                print "Checking that user "+username+" is logged on"
                linkLogout = "link=Logout "+username
                if sel.is_element_present(linkLogout)==False:
                    mclib.AppendErrorMessage(self,sel,"'Logout "+username+"' link on Home page not found")
                # Navigating to user profile to check the user's account parameters
                print "Checking the user's profile"
                linkYourProfile = "link=Your Profile"
                if sel.is_element_present(linkYourProfile)==False:
                    mclib.AppendErrorMessage(self,sel,"'Your profile' link on Home page not found")
                else:
                    sel.click("link=Your Profile")
                    sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])
                    print "Checking Twitter user's name on Profile page..."
                    if sel.is_element_present("css=div.form_box input#id_username")==False:
                        mclib.AppendErrorMessage(self,sel,"User Name field on Profile page not found")
                    else:
                        if sel.get_value("css=div.form_box input#id_username")!=username:
                            mclib.AppendErrorMessage(self,sel,"Unexpected user name found")
                            print "Expected user name: "+username
                            print "- Actual user name: "+sel.get_value("css=div.form_box input#id_username")
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

