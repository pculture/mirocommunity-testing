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
#   * subroutine InlineEditAuthor(self,sel,theme,newauthor) - replaces the current
#                author of the video with <newauthor>
#   * subroutine InlineEditDescription(self,sel,theme,newdescription) - replaces
#                the current description of the video with <newdescription>
#   * subroutine InlineEditCategory(self,sel,theme,newcategory) - adds the video to
#                category <newcategory>
#   * subroutine InlineEditTags(self,sel,theme,newtag) - adds a new tag <newtag> to
#                the video
#   * subroutine InlineEditWebsite(self,sel,theme,newwebsite) - replaces the current
#                website URL for the video with <newwebsite>
#   * subroutine PostComment(self,sel,theme,comment) - posts <comment>
#   * subroutine DeleteComment(self,sel,theme,comment) - deletes <comment>
#   * subroutine PostEditorsComment(self,sel,editorscomment) - posts <editorscomment>.
#                Theme 4 (Blue Theme) only
#   * subroutine PostToFacebook(self,sel,theme) - posts the currently selected video
#                on Facebook
#   * subroutine PostToTwitter(self,sel,theme) - posts the currently selected video
#                on Twitter
#   * subroutine EmailToFriends(self,sel,theme,email) - sends the link to the currently
#                selected video to <email> address
#   * subroutine AddToPlaylist(self,sel,theme,playlist) - adds the currently selected
#                video to <playlist>. Creates a new <playlist> if an existing one is not found


from selenium import selenium

import unittest, time, re, urllib, HTMLParser
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
        mclib.AppendErrorMessage(self,sel,"Dialog for inline editing the publication date was not found")
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



# ==================================================================
#                    INLINE EDIT THE VIDEO AUTHOR                  =
# ==================================================================

# This subroutine replaces the current author of the video with <newauthor>

def InlineEditAuthor(self,sel,theme,newauthor):
    if theme==4:
        linkCurrentAuthor = "css=div.vid_author > div.posted_by > div.editable > div.display_data > a"
        dialogEditAuthor = "css=div.vid_author > div.posted_by > div.editable > div.simple_overlay > h2"
    else:
        linkCurrentAuthor = "css=div.byline > div.editable > div.display_data > a"
        dialogEditAuthor = "css=div.byline > div.editable > div.simple_overlay > h2"
    linkEditAuthor = linkCurrentAuthor + ".edit_link"
    currentAuthor = sel.get_text(linkCurrentAuthor)
    print "The current author for this video is '"+currentAuthor+"'"
    print "Updating the author..."
    sel.click(linkEditAuthor)
    time.sleep(5)
    if sel.is_visible(dialogEditAuthor)!=True:
        mclib.AppendErrorMessage(self,sel,"Dialog for inline editing the author was not found")
    else:
        sel.uncheck("//li/label[span='"+currentAuthor+"']/input[@name='authors']")
        sel.check("//li/label[span='"+newauthor+"']/input[@name='authors']")
        sel.click("css=button.done")
        time.sleep(3)
        print "Done"
        print "Checking that the author has been updated correctly..."
        updatedAuthor = sel.get_text(linkCurrentAuthor)
        if updatedAuthor != newauthor:
            mclib.AppendErrorMessage(self,sel,"The author has not been updated as expected")
            print "Expected value: "+newauthor
            print "- Actual value: "+updatedAuthor
        else:
            print "OK - test passed"



# ==================================================================
#                 INLINE EDIT THE VIDEO DESCRIPTION                =
# ==================================================================

# This subroutine replaces the current description of the video with <newdescription>

def InlineEditDescription(self,sel,theme,newdescription):
    if theme==4:
        linkEditDescription = "css=div.editable > div.display_data > h4.meta_title > a.edit_link"
        dialogEditDescription = "css=div.simple_overlay:contains('Editing Description')"
    else:
        linkEditDescription = "css=div.editable > div.display_data > h4.meta_title > a.edit_link"
        dialogEditDescription = "css=div#main > div.editable > div.simple_overlay > h2"
    print "Editing the description..."
    sel.click(linkEditDescription)
    time.sleep(5)
    if sel.is_visible(dialogEditDescription)!=True:
        mclib.AppendErrorMessage(self,sel,"Dialog for inline editing of the description was not found")
    else:
        sel.type("id=id_description", newdescription)
        sel.click("css=button.done")
        time.sleep(3)
        print "Done"
        print "Checking that the description has been updated correctly..."
        linkDescription = "css=div.editable > div.display_data > div.description"
        updatedDescription = sel.get_text(linkDescription)
        if updatedDescription != mclib.remove_html_tags(newdescription):
            mclib.AppendErrorMessage(self,sel,"The description has not been updated as expected")
            print "Expected value: "+mclib.remove_html_tags(newdescription)
            print "- Actual value: "+updatedDescription
        else:
            print "OK - test passed"




