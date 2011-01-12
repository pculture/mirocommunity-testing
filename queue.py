# Module QUEUE.PY
# includes:
#   * function CheckVideoStatus(self,sel,title,status) - checks the status
#              of a video through Bulk Edit page
#              Status can be set to "Approved", "Featured", or "Rejected".
#              Returns True if the video is found in the set of videos with 
#              this status and False otherwise
#   * subroutine NavigateToReviewQueue(self,sel) - opens /admin/approve_reject
#   * subroutine ProcessVideo(self,sel,page,number,action) - processes (approves,
#                features, or rejects) video No. <number> on page <page>.
#                <page> should be a string variable (a numeral or "Last")
#                <number> should be a numeric between 1 and 10; numbers greater than 10
#                are treated as 10
#                <action> may take values: "Approved","Featured","Rejected"
#   * subroutine ApproveVideoPage(self,sel,page) - approves all the videos 
#                on page <page>.
#                <page> should be a string variable (a numeral or "Last")
#   * function   RejectVideoPage(self,sel,page) - rejects all the videos 
#                on page <page>.
#                <page> should be a string variable (a numeral or "Last")
#                Returns the list of videos on the rejected page
#   * function   ClearQueue(self,sel) - clears the entire queue
#                Returns the list of videos on page 1
#   * subroutine EditVideoInQueue(self,sel,page,number,title,user,posted,thumbnail,
#                description,category,tag,website) - edits the parameters of the
#                video No. <number> on page <page>.
#                <page> should be a string variable (a numeral or "Last")
#                <number> should be a numeric between 1 and 10; numbers greater than 10
#                are treated as 10
#                <title> - new title
#                <user> - new author associated with the video
#                <posted> - new submission date
#                <thumbnail> - new thumb image (can be URL or file name and path)
#                <description> - new description
#                <category> - new category associated with the video
#                <tag> - new tag for the video
#                <website> - a new website URL
#   * subroutine ViewRSSFeeds(self,sel,feed) - opens RSS feeds with videos awaiting
#                moderation and checks relevant pages
#                <feed> must be = "Unapproved RSS" or "Unapproved User RSS"
#   * function FindVideoInQueue(self,sel,title) - returns page number and video number
#                for a video in the premoderation queue
#                If not found, the function returns [0,0]
#   * subroutine RejectVideoFromQueue(self,sel,title) - checks if the video being
#                submitted is in the premoderation queue ("Unapproved") 
#                If yes, rejects it
#                <title> should be in Unicode format
#                Created for extensive use in Submit Video test cases

from selenium import selenium

import unittest, time, re, urllib
import testvars, mclib, loginlogout

def NavigateToReviewQueue(self,sel):
    sel.open(testvars.MCTestVariables["ReviewQueuePage"])
#    sel.click(testvars.MCUI["AdminReviewQueue"])
    sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])
    try: self.failUnless(sel.is_text_present("Videos for Review"))
    except AssertionError, e:
#        self.verificationErrors.append("Not logged in as an Administrator")
        self.fail("Not logged in as an Administrator")


# =======================================
# =          CHECK VIDEO STATUS         =
# =======================================

# This function checks the status of a video through Bulk Edit page
# Status can be set to "Approved", "Featured", or "Rejected".
# Returns True if the video is found in the set of videos with this status
# and False otherwise

def CheckVideoStatus(self,sel,title,status):
    if (status!="Approved" and status!="Featured" and status!="Rejected"):
        self.fail("Wrong value of Status parameter passed to CheckVideoStatus subroutine")
    # Navigate to Bulk Edit page
    sel.open(testvars.MCTestVariables["BulkEditPage"])
#    sel.click(testvars.MCUI["AdminBulkEdit"])
    sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])
    print " "
    print "Searching for the "+status+" video..."
    # Trim the title of metacharacters and digits to avoid problems with search filter
#    trimmedTitle = mclib.remove_digits(mclib.remove_punctuation(title))
    trimmedTitle = mclib.split_by_punctuation_char(title)
#    print title
#    print trimmedTitle
    sel.type("q",trimmedTitle)
    # Item with zero index is the part of the title before the 1st period
    if status=="Featured":
        sel.select("filter", "label=Featured Videos")
        time.sleep(20) #the above filter is VERY slow!
    elif status=="Rejected":
        sel.select("filter", "label=Rejected Videos")
        time.sleep(20) #the above filter is VERY slow!
    sel.click("//div[@id='labels']/form[1]/button")
    sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])
    if sel.is_text_present(title)==True:    # found video?
        print "Found video \""+title+"\" in the list of "+status+" videos - OK"
        return True
    else:    
