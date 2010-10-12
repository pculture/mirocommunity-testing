#=======================================================================
#
#                             COMMENTS TESTS
#
#=======================================================================
#
# Includes the following test cases:
#     1. testcase_Comments_NoModeration_NoLogin
#     2. testcase_Comments_NoModeration_LoginRequired
#     3. testcase_Comments_ModerationRequired_NoLogin
#     4. testcase_Comments_ModerationRequired_LoginRequired

from selenium import selenium
import unittest, time, re, loginlogout, sitesettings, categories, testvars
import sys

global initialCategories
initialCategories = [""]
# ----------------------------------------------------------------------

#------ Variables ---------
import random

global gFirstVideoMainPageListTheme
gFirstVideoMainPageListTheme = "//h2[@class='vid_title']/a"

global gPostCommentButton
gPostCommentButton = "//p[@class='submit']/input[@name='submit']"

global gTestPosterName
gTestPosterName = '//input[@id="id_name"]'

global gLogInButtonInPopUpWindow
gLogInButtonInPopUpWindow = "//input[@value='Log In']"

global gUserLogin
gUserLogin = 'seleniumTestUser'

global gUserPassword
gUserPassword = 'selenium'

global gCommentModerationText
gCommentModerationText = 'Your comment has been sent to the moderators.'

global gSeleniumServerPort
gSeleniumServerPort = testvars.MCTestVariables["Port"]

global gTimeOut
gTimeOut = 20

global gLoginButtonInLoginPopUpWindow
gLoginButtonInLoginPopUpWindow = "//input[@value='Log In']"


class ThemeStruct:
    themePath = None
    firstVideoOnPage = None
    postCommentButton = None
    postCommentButtonAdmin = None
    posterNameEditField = None
    commentEditField = None
    posterEmailEditField = None
    deleteCommentButtonPart1 = None
    deleteCommentButtonPart2 = None
    
    def __init__(self, inThemePath, inFirstVideoOnPage, inPostCommentButton, inPostCommentButtonAdmin,
                 inPosterNameEditField, inCommentEditField, inPosterEmailEditField, inDeleteCommentButtonPart1, inDeleteCommentButtonPart2):
        self.themePath = inThemePath
        self.firstVideoOnPage = inFirstVideoOnPage
        self.postCommentButton = inPostCommentButton
        self.postCommentButtonAdmin = inPostCommentButtonAdmin
        self.posterNameEditField = inPosterNameEditField
        self.commentEditField = inCommentEditField
        self.posterEmailEditField = inPosterEmailEditField
        self.deleteCommentButtonPart1 = inDeleteCommentButtonPart1
        self.deleteCommentButtonPart2 = inDeleteCommentButtonPart2

global gListTheme
gListTheme = ThemeStruct( testvars.MCTestVariables["ListThemeLink"], "//h2[@class='vid_title']/a", "//p[@class='submit']/input[@name='submit']",
                          "//p[@class='submit']/input[@name='submit']", '//input[@id="id_name"]', "id_comment", "id_email",
                          "//li[contains(.,'", "')]/div/div/form[button='delete']/button")

global gScrollingTheme
gScrollingTheme = ThemeStruct( testvars.MCTestVariables["ScrollingThemeLink"], "//div[@id='content']/div[4]/div[2]/div/h3/a", "submit", "submit",
                               "id_name", "id_comment", "id_email",
                              "//li[contains(.,'", "')]/div/div/form[button='delete']/button")

global gCategoryTheme
gCategoryTheme = ThemeStruct( testvars.MCTestVariables["CategoryThemeLink"], "//div[@id='content']/div[4]/div[2]/div/h3/a", "submit", "submit",
                              "id_name", "id_comment", "id_email" ,
                              "//li[contains(.,'", "')]/div/div/form[button='delete']/button")

global gBlueTheme
gBlueTheme = ThemeStruct( testvars.MCTestVariables["BlueThemeLink"], "//div[@id='content']/div/div[2]/ul[1]/li[1]/div/h2/a", "//button[@type='submit']",
                          "//form[@id='comment_form']/p[4]/button", "id_name", "id_comment", "id_email",
                          "//li[contains(.,'", "')]/div/form[button='delete']/button")

