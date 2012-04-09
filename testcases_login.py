#=======================================================================
#
#                             LOGIN / LOGOUT TESTS
#
#=======================================================================
#
# Includes the following test cases:
#     1. TestCase_LoginWithFacebookAccount_596
#     2. TestCase_LoginWithTwitterAccount_597
#     3. TestCase_LoginWithOpenIDAccount_598
#     4. TestCase_LoginWithGoogleAccount_599
#     5. TestCase_SignUpAndLogin_600


from selenium import selenium
import imaplib
import unittest, os, time, re, mclib, testcase_base
import loginlogout, sitesettings, testvars, categories, submitvideos, sitesettings, queue, videopage
import sys

# ----------------------------------------------------------------------

class TestCase_LoginWithFacebookAccount_596(testcase_base.testcase_BaseTestCase):
    
    def test_LoginWithFBAccount(self):
        sel = self.selenium
#       Log in as Admin
        loginlogout.LogInAsAdmin(self,sel)
        print "Starting tests..."
        for theme in range(1,4):
            print ""
            print "============================================"
            print ""
            print "Running Login with Facebook account test with theme: "+str(theme)
            print "Changing theme..."
            sitesettings.ChangeTheme(self,sel,theme)
            loginlogout.LogInAsFacebookUser(self,sel,testvars.MCTestVariables["FBUsername"],testvars.MCTestVariables["FBLogin"],testvars.MCTestVariables["FBPassword"].decode('base64'))
            loginlogout.LogOut(self,sel)
            print "Logging out from Facebook..."
            sel.open("http://www.facebook.com")
            sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])
            sel.click("css=label.uiLinkButton input")
            sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])



class TestCase_LoginWithTwitterAccount_597(testcase_base.testcase_BaseTestCase):
    
    def test_LoginWithTwitterAccount(self):
        sel = self.selenium
#       Log in as Admin
        loginlogout.LogInAsAdmin(self,sel)
        print "Starting tests..."
        for theme in range(1,4):
            print ""
            print "============================================"
            print ""
            print "Running Login with Twitter account test with theme: "+str(theme)
            print "Changing theme..."
            sitesettings.ChangeTheme(self,sel,theme)
            loginlogout.LogInAsTwitterUser(self,sel,testvars.MCTestVariables["TwitterLogin"],testvars.MCTestVariables["TwitterPassword"].decode('base64'))
            loginlogout.LogOut(self,sel)
            print "Logging out from Twitter..."
            sel.open("http://www.twitter.com")
            sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])
            sel.click("css=span.caret")
            sel.click("css=a#signout-button")

class TestCase_LoginWithOpenIDAccount_598(testcase_base.testcase_BaseTestCase):
    
    def test_LoginWithOpenIDAccount(self):
        sel = self.selenium
#       Log in as Admin
        loginlogout.LogInAsAdmin(self,sel)
        print "Starting tests..."
        for theme in range(1,4):
            print ""
            print "============================================"
            print ""
            print "Running Login with OpenID account test with theme: "+str(theme)
            print "Changing theme..."
            sitesettings.ChangeTheme(self,sel,theme)
            loginlogout.LogInAsOpenIDUser(self,sel,testvars.MCTestVariables["OpenIDLogin"],testvars.MCTestVariables["OpenIDPassword"].decode('base64'))
            loginlogout.LogOut(self,sel)
            print "Logging out from myopenid.com..."
            sel.open("http://www.myopenid.com")
            sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])
            sel.click("link=Sign Out")
            sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])


class TestCase_LoginWithGoogleAccount_599(testcase_base.testcase_BaseTestCase):
    
    def test_LoginWithGoogleAccount(self):
        sel = self.selenium
#       Log in as Admin
        loginlogout.LogInAsAdmin(self,sel)
        print "Starting tests..."
        for theme in range(1,4):
            print ""
            print "============================================"
            print ""
            print "Running Login with Google account test with theme: "+str(theme)
            print "Changing theme..."
            sitesettings.ChangeTheme(self,sel,theme)
            loginlogout.LogInAsGoogleUser(self,sel,testvars.MCTestVariables["TestEmail"],testvars.MCTestVariables["TestEmailPassword"].decode('base64'))
            loginlogout.LogOut(self,sel)

class TestCase_SignUpAndLogin_600(testcase_base.testcase_BaseTestCase):
    
    def test_SignUpAndLogin(self):
        sel = self.selenium
#       Log in as Admin
        loginlogout.LogInAsAdmin(self,sel)
        print "Starting tests..."
        for theme in range(1,4):
            print ""
            print "============================================"
            print ""
            print "Running Sign Up and Login test with theme: "+str(theme)
            print "Changing theme..."
            sitesettings.ChangeTheme(self,sel,theme)
            loginlogout.LogOut(self,sel)
            newUsername = "test_"+time.strftime("%d_%m_%Y__%H_%M", time.localtime())+"_theme"+str(theme)
            newPassword = "testpassword"
            print "Signing up as user "+newUsername
            loginlogout.SignUp(self,sel,newUsername,newPassword,testvars.MCTestVariables["TestEmail"])
            loginlogout.ActivateUserAccount(self,sel,testvars.MCTestVariables["TestEmail"],testvars.MCTestVariables["TestEmailPassword"].decode('base64'))
            loginlogout.LogInBasic(self,sel,newUsername,newPassword)
            # Navigating to user profile to check the user's account parameters
            print "Checking the user's profile..."
            linkYourProfile = "link=Your Profile"
            if sel.is_element_present(linkYourProfile)==False:
                mclib.AppendErrorMessage(self,sel,"'Your profile' link on Home page not found")
            else:
                sel.click("link=Your Profile")
                sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])
                if sel.get_value("id_email")!=testvars.MCTestVariables["TestEmail"]:
                    mclib.AppendErrorMessage(self,sel,"Unexpected user email encountered in User Profile")
                    print "Expected email: "+testvars.MCTestVariables["TestEmail"]
                    print "- Actual email: "+sel.get_value("id_email")
                    print "Checking user's name on Profile page..."
                if sel.is_element_present("id_username")==False:
                    mclib.AppendErrorMessage(self,sel,"User Name field on Profile page not found")
                else:
                    if sel.get_value("id_username")!=newUsername:
                        mclib.AppendErrorMessage(self,sel,"Unexpected user name found")
                        print "Expected user name: "+newUsername
                        print "- Actual user name: "+sel.get_value("id_username")
                    else:
                        print "OK"