#        mclib.AppendErrorMessage(self,sel,"Query did not return the video "+title)
        print "Query did not return the video "+title
        print "Also tried searching by: "+trimmedTitle
        return False



# =======================================
# =      PROCESS VIDEO IN THE QUEUE     =
# =======================================

# This subroutine processes (approves, features, or rejects) video No. <number>
# on page <page>.
# <page> should be a string variable (a numeral or "Last")
# <number> should be a numeric between 1 and 10; numbers greater than 10
# are treated as 10
# <action> may take values: "Approved","Featured","Rejected"

def ProcessVideo(self,sel,page,number,action):
    # Check that the value of <action> is correct
    if (action!="Approved" and action!="Featured" and action!="Rejected"):
        self.fail("Wrong value of Action parameter passed to ProcessVideo subroutine")
    NavigateToReviewQueue(self,sel)
    if page=="Last": pageNo = "1000000"
    else: pageNo = page
    # Construct the URL of the page in the queue with the given number
    pageLink = testvars.MCTestVariables["ReviewQueuePage"]+"/?page="+pageNo
#    print pageLink
    try:
        sel.open(pageLink)
        sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])
    except: pass
        #self.fail("Could not open page "+pageNo+" in the queue")
    # Construct the link for approving a video with its number on the page
    if number > 10: number=10
    elif number < 1: number=1
    baseLink = "//div[@id='admin_videolisting_row']/div["+str(number)
    titleLink = baseLink+"]/div[1]/h3/a"
    featureLink = baseLink+"]/div[2]/a[1]/span"
    approveLink = baseLink+"]/div[2]/a[2]/span"
    rejectLink = baseLink+"]/div[2]/a[3]/span"
    # Memorize the title of the chosen video
    if sel.is_element_present(titleLink)==True:
        videoTitle = sel.get_text(titleLink)
    else:
        mclib.AppendErrorMessage(self,sel,"Video title not found")
    # Now determining what to do with the video
    if action=="Featured":    actionLink=featureLink
    elif action=="Approved":    actionLink=approveLink
    elif action=="Rejected":    actionLink=rejectLink
    actionDesc = action[:(len(action)-2)]+"ing"    # Convert <action> to 'gerundiciple'
    print actionDesc+" video No."+str(number)+" on queue page "+pageNo+"..."
    if sel.is_element_present(actionLink)==True:
        sel.click(actionLink)
        time.sleep(5)
        print "OK"
    else:
        actionDesc = action[:(len(action)-1)]   
        mclib.AppendErrorMessage(self,sel,actionDesc+" link not found for the video")
    print CheckVideoStatus(self,sel,videoTitle,action)



# =======================================
# =          APPROVE VIDEO PAGE         =
# =======================================

# This subroutine approves all the videos on page <page>.
# <page> should be a string variable (a numeral or "Last")

def ApproveVideoPage(self,sel,page):
    NavigateToReviewQueue(self,sel)
    if page=="Last": pageNo = "1000000"
    else: pageNo = page
    # Construct the URL of the page in the queue with the given number
    pageLink = testvars.MCTestVariables["ReviewQueuePage"]+"/?page="+pageNo
    try:
        sel.open(pageLink)
        sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])
    except: pass
    time.sleep(5)
    # Check if there are any videos in the queue for the test to run
    if sel.is_element_present("//div[@id='admin_videolisting_row']/div[1]")==False:
        self.fail("No videos found on the queue page. Not enough test data to run the test.")
    # Memorize the list of video titles on the page
    print "Memorizing the list of videos found on the page..."
    videoList = ['']
    for i in range(1,11):
        titleLink = "//div[@id='admin_videolisting_row']/div["+str(i)+"]/div[1]/h3/a"
        if sel.is_element_present(titleLink)==True:
            newTitle=sel.get_text(titleLink)
            videoList.append(newTitle)
        else:
            videoList.append("None")
    videoList.remove('')
    print "Found the following videos on the queue page "+page+":"
    print videoList
    # Approve page
    approveButton = "//div[@id='content']/a[1]/span"
    if sel.is_element_present(approveButton)==False: # If approve button not found
        mclib.AppendErrorMessage(self,sel,"'Approve All the Videos on This Page' button not found")
    else:
        sel.click(approveButton)
        sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])
        print "Approved page"
        # Check that all the videos were approved
        print "Checking that all the videos were successfully approved..."
        sel.open("/listing/new/")
        sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])
        for item in videoList:
            if item!="None":
                itemLink = "//a[text()='"+item+"']"
                if sel.is_element_present("link="+item)==True:
                    videoLink = sel.get_attribute("link="+item+"@href")
                    print "Found video *"+item+"* at URL: "+videoLink
                else:
                    mclib.AppendErrorMessage(self,sel,"Could not find video "+item+" in the list of new videos.")
            else:
                print "N/A"