# ==================================================================
#                 INLINE EDIT THE VIDEO CATEGORY                   =
# ==================================================================

# This subroutine adds the video to category <newcategory>

def InlineEditCategory(self,sel,theme,newcategory):
    if theme==4:
        linkEditCategory = "css=a#add_cat.edit_link"
        dialogEditCategory = "css=div.sidebar > div.share_box > div.meta > div.editable > div.simple_overlay > h2:contains('Editing Categories')"
    else:
        linkEditCategory = "css=a#add_cat.edit_link"
        dialogEditCategory = "css=div#tags > ul.meta_listing > li.item > div.editable > div.simple_overlay > h2"
    print "Editing the description..."
    sel.click(linkEditCategory)
    time.sleep(5)
    if sel.is_visible(dialogEditCategory)!=True:
        mclib.AppendErrorMessage(self,sel,"Dialog for inline editing of the category was not found")
    else:
        sel.check("//li/label[span='"+newcategory+"']/input[@name='categories']")
        sel.click("css=button.done")
        time.sleep(3)
        print "Done"
        print "Checking that the category has been added correctly..."
#        if sel.is_element_present("css=ul.meta_listing > li.item > div.editable > div.display_data > div.floatleft > ul > li[a="+newcategory+"]") == False:
        if theme!=4: categoryCSS = "css=ul.meta_listing > li.item > div.editable > div.display_data > div.floatleft > ul > li:contains("+newcategory+")"
        else: categoryCSS = "css=div.meta > div.editable:nth-child(2) > div.display_data > div.floatleft > ul > li:contains("+newcategory+")"
        if sel.is_element_present(categoryCSS) == False:
            mclib.AppendErrorMessage(self,sel,"The category has not been updated as expected")
            print "Expected category: "+newcategory
            if theme!=4: ActualList = "css=ul.meta_listing > li.item > div.editable > div.display_data > div.floatleft > ul"
            else: ActualList = "css=div.meta > div.editable:nth-child(2) > div.display_data > div.floatleft > ul"
            print "Actual list of categories: "+sel.get_text(ActualList)
        else:
            print "OK - test passed"



# ==================================================================
#                   INLINE EDIT THE VIDEO TAGS                     =
# ==================================================================

# This subroutine adds a new tag <newtag> to the video

def InlineEditTags(self,sel,theme,newtag):
    if theme==4:
        linkEditTags = "css=a#add_tag.edit_link"
        dialogEditTags = "css=div.meta > div.editable > div.simple_overlay > h2:contains('Editing Tags')"
    else:
        linkEditTags = "css=a#add_tag.edit_link"
        dialogEditTags = "css=div#tags > ul.meta_listing > li.item > div.editable > div.simple_overlay > h2:contains('Editing Tags')"
    print "Editing the tags..."
    sel.click(linkEditTags)
    time.sleep(5)
    if sel.is_visible(dialogEditTags)!=True:
        mclib.AppendErrorMessage(self,sel,"Dialog for inline editing of the tags was not found")
    else:
        sel.type("id=id_tags", newtag)
        sel.click("css=button.done")
        time.sleep(3)
        print "Done"
        print "Checking that the tags have been updated correctly..."
        if theme!=4: tagCSS = "css=ul.meta_listing > li.item > div.editable:nth-child(1) > div.display_data > div.floatleft > ul > li:contains("+newtag.lower()+")"
        else: tagCSS = "css=div.meta > div.editable:nth-child(1) > div.display_data > div.floatleft > ul > li:contains("+newtag.lower()+")"
        if sel.is_element_present(tagCSS) == False:
            mclib.AppendErrorMessage(self,sel,"The tags have not been updated as expected")
            print "Expected tag: "+newtag.lower()
            if theme!=4: ActualList = "css=ul.meta_listing > li.item > div.editable:nth-child(1) > div.display_data > div.floatleft > ul"
            else: ActualList = "css=div.meta > div.editable:nth-child(1) > div.display_data > div.floatleft > ul"
            print "Actual list of tags: "+sel.get_text(ActualList)
        else:
            print "OK - test passed"




