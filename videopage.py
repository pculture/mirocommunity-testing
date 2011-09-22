# Module VIDEOPAGE.PY
# includes:
#   * function   InlineManageVideo(self,sel,theme,action) - features or
#                unfeatures the video with the use of the button on the video page
#                and checks that the video has the correct status of a video
#                through Bulk Edit page
#                Returns True if the video is found in the set of videos with
#                this status and False otherwise
#                <action> can take "Feature" or "Unfeature" values


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
        