# THIS CRASHES FIREFOX AFTER 6 OR 7 (OUT OF 10) ITERATIONS
#    for item in videoList:
#        if item!="None":
#            newResult=CheckVideoStatus(self,sel,item,action)
#            print item+"__________"+str(newResult)
#            if newResult==False:
#                mclib.AppendErrorMessage(self,sel,"Could not find video "+item+" in the list of "+action.lower()+" videos.")
#            sel.click(testvars.MCUI["AdminReviewQueue"])
#            sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])
#        else:
#            print "None__________None"



# =======================================
# =          REJECT VIDEO PAGE         =
# =======================================

# This subroutine rejects all the videos on page <page>.
# <page> should be a string variable (a numeral or "Last")

def RejectVideoPage(self,sel,page):
    NavigateToReviewQueue(self,sel)
    if page=="Last": pageNo = "1000000"
    else: pageNo = page
    # Construct the URL of the page in the queue with the given number
    pageLink = testvars.MCTestVariables["ReviewQueuePage"]+"/?page="+pageNo
    try:
        sel.open(pageLink)
        sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])
    except: pass
    time.sleep(5)
    # Check if there are any videos in the queue for the test to run
    if sel.is_element_present("//div[@id='admin_videolisting_row']/div[1]")==False:
        self.fail("No videos found on the queue page. Not enough test data to run the test.")
    # Memorize the list of video titles on the page
    print "Memorizing the list of videos found on the page..."
    videoList = ['']
    for i in range(1,11):
        titleLink = "//div[@id='admin_videolisting_row']/div["+str(i)+"]/div[1]/h3/a"
        if sel.is_element_present(titleLink)==True:
            newTitle=sel.get_text(titleLink)
            videoList.append(newTitle)
        else:
            videoList.append("None")
    videoList.remove('')
    print "Found the following videos on the queue page "+page+":"
    print videoList
    # Reject page
    rejectButton = "//div[@id='content']/a[2]/span"
    if sel.is_element_present(rejectButton)==False: # If reject button not found
        mclib.AppendErrorMessage(self,sel,"'Reject All the Videos on This Page' button not found")
    else:
        sel.click(rejectButton)
        sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])
        print "Rejected page"
        return videoList

    # Check that all the videos were rejected
#    print "Checking that all the videos were successfully rejected..."
#    sel.open(testvars.MCUI["AdminBulkEdit"])
#    sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])
#    for item in videoList:
#        if item!="None":
#            newResult=CheckVideoStatus(self,sel,item,"Rejected")
#            print item+"__________"+str(newResult)
#            if newResult==False:
#                mclib.AppendErrorMessage(self,sel,"Could not find video "+item+" in the list of rejected videos.")
#            sel.click(testvars.MCUI["AdminReviewQueue"])
#            sel.open("http://dalmatia.mirocommunity.org/admin/bulk_edit")
#            sel.click(testvars.MCTestVariables["ViewMainSiteLink"])
#            sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])
#            loginlogout.LogOut(self,sel)
#            loginlogout.LogInAsAdmin(self,sel)
#            sel.click("//div[@id='header']/a[2]/span")
#            sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])
#        else:
#            print "None__________None"

#    page = 1
#    firstVideo = ""
#    rejectedURL = testvars.MCTestVariables["BulkEditPage"]+"/?category=&author=&filter=rejected&q=&page="+str(page)
#    print rejectedURL
#    sel.set_timeout(200000)
#    sel.open(rejectedURL)
#    sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])
    # Check and open the next page - repeat until the next page is identical with the previous one
