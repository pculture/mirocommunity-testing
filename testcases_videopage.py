#=======================================================================
#
#                             VIDEO PAGE TESTS
#
#=======================================================================
#
# Includes the following test cases:
#     1. TestCase_FeatureVideo_566
#     2. TestCase_UnfeatureVideo_567
#     3. TestCase_RejectVideo_568

from selenium import selenium
import unittest, time, re, mclib, testcase_base
import loginlogout, sitesettings, testvars, categories, submitvideos, sitesettings, queue, videopage,  bulkedit
import sys

# ----------------------------------------------------------------------

class TestCase_FeatureVideo_566(testcase_base.testcase_BaseTestCase):
    
    def UnfeatureAllVideos(self,sel):
        print "Unfeaturing all the featured videos"
        bulkedit.NavigateToBulkEdit(self,sel)
        while sel.is_element_present("id_form-0-BULK")==1:
            bulkedit.BulkEditAllVideosOnPage(self,sel,1,"Featured Videos","Unfeature")
            sel.open(testvars.MCTestVariables["BulkEditPage"]+"/?page=1")
            sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])
            sel.select("name=filter", "label=Featured Videos")
            sel.click("css=button.med_button")
            sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])
        

    def FeatureVideo(self, sel, theme):
        # Selecting the first video from the list of current videos on Bulk Edit page
        bulkedit.PickFirstVideo(self,sel,"Current")
        time.sleep(15)
        if videopage.InlineManageVideo(self,sel,theme,"Feature")==True:
            print "OK, test passed"
        else:
            print "Oops, test failed"
            mclib.AppendErrorMessage(self,sel,"Could not find the video in the list of featured videos")

    def test_FeatureVideo(self):
        sel = self.selenium
#       Log in as Admin
        loginlogout.LogInAsAdmin(self,sel)
        print "Unfeaturing all the videos..."
        TestCase_FeatureVideo_566.UnfeatureAllVideos(self,sel)
        print "Starting tests..."
        for theme in range(1,5):
            print ""
            print "============================================"
            print ""
            print "Running Feature Video test with theme: "+str(theme)
            print "Changing theme..."
            sitesettings.ChangeTheme(self,sel,theme)
            TestCase_FeatureVideo_566.FeatureVideo(self,sel,theme)
        #theme = sitesettings.ThemeScanner(self,sel)




class TestCase_UnfeatureVideo_567(testcase_base.testcase_BaseTestCase):
    
    def FeatureSomeVideos(self,sel):
        print "Featuring a page of videos"
        bulkedit.NavigateToBulkEdit(self,sel)
        if sel.is_element_present("id_form-0-BULK")==1:
            bulkedit.BulkEditAllVideosOnPage(self,sel,1,"Current Videos","Feature")
        else:
            mclib.AppendErrorMessage(self,sel,"Not enough videos to run the test")
        

    def UnfeatureVideo(self, sel, theme):
        # Selecting the first video from the list of featured videos on Bulk Edit page
        bulkedit.PickFirstVideo(self,sel,"Featured")
        time.sleep(15)
        if videopage.InlineManageVideo(self,sel,theme,"Unfeature")==True:
            print "OK, test passed"
        else:
            print "Oops, test failed"
            mclib.AppendErrorMessage(self,sel,"Could not find the video in the list of featured videos")

    def test_UnfeatureVideo(self):
        sel = self.selenium
#       Log in as Admin
        loginlogout.LogInAsAdmin(self,sel)
        print "Featuring a few videos..."
        TestCase_UnfeatureVideo_567.FeatureSomeVideos(self,sel)
        print "Starting tests..."
        for theme in range(1,5):
            print ""
            print "============================================"
            print ""
            print "Running Unfeature Video test with theme: "+str(theme)
            print "Changing theme..."
            sitesettings.ChangeTheme(self,sel,theme)
            TestCase_UnfeatureVideo_567.UnfeatureVideo(self,sel,theme)
        #theme = sitesettings.ThemeScanner(self,sel)




class TestCase_RejectVideo_568(testcase_base.testcase_BaseTestCase):
    
    def RejectVideo(self, sel, theme):
        # Selecting the first video from the list of current videos on Bulk Edit page
        bulkedit.PickFirstVideo(self,sel,"Current")
        time.sleep(15)
        if videopage.InlineManageVideo(self,sel,theme,"Reject")==True:
            print "OK, test passed"
        else:
            print "Oops, test failed"
            mclib.AppendErrorMessage(self,sel,"Could not find the video in the list of featured videos")

    def test_RejectVideo(self):
        sel = self.selenium
#       Log in as Admin
        loginlogout.LogInAsAdmin(self,sel)
        for theme in range(1,5):
            print ""
            print "============================================"
            print ""
            print "Running Reject Video test with theme: "+str(theme)
            print "Changing theme..."
            sitesettings.ChangeTheme(self,sel,theme)
            TestCase_RejectVideo_568.RejectVideo(self,sel,theme)
        #theme = sitesettings.ThemeScanner(self,sel)
