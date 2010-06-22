#=======================================================================
#
#                             BULK EDIT TESTS
#
#=======================================================================
#
# Includes the following test cases:
#     1. testcase_BulkEdit_EditAndDelete
#     2. testcase_BulkEdit_FeatureAndUnfeature
#     3. testcase_BulkEdit_EditSingleVideo
#     4. testcase_BulkEdit_DeleteSingleVideo
#     5. testcase_BulkEdit_UnapproveCurrent
#     6. testcase_BulkEdit_UnapproveFeatured

from selenium import selenium
import unittest, time, re, loginlogout, sitesettings, categories, testvars, random
import sys

global initialCategories
initialCategories = [""]
# ----------------------------------------------------------------------

#------ Variables ---------

global gLoginButtonInLoginPopUpWindow
gLoginButtonInLoginPopUpWindow = "//input[@value='Log In']"

global gViewAdmin
gViewAdmin = 'link=View Admin'

global gLinkLogin
gLinkLogin = 'link=Login'

global gBulkEditOnAdminPage
gBulkEditOnAdminPage = "//div[@id='admin_subnav']/ul/li[3]/a/span"

global gCategoriesOnAdminPage
gCategoriesOnAdminPage = "XPath=id('admin_subnav')/ul/li[4]/a/span"

global gReviewQueueOnAdminPage
gReviewQueueOnAdminPage = "XPath=id('admin_subnav')/ul/li[1]/a/span"

global gSearchEditBoxOnBulkEditPage
gSearchEditBoxOnBulkEditPage = "XPath=id('labels')/form[1]/input"

global gSearchButtonOnBulkEditPage
gSearchButtonOnBulkEditPage = "//button[span='Search']"

global gSubmitVideoButtonOnAdminPage
gSubmitVideoButtonOnAdminPage = "XPath=id('admin_subnav')/ul/li[5]/a/span"

global gSubmitButtonOnSubmitVideoPage
gSubmitButtonOnSubmitVideoPage = "XPath=id('submit_video')/table/tbody/tr[2]/td/input"

global gSubmitButtonOnSubmitVideoPage2
gSubmitButtonOnSubmitVideoPage2 = "XPath=id('submit_video')/table/tbody/tr[3]/td/input"

global gUrlEditFieldOnSubmitVideoPage
gUrlEditFieldOnSubmitVideoPage = "XPath=id('id_url')"

global gCategoryNameEditField
gCategoryNameEditField = "XPath=id('id_name')"

global gCategorySlugEditField
gCategorySlugEditField = "XPath=id('id_slug')"

global gCategoryName
gCategoryName = "BulkEditTestCategory"

global gAddCategoryButton
gAddCategoryButton = "XPath=id('label_sidebar')/button"

global gAddCategoryButtonOnCategoryPage
gAddCategoryButtonOnCategoryPage = "XPath=id('content')/a/span"

global gCloseAddCategoryWindowButton
gCloseAddCategoryWindowButton = "XPath=id('label_sidebar')/div[1]"

global gVideo1Url
gVideo1Url = 'http://www.youtube.com/watch?v=be-BoM-WokY'

global gVideo2Url
gVideo2Url = 'http://www.youtube.com/watch?v=-5OmdTaPzd8'

global gVideosLabel
gVideosLabel = "Judo"

global gToggleAll
gToggleAll = "toggle_all"

global gApplyButton
gApplyButton = "//button[@type='button']"
#----
global gActionSelector
gActionSelector = "bulk_action_selector"

global gDeleteOption
gDeleteOption = "label=Delete"

global gEditOption
gEditOption = "label=Edit"

global gFeatureOption
gFeatureOption = "label=Feature"

global gUnfeatureOption
gUnfeatureOption = "label=Unfeature"

global gUnapproveOption
gUnapproveOption = "label=Unapprove"
#----
global gFilterSelector
gFilterSelector = "filter"

global gCurrentFilterOption
gCurrentFilterOption = "label=Current Videos"

