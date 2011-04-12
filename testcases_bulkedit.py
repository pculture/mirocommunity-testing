#=======================================================================
#
#                             BULK EDIT TESTS
#
#=======================================================================
#
# Includes the following test cases:
#     1. testcase_BulkEdit_BulkEdit_446
#     2. testcase_BulkEdit_BulkDelete_447
#     3. testcase_BulkEdit_BulkFeature_448
#     4. testcase_BulkEdit_BulkUnfeature_449
#     5. testcase_BulkEdit_DeleteSingleVideo_453
#     6. testcase_BulkEdit_EditSingleVideo_452
#     7. testcase_BulkEdit_UnapproveCurrent_450
#     8. testcase_BulkEdit_UnapproveFeatured_451
#     9. testcase_BulkEdit_SortByTitle_454
#     10. testcase_BulkEdit_SortBySource_455
#     11. testcase_BulkEdit_SortByDatePublished_456
#     12. testcase_BulkEdit_SortByDateImported_457


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
gEditDate = "1999-06-11 00:00:00"

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

global gVideoTitleOnBulkEditPagePart1
gVideoTitleOnBulkEditPagePart1 = "XPath=id('labels')/form[2]/table/tbody/tr["

global gVideoTitleOnBulkEditPagePart2
gVideoTitleOnBulkEditPagePart2 = "]/td[2]/span"

global gSourceTitleOnBulkEditPagePart1
gSourceTitleOnBulkEditPagePart1 = "XPath=id('labels')/form[2]/table/tbody/tr["

global gSourceTitleOnBulkEditPagePart2
gSourceTitleOnBulkEditPagePart2 = "]/td[3]"

global gDatePublishedTitleOnBulkEditPagePart1
gDatePublishedTitleOnBulkEditPagePart1 = "XPath=id('labels')/form[2]/table/tbody/tr["

global gDatePublishedTitleOnBulkEditPagePart2
gDatePublishedTitleOnBulkEditPagePart2 = "]/td[5]/span"

global gDateImportedTitleOnBulkEditPagePart1
gDateImportedTitleOnBulkEditPagePart1 = "XPath=id('labels')/form[2]/table/tbody/tr["

global gDateImportedTitleOnBulkEditPagePart2
gDateImportedTitleOnBulkEditPagePart2 = "]/td[6]/span"

global gPageLinkPart1
gPageLinkPart1 = "XPath=id('labels')/form[2]/div[3]/ul/li["

global gPageLinkPart2
gPageLinkPart2 = "]/a/span"

global gSortByVideoTitleLink
gSortByVideoTitleLink = "XPath=id('labels')/form[2]/table/thead/tr/th[2]/a"

global gSortBySource
gSortBySource = "XPath=id('labels')/form[2]/table/thead/tr/th[3]/a"

global gSortByDatePublished
gSortByDatePublished = "XPath=id('labels')/form[2]/table/thead/tr/th[5]/a"

global gSortByDateImported
gSortByDateImported = "XPath=id('labels')/form[2]/table/thead/tr/th[6]/a"

#-----

global gSeleniumServerPort
gSeleniumServerPort = testvars.MCTestVariables["Port"]

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
        self.selenium.set_timeout(testvars.MCTestVariables["TimeOut"])

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
#        sel.click(gVideosSectionOnAdminPage)
        sel.open(testvars.MCTestVariables["ReviewQueuePage"])
        sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])

    #Submits video with given URL, works if video was submitted before
    def SubmitVideo(self, in_VideoUrl):
        sel = self.selenium
        sel.open(testvars.MCTestVariables["ReviewQueuePage"])
        sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])
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
        sel.open(testvars.MCTestVariables["BulkEditPage"])
#        sel.click(gBulkEditOnAdminPage)
        sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])

        time.sleep(5)
        sel.type(gSearchEditBoxOnBulkEditPage, gVideosLabel)
        time.sleep(5)
        sel.click(gSearchButtonOnBulkEditPage)
        sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])

        time.sleep(5)
        sel.click(gToggleAll)
        sel.select(gActionSelector, gDeleteOption)
        sel.click(gApplyButton)
        sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])

    #Adds new category with name defined in 'gCategoryName', works if category was added before
    def AddCategory(self):
        sel = self.selenium
 #       sel.click(gCategoriesOnAdminPage)
        sel.open(testvars.MCTestVariables["CategoriesPage"])
        sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])

        sel.click(gAddCategoryButtonOnCategoryPage)
        WaitUntilElementOnTheScreen(sel, gAddCategoryButton, gTimeOut)

        time.sleep(2)

        sel.type(gCategoryNameEditField, "")
        sel.type(gCategoryNameEditField, gCategoryName)

        sel.type(gCategorySlugEditField, "")
        sel.type(gCategorySlugEditField, gCategoryName)
        sel.click(gAddCategoryButton)

        time.sleep(5)
        if sel.is_element_present(gCategoryNameEditField):
            sel.click(gCloseAddCategoryWindowButton)

    #Adds new user with name defined in 'gBulkEditUserName', works if user was added before
    def AddUser(self):
        
        sel = self.selenium