#    while firstVideo!=sel.get_text("//div[@id='labels']/form[2]/table/tbody/tr[1]/td[2]/span"):
#        firstVideo = sel.get_text("//div[@id='labels']/form[2]/table/tbody/tr[1]/td[2]/span")
#        for rowNo in range (1,11):
#            titleElement = "//div[@id='labels']/form[2]/table/tbody/tr["+str(rowNo)+"]/td[2]/span"
#            if sel.is_element_present(titleElement):
#                tempTitle = sel.get_text(titleElement)
#                for item in videoList:
#                    if item==tempTitle:
#                        print "Found video "+item+" in the list of rejected videos"
#        page = page+1
#        rejectedURL = testvars.MCTestVariables["BulkEditPage"]+"/?category=&author=&filter=rejected&q=&page="+str(page)
#        sel.open(rejectedURL)
#        sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])
    


# =======================================
# =             CLEAR QUEUE             =
# =======================================

# This subroutine clears the entire queue

def ClearQueue(self,sel):
    NavigateToReviewQueue(self,sel)
    # Memorize the list of video titles on the page
    print "Memorizing the list of videos found on page 1..."
    videoList = ['']
    for i in range(1,11):
        titleLink = "//div[@id='admin_videolisting_row']/div["+str(i)+"]/div[1]/h3/a"
        if sel.is_element_present(titleLink)==True:
            newTitle=sel.get_text(titleLink)
            videoList.append(newTitle)
        else:
            pass
    # Check if there are any videos in the queue for the test to run
    if sel.is_element_present("//div[@id='admin_videolisting_row']/div[1]")==False:
        self.fail("No videos found on the queue page. Not enough test data to run the test.")
    print "Memorizing the list of videos found on the last page..."
    pageLink = testvars.MCTestVariables["ReviewQueuePage"]+"/?page=1000000"
    try:
        sel.open(pageLink)
        sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])
    except: pass
    time.sleep(5)
    for i in range(1,11):
        titleLink = "//div[@id='admin_videolisting_row']/div["+str(i)+"]/div[1]/h3/a"
        if sel.is_element_present(titleLink)==True:
            newTitle=sel.get_text(titleLink)
            videoList.append(newTitle)
        else:
            pass
    videoList.remove('')
    print "Found the following videos on the first and last pages of the queue:"
    print videoList
    # Clear queue
    clearButton = "//div[@id='content']/a[3]/span"
    if sel.is_element_present(clearButton)==False: # If clear button not found
        mclib.AppendErrorMessage(self,sel,"'Clear Queue' button not found")
    else:
        sel.click(clearButton)
        sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])
        sel.click("confirm")
        sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])
        print "Cleared queue" 
        # Checking that the queue contains no videos for moderation
        print "Checking that the queue is cleared..."
        titleLink = "//div[@id='admin_videolisting_row']/div[1]/div[1]/h3/a"
        if sel.is_element_present(titleLink)==True:
            mclib.AppendErrorMessage(self,sel,"Found a video in the queue")
        else:
            if sel.is_text_present("You have no videos that need reviewing")==False:
                mclib.AppendErrorMessage(self,sel,"Expected text message 'You have no videos that need reviewing' not found")
            else:
                print "OK"
        return videoList
    


# =======================================
# =          EDIT VIDEO IN QUEUE        =
# =======================================

# This subroutine edits the parameters of the video No. <number> on page <page>.
# <page> should be a string variable (a numeral or "Last")
# <number> should be a numeric between 1 and 10; numbers greater than 10
# are treated as 10
# <title> - new title
# <user> - new author associated with the video
# <posted> - new submission date
# <thumbnail> - new thumb image (can be URL or file name and path)
# <description> - new description
# <category> - new category associated with the video
# <tag> - new tag for the video
# <website> - a new website URL

def EditVideoInQueue(self,sel,page,number,title,user,posted,thumbnail,description,category,tag,website):
    NavigateToReviewQueue(self,sel)
    if page=="Last": pageNo = "1000000"
    else: pageNo = page
    # Construct the URL of the page in the queue with the given number
    pageLink = testvars.MCTestVariables["ReviewQueuePage"]+"/?page="+pageNo
#    print pageLink
    try:
        sel.open(pageLink)
        sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])
    except:
        time.sleep(10)
        pass
        #self.fail("Could not open page "+pageNo+" in the queue")
    # Construct the link for approving a video with its number on the page
    if number > 10: number=10
    elif number < 1: number=1
    # Open the selected video for preview
    titleLink = "//div[@id='admin_videolisting_row']/div["+str(number)+"]/div[1]/h3/a"