global gFeaturedFilterOption
gFeaturedFilterOption = "label=Featured Videos"
#----
global gEditTitle
gEditTitle = "BulkEditTestTitleJudo"

global gEditDate
gEditDate = "1666-06-11 00:00:00"

global gEditDescription
gEditDescription = "BulkEditTestDescription"

global gEditTag
gEditTag = "bulkedittesttag"

#---
global gEditCategoryXPath
gEditCategoryXPath = "//li/label[span='BulkEditTestCategory']/input[@name='form-2-categories']"

global gEditUserXPath
gEditUserXPath = "//li/label[span='BulkEditTestUser']/input[@name='form-2-authors']"

global gEditPageTitleEditField
gEditPageTitleEditField = "XPath=id('id_form-2-name')"

global gEditPageDateEditField
gEditPageDateEditField = "XPath=id('id_form-2-when_published')"

global gEditPageDescriptionEditField
gEditPageDescriptionEditField = "XPath=id('id_form-2-description')"

global gEditPageTagsEditField
gEditPageTagsEditField = "XPath=id('id_form-2-tags')"
#---
global gEditCategoryXPathSingleVideo
gEditCategoryXPathSingleVideo = "//li/label[span='BulkEditTestCategory']/input[@name='form-0-categories']"

global gEditUserXPathSingleVideo
gEditUserXPathSingleVideo = "//li/label[span='BulkEditTestUser']/input[@name='form-0-authors']"

global gEditPageTitleEditFieldSingleVideo
gEditPageTitleEditFieldSingleVideo = "XPath=id('id_form-0-name')"

global gEditPageDateEditFieldSingleVideo
gEditPageDateEditFieldSingleVideo = "XPath=id('id_form-0-when_published')"

global gEditPageDescriptionEditFieldSingleVideo
gEditPageDescriptionEditFieldSingleVideo = "XPath=id('id_form-0-description')"

global gEditPageTagsEditFieldSingleVideo
gEditPageTagsEditFieldSingleVideo = "XPath=id('id_form-0-tags')"
#---

global gVideosSectionOnAdminPage
gVideosSectionOnAdminPage = "XPath=id('admin_nav')/li[1]/a"

global gUsersSectionOnAdminPage
gUsersSectionOnAdminPage = "XPath=id('admin_nav')/li[3]/a"

#---

global gAddUserButtonOnUsersPage
gAddUserButtonOnUsersPage = "XPath=id('label_sidebar')/a/span"

global gAddUserButtonInAddUserWindow
gAddUserButtonInAddUserWindow = "XPath=id('add_user')/form/button"

global gUserNameEditBoxInAddUserWindow
gUserNameEditBoxInAddUserWindow = "XPath=id('id_username')"

global gUserRadioButtonInAddUserWindow
gUserRadioButtonInAddUserWindow = "XPath=id('id_role_0')"

global gPasswordEditBoxInAddUserWindow
gPasswordEditBoxInAddUserWindow = "XPath=id('id_password_f')"

global gConfirmPasswordEditBoxInAddUserWindow
gConfirmPasswordEditBoxInAddUserWindow = "XPath=id('id_password_f2')"

global gBulkEditUserName
gBulkEditUserName = "BulkEditTestUser"

global gBulkEditUserPassword
gBulkEditUserPassword = "password"

global gSaveChangesButtonInEditWindow
gSaveChangesButtonInEditWindow = "XPath=id('massedit')/button"

global gSaveChangesButtonInEditWindowSingleVideo
gSaveChangesButtonInEditWindowSingleVideo = "XPath=id('labels')/form[2]/table/tbody/tr[1]/td[1]/div/button"

global gLinkToViewFirstVideo
gLinkToViewFirstVideo = "XPath=id('labels')/form[2]/table/tbody/tr[1]/td[2]/div/a[3]"

global gLinkToViewSecondVideo
gLinkToViewSecondVideo = "XPath=id('labels')/form[2]/table/tbody/tr[2]/td[2]/div/a[3]"

