#=======================================================================
#
#                       REVIEW QUEUE TESTS
#
#=======================================================================
#
# Includes the following test cases:
#     1. TestCase_ApproveVideo
#     2. TestCase_FeatureVideo
#     3. TestCase_RejectVideo
#     4. TestCase_ApprovePage
#     5. TestCase_RejectPage
#     6. TestCase_ClearQueue
#     7. TestCase_EditVideoInQueue
#     8. TestCase_RSSVideosAwaitingModeration


from selenium import selenium
import unittest, time, re, sys
import mclib, loginlogout, queue, testvars

# ----------------------------------------------------------------------


class TestCase_ApproveVideo(unittest.TestCase):
    
# Open the desired browser and set up the test
    def setUp(self):
        self.verificationErrors = []
        self.selenium = selenium("localhost", 4444, testvars.MCTestVariables["Browser"], testvars.MCTestVariables["TestSite"])
        self.selenium.start()


# The user actions executed in the test scenario
    def test_ApproveVideo(self):
        sel = self.selenium
        loginlogout.LogInAsAdmin(self,sel)
        page = "Last"
        number = 1
        queue.ProcessVideo(self,sel,page,number,"Approved")

# Close the browser, log errors, perform cleanup    
    def tearDown(self):
        self.selenium.stop()
# the command on the previous line should close the browser
        self.assertEqual([], self.verificationErrors)



class TestCase_FeatureVideo(unittest.TestCase):
    
# Open the desired browser and set up the test
    def setUp(self):
        self.verificationErrors = []
        self.selenium = selenium("localhost", 4444, testvars.MCTestVariables["Browser"], testvars.MCTestVariables["TestSite"])
        self.selenium.start()

# The user actions executed in the test scenario
    def test_FeatureVideo(self):
        sel = self.selenium
        loginlogout.LogInAsAdmin(self,sel)
        page = "1"
        number = 1
        queue.ProcessVideo(self,sel,page,number,"Featured")

# Close the browser, log errors, perform cleanup    
    def tearDown(self):
        self.selenium.stop()
# the command on the previous line should close the browser
        self.assertEqual([], self.verificationErrors)


class TestCase_RejectVideo(unittest.TestCase):
    
# Open the desired browser and set up the test
    def setUp(self):
        self.verificationErrors = []
        self.selenium = selenium("localhost", 4444, testvars.MCTestVariables["Browser"], testvars.MCTestVariables["TestSite"])
        self.selenium.start()

# The user actions executed in the test scenario
    def test_RejectVideo(self):
        sel = self.selenium
        loginlogout.LogInAsAdmin(self,sel)
        page = "1"
        number = 1
        queue.ProcessVideo(self,sel,page,number,"Rejected")

# Close the browser, log errors, perform cleanup    
    def tearDown(self):
        self.selenium.stop()
# the command on the previous line should close the browser
        self.assertEqual([], self.verificationErrors)



class TestCase_ApprovePage(unittest.TestCase):
    
# Open the desired browser and set up the test
    def setUp(self):
        self.verificationErrors = []
        self.selenium = selenium("localhost", 4444, testvars.MCTestVariables["Browser"], testvars.MCTestVariables["TestSite"])
        self.selenium.start()

# The user actions executed in the test scenario
    def test_ApprovePage(self):
        sel = self.selenium
        loginlogout.LogInAsAdmin(self,sel)
        page = "1"
        queue.ApproveVideoPage(self,sel,page)

# Close the browser, log errors, perform cleanup    
    def tearDown(self):
        self.selenium.stop()
# the command on the previous line should close the browser
        self.assertEqual([], self.verificationErrors)


class TestCase_RejectPage(unittest.TestCase):
    
# Open the desired browser and set up the test
    def setUp(self):
        self.verificationErrors = []
        self.selenium = selenium("localhost", 4444, testvars.MCTestVariables["Browser"], testvars.MCTestVariables["TestSite"])
        self.selenium.start()

# The user actions executed in the test scenario
    def test_RejectPage(self):
        sel = self.selenium
        loginlogout.LogInAsAdmin(self,sel)
        page = "1"
        videosRejected = queue.RejectVideoPage(self,sel,page)
        # Check that videos were rejected
        print "Checking that videos were successfully rejected..."
        # At present, it is technically impossible to check the status for
        # every video on the rejected page because of an issue with
        # Bulk Edit page (5 or 6 are the viable limit)
        # As a temporary solution until the issue is resolved,
        # just three videos will be checked - the first, the last, and one
        # from the middle
        print "Looking up the following videos:"
        videosToCheck = [videosRejected[0],videosRejected[4],videosRejected[9]]
        print videosToCheck
        # Searching each selected video in the list of Rejected videos
        # on Bulk Edit page
        for item in videosToCheck:
            if item!="None":
                newResult=queue.CheckVideoStatus(self,sel,item,"Rejected")
                print item+"__________"+str(newResult)
                if newResult==False:
                    mclib.AppendErrorMessage(self,sel,"Could not find video "+item+" in the list of rejected videos.")
                sel.click(testvars.MCUI["AdminReviewQueue"])
                sel.click(testvars.MCTestVariables["ViewMainSiteLink"])
                sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])
                sel.click(testvars.MCTestVariables["ViewAdmin"])
                sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])
            else:
                print "None__________None"

