# Module SOURCES.PY
# includes:
#   * function SourceLocation(self,sel,source) - returns [page number,row number] on 
#                /admin/manage where the desired source is placed and [0,0] if the
#                source not found
#   * function GetSourceList(self,sel) - returns the list of all the sources
#   * function SearchForVideos(self,sel,searchterm,sortby) - searches for a term searchterm
#                and returns the number of videos on the first result page
#                sortby = 0 - "Latest"
#                       = 1 - "Relevance"
#   * subroutine AttributeCategoryToSource(self,sel,category) - checks the check box
#                for the desired category on the source feed submission page
#   * subroutine AttributeUserToSource(self,sel,username) - checks the check box
#                for the desired user on the source feed submission page
#   * subroutine DeleteSource(self,sel,source) - deletes source from the system
#   * subroutine AddSource(self,sel,sourceURL,autoApprove,category,user) - adds new
#                user feed with URL <sourceURL> to the system.
#                autoApprove = 1 - Approve All (current and future)
#                            = 0 - Review Them First
#                category - associated category
#                user - associated user
#   * subroutine AddDuplicateSource(self,sel,sourceURL) - attempts to add a duplicate
#                source feed with URL <sourceURL> to the system and checks for the
#                expected error message
#   * subroutine SearchForVideos(self,sel,searchterm,sortby) - searches for a term 
#                searchterm
#   * subroutine AddSearchFeed(self,sel,searchterm,sortby) - searches for a term 
#                searchterm and saves results as a feed
#                sortby = 0 - "Latest"
#                       = 1 - "Relevance"
#   * subroutine EditSource(self,sel,sourceName,sourceNewname,sourceURL,sourceSite,
#                category,user) - updates the following parameters for a <sourceName> source:
#                sourceNewname - name
#                sourceURL - URL 
#                category - adds another associated category
#                user - adds another associated user
#   * subroutine MarkListedSources(self,sel,sourcelist) - mark all the sources in the sourcelist
#                for bulk operations. All the sources should be on the same page
#   * subroutine BulkEditSource(self,sel,sourcelist,autoApprove,category,user) - updates 
#                the following parameters for a few sources listed in <sourcelist> at a time:
#                autoApprove = 1 - On
#                            = 0 - Off
#                category - adds another associated category
#                user - adds another associated user
#   * subroutine BulkDeleteSource(self,sel,sourcelist) - deletes the sources included
#                in sourcelist
#   * subroutine SortSources(self,sel,parameter,order) - sorts the list of sources by parameter
#                Parameter can take one of the following values: Name, Type, AutoApprove
#                Order can be set to Asc (ascending) or Desc (descending)
#   * subroutine SearchInSources(self,sel,category,author,query) - searches for sources in the list 
#                of sources by <query>, <category>, and/or <author>
#   * subroutine FilterSources(self,sel,filter) - filters sources by type (<filter>), which
#                can take values "All", "Users", "Searches", or "Feeds"


from selenium import selenium

import unittest, time, re, urllib
import testvars, mclib

def NavigateToManageSources(self,sel):
    sel.set_timeout(150000)
    sel.open(testvars.MCTestVariables["ManageSourcesPage"])
    sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])
    try: self.failUnless(sel.is_text_present("Manage Your Video Sources"))
    except AssertionError, e:
#        self.verificationErrors.append("Not logged in as an Administrator")
        self.fail("Not logged in as an Administrator")
    

# =======================================
# =        FIND SOURCE IN THE LIST      =
# =======================================

# This function returns the row number for the desired source
# on /manage pages.
# Returns [page number,row number] if the source is found and [0,0] otherwise.

def SourceLocation(self,sel,source):
    sel.set_timeout(150000)
    page = 1 # page number
    tempSource = ""
    try:
        sel.open(testvars.MCTestVariables["ManageSourcesPage"]+"/?page="+str(page))
        sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])
    except: pass
    while sel.is_text_present("Page not found")==False:
#        if sel.is_element_present("css=span.overflow:contains("+source+")"):
#            row = Evaluate("count(//tr[td/span[contains(text(),'Croatia')]]/preceding-sibling::*)")+1
#            break
        row = 0   # row number
        tempSource=""
        # Only one source on the page? If not, go ahead
        sourceTableCell="//div[@id='labels']/form[2]/table/tbody/tr/td[2]/span"  # no row number in the link
        if sel.is_element_present(sourceTableCell):
            if sel.get_text(sourceTableCell)==source:
                row = 1
                return [page,row]
        # Name of the first source in the list - for multiple rows on the page
        row = 1
        sourceTableCell="//div[@id='labels']/form[2]/table/tbody/tr[1]/td[2]/span"
        while sel.is_element_present(sourceTableCell):
            tempSource = sel.get_text(sourceTableCell)
            if tempSource==source:
                break
            row=row+1
            sourceTableCell="//div[@id='labels']/form[2]/table/tbody/tr["+str(row)+"]/td[2]/span"
        if tempSource==source:
            break
        # End of page reached?
        page = page+1
        try:
            sel.open(testvars.MCTestVariables["ManageSourcesPage"]+"/?page="+str(page))
            sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])
        except: pass
    # Return results
    if tempSource==source:
        return [page,row] 
    else:
        return [0,0]


        
#        row = 0   # row number
#        tempSource=""
        # Only one source on the page? If not, go ahead
#        sourceTableCell="//div[@id='labels']/form[2]/table/tbody/tr/td[2]/span"  # no row number in the link
#        if sel.is_element_present(sourceTableCell):
#            if sel.get_text(sourceTableCell)==source:
#                return [page,row]
        # Name of the first source in the list - for multiple rows on the page
#        row = 1
#        sourceTableCell="//div[@id='labels']/form[2]/table/tbody/tr[1]/td[2]/span"
#        while sel.is_element_present(sourceTableCell):
#            tempSource = sel.get_text(sourceTableCell)
#            if tempSource==source:
#                break
#            row=row+1
#            sourceTableCell="//div[@id='labels']/form[2]/table/tbody/tr["+str(row)+"]/td[2]/span"
#        if tempSource==source:
#            break
        # End of page reached?
#        page = page+1
#        try:
#            sel.open(testvars.MCTestVariables["ManageSourcesPage"]+"/?page="+str(page))
#            sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])
#        except: pass
    # Return results
#    if tempSource==source:
#        return [page,row] 
#    else:
#        return [0,0]


# =======================================
# =           GET SOURCE LIST           =
# =======================================

# This function returns the list of all the sources in the system

