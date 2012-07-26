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
#     8. TestCase_EditAuthor_573
#     9. TestCase_EditDescription_574
#     10. TestCase_EditCategory_575
#     11. TestCase_EditTags_576
#     12. TestCase_EditWebsite_577
#     13. TestCase_AddEditorsComment_578
#     14. TestCase_PostToFacebook_579
#     15. TestCase_PostToTwitter_580
#     16. TestCase_EmailToFriends_581
#     17. TestCase_AddToPlaylist_582
#     18. TestCase_DeleteComment_583


from selenium import selenium
from email.parser import HeaderParser
import imaplib
import unittest, os, time, re, mclib, testcase_base
# import urllib, Image, ImageChop
import loginlogout, sitesettings, testvars, categories, submitvideos, sitesettings, queue, videopage,  bulkedit, testcases_comments
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
        for theme in range(1,2):
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
        for theme in range(1,2):
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
        for theme in range(1,2):
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
        for theme in range(1,2):
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
        for theme in range(1,3):
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
        for theme in range(1,2):
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
        for theme in range(1,2):
            print ""
            print "============================================"
            print ""
            print "Running Edit Publication Date Inline test with theme: "+str(theme)
            print "Changing theme..."
            sitesettings.ChangeTheme(self,sel,theme)
            TestCase_EditPublicationDate_572.EditPublicationDate(self,sel,theme)



class TestCase_EditAuthor_573(testcase_base.testcase_BaseTestCase):
    
    def EditAuthor(self, sel, theme):
        # Selecting video No. <theme> from New Videos listing
        videoTitleLink = videopage.PickVideoFromNewVideosListingPage(self, sel, theme)
        videoTitle=sel.get_text(videoTitleLink)
        print "Opening video page for video "+videoTitle+"..."
        sel.click(videoTitleLink)
        sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])
        # The current author for the video will be replaced with a test user
        newAuthor = testvars.MCTestVariables["UserName"]
        print "Replacing the existing date with "+newAuthor
        videopage.InlineEditAuthor(self,sel,theme,newAuthor)

    def test_EditAuthor(self):
        sel = self.selenium
#       Log in as Admin
        loginlogout.LogInAsAdmin(self,sel)
        for theme in range(1,2):
            print ""
            print "============================================"
            print ""
            print "Running Edit Author test with theme: "+str(theme)
            print "Changing theme..."
            sitesettings.ChangeTheme(self,sel,theme)
            TestCase_EditAuthor_573.EditAuthor(self,sel,theme)



class TestCase_EditDescription_574(testcase_base.testcase_BaseTestCase):
    
    def EditDescription(self, sel, theme):
        # Selecting video No. <theme> from New Videos listing
        videoTitleLink = videopage.PickVideoFromNewVideosListingPage(self, sel, theme)
        videoTitle=sel.get_text(videoTitleLink)
        print "Opening video page for video "+videoTitle+"..."
        sel.click(videoTitleLink)
        sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])
        
        newDescription = r'<h1>Advantages of Miro Community</h1><ul><li>Run a beautiful video '
        newDescription = newDescription + 'presentation website on your own domain, without having to maintain the software.</li>'
        newDescription = newDescription + '<li>Works with your existing video hosting setup and workflow - no need to re-post '
        newDescription = newDescription + 'videos.</li> <li>Works with free video hosting services, if you do not already have '
        newDescription = newDescription + 'videos online.</li> <li>Lets you bring together videos from a wide-variety of hosts and '
        newDescription = newDescription + 'sources, into one curated experience.</li><li>Automatically import and publish RSS feeds '
        newDescription = newDescription + 'of videos from any source.</li> <li>Create a discussion space for video about your '
        newDescription = newDescription + 'community; strengthen your relationships with your community.</li><li>Runs on open-source '
        newDescription = newDescription + 'software.</li></ul>'
#        newDescription = 'test Oct7'
        print "Updating the description with the following text: "
        print newDescription
        videopage.InlineEditDescription(self,sel,theme,newDescription)

    def test_EditDescription(self):
        sel = self.selenium
#       Log in as Admin
        loginlogout.LogInAsAdmin(self,sel)
        sitesettings.ChangeTheme(self,sel,theme=1)
        TestCase_EditDescription_574.EditDescription(self,sel,theme)