#    print titleLink
    if sel.is_element_present(titleLink)==False:
        self.fail("Link to selected video not found. Not enough data to run the test")
    else:
        oldTitle = ""
        oldTitle = sel.get_text(titleLink)
        print "Old video title is: "+oldTitle
        sel.click(titleLink)
        time.sleep(5)
#        sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])
        # Edit video parameters
        if title!="":
            print "Changing video title..."
            sel.click("//div[@id='admin_rightpane']/div/div[1]/div/div[1]/h2/a/span")
            time.sleep(3)
            sel.type("id_name", title)
            sel.click("//button[@type='submit']")
            time.sleep(5)
            # Checking new video title
            newTitleUntrimmed = sel.get_text("//div[@id='admin_rightpane']/div/div[1]/div/div[1]/h2")
            newTitle = newTitleUntrimmed.replace(' Edit','')
            if newTitle!=title:
                mclib.AppendErrorMessage(self,sel,"The video TITLE was updated incorrectly.")
                print "Expected title: "+title
                print "- Actual title: "+newTitle
            else:
                print "OK"
        if user!="":
            oldUsers = sel.get_text("//div[@id='admin_rightpane']/div/div[2]/div[1]/div[1]")
            print "Old author(s) - "+oldUsers.replace('Edit','')
            if oldUsers.find(user)!=-1:
                print "Author "+user+" is already associated with this video. Skipping update."
            else:
                print "Adding new author..."
                sel.click("//div[@id='admin_rightpane']/div/div[2]/div[1]/div[1]/a[@class='edit_link']")
                time.sleep(3)
                rowNo=1
                authorCaption = "//div[@id='admin_rightpane']/div/div[2]/div[1]/div[2]/form/ul/li/ul/li["+str(rowNo)+"]/label/span"
                while sel.is_element_present(authorCaption):
                    tempAuth = sel.get_text(authorCaption)
                    if tempAuth==user:
                        break
                    rowNo = rowNo + 1
                    authorCaption = "//div[@id='admin_rightpane']/div/div[2]/div[1]/div[2]/form/ul/li/ul/li["+str(rowNo)+"]/label/span"
                if tempAuth==user:
                    sel.click("id_authors_"+str(rowNo-1))
                else:
                    mclib.AppendErrorMessage(self,sel,"Author "+author+" not found")
                sel.click("//button[@type='submit']")
                time.sleep(8)
                sel.refresh()
                sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])
                newUsers = sel.get_text("//div[@id='admin_rightpane']/div/div[2]/div[1]/div[1]")
                print "List of new authors: "+newUsers.replace('Edit','')
                if newUsers.find(user)==-1:
                    mclib.AppendErrorMessage(self,sel,"The AUTHOR was updated incorrectly.")
                    print "Expected authors: "+oldUsers.replace('Edit','')+" "+user
                    print "- Actual authors: "+newUsers
                else:
                    print "OK"
        if posted!="":
            oldPosted = sel.get_text("//div[@id='admin_rightpane']/div/div[2]/div[2]/div[1]")
            print "Old date: "+oldPosted
            print "Changing posted date..."
            sel.click("//div[@id='admin_rightpane']/div/div[2]/div[2]/div[1]/span")
            time.sleep(10)
            sel.type("id_when_published", posted)
            sel.click("//button[@type='submit']")
            time.sleep(5)
            # Checking new date
            # TO DO - when the bug is fixed
        if description!="":
            oldDescription = sel.get_text("//div[@id='admin_rightpane']/div/div[5]/div[1]/div")
            print "Old description: "+oldDescription
            print "Changing description..."
            sel.click("//div[@id='admin_rightpane']/div/div[5]/div[1]/h4/a")
            time.sleep(3)
            sel.type("id_description", description)
            sel.click("//button[@type='submit']")
            time.sleep(5)
            # Checking new description
            newDescription = sel.get_text("//div[@id='admin_rightpane']/div/div[5]/div[1]/div")
            if newDescription!=description:
                mclib.AppendErrorMessage(self,sel,"The video DESCRIPTION was updated incorrectly.")
                print "Expected description: "+description
                print "- Actual description: "+newDescription
            else:
                print "OK"
        if category!="":
            if sel.is_element_present("//div[@id='tags']/ul/li[1]/div/div[1]/div/ul"):
                oldCatList = sel.get_text("//div[@id='tags']/ul/li[1]/div/div[1]/div/ul")
            else:
                oldCatList = ""
            print "List of old categories: "+oldCatList
            if category in oldCatList:
                print "Category "+category+" is already associated with this video. Skipping update."
            else:
                print "Adding new category..."
                sel.click("//a[@id='add_cat']/span")
                time.sleep(3)
                rowNo=1
                catCaption = "//div[@id='tags']/ul/li[1]/div/div[2]/form/ul/li/ul/li["+str(rowNo)+"]/label/span"
                while sel.is_element_present(catCaption):
                    tempCat = sel.get_text(catCaption)
                    if tempCat==category:
                        break
                    rowNo = rowNo + 1
                    catCaption = "//div[@id='tags']/ul/li[1]/div/div[2]/form/ul/li/ul/li["+str(rowNo)+"]/label/span"
                if tempCat==category:
                    sel.click("id_categories_"+str(rowNo-1))
                else:
                    mclib.AppendErrorMessage(self,sel,"Category "+category+" not found")
                sel.click("//button[@type='submit']")
                time.sleep(8)
                newCatList = sel.get_text("//div[@id='tags']/ul/li[1]/div/div[1]/div/ul")
                print "List of new categories: "+newCatList
                if newCatList.find(category)==-1:
                    mclib.AppendErrorMessage(self,sel,"The CATEGORY was updated incorrectly.")
                    expectedCatList = oldCatList.split(' ')
                    print "Expected categories: "+' '.join(sorted(expectedCatList.append(category)))
                    print "- Actual categories: "+newCatList
                else:
                    print "OK"
        if tag!="":
            tagListElement = "//div[@id='tags']/ul/li[2]/div/div[1]/div/ul"
            if sel.is_element_present(tagListElement):
                oldTags = sel.get_text(tagListElement)
            else: # Tag list not found on page
                oldTags = ""
            print "List of old tags: "+oldTags
            if tag in oldTags:
                print "Tag "+tag+" is already associated with this video. Skipping update."
            else:
                sel.click("//div[@id='tags']/ul/li[2]/div/div[1]/div/h4/a")
                time.sleep(5)
                existingTagList = sel.get_text("id_tags")
                if existingTagList=="":
                    updatedTags = tag
                else:
                    if existingTagList.find(',')!=-1:
                        updatedTags = existingTagList + ", " + tag
                    else:
                        updatedTags = existingTagList + " " + tag
                print "Adding new tag..."
                sel.type("id_tags", updatedTags)
                sel.click("//button[@type='submit']")
                time.sleep(5)
                if sel.is_element_present(tagListElement)==False:
                    mclib.AppendErrorMessage(self,sel,"List of tags for the video not found")
                else:
                    newTags = sel.get_text("//div[@id='tags']/ul/li[2]/div/div[1]/div/ul")
                    print "List of new tags: "+newTags
                    print "Checking if the tags were updated properly..."
                    if oldTags!=((newTags.replace(tag,'')).replace('  ',' ')).strip() or newTags.find(tag)==-1:
                        mclib.AppendErrorMessage(self,sel,"The video TAGS were updated incorrectly.")
                        print "Expected tags: "+' '.join(sorted(updatedTags.split(' ')))
                        print "- Actual tags: "+newTags
