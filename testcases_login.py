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
        for theme in range(1,5):
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
        for theme in range(1,5):
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
            sel.click("css=form#signout-form a.signout-button")
            sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])



class TestCase_LoginWithOpenIDAccount_598(testcase_base.testcase_BaseTestCase):
    
    def test_LoginWithOpenIDAccount(self):
        sel = self.selenium
#       Log in as Admin
        loginlogout.LogInAsAdmin(self,sel)
        print "Starting tests..."
        for theme in range(1,5):
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
        for theme in range(1,5):
            print ""
            print "============================================"
            print ""
            print "Running Login with Google account test with theme: "+str(theme)
            print "Changing theme..."
            sitesettings.ChangeTheme(self,sel,theme)
            loginlogout.LogInAsGoogleUser(self,sel,testvars.MCTestVariables["FBLogin"],testvars.MCTestVariables["FBPassword"].decode('base64'))
            loginlogout.LogOut(self,sel)
            print "Logging out from Google..."
            sel.open("http://www.gmail.com")
            sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])
            sel.click("id=gbgs4")
            sel.click("id=gb_71")
            sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])