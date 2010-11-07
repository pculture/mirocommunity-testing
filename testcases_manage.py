#=======================================================================
#
#                       MANAGE SOURCES TESTS
#
#=======================================================================
#
# Includes the following test cases:
#     1. TestCase_AddSourceFeed_257
#     2. TestCase_AddDuplicateFeed_258
#     3. TestCase_AddSourceWithDuplicateVideos_259
#     4. TestCase_EditSource_479
#     5. TestCase_BulkEditSources_264
#     6. TestCase_BulkDeleteSources_265
#     7. TestCase_SearchForVideos_260
#     8. TestCase_SearchVideoByNonASCIITerm_261
#     9. TestCase_AddSearchFeed_262
#     10. TestCase_SortSources_266
#     11. TestCase_SearchInSources_267
#     12. TestCase_FilterSources_268


from selenium import selenium
import unittest, time, re, sys
import mclib, loginlogout, categories, sources, queue, testvars

# ----------------------------------------------------------------------


class TestCase_AddSourceFeed_257(unittest.TestCase):
    
# Open the desired browser and set up the test
    def setUp(self):
        self.verificationErrors = []
        self.selenium = selenium("localhost", testvars.MCTestVariables["Port"], testvars.MCTestVariables["Browser"], testvars.MCTestVariables["TestSite"])
        self.selenium.start()

# The user actions executed in the test scenario
    def test_AddSourceFeed_257(self):
        sel = self.selenium
        loginlogout.LogInAsAdmin(self,sel)
        # Check if the source exists. If yes, delete it
        # source = "Al Jazeera Arts World - Video"
        # sourceURL = "http://feeds2.feedburner.com/video/artsworld"
        source = "Alaska HDTV | Discover the Great Land"
        sourceURL = "http://feeds.feedburner.com/alaskapodshow"
        if sources.SourceLocation(self,sel,source)!=[0,0]:
            sources.DeleteSource(self,sel,source)
        # Add the source with the specified URL and Approve All parameter set to true
        # Associate it with a category and "Selene Test-Admin" user
        sources.AddSource(self,sel,sourceURL,0,testvars.newCategories[3],"Selene Test-Admin")

# Close the browser, log errors, perform cleanup    
    def tearDown(self):
        self.selenium.stop()
# the command on the previous line should close the browser
        self.assertEqual([], self.verificationErrors)


class TestCase_AddDuplicateFeed_258(unittest.TestCase):
    
# Open the desired browser and set up the test
    def setUp(self):
        self.verificationErrors = []
        self.selenium = selenium("localhost", testvars.MCTestVariables["Port"], testvars.MCTestVariables["Browser"], testvars.MCTestVariables["TestSite"])
        self.selenium.start()

# The user actions executed in the test scenario
    def test_AddDuplicateFeed_258(self):
        sel = self.selenium
        loginlogout.LogInAsAdmin(self,sel)
        #sourceURL = "http://feeds2.feedburner.com/video/artsworld"
        sourceURL = "http://feeds.feedburner.com/alaskapodshow"
        sources.AddDuplicateSource(self,sel,sourceURL)

# Close the browser, log errors, perform cleanup    
    def tearDown(self):
        self.selenium.stop()
# the command on the previous line should close the browser
        self.assertEqual([], self.verificationErrors)


class TestCase_AddSourceWithDuplicateVideos_259(unittest.TestCase):
    
# Open the desired browser and set up the test
    def setUp(self):
        self.verificationErrors = []
        self.selenium = selenium("localhost", testvars.MCTestVariables["Port"], testvars.MCTestVariables["Browser"], testvars.MCTestVariables["TestSite"])
        self.selenium.start()