# ==================================================================
#                INLINE EDIT THE VIDEO WEBSITE URL                 =
# ==================================================================

# This subroutine replaces the current website URL for the video with <newwebsite> 

def InlineEditWebsite(self,sel,theme,newwebsite):
    if theme==4:
        print "Website URL for a video cannot be edited in Blue Theme. Test skipped."
        return
    else:
        linkEditWebsite = "css=div#main > div#tags > ul.meta_listing > li.item > div.editable > div.display_data > div.floatleft > h3 > a.edit_link"
        dialogEditWebsite = "css=div#main > div#tags > ul.meta_listing > li.item:nth-child(3) > div.editable > div.simple_overlay > h2"
        print "Editing the website URL..."
        sel.click(linkEditWebsite)
        time.sleep(5)
        if sel.is_visible(dialogEditWebsite)!=True:
            mclib.AppendErrorMessage(self,sel,"Dialog for inline editing of the website URL was not found")
        else:
            sel.type("id=id_website_url", newwebsite)
            sel.click("css=button.done")
            time.sleep(3)
            print "Done"
            print "Checking that the website URL has been updated correctly..."
            linkWebsite = "css=span.url"
            updatedWebsite = sel.get_text(linkWebsite)
            if updatedWebsite != newwebsite:
                mclib.AppendErrorMessage(self,sel,"The website URL has not been updated as expected")
                print "Expected value: "+newwebsite
                print "- Actual value: "+updatedWebsite
            else:
                print "OK - test passed"




# ==================================================================
#                            POST COMMENT                          =
# ==================================================================

# This subroutine posts <comment>

def PostComment(self,sel,theme,comment):
    if theme==4:
        textareaComment = "css=textarea#id_comment"
        buttonComment = "css=button.post_comment"
    else:
        textareaComment = "css=textarea#id_comment"
        buttonComment = "css=input.submit-post"
    sel.type(textareaComment,comment)
    sel.click(buttonComment)
    print "Done"
    time.sleep(15)
    # Checking that the comment has actually been posted
    if sel.is_text_present(comment)==False:
        mclib.AppendErrorMessage(self,sel,"The comment has not been posted properly")


        
# ==================================================================
#                          DELETE COMMENT                          =
# ==================================================================

# This subroutine deletes <comment>

def DeleteComment(self,sel,theme,comment):
    # Searching for comment on the page
    if sel.is_text_present(comment)==False:
        mclib.AppendErrorMessage(self,sel,"The desired comment not found")
    else:
        print "Deleting comment "+comment+"..."
        if theme==4:
            buttonDelete = "//ul[@id='comments']/li[contains(./div[@class='item_details']/div[@class='comment'],'"+comment+"')]/div[@class='comment-moderation']/form[1]/button[@type='submit']"
        else:
            buttonDelete = "//li[contains(./div[@class='comment-body'],'"+comment+"')]/div[@class='comment-poster']/div[@class='comment-moderation']/form[1]/button[text()='delete']"
        print sel.is_element_present(buttonDelete)
        sel.click(buttonDelete)
        sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])
#        time.sleep(3)
        print "Checking that the comment has been deleted correctly..."
        if sel.is_text_present(comment):
            mclib.AppendErrorMessage(self,sel,"The comment has not been deleted properly")
        else:
            print "OK"



# ==================================================================
#                        POST EDITORS COMMENT                      =
# ==================================================================

# This subroutine posts <editorscomment>. Theme 4 (Blue Theme) only

def PostEditorsComment(self,sel,editorscomment):
    linkEditorsComment = "css=div.main > div.editable > div.display_data > a.edit_link"
    dialogEditorsComment = "css=div.main > div.editable > div.simple_overlay > h2:contains('Editing Editors comment')"
    sel.click(linkEditorsComment)
    time.sleep(5)
    if sel.is_visible(dialogEditorsComment)!=True:
        mclib.AppendErrorMessage(self,sel,"Dialog for posting the editors comment was not found")
    else:
        sel.type("id=id_editors_comment", editorscomment)
        sel.click("css=button.done")
        time.sleep(3)
        print "Done"
        print "Checking that the website URL has been updated correctly..."
#        linkEditorsComment = "css=div.description:nth-child(1)"
        linkEditorsComment = "css=div.editors_notes"
        str = sel.get_text(linkEditorsComment)
        postedComment = re.split("writes: ",str.replace("\n",""))
