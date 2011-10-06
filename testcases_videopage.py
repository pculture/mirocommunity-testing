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
#     4. TestCase_ApproveVideo_569
#     5. TestCase_UpdateThumbnail_570

from selenium import selenium
import unittest, os, time, re, mclib, testcase_base
# import urllib, Image, ImageChop
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




class TestCase_RejectVideo_568(testcase_base.testcase_BaseTestCase):
    
    def RejectVideo(self, sel, theme):
        # Selecting the first video from the list of current videos on Bulk Edit page
        bulkedit.PickFirstVideo(self,sel,"Current")
        time.sleep(15)
        if videopage.InlineManageVideo(self,sel,theme,"Reject")==True:
            print "OK, test passed"
        else:
            print "Oops, test failed"
            mclib.AppendErrorMessage(self,sel,"Could not find the video in the list of rejected videos")

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



class TestCase_ApproveVideo_569(testcase_base.testcase_BaseTestCase):
    
    def ApproveVideo(self, sel, theme):
        # Selecting the first video from the list of rejected videos on Bulk Edit page
        bulkedit.PickFirstVideo(self,sel,"Rejected")
        time.sleep(15)
        if videopage.InlineManageVideo(self,sel,theme,"Approve")==True:
            print "OK, test passed"
        else:
            print "Oops, test failed"
            mclib.AppendErrorMessage(self,sel,"Could not find the video in the list of approved videos")

    def test_ApproveVideo(self):
        sel = self.selenium
#       Log in as Admin
        loginlogout.LogInAsAdmin(self,sel)
        for theme in range(1,5):
            print ""
            print "============================================"
            print ""
            print "Running Approve Video test with theme: "+str(theme)
            print "Changing theme..."
            sitesettings.ChangeTheme(self,sel,theme)
            TestCase_ApproveVideo_569.ApproveVideo(self,sel,theme)



class TestCase_UpdateThumbnail_570(testcase_base.testcase_BaseTestCase):
    
    def UpdateThumbnail(self, sel, theme):
        videoNumber = str(theme+1) # Select video No. between 1 and 4
        # Selecting the first video from the list of new videos
        sel.open(testvars.MCTestVariables["NewVideosListingPage"])
        sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])
        #"css = div#content div.video:nth(0) > a.thumbnail > img"
        # Memorizing the video title
        if theme!=4:  videoTitleLink ="//div[@id='content']/div["+videoNumber+"]/div/h3/a"
        else:  videoTitleLink="css=ul.vid_list > li:nth-child("+videoNumber+")> div.item_details>h2>a"
        videoTitle=sel.get_text(videoTitleLink)

        print "Step A. Upload thumbnail from YouTube"
        print "Opening the video page for video "+videoTitle+" ..."
#        sel.click("css = div#content div.video:nth(0) > a.thumbnail > img")
        
#        imageSrc = sel.get_attribute("//div[@id='content']/div["+videoNumber+"]/a/img@src")
#        image1 = Image.open(urlib.urlopen(imageSrc))
        sel.click(videoTitleLink)
        sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])
        YouTubeThumbURL = "http://img.youtube.com/vi/qzotQbR0GC0/0.jpg"
        videopage.ChangeThumbnail(self,sel,theme,YouTubeThumbURL,"")
        sel.open(testvars.MCTestVariables["NewVideosListingPage"])
        sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])
#        imageSrc = sel.get_attribute("//div[@id='content']/div["+videoNumber+"]/a/img@src")
#        image2 = Image.open(urlib.urlopen(imageSrc))
#        if ImageChop.difference(image2,image1) == None:
#            mclib.AppendErrorMessage(self,sel,"The thumbnail has not changed")
        print ""

        print "Step B. Upload an image from TestInput folder"
        print "Opening the video page for video "+videoTitle+" ..."
        sel.click("link="+videoTitle)
        sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])
        fileNewImage = "background2.jpg"
        thumbnailFile = os.path.join(testvars.MCTestVariables["GraphicFilesDirectory"],fileNewImage)
        videopage.ChangeThumbnail(self,sel,theme,"",thumbnailFile)
        print ""
        
        

    def test_UpdateThumbnail(self):
        sel = self.selenium
#       Log in as Admin
        loginlogout.LogInAsAdmin(self,sel)
        for theme in range(1,5):
            print ""
            print "============================================"
            print ""
            print "Running Update Thumbnail test with theme: "+str(theme)
            print "Changing theme..."
            sitesettings.ChangeTheme(self,sel,theme)
            TestCase_UpdateThumbnail_570.UpdateThumbnail(self,sel,theme)