def GetSourceList(self,sel):
    sel.set_timeout(testvars.MCTestVariables["TimeOut"])
    print "Retrieving the current list of sources..."
    page = 1 # page number
    sel.open(testvars.MCTestVariables["ManageSourcesPage"]+"/?page="+str(page))
    sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])
    sourceList=['']
    no = 1    
    while sel.is_text_present("Page not found")==False:
        row = 0   # row number
        tempSource=""
        # Only one source on the page? If not, go ahead
        sourceTableCell="//div[@id='labels']/form[2]/table/tbody/tr/td[2]/span"  # no row number in the link
        if sel.is_element_present(sourceTableCell):
            tempSource = sel.get_text(sourceTableCell)
            sourceList.append(tempSource)
            no = no + 1
        # Name of the first source in the list - for multiple rows on the page
        row = 2
        sourceTableCell="//div[@id='labels']/form[2]/table/tbody/tr["+str(row)+"]/td[2]/span"
        while sel.is_element_present(sourceTableCell):
            tempSource = sel.get_text(sourceTableCell)
            row=row+1
            sourceList.append(tempSource)
            no = no + 1
            sourceTableCell="//div[@id='labels']/form[2]/table/tbody/tr["+str(row)+"]/td[2]/span"
        # End of page reached?
        page = page+1
        try:
            sel.open(testvars.MCTestVariables["ManageSourcesPage"]+"/?page="+str(page))
            sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])
        except: pass
    # If list not empty, remove the blank item
    if no>1:
        sourceList.remove("")
    return sourceList



# =======================================
# =          SEARCH FOR VIDEOS          =
# =======================================

# This function searches for a term searchterm
# and returns the number of videos on the first result page
# sortby = 0 - "Latest"
#        = 1 - "Relevance"

def SearchForVideos(self,sel,searchterm,sortby):
    NavigateToManageSources(self,sel)
    res = 0
    buttonSearchForVideo = "//div[@id='content']/a[1]/span"
    # Check that Search For Video button is present
    print "Checking that 'Search for Video' button is available"
    if sel.is_element_present(buttonSearchForVideo)==False or sel.is_visible(buttonSearchForVideo)==False:
        mclib.AppendErrorMessage(self,sel,"Search for Video button not found")
    else:
        print "OK"
        sel.click(buttonSearchForVideo)
        time.sleep(2)
        print "Looking for 'Search Video Sites' pop-up..."
        if sel.is_element_present('admin_search_sources')==False:
            mclib.AppendErrorMessage(self,sel,"Search Video Sites pop-up not found")
        else:
            print "OK"
            print "Entering search criteria..."
            if sel.is_element_present("query")==False:
                mclib.AppendErrorMessage(self,sel,"Query edit field not found")
            else:
                sel.type("query", searchterm)
            selectSortby = "//div[@id='admin_search_sources']/form/span/select"
            if sel.is_element_present(selectSortby)==False:
                mclib.AppendErrorMessage(self,sel,"Sort By drop-down list not found")
            else:
                if sortby == 0: sel.select(selectSortby, "label=Latest")
                elif sortby == 1: sel.select(selectSortby, "label=Relevance")
                else: print "Invalid value of sortby argument provided. Ignored this parameter."
            submitButton = "//div[@id='admin_search_sources']/form/button"
            if sel.is_element_present(submitButton)==False:
                mclib.AppendErrorMessage(self,sel,"Search button on Search Video Sites pop-up not found")
            else:
                print "Submitting search criteria..."
                sel.click(submitButton)
                sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])
                # Check that the loaded page is the search results page indeed 
                print "Checking the URL of the page with query results..."
#                searchtermSlug = searchterm.replace(" ","+")
#                print searchtermSlug
#                expectedURL = "http://dalmatia.mirocommunity.org/admin/manage/search/?query="+urllib.quote(searchtermSlug.encode('utf-8'))
#                print urllib.quote(searchtermSlug.encode('utf-8'))
                searchtermSlug = urllib.quote(searchterm.encode('utf-8'))
                expectedURL = testvars.MCTestVariables["TestSite"]+"admin/manage/search/?query="+searchtermSlug.replace("%20","+")
                print expectedURL
                actualURL = sel.get_location()
                if actualURL!=expectedURL:
                    mclib.AppendErrorMessage(self,sel,"Wrong page URL encountered")
                    print "Expected URL: "+expectedURL
                    print "- Actual URL: "+actualURL
                else:
                    print "OK"
                print "Checking the title of the page with query results..."
                if sel.is_text_present("Searched Video Sites for \""+searchterm+"\"")==False:
                    mclib.AppendErrorMessage(self,sel,"Wrong title on search results page")
                    print "Expected title: "+"Searched Video Sites for \""+searchterm+"\""
                else:
                    print "OK"
                    res = sel.get_xpath_count("//div[@id='admin_videolisting_row']/div") 
                    print str(res)+" videos found on the first results page"
                    return res




# =======================================
# =    ATTRIBUTE CATEGORY TO SOURCE     =
# =======================================

# This subroutine checks the check box for the desired category on the source feed submission page

def AttributeCategoryToSource(self,sel,category):
#    if sel.is_element_present("//div[@id='content']/form/div[3]/ul/li[1]/ul")==True:
    if sel.is_element_present("css=div.input_field ul li.scrollable:nth-child(1)")==False:
        mclib.AppendErrorMessage(self,sel,"List of categories not found")
    else:
        catCheckbox = "//div[@class='input_field']/ul/li[1]/ul/li[contains(./label/span,'"+category+"')]/label/input[@name='auto_categories']"
        if sel.is_element_present(catCheckbox) == False:
            mclib.AppendErrorMessage(self,sel,"Category not found: "+category)
        else:
            sel.check(catCheckbox)



# =======================================
# =       ATTRIBUTE USER TO SOURCE      =
# =======================================

# This subroutine checks the check box for the desired user on the source feed submission page

def AttributeUserToSource(self,sel,username):
#    if sel.is_element_present("//div[@id='content']/form/div[3]/ul/li[2]/ul")==False:
    if sel.is_element_present("css=div.input_field ul li.scrollable:nth-child(2)")==False:
        mclib.AppendErrorMessage(self,sel,"List of users not found")
    else:
        userBox = "//li/label[span='"+username+"']/input[@name='auto_authors']"
        if sel.is_element_present(userBox)==False:
            mclib.AppendErrorMessage(self,sel,"Checkbox for user "+username+" not found")
        else:
            sel.check(userBox)



# =======================================
# =           DELETE SOURCE             =
# =======================================

# This subroutine deletes a source feed from the system.

