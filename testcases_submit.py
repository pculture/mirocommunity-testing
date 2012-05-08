#=======================================================================
#
#                       SUBMIT VIDEO TESTS
#
#=======================================================================
#
# Includes the following test cases:
#     1. TestCase_SubmitVideoAsAdmin_471
#     2. TestCase_SubmitVideoAsLoggedUser_472
#     3. TestCase_SubmitVideoAsUnloggedUser_473
#     4. TestCase_SubmitVideoFromAdminPage_474
#     5. TestCase_SubmitDuplicateVideo_475
#     6. TestCase_SubmitVideoWithEmbedCode_476


from selenium import selenium
import unittest, time, re, loginlogout, sitesettings, testvars, queue, submitvideos
import sys

# ----------------------------------------------------------------------

class TestCase_SubmitVideoAsAdmin_471(unittest.TestCase):
    
# Open the desired browser and set up the test
    def setUp(self):
        self.verificationErrors = []
        self.selenium = selenium("localhost", testvars.MCTestVariables["Port"], testvars.MCTestVariables["Browser"], testvars.MCTestVariables["TestSite"])
        self.selenium.start()

    def test_SubmitVideoAsAdmin_471(self):
        sel = self.selenium
        # Log in as an Administrator
        loginlogout.LogInAsAdmin(self,sel)
        theme = 1
        sitesettings.ChangeTheme(self,sel,theme)
        # Display 'Submit a Video' button on front page
        sitesettings.DisplaySubmitVideo(self,sel,theme)
        # Set video parameters
        testVideoURL = "http://www.youtube.com/watch?v=43scrCjAVHc"
        testVideoTitle = "Mozilla Firefox"
        titleUnicode = unicode(testVideoTitle)
        # Check if the video is in the premoderation queue ("Unapproved") 
        # If yes, reject it
        queue.RejectVideoFromQueue(self,sel,titleUnicode)            
        # Navigate to the front page
#        sel.click(testvars.MCTestVariables["ViewMainSiteLink"])
        sel.open(testvars.MCTestVariables["TestSite"])
        sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])
        for theme in range(1,2):
            print ""
            print "The current theme is "+str(theme)
            # Check if the video is in the current ("Approved") set of videos
            # If yes, delete it
            submitvideos.RejectVideoFromApproved(self,sel,testVideoTitle)
            # Set the theme
            sitesettings.ChangeTheme(self,sel,theme)
            # Navigate to the front page
#            sel.click(testvars.MCTestVariables["ViewMainSiteLink"])
            sel.open(testvars.MCTestVariables["TestSite"])
            sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])
            # Submit a video and check the results
            submitvideos.SubmitVideo(self,sel,testVideoURL,theme,"Admin")  # as Admin 

# Close the browser, log errors, perform cleanup    
    def tearDown(self):
        self.selenium.stop()
# the command on the previous line should close the browser
        self.assertEqual([], self.verificationErrors)


class TestCase_SubmitVideoAsLoggedUser_472(unittest.TestCase):
    
# Open the desired browser and set up the test
    def setUp(self):
        self.verificationErrors = []
        self.selenium = selenium("localhost", testvars.MCTestVariables["Port"], testvars.MCTestVariables["Browser"], testvars.MCTestVariables["TestSite"])
        self.selenium.start()

# The user actions executed in the test scenario
    def test_SubmitVideoAsLoggedUser_472(self):
        sel = self.selenium
        # Set video parameters
        testVideoURL = "http://www.youtube.com/watch?v=MFREixTg4eI"
        testVideoTitle = "Miro Video Player"
        titleUnicode = unicode(testVideoTitle)
        # Log in as an Administrator
        loginlogout.LogInAsAdmin(self,sel)
        theme = 1
        sitesettings.ChangeTheme(self,sel,theme)
        # Display 'Submit a Video' button on front page
        sitesettings.DisplaySubmitVideo(self,sel,theme)
        # Check if the video is in the premoderation queue ("Unapproved") 
        # If yes, reject it
        queue.RejectVideoFromQueue(self,sel,titleUnicode)            
        # Navigate to the front page
#        sel.click(testvars.MCTestVariables["ViewMainSiteLink"])
        sel.open(testvars.MCTestVariables["TestSite"])
        sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])
        # Check if the video is in the current ("Approved") set of videos
        # If yes, delete it
        submitvideos.RejectVideoFromApproved(self,sel,testVideoTitle)
        for theme in range(1,2):
            print ""
            print "The current theme is "+str(theme)
            # Set the theme
            sitesettings.ChangeTheme(self,sel,theme)
            # Navigate to the front page
