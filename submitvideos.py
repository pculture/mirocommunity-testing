# Module SUBMITVIDEOS.PY
# includes:
#   * function CheckTextPresent(self, sel, Text1, Time1, ErrorText1) - checks for text Text1
#              during Time1 seconds and prints error ErrorText1 if not found
#   * function CheckTextNotPresent(self, sel, Text1, Time1, ErrorText1) - checks for text Text1
#              during Time1 seconds and prints error ErrorText1 if it is found
#   * subroutine SubmitVideo(self, sel, video_url, theme, role) - submits an individual video with
#                <video_url>. <theme> can take values between 0 and 4 (0 - Admin interface,
#                1 - List, 2 - Scrolling, 3 - Category, 4 - Blue)
#                <role> defines the privileges of the virtual user; can take values "Admin",
#                "LoggedUser", "UnloggedUser"
#   * subroutine SubmitDuplicateVideo(self, sel, video_url, theme) - attempts to submit a
#                duplicate video with <video_url> identical to the URL of another video, already
#                approved or awaiting moderaton in the system.
#                <theme> can take values between 1 and 4 (1 - List, 2 - Scrolling, 3 - Category,
#                4 - Blue)
#   * subroutine SubmitVideoWithEmbed(self, sel, video_url, video_title, video_embed, video_thumbfile,
#                video_thumbURL, video_description, video_tags, theme, role) - submits an individual
#                video in a custom format that requires the use of an embed code with <video_url>.
#                <video_title> - any string identifier
#                <video_embed> - embed code for the video
#                <video_thumbfile> - file name and path for thumbnail image
#                <video_thumbURL> - URL for custom thumbnail image
#                <theme> can take values between 1 and 4 (1 - List, 2 - Scrolling, 3 - Category, 4 - Blue)
#   * subroutine RejectVideoFromApproved(self,sel,title) - checks if the video being submitted
#                is in the current ("Approved") set of videos
#                If yes, deletes it

from selenium import selenium

import unittest, time, re, loginlogout 
import testvars, mclib, queue


def CheckTextPresent(self, sel, Text1, Time1, ErrorText1):
     print "Check Text Present: "+str(Text1)
     for i in range(Time1):
         t1=i
         if sel.is_text_present(Text1):
             #print "Text found in "+str(t1)+" sec"
             return True
         time.sleep(1)
     print "ERROR: Text not found in "+str(t1)+" sec. " + ErrorText1
     return False

def CheckTextNotPresent(self, sel, Text1, Time1, ErrorText1):
     print "Check Text Not Present: "+str(Text1)
     for i in range(Time1):
         t1=i
         if sel.is_text_present(Text1):
             print "Text found: "+str(ErrorText1)
             return 0
         time.sleep(1)
     #print "Text not found in "+str(t1)+" sec. "
     return 1



# =======================================
# =             SUBMIT VIDEO            =
# =======================================

# This subroutine submits an individual Youtube/Vimeo video with <video_url>.
# <theme> can take values between 0 and 4 (0 - Admin interface,1 - List, 2 - Scrolling, 3 - Category, 4 - Blue)
# <role> defines the privileges of the virtual user; can take values "Admin", "LoggedUser",
# "UnloggedUser"
        