#                        print (newTags.replace(tag,'')).replace('  ',' ')
                    else:
                        print "OK"

        if website!="":
            oldURL=sel.get_text("//div[@id='tags']/ul/li[3]/div/div[1]/div/span/a")
            print "Old website URL: "+oldURL
            print "Updating the website URL..."
            sel.click("//div[@id='tags']/ul/li[3]/div/div[1]/div/h3/a/span")
            time.sleep(3)
            sel.type("id_website_url",website)
            sel.click("//button[@type='submit']")
            time.sleep(5)
            newURL = sel.get_text("//div[@id='tags']/ul/li[3]/div/div[1]/div/span/a")
            print "New website URL: "+newURL
            if newURL!=website:
                mclib.AppendErrorMessage(self,sel,"The video WEBSITE URL was updated incorrectly.")
                print "Expected website URL: "+website
                print "- Actual website URL: "+newURL
            else:
                print "OK"
        if thumbnail!="":
            print "Uploading new thumbnail..."
            print "Source image: "+thumbnail
            sel.click("link=Upload/Replace Thumbnail")
            time.sleep(3)
            if thumbnail.find("http:")!=-1:
                sel.type("id_thumbnail_url",thumbnail)
            else:
                sel.type("id_thumbnail",thumbnail)
            sel.click("//button[@type='submit']")
            print "OK"
            time.sleep(5)
    