#        print postedComment
        if postedComment[1] != mclib.remove_html_tags(editorscomment):
            mclib.AppendErrorMessage(self,sel,"The Editor's Comment has not been updated as expected")
            print "Expected value: "+mclib.remove_html_tags(editorscomment)
            print "- Actual value: "+postedComment[1]
        else:
            print "OK - test passed"



# ==================================================================
#                        POST VIDEO ON FACEBOOK                    =
# ==================================================================

# This subroutine posts the currently selected video on Facebook

def PostToFacebook(self,sel,theme,videotitle):
    currentpageURL = sel.get_location()
    linkPostFacebook = "css=span.FBConnectButton_Text_Simple"
    sel.click(linkPostFacebook)
    sel.wait_for_pop_up("sharer", testvars.MCTestVariables["TimeOut"])
    sel.select_window("title=Facebook")
    sel.click("css=textarea.uiTextareaNoResize")
    sel.type("css=textarea.uiTextareaNoResize", "TEST POST, theme "+str(theme))
    title = sel.get_text("css=a.UIShareStage_InlineEdit")
    if title!=videotitle:
        mclib.AppendErrorMessage(self,sel,"Video title passed to Facebook does not match the real one")
        print "Expected to find: "+videotitle
        print "-Actually passed: "+title
    videoURL = sel.get_text("css=div.UIShareStage_Subtitle")
#    if videoURL!=currentpageURL:
#        mclib.AppendErrorMessage(self,sel,"Video URL passed to Facebook does not match the real URL")
#        print "Expected to find: "+currentpageURL
#        print "-Actually passed: "+videoURL
    sel.click("css=label.uiButtonConfirm")
    time.sleep(15)
    # Check that the Facebook popup is closed
    if (u'Facebook') in sel.get_all_window_titles():
        mclib.AppendErrorMessage(self,sel,"Facebook sharing popup did not close as expected")
    else:
        sel.select_window("null")
        sel.open("http://www.facebook.com")
        sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])
        sel.click("link=Pat Culture")
        time.sleep(5)
        if sel.is_text_present(title)==False:
            mclib.AppendErrorMessage(self,sel,"New post with the video title not found")
        else:
            if sel.is_element_present("link="+title)==False:
                mclib.AppendErrorMessage(self,sel,"Link to the posted video not found")
            else:
                postedURL = sel.get_attribute('//a[text()="'+title+'"]@href')
                print postedURL
#                sel.click("link="+title)
#                sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])
                if postedURL!=currentpageURL:
                    mclib.AppendErrorMessage(self,sel,"Facebook post links to the wrong page")
                    print "Expected to find: "+currentpageURL
                    print "- Actually found: "+postedURL
                else:
                    print "OK. Test passed"


# ==================================================================
#                        POST VIDEO ON TWITTER                    =
# ==================================================================

# This subroutine posts the currently selected video on Twitter

def PostToTwitter(self,sel,theme):
    print "Clicking Tweet This Video link..."
    linkPostTwitter = "css=a.twitter"
    sel.click(linkPostTwitter)
    time.sleep(5)
#    print sel.get_all_window_titles()
    if (u'Sign in to Twitter') in sel.get_all_window_titles():
        print "Logging in to Twitter"
        sel.select_window("title=Sign in to Twitter")
        sel.type("css=form#login-form fieldset.sign-in div.row input#username_or_email.text",testvars.MCTestVariables["TwitterLogin"])
        sel.type("css=form#login-form fieldset.sign-in div.row input#password.password",testvars.MCTestVariables["TwitterPassword"].decode('base64'))
        sel.click("css=form#login-form div.row input.submit")
        sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])
    else:
        sel.select_window("title=Post a Tweet on Twitter")
    #print sel.get_all_window_titles()
    print "Posting the following tweet:"
    defaultTweet = sel.get_value("css=span.field > textarea#status")
    newTweet = "TEST TWEET: theme" + str(theme) + ". " + defaultTweet
    h = HTMLParser.HTMLParser()
    newTweetTrimmed = h.unescape(newTweet)
    print newTweet
    sel.type("css=span.field > textarea#status",newTweet)
    sel.click("css=input.button.submit")
    time.sleep(10)
 #   print sel.get_all_window_titles()
 #   print sel.get_title()
#    sel.select_window("title=Twitter / Home")
#    print sel.get_all_window_titles()
#    print sel.get_location()
    sel.open("http://twitter.com/#!/PCFQA")
    time.sleep(15)