#            sel.click(testvars.MCTestVariables["ViewMainSiteLink"])
            sel.open(testvars.MCTestVariables["TestSite"])
            sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])
            # Log out
            loginlogout.LogOut(self,sel)
            # Log in as User
            loginlogout.LogInAsUser(self,sel)
            # Submit a video and check the results
            submitvideos.SubmitVideo(self, sel, testVideoURL, theme, "LoggedUser")  # as Admin 
            # Log out
            loginlogout.LogOut(self,sel)
            # Log in as Administrator
            loginlogout.LogInAsAdmin(self,sel)
            # Check if the video is in the premoderation queue ("Unapproved") 
            # If yes, reject it
            queue.RejectVideoFromQueue(self,sel,titleUnicode)            

# Close the browser, log errors, perform cleanup    
    def tearDown(self):
        self.selenium.stop()
# the command on the previous line should close the browser
        self.assertEqual([], self.verificationErrors)


class TestCase_SubmitVideoAsUnloggedUser_473(unittest.TestCase):
    
# Open the desired browser and set up the test
    def setUp(self):
        self.verificationErrors = []
        self.selenium = selenium("localhost", testvars.MCTestVariables["Port"], testvars.MCTestVariables["Browser"], testvars.MCTestVariables["TestSite"])
        self.selenium.start()

# The user actions executed in the test scenario
    def test_SubmitVideoAsUnloggedUser_473(self):
        sel = self.selenium
        # Log in as an Administrator
        loginlogout.LogInAsAdmin(self,sel)
        theme = 1
        sitesettings.ChangeTheme(self,sel,theme)
        # Check 'Require Login to Submit Video' on site settings page
        sitesettings.UncheckRequireLoginToSubmitVideo(self,sel)
        # Set video parameters
        testVideoURL = "http://www.youtube.com/watch?v=yjdUr1CATy8"
        testVideoTitle = "Go Open Source: Miro"
        titleUnicode = unicode(testVideoTitle)
        # Check if the video is in the premoderation queue ("Unapproved") 
        # If yes, reject it
        queue.RejectVideoFromQueue(self,sel,titleUnicode)            
        # Navigate to the front page
#        sel.click(testvars.MCTestVariables["ViewMainSiteLink"])
        sel.open(testvars.MCTestVariables["TestSite"])
        sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])
        # Check if the video is in the current ("Approved") set of videos
        # If yes, delete it
        submitvideos.RejectVideoFromApproved(self,sel,testVideoTitle)
        for theme in range(1,2):
            print ""
            print "The current theme is "+str(theme)
            # Set the theme
            sitesettings.ChangeTheme(self,sel,theme)
            # Navigate to the front page
#            sel.click(testvars.MCTestVariables["ViewMainSiteLink"])
            sel.open(testvars.MCTestVariables["TestSite"])
            sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])
            # Log out
            loginlogout.LogOut(self,sel)
            # Submit a video and check the results
            submitvideos.SubmitVideo(self, sel, testVideoURL, theme, "UnloggedUser")  # as Admin 
            # Log in as Administrator
            loginlogout.LogInAsAdmin(self,sel)
            # Check if the video is in the premoderation queue ("Unapproved") 
            # If yes, reject it
            print titleUnicode
            queue.RejectVideoFromQueue(self,sel,titleUnicode)            

# Close the browser, log errors, perform cleanup    
    def tearDown(self):
        self.selenium.stop()
# the command on the previous line should close the browser
        self.assertEqual([], self.verificationErrors)


class TestCase_SubmitVideoFromAdminPage_474(unittest.TestCase):
    
# Open the desired browser and set up the test
    def setUp(self):
        self.verificationErrors = []
        self.selenium = selenium("localhost", testvars.MCTestVariables["Port"], testvars.MCTestVariables["Browser"], testvars.MCTestVariables["TestSite"])
        self.selenium.start()

# The user actions executed in the test scenario
    def test_SubmitVideoFromAdminPage_474(self):
        sel = self.selenium
        # Log in as an Administrator
        loginlogout.LogInAsAdmin(self,sel)
        theme = 0 # Admin interface
        # Set video parameters
        testVideoURL = "http://www.youtube.com/watch?v=QIQwMwesb0w"
        testVideoTitle = "Miro Demo"
        titleUnicode = unicode(testVideoTitle)
        # Check if the video is in the premoderation queue ("Unapproved") 
        # If yes, reject it
        queue.RejectVideoFromQueue(self,sel,titleUnicode)            
        # Navigate to the front page