# Close the browser, log errors, perform cleanup    
    def tearDown(self):
        self.selenium.stop()
# the command on the previous line should close the browser
        self.assertEqual([], self.verificationErrors)


class TestCase_ClearQueue(unittest.TestCase):
    
# Open the desired browser and set up the test
    def setUp(self):
        self.verificationErrors = []
        self.selenium = selenium("localhost", 4444, testvars.MCTestVariables["Browser"], testvars.MCTestVariables["TestSite"])
        self.selenium.start()

# The user actions executed in the test scenario
    def test_ClearQueue(self):
        sel = self.selenium
        loginlogout.LogInAsAdmin(self,sel)
        # Memorizing 
        videosRejected = queue.ClearQueue(self,sel)
        # Check that videos were rejected
        print "Checking that videos were successfully rejected..."
        # At present, it is technically impossible to check the status for
        # every video on the rejected page because of an issue with
        # Bulk Edit page (5 or 6 are the viable limit)
        # As a temporary solution until the issue is resolved,
        # just three videos will be checked - the first, the last, and one
        # from the middle
        print "Looking up the following videos:"
        last = len(videosRejected)-1
        videosToCheck = [videosRejected[0],videosRejected[last/2],videosRejected[last]]
        print videosToCheck
        # Searching each selected video in the list of Rejected videos
        # on Bulk Edit page
        for item in videosToCheck:
            if item!="None":
                newResult=queue.CheckVideoStatus(self,sel,item,"Rejected")
                print item+"__________"+str(newResult)
                if newResult==False:
                    mclib.AppendErrorMessage(self,sel,"Could not find video "+item+" in the list of rejected videos.")
                sel.click(testvars.MCUI["AdminReviewQueue"])
                sel.click(testvars.MCTestVariables["ViewMainSiteLink"])
                sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])
                sel.click(testvars.MCTestVariables["ViewAdmin"])
                sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])
            else:
                print "None__________None"

        
# Close the browser, log errors, perform cleanup    
    def tearDown(self):
        self.selenium.stop()
# the command on the previous line should close the browser
        self.assertEqual([], self.verificationErrors)


class TestCase_EditVideoInQueue(unittest.TestCase):
    
# Open the desired browser and set up the test
    def setUp(self):
        self.verificationErrors = []
        self.selenium = selenium("localhost", 4444, testvars.MCTestVariables["Browser"], testvars.MCTestVariables["TestSite"])
        self.selenium.start()

# The user actions executed in the test scenario
    def test_EditVideoInQueue(self):
        sel = self.selenium
        loginlogout.LogInAsAdmin(self,sel)
        page = "Last"
        number = 1
        title = "Test "+time.strftime("%d-%m-%Y %H:%M:%S", time.localtime())
        user = "Selene Test-Admin"
        posted = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        thumbnail = testvars.MCTestVariables["GraphicFilesDirectory"]+"\\"+"background3.jpg"
        description = "Test Description"
        category = "art"
        tag = "test"
        website = "http://www.youtube.com/watch?v=oCflnfXt4N0"
        queue.EditVideoInQueue(self,sel,page,number,title,user,posted,thumbnail,description,category,tag,website)

# Close the browser, log errors, perform cleanup    
    def tearDown(self):
        self.selenium.stop()
# the command on the previous line should close the browser
        self.assertEqual([], self.verificationErrors)


class TestCase_RSSVideosAwaitingModeration(unittest.TestCase):
    
# Open the desired browser and set up the test
    def setUp(self):
        self.verificationErrors = []
        self.selenium = selenium("localhost", 4444, testvars.MCTestVariables["Browser"], testvars.MCTestVariables["TestSite"])
        self.selenium.start()

# The user actions executed in the test scenario
    def test_RSSVideosAwaitingModeration(self):
        sel = self.selenium
        loginlogout.LogInAsAdmin(self,sel)
        currentLink="Unapproved RSS"
        print "Clicking "+currentLink+" link"
        queue.ViewRSSFeeds(self,sel,currentLink)
        print ""
        currentLink="Unapproved User RSS"
        print "Clicking "+currentLink+" link"
        queue.ViewRSSFeeds(self,sel,currentLink)

# Close the browser, log errors, perform cleanup    
    def tearDown(self):
        self.selenium.stop()
# the command on the previous line should close the browser
        self.assertEqual([], self.verificationErrors)