# The user actions executed in the test scenario
    def test_AddSourceWithDuplicateVideos_259(self):
        sel = self.selenium
        loginlogout.LogInAsAdmin(self,sel)
        # Delete existing source, if appropriate
        source = "Yahoo Media TEST"
        if sources.SourceLocation(self,sel,source)!=[0,0]:
            sources.DeleteSource(self,sel,source)
        # Add new source
        sources.AddSource(self,sel,"http://participatoryculture.org/feeds_test/feed1.rss",1,"","")
        # Now check the videos imported
        sel.open(testvars.MCTestVariables["ManageSourcesPage"])
        sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])
        sourceLoc = sources.SourceLocation(self,sel,source)
        page = sourceLoc[0]
        rowNo = sourceLoc[1]
        if rowNo == 0:
            row = ""
        else:
            row = "["+str(rowNo)+"]"
        print "Viewing source "+source+"..."
        sel.open(testvars.MCTestVariables["ManageSourcesPage"]+"/?page="+str(page))
        sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])
        viewLink="//div[@id='labels']/form[2]/table/tbody/tr"+str(row)+"/td[2]/div/a[3]"
        if sel.is_element_present(viewLink)==True:
            sel.click(viewLink)
            sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])
            print "Counting imported videos..."
            cnt = sel.get_xpath_count("//a[@class='thumbnail']") 
            print str(cnt)+" videos found"
        else:
            mclib.AppendErrorMessage(self,sel,"Could not find View link for source: "+source)

# Close the browser, log errors, perform cleanup    
    def tearDown(self):
        self.selenium.stop()
# the command on the previous line should close the browser
        self.assertEqual([], self.verificationErrors)



class TestCase_EditSource_479(unittest.TestCase):
    
# Open the desired browser and set up the test
    def setUp(self):
        self.verificationErrors = []
        self.selenium = selenium("localhost", testvars.MCTestVariables["Port"], testvars.MCTestVariables["Browser"], testvars.MCTestVariables["TestSite"])
        self.selenium.start()

# The user actions executed in the test scenario

    def test_EditSource_479(self):
        sel = self.selenium
        loginlogout.LogInAsAdmin(self,sel)
        #oldSourceName = "Al Jazeera Arts World - Video"
        oldSourceName = "Alaska HDTV | Discover the Great Land"
        oldSourceURL = "http://feeds.feedburner.com/alaskapodshow"
        # Does source to be edited exist? If not, add it
        if sources.SourceLocation(self,sel,oldSourceName)==[0,0]:
            print oldSourceName+" feed not found - adding it..."
            sources.AddSource(self,sel,oldSourceURL,0,"","")
        newSourceName = "Best of Attenborough"
        # Does the target source exist? If yes, delete it
        if sources.SourceLocation(self,sel,newSourceName)!=[0,0]:
            print "Target feed "+newSourceName+" already exists - deleting it..."
            sources.DeleteSource(self,sel,newSourceName)
        # If the pre-defined category is missing in the system,
        # pick the first category from the list of existing categories
        newcat = testvars.newCategories[6]
        if categories.CategoryRow(self,sel,newcat)==0:
            newcat = categories.GetCategoryList(self,sel)[0]
        print "New category: "+newcat
        sources.EditSource(self,sel,oldSourceName,newSourceName,"http://www.youtube.com/user/BestofAttenborough","http://delicious.com/BestofAttenborough",newcat,"selene test-user")

# Close the browser, log errors, perform cleanup    
    def tearDown(self):
        self.selenium.stop()
# the command on the previous line should close the browser
        self.assertEqual([], self.verificationErrors)


class TestCase_BulkEditSources_264(unittest.TestCase):
    
# Open the desired browser and set up the test
    def setUp(self):
        self.verificationErrors = []
        self.selenium = selenium("localhost", testvars.MCTestVariables["Port"], testvars.MCTestVariables["Browser"], testvars.MCTestVariables["TestSite"])
        self.selenium.start()

# The user actions executed in the test scenario
    def test_BulkEditSources_264(self):
        sel = self.selenium
        loginlogout.LogInAsAdmin(self,sel)
        # List all the available sources
        sourcelist = sources.GetSourceList(self,sel)
        print sourcelist
        # Pick two sources
        editList = sourcelist[8:10]
        print editList
        # If the pre-defined category is missing in the system, pick the last
        # category from the list of existing categories
        newcat = "family"
        if categories.CategoryRow(self,sel,newcat)==0:
            categoryList = categories.GetCategoryList(self,sel)
            q= len(categoryList)
            newcat = categoryList[q-1]
        print "New category: "+newcat
        # Bulk edit the selected sources
        sources.BulkEditSource(self,sel,editList,1,newcat,"selene test-user")

# Close the browser, log errors, perform cleanup    
    def tearDown(self):
        self.selenium.stop()
# the command on the previous line should close the browser
        self.assertEqual([], self.verificationErrors)


class TestCase_BulkDeleteSources_265(unittest.TestCase):
    