#        sel.click(testvars.MCTestVariables["ViewMainSiteLink"])
        sel.open(testvars.MCTestVariables["TestSite"])
        sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])
        # Check if the video is in the current ("Approved") set of videos
        # If yes, delete it
        submitvideos.RejectVideoFromApproved(self,sel,testVideoTitle)
        # Submit a video and check the results
        submitvideos.SubmitVideo(self, sel, testVideoURL, theme, "Admin")  # as Admin 


# Close the browser, log errors, perform cleanup    
    def tearDown(self):
        self.selenium.stop()
# the command on the previous line should close the browser
        self.assertEqual([], self.verificationErrors)


class TestCase_SubmitDuplicateVideo_475(unittest.TestCase):
    
# Open the desired browser and set up the test
    def setUp(self):
        self.verificationErrors = []
        self.selenium = selenium("localhost", testvars.MCTestVariables["Port"], testvars.MCTestVariables["Browser"], testvars.MCTestVariables["TestSite"])
        self.selenium.start()

    def ChangeThemeAndSubmitDuplicateVideo(self,sel,theme,testVideoURL):
        print "Changing theme "+str(theme)
        sitesettings.ChangeTheme(self,sel,theme)
#        sel.click(testvars.MCTestVariables["ViewMainSiteLink"])
        sel.open(testvars.MCTestVariables["TestSite"])
        sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])
        loginlogout.LogOut(self,sel)
        # Submit a video and check the results
        submitvideos.SubmitDuplicateVideo(self, sel, testVideoURL, theme)
        loginlogout.LogInAsAdmin(self,sel)
    
# The user actions executed in the test scenario
    def test_SubmitDuplicateVideo_475(self):
        sel = self.selenium
        # Log in as an Administrator
        loginlogout.LogInAsAdmin(self,sel)
        theme = 1 # List theme
        sitesettings.ChangeTheme(self,sel,theme)
        sitesettings.UncheckRequireLoginToSubmitVideo(self,sel)
        # Set video parameters
        testVideoURL = "http://www.youtube.com/watch?v=QIQwMwesb0w"
        testVideoTitle = "Miro Demo"
        titleUnicode = unicode(testVideoTitle)
        # Check if the video is in the premoderation queue ("Unapproved")
        print "Looking for the video "+testVideoTitle+" in the premoderation queue"
        if queue.FindVideoInQueue(self,sel,testVideoTitle)!=[0,0]:
            print "Found the video in the premoderation queue"
            for theme in range(1,2):
                TestCase_SubmitDuplicateVideo_475.ChangeThemeAndSubmitDuplicateVideo(self,sel,theme,testVideoURL)
        else:
            print "Could not find the video in the premoderation queue"
            # Check if the video is in the current ("Approved") set of videos
            if queue.CheckVideoStatus(self,sel,testVideoTitle,"Approved")==False:
                print "Could not find the video among the approved videos"
                self.fail("The test case demands that a copy of the video already existed in the system. Cannot continue now.")
            else:
                print "Found the video among the approved videos"
                for theme in range(1,2):
                    TestCase_SubmitDuplicateVideo_475.ChangeThemeAndSubmitDuplicateVideo(self,sel,theme,testVideoURL)

# Close the browser, log errors, perform cleanup    
    def tearDown(self):
        self.selenium.stop()
# the command on the previous line should close the browser
        self.assertEqual([], self.verificationErrors)


class TestCase_SubmitVideoWithEmbedCode_476(unittest.TestCase):
    
# Open the desired browser and set up the test
    def setUp(self):
        self.verificationErrors = []
        self.selenium = selenium("localhost", testvars.MCTestVariables["Port"], testvars.MCTestVariables["Browser"], testvars.MCTestVariables["TestSite"])
        self.selenium.start()

# The user actions executed in the test scenario
    def test_SubmitVideoWithEmbedCode_476(self):
        sel = self.selenium
        # Log in as an Administrator
        loginlogout.LogInAsAdmin(self,sel)
        theme = 1 # List theme
        role = "Admin"
        sitesettings.ChangeTheme(self,sel,theme)
        # Display 'Submit a Video' button on front page
        sitesettings.DisplaySubmitVideo(self,sel,theme)