class TestCase_EditCategory_575(testcase_base.testcase_BaseTestCase):
    
    def EditCategory(self, sel, theme):
        # Selecting video No. <theme> from New Videos listing
        videoTitleLink = videopage.PickVideoFromNewVideosListingPage(self, sel, theme=1)
        videoTitle=sel.get_text(videoTitleLink)
        print "Opening video page for video "+videoTitle+"..."
        sel.click(videoTitleLink)
        sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])
        newCategory = testvars.newCategories[theme-1]
        print "Changing the category to: "+newCategory
        videopage.InlineEditCategory(self,sel,theme,newCategory)

    def test_EditCategory(self):
        sel = self.selenium
#       Log in as Admin
        loginlogout.LogInAsAdmin(self,sel)
        sitesettings.ChangeTheme(self,sel,theme=1)
        TestCase_EditCategory_575.EditCategory(self,sel,theme=1)



class TestCase_EditTags_576(testcase_base.testcase_BaseTestCase):
    
    def EditTags(self, sel, theme):
        # Selecting video No. <theme> from New Videos listing
        videoTitleLink = videopage.PickVideoFromNewVideosListingPage(self, sel, theme)
        videoTitle=sel.get_text(videoTitleLink)
        print "Opening video page for video "+videoTitle+"..."
        sel.click(videoTitleLink)
        sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])
        newTag = "TestWithTheme"+str(theme)
        print "Changing the tag to: "+newTag
        videopage.InlineEditTags(self,sel,theme,newTag)

    def test_EditTags(self):
        sel = self.selenium
#       Log in as Admin
        loginlogout.LogInAsAdmin(self,sel)
        for theme in range(1,2):
            print ""
            print "============================================"
            print ""
            print "Running Edit Tags test with theme: "+str(theme)
            print "Changing theme..."
            sitesettings.ChangeTheme(self,sel,theme)
            TestCase_EditTags_576.EditTags(self,sel,theme)


class TestCase_EditWebsite_577(testcase_base.testcase_BaseTestCase):
    
    def EditWebsite(self, sel, theme):
        # Selecting video No. <theme> from New Videos listing
        videoTitleLink = videopage.PickVideoFromNewVideosListingPage(self, sel, theme)
        videoTitle=sel.get_text(videoTitleLink)
        print "Opening video page for video "+videoTitle+"..."
        sel.click(videoTitleLink)
        sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])
        newWebsite = "http://www.mirocommunity.org/"
        print "Changing the website to: "+newWebsite
        videopage.InlineEditWebsite(self,sel,theme,newWebsite)

    def test_EditWebsite(self):
        sel = self.selenium
#       Log in as Admin
        loginlogout.LogInAsAdmin(self,sel)
        for theme in range(1,2):
            print ""
            print "============================================"
            print ""
            print "Running Edit Website test with theme: "+str(theme)
            print "Changing theme..."
            sitesettings.ChangeTheme(self,sel,theme)
            TestCase_EditWebsite_577.EditWebsite(self,sel,theme)



class TestCase_AddEditorsComment_578(testcase_base.testcase_BaseTestCase):
    
    def test_AddEditorsComment(self):
        sel = self.selenium
#       Log in as Admin
        loginlogout.LogInAsAdmin(self,sel)
        theme = 4 # The feature is available for Blue theme only
        print "Changing theme..."
        sitesettings.ChangeTheme(self,sel,theme)
        # Selecting video No. <theme> from New Videos listing
        videoTitleLink = videopage.PickVideoFromNewVideosListingPage(self, sel, theme)
        videoTitle=sel.get_text(videoTitleLink)
        print "Opening video page for video "+videoTitle+"..."
        sel.click(videoTitleLink)
        sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])
#        newEditorsComment = "<b>TEST</b>"
        newEditorsComment = r"<p><b>Why use MiroCommunity?</b></p>"
        newEditorsComment = newEditorsComment + "<p><b><i>Leverage Existing Video</i></b> Your community already has "
        newEditorsComment = newEditorsComment + "a LOT of relevant video floating around on the internet. "
        newEditorsComment = newEditorsComment + "<b>Miro Community</b> can aggregate it all in one central location. "
        newEditorsComment = newEditorsComment + "Videos can be created by you or your organization, but can also easily "
        newEditorsComment = newEditorsComment + "be brought in from a broader pool of creators. Videos can come from "
        newEditorsComment = newEditorsComment + "YouTube, blip.tv, Vimeo, or almost any video blog or site powered by "
        newEditorsComment = newEditorsComment + "drupal, plone, or other CMS that creates a media RSS feed.</p>"
        newEditorsComment = newEditorsComment + "<b><i>A Video-Centric Approach</i></b> Put video front and center. The most successful "
        newEditorsComment = newEditorsComment + "video sites are centered around the videos; for example, <a href='www.youtube."
        newEditorsComment = newEditorsComment + "com'>YouTube</a>, Hulu, and the TED conference. These sites have regular "
        newEditorsComment = newEditorsComment + "viewers/visitors who come expecting entertainment, enrichment, and engagement. "
        newEditorsComment = newEditorsComment + "Miro Community makes video easy to find, and lets you point people directly "
        newEditorsComment = newEditorsComment + "to the content they are looking for.</p>"
        print "Posting the Editor's comment: "+newEditorsComment
        videopage.PostEditorsComment(self,sel,newEditorsComment)