#        sel.click(gUsersSectionOnAdminPage)
        sel.open(testvars.MCTestVariables["UserPage"])
        sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])

        sel.click(gAddUserButtonOnUsersPage)
        WaitUntilElementOnTheScreen(sel, gUserRadioButtonInAddUserWindow, gTimeOut)

        sel.type(gUserNameEditBoxInAddUserWindow, gBulkEditUserName)
        sel.click(gUserRadioButtonInAddUserWindow)
        sel.type(gPasswordEditBoxInAddUserWindow, gBulkEditUserPassword)
        sel.type(gConfirmPasswordEditBoxInAddUserWindow, gBulkEditUserPassword)

        sel.click(gAddUserButtonInAddUserWindow)
        sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])

#        sel.click(gVideosSectionOnAdminPage)
#        sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])

    #Checks if changes that were made during editing of bulk of videos were saved and they are correct 
    def checkChanges(self, in_ViewLink, in_CheckTags):
        
        sel = self.selenium
        sel.click(in_ViewLink)
        sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])

        #XPath=id('main')/div[1]/div/div/div[1]/h2[contains(.,'BulkEditTestTitleJudo')]

        if (not sel.is_element_present(gTitlePathOnViewVideoPage + gEditTitle + "')]") ):
            print "ERROR: Title was not found or it is incorrect"
            self.failUnless(False)

        if (not sel.is_element_present(gUserPathOnViewVideoPage + gBulkEditUserName + "')]") ):
            print "ERROR: User's Name was not found or it is incorrect"
            self.failUnless(False)

        if (not sel.is_element_present(gDescriptionPathOnViewVideoPage + gEditDescription + "')]") ):
            print "ERROR: Description was not found or it is incorrect"
            self.failUnless(False)

        if (not sel.is_element_present(gCategoryPathOnViewVideoPage + gCategoryName + "')]") ):
            print "ERROR: Category was not found or it is incorrect"
            self.failUnless(False)

        if in_CheckTags:
            if (not sel.is_element_present(gTagsPathOnViewVideoPage + gEditTag + "')]") ):
                print "ERROR: Tag was not found or it is incorrect"
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
        print "Logging in as admin and going to 'View Admin' page..."
        self.LoginAsAdminSetThemeGoToViewAdmin()
        #time.sleep(20)
        print "Deleting videos..."
        self.DeleteVideos()
        #time.sleep(20)
        print "Adding a user..."
        self.AddUser()
        #time.sleep(20)
        print "Adding a category..."
        self.AddCategory()
        #time.sleep(20)
        print "Submitting the first video..."
        self.SubmitVideo(gVideo1Url)
        #time.sleep(20)
        print "Submitting the second video..."
        self.SubmitVideo(gVideo2Url)
        #time.sleep(20)
            

#Tests AUT for edititng and deleting videos by 'Bulk Edit'
class testcase_BulkEdit_BulkEdit_446(testcase_BaseClassForBulkEdit):
        
    #The body of test case
    def test_case(self):

        print ""
        print "Starting 'testcase_BulkEdit_EditAndDelete' test case..."
        sel = self.selenium
        self.LoginDeleteVideosAddUserAddCategoryAddVideos()

        print "Opening 'Bulk Edit' page..."