def DeleteSource(self,sel,source):
    sourceLoc = SourceLocation(self,sel,source)
    if sourceLoc!=[0,0]:
        page = sourceLoc[0]
        rowNo = sourceLoc[1]
        if rowNo == 0:
            row = ""
        else:
            row = "["+str(rowNo)+"]"
        print "Deleting source "+source+"..."
        sel.set_timeout("150000")
        sel.open(testvars.MCTestVariables["ManageSourcesPage"]+"/?page="+str(page))
        sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])
        deleteLink="//div[@id='labels']/form[2]/table/tbody/tr"+str(row)+"/td[2]/div/a[2]"
        if sel.is_element_present(deleteLink)==True:
            sel.click(deleteLink)
            time.sleep(2)
            if sel.get_confirmation()=="Press OK to delete all videos from this source.":
#                sel.click("//div[@id='massedit']/button")
                print "Confirming deletion..."
            else:
                mclib.AppendErrorMessage(self,sel,"Confirmation to delete the source not requested")
            time.sleep(3)
            sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])
            if SourceLocation(self,sel,source)!=[0,0]:
#            if sel.is_text_present(source)==True:
                mclib.AppendErrorMessage(self,sel,"Failed to delete source: "+source)
            else:
                print "Successfully deleted source: "+source
        else:
            mclib.AppendErrorMessage(self,sel,"Could not find Delete link for source: "+source)
    else:
        mclib.AppendErrorMessage(self,sel,"Could not find source to be deleted: "+source)
        
    

# =======================================
# =              ADD SOURCE             =
# =======================================

# This subroutine adds a new source feed with URL <sourceURL> to the system.
# autoApprove = 1 - Approve All (current and future)
#             = 0 - Review Them First
# category - associated category

def AddSource(self,sel,sourceURL,autoApprove,category,user):
    NavigateToManageSources(self,sel)
    buttonAddFeed = "//div[@id='content']/a[2]/span"
    # Check that Add Feed button is present
    if sel.is_element_present(buttonAddFeed)==False or sel.is_visible(buttonAddFeed)==False:
        mclib.AppendErrorMessage(self,sel,"Add Feed button not found")
    else:
        sel.click(buttonAddFeed)
        time.sleep(2)
        # Is the Add a Source pop-up displayed?
        if sel.is_element_present("admin_feed_add")==False or sel.is_visible("admin_feed_add")==False:
            mclib.AppendErrorMessage(self,sel,"Add Sources of Video Pop-up not found")
        else:
            # Pop-up is present - now enter the source URL and save
            sel.type("id_feed_url",sourceURL)
            sel.click("//button[@type='submit']")
            sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])
            #=================== STEP 2 ==========================
            # Did the second page of source add process appear?
            if sel.is_text_present("Review Feed Before Adding")==False:
                mclib.AppendErrorMessage(self,sel,"Review Feed Before Adding page not found at step 2")
            else:
                # Get the title of the feed
                feedName = "css=div#content form div.floatleft h3"
                if sel.is_element_present(feedName)==True:
                    sourceName = sel.get_text(feedName)
                    print "Preparing to import feed: "+sourceName
                else:
                    mclib.AppendErrorMessage(self,sel,"Feed name is not displayed at Review Feed page")
                # Get the estimated number of videos
                #print "Pre-import estimate: "+sel.get_text("//div[@id='content']/form/div[2]/div/span")
                print "Pre-import estimate: "+sel.get_text("css=div#content form div.floatleft div.video_count span")
                # Set Approve All, if appropriate
                if autoApprove==1:
                    if sel.is_element_present("id_auto_approve_0")==True:
                        sel.click("id_auto_approve_0")
                    else:
                        mclib.AppendErrorMessage(self,sel,"Approve all videos (current and future) radio button not found")
                # Attribute to a category, if appropriate
                if category!="":
                    AttributeCategoryToSource(self,sel,category)
                # Attribute to a user, if appropriate
                if user!="":
                    AttributeUserToSource(self,sel,user)
                # Click the button to complete import
                sel.click("//div[@id='content']/form/button[2]")
                sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])
                print "Importing feed..."
                # Wait for import to complete
                timeElapsed = 0
                if autoApprove==1:
                    nextLink = "See these videos"
                else:
                    nextLink = "Review these videos"
#                while sel.is_text_present(nextLink)==False and sel.is_text_present("Just a Moment")==True:
#                    time.sleep(1)
#                    timeElapsed = timeElapsed + 1
#                    if timeElapsed > 3600: # more than 60 mins
#                        break
#                sel.wait_for_condition('selenium.isTextPresent("'+nextLink+'")','3600000')
                sel.wait_for_condition('selenium.isElementPresent("link='+nextLink+'")','3600000')
                if sel.is_text_present(nextLink)==False:
                    mclib.AppendErrorMessage(self,sel,"Import was not successfully finished in 60 minutes")
                    return -1
                linkBackToManage = "link=go back to Manage Sources"
                if sel.is_element_present(linkBackToManage)==True:
                    sel.click(linkBackToManage)
                    sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])
                else:
                    mclib.AppendErrorMessage(self,sel,"Link 'Go back to Manage Sources' not found")
                    sel.open("admin/manage")
                    sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])
                print "Checking that the source feed was added..."
                checkSource = SourceLocation(self,sel,sourceName)
                if checkSource==[0,0]:
                    mclib.AppendErrorMessage(self,sel,"New source not found in the list of sources")
                else:
                    print "New feed successfully added to the system"
                    page = checkSource[0]
                    rowNo = checkSource[1]
                    if rowNo == 0:
                        row = ""
                    else:
                        row = "["+str(rowNo)+"]"
                    sel.open(testvars.MCTestVariables["ManageSourcesPage"]+"/?page="+str(page))
                    sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])
                    approveCell="//div[@id='labels']/form[2]/table/tbody/tr"+row+"/td[6]"
                    approveCellOn="//div[@id='labels']/form[2]/table/tbody/tr"+row+"/td[6]/a[1]"
                    approveCellOff="//div[@id='labels']/form[2]/table/tbody/tr"+row+"/td[6]/a[2]"
                    print "Checking the value of Approve All / Review First parameter..."
                    if sel.is_element_present(approveCell)==True:
                        if sel.is_visible(approveCellOn)==True and autoApprove==1: print "OK"
                        elif sel.is_visible(approveCellOff)==True and autoApprove==0: print "OK"
                        else:
                            if sel.is_visible(approveCellOn)==True:
                                approveValue = "On"
                            elif sel.is_visible(approveCellOff)==True:
                                approveValue = "Off"
                            mclib.AppendErrorMessage(self,sel,"Wrong value of Approve All / Review First parameter displayed")
                            print "Expected value: "+str(autoApprove)+" (Legend: 1 - On, 0 - Off)"
                            print "- Actual value: "+approveValue
                    else:
                        mclib.AppendErrorMessage(self,sel,"Value of Approve All / Review First parameter not found")
                    categoryCell="//div[@id='labels']/form[2]/table/tbody/tr"+row+"/td[3]"
                    if category!="":
                        print "Checking the value of Category parameter for the new source..."
                        if sel.is_element_present(categoryCell)==True:
                            if sel.get_text(categoryCell)!=category:
                                mclib.AppendErrorMessage(self,sel,"Wrong value of category displayed for the source")
                                print "Expected value: "+category
                                print "Actual value: "+sel.get_text(categoryCell)
                            else:
                                print "OK"
                        else:
                            mclib.AppendErrorMessage(self,sel,"Value of category parameter for the source not found")
                    userCell="//div[@id='labels']/form[2]/table/tbody/tr"+row+"/td[4]/span"
                    if user!="":
                        print "Checking the value of user parameter for the new source..."
                        if sel.is_element_present(userCell)==True:
                            if sel.get_text(userCell)!=user:
                                mclib.AppendErrorMessage(self,sel,"Wrong username displayed for the source")
                                print "Expected value: "+user
                                print "Actual value: "+sel.get_text(userCell)
                            else:
                                print "OK"
                        else:
                            mclib.AppendErrorMessage(self,sel,"Value of user parameter for the source not found")
                        
                
        
    
    