# Open the desired browser and set up the test
    def setUp(self):
        self.verificationErrors = []
        self.selenium = selenium("localhost", testvars.MCTestVariables["Port"], testvars.MCTestVariables["Browser"], testvars.MCTestVariables["TestSite"])
        self.selenium.start()

# The user actions executed in the test scenario
    def test_BulkDeleteSources_265(self):
        sel = self.selenium
        loginlogout.LogInAsAdmin(self,sel)
        sourcelist = sources.GetSourceList(self,sel)
        print "Full list of available sources:"
        print sourcelist
        deleteList = sourcelist[4:6]
        print "The following sources will be deleted:"
        print deleteList
        sources.BulkDeleteSource(self,sel,deleteList)

# Close the browser, log errors, perform cleanup    
    def tearDown(self):
        self.selenium.stop()
# the command on the previous line should close the browser
        self.assertEqual([], self.verificationErrors)



class TestCase_SearchForVideos_260(unittest.TestCase):
    
# Open the desired browser and set up the test
    def setUp(self):
        self.verificationErrors = []
        self.selenium = selenium("localhost", testvars.MCTestVariables["Port"], testvars.MCTestVariables["Browser"], testvars.MCTestVariables["TestSite"])
        self.selenium.start()

# The user actions executed in the test scenario
    def test_SearchForVideos_260(self):
        sel = self.selenium
        loginlogout.LogInAsAdmin(self,sel)
        
        searchterm = "tango"
        sortby = 0 # Latest
        if sources.SearchForVideos(self,sel,searchterm,sortby)==0:
            print "0 videos found - cannot approve, feature or add to queue items"
        else:
            # Approve video No.1
            video1title = sel.get_text("//div[@id='admin_videolisting_row']/div[1]/div[1]/h3/a")
            print "Approving video \""+video1title+"\"..."
            approveLink = "//div[@id='admin_videolisting_row']/div[1]/div[2]/a[2]/span"
            if sel.is_element_present(approveLink)==True:
                sel.click(approveLink)
                time.sleep(8)
                print "OK"
            else:
                mclib.AppendErrorMessage(self,sel,"Approve link not found for the video")
            # Feature video No.2 (as video 1 disappears from the list, )
            video2title = sel.get_text("//div[@id='admin_videolisting_row']/div[1]/div[1]/h3/a")
            print "Featuring video \""+video2title+"\"..."
            featureLink = "//div[@id='admin_videolisting_row']/div[1]/div[2]/a[1]/span"
            if sel.is_element_present(featureLink)==True:
                sel.click(featureLink)
                time.sleep(8)
                print "OK"
            else:
                mclib.AppendErrorMessage(self,sel,"Feature link not found for the video")
            # Add to Queue video No.3
            video3title = sel.get_text("//div[@id='admin_videolisting_row']/div[1]/div[1]/h3/a")
            print "Adding video \""+video3title+"\" to the queue..."
            queueLink = "//div[@id='admin_videolisting_row']/div[1]/div[2]/a[3]/span"
            if sel.is_element_present(queueLink)==True:
                sel.click(queueLink)
                time.sleep(5)
                #sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])
                print "OK"
            else:
                mclib.AppendErrorMessage(self,sel,"Add to Queue link not found for the video")

            #Checking the new videos in the lists
            #Searching for the approved video
            queue.CheckVideoStatus(self,sel,video1title,"Approved")
            
            # Navigate to Manage Sources page to prevent freezing if the script
            sel.click(testvars.MCUI["AdminManageSources"])
            sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])

            print " "
            #Searching for the featured video
            queue.CheckVideoStatus(self,sel,video2title,"Featured")

            print " "
            print "Searching for the video in the queue..."
            # Looking for the last page in the queue
            try:
                sel.open(testvars.MCTestVariables["ReviewQueuePage"]+"/?page=1000000")
                sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])
            except: pass
            if sel.is_element_present("//a[contains(text(),video3title)]")==True:
                print "Found video \""+video3title+"\" in the queue on the last page - OK"
            else:
                mclib.AppendErrorMessage(self,sel,"Could not find video "+video3title+" on the last page of the queue")
                
# Close the browser, log errors, perform cleanup    
    def tearDown(self):
        self.selenium.stop()
# the command on the previous line should close the browser
        self.assertEqual([], self.verificationErrors)