#        sel.click(gBulkEditOnAdminPage)
        sel.open(testvars.MCTestVariables["BulkEditPage"])
        sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])

        print "Searching all videos with 'gVideosLabel'..."
        time.sleep(5)
        sel.type(gSearchEditBoxOnBulkEditPage, gVideosLabel)
        time.sleep(5)
        sel.click(gSearchButtonOnBulkEditPage)
        sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])

        print "Checking all found videos..."
        time.sleep(5)
        sel.click(gToggleAll)
        time.sleep(5)
        print "Choosing 'Edit' option and clicking 'Apply' button..."
        sel.select(gActionSelector, gEditOption)
        time.sleep(10)
        sel.click(gApplyButton)

        print "Editing selected videos..."
        WaitUntilElementOnTheScreen(sel, gEditCategoryXPath, gTimeOut)
        time.sleep(10)
        sel.type(gEditPageTitleEditField, "")
        sel.type(gEditPageTitleEditField, gEditTitle)
        sel.type(gEditPageDateEditField, "")
        sel.type(gEditPageDateEditField, gEditDate)
        sel.type(gEditPageDescriptionEditField, "")
        sel.type(gEditPageDescriptionEditField, gEditDescription)
        sel.type(gEditPageTagsEditField, "")
        sel.type(gEditPageTagsEditField, gEditTag)

        sel.check(gEditCategoryXPath)
        sel.check(gEditUserXPath)

        #time.sleep(60)        
        print "Saving changes..."        
        sel.click(gSaveChangesButtonInEditWindow)

        sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])

        #time.sleep(60)        

        print "Checking changes in the first video..."        
        self.checkChanges(gLinkToViewFirstVideo, True)

        sel.click(gViewAdmin)
        sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])

        #sel.click(gBulkEditOnAdminPage)
        sel.open(testvars.MCTestVariables["BulkEditPage"])
        sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])

        sel.type(gSearchEditBoxOnBulkEditPage, gVideosLabel)
        sel.click(gSearchButtonOnBulkEditPage)
#        sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])
        sel.wait_for_page_to_load("300000")

        print "Checking changes in the second video..."                
        self.checkChanges(gLinkToViewSecondVideo, True)
        

class testcase_BulkEdit_BulkDelete_447(testcase_BaseClassForBulkEdit):
        
    #The body of test case
    def test_case(self):

        print ""
        print "Starting 'testcase_BulkEdit_BulkDelete' test case..."
        sel = self.selenium
        self.LoginDeleteVideosAddUserAddCategoryAddVideos()

        print "Opening 'Bulk Edit' page..."
#        sel.click(gBulkEditOnAdminPage)
        sel.open(testvars.MCTestVariables["BulkEditPage"])
        sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])

        print "Searching all videos with 'gVideosLabel'..."
        sel.type(gSearchEditBoxOnBulkEditPage, gVideosLabel)
        sel.click(gSearchButtonOnBulkEditPage)
        sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])

        print "Checking all found videos..."
        sel.click(gToggleAll)

        # Delete

        print "Deleting videos..."                
        self.DeleteVideos()

        print "Verifying if videos have been deleted..."                
#        sel.click(gBulkEditOnAdminPage)
        sel.open(testvars.MCTestVariables["BulkEditPage"])
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
class testcase_BulkEdit_BulkFeature_448(testcase_BaseClassForBulkEdit):

     #The body of test case     
     def test_case(self):
         
        print ""
        print "Starting 'testcase_BulkEdit_BulkFeature' test case..."
        sel = self.selenium
        self.LoginDeleteVideosAddVideos()

        print "Opening 'Bulk Edit' page..."        
#        sel.click(gBulkEditOnAdminPage)
        sel.open(testvars.MCTestVariables["BulkEditPage"])
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


class testcase_BulkEdit_BulkUnfeature_449(testcase_BaseClassForBulkEdit):

     #The body of test case     
     def test_case(self):
         
        print ""
        print "Starting 'testcase_BulkEdit_BulkUnfeature' test case..."
        sel = self.selenium
        self.LoginDeleteVideosAddVideos()

        print "Opening 'Bulk Edit' page..."        
#        sel.click(gBulkEditOnAdminPage)
        sel.open(testvars.MCTestVariables["BulkEditPage"])
        sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])

        print "Searching all videos with 'gVideosLabel'..."
        sel.type(gSearchEditBoxOnBulkEditPage, gVideosLabel)
        sel.click(gSearchButtonOnBulkEditPage)
        sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])

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
class testcase_BulkEdit_EditSingleVideo_452(testcase_BaseClassForBulkEdit):
    #The body of test case     
     def test_case(self):
         
        print ""
        print "Starting 'testcase_BulkEdit_EditSingleVideo' test case..."
        sel = self.selenium
        self.LoginDeleteVideosAddUserAddCategoryAddVideos()

        print "Opening 'Bulk Edit' page..."        