# =======================================
# =        ADD DUPLICATE SOURCE         =
# =======================================

# This subroutine attempts to add a duplicate source feed with URL <sourceURL> to the system.

def AddDuplicateSource(self,sel,sourceURL):
    NavigateToManageSources(self,sel)
    buttonAddFeed = "//div[@id='content']/a[2]/span"
    # Check that Add Feed button is present
    if sel.is_element_present(buttonAddFeed)==False or sel.is_visible(buttonAddFeed)==False:
        mclib.AppendErrorMessage(self,sel,"Add Feed button not found")
    else:
        sel.click(buttonAddFeed)
        time.sleep(2)
        # Is the Add a Source pop-up displayed?
        if sel.is_element_present("admin_feed_add")==False or sel.is_visible("admin_feed_add")==False:
            mclib.AppendErrorMessage(self,sel,"Add Sources of Video Pop-up not found")
        else:
            # Pop-up is present - now enter the source URL and save
            sel.type("id_feed_url",sourceURL)
            sel.click("//button[@type='submit']")
            sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])
            #=================== STEP 2 ==========================
            # Did the second page of source add process appear?
            print "Checking for the alert message about feed duplication..."
            if sel.is_text_present("* That feed already exists on this site.")==False:
                mclib.AppendErrorMessage(self,sel,"Alert message about feed duplication was not found")
            else:
                print "OK"



# =======================================
# =           ADD SEARCH FEED           =
# =======================================

# This subroutine searches for a term searchterm and saves results as a feed
# sortby = 0 - "Latest"
#        = 1 - "Relevance"

def AddSearchFeed(self,sel,searchterm,sortby):
    SearchForVideos(self,sel,searchterm,sortby)
    print "Saving search results as a source..."
    saveButton = "//div[@id='content']/a/span"
    if sel.is_element_present(saveButton)==False:
        mclib.AppendErrorMessage(self,sel,"Save as a Source button not found")
    else:
        sel.click(saveButton)
        sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])
        if sel.is_text_present("Searched Video Sites for \""+searchterm+"\"")==False:
            mclib.AppendErrorMessage(self,sel,"Wrong title on search results page")
            print "Expected title: "+"Searched Video Sites for \""+searchterm+"\""
            print "- Actual title: "+sel.get_text("//div[@id='content']/h2[2]")
        else:
            print "OK"
            if sel.is_text_present("This search is saved")==False:
                mclib.AppendErrorMessage(self,sel,"'This search is saved' message not found")
            sel.click(testvars.MCUI["AdminManageSources"])
            sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])
            print "Looking for new search feed in the list of sources..."
            sl = SourceLocation(self,sel,searchterm)
            if sl==[0,0]:
                mclib.AppendErrorMessage(self,sel,"New search feed not found")
            else:
                print "OK"
                print "Checking source type..."
                page = sl[0]
                rowNo = sl[1]
                if rowNo == 0:
                    row = ""
                else:
                    row = "["+str(rowNo)+"]"
                sel.open(testvars.MCTestVariables["ManageSourcesPage"]+"/?page="+str(page))
                sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])
                typeElement = "//div[@id='labels']/form[2]/table/tbody/tr"+row+"/td[5]"
                if sel.get_text(typeElement)!="Search":
                    mclib.AppendErrorMessage(self,sel,"Wrong type displayed for the new source feed")
                    print "Expected type: Search"
                    print "- Actual type: "+sel.get_text(typeElement)
                else:
                    print "OK"
                            




# =======================================
# =             EDIT SOURCE             =
# =======================================

# This subroutine updates the following parameters for a <sourceName> source:
# sourceNewname - name
# sourceURL - URL 
# category - adds another associated category
# user - adds another associated user

