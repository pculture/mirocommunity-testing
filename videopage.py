# Module VIDEOPAGE.PY
# includes:
#   * function   InlineManageVideo(self,sel,theme,action) - features or
#                unfeatures the video with the use of the button on the video page
#                and checks that the video has the correct status of a video
#                through Bulk Edit page
#                Returns True if the video is found in the set of videos with
#                this status and False otherwise
#                <action> can take "Feature" or "Unfeature" values
#   * function GetThumbnailURL(self,sel) - returns the video's thumbnail URL or "",
#                if it is missing
#   * function PickVideoFromNewVideosListingPage(self, sel, theme) - returns the link
#                to video No. <theme> from New Videos page
#   * subroutine ChangeThumbnail(self,sel,theme,thumbURL,thumbFile) - modifies
#                the video thumbnail through the video page to <thumbURL>, if it
#                is not blank, or to <thumbFile> otherwise
#   * subroutine InlineEditTitle(self,sel,theme,newtitle) - updates the title of the
#                video with <newtitle> text
#   * subroutine InlineEditPublicationDate(self,sel,theme,newdate) - updates the
#                publication date of the video with <newdate> text
#                Date format: Format: yyyy-mm-dd hh:mm:ss


from selenium import selenium

import unittest, time, re, urllib
import testvars, mclib, loginlogout, queue, bulkedit



# ==================================================================
#      INLINE MANAGE (FEATURE/UNFEATURE/APPROVE/REJECT VIDEO)      =
# ==================================================================

# This function features or unfeatures the video with the use of the button on the video page
# and checks that the video has the correct status of a video through Bulk Edit page
# Returns True if the video is found in the set of videos with this status
# and False otherwise
# <action> can take "Feature", "Unfeature", "Approve" or "Reject" values

def InlineManageVideo(self,sel,theme,action):
    if action=="Feature":
        if theme!=4:    ActionLink="Feature this video"
        else:           ActionLink="Feature this Video"
    elif action=="Unfeature":
        if theme!=4:    ActionLink="Unfeature this video"
        else:           ActionLink="Unfeature this Video"
    elif action=="Reject":
        if theme!=4:    ActionLink="Reject this video"
        else:           ActionLink="Reject this Video"
    elif action=="Approve":
        if theme!=4:    ActionLink="Approve this video"
        else:           ActionLink="Approve this Video"
    else: mclib.AppendErrorMessage(self,sel,"Wrong parameter passed to InlineManageVideo procedure")
    if sel.is_element_present("link="+ActionLink)==0: # Action button not found on the video page
        mclib.AppendErrorMessage(self,sel,"'"+ActionLink+"' button is missing")
        # self.fail("Impossible to carry on with the test")
        return False
    else:
        # Memorize the video title
        if theme!=4:   titleCaption = "//div[@id='main']/div[1]/div/div/div[1]/h2"
        else:          titleCaption = "css=h2.edit_click" #"//div[@id='view_video']/div[3]/div[1]/div/div[1]/h2"
        titleUntrimmed = sel.get_text(titleCaption)
        title = titleUntrimmed.replace(' Edit','')
        print "Going to "+action+" video: "+title
        print "Clicking the button..."
        sel.click("link="+ActionLink)  # Click Action button
        time.sleep(5)
        sel.refresh()
        time.sleep(5)
#        sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])
        if sel.is_element_present("link="+ActionLink)!=0:  # Action button must have disappeared
            mclib.AppendErrorMessage(self,sel,"'"+action+"' button is still present on the page, though it should not")
            return False
        else:
            print "OK"
            print "Verifying that the video has actually been "+action+"d..."
            if action=="Feature": blCheckResult = queue.CheckVideoStatus(self,sel,title,"Featured")
            if action=="Unfeature": blCheckResult = not(queue.CheckVideoStatus(self,sel,title,"Featured"))
            if action=="Reject": blCheckResult = queue.CheckVideoStatus(self,sel,title,"Rejected")
            if action=="Approve": blCheckResult = queue.CheckVideoStatus(self,sel,title,"Approved")
            time.sleep(3)
            if action!="Reject":
                print "Rejecting the "+action+"d video..."
                bulkedit.DeleteVideo(self,sel,title)
                return blCheckResult
            else:
                print "Approving the rejected video..."
                bulkedit.ApproveRejectedVideo(self,sel,title)
                return blCheckResult
        

# ==================================================================
#                        GET CURRENT THUMBNAIL URL                 =
# ==================================================================

# This function returns the video's thumbnail URL or "", if it is missing