#        sel.click(gBulkEditOnAdminPage)
        sel.open(testvars.MCTestVariables["BulkEditPage"])
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
#        sel.click("//div[@id='labels']/form[0]/table/tbody/tr[2]/td[1]/div/div[2]/ul/li[9]/a]")
        sel.click("link=Click to edit the users associated with this video")
        time.sleep(15)
        sel.check(gEditUserXPathSingleVideo)

        print "Saving changes..."        
        sel.click(gSaveChangesButtonInEditWindow)
        sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])

        print "Checking changes in the first video..."        
        self.checkChanges(gLinkToViewFirstVideo, False)

        time.sleep(10)        
                
#Tests AUT for deleting a single video
class testcase_BulkEdit_DeleteSingleVideo_453(testcase_BaseClassForBulkEdit):
    
    def test_case(self):
        print ""
        print "Starting 'testcase_BulkEdit_DeleteSingleVideo' test case..."
        sel = self.selenium
        self.LoginDeleteVideosAddVideos()

        print "Opening 'Bulk Edit' page..."        
#        sel.click(gBulkEditOnAdminPage)
        sel.open(testvars.MCTestVariables["BulkEditPage"])
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
class testcase_BulkEdit_UnapproveCurrent_450(testcase_BaseClassForBulkEdit):

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
#        sel.click(gReviewQueueOnAdminPage)
        sel.open(testvars.MCTestVariables["ReviewQueuePage"])
        sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])

        print "Clearing the queue..."
        if sel.is_element_present(gClearQueueButtonOnReviewQueuePage):
            sel.click(gClearQueueButtonOnReviewQueuePage)
            sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])
            sel.click(gYesClearQueueButton)
            sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])        

        print "Opening 'Bulk Edit' page..."        
#        sel.click(gBulkEditOnAdminPage)
        sel.open(testvars.MCTestVariables["BulkEditPage"])
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
class testcase_BulkEdit_UnapproveFeatured_451(testcase_BulkEdit_UnapproveCurrent_450):

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
#        sel.click(gBulkEditOnAdminPage)
        sel.open(testvars.MCTestVariables["BulkEditPage"])
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