def EditSource(self,sel,sourceName,sourceNewname,sourceURL,sourceSite,category,user):
    NavigateToManageSources(self,sel)
    sourceLoc = SourceLocation(self,sel,sourceName)
    if sourceLoc==[0,0]:
        mclib.AppendErrorMessage(self,sel,"Could not find source to be edited: "+source)
    else:
        page = sourceLoc[0]
        rowNo = sourceLoc[1]
        if rowNo == 0:
            row = ""
        else:
            row = "["+str(rowNo)+"]"
        print "Editing source "+sourceName+"..."
        sel.open(testvars.MCTestVariables["ManageSourcesPage"]+"/?page="+str(page))
        sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])
        # Memorize feed URL for future reference
        feedLink="//div[@id='labels']/form[2]/table/tbody/tr"+row+"/td[2]/div/a[3]"
        feedURL = sel.get_attribute(feedLink+"/@href")
        print "The feed to be edited is on page: "+feedURL
        editLink="//div[@id='labels']/form[2]/table/tbody/tr"+row+"/td[2]/div/a[1]"
        if sel.is_element_present(editLink)==False:
            mclib.AppendErrorMessage(self,sel,"Could not find Edit link for source: "+source)
        else:
            sel.click(editLink)
            time.sleep(2)
            # Is the Editing pop-up displayed?
            editPopup = "//div[@id='labels']/form[2]/table/tbody/tr"+row+"/td[1]/div"
            if sel.is_element_present(editPopup)==False or sel.is_visible(editPopup)==False:
                mclib.AppendErrorMessage(self,sel,"Editing Pop-up not found")
            else:
                # Pop-up is present
                # Check Name field and update it, if appropriate
                editName = "id_form-"+str(rowNo-1)+"-name"
                if sel.is_element_present(editName)==False:
                    mclib.AppendErrorMessage(self,sel,"Edit field 'Name' not found")
                else:
                    if sourceNewname!="":
                        sel.type(editName,sourceNewname)
                # Check Feed URL field and update it, if appropriate
                editURL = "id_form-"+str(rowNo-1)+"-feed_url"
                if sel.is_element_present(editURL)==False:
                    mclib.AppendErrorMessage(self,sel,"Edit field 'Feed URL' not found")
                else:
                    if sourceURL!="":
                        sel.type(editURL,sourceURL)
                # Check Webpage field and update it, if appropriate
                editSite = "id_form-"+str(rowNo-1)+"-webpage"
                if sel.is_element_present(editSite)==False:
                    mclib.AppendErrorMessage(self,sel,"Edit field 'Webpage' not found")
                else:
                    if sourceSite!="":
                        sel.type(editSite,sourceSite)
                # Check list of Categories and update it, if appropriate
                listCategory = "//div[@id='labels']/form[2]/table/tbody/tr"+row+"/td[1]/div/div[2]/ul/li[5]/ul"
                if sel.is_element_present(listCategory)==False:
                    mclib.AppendErrorMessage(self,sel,"List of Categories not found")
                else:
                    if category!="":
                        no=1
                        catCaption = listCategory + "/li["+str(no)+"]/label/span"
                        catBox=""
                        while sel.is_element_present(catCaption)==True:
                            if sel.get_text(catCaption)==category:
                                catBox = "id_form-"+str(rowNo-1)+"-auto_categories_"+str(no-1)
                                sel.check(catBox)
                                break
                            no = no+1
                            catCaption = listCategory + "/li["+str(no)+"]/label/span"
                        if catBox=="":
                            mclib.AppendErrorMessage(self,sel,"Category not found: "+category)
                # Check list of Users and update it, if appropriate
                listUsers = "//div[@id='labels']/form[2]/table/tbody/tr"+row+"/td[1]/div/div[2]/ul/li[6]/ul"
                if sel.is_element_present(listUsers)==False:
                    mclib.AppendErrorMessage(self,sel,"List of Users not found")
                else:
                    if user!="":
                        no=1
                        userCaption = listUsers + "/li["+str(no)+"]/label/span"
                        userBox=""
                        while sel.is_element_present(userCaption)==True:
                            if sel.get_text(userCaption)==user:
                                userBox = "id_form-"+str(rowNo-1)+"-auto_authors_"+str(no-1)
                                sel.check(userBox)
                                break
                            no = no+1
                            userCaption = listUsers + "/li["+str(no)+"]/label/span"
                        if userBox=="":
                            mclib.AppendErrorMessage(self,sel,"User not found: "+user)
                updateButton = "//div[@id='labels']/form[2]/table/tbody/tr"+row+"/td[1]/div/button"
                if sel.is_element_present(updateButton)==False:
                    mclib.AppendErrorMessage(self,sel,"Update button not found")
                else:
                    sel.click(updateButton)
                    sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])
                # Checking results
                print "Checking that the source feed was updated properly..."
                if sourceNewname=="":
                    checkSource = SourceLocation(self,sel,sourceName)
                else:
                    checkSource = SourceLocation(self,sel,sourceNewname)
                if checkSource==[0,0]:
                    mclib.AppendErrorMessage(self,sel,"Source not found in the list of sources")
                else:
                    print "Source found"
                    page = checkSource[0]
                    rowNo = checkSource[1]
                    if rowNo == 0:
                        row = ""
                    else:
                        row = "["+str(rowNo)+"]"
                    sel.open(testvars.MCTestVariables["ManageSourcesPage"]+"/?page="+str(page))
                    sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])
                    # Check feed URL
                    feedLink="//div[@id='labels']/form[2]/table/tbody/tr"+row+"/td[2]/div/a[3]"
                    newfeedURL = sel.get_attribute(feedLink+"/@href")
                    print "Checking feed URL..."
                    if newfeedURL!=feedURL:
                        mclib.AppendErrorMessage(self,sel,"URLs of feed page before and after update do not match")
                        print "Initial URL: "+feedURL
                        print "=== New URL: "+newfeedURL
                    else:
                        print "OK"
                    categoryCell="//div[@id='labels']/form[2]/table/tbody/tr"+row+"/td[3]"
                    if category!="":
                        print "Checking the new value of Category parameter for the source..."
                        if sel.is_element_present(categoryCell)==True:
                            newCategory = sel.get_text(categoryCell)
                            if newCategory.find(category)==-1:
                                mclib.AppendErrorMessage(self,sel,"New category not displayed for the source")
                                print "Sought value: "+category
                                print "- Found only: "+newCategory
                            else:
                                print "OK"
                        else:
                            mclib.AppendErrorMessage(self,sel,"Value of category parameter for the source not found")
                    userCell="//div[@id='labels']/form[2]/table/tbody/tr"+row+"/td[4]/span"
                    if user!="":
                        print "Checking the value of new user parameter for the source..."
                        if sel.is_element_present(userCell)==True:
                            newUser = sel.get_text(userCell)
                            if newUser.find(user)==-1:
                                mclib.AppendErrorMessage(self,sel,"New username not displayed for the source")
                                print "Sought value: "+user
                                print "- Found only: "+newUser
                            else:
                                print "OK"
                        else:
                            mclib.AppendErrorMessage(self,sel,"Value of user parameter for the source not found")
                        


# =======================================
# =        MARK SELECTED SOURCES        =
# =======================================

# This subroutine marks all the sources listed in <sourcelist>
# for use with bulk operations
# These sources should be all on the same page

def MarkListedSources(self,sel,sourcelist):
    # Get location of each source in sourcelist
    sourceIndex = [[100,100]]
    for item in sourcelist:
        sourceLoc = SourceLocation(self,sel,item)
        sourceIndex.append(sourceLoc)
    sourceIndex.remove([100,100])
    # Mark each source in sourcelist
    for item in range(0,len(sourceIndex)):
        if sourceIndex[item]==[0,0]:
            mclib.AppendErrorMessage(self,sel,"Source not found: "+str(sourceIndex[item]))
        else:
            sourceLoc = sourceIndex[item]
            page = sourceLoc[0]
            rowNo = sourceLoc[1]
            if rowNo == 0:
                rowNo = 1
                row = ""
            else:
                row = "["+str(rowNo)+"]"