# =======================================
# =            VIEW RSS FEEDS           =
# =======================================

# This subroutine opens RSS feeds with videos awaiting moderation
# and checks relevant pages
# <feed> must be = "Unapproved RSS" or "Unapproved User RSS"

def ViewRSSFeeds(self,sel,feed):
    NavigateToReviewQueue(self,sel)
    if (feed!="Unapproved RSS" and feed!="Unapproved User RSS"):
        self.fail("Wrong parameter passed to ViewRSSFeeds subroutine")
    # Retrieving site title in order to check the feed title
    if sel.is_element_present("//div[@id='logo']/h1/a"):
        siteTitle = sel.get_text("//div[@id='logo']/h1/a")
    else:
        mclib.AppendErrorMessage(self,sel,"Cannot find site title on the administrator pages")
        siteTitle=""
    RSSFeedLink = "link="+feed
    if sel.is_element_present(RSSFeedLink)==False:
        if sel.is_text_present("You have no videos that need reviewing.")==False:
            mclib.AppendErrorMessage(self,sel,feed+" link not found")
        else:
            print "Queue is empty. RSS feed is unavailable"
    else:
        sel.click(RSSFeedLink)
        sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])
        expectedTitle = siteTitle + ":"+ " Videos Awaiting Moderation"
        print "Checking the feed title..."
        if sel.is_element_present("feedTitleText")==True:
            actualTitle = sel.get_text("feedTitleText")
            if actualTitle!=expectedTitle:
                mclib.AppendErrorMessage(self,sel,"Unexpected feed title found")
                print "Expected title: "+expectedTitle
                print "- Actual title: "+actualTitle
            else:
                print "OK"
        print "Searching for videos in the RSS feed..."
        videoEntryItems = ['']
        if sel.is_element_present("feedContent")==True:
            videosCount=sel.get_xpath_count("//x:div[@id='feedContent']/x:div")
            print "Found "+videosCount+" videos"
            if videosCount > 0:
                print "Checking the first video in feed..."
                #print sel.get_text("//x:div[@id='feedContent']/x:div[1]")
                videoTitleElement= "//x:div[@id='feedContent']/x:div[1]/x:h3/x:a"
                if sel.is_element_present(videoTitleElement)==False:
                    mclib.AppendErrorMessage(self,sel,"Video title not found")
                else:
                    videoTitleText = sel.get_text(videoTitleElement)
                    videoTitleLink = sel.get_attribute(videoTitleElement+"@href")
                    print "Video title: "+videoTitleText
                    print "Video page: "+videoTitleLink
                    expectedVideoTitleLink = testvars.MCTestVariables["TestSite"]+"video/"
                    if videoTitleLink.find(expectedVideoTitleLink)==-1:
                        mclib.AppendErrorMessage(self,sel,"Expected link in the video title not found")
                        print "Expected to find in the title link: "+expectedVideoTitleLink
                        print "Actual link: "+videoTitleLink
                    expectedThumbnailLink = videoTitleLink.replace(testvars.MCTestVariables["TestSite"],'/') # removing site name from the link
                    thumbnailLink = sel.get_attribute("//x:div[@id='feedContent']/x:div[1]/x:div[1]/table/tr/td[1]/a@href")
                    if thumbnailLink!=expectedThumbnailLink:
                        mclib.AppendErrorMessage(self,sel,"Thumbnail does not point to the video page as expected")
                        print "Expected thumbnail link: "+expectedThumbnailLink
                        print "Actual link: "+thumbnailLink
                    authorElement = "//x:div[@id='feedContent']/x:div[1]/x:div[1]/table/tr/td[3]/div[1]/a"
                    if sel.is_element_present(authorElement)==False:
                        print "Video author not found in RSS"
                    else:
                        print "Video author: "+sel.get_text(authorElement)
                        authorLink = sel.get_attribute(authorElement+"@href")
                        expectedAuthorLink = "author/"
                        if authorLink.find(expectedAuthorLink)==-1:
                            mclib.AppendErrorMessage(self,sel,"Expected author link not found")
                            print "Expected to find in the author link: "+expectedAuthorLink
                            print "Actual link: "+authorLink
                    tagListElement = sel.get_text("//x:div[@id='feedContent']/x:div[1]/x:div[1]/table/tr/td[3]/div[3]")
                    if sel.is_element_present(tagListElement)==False:
                        print "Tag list for the video not found in RSS"
                    else:
                        tagList = sel.get_text(tagListElement)
                        if tagList.find("Tags:")==-1:
                            mclib.AppendErrorMessage(self,sel,"Expected tag list not found")
                        print tagList
                    originalLinkElement="//x:div[@id='feedContent']/x:div[1]/x:div[1]/table/tr/td[3]/div[4]"
                    if sel.is_element_present(originalLinkElement)==False:
                        print "Original link to the video not found in RSS"
                    else:
                        originalLink = sel.get_text(originalLinkElement)
                        if originalLink.find("Original link:")==-1:
                            mclib.AppendErrorMessage(self,sel,"Expected original link not found in RSS feed")
                        else:
                            originalLinkURL = originalLink.replace("Original link:",'')
                        print originalLink
                    watchLink = "//x:div[@id='feedContent']/x:div[1]/x:div[2]/x:div/x:a"
                    watchLinkURL = sel.get_attribute(watchLink+"@href")
                    print "Original video URL under 'Watch' link: "+watchLinkURL