#    sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])
#    print sel.get_title()
    print "Checking that the tweet was posted successfully..."
#    print sel.is_element_present("css=div.stream-manager")
#    print sel.is_element_present("css=div.stream div#stream-items-id.stream-items div.js-stream-item:nth-child(1)")
#    xxx = sel.get_text("css=div.stream div#stream-items-id.stream-items div.js-stream-item:nth-child(1) div.stream-item-content div.tweet-content div.tweet-row div.tweet-text")
#    print xxx
    if sel.is_text_present(newTweetTrimmed.replace("http://",""))==False:
        mclib.AppendErrorMessage(self,sel,"New tweet not found")
        print "Expected text: "+newTweetTrimmed.replace("http://","")
        if sel.is_element_present("css=div.stream div#stream-items-id.stream-items div.js-stream-item:nth-child(1) div.stream-item-content div.tweet-content div.tweet-row div.tweet-text")==True:
            print "- Actual text: "+sel.get_text("css=div.stream div#stream-items-id.stream-items div.js-stream-item:nth-child(1) div.stream-item-content div.tweet-content div.tweet-row div.tweet-text")
            print sel.is_text_present(newTweetTrimmed.replace("http://",""))==sel.get_text("css=div.stream div#stream-items-id.stream-items div.js-stream-item:nth-child(1) div.stream-item-content div.tweet-content div.tweet-row div.tweet-text")
        else:
            print "- Actual text: ***NOT FOUND***"
    else:
        print "OK. Test passed"
    print "Closing Twitter, switching back to MiroCommunity..."    
    sel.close()
    sel.select_window("null")
    print "OK"
    
        

# ==================================================================
#                        EMAIL VIDEO TO FRIENDS                    =
# ==================================================================

# This subroutine sends the link to the currently selected video to <email> address

def EmailToFriends(self,sel,theme,email):
    print "Clicking Email To Friends link..."
    linkEmailFriends = "css=a.email"
    sel.click(linkEmailFriends)
    time.sleep(5)
    if sel.is_element_present("css=form#share_form")==False:
        mclib.AppendErrorMessage(self,sel,"Email dialog not found")
    else:
        if sel.get_value("css=input#id_sender_email")=="":
            sel.type("css=input#id_sender_email","pcf.subwriter@gmail.com")
        sel.type("css=input#id_recipient_email",email)
        sel.type("css=textarea#id_message","TEST with theme "+str(theme))
        sel.click("css=input[type='submit'][value='Share!']")
        time.sleep(5)
        if (sel.is_element_present("css=div#share_thanks")==False or sel.is_text_present("Thanks!")==False):
            mclib.AppendErrorMessage(self,sel,"Confirmation message on sending off the email not found")
        else:
            sel.click("css=a.close")
    


# ==================================================================
#                        ADD VIDEO TO PLAYLISTS                    =
# ==================================================================

# This subroutine adds the currently selected video to <playlist>
# Creates a new <playlist> if an existing one is not found

def AddToPlaylist(self,sel,theme,playlist):
    if sel.is_element_present("css=div.playlist_title > a:contains('"+playlist+"')"):
        mclib.AppendErrorMessage(self,sel,"This video has alreday been added to playlist "+playlist+". Cannot proceed with the test")
    if sel.is_element_present("css=select#id_playlist > option:contains('"+playlist+"')"):
        print "Playlist "+playlist+" found, adding video..."
        sel.select("id=id_playlist", "label="+playlist)
        time.sleep(2)
        sel.click("css=input[type=\"submit\"]")
        sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])
    else:
        # Create new playlist
        print "Playlist "+playlist+" not found, creating new playlist..."
        sel.select("id=id_playlist", "label=New Playlist...")
        time.sleep(2)
        sel.answer_on_next_prompt(playlist)
        sel.click("css=input[type=\"submit\"]")
        time.sleep(2)
        self.assertEqual("Enter the name for the new playlist:", sel.get_prompt())
        time.sleep(5)
    print "Checking that the video has been added to playlist"
#    if sel.is_element_present("css=div.playlist_title > a:contains('"+playlist+"')")==False:
    if sel.is_text_present(playlist)==False:
#        print sel.get_text("css=div#playlists div ul li")
        mclib.AppendErrorMessage(self,sel,"The marker of playlist "+playlist+" has not been found")
    else:
        print "OK"
            

    
    