#            sel.open(testvars.MCTestVariables["ManageSourcesPage"]+"/?page="+str(page))
#            sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])
            checkboxSource = "id_form-"+str(rowNo-1)+"-BULK"
            if sel.is_element_present(checkboxSource)==True:
                sel.check(checkboxSource)
                print "Marked source: "+sourcelist[item]
            else:
                mclib.AppendErrorMessage(self,sel,"Checkbox not found for source: "+item)

                
        
# =======================================
# =          BULK EDIT SOURCES          =
# =======================================

# This subroutine updates the following parameters for a few sources
# listed in <sourcelist> at a time:
# autoApprove = 1 - On
#             = 0 - Off
# category - adds another associated category
# user - adds another associated user

def BulkEditSource(self,sel,sourcelist,autoApprove,category,user):
    NavigateToManageSources(self,sel)
    # Count the total number of sources to obtain the bulk edit controls
    sourceCount = len(GetSourceList(self,sel))
    if sourceCount>15: sourceCount = 15 # if the list of sources is longer than one page
    print sourceCount
    # Check the checkboxes opposite the sources to be edited
    NavigateToManageSources(self,sel)
    MarkListedSources(self,sel,sourcelist)
    # Apply edit to all the marked sources
    sel.select("bulk_action_selector", "label=Edit")
    sel.click("//button[@type='button']")
    time.sleep(10) #may be pretty slow
    if sel.is_element_present("massedit")==False:
        mclib.AppendErrorMessage(self,sel,"Bulk edit pop-up not found")
    else:
        # Set Approve On/Off
        if autoApprove==1:
            sel.click("id_form-"+str(sourceCount)+"-auto_approve_0")
        else:
            sel.click("id_form-"+str(sourceCount)+"-auto_approve_1")
        listCategory = "//div[@id='massedit']/div[2]/ul/li[2]"
        if sel.is_element_present(listCategory)==False:
            mclib.AppendErrorMessage(self,sel,"List of Categories not found")
        else:
            if category!="":
                no=1
                catCaption = listCategory + "/ul/li["+str(no)+"]/label/span"
                catBox=""
                while sel.is_element_present(catCaption)==True:
                    if sel.get_text(catCaption)==category:
                        catBox = "id_form-"+str(sourceCount)+"-auto_categories_"+str(no-1)
                        sel.check(catBox)
                        break
                    no = no+1
                    catCaption = listCategory + "/ul/li["+str(no)+"]/label/span"
                if catBox=="":
                    mclib.AppendErrorMessage(self,sel,"Category not found: "+category)
        # Check list of Users and update it, if appropriate
        listUsers = "//div[@id='massedit']/div[2]/ul/li[3]"
        if sel.is_element_present(listUsers)==False:
            mclib.AppendErrorMessage(self,sel,"List of Users not found")
        else:
            if user!="":
                no=1
                userCaption = listUsers + "/ul/li["+str(no)+"]/label/span"
                userBox=""
                while sel.is_element_present(userCaption)==True:
                    if sel.get_text(userCaption)==user:
                        userBox = "id_form-"+str(sourceCount)+"-auto_authors_"+str(no-1)
                        sel.check(userBox)
                        break
                    no = no+1
                    userCaption = listUsers + "/ul/li["+str(no)+"]/label/span"
                if userBox=="":
                    mclib.AppendErrorMessage(self,sel,"User not found: "+user)
        updateButton = "//div[@id='massedit']/button"
        if sel.is_element_present(updateButton)==False:
            mclib.AppendErrorMessage(self,sel,"Update button not found")
        else:
            sel.click(updateButton)
            sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])
        # Check the results
        for item in sourcelist:
            checkSource = SourceLocation(self,sel,item)
            if checkSource==[0,0]:
                mclib.AppendErrorMessage(self,sel,"Source not found: "+item)
            else:
                page = checkSource[0]
                rowNo = checkSource[1]
                if rowNo == 0:
                    row = ""
                else:
                    row = "["+str(rowNo)+"]"
                sel.open(testvars.MCTestVariables["ManageSourcesPage"]+"/?page="+str(page))
                sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])
                approveCell="//div[@id='labels']/form[2]/table/tbody/tr"+row+"/td[6]/a[1]"
                print "Checking the new value of Approve All / Review First parameter..."
                if sel.is_element_present(approveCell)==True:
                    approveValue = sel.get_text(approveCell)
                    if approveValue=="On" and autoApprove==1: print "OK"
                    elif approveValue=="Off" and autoApprove==0: print "OK"
                    else:
                        mclib.AppendErrorMessage(self,sel,"Wrong value of Approve All / Review First parameter displayed for source: "+item)
                        print "Expected value: "+str(autoApprove)+" (Legend: 1 - On, 0 - Off)"
                        print "- Actual value: "+approveValue
                else:
                    mclib.AppendErrorMessage(self,sel,"Value of Approve All / Review First parameter not found for source: "+item)
                categoryCell="//div[@id='labels']/form[2]/table/tbody/tr"+row+"/td[3]"
                if category!="":
                    print "Checking the new value of Category parameter for the source "+item+"..."
                    if sel.is_element_present(categoryCell)==True:
                        actualCategory = sel.get_text(categoryCell)
                        if actualCategory.find(category)==-1:
                            mclib.AppendErrorMessage(self,sel,"Wrong value of category displayed for the source: "+item)
                            print "Expected value: "+category
                            print "Actual value: "+actualCategory
                        else:
                            print "OK"
                    else:
                        mclib.AppendErrorMessage(self,sel,"Value of category parameter not found for the source: "+item)
                userCell="//div[@id='labels']/form[2]/table/tbody/tr"+row+"/td[4]/span"
                if user!="":
                    print "Checking the new value of user parameter for the source "+item+"..."
                    if sel.is_element_present(userCell)==True:
                        actualUser = sel.get_text(userCell)
                        if actualUser.find(user)==-1:
                            mclib.AppendErrorMessage(self,sel,"Wrong username displayed for the source: "+item)
                            print "Expected value: "+user
                            print "Actual value: "+actualUser
                        else:
                            print "OK"
                    else:
                        mclib.AppendErrorMessage(self,sel,"Value of user parameter not found for the source: "+item)
            
    
    