class TestCase_SearchVideoByNonASCIITerm_261(unittest.TestCase):
    
# Open the desired browser and set up the test
    def setUp(self):
        self.verificationErrors = []
        self.selenium = selenium("localhost", testvars.MCTestVariables["Port"], testvars.MCTestVariables["Browser"], testvars.MCTestVariables["TestSite"])
        self.selenium.start()

# The user actions executed in the test scenario
    def test_SearchVideoByNonASCIITerm_261(self):
        sel = self.selenium
        loginlogout.LogInAsAdmin(self,sel)
        searchterm = u"\u0442\u0443\u0440\u0438\u0437\u043C"  #'tourism' in Cyrillic alphabet
#        searchterm = u"\u0414\u0443\u0431\u0440\u043E\u0432\u043D\u0438\u043A"  #'Dubrovnik' in Cyrillic alphabet
        sortby = 1 # sort by Relevance
        if sources.SearchForVideos(self,sel,searchterm,sortby)==0:
            print "0 videos found - cannot approve, feature or add to queue items"
        else:
            # Approve video No.1
            video1title = sel.get_text("//div[@id='admin_videolisting_row']/div[1]/div[1]/h3/a")
            print "Approving video \""+video1title+"\"..."
            approveLink = "//div[@id='admin_videolisting_row']/div[1]/div[2]/a[2]/span"
            if sel.is_element_present(approveLink)==True:
                sel.click(approveLink)
                time.sleep(10)
                print "OK"
            else:
                mclib.AppendErrorMessage(self,sel,"Approve link not found for the video")
            # Feature video No.2 (as video 1 disappears from the list, )
            video2title = sel.get_text("//div[@id='admin_videolisting_row']/div[1]/div[1]/h3/a")
            print "Featuring video \""+video2title+"\"..."
            featureLink = "//div[@id='admin_videolisting_row']/div[1]/div[2]/a[1]/span"
            if sel.is_element_present(featureLink)==True:
                sel.click(featureLink)
                time.sleep(5)
                #sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])
                print "OK"
            else:
                mclib.AppendErrorMessage(self,sel,"Feature link not found for the video")
            # Add to Queue video No.3
            video3title = sel.get_text("//div[@id='admin_videolisting_row']/div[1]/div[1]/h3/a")
            print "Adding video \""+video3title+"\" to the queue..."
            queueLink = "//div[@id='admin_videolisting_row']/div[1]/div[2]/a[3]/span"
            if sel.is_element_present(queueLink)==True:
                sel.click(queueLink)
                time.sleep(5)
                print "OK"
            else:
                mclib.AppendErrorMessage(self,sel,"Add to Queue link not found for the video")

            #Checking the new videos in the lists
            #Searching for the approved video
            queue.CheckVideoStatus(self,sel,video1title,"Approved")
            
            # Navigate to Manage Sources page to prevent freezing if the script
            sel.click(testvars.MCUI["AdminManageSources"])
            sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])

            print " "
            #Searching for the featured video
            queue.CheckVideoStatus(self,sel,video2title,"Featured")

            print ""
            print "Searching for the video in the queue..."
            # Looking for the last page in the queue
            try:
                sel.open(testvars.MCTestVariables["ReviewQueuePage"]+"/?page=1000000")
                sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])
            except: pass
            if sel.is_element_present("//a[contains(text(),video3title)]")==True:
                print "Found video \""+video3title+"\" in the queue on the last page - OK"
            else:
                mclib.AppendErrorMessage(self,sel,"Could not find video "+video3title+" on the last page of the queue")
                
# Close the browser, log errors, perform cleanup    
    def tearDown(self):
        self.selenium.stop()
# the command on the previous line should close the browser
        self.assertEqual([], self.verificationErrors)


class TestCase_AddSearchFeed_262(unittest.TestCase):
    
# Open the desired browser and set up the test
    def setUp(self):
        self.verificationErrors = []
        self.selenium = selenium("localhost", testvars.MCTestVariables["Port"], testvars.MCTestVariables["Browser"], testvars.MCTestVariables["TestSite"])
        self.selenium.start()