#                if watchLinkURL!=originalLinkURL:
#                    mclib.AppendErrorMessage(self,sel,"Expected original video URL not found in 'Watch' link")
#                    print "Found: "+watchLinkURL
        else:
            print "Could not find any videos in this RSS feed"


# =======================================
# =         FIND VIDEO IN QUEUE         =
# =======================================

# This function returns page number and video number for a video
# in the premoderation queue
# If not found, the function returns [0,0]

def FindVideoInQueue(self,sel,title):
    resRow = 0
    resPage = 0
    page = 1
    firstVideoOnPreviousPage = 'some_dummy_text'
    try:
        sel.open(testvars.MCTestVariables["ReviewQueuePage"]+"/?page="+str(page))
        sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])
    except: pass
    time.sleep(10)
    row = 1
    titleElement = "//div[@id='admin_videolisting_row']/div["+str(row)+"]/div[1]/h3/a"
    if sel.is_element_present(titleElement)==True:
        firstVideoOnCurrentPage = sel.get_text(titleElement)  # Memorizing the first title on the page for page identification
    else:
        firstVideoOnCurrentPage = firstVideoOnPreviousPage
    while firstVideoOnCurrentPage!=firstVideoOnPreviousPage:  # page increment produces a new page, rather than reopens the previous page
        # Cycle through all videos on the page 
        while sel.is_element_present(titleElement)==True:
            tempTitle = sel.get_text(titleElement)
            #print tempTitle
            if tempTitle==title:
                break
            row = row+1
            titleElement = "//div[@id='admin_videolisting_row']/div["+str(row)+"]/div[1]/h3/a"
        if tempTitle==title:
            resRow = row
            resPage = page
            break
        page = page + 1
        try:
            sel.open(testvars.MCTestVariables["ReviewQueuePage"]+"/?page="+str(page))
            sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])
        except: pass
        #print "Opened page "+str(page)
        time.sleep(10)
        row = 1
        titleElement = "//div[@id='admin_videolisting_row']/div["+str(row)+"]/div[1]/h3/a"
        firstVideoOnPreviousPage = firstVideoOnCurrentPage
        firstVideoOnCurrentPage = sel.get_text(titleElement)
    return [resPage,resRow]



# =======================================
# =       REJECT VIDEO FROM QUEUE       =
# =======================================

# This subroutine checks if the video being submitted is in the premoderation queue ("Unapproved") 
# If yes, rejects it
# <title> should be in Unicode format

def RejectVideoFromQueue(self,sel,title):
    videoLocation = FindVideoInQueue(self,sel,title)
    if videoLocation!=[0,0]:
        print "Found video '"+title+"' in the review queue. Preparing to reject it..."
        page = str(videoLocation[0])
        number = videoLocation[1]
        action = "Rejected"
        ProcessVideo(self,sel,page,number,action)
    else:
        print "Could not find video '"+title+"' in the premoderation queue"

