# Module BULKEDIT.PY
# includes:
#   * subroutine NavigateToBulkEdit(self,sel) - opens /admin/bulk_edit
#   * subroutine PickFirstVideo(self,sel,video_set) - navigates to Bulk Edit
#                page and picks the top video on the first page of the selected
#                <video_set>, then opens the video page.
#                <video_set> can take the following values: "Current", "Featured"
#   * subroutine DeleteVideo(self,sel,title) - this subroutine finds the
#                video with title <title> and deletes (rejects) it
#   * subroutine ApproveRejectedVideo(self,sel,title) - finds the rejected
#                video with title <title> and approves it
#   * subroutine BulkEditAllVideosOnPage(self,sel,page,set,action) -
#                performs bulk action <action> on all the videos
#                in the selected <set> on the page <page>.
#                <page> should be a numeral
#                <set> may take values: "Current Videos", "Featured Videos",
#                "Rejected Videos", "Unapproved Videos".
#                <action> may take values: "Edit", "Delete", "Approve",
#                "Unapprove", "Feature","Unfeature"


from selenium import selenium

import unittest, time, re, urllib
import testvars, mclib, loginlogout

def NavigateToBulkEdit(self,sel):
    sel.open(testvars.MCTestVariables["BulkEditPage"])
#    sel.click(testvars.MCUI["AdminReviewQueue"])
    sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])
    try: self.failUnless(sel.is_text_present(""))
    except AssertionError, e:
#        self.verificationErrors.append("Not logged in as an Administrator")
        self.fail("Not logged in as an Administrator")



# =======================================
# =            PICK FIRST VIDEO         =
# =======================================

# This subroutine navigates to Bulk Edit page and picks the top video on the first page of the selected <video_set>,
# then opens the video page.
# <video_set> can take the following values: "Current", "Featured"

def PickFirstVideo(self,sel,video_set):
    print "Selecting the first video from the set of "+video_set+" videos on Bulk Edit page..."
    sel.open(testvars.MCTestVariables["BulkEditPage"])
    sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])
    try: self.failUnless(sel.is_text_present("Videos | Bulk Edit"))
    except AssertionError, e:
#        self.verificationErrors.append("Not logged in as an Administrator")
        self.fail("Not logged in as an Administrator")
    if video_set=="Featured":
        sel.select("name=filter", "label="+video_set+" Videos")
        sel.click("css=button.med_button")
        sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])
    title = sel.get_text("//div[2]/div/div[2]/form[2]/table/tbody/tr[1]/td[2]/span")
    print title
#/html/body/div[2]/div/div[2]/form[2]/table/tbody/tr/td[2]/span
    sel.click("//div[@id='labels']/form[2]/table/tbody/tr[1]/td[2]/div/a[3]")
    time.sleep(5)
#    sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])




# =======================================
# =             DELETE VIDEO            =
# =======================================

# This subroutine finds the video with title <title> and deletes
# (rejects) it

def DeleteVideo(self,sel,title):
#    sel.set_timeout(testvars.MCTestVariables["TimeOut"])
    sel.set_timeout("300000")
    # Navigate to Bulk Edit page
    NavigateToBulkEdit(self,sel)
    print " "
    print "Searching for the video..."
    # Trim the title of metacharacters and digits to avoid problems with search filter
#    trimmedTitle = mclib.remove_digits(mclib.remove_punctuation(title))
    trimmedTitle = mclib.split_by_punctuation_char(title)
#    print title
#    print trimmedTitle
    sel.type("q",trimmedTitle)
    # Item with zero index is the part of the title before the 1st period
    sel.click("//div[@id='labels']/form[1]/button")
    sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])
    if sel.is_text_present(title)==True:    # found video?
        print "Found video \""+title+"\" in the list - OK"
        sel.click("css=td[span[text()="+title+"]] > div.actions > a.delete_icon")
    else:    
        mclib.AppendErrorMessage(self,sel,"Query did not return the video "+title)
        print "Query did not return the video "+title
        print "Also tried searching by: "+trimmedTitle



# =======================================
# =       APPROVE REJECTED VIDEO        =
# =======================================

# This subroutine finds the rejected video with title <title> and approves it

def ApproveRejectedVideo(self,sel,title):
#    sel.set_timeout(testvars.MCTestVariables["TimeOut"])
    sel.set_timeout("300000")
    # Navigate to Bulk Edit page
    NavigateToBulkEdit(self,sel)
    print " "
    print "Searching for the video..."
    # Trim the title of metacharacters and digits to avoid problems with search filter
#    trimmedTitle = mclib.remove_digits(mclib.remove_punctuation(title))
    trimmedTitle = mclib.split_by_punctuation_char(title)
#    print title
#    print trimmedTitle
    sel.type("q",trimmedTitle)
    sel.select("name=filter", "label=Rejected Videos")
    sel.click("css=button.med_button")
    sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])
    # Item with zero index is the part of the title before the 1st period
    sel.check("css=input#id_form-0-BULK")
    sel.select("id=bulk_action_selector", "label=Approve")
    sel.click("css=div.bulkedit_controls > button.med_button")
    sel.click("//div[@id='massedit']/button")
    sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])



# =======================================
# =   BULK EDIT ALL VIDEOS ON THE PAGE  =
# =======================================

# This subroutine performs bulk action <action> on all the videos
# in the selected <set> on the page <page>.
# <page> should be a numeral
# <set> may take values: "Current Videos", "Featured Videos", "Rejected Videos",
# "Unapproved Videos".
# <action> may take values: "Edit", "Delete", "Approve", "Unapprove", "Feature","Unfeature"

def BulkEditAllVideosOnPage(self,sel,page,set,action):
    sel.open(testvars.MCTestVariables["BulkEditPage"]+"/?page="+str(page))
    sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])
    sel.select("name=filter", "label="+set)
    sel.click("css=button.med_button")
    sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])
    sel.click("id=toggle_all")
    sel.select("id=bulk_action_selector", "label="+action)
    sel.click("css=div.bulkedit_controls > button.med_button")
    sel.click("//div[@id='massedit']/button")
    sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])

    