class TestCase_PostToFacebook_579(testcase_base.testcase_BaseTestCase):
    
    def PostToFacebook(self, sel, theme):
        # Selecting video No. <theme> from New Videos listing
        videoTitleLink = videopage.PickVideoFromNewVideosListingPage(self, sel, theme)
        videoTitle=sel.get_text(videoTitleLink)
        print "Opening video page for video "+videoTitle+"..."
        sel.click(videoTitleLink)
        sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])
        print "Posting the video on Facebook..."
        videopage.PostToFacebook(self,sel,theme, videoTitle)

    def test_PostToFacebook(self):
        sel = self.selenium
#       Log in to Facebook
        loginlogout.LogInToFacebook(self,sel)
#       Log in as Admin
        loginlogout.LogInAsAdmin(self,sel)
        for theme in range(1,2):
            print ""
            print "============================================"
            print ""
            print "Running Post to Facebook test with theme: "+str(theme)
            print "Changing theme..."
            sitesettings.ChangeTheme(self,sel,theme)
            TestCase_PostToFacebook_579.PostToFacebook(self,sel,theme)



class TestCase_PostToTwitter_580(testcase_base.testcase_BaseTestCase):
    
    def PostToTwitter(self, sel, theme):
        # Selecting video No. <theme> from New Videos listing
        videoTitleLink = videopage.PickVideoFromNewVideosListingPage(self, sel, theme)
        videoTitle=sel.get_text(videoTitleLink)
        print "Opening video page for video "+videoTitle+"..."
        sel.click(videoTitleLink)
        sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])
        print "Posting the video on Twitter..."
        videopage.PostToTwitter(self,sel,theme)

    def test_PostToTwitter(self):
        sel = self.selenium
        print "Logging in to Twitter..."
        loginlogout.LogInToTwitter(self,sel)
#        sel.click("link=PCFQA")
        sel.open("https://twitter.com/#!/PCFQA")
        time.sleep(15)
        print "OK"
        buttonDelete = "css=div.js-stream-item:nth-child(1) div.stream-item-content div.tweet-content div.tweet-row span.tweet-actions a.delete-action"
        # Twitter forbids repetitive identical tweets, so older test tweets will be erased before the test starts to avoid duplication
        print "Searching for old test tweets..."
        while sel.is_text_present("TEST TWEET"):
            sel.click(buttonDelete)
            time.sleep(1)
            if sel.is_visible("css=div.twttr-prompt"):
                sel.click("css=div.js-prompt-ok")
                time.sleep(3)
                print "Deleted old test tweet"
                sel.refresh()
                time.sleep(5)
        print "Done"
#       Log in as Admin
        loginlogout.LogInAsAdmin(self,sel)
        for theme in range(1,2):
            print ""
            print "============================================"
            print ""
            print "Running Post to Twitter test with theme: "+str(theme)
            print "Changing theme..."
            sitesettings.ChangeTheme(self,sel,theme)
            TestCase_PostToTwitter_580.PostToTwitter(self,sel,theme)