# The user actions executed in the test scenario
    def test_AddSearchFeed_262(self):
        sel = self.selenium
        loginlogout.LogInAsAdmin(self,sel)
        # Add search feed with sorting by date
        searchterm = "Croatia"
        if sources.SourceLocation(self,sel,searchterm)!=[0,0]:
            sources.DeleteSource(self,sel,searchterm)
        sources.AddSearchFeed(self,sel,searchterm,0)
        # Add search feed with sorting by relevance
        searchterm = "Dalmatian resorts"
        if sources.SourceLocation(self,sel,searchterm)!=[0,0]:
            sources.DeleteSource(self,sel,searchterm)
        sources.AddSearchFeed(self,sel,searchterm,1)

# Close the browser, log errors, perform cleanup    
    def tearDown(self):
        self.selenium.stop()
# the command on the previous line should close the browser
        self.assertEqual([], self.verificationErrors)



class TestCase_SortSources_266(unittest.TestCase):
    
# Open the desired browser and set up the test
    def setUp(self):
        self.verificationErrors = []
        self.selenium = selenium("localhost", testvars.MCTestVariables["Port"], testvars.MCTestVariables["Browser"], testvars.MCTestVariables["TestSite"])
        self.selenium.start()

# Auxiliary subroutine which retrieves the list of values for the selected parameter
# for the purpose of verifying the sorting
    def GetSourceParameterList(self,sel,parameter):
        if parameter=="Name":    col="2]/span"
        elif parameter=="Type":    col="5]"
        elif parameter=="AutoApprove":    col="6]"
        else:
            print "Wrong value of list parameter passed to function"
            return ['-1']
        page = 1 # page number
        sourceList=['']
        no = 1
        baseURL = sel.get_location()
#        print baseURL
        while sel.is_text_present("Page not found")==False:
            row = 0   # row number
            tempSource=""
            # Only one source on the page? If not, go ahead
            sourceTableCell="//div[@id='labels']/form[2]/table/tbody/tr/td["+col  # no row number in the link
            if sel.is_element_present(sourceTableCell):
                if parameter=="Name" or parameter=="Type":
                    tempSource = sel.get_text(sourceTableCell)
                else:
                    if sel.is_visible(sourceTableCell+"/a[1]")==True:    tempSource = "On"
                    elif sel.is_visible(sourceTableCell+"/a[2]")==True:    tempSource = "Off"
                    else:    tempSource = ""
                sourceList.append(tempSource)
                no = no + 1
            # Name of the first source in the list - for multiple rows on the page
            row = 2
            sourceTableCell="//div[@id='labels']/form[2]/table/tbody/tr["+str(row)+"]/td["+col
            while sel.is_element_present(sourceTableCell):
                if parameter=="Name" or parameter=="Type":
                    tempSource = sel.get_text(sourceTableCell)
                else:
                    if sel.is_visible(sourceTableCell+"/a[1]")==True:    tempSource = "On"
                    elif sel.is_visible(sourceTableCell+"/a[2]")==True:    tempSource = "Off"
                    else:    tempSource = ""
                row=row+1
                sourceList.append(tempSource)
                no = no + 1
                sourceTableCell="//div[@id='labels']/form[2]/table/tbody/tr["+str(row)+"]/td["+col
            # End of page reached?
            page = page+1
            try:
                sel.open(baseURL+"&page="+str(page))
                sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])
            except: pass
        # If list not empty, remove the blank item
        if no>1:
            sourceList.remove("")
        return sourceList