#Tests AUT for sorting videos by 'Video Title' on 'Bulk Edit page'
class testcase_BulkEdit_SortByTitle_454(testcase_BaseClassForBulkEdit):

    cFirstPage = True
    cFirstVideoTitleLower = ""
    cSecondVideoTitleLower = ""
    cFirstVideoTitleOridinal = ""
    cSecondVideoTitleOriginal = ""
    cPreviousComparison = ""
    cPageNumber = 0

    cGetElementMethod = None
    cCompareMethod = None
    cSortingLink = None

    
    cMonths = ["jan, ","feb, ","mar, ","apr, ","may, ","jun, ","jul, ","aug, ","sep, ","oct, ","nov, ","dec, "]            

    #function that compares two strings
    def compareTwoStrings_(self, in_Str1, in_Str2):
        if in_Str1 > in_Str2:
            return ">"
        elif in_Str1 < in_Str2:
            return "<"
        else:
            return "=="
        
    #function that compares two Dates, the blank Date is lower that any other that has value
    def compareTwoDates(self, in_Str1, in_Str2):

        in_Str1 = in_Str1.lower()
        in_Str2 = in_Str2.lower()        

        if in_Str1 == "":
            if in_Str2 != "":
                return "<"
            else:
                return "=="
        elif in_Str2 =="":
            return ">"
        
        lMonth1 = -1
        lMonth2 = -1
        lYear1 = -1
        lYear2 = -1
        lDay1 = -1
        lDay2 = -1
        
        for i in range(0, len(self.cMonths)):
            if in_Str1.find(self.cMonths[i]) != -1:
                in_Str1 = in_Str1.replace(self.cMonths[i], "")
                lMonth1 = i
        in_Str1.replace(" ", "")
        lTempStr = in_Str1.partition(" ")
        lDay1 = long(lTempStr[0])
        lYear1 = long(lTempStr[2])

        for i in range(0, len(self.cMonths)):
            if in_Str2.find(self.cMonths[i]) != -1:
                in_Str2 = in_Str2.replace(self.cMonths[i], "")
                lMonth2 = i
        in_Str2.replace(" ", "")
        lTempStr = in_Str2.partition(" ")
        lDay2 = long(lTempStr[0])
        lYear2 = long(lTempStr[2])        

        lResultStr1 = lYear1*500 + lMonth1*40 + long(lDay1)
        lResultStr2 = lYear2*500 + lMonth2*40 + long(lDay2)

        if lResultStr1 > lResultStr2:
            return ">"
        elif lResultStr1 < lResultStr2:
            return "<"
        else:
            return "=="        

    #returns XPath to a page link with specified number from 'Bulk Edit' page
    def getPageLink_(self, in_Number):
        return gPageLinkPart1+str(in_Number)+gPageLinkPart2        

    #returns XPath for a Video's 'Video Title', needed row(video) specified by number
    def getVideoTitlePath_(self, in_Number):
        return gVideoTitleOnBulkEditPagePart1+str(in_Number)+gVideoTitleOnBulkEditPagePart2

    #returns XPath for a Video's 'Source', needed row(video) specified by number
    def getSourceTitlePath_(self, in_Number):
        return gSourceTitleOnBulkEditPagePart1+str(in_Number)+gSourceTitleOnBulkEditPagePart2

    #returns XPath for a Video's 'Date Published', needed row(video) specified by number
    def getDatePublishedTitlePath(self, in_Number):
        return gDatePublishedTitleOnBulkEditPagePart1+str(in_Number)+gDatePublishedTitleOnBulkEditPagePart2

    #returns XPath for a Video's 'Date Imported', needed row(video) specified by number
    def getDateImportedTitlePath(self, in_Number):
        return gDateImportedTitleOnBulkEditPagePart1+str(in_Number)+gDateImportedTitleOnBulkEditPagePart2

    #checks if page is sorted, it does not check if it's sorted in ascending or descending order, it just check if it's sorted in any way
    def checkIfPageIsSorted(self, in_GetElementMethod, in_CompareMethod):
        sel = self.selenium
        self.cPageNumber = self.cPageNumber + 1
        print ""
        lNoErrorsIndicator = True
        print ""
        if self.cFirstPage:

            if sel.is_element_present(in_GetElementMethod(1)):
                self.cFirstVideoTitleOridinal = sel.get_text(in_GetElementMethod(1))
                self.cFirstVideoTitleLower = self.cFirstVideoTitleOridinal.lower()

            i = 1            
            while sel.is_element_present(in_GetElementMethod(i+1)):

                self.cSecondVideoTitleOriginal = sel.get_text(in_GetElementMethod(i+1))
                self.cSecondVideoTitleLower = self.cSecondVideoTitleOriginal.lower()

                lCurrentComparison = in_CompareMethod(self.cFirstVideoTitleLower, self.cSecondVideoTitleLower)                
                
                if (lCurrentComparison != "=="):
                    if (self.cPreviousComparison != ""):
                        if (lCurrentComparison != self.cPreviousComparison):
                            print ""
                            print "ERROR: Elements #", i, "and #", i+1, "on page #", self.cPageNumber, " are not sorted properly!"
                            print "Value of element #", i, " is ", self.cFirstVideoTitleOridinal
                            print "Value of element #", i+1, " is ", self.cSecondVideoTitleOriginal
                            print "Previous comparison is ", self.cPreviousComparison
                            print "Current comparison is ", lCurrentComparison
                            print "Char's listing in lower case of element #", i
                            print "-----"
                            lStr_ = ""
                            for j in range(0, len(self.cFirstVideoTitleLower)):
                                lStr_ = lStr_ + str(ord(self.cFirstVideoTitleLower[j])) + " ,"
                            print lStr_
                            print "-----"
                            print "Char's listing in lower case of element #", i+1
                            print "-----"
                            lStr_ = ""
                            for j in range(0, len(self.cSecondVideoTitleLower)):
                                lStr_ = lStr_ + str(ord(self.cSecondVideoTitleLower[j])) + " ,"
                            print lStr_
                            print "-----"
                            lNoErrorsIndicator = False
                            #self.assertEqual(False, True)
                            try: self.failUnless(False)
                            except AssertionError, e: self.verificationErrors = "For ERRORs check logs above )))"
                            #except AssertionError, e: None
                    self.cPreviousComparison = lCurrentComparison
                        
                i = i+1
                self.cFirstVideoTitleOridinal = self.cSecondVideoTitleOriginal
                self.cFirstVideoTitleLower = self.cSecondVideoTitleLower
                
            return lNoErrorsIndicator
        
        else:

            if sel.is_element_present(in_GetElementMethod(1)):
                self.cSecondVideoTitleOriginal = sel.get_text(in_GetElementMethod(1))
                self.cSecondVideoTitleLower = self.cSecondVideoTitleOriginal.lower()            

            lCurrentComparison = in_CompareMethod(self.cFirstVideoTitleLower, self.cSecondVideoTitleLower)
            if lCurrentComparison != "==":
                if (self.cPreviousComparison != ""):
                    if (lCurrentComparison != self.cPreviousComparison):
                        print ""
                        print "ERROR: The last element from page #", self.cPageNumber-1, "and the first element from page #", self.cPageNumber, " are not sorted properly!"
                        print "Value of the last element from page #", self.cPageNumber-1, " is ", self.cFirstVideoTitleOridinal
                        print "Value of the first element from page #", self.cPageNumber, " is ", self.cSecondVideoTitleOriginal
                        print "Previous comparison is ", self.cPreviousComparison
                        print "Current comparison is ", lCurrentComparison
                        print "Char's listing in lower case of The last element from page #", self.cPageNumber-1
                        print "-----"
                        lStr_ = ""
                        for j in range(0, len(self.cFirstVideoTitleLower)):
                            lStr_ = lStr_ + str(ord(self.cFirstVideoTitleLower[j])) + " ,"
                        print lStr_
                        print "-----"
                        print "Char's listing in lower case of the first element from page #", self.cPageNumber
                        print "-----"
                        lStr_ = ""
                        for j in range(0, len(self.cSecondVideoTitleLower)):
                            lStr_ = lStr_ + str(ord(self.cSecondVideoTitleLower[j])) + " ,"
                        print lStr_
                        print "-----"
                        lNoErrorsIndicator = False
                        #self.assertEqual(False, True)
                        try: self.failUnless(False)
                        except AssertionError, e: self.verificationErrors = "For ERRORs check logs above )))"
                self.cPreviousComparison = lCurrentComparison

            self.cFirstVideoTitleOridinal = self.cSecondVideoTitleOriginal
            self.cFirstVideoTitleLower = self.cSecondVideoTitleLower
                    
            i = 1            
            while sel.is_element_present(in_GetElementMethod(i+1)):

                self.cSecondVideoTitleOriginal = sel.get_text(in_GetElementMethod(i+1))
                self.cSecondVideoTitleLower = self.cSecondVideoTitleOriginal.lower()

                lCurrentComparison = in_CompareMethod(self.cFirstVideoTitleLower, self.cSecondVideoTitleLower)                
                
                if (lCurrentComparison != "=="):
                    if (self.cPreviousComparison != ""):
                        if (lCurrentComparison != self.cPreviousComparison):
                            print ""
                            print "ERROR: Elements #", i, "and #", i+1, "on page #", self.cPageNumber, " are not sorted properly!"
                            print "Value of element #", i, " is ", self.cFirstVideoTitleOridinal
                            print "Value of element #", i+1, " is ", self.cSecondVideoTitleOriginal
                            print "Previous comparison is ", self.cPreviousComparison
                            print "Current comparison is ", lCurrentComparison
                            print "Char's listing in lower case of element #", i
                            print "-----"
                            lStr_ = ""
                            for j in range(0, len(self.cFirstVideoTitleLower)):
                                lStr_ = lStr_ + str(ord(self.cFirstVideoTitleLower[j])) + " ,"
                            print lStr_
                            print "-----"
                            print "Char's listing in lower case of element #", i+1
                            print "-----"
                            lStr_ = ""
                            for j in range(0, len(self.cSecondVideoTitleLower)):
                                lStr_ = lStr_ + str(ord(self.cSecondVideoTitleLower[j])) + " ,"
                            print lStr_
                            print "-----"
                            lNoErrorsIndicator = False
                            #self.assertEqual(False, True)
                            try: self.failUnless(False)
                            except AssertionError, e: self.verificationErrors = "For ERRORs check logs above )))"
                            #except AssertionError, e: None
                    self.cPreviousComparison = lCurrentComparison
                        
                i = i+1
                self.cFirstVideoTitleOridinal = self.cSecondVideoTitleOriginal
                self.cFirstVideoTitleLower = self.cSecondVideoTitleLower
                
            return lNoErrorsIndicator

    #should be called after one of the links to sort videos has been clicked
    def zeroVariables(self):
        self.cFirstPage = True
        self.cFirstVideoTitleLower = ""
        self.cSecondVideoTitleLower = ""
        self.cFirstVideoTitleOridinal = ""
        self.cSecondVideoTitleOriginal = ""
        self.cPreviousComparison = ""
        self.cPageNumber = 0  

    #this funcion has to be redefined in inherited classes, it defines methods to be used during checking of sorting results
    def initialize(self):
        print ""
        print "Starting 'testcase_BulkEdit_SortByTitle' test case..."
        self.cGetElementMethod = self.getVideoTitlePath_
        self.cCompareMethod = self.compareTwoStrings_
        self.cSortingLink = gSortByVideoTitleLink
        

    #code of the test case
    def test_case(self):
        
        self.initialize()
        
        sel = self.selenium
        print "Loging in..."
        LogIn(sel, testvars.MCTestVariables["AdminLogin"], testvars.MCTestVariables["AdminPassword"])
        WaitUntilElementOnTheScreen(sel, gViewAdmin, gTimeOut)
        print "Cliking 'View Admin' link..."
        sel.click(gViewAdmin)
        sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])
        print "Going on 'Bulk Edit' page..."