global gAllThemes
gAllThemes = [gListTheme,gScrollingTheme,gCategoryTheme,gBlueTheme]
#//li[contains(.,'Vasya')]/div/form[button="delete"]/button                

"""
"ScrollingThemeLink":"/admin/themes/set_default/2", \
"CategoryThemeLink":"/admin/themes/set_default/3", \
"BlueThemeLink":"/admin/themes/set_default/4", \
"""

#-------------------------

#------ Functions --------

def WaitUntilTextOnTheScreen(sel, text, inTime):
    ltime = 0
    while (ltime < inTime):
        if sel.is_text_present(text):
            return True
        time.sleep(1)
        ltime = ltime + 1
    return False

def WaitUntilElementOnTheScreen(sel, inElement, inTime):
    ltime = 0
    while (ltime < inTime):
        if sel.is_element_present(inElement):
            return True
        time.sleep(1)
        ltime = ltime + 1
    return False

#function to generate comments which contains date and time function was called
def generateComment():
    ltime = str( time.localtime().tm_hour) + 'h' + str( time.localtime().tm_min) + 'm' +  str( time.localtime().tm_sec ) + 'sec_'
    comment = "Test comment:_"+ltime+str( time.localtime().tm_mday)+'/'+str(time.localtime().tm_mon)+'/'+str(time.localtime().tm_year)
    return comment

#function which performs login with given Login and Password
def LogIn(sel, Login, Password):
    sel.open("/")
    sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])
    sel.click("link=Login")
    if (not WaitUntilElementOnTheScreen(sel, gLoginButtonInLoginPopUpWindow, gTimeOut)):
        return False
    sel.window_maximize()
    sel.click("id_username")
    sel.type("id_username", Login)
    sel.click("id_password")
    sel.type("id_password", Password)
    sel.click(gLoginButtonInLoginPopUpWindow)
    sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])
    sel.open("/")
    return True

#changes additional setting(page has to be opened prior to function's call)
def ChangeAdditionalSettings(sel, DisplaySubmitVideoNavItem, RequireUsersToLoginToSubmitVideo,
                             UseOriginalDate, HoldCommentsForModeration, RequireLogin):
    
    if (not WaitUntilElementOnTheScreen(sel, "id_display_submit_button", gTimeOut)):
       return False
            
    if DisplaySubmitVideoNavItem:
        sel.check("id_display_submit_button")
    else:
        sel.uncheck("id_display_submit_button")

    if RequireUsersToLoginToSubmitVideo:
        sel.check("id_submission_requires_login")
    else:
        sel.uncheck("id_submission_requires_login")             

    if UseOriginalDate:
        sel.check("id_use_original_date")
    else:
        sel.uncheck("id_use_original_date")                     

    if HoldCommentsForModeration:
        sel.check("id_screen_all_comments")
    else:
        sel.uncheck("id_screen_all_comments")                           

    if RequireLogin:
        sel.check("id_comments_required_login")
    else:
        sel.uncheck("id_comments_required_login")

    return True        
    

#----------------------
#as setUp() and tearDown() are the same for all test cases we have a good reason to inlude them into one base class
class testcase_BaseTestCase(unittest.TestCase):
    
    def setUp(self):
        self.verificationErrors = []
        self.selenium = selenium("localhost", gSeleniumServerPort, testvars.MCTestVariables["Browser"], testvars.MCTestVariables["TestSite"])
        self.selenium.start()

    def test_case():
        return 1

    def tearDown(self):
        self.selenium.stop()
        self.assertEqual([], self.verificationErrors)        