# =======================================
# =         BULK DELETE SOURCES         =
# =======================================

# This subroutine deletes the selected sources 

def BulkDeleteSource(self,sel,sourcelist):
    NavigateToManageSources(self,sel)
    # Check the checkboxes opposite the sources to be deleted
    MarkListedSources(self,sel,sourcelist)
    # Apply delete to all the marked sources
    print "Deleting the marked sources..."
    sel.select("bulk_action_selector", "label=Remove")
    sel.click("//button[@type='button']")
    time.sleep(10) #may be pretty slow
    sel.refresh()
    sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])
    # Now checking results
    for item in sourcelist:
        print "Checking source: "+item+"..."
        if SourceLocation(self,sel,item)!=[0,0]:
            mclib.AppendErrorMessage(self,sel,"Source not deleted: "+item)
        else:
            print "OK"



# =======================================
# =             SORT SOURCES            =
# =======================================

# This subroutine sorts the list of sources by parameter
# Parameter can take one of the following values: Name, Type, AutoApprove
# Order can be set to Asc (ascending) or Desc (descending)

def SortSources(self,sel,parameter,order):
    NavigateToManageSources(self,sel)
    baseHeader = "//div[@id='labels']/form[2]/table/thead/tr/"
    if parameter=="Name":
        print "Sorting the list of sources by NAME in order: "+order+"..."
        header = baseHeader+"th[2]/a"
#        list1 = GetSourceList(self,sel)
        if sel.is_element_present(header)==True:
            # By default, the list of sources is sorted alphabetically by name in ascending order
            # Click the header to reorder it in descending order
            link=sel.get_attribute(header+"@href")
#            print link
            expectedLink="?sort=-name__lower"
            if link.find(expectedLink)==-1:
                mclib.AppendErrorMessage(self,sel,"Expected link for sorting by NAME DESCENDING not found")
                print "Expected link: "+expectedLink
                print "- Actual link: "+link
            else:
                sel.click(header)
                sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])
                if order=="Asc":
                    link=sel.get_attribute(header+"@href")
#                    print link
#                    expectedLink="?sort=name__lower"
                    expectedLink=""
                    if link.find(expectedLink)==-1:
                        mclib.AppendErrorMessage(self,sel,"Expected link for sorting by NAME ASCENDING not found")
                        print "Expected link: "+expectedLink
                        print "- Actual link: "+link
                    else:
                        sel.click(header)
                        sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])
    elif parameter=="Type":
        print "Sorting the list of sources by TYPE in order: "+order+"..."
        header = baseHeader+"th[5]/a"
        if sel.is_element_present(header)==True:
            link=sel.get_attribute(header+"@href")
 #           print link
            expectedLink="?sort=type"
            if link.find(expectedLink)==-1:
                mclib.AppendErrorMessage(self,sel,"Expected link for sorting by TYPE ASCENDING not found")
            else:
                sel.click(header)
                sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])
                link=sel.get_attribute(header+"@href")
#                print link
                expectedLink="?sort=-type"
                if link.find(expectedLink)==-1:
                    mclib.AppendErrorMessage(self,sel,"Expected link for sorting by TYPE DESCENDING not found")
                else:
                    if order=="Desc":
                        sel.click(header)
                        sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])
                    else: pass
    elif parameter=="AutoApprove":
        print "Sorting the list of sources by AUTOAPPROVE in order: "+order+"..."
        header = baseHeader+"th[6]/a"
        if sel.is_element_present(header)==True:
            link=sel.get_attribute(header+"@href")
#            print link
            expectedLink="?sort=auto_approve"
            if link.find(expectedLink)==-1:
                mclib.AppendErrorMessage(self,sel,"Expected link for sorting by AUTO APPROVE ASCENDING not found")
            else:
                sel.click(header)
                sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])
                link=sel.get_attribute(header+"@href")
#                print link
                expectedLink="?sort=-auto_approve"
                if link.find(expectedLink)==-1:
                    mclib.AppendErrorMessage(self,sel,"Expected link for sorting by AUTO APPROVE DESCENDING not found")
                else:
                    if order=="Desc":
                        sel.click(header)
                        sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])
                    else: pass
    else:
        mclib.AppendErrorMessage(self,sel,"Wrong value of sort parameter supplied")



# =======================================
# =          SEARCH IN SOURCES          =
# =======================================

# This subroutine searches for sources in the list of sources by <query>,
# <category>, and/or <author>

def SearchInSources(self,sel,category,author,query):
    NavigateToManageSources(self,sel)
    # Specify category, if appropriate
    if category!="":
        if sel.is_element_present("category")==False:
            mclib.AppendErrorMessage(self,sel,"Category filter drop-down list not found")
        else:
            print "Selecting category: "+category+"..."
            sel.select("category",category)
    # Specify author, if appropriate
    if author!="":
        if sel.is_element_present("author")==False:
            mclib.AppendErrorMessage(self,sel,"Author filter drop-down list not found")
        else:
            print "Selecting author: "+author+"..."
            sel.select("author",author)
    # Type search query, if appropriate
    if query!="":
        if sel.is_element_present("q")==False:
            mclib.AppendErrorMessage(self,sel,"Input field for the search query not found")
        else:
            print "Typing query: "+query+"..."
            sel.type("q",query)
    # Click Search button
    if sel.is_element_present("//div[@id='labels']/form[1]/button")==False:
        mclib.AppendErrorMessage(self,sel,"Search button not found")
    else:
        print "Searching..."
        sel.click("//div[@id='labels']/form[1]/button")
        sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])
        print "Done"
    # Now check search results
    print "Checking search results..."
    baseURL = sel.get_location()