def SubmitVideo(self, sel, video_url, theme, role):
    if role!="Admin" and role!="LoggedUser" and role!="UnloggedUser":
        self.fail("Wrong value of role parameter passed to SubmitVideo subroutine")
    else:
        print "preparing to submit video: " +str(video_url)+"..."
        if theme==0: # Admin interface
            submitVideoButton = "//a[@href='/submit_video/']"
        elif theme==4: # Blue theme
            submitVideoButton = "//div[@id='nav']/ul/li[6]/a"
        else: # Any other front page theme
            submitVideoButton = "//ul[@id='nav']/li[6]/a/span"
        print "Checking if 'Submit Video' button is accessible..."
        if sel.is_element_present(submitVideoButton)==False:
            mclib.AppendErrorMessage(self,sel,"Could not find 'Submit Video' button")
        else:
            print "OK. Clicking the button..."
            sel.click(submitVideoButton)
            if CheckTextPresent(self, sel, "Enter the URL of your video", 30, "Time out")==False:
                mclib.AppendErrorMessage(self,el,"Could not find the prompt to enter the video URL")
            else:
                "OK. Entering the video URL..."
                sel.type("id_url", video_url)
                sel.click("//input[@value='Submit']")
                time.sleep(5)
                # Retrieving and storing video attributes
                if sel.is_text_present('That video has already been submitted!'):
                    mclib.AppendErrorMessage(self,sel,'Duplication occurred - the video is already in the system (approved or awaiting moderation)')
                elif sel.is_element_present('submit_video')==False:
                    mclib.AppendErrorMessage(self,sel,"Could not find the expected pop-up with the video attributes")
                else:
                    print "OK. Reading the video attributes..."
                    if sel.is_element_present("//form[@id='submit_video']/table/tbody/tr[1]/td/div/h2/a"):
                        video_title = sel.get_text("//form[@id='submit_video']/table/tbody/tr[1]/td/div/h2/a")
                        print "Title: "+video_title
                    if sel.is_element_present("//form[@id='submit_video']/table/tbody/tr[1]/td/div/span/span[1]"):
                        video_author = sel.get_text("//form[@id='submit_video']/table/tbody/tr[1]/td/div/span/span[1]")
                        print "Author: "+video_author
                    if sel.is_element_present("//form[@id='submit_video']/table/tbody/tr[1]/td/div/span/span[2]"):
                        video_date = sel.get_text("//form[@id='submit_video']/table/tbody/tr[1]/td/div/span/span[2]")
                        print "Date: "+ video_date
                    if sel.is_element_present("//form[@id='submit_video']/table/tbody/tr[1]/td/div/div[1]"):
                        video_tags = sel.get_text("//form[@id='submit_video']/table/tbody/tr[1]/td/div/div[1]")
                        print "Tags: "+video_tags
                    if sel.is_element_present("//form[@id='submit_video']/table/tbody/tr[1]/td/div/div[2]"):
                        video_description = sel.get_text("//form[@id='submit_video']/table/tbody/tr[1]/td/div/div[2]")
                        print "Description: "+video_description
#                if CheckTextPresent(self, sel, "You can also optionally add tags for the video (below).", 30, "ERROR: Time out")==False:
#                    mclib.AppendErrorMessage(self,sel,"Could not find the option to add tags for the video being submitted")
                    print "Now uploading the video..."
                    sel.click("//input[@value='Submit']")
                    # Checking that the video was submitted correctly
                    print "Checking that the video was submitted correctly..."
                    if role!="Admin":
                        time.sleep(8)
                        #checkMessage = CheckTextPresent(self, sel, "Thanks for submitting a video, our moderators will review it soon.", 30, "Moderation message not found")
                        if sel.is_text_present("Thanks for submitting a video, our moderators will review it soon.")==False:
                            mclib.AppendErrorMessage(self,sel,"Could not find the message: 'Thanks for submitting a video, our moderators will review it soon'")
                            
                        else:
                            sel.click("//div[@id='overlay']/div[1]")
                            time.sleep(2)
                            loginlogout.LogOut(self,sel)
                            loginlogout.LogInAsAdmin(self,sel)
                            print "Looking for the submitted video in the review queue..."
                            if queue.FindVideoInQueue(self,sel,video_title)==[0,0]:
                                mclib.AppendErrorMessage(self,sel,"Submitted video not found in the review queue")
                            else:
                                print "OK"
                    else: # for Admin
                        sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])
                        video_tags_list = ((video_tags.replace('Tags: ','')).lower()).split(', ')
#                print video_tags_list
#                print [x for x in video_tags_list if sel.is_text_present(x)==True]
                        if sel.is_element_present("//a[text()='"+video_url+"']")==False and sel.is_element_present("//a[@href='"+video_url+"']")==False:
                            mclib.AppendErrorMessage(self,sel,"Link to original video not found")
                        elif sel.is_text_present(video_title)==False:
                            mclib.AppendErrorMessage(self,sel,"Video TITLE not found")
                        elif sel.is_text_present(video_author)==False:
                            mclib.AppendErrorMessage(self,sel,"Video AUTHOR not found")
                        elif video_tags_list!=[x for x in video_tags_list if sel.is_text_present(x)==True]:
                    # (Checking if every element of the list is present on the web page)
                            mclib.AppendErrorMessage(self,sel,"Video TAGS not found")
                        elif sel.is_text_present(video_description)==False:
                            mclib.AppendErrorMessage(self,sel,"Video DESCRIPTION not found")
                        else:
                            print "OK"



# =======================================
# =       SUBMIT DUPLICATE VIDEO        =
# =======================================