#base class for all test cases related to comments
class testcase_BaseComments(testcase_BaseTestCase):

    #generated comments are saved in these variables
    comment = ""
    commentNotLogged = ""
    commentUser = ""
    commentAdmin = ""

    #shows if comment was posted by not logged in user
    bCommentNotLogged = 0

    #XPath to the first video on Main Page, it is necessary because of using different themes
    firstVideoOnMainPage = None

    #Theme which should be tested
    themeToTest = None    

    #boolean variable which defines if theme has to be setup prior to test execution
    bSetTheme = 1
    #boolean variable which defines value to set for 'Hold comments for moderation' option from additional setting 
    bHoldForModeration = 0
    #boolean variable which defines value to set for 'Require Login' option from additional setting
    bRequireLogin = 0    

    #function to call in order to test AUT when user is not logged in
    NotLoggetTest = None
    #function to call in order to test AUT when user is logged in as User
    UserTest = None
    #function to call in order to test AUT when user is logged in as Admin
    AdminTest = None

    #tests if comment can be posted by not logged in user
    def NotLogged_CommentPosted(self):
        #print "Log--> Executing NotLogged_CommentPosted()"                        
        sel = self.selenium
        print "Clicking first video on the page..."
        sel.click(self.themeToTest.firstVideoOnPage)
        sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])
        print "Generating and posting a comment..."                        
        self.commentNotLogged = generateComment()
        self.bCommentNotLogged = 1
        sel.type(self.themeToTest.commentEditField, self.commentNotLogged)
        sel.type( self.themeToTest.posterNameEditField, "TestPoster")
        sel.click(self.themeToTest.postCommentButton)
        sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])
        print 'Asserting comment is on the page...'
        self.failUnless(sel.is_text_present(self.commentNotLogged))
#        print 'Log----> Going back to the main page'
        sel.open("/")

    #tests possibility of posting a comment when user is not logged in
    def NotLogged_NotPossibleToPost(self):
        #print "Log--> Executing NotLogged_NotPossibleToPost()"                        
        sel = self.selenium
        sel.click(self.themeToTest.firstVideoOnPage)
        print "Clicking first video on the page..."  
        sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])
        print "Checking that input fields to post a comment are not on the page..."
        self.failIf(sel.is_element_present(self.themeToTest.commentEditField))
        self.failIf(sel.is_element_present(self.themeToTest.posterNameEditField))
        self.failIf(sel.is_element_present(self.themeToTest.posterEmailEditField))
#        print 'Log----> Going back to the main page'
        sel.open("/")

    #tests application when user is not logged in and all comments have to be moderated by admin
    def NotLogged_ModerationRequired(self):
        #click on the first video and post comment as not logged in user
        #print "Log--> Executing NotLogged_ModerationRequired()"                        
        sel = self.selenium
        print "Clicking on the first video on the page..."
        sel.click(self.themeToTest.firstVideoOnPage)
        sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])
        self.bCommentNotLogged = 1
        print "Generating and posting new comment..."        
        self.commentNotLogged = generateComment()
        sel.type(self.themeToTest.commentEditField, self.commentNotLogged)
        sel.type(self.themeToTest.posterNameEditField, "TestPoster")
        sel.click(self.themeToTest.postCommentButton)
        #wait until notification that comment was sent to moderators presents on the page
        print "Waiting for notification that comment was sent to moderators..."
        if (not WaitUntilTextOnTheScreen(sel, gCommentModerationText, gTimeOut)):
            print "ERROR: Notification that comment was sent to moderators is not on the page"
            self.failIf(True)
        else:
            print 'Text "', gCommentModerationText, '" is on the page'

        #login as admin and approve the comment that was sent in previous step
        print 'Logging in as Admin...'
        loginlogout.LogInAsAdmin(self,sel)
        print 'Opening Admin|Comments page and approving previously posted comment...'
        sel.click("link=View Admin")
        sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])
        sel.click("link=Comments")
        sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])
        sel.click('//tr[td="' + self.commentNotLogged + '"]/td/div/form/input[@class="approve submit"]')
        sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])

        #assert comment is present on the page 
        print 'Returning to the main page...'
        sel.click('link=View Main Site')
        sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])
        print 'Logging out...'
        loginlogout.LogOut(self,sel)
        print "Clicking on the first video on the page..."
        sel.click(self.themeToTest.firstVideoOnPage)
        sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])
        print 'Asserting the comment is on the page...'
        self.failUnless(sel.is_text_present(self.commentNotLogged))

        #-----
        #-----
        #-----        

        print "Generating and posting a new comment..."
        #post new comment and assert if notification that comment was sent to moderators presents on the page
        self.comment = generateComment()
        sel.type(self.themeToTest.commentEditField, self.comment)
        sel.type( self.themeToTest.posterNameEditField, "TestPoster")
        sel.click(self.themeToTest.postCommentButton)
        print "Waiting for notification that comment was sent to moderators..."
        if (not WaitUntilTextOnTheScreen(sel, gCommentModerationText, gTimeOut)):
            print "ERROR: Notification that comment was sent to moderators is not on the page"
            self.failIf(True)
        else:
            print 'Text "', gCommentModerationText, '" is on the page'

        #login as admin and remove the comment that was sent in previous step
        print 'Logging in as Admin'
        loginlogout.LogInAsAdmin(self,sel)
        print 'Opening Admin|Comments and removing previously posted comment...'