#        sel.click(gBulkEditOnAdminPage)
        sel.open(testvars.MCTestVariables["BulkEditPage"])
        sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])

        #-------------------------------------------------------------------------------------------------------------------------------
        print "Sorting Videos by one of the attributes..."
        sel.click(self.cSortingLink)
        sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])

        print "Checking if the first page is sorted..."        
        self.checkIfPageIsSorted(self.cGetElementMethod, self.cCompareMethod)
        self.cFirstPage = False
        i = 2
        while sel.is_element_present(self.getPageLink_(i)):
            print "Checking if the page #", i, " is sorted..."
            sel.click(self.getPageLink_(i))
            sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])
            self.checkIfPageIsSorted(self.cGetElementMethod, self.cCompareMethod)
            i = i + 1
            
        #-------------------------------------------------------------------------------------------------------------------------------

        print "Set start values to variables..."
        self.zeroVariables()          

        print "Checking if there is a first page..."
        if sel.is_element_present(self.getPageLink_(1)):
            print "Going back to the first page..."
            sel.click(self.getPageLink_(1))
            sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])

        print "Sorting Videos by one of the attributes..."

        sel.click(self.cSortingLink)            
        sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])

        print "Checking if the first page is sorted..."        
        self.checkIfPageIsSorted(self.cGetElementMethod, self.cCompareMethod)
        self.cFirstPage = False
        i = 2
        while sel.is_element_present(self.getPageLink_(i)):
            print "Checking if the page #", i, " is sorted..."
            sel.click(self.getPageLink_(i))
            sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])
            self.checkIfPageIsSorted(self.cGetElementMethod, self.cCompareMethod)
            i = i + 1

        print "Algorithm, that is used to check if page is sorted, is based on checking if previous pair of elements has the same results as current pair,\n\
              it does not know which way page is supposed to be sorted. Thus, single error on the page will result into two error reports."