global gTitlePathOnViewVideoPage
gTitlePathOnViewVideoPage = "XPath=id('main')/div[1]/div/div/div[1]/h2[contains(.,'"

global gUserPathOnViewVideoPage
gUserPathOnViewVideoPage = "XPath=id('main')/div[3]/div/div[1]/a[contains(.,'"

global gDescriptionPathOnViewVideoPage
gDescriptionPathOnViewVideoPage = "XPath=id('main')/div[6]/div[1]/div[contains(.,'"

global gCategoryPathOnViewVideoPage
gCategoryPathOnViewVideoPage = "XPath=id('tags')/ul/li[1]/div/div[1]/div/ul/li/a[contains(.,'"

global gTagsPathOnViewVideoPage
gTagsPathOnViewVideoPage = "XPath=id('tags')/ul/li[2]/div/div[1]/div/ul/li/a[contains(.,'"

global gFirstVideoTitlePathOnBulkEditPage
gFirstVideoTitlePathOnBulkEditPage = "XPath=id('labels')/form[2]/table/tbody/tr[1]/td[2]/span[contains(.,'"

global gSecondVideoTitlePathOnBulkEditPage
gSecondVideoTitlePathOnBulkEditPage = "XPath=id('labels')/form[2]/table/tbody/tr[1]/td[2]/span[contains(.,'"

global gFirstVideoEditLink
gFirstVideoEditLink = "XPath=id('labels')/form[2]/table/tbody/tr[1]/td[2]/div/a[1]"

global gFirstVideoDeleteLink
gFirstVideoDeleteLink = "XPath=id('labels')/form[2]/table/tbody/tr[1]/td[2]/div/a[2]"

global gClearQueueButtonOnReviewQueuePage
gClearQueueButtonOnReviewQueuePage = "XPath=id('content')/a[3]/span"

global gYesClearQueueButton
gYesClearQueueButton = "XPath=id('content')/form/button"

#-----
global gVideoPathOnBulkEditPage
gVideoPathOnBulkEditPage = "XPath=id('labels')/form[2]/table/tbody/tr/td[2]/span[contains(.,'"

global gFirstVideoOriginalName
gFirstVideoOriginalName = "best of judo"

global gSecondVideoOriginalName
gSecondVideoOriginalName = "legends of judo"
#-----


global gSeleniumServerPort
gSeleniumServerPort = 4444

global gTimeOut
gTimeOut = 20


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

#function which performs login with given Login and Password
def LogIn(sel, Login, Password):
    sel.open("/")
    sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])
    sel.click(gLinkLogin)
    if (not WaitUntilElementOnTheScreen(sel, gLoginButtonInLoginPopUpWindow, gTimeOut)):
        return False
    sel.window_maximize()
    sel.type("id_username", Login)
    sel.type("id_password", "")
    sel.type("id_password", Password)
    sel.click(gLoginButtonInLoginPopUpWindow)
    sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])
    return True
    

#as setUp() and tearDown() are the same for all test cases we have a good reason to inlude them into one base class
class testcase_BaseTestCase(unittest.TestCase):
    
    def setUp(self):
        self.verificationErrors = []
        self.selenium = selenium("localhost", gSeleniumServerPort, testvars.MCTestVariables["Browser"], testvars.MCTestVariables["TestSite"])
        self.selenium.start()

    def test_case(self):
        return 1

    def tearDown(self):
        self.selenium.stop()
        self.assertEqual([], self.verificationErrors)

