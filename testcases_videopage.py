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
#     6. TestCase_EditTitleInline_571
#     7. TestCase_EditPublicationDate_572

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
        # Selecting video No. <theme> from New Videos listing
        videoTitleLink = videopage.PickVideoFromNewVideosListingPage(self, sel, theme)
        videoTitle=sel.get_text(videoTitleLink)

        print "Step A. Upload thumbnail from YouTube"
        print "Opening the video page for video "+videoTitle+" ..."
#        sel.click("css = div#content div.video:nth(0) > a.thumbnail > img")
        
#        imageSrc = sel.get_attribute("//div[@id='content']/div["+videoNumber+"]/a/img@src")
#        image1 = Image.open(urlib.urlopen(imageSrc))
        sel.click(videoTitleLink)
        sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])
        YouTubeThumbURL = "http://img.youtube.com/vi/qzotQbR0GC0/0.jpg"
        initialThumbURL = videopage.GetThumbnailURL(self,sel)
        print initialThumbURL
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
        fileNewImage = "background"+str(theme)+".jpg"
        thumbnailFile = os.path.join(testvars.MCTestVariables["GraphicFilesDirectory"],fileNewImage)
        videopage.ChangeThumbnail(self,sel,theme,"",thumbnailFile)
        print ""

        if initialThumbURL!="":
            print "Step C. Restore the initial thumbnail"
            sel.open(testvars.MCTestVariables["NewVideosListingPage"])
            sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])
            sel.click(videoTitleLink)
            sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])
            videopage.ChangeThumbnail(self,sel,theme,initialThumbURL,"")
            

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



class TestCase_EditTitleInline_571(testcase_base.testcase_BaseTestCase):
    
    def EditTitle(self, sel, theme):
        # Selecting video No. <theme> from New Videos listing
        videoTitleLink = videopage.PickVideoFromNewVideosListingPage(self, sel, theme)
        videoTitle=sel.get_text(videoTitleLink)
        print "Opening video page for video "+videoTitle+"..."
        sel.click(videoTitleLink)
        sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])
        newTitle = "test title"
        print "Replacing the existing title with "+newTitle
        videopage.InlineEditTitle(self,sel,theme,newTitle)
        if queue.CheckVideoStatus(self,sel,newTitle,"Approved")==True:
            print "OK, test passed"
            print "Restoring the original title..."
            sel.open(testvars.MCTestVariables["NewVideosListingPage"])
            sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])
            sel.click(videoTitleLink)
            sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])
            videopage.InlineEditTitle(self,sel,theme,videoTitle)
        else:
            print "Oops, test failed"
            mclib.AppendErrorMessage(self,sel,"Could not find the video in the list of approved videos")

    def test_EditTitle(self):
        sel = self.selenium
#       Log in as Admin
        loginlogout.LogInAsAdmin(self,sel)
        for theme in range(1,5):
            print ""
            print "============================================"
            print ""
            print "Running Edit Title Inline test with theme: "+str(theme)
            print "Changing theme..."
            sitesettings.ChangeTheme(self,sel,theme)
            TestCase_EditTitleInline_571.EditTitle(self,sel,theme)





class TestCase_EditPublicationDate_572(testcase_base.testcase_BaseTestCase):
    
    def EditPublicationDate(self, sel, theme):
        # Selecting video No. <theme> from New Videos listing
        videoTitleLink = videopage.PickVideoFromNewVideosListingPage(self, sel, theme)
        videoTitle=sel.get_text(videoTitleLink)
        print "Opening video page for video "+videoTitle+"..."
        sel.click(videoTitleLink)
        sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])
        newDate = "2010-01-01 23:59:59"   #Format: yyyy-mm-dd hh:mm:ss
        print "Replacing the existing date with "+newDate
        videopage.InlineEditPublicationDate(self,sel,theme,newDate)

    def test_EditPublicationDate(self):
        sel = self.selenium
#       Log in as Admin
        loginlogout.LogInAsAdmin(self,sel)
        # Check Use Original Date check box on Settings page
        sitesettings.CheckUseOriginalDate(self,sel)
        for theme in range(1,5):
            print ""
            print "============================================"
            print ""
            print "Running Edit Publication Date Inline test with theme: "+str(theme)
            print "Changing theme..."
            sitesettings.ChangeTheme(self,sel,theme)
            TestCase_EditPublicationDate_572.EditPublicationDate(self,sel,theme)