# The user actions executed in the test scenario
    def test_SortSources_266(self):
        sel = self.selenium
        loginlogout.LogInAsAdmin(self,sel)

        print ""
        sources.SortSources(self,sel,"Name","Asc")
        resultList = TestCase_SortSources_266.GetSourceParameterList(self,sel,"Name")
        print resultList
        sortedList = sorted(resultList,key=unicode.lower)
        if resultList==sortedList:
            print "Sorting checked - CORRECT"
        else:
            mclib.AppendErrorMessage(self,sel,"Sorting by NAME ASCENDING was incorrect")

        print ""
        sources.SortSources(self,sel,"Name","Desc")
        resultList = TestCase_SortSources_266.GetSourceParameterList(self,sel,"Name")
        print resultList
        sortedList = sorted(resultList,key=unicode.lower,reverse=True)
        if resultList==sortedList:
            print "Sorting checked - CORRECT"
        else:
            mclib.AppendErrorMessage(self,sel,"Sorting by NAME DESCENDING was incorrect")
            
        print ""
        sources.SortSources(self,sel,"Type","Asc")
        resultList = TestCase_SortSources_266.GetSourceParameterList(self,sel,"Type")
        print resultList
        sortedList = sorted(resultList,key=unicode.lower)
        if resultList==sortedList:
            print "Sorting checked - CORRECT"
        else:
            mclib.AppendErrorMessage(self,sel,"Sorting by TYPE ASCENDING was incorrect")
        
        print ""
        sources.SortSources(self,sel,"Type","Desc")
        resultList = TestCase_SortSources_266.GetSourceParameterList(self,sel,"Type")
        print resultList
        sortedList = sorted(resultList,key=unicode.lower,reverse=True)
        if resultList==sortedList:
            print "Sorting checked - CORRECT"
        else:
            mclib.AppendErrorMessage(self,sel,"Sorting by TYPE DESCENDING was incorrect")

        print ""
        sources.SortSources(self,sel,"AutoApprove","Asc")
        resultList = TestCase_SortSources_266.GetSourceParameterList(self,sel,"AutoApprove")
        print resultList
        sortedList = sorted(resultList,key=str.lower)
        if resultList==sortedList:
            print "Sorting checked - CORRECT"
        else:
            mclib.AppendErrorMessage(self,sel,"Sorting by AUTOAPPROVE ASCENDING was incorrect")
        
        print ""
        sources.SortSources(self,sel,"AutoApprove","Desc")
        resultList = TestCase_SortSources_266.GetSourceParameterList(self,sel,"AutoApprove")
        print resultList
        sortedList = sorted(resultList,key=str.lower,reverse=True)
        if resultList==sortedList:
            print "Sorting checked - CORRECT"
        else:
            mclib.AppendErrorMessage(self,sel,"Sorting by AUTOAPPROVE DESCENDING was incorrect")

# Close the browser, log errors, perform cleanup    
    def tearDown(self):
        self.selenium.stop()
# the command on the previous line should close the browser
        self.assertEqual([], self.verificationErrors)


class TestCase_SearchInSources_267(unittest.TestCase):
    
# Open the desired browser and set up the test
    def setUp(self):
        self.verificationErrors = []
        self.selenium = selenium("localhost", testvars.MCTestVariables["Port"], testvars.MCTestVariables["Browser"], testvars.MCTestVariables["TestSite"])
        self.selenium.start()


# The user actions executed in the test scenario
    def test_SearchInSources_267(self):
        sel = self.selenium
        loginlogout.LogInAsAdmin(self,sel)
        # Search by query in particular user and category
        print "Search 1"
        sources.SearchInSources(self,sel,"art","Selene Test-Admin","Attenborough")
        print ""
        # Search in all feeds by query
        print "Search 2"
        sources.SearchInSources(self,sel,"","","Yahoo")
        print ""
        # Search in feeds by category
        print "Search 3"
        sources.SearchInSources(self,sel,"film","","")
        print ""
        # Search in feeds by user
        print "Search 4"
        sources.SearchInSources(self,sel,"","selene test-user","")


# Close the browser, log errors, perform cleanup    
    def tearDown(self):
        self.selenium.stop()
# the command on the previous line should close the browser
        self.assertEqual([], self.verificationErrors)



class TestCase_FilterSources_268(unittest.TestCase):
    
# Open the desired browser and set up the test
    def setUp(self):
        self.verificationErrors = []
        self.selenium = selenium("localhost", testvars.MCTestVariables["Port"], testvars.MCTestVariables["Browser"], testvars.MCTestVariables["TestSite"])
        self.selenium.start()

# The user actions executed in the test scenario
    def test_FilterSources_268(self):
        sel = self.selenium
        loginlogout.LogInAsAdmin(self,sel)
        print "Show All sources"
        sources.FilterSources(self,sel,"All")
        print ""
        print "Show Video Site Users only"
        sources.FilterSources(self,sel,"Users")
        print ""
        print "Show Video Site Searches only"
        sources.FilterSources(self,sel,"Searches")
        print ""
        print "Show RSS Feeds only"
        sources.FilterSources(self,sel,"Feeds")

# Close the browser, log errors, perform cleanup    
    def tearDown(self):
        self.selenium.stop()
# the command on the previous line should close the browser
        self.assertEqual([], self.verificationErrors)