#class which contains some functions that are going to be used only for testing 'Bulk Edit'
class testcase_BaseClassForBulkEdit(testcase_BaseTestCase):    

    #Logins as Admin and goes to View Admin page
    def LoginAsAdminSetThemeGoToViewAdmin(self):
        sel = self.selenium
        LogIn(sel, testvars.MCTestVariables["AdminLogin"], testvars.MCTestVariables["AdminPassword"])
        sel.open(testvars.MCTestVariables["ListThemeLink"])
        sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])
        sel.click(gVideosSectionOnAdminPage)
        sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])

    #Submits video with given URL, works if video was submitted before
    def SubmitVideo(self, in_VideoUrl):
        sel = self.selenium
        sel.click(gSubmitVideoButtonOnAdminPage)
        if (not WaitUntilElementOnTheScreen(sel, gSubmitButtonOnSubmitVideoPage, gTimeOut)):
             return False
        sel.type(gUrlEditFieldOnSubmitVideoPage, in_VideoUrl)
        sel.click(gSubmitButtonOnSubmitVideoPage)

        time.sleep(5)
        if sel.is_element_present(gSubmitButtonOnSubmitVideoPage2):
            sel.click(gSubmitButtonOnSubmitVideoPage2)
            sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])
        else:
            WaitUntilElementOnTheScreen(sel, gViewAdmin, gTimeOut)

        sel.click(gViewAdmin)
        sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])

    #Searches videos with 'gVideosLabel' and deletes them
    def DeleteVideos(self):
        sel = self.selenium
        sel.click(gBulkEditOnAdminPage)
        sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])

        sel.type(gSearchEditBoxOnBulkEditPage, gVideosLabel)
        sel.click(gSearchButtonOnBulkEditPage)
        sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])

        sel.click(gToggleAll)
        sel.select(gActionSelector, gDeleteOption)
        sel.click(gApplyButton)
        sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])

    #Adds new category with name defined in 'gCategoryName', works if category was added before
    def AddCategory(self):
        sel = self.selenium
        sel.click(gCategoriesOnAdminPage)
        sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])

        sel.click(gAddCategoryButtonOnCategoryPage)
        WaitUntilElementOnTheScreen(sel, gAddCategoryButton, gTimeOut)

        time.sleep(2)

        sel.type(gCategoryNameEditField, gCategoryName)

        sel.type(gCategorySlugEditField, gCategoryName)
        sel.click(gAddCategoryButton)

        time.sleep(5)
        if sel.is_element_present(gCategoryNameEditField):
            sel.click(gCloseAddCategoryWindowButton)

    #Adds new user with name defined in 'gBulkEditUserName', works if user was added before
    def AddUser(self):
        
        sel = self.selenium

        sel.click(gUsersSectionOnAdminPage)
        sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])

        sel.click(gAddUserButtonOnUsersPage)
        WaitUntilElementOnTheScreen(sel, gUserRadioButtonInAddUserWindow, gTimeOut)

        sel.type(gUserNameEditBoxInAddUserWindow, gBulkEditUserName)
        sel.click(gUserRadioButtonInAddUserWindow)
        sel.type(gPasswordEditBoxInAddUserWindow, gBulkEditUserPassword)
        sel.type(gConfirmPasswordEditBoxInAddUserWindow, gBulkEditUserPassword)

        sel.click(gAddUserButtonInAddUserWindow)
        sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])

        sel.click(gVideosSectionOnAdminPage)
        sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])

    #Checks if changes that were made during editing of bulk of videos were saved and they are correct 
    def checkChanges(self, in_ViewLink, in_CheckTags):
        
        sel = self.selenium
        sel.click(in_ViewLink)
        sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])

        #XPath=id('main')/div[1]/div/div/div[1]/h2[contains(.,'BulkEditTestTitleJudo')]

        if (not sel.is_element_present(gTitlePathOnViewVideoPage + gEditTitle + "')]") ):
            print "ERROR: Title was not fount or it is incorrect"
            self.failUnless(False)

        if (not sel.is_element_present(gUserPathOnViewVideoPage + gBulkEditUserName + "')]") ):
            print "ERROR: User's Name was not fount or it is incorrect"
            self.failUnless(False)

        if (not sel.is_element_present(gDescriptionPathOnViewVideoPage + gEditDescription + "')]") ):
            print "ERROR: Description was not fount or it is incorrect"
            self.failUnless(False)

        if (not sel.is_element_present(gCategoryPathOnViewVideoPage + gCategoryName + "')]") ):
            print "ERROR: Category was not fount or it is incorrect"
            self.failUnless(False)

        if in_CheckTags:
            if (not sel.is_element_present(gTagsPathOnViewVideoPage + gEditTag + "')]") ):
                print "ERROR: Tag was not fount or it is incorrect"
                self.failUnless(False)
        
        return 1

    def LoginDeleteVideosAddVideos(self):
        print "Loging in as admin and going to the 'View Admin' page..."
        self.LoginAsAdminSetThemeGoToViewAdmin()
        print "Deleting videos..."
        self.DeleteVideos()
        print "Submitting the first video..."
        self.SubmitVideo(gVideo1Url)
        print "Submitting the second video..."
        self.SubmitVideo(gVideo2Url)
        
    def LoginDeleteVideosAddUserAddCategoryAddVideos(self):
        print "Loging in as admin and going to 'View Admin' page..."
        self.LoginAsAdminSetThemeGoToViewAdmin()
        print "Deleting videos..."
        self.DeleteVideos()
        print "Adding a user..."
        self.AddUser()
        print "Adding a category..."
        self.AddCategory()
        print "Submitting the first video..."
        self.SubmitVideo(gVideo1Url)
        print "Submitting the second video..."
        self.SubmitVideo(gVideo2Url)
        
            
            