class TestCase_EmailToFriends_581(testcase_base.testcase_BaseTestCase):
    
    def EmailToFriends(self, sel, theme):
        # Selecting video No. <theme> from New Videos listing
        videoTitleLink = videopage.PickVideoFromNewVideosListingPage(self, sel, theme)
        videoTitle=sel.get_text(videoTitleLink)
        print "Opening video page for video "+videoTitle+"..."
        sel.click(videoTitleLink)
        sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])
        videoPageURL = sel.get_location()
        print "Mailing the link to video to friends..."
        videopage.EmailToFriends(self,sel,theme,testvars.MCTestVariables["TestEmail"])
        time.sleep(10)
        print "Checking the last email in the inbox..."
        mailUser = testvars.MCTestVariables["TestEmail"]
        mailPassword = testvars.MCTestVariables["TestEmailPassword"]
        mail = imaplib.IMAP4_SSL('imap.gmail.com', 993)
        mail.login(mailUser, mailPassword)
        mail.select('Inbox')
        result, data = mail.search(None, "ALL")
        ids = data[0] # data is a list.
        id_list = ids.split() # ids is a space separated string
        latest_email_id = id_list[-1] # get the latest
        result, data = mail.fetch(latest_email_id, "(RFC822)") # fetch the email body (RFC822) for the given ID
        emailHeader = HeaderParser().parsestr(data[0][1])
        print "Email sender: " + emailHeader['From']
        print "Email subject: " + emailHeader['Subject']
        if emailHeader['From'] != "Miro Community <mirocommunity@pculture.org>":
            mclib.AppendErrorMessage(self,sel,"Unexpected mail sender found")
        elif not(videoTitle in data[0][1]):
            mclib.AppendErrorMessage(self,sel,"Video title not found in email")
            print "Video title: "+videoTitle
            print data[0][1]
#        elif not('href=3D"'+videoPageURL+'"' in data[0][1]):
#        elif not(videoPageURL in data[0][1]):
#            mclib.AppendErrorMessage(self,sel,"Link to video not found")
#            print "Link to video: "+videoPageURL
#            print data[0][1]
        else:
            print "OK"
#        print 'Message %s\n%s\n' % (latest_email_id, data[0][1])
        mail.close()
        mail.logout()        
        
    def test_EmailToFriends(self):
        sel = self.selenium
#       Log in as Admin
        loginlogout.LogInAsAdmin(self,sel)
        for theme in range(1,2):
            print ""
            print "============================================"
            print ""
            print "Running Email To Friends test with theme: "+str(theme)
            print "Changing theme..."
            sitesettings.ChangeTheme(self,sel,theme)
            TestCase_EmailToFriends_581.EmailToFriends(self,sel,theme)



class TestCase_AddToPlaylist_582(testcase_base.testcase_BaseTestCase):
    
    def AddToPlaylist(self, sel, theme):
        # Selecting video No. <theme> from New Videos listing
        videoTitleLink = videopage.PickVideoFromNewVideosListingPage(self, sel, theme)
        videoTitle=sel.get_text(videoTitleLink)
        print "Opening video page for video "+videoTitle+"..."
        sel.click(videoTitleLink)
        sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])
        playlist = "Test "+str(theme)+" "+time.strftime("%d-%m-%Y %H:%M:%S", time.localtime())
        print "Adding the video to playlist "+playlist+"..."
        videopage.AddToPlaylist(self,sel,theme, playlist)

    def test_AddToPlaylist(self):
        sel = self.selenium
#       Log in as Admin
        loginlogout.LogInAsAdmin(self,sel)
        # Ensure that playlists are enabled
        sitesettings.EnablePlaylists(self,sel,"Yes")
        for theme in range(1,2):
            print ""
            print "============================================"
            print ""
            print "Running Add to Playlist test with theme: "+str(theme)
            print "Changing theme..."
            sitesettings.ChangeTheme(self,sel,theme)
            TestCase_AddToPlaylist_582.AddToPlaylist(self,sel,theme)


class TestCase_DeleteComment_583(testcase_base.testcase_BaseTestCase):
    
    def DeleteComment(self, sel, theme):
        # Selecting video No. <theme> from New Videos listing
        videoTitleLink = videopage.PickVideoFromNewVideosListingPage(self, sel, theme)
        videoTitle=sel.get_text(videoTitleLink)
        print "Opening video page for video "+videoTitle+"..."
        sel.click(videoTitleLink)
        sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])
        temp_comment = testcases_comments.generateComment()
        print "Posting a test comment..."
        videopage.PostComment(self,sel,theme,temp_comment)
        print "Deleting the test comment"
        videopage.DeleteComment(self,sel,theme,temp_comment)

    def test_DeleteComment(self):
        sel = self.selenium
#       Log in as Admin
        loginlogout.LogInAsAdmin(self,sel)
        for theme in range(1,2):
            print ""
            print "============================================"
            print ""
            print "Running Delete Comment test with theme: "+str(theme)
            print "Changing theme..."
            sitesettings.ChangeTheme(self,sel,theme)
            TestCase_DeleteComment_583.DeleteComment(self,sel,theme)