#        sitesettings.UncheckRequireLoginToSubmitVideo(self,sel)
        # Set video parameters
        testVideoURL = "http://www.veoh.com/browse/videos/category/technology/watch/v6574185k5jF5K4E"
        testVideoTitle = "Veoh Video for Test"
        testVideoEmbedCode = r'<object width="410" height="341" id="veohFlashPlayer" name="veohFlashPlayer"><param name="movie" '
        testVideoEmbedCode = testVideoEmbedCode + r'value="http://www.veoh.com/static/swf/webplayer/WebPlayer.swf?version='
        testVideoEmbedCode = testVideoEmbedCode + r'AFrontend.5.5.2.1048&permalinkId=v6574185k5jF5K4E&player=videodetailsembedded&'
        testVideoEmbedCode = testVideoEmbedCode + r'videoAutoPlay=0&id=anonymous"></param><param name="allowFullScreen" value="true">'
        testVideoEmbedCode = testVideoEmbedCode + r'</param><param name="allowscriptaccess" value="always"></param><embed '
        testVideoEmbedCode = testVideoEmbedCode + r'src="http://www.veoh.com/static/swf/webplayer/WebPlayer.swf?version='
        testVideoEmbedCode = testVideoEmbedCode + r'AFrontend.5.5.2.1048&permalinkId=v6574185k5jF5K4E&player=videodetailsembedded&'
        testVideoEmbedCode = testVideoEmbedCode + r'videoAutoPlay=0&id=anonymous" type="application/x-shockwave-flash" allowscriptaccess="always"'
        testVideoEmbedCode = testVideoEmbedCode + r'allowfullscreen="true" width="410" height="341" id="veohFlashPlayerEmbed"'
        testVideoEmbedCode = testVideoEmbedCode + r' name="veohFlashPlayerEmbed"></embed></object><br /><font size="1">Watch '
        testVideoEmbedCode = testVideoEmbedCode + r'<a href="http://www.veoh.com/browse/videos/category/technology/watch/v6574185k5jF5K4E">'
        testVideoEmbedCode = testVideoEmbedCode + r'Online Video Distribution Miro Co-Branded Player Offer</a> in '
        testVideoEmbedCode = testVideoEmbedCode + r'<a href="http://www.veoh.com/browse/videos/category/technology">Technology'
        testVideoEmbedCode = testVideoEmbedCode + r'</a>&nbsp;&nbsp;|&nbsp;&nbsp;View More <a href="http://www.veoh.com">Free Videos Online at Veoh.com'
        testVideoEmbedCode = testVideoEmbedCode + r'</a></font>'
        testVideoThumbfile = '' #r'D:\TestInput\background1.jpg'
        testVideoThumbURL = 'http://ll-appserver.veoh.com/images/veoh.gif?version=AFrontend.5.5.2.1055'
        testVideoDescription = 'test description for a Veoh video with embed code'
        testVideoTags = 'test veoh'
        titleUnicode = unicode(testVideoTitle)
        # Check if the video is in the premoderation queue ("Unapproved") 
        # If yes, reject it
        queue.RejectVideoFromQueue(self,sel,titleUnicode)            
        # Navigate to the front page
#        sel.click(testvars.MCTestVariables["ViewMainSiteLink"])
        sel.open(testvars.MCTestVariables["TestSite"])
        sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])
        for theme in range(1,2):
            print ""
            print "The current theme is "+str(theme)
            # Check if the video is in the current ("Approved") set of videos
            # If yes, delete it
            submitvideos.RejectVideoFromApproved(self,sel,testVideoTitle)
            # Set the theme
            sitesettings.ChangeTheme(self,sel,theme)
            # Navigate to the front page
#            sel.click(testvars.MCTestVariables["ViewMainSiteLink"])
            sel.open(testvars.MCTestVariables["TestSite"])
            sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])
            # Submit a video and check the results
            submitvideos.SubmitVideoWithEmbed(self,sel,testVideoURL,testVideoTitle,testVideoEmbedCode,testVideoThumbfile,testVideoThumbURL,testVideoDescription,testVideoTags, theme, role)

# Close the browser, log errors, perform cleanup    
    def tearDown(self):
        self.selenium.stop()
# the command on the previous line should close the browser
        self.assertEqual([], self.verificationErrors)