#Tests AUT for edititng and deleting videos by 'Bulk Edit'
class testcase_BulkEdit_EditAndDelete(testcase_BaseClassForBulkEdit):
        
    #The body of test case
    def test_case(self):

        print ""
        print "Starting 'testcase_BulkEdit_EditAndDelete' test case..."
        sel = self.selenium
        self.LoginDeleteVideosAddUserAddCategoryAddVideos()

        print "Opening 'Bulk Edit' page..."
        sel.click(gBulkEditOnAdminPage)
        sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])

        print "Searching all videos with 'gVideosLabel'..."
        sel.type(gSearchEditBoxOnBulkEditPage, gVideosLabel)
        sel.click(gSearchButtonOnBulkEditPage)
        sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])

        print "Checking all found videos..."
        sel.click(gToggleAll)
        print "Choosing 'Edit' option and clicking 'Apply' button..."
        sel.select(gActionSelector, gEditOption)
        sel.click(gApplyButton)

        print "Editing selected videos..."
        WaitUntilElementOnTheScreen(sel, gEditCategoryXPath, gTimeOut)
        sel.type(gEditPageTitleEditField, gEditTitle)
        sel.type(gEditPageDateEditField, gEditDate)
        sel.type(gEditPageDescriptionEditField, gEditDescription)
        sel.type(gEditPageTagsEditField, gEditTag)

        sel.check(gEditCategoryXPath)
        sel.check(gEditUserXPath)

        print "Saving changes..."        
        sel.click(gSaveChangesButtonInEditWindow)

        sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])

        print "Checking changes in the first video..."        
        self.checkChanges(gLinkToViewFirstVideo, True)

        sel.click(gViewAdmin)
        sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])

        sel.click(gBulkEditOnAdminPage)
        sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])

        sel.type(gSearchEditBoxOnBulkEditPage, gVideosLabel)
        sel.click(gSearchButtonOnBulkEditPage)
        sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])        

        print "Checking changes in the second video..."                
        self.checkChanges(gLinkToViewSecondVideo, True)
        
        # Delete

        print "Deleting videos..."                
        sel.click(gViewAdmin)
        sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])

        self.DeleteVideos()

        print "Verifying if videos have been deleted..."                
        sel.click(gBulkEditOnAdminPage)
        sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])

        sel.type(gSearchEditBoxOnBulkEditPage, gVideosLabel)
        sel.click(gSearchButtonOnBulkEditPage)
        sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])

        if (sel.is_element_present(gFirstVideoTitlePathOnBulkEditPage + gEditTitle + "')]") ):
            print "ERROR: Video was not deleted"
            self.failUnless(False)

        if (sel.is_element_present(gSecondVideoTitlePathOnBulkEditPage + gEditTitle + "')]") ):
            print "ERROR: Video was not deleted"
            self.failUnless(False)                            