#        sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])
        sel.click("link=View Admin")
        sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])
        sel.click("link=Comments")
        sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])
        sel.click('//tr[td="' + self.comment + '"]/td/div/form/input[@class="remove submit"]')

        #assert comment is not present on the page
        print 'Going back on main page...'
        sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])
        sel.click('link=View Main Site')
        sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])
        print 'Logging out...'
        sel.click('link=Logout seleniumTestAdmin')
        sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])
        print "Clicking on the first video on the page..."
        sel.click(self.themeToTest.firstVideoOnPage)
        sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])
        print 'Asserting the comment is not on the page...'
        self.failIf(sel.is_text_present(self.comment))
        print 'Going back on main page...'
        sel.open('/')
        
    #tests if comment can be posted by logged in user
    def LoggedAsUser_CommentPosted(self):
        #login as an User
        #print 'Executing LoggedAsUser_CommentPosted()'
        sel = self.selenium
        print 'Logging in as User...'
        loginlogout.LogInAsUser(self,sel)
#        LogIn(sel, gUserLogin, gUserPassword)
        #click on the first video and post a comment
        print "Clicking on the first video on the page..."
        sel.click(self.themeToTest.firstVideoOnPage)
        sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])
        print 'Generating and posting a new comment...'
        self.commentUser = generateComment()
        sel.type(self.themeToTest.commentEditField, self.commentUser)
        sel.click(self.themeToTest.postCommentButton)
        sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])
        #assert comment presents on the page
        print 'Asserting the comment is on the page...'
        self.failUnless(sel.is_text_present(self.commentUser))
        print 'Going back on main page...'
        sel.open("/")
        print 'Logging out...'
        loginlogout.LogOut(self,sel)

    #tests application when user is logged in as an user and all comments have to be moderated by admin
    def LoggedAsUser_ModerationRequired(self):
        #login as a User
        #print 'Log--> Executing LoggedAsUser_ModerationRequired()'
        sel = self.selenium
        print 'Logging in as User...'
        loginlogout.LogInAsUser(self,sel)
 #       LogIn(sel, gUserLogin, gUserPassword)
        #click on the first video and post a comment
        print 'Clicking on the first video on the page...'     
        sel.click(self.themeToTest.firstVideoOnPage)
        sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])
        print 'Generating and posting new comment...'
        self.commentUser = generateComment()
        sel.type(self.themeToTest.commentEditField, self.commentUser)
        sel.click(self.themeToTest.postCommentButton)
        #wait until notification that comment was sent to moderators presents on the page
        print "Waiting for notification that comment was sent to moderators..."
        if (not WaitUntilTextOnTheScreen(sel, gCommentModerationText, gTimeOut)):
            print "ERROR: Notification that comment was sent to moderators is not displayed on the page"
            self.failIf(True)
        else:
            print 'Text "', gCommentModerationText, '" is on the page'

        #logout
        print "Logging out..."
        loginlogout.LogOut(self,sel)
        #login as admin and approve the comment that was sent in previous step
        print 'Logging in as Admin...'
        loginlogout.LogInAsAdmin(self,sel)
        print 'Opening settings and approving a previously posted comment...'
        sel.click("link=View Admin")
        sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])
        sel.click("link=Comments")
        sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])
        sel.click('//tr[td="' + self.commentUser + '"]/td/div/form/input[@class="approve submit"]')
        sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])

        #login as a user and assert that the comment is present on the page
        print "Going back on the main page..."
        sel.click('link=View Main Site')
        sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])
        print "Logging out..."
        loginlogout.LogOut(self,sel)
        print 'Logging in as User...'
        loginlogout.LogInAsUser(self,sel)