# This subroutine attempts to submit a duplicate video with <video_url> identical to the URL
# of another video, already approved or awaiting moderaton in the system.
# <theme> can take values between 1 and 4 (1 - List, 2 - Scrolling, 3 - Category, 4 - Blue)
        
def SubmitDuplicateVideo(self, sel, video_url, theme):
    print "Attempting to submit video: " +str(video_url)+"..."
    if theme==4: # Blue theme
        submitVideoButton = "//div[@id='nav']/ul/li[6]/a"
    else: # Any other front page theme
        submitVideoButton = "//ul[@id='nav']/li[6]/a/span"
    print "Checking if 'Submit Video' button is accessible..."
    if sel.is_element_present(submitVideoButton)==False:
        mclib.AppendErrorMessage(self,sel,"Could not find 'Submit Video' button")
    else:
        print "OK. Clicking the button..."
        sel.click(submitVideoButton)
        if CheckTextPresent(self, sel, "Enter the URL of your video", 30, "Time out")==False:
            mclib.AppendErrorMessage(self,sel,"Could not find the prompt to enter the video URL")
        else:
            print "OK. Entering the video URL..."
            sel.type("id_url", video_url)
            print "Now trying to actually submit the video..."
            sel.click("//input[@value='Submit']")
            time.sleep(5)
            # Retrieving and storing video attributes
            if sel.is_text_present('That video has already been submitted!')==False:
                mclib.AppendErrorMessage(self,sel,'Expected error message on video duplicaton not found')
            else:
                sel.click("//div[@id='overlay']/div[1]")
                alertText = sel.get_text("//form[@id='submit_video']/div[2]")
                print "Message text: "
                print alertText
                print "OK - the submission attempt was rejected as expected"



# =======================================
# =     SUBMIT VIDEO WITH EMBED CODE    =
# =======================================

# This subroutine submits an individual video in a custom format that requires the use of an embed code
# with <video_url>.
# <video_title> - any string identifier
# <video_embed> - embed code for the video
# <video_thumbfile> - file name and path for thumbnail image
# <video_thumbURL> - URL for custom thumbnail image
# <theme> can take values between 1 and 4 (1 - List, 2 - Scrolling, 3 - Category, 4 - Blue)
# <role> defines the privileges of the virtual user; can take values "Admin", "LoggedUser",
# "UnloggedUser"
        