#Tests AUT for featuring and unfeaturing videos by 'Bulk Edit'
class testcase_BulkEdit_FeatureAndUnfeature(testcase_BaseClassForBulkEdit):

     #The body of test case     
     def test_case(self):
         
        print ""
        print "Starting 'testcase_BulkEdit_FeatureAndUnfeature' test case..."
        sel = self.selenium
        self.LoginDeleteVideosAddVideos()

        print "Opening 'Bulk Edit' page..."        
        sel.click(gBulkEditOnAdminPage)
        sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])

        print "Searching all videos with 'gVideosLabel'..."
        sel.type(gSearchEditBoxOnBulkEditPage, gVideosLabel)
        sel.click(gSearchButtonOnBulkEditPage)
        sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])

        print "Featuring all found videos..."
        sel.click(gToggleAll)
        sel.select(gActionSelector, gFeatureOption)
        sel.click(gApplyButton)
        sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])

        print "Verifying if videos have been featured..."
        sel.select(gFilterSelector, gFeaturedFilterOption)
        sel.click(gSearchButtonOnBulkEditPage)
        sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])

        if (not sel.is_element_present(gVideoPathOnBulkEditPage + gFirstVideoOriginalName + "')]") ):
            print "ERROR: Video was not featured"
            self.failUnless(False)

        if (not sel.is_element_present(gVideoPathOnBulkEditPage + gSecondVideoOriginalName + "')]") ):
            print "ERROR: Video was not featured"
            self.failUnless(False)

        #---
        print "Unfeaturing videos..."
        sel.click(gToggleAll)
        sel.select(gActionSelector, gUnfeatureOption)
        sel.click(gApplyButton)
        sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])        

        print "Verifying if videos have been unfeatured..."
        sel.select(gFilterSelector, gFeaturedFilterOption)
        sel.click(gSearchButtonOnBulkEditPage)
        sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])

        if (sel.is_element_present(gVideoPathOnBulkEditPage + gFirstVideoOriginalName + "')]") ):
            print "ERROR: Video was not unfeatured"
            self.failUnless(False)

        if (sel.is_element_present(gVideoPathOnBulkEditPage + gSecondVideoOriginalName + "')]") ):
            print "ERROR: Video was not unfeatured"
            self.failUnless(False)        


#Tests AUT for editing a single video
class testcase_BulkEdit_EditSingleVideo(testcase_BaseClassForBulkEdit):
    #The body of test case     
     def test_case(self):
         
        print ""
        print "Starting 'testcase_BulkEdit_EditSingleVideo' test case..."
        sel = self.selenium
        self.LoginDeleteVideosAddUserAddCategoryAddVideos()

        print "Opening 'Bulk Edit' page..."        
        sel.click(gBulkEditOnAdminPage)
        sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])

        print "Searching all videos with 'gVideosLabel'..."
        sel.type(gSearchEditBoxOnBulkEditPage, gVideosLabel)
        sel.click(gSearchButtonOnBulkEditPage)
        sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])        

        print "Editing the first video..."
        sel.click(gFirstVideoEditLink)

        WaitUntilElementOnTheScreen(sel, gEditCategoryXPathSingleVideo, gTimeOut)
        sel.type(gEditPageTitleEditFieldSingleVideo, gEditTitle)
        sel.type(gEditPageDateEditFieldSingleVideo, gEditDate)
        sel.type(gEditPageDescriptionEditFieldSingleVideo, gEditDescription)
        sel.type(gEditPageTagsEditFieldSingleVideo, gEditTag)

        sel.check(gEditCategoryXPathSingleVideo)
        sel.check(gEditUserXPathSingleVideo)

        print "Saving changes..."        
        sel.click(gSaveChangesButtonInEditWindow)
        sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])

        print "Checking changes in the first video..."        
        self.checkChanges(gLinkToViewFirstVideo, False)

        time.sleep(10)        
                