#    print "- Actual URL: "+baseURL
    page = 1 # page number
    try:
        sel.open(baseURL+"&page="+str(page))
        sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])
    except:    pass
    while sel.is_text_present("Page not found")==False:
        row = 0   # row number
        # Only one source on the page? If not, go ahead
        if sel.is_element_present("//div[@id='labels']/form[2]/table/tbody/tr/td[2]/span"): # no row number in the link
            if category!="":
                tempCat=sel.get_text("//div[@id='labels']/form[2]/table/tbody/tr/td[3]")
                if tempCat.find(category)==-1:
                    mclib.AppendErrorMessage(self,sel,"Result set does not meet category criteria")
            if author!="":
                tempAuthor=sel.get_text("//div[@id='labels']/form[2]/table/tbody/tr/td[4]")
                if tempAuthor.find(author)==-1:
                    mclib.AppendErrorMessage(self,sel,"Result set does not meet author criteria")
            if query!="":
                tempName=sel.get_text("//div[@id='labels']/form[2]/table/tbody/tr/td[2]/span")
                if tempName.find(query)==-1:
                    mclib.AppendErrorMessage(self,sel,"Result set does not meet the search query")
        # Name of the first source in the list - for multiple rows on the page
        row = 2
        sourceTableCell="//div[@id='labels']/form[2]/table/tbody/tr["+str(row)+"]/td[2]/span"
        while sel.is_element_present(sourceTableCell):
            if category!="":
                tempCat=sel.get_text("//div[@id='labels']/form[2]/table/tbody/tr["+str(row)+"]/td[3]")
                if tempCat.find(category)==-1:
                    mclib.AppendErrorMessage(self,sel,"Result set does not meet category criteria")
            if author!="":
                tempAuthor=sel.get_text("//div[@id='labels']/form[2]/table/tbody/tr["+str(row)+"]/td[4]")
                if tempAuthor.find(author)==-1:
                    mclib.AppendErrorMessage(self,sel,"Result set does not meet author criteria")
            if query!="":
                tempName=sel.get_text("//div[@id='labels']/form[2]/table/tbody/tr["+str(row)+"]/td[2]/span")
                if tempName.find(query)==-1:
                    mclib.AppendErrorMessage(self,sel,"Result set does not meet the search query")
            row=row+1
            sourceTableCell="//div[@id='labels']/form[2]/table/tbody/tr["+str(row)+"]/td[2]/span"
        # End of page reached?
        page = page+1
        try:
            sel.open(baseURL+"&page="+str(page))
            sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])
        except: pass
    print "OK"             


# =======================================
# =            FILTER SOURCES           =
# =======================================

# This subroutine filters sources by type (<filter>), which
# can take values "All", "Users", "Searches", or "Feeds"

def FilterSources(self,sel,filter):
    NavigateToManageSources(self,sel)
    if filter=="All":
        if sel.is_element_present("link=All")==False:
            mclib.AppendErrorMessage("Link 'All' not found")
        else:
            sel.click("link=All")
            sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])
            actualURL = sel.get_location()
            expectedURL = testvars.MCTestVariables["TestSite"]+testvars.MCTestVariables["ManageSourcesPage"]+"/"
            print "Checking the URL of the result page..."
            if actualURL!=expectedURL:
                mclib.AppendErrorMessage(self,sel,"The URL of the result page is different from expected URL")
                print "Expected URL: "+expectedURL
                print "- Actual URL: "+actualURL
            else:
                print "OK"
    elif filter=="Users":
        if sel.is_element_present("link=Video Site Users")==False:
            mclib.AppendErrorMessage("Link 'Video Site Users' not found")
        else:
            sel.click("link=Video Site Users")
            sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])
            actualURL = sel.get_location()
            expectedURL = testvars.MCTestVariables["TestSite"]+testvars.MCTestVariables["ManageSourcesPage"]+"/?filter=user"
            print "Checking the URL of the result page..."
            if actualURL!=expectedURL:
                mclib.AppendErrorMessage(self,sel,"The URL of the result page is different from expected URL")
                print "Expected URL: "+expectedURL
                print "- Actual URL: "+actualURL
            else:
                print "OK"
                print "Checking that all videos on the page meet the filter criterion..."
                row=1
                err=0
                typeTableCell="//div[@id='labels']/form[2]/table/tbody/tr["+str(row)+"]/td[5]"
                while sel.is_element_present(typeTableCell):
                    type = sel.get_text(typeTableCell)
                    if type.find("User: ")==-1:
                        mclib.AppendErrorMessage(self,sel,"Non-user source found in the list filtered by user sources")
                        err=1
                        break
                    row=row+1
                    typeTableCell="//div[@id='labels']/form[2]/table/tbody/tr["+str(row)+"]/td[5]"
                if err==0:
                    print "OK"
    elif filter=="Searches":
        if sel.is_element_present("link=Video Site Searches")==False:
            mclib.AppendErrorMessage("Link 'Video Site Searches' not found")
        else:
            sel.click("link=Video Site Searches")
            sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])
            actualURL = sel.get_location()
            expectedURL = testvars.MCTestVariables["TestSite"]+testvars.MCTestVariables["ManageSourcesPage"]+"/?filter=search"
            print "Checking the URL of the result page..."
            if actualURL!=expectedURL:
                mclib.AppendErrorMessage(self,sel,"The URL of the result page is different from expected URL")
                print "Expected URL: "+expectedURL
                print "- Actual URL: "+actualURL
            else:
                print "OK"
                print "Checking that all videos on the page meet the filter criterion..."
                row=1
                err=0
                typeTableCell="//div[@id='labels']/form[2]/table/tbody/tr["+str(row)+"]/td[5]"
                while sel.is_element_present(typeTableCell):
                    type = sel.get_text(typeTableCell)
                    if type!="Search":
                        mclib.AppendErrorMessage(self,sel,"Non-search source found in the list filtered by search sources")
                        err=1
                        break
                    row=row+1
                    typeTableCell="//div[@id='labels']/form[2]/table/tbody/tr["+str(row)+"]/td[5]"
                if err==0:
                    print "OK"
    elif filter=="Feeds":
        if sel.is_element_present("link=RSS Feeds")==False:
            mclib.AppendErrorMessage("Link 'RSS Feeds' not found")
        else:
            sel.click("link=RSS Feeds")
            sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])
            actualURL = sel.get_location()
            expectedURL = testvars.MCTestVariables["TestSite"]+testvars.MCTestVariables["ManageSourcesPage"]+"/?filter=feed"
            print "Checking the URL of the result page..."
            if actualURL!=expectedURL:
                mclib.AppendErrorMessage(self,sel,"The URL of the result page is different from expected URL")
                print "Expected URL: "+expectedURL
                print "- Actual URL: "+actualURL
            else:
                print "OK"
                print "Checking that all videos on the page meet the filter criterion..."
                row=1
                err=0
                typeTableCell="//div[@id='labels']/form[2]/table/tbody/tr["+str(row)+"]/td[5]"
                while sel.is_element_present(typeTableCell):
                    type = sel.get_text(typeTableCell)
                    if type!="Feed":
                        mclib.AppendErrorMessage(self,sel,"Non-search source found in the list filtered by search sources")
                        err=1
                        break
                    row=row+1
                    typeTableCell="//div[@id='labels']/form[2]/table/tbody/tr["+str(row)+"]/td[5]"
                if err==0:
                    print "OK"
    else:
        mclib.AppendErrorMessage(self,sel,"Wrong parameter passed to FilterSources subroutine")