#Tests AUT for sorting videos by 'Source' on 'Bulk Edit page'
class testcase_BulkEdit_SortBySource_455(testcase_BulkEdit_SortByTitle_454):

    def initialize(self):
        
        print ""
        print "Starting 'testcase_BulkEdit_SortBySource' test case..."
        self.cGetElementMethod = self.getSourceTitlePath_
        self.cCompareMethod = self.compareTwoStrings_
        self.cSortingLink = gSortBySource

#Tests AUT for sorting videos by 'Date Published' on 'Bulk Edit page'
class testcase_BulkEdit_SortByDatePublished_456(testcase_BulkEdit_SortByTitle_454):

    def initialize(self):
        
        print ""
        print "Starting 'testcase_BulkEdit_SortByDatePublished' test case..."
        self.cGetElementMethod = self.getDatePublishedTitlePath
        self.cCompareMethod = self.compareTwoDates
        self.cSortingLink = gSortByDatePublished

#Tests AUT for sorting videos by 'Date Imported' on 'Bulk Edit page'
class testcase_BulkEdit_SortByDateImported_457(testcase_BulkEdit_SortByTitle_454):

    def initialize(self):
        
        print ""
        print "Starting 'testcase_BulkEdit_SortByDateImported' test case..."
        self.cGetElementMethod = self.getDateImportedTitlePath
        self.cCompareMethod = self.compareTwoDates
        self.cSortingLink = gSortByDateImported
    