def GetThumbnailURL(self,sel):
    result = ""
    linkCaption = "Upload/Replace Thumbnail"
    linkUploadThumbnail = "link="+linkCaption
    if sel.is_element_present(linkUploadThumbnail)==False:
        mclib.AppendErrorMessage(self,sel,"Upload/Replace Thumbnail link not found")
    else:
        sel.click(linkUploadThumbnail)
        time.sleep(5)
        overlayEditingThumbnail = "css=div.editable div.simple_overlay h2"
        if sel.is_visible(overlayEditingThumbnail)==False:
            mclib.AppendErrorMessage(self,sel,"Dialog for Editing Thumbnail was not found")
        else:
            result = sel.get_value("css=input#id_thumbnail_url")
            sel.click("css=a.close")
    return result



# ==================================================================
#                        CHANGE THUMBNAIL                          =
# ==================================================================

# This subroutine modifies the video thumbnail through the video page to
# <thumbURL>, if it is not blank, or to <thumbFile> otherwise

def ChangeThumbnail(self,sel,theme,thumbURL,thumbFile):
    linkCaption = "Upload/Replace Thumbnail"
    print "Looking for "+linkCaption+" ..."
    linkUploadThumbnail = "link="+linkCaption
    if sel.is_element_present(linkUploadThumbnail)==False:
        mclib.AppendErrorMessage(self,sel,"Upload/Replace Thumbnail link not found")
    else:
        print "Clicking "+linkCaption+" ..."
        sel.click(linkUploadThumbnail)
        time.sleep(5)
        overlayEditingThumbnail = "css=div.editable div.simple_overlay h2"
        if sel.is_visible(overlayEditingThumbnail)==False:
            mclib.AppendErrorMessage(self,sel,"Dialog for Editing Thumbnail was not found")
        else:
            print "OK"
            print "Entering the new thumbnail..."
            if thumbURL!="": sel.type("css=input#id_thumbnail_url", thumbURL)
            elif thumbFile!="": sel.type("css=input#id_thumbnail", thumbFile)
            else: mclib.AppendErrorMessage(self,sel,"New thumbnail was not provided")
            sel.click("css=button.done")
            time.sleep(5)
            print "Done"



# ==================================================================
#           PICK VIDEO FROM NEW VIDEOS LISTING PAGE                =
# ==================================================================

# This function returns the link to video No. <theme> from New Videos page

def PickVideoFromNewVideosListingPage(self, sel, theme):
    videoNumber = str(theme+1) # Select video No. between 1 and 4
    # Selecting the first video from the list of new videos
    sel.open(testvars.MCTestVariables["NewVideosListingPage"])
    sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])
    #"css = div#content div.video:nth(0) > a.thumbnail > img"
    # Memorizing the video title
    if theme!=4:  videoTitleLink ="//div[@id='content']/div["+videoNumber+"]/div/h3/a"
    else:  videoTitleLink="css=ul.vid_list > li:nth-child("+videoNumber+")> div.item_details>h2>a"
    return videoTitleLink




# ==================================================================
#                   INLINE EDIT THE VIDEO TITLE                    =
# ==================================================================

# This subroutine updates the title of the video with <newtitle> text

def InlineEditTitle(self,sel,theme,newtitle):
    sel.click("css=a.edit_link > span")
    time.sleep(5)
    if sel.is_visible("css=div.vid_title>div.editable>div.simple_overlay>h2")!=True:
        mclib.AppendErrorMessage(self,sel,"Dialog for inline editing the video title was not found")
    else:
        sel.type("css=input#id_name", newtitle)
        sel.click("css=button.done")
        time.sleep(3)


# ==================================================================
#                 INLINE EDIT THE PUBLICATION DATE                 =
# ==================================================================

# This subroutine updates the publication date of the video with <newdate> text
# Date format: Format: yyyy-mm-dd hh:mm:ss

def InlineEditPublicationDate(self,sel,theme,newdate):
    if theme==4:
        linkEditDate = "css=div.posted_at > div.editable > div.display_data > span.edit_link"
        dialogEditDate = "css=div.posted_at > div.editable > div.simple_overlay > h2"
    else:
        linkEditDate = "css=div.date > div.editable > div.display_data > span.edit_link"
        dialogEditDate = "css=div.date > div.editable > div.simple_overlay > h2"
    sel.click(linkEditDate)
    time.sleep(5)
    if sel.is_visible(dialogEditDate)!=True:
        mclib.AppendErrorMessage(self,sel,"Dialog for inline editing the video title was not found")
    else:
        sel.type("css=input#id_when_published", newdate)
        sel.click("css=button.done")
        time.sleep(3)
        print "Verifying that the publication date has been changed..."
        sel.click(dialogEditDate)
        if sel.get_value("css=input#id_when_published")==newdate:
            print "OK"
        else:
            mclib.AppendErrorMessage(self,sel,"The publication date has not been updated correctly")
        sel.click("css=a.close")