#        LogIn(sel, gUserLogin, gUserPassword)
        print 'Clicking on the first video on the page...' 
        sel.click(self.themeToTest.firstVideoOnPage)
        sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])
        print 'Asserting the comment is on the page...'
        self.failUnless(sel.is_text_present(self.commentUser))

        #-----
        #-----
        #-----

        #generate and post new comment
        print 'Generating and posting a new comment...'
        self.comment = generateComment()
        sel.type(self.themeToTest.commentEditField, self.comment)
        sel.click(self.themeToTest.postCommentButton)
        #wait until notification that comment was sent to moderators presents on the page
        print "Waiting for notification that comment was sent to moderators..."
        if (not WaitUntilTextOnTheScreen(sel, gCommentModerationText, gTimeOut)):
            print "ERROR: Notification that comment was sent to moderators is not on the page"
            self.failIf(True)
        else:
            print 'Text "', gCommentModerationText, '" is on the page'

        #logout
        print "Logging out..."
        loginlogout.LogOut(self,sel)
        #login as admin and remove the comment that was sent in previous step
        print 'Logging in as Admin...'
        loginlogout.LogInAsAdmin(self,sel)
        print 'Opening Admin|Comments and removing a previously posted comment...'
        sel.click("link=View Admin")
        sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])
        sel.click("link=Comments")
        sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])
        sel.click('//tr[td="' + self.comment + '"]/td/div/form/input[@class="remove submit"]')

        #assert comment does not present on the page
        print "Going back on the main page..."
        sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])
        sel.click('link=View Main Site')
        sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])
        print "Logging out"
        loginlogout.LogOut(self,sel)
        print 'Clicking on the first video on the page...' 
        sel.click(self.themeToTest.firstVideoOnPage)
        sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])
        print 'Asserting the comment is on the page...'
        self.failIf(sel.is_text_present(self.comment))
        sel.open('/')
        
    #tests if comment can be posted by the Admin
    def LoggedAsAdmin_CommentPosted(self):
#        print "Executing LoggedAsAdmin_CommentPosted()"                        
        sel = self.selenium
        print "Logging in as admin..."
        loginlogout.LogInAsAdmin(self,sel)
#        LogIn(sel, testvars.MCTestVariables["AdminLogin"], testvars.MCTestVariables["AdminPassword"])
        print "Clicking first video on the page..." 
        sel.click(self.themeToTest.firstVideoOnPage)
        sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])
        print "Generating and posting new comment..."
        self.comment = generateComment()
        sel.type(self.themeToTest.commentEditField, self.comment)
        sel.click(self.themeToTest.postCommentButtonAdmin)
        sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])
        print 'Asserting comment is on the page...'
        self.failUnless(sel.is_text_present(self.comment))

        #deleting posts
        if self.bCommentNotLogged:
            print 'Deleting comment posted by unlogged user...'
            sel.click(self.themeToTest.deleteCommentButtonPart1 + self.commentNotLogged +self.themeToTest.deleteCommentButtonPart2)
            sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])
            self.failIf(sel.is_text_present(self.commentNotLogged))
        print 'Deleting comment posted by logged user...'
        sel.click(self.themeToTest.deleteCommentButtonPart1 + self.commentUser +self.themeToTest.deleteCommentButtonPart2)
        sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])
        self.failIf(sel.is_text_present(self.commentUser))
        print 'Deleting comment posted by Admin...'
        sel.click(self.themeToTest.deleteCommentButtonPart1 + self.comment +self.themeToTest.deleteCommentButtonPart2)
        sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])
        self.failIf(sel.is_text_present(self.comment))
        
        print 'Going back to the main page...'
        sel.open("/")
        print 'Logging out...'
        loginlogout.LogOut(self,sel)
        
    #dummy function has to be redefined in inherited classes
    def SetParams(self):
        return False

    #changes site settings and sets up theme if it's necessary
    def ChangeSiteSettings(self):
        sel = self.selenium
        if (not LogIn(sel, testvars.MCTestVariables["AdminLogin"], testvars.MCTestVariables["AdminPassword"])):
            print "Login window did not pop up"
            self.failIf(True)