#Tests AUT for deleting a single video
class testcase_BulkEdit_DeleteSingleVideo(testcase_BaseClassForBulkEdit):
    
    def test_case(self):
        print ""
        print "Starting 'testcase_BulkEdit_DeleteSingleVideo' test case..."
        sel = self.selenium
        self.LoginDeleteVideosAddVideos()

        print "Opening 'Bulk Edit' page..."        
        sel.click(gBulkEditOnAdminPage)
        sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])

        print "Searching all videos with 'gVideosLabel'..."
        sel.type(gSearchEditBoxOnBulkEditPage, gVideosLabel)
        sel.click(gSearchButtonOnBulkEditPage)
        sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])

        print "Deleting the first video..."
        sel.click(gFirstVideoDeleteLink)
        sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])

        print "Checking if video has been deleted..."
        if (sel.is_text_present(gFirstVideoOriginalName)):
            print "ERROR: Video has not been deleted"
            self.failUnless(False)


#Tests AUT for unapproving current videos
class testcase_BulkEdit_UnapproveCurrent(testcase_BaseClassForBulkEdit):

    #dummy function
    def FeaturingVideos(self):
        return 1

    def SearchingVideos(self):
        sel = self.selenium
        print "Searching all videos with 'gVideosLabel'..."
        sel.type(gSearchEditBoxOnBulkEditPage, gVideosLabel)
        sel.click(gSearchButtonOnBulkEditPage)
        sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])        
        
    def test_case(self):
        print ""
        sel = self.selenium
        self.LoginDeleteVideosAddVideos()

        #it's dummy function
        self.FeaturingVideos()        

        print "Opening 'Review Queue' page..."        
        sel.click(gReviewQueueOnAdminPage)
        sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])

        print "Clearing the queue"
        sel.click(gClearQueueButtonOnReviewQueuePage)
        sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])

        sel.click(gYesClearQueueButton)
        sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])        

        print "Opening 'Bulk Edit' page..."        
        sel.click(gBulkEditOnAdminPage)
        sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])

        #Searches videos    
        self.SearchingVideos()

        print "Unapproving all found videos..."
        sel.click(gToggleAll)
        sel.select(gActionSelector, gUnapproveOption)
        sel.click(gApplyButton)
        sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])

        print "Opening 'Review Queue' page..."        
        sel.click(gReviewQueueOnAdminPage)
        sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])
    
        print "Checking if video in the 'Review Queue'..."
        if (not sel.is_text_present(gFirstVideoOriginalName)):
            print "ERROR: Video is not in the list"
            self.failUnless(False)        

        print "Checking if video in the 'Review Queue'..."
        if (not sel.is_text_present(gSecondVideoOriginalName)):
            print "ERROR: Video is not in the list"
            self.failUnless(False)

#Tests AUT for unapproving featured videos
class testcase_BulkEdit_UnapproveFeatured(testcase_BulkEdit_UnapproveCurrent):

    #This function searches videos
    def SearchingVideos(self):
        sel = self.selenium
        print "Searching all featured videos with 'gVideosLabel'..."
        sel.select(gFilterSelector, gFeaturedFilterOption)
        sel.type(gSearchEditBoxOnBulkEditPage, gVideosLabel)
        sel.click(gSearchButtonOnBulkEditPage)
        sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])            

    #This function features videos
    def FeaturingVideos(self):

        sel = self.selenium        

        print "Opening 'Bulk Edit' page..."        
        sel.click(gBulkEditOnAdminPage)
        sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])        
        
        print "Searching all videos with 'gVideosLabel'..."
        sel.type(gSearchEditBoxOnBulkEditPage, gVideosLabel)
        sel.click(gSearchButtonOnBulkEditPage)
        sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])

        print "Featuring all found videos..."
        sel.click(gToggleAll)
        sel.select(gActionSelector, gFeatureOption)
        sel.click(gApplyButton)
        sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])            