def SubmitVideoWithEmbed(self, sel, video_url, video_title, video_embed, video_thumbfile, video_thumbURL, video_description, video_tags, theme, role):
    if role!="Admin" and role!="LoggedUser" and role!="UnloggedUser":
        self.fail("Wrong value of role parameter passed to SubmitVideoWithEmbed subroutine")
    else:
        print "preparing to submit video: " +str(video_url)+"..."
        if theme==0: # Admin interface
            submitVideoButton = "//a[@href='/submit_video/']"
        elif theme==4: # Blue theme
            submitVideoButton = "//div[@id='nav']/ul/li[6]/a"
        else: # Any other front page theme
            submitVideoButton = "//ul[@id='nav']/li[6]/a/span"
        print "Checking if 'Submit Video' button is accessible..."
        if sel.is_element_present(submitVideoButton)==False:
            mclib.AppendErrorMessage(self,sel,"Could not find 'Submit Video' button")
        else:
            print "OK. Clicking the button..."
            sel.click(submitVideoButton)
            if CheckTextPresent(self, sel, "Enter the URL of your video", 30, "Time out")==False:
                mclib.AppendErrorMessage(self,el,"Could not find the prompt to enter the video URL")
            else:
                "OK. Entering the video URL..."
                sel.type("id_url", video_url)
                sel.click("//input[@value='Submit']")
                time.sleep(5)
                # Retrieving and storing video attributes
                if sel.is_text_present('That video has already been submitted!'):
                    mclib.AppendErrorMessage(self,sel,'Duplication occurred - the video is already in the system (approved or awaiting moderation)')
                elif sel.is_element_present('submit_video')==False:
                    mclib.AppendErrorMessage(self,sel,"Could not find the expected pop-up with the video attributes")
                else:
                    print "OK. Entering the video attributes and embed code..."
                    # Entering Video Name (mandatory field)
                    if sel.is_element_present("id_name")==False:
                        mclib.AppendErrorMessage(self,sel,"Input field for Video Name not found")
                    else:
                        print "Typing the name of the video file..."
                        sel.type("id_name",video_title)
                    # Entering Video Embed code (mandatory field)
                    if sel.is_element_present("id_embed")==False:
                        mclib.AppendErrorMessage(self,sel,"Input field for Video Embed code not found")
                    else:
                        print "Typing the embed code..."
                        sel.type("id_embed",video_embed)
                    # Entering Video thumbnail file (optional)
                    if video_thumbfile!="":
                        if sel.is_element_present("id_thumbnail_file")==False:
                            mclib.AppendErrorMessage(self,sel,"Input field for thumbnail file name and path not found")
                        else:
                            print "Entering the file name and path for thumbnail image..."
                            sel.type("id_thumbnail_file",video_thumbfile)
                    # Entering Video thumbnail URL (optional) 
                    if video_thumbURL!="":
                        if sel.is_element_present("id_thumbnail")==False:
                            mclib.AppendErrorMessage(self,sel,"Input field for thumbnail URL not found")
                        else:
                            print "Entering the thumbnail URL..."
                            sel.type("id_thumbnail",video_thumbfile)
                    # Entering Video description (optional)
                    if video_description!="":
                        if sel.is_element_present("id_description")==False:
                            mclib.AppendErrorMessage(self,sel,"Input field for video description not found")
                        else:
                            print "Typing in the video description..."
                            sel.type("id_description",video_description)
                    # Entering Video tags (optional)
                    if video_tags!="":
                        if sel.is_element_present("//input[@id='id_tags']")==False:
                            mclib.AppendErrorMessage(self,sel,"Input field for video tags not found")
                        else:
                            print "Typing in the video tags..."
                            sel.type("//input[@id='id_tags']",video_tags)
                    print "Now uploading the video..."
                    sel.click("//input[@value='Submit']")
                    sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])
                    # Checking that the video was submitted correctly
                    print "Checking that the video was submitted correctly..."
                    video_tags_list = ((video_tags.replace('Tags: ','')).lower()).split(', ')
                    if sel.is_element_present("//a[text()='"+video_url+"']")==False and sel.is_element_present("//a[@href='"+video_url+"']")==False:
                        mclib.AppendErrorMessage(self,sel,"Link to original video not found")
                    elif sel.is_text_present(video_title)==False:
                        mclib.AppendErrorMessage(self,sel,"Video TITLE not found")
#                    elif sel.is_text_present(video_author)==False:
#                        mclib.AppendErrorMessage(self,sel,"Video AUTHOR not found")
                    elif video_tags_list!=[x for x in video_tags_list if sel.is_text_present(x)==True]:
                    # (Checking if every element of the list is present on the web page)
                        mclib.AppendErrorMessage(self,sel,"Video TAGS not found")
                    elif sel.is_text_present(video_description)==False:
                        mclib.AppendErrorMessage(self,sel,"Video DESCRIPTION not found")
                    else:
                        print "OK"


# =======================================
# =     REJECT VIDEO FROM APPROVED      =
# =======================================

# This subroutine checks if the video being submitted is in the current ("Approved") set of videos
# If yes, deletes it

def RejectVideoFromApproved(self,sel,title):
    sel.open(testvars.MCTestVariables["ReviewQueuePage"])
    sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])
    if queue.CheckVideoStatus(self,sel,title,"Approved")==True:
        print "Duplicate video found - preparing to delete it..."
        sel.set_timeout(300000)
        sel.open(testvars.MCTestVariables["BulkEditPage"])
        sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])
        trimmedTitle = mclib.split_by_punctuation_char(title)
       #    print title
       #    print trimmedTitle
        sel.type("q",trimmedTitle)
        sel.click("//div[@id='labels']/form[1]/button")
        sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])
        if sel.is_text_present(title)==True:    # found video?
            row = 1
            titleElement="//div[@id='labels']/form[2]/table/tbody/tr["+str(row)+"]/td[2]/span"
            while sel.is_element_present(titleElement):
                tempTitle = sel.get_text(titleElement)
                if tempTitle==title:
                    break
                row = row + 1
                titleElement="//div[@id='labels']/form[2]/table/tbody/tr["+str(row)+"]/td[2]/span"
            if tempTitle==title:
                deleteElement = "//div[@id='labels']/form[2]/table/tbody/tr["+str(row)+"]/td[2]/div/a[2]"
                sel.click(deleteElement)
                sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])
        else:    
            mclib.AppendErrorMessage(self,sel,"Query did not return the video "+title)
            print "Also tried searching by: "+trimmedTitle
            self.fail("Cannot proceed with the test scenario")