#        if self.bSetTheme:
#            sel.open(self.themeToTest.themePath)
        sel.open(testvars.MCTestVariables["SettingsPage"])
        sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])
        if (not ChangeAdditionalSettings(sel, 0, 0, 0, self.bHoldForModeration, self.bRequireLogin)):
            print 'ERROR: Additional Settings could not be changed'
            self.failIf(True)
        sel.click('submit_settings')
        sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])
        # ----- Added to make up for blank page bug
        sel.open(testvars.MCTestVariables["SettingsPage"])
        sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])
        # --------------------
        sel.click('link=View Main Site')
        sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])
        sel.click('link=Logout seleniumTestAdmin')
        sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])

    #performs tests
    def test_case(self):
        sel=self.selenium
        self.SetParams()
        self.ChangeSiteSettings()
        for item in gAllThemes:
            print ""
            if item==gListTheme:
                theme="LIST"
                themeNo=1
            elif item==gScrollingTheme:
                theme="SCROLLING"
                themeNo=2
            elif item==gCategoryTheme:
                theme="CATEGORY"
                themeNo=3
            elif item==gBlueTheme:
                theme="BLUE"
                themeNo=4
            else:
                theme="Unknown"
                themeNo=1
            print "Running test case in theme: "+theme
            self.themeToTest=item
            loginlogout.LogInAsAdmin(self,sel)
            sitesettings.ChangeTheme(self,sel,themeNo)
            loginlogout.LogOut(self,sel)
            if self.NotLoggetTest:
                print "Starting test for UNLOGGED USER"
                self.NotLoggetTest()
            if self.UserTest:
                print "Starting test for LOGGED USER"
                self.UserTest()
            if self.AdminTest:
                print "Starting test for ADMIN"
                self.AdminTest()


    def logTestDescription(self):
        print "Starting test"

    #//li[contains(.,'Vasya')]/div/form[button="delete"]/button                


#tests AUT without 'Hold comments for moderation' and 'Require Login' with List theme
class testcase_Comments_NoModeration_NoLogin(testcase_BaseComments):

    def logTestDescription(self):
        print ""
        print "Executing testcase_Comments_NoModeration_NoLogin"            
    
    def SetParams(self):
        self.bHoldForModeration = 0
        self.bRequireLogin = 0
        self.NotLoggetTest = self.NotLogged_CommentPosted
        self.UserTest = self.LoggedAsUser_CommentPosted
        self.AdminTest = self.LoggedAsAdmin_CommentPosted

#tests AUT without 'Hold comments for moderation' and with 'Require Login' with List theme
class testcase_Comments_NoModeration_LoginRequired(testcase_BaseComments):

    def logTestDescription(self):
        print ""
        print "Executing testcase_Comments_NoModeration_LoginRequired"                
    
    def SetParams(self):
        self.bHoldForModeration = 0
        self.bRequireLogin = 1
        self.NotLoggetTest = self.NotLogged_NotPossibleToPost
        self.UserTest = self.LoggedAsUser_CommentPosted
        self.AdminTest = self.LoggedAsAdmin_CommentPosted

#tests AUT with 'Hold comments for moderation' and without 'Require Login' with List theme
class testcase_Comments_ModerationRequired_NoLogin(testcase_BaseComments):

    def logTestDescription(self):
        print ""
        print "Executing testcase_Comments_ModerationRequired_NoLogin"  
    
    def SetParams(self):
        self.bHoldForModeration = 1
        self.bRequireLogin = 0
        self.NotLoggetTest = self.NotLogged_ModerationRequired
        self.UserTest = self.LoggedAsUser_ModerationRequired
        self.AdminTest = self.LoggedAsAdmin_CommentPosted

#tests AUT with 'Hold comments for moderation' and 'Require Login' with List theme
class testcase_Comments_ModerationRequired_LoginRequired(testcase_BaseComments):

    def logTestDescription(self):
        print ""
        print "Log--> Executing testcase_Comments_ModerationRequired_LoginRequired"                        
    
    def SetParams(self):
        self.bHoldForModeration = 1
        self.bRequireLogin = 1
        self.NotLoggetTest = self.NotLogged_NotPossibleToPost
        self.UserTest = self.LoggedAsUser_ModerationRequired
        self.AdminTest = self.LoggedAsAdmin_CommentPosted

        
    
#if __name__ == "__main__":
#    unittest.main()
