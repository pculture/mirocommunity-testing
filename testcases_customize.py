#=======================================================================
#
#                       CUSTOMIZE DESIGN TESTS
#
#=======================================================================
#
# Includes the following test cases:
#     1. TestCase_ChangeSiteSettings
#     2. TestCase_ChangeOrganization
#     3. TestCase_UploadLogo
#     4. TestCase_UploadBackground
#     5. TestCase_DeleteBackground
#     6. TestCase_AddCustomCSS
#     7. TestCase_DisplaySubmitVideo
#     8. TestCase_CheckRequireLoginToSubmitVideo


from selenium import selenium
import unittest, time, re, loginlogout, sitesettings, testvars
import sys

# ----------------------------------------------------------------------


class TestCase_ChangeSiteSettings(unittest.TestCase):
    
# Open the desired browser and set up the test
    def setUp(self):
        self.verificationErrors = []
        self.selenium = selenium("localhost", 4444, testvars.MCTestVariables["Browser"], testvars.MCTestVariables["TestSite"])
        self.selenium.start()

# The user actions executed in the test scenario
    def ChangeSiteSettings(self,sel,theme):
        print ""
        print "Running ChangeSiteSettings test... with theme No."+str(theme)
#       Change site settings
        sitesettings.ModifySiteSettings(self,sel,theme)

    def test_ChangeSiteSettings(self):
        sel = self.selenium
#       Log in as Admin
        loginlogout.LogInAsAdmin(self,sel)
#       Repeat for each theme from No.1 to No.4
        for theme in range(1,5):
            sitesettings.ChangeTheme(self,sel,theme)
            TestCase_ChangeSiteSettings.ChangeSiteSettings(self,sel,theme)
        
# Close the browser, log errors, perform cleanup    
    def tearDown(self):
        self.selenium.stop()
# the command on the previous line should close the browser
        self.assertEqual([], self.verificationErrors)


class TestCase_ChangeOrganization(unittest.TestCase):
    
# Open the desired browser and set up the test
    def setUp(self):
        self.verificationErrors = []
        self.selenium = selenium("localhost", 4444, testvars.MCTestVariables["Browser"], testvars.MCTestVariables["TestSite"])
        self.selenium.start()

# The user actions executed in the test scenario
    def ChangeOrganizationSettings(self,sel,theme):
        print "Running ChangeOrganizationSettings test... with theme No."+str(theme)
#       Change site settings
        sitesettings.ModifyOrganizationSettings(self,sel,theme)

    def test_ChangeOrganizationSettings(self):
        sel = self.selenium
#       Log in as Admin
        loginlogout.LogInAsAdmin(self,sel)
#       Repeat for each theme from No.1 to No.4
        for theme in range(1,5):
            sitesettings.ChangeTheme(self,sel,theme)
            # Change site settings
            TestCase_ChangeOrganization.ChangeOrganizationSettings(self,sel,theme)

# Close the browser, log errors, perform cleanup    
    def tearDown(self):
        self.selenium.stop()
# the command on the previous line should close the browser
        self.assertEqual([], self.verificationErrors)


class TestCase_UploadLogo(unittest.TestCase):
    
# Open the desired browser and set up the test
    def setUp(self):
        self.verificationErrors = []
        self.selenium = selenium("localhost", 4444, testvars.MCTestVariables["Browser"], testvars.MCTestVariables["TestSite"])
        self.selenium.start()

# The user actions executed in the test scenario
    def UploadLogo(self,sel,theme):
        print ""
        print "Running UploadLogo test... with theme No."+str(theme)
        newlogo = "dalmatia1.jpg"
        print "Uploading file: "+newlogo
#       Upload new site logo
        sitesettings.UploadSiteLogo(self,sel,theme,newlogo)
        # Repeat for another file. This is done to ensure that logo actually changes at each test run
        newlogo = "dalmatia2.jpg"
        print "Uploading file: "+newlogo
#       Upload new site logo
        sitesettings.UploadSiteLogo(self,sel,theme,newlogo)
        
    def test_UploadLogo(self):
        sel = self.selenium
#       Log in as Admin
        loginlogout.LogInAsAdmin(self,sel)
#       Repeat for each theme from No.1 to No.4
        for theme in range(1,5):
            sitesettings.ChangeTheme(self,sel,theme)
            TestCase_UploadLogo.UploadLogo(self,sel,theme)
        
# Close the browser, log errors, perform cleanup    
    def tearDown(self):
        self.selenium.stop()
# the command on the previous line should close the browser
        self.assertEqual([], self.verificationErrors)


class TestCase_UploadBackground(unittest.TestCase):
    
# Open the desired browser and set up the test
    def setUp(self):
        self.verificationErrors = []
        self.selenium = selenium("localhost", 4444, testvars.MCTestVariables["Browser"], testvars.MCTestVariables["TestSite"])
        self.selenium.start()

# The user actions executed in the test scenario
    def UploadBackground(self,sel,theme):
        print ""
        print "Running UploadBackground test... with theme No."+str(theme)
        newbkgr = "background5.jpg"
        print "Uploading file: "+newbkgr
#       Upload new background image
        sitesettings.UploadBackgroundImage(self,sel,theme,newbkgr)
        
    def test_UploadBackground(self):
        sel = self.selenium
#       Log in as Admin
        loginlogout.LogInAsAdmin(self,sel)
#       Repeat for each theme from No.1 to No.4
        for theme in range(1,5):
            sitesettings.ChangeTheme(self,sel,theme)
            TestCase_UploadBackground.UploadBackground(self,sel,theme)
        

# Close the browser, log errors, perform cleanup    
    def tearDown(self):
        self.selenium.stop()
# the command on the previous line should close the browser
        self.assertEqual([], self.verificationErrors)


class TestCase_DeleteBackground(unittest.TestCase):
    
# Open the desired browser and set up the test
    def setUp(self):
        self.verificationErrors = []
        self.selenium = selenium("localhost", 4444, testvars.MCTestVariables["Browser"], testvars.MCTestVariables["TestSite"])
        self.selenium.start()

# The user actions executed in the test scenario
    def DeleteBackground(self,sel):
        print ""
        print "Running DeleteBackground test..."
#       Delete background
        sitesettings.DeleteBackgroundImage(self,sel)
        
    def test_DeleteBackground(self):
        sel = self.selenium
#       Log in as Admin
        loginlogout.LogInAsAdmin(self,sel)
        TestCase_DeleteBackground.DeleteBackground(self,sel)
        

# Close the browser, log errors, perform cleanup    
    def tearDown(self):
        self.selenium.stop()
# the command on the previous line should close the browser
        self.assertEqual([], self.verificationErrors)



class TestCase_AddCustomCSS(unittest.TestCase):
    
# Open the desired browser and set up the test
    def setUp(self):
        self.verificationErrors = []
        self.selenium = selenium("localhost", 4444, testvars.MCTestVariables["Browser"], testvars.MCTestVariables["TestSite"])
        self.selenium.start()

# The user actions executed in the test scenario
    def AddCustomCSS(self,sel):
        print ""
        print "Running AddCustomCSS test..."
        cssString = "body\n{\nbackground-color:#d0e4fe;\n}\nh1\n{\ncolor:orange;\ntext-align:center;\n}\np\n{\nfont-family:\"Times New Roman\";\nfont-size:20px;\n}"
        print "Adding CSS: "+cssString
#       Add custom CSS
        sitesettings.AddCustomCSS(self,sel,cssString)
        print "Deleting custom CSS"
        sitesettings.DeleteCustomCSS(self,sel)
        
    def test_AddCustomCSS(self):
        sel = self.selenium
#       Log in as Admin
        loginlogout.LogInAsAdmin(self,sel)
        TestCase_AddCustomCSS.AddCustomCSS(self,sel)

# Close the browser, log errors, perform cleanup    
    def tearDown(self):
        self.selenium.stop()
# the command on the previous line should close the browser
        self.assertEqual([], self.verificationErrors)



class TestCase_DisplaySubmitVideo(unittest.TestCase):
    
# Open the desired browser and set up the test
    def setUp(self):
        self.verificationErrors = []
        self.selenium = selenium("localhost", 4444, testvars.MCTestVariables["Browser"], testvars.MCTestVariables["TestSite"])
        self.selenium.start()

# The user actions executed in the test scenario
    def DisplaySubmitVideo(self,sel,theme):
        print ""
        print "Running DisplaySubmitVideo test... with theme No."+str(theme)
#       Check Display Submit a Video check box 
        sitesettings.DisplaySubmitVideo(self,sel,theme)
#       Uncheck Display Submit a Video check box 
        sitesettings.HideSubmitVideo(self,sel,theme)
        
    def test_DisplaySubmitVideo(self):
        sel = self.selenium
#       Log in as Admin
        loginlogout.LogInAsAdmin(self,sel)
#       Repeat for each theme from No.1 to No.4
        for theme in range(1,5):
            sitesettings.ChangeTheme(self,sel,theme)
            TestCase_DisplaySubmitVideo.DisplaySubmitVideo(self,sel,theme)

# Close the browser, log errors, perform cleanup    
    def tearDown(self):
        self.selenium.stop()
# the command on the previous line should close the browser
        self.assertEqual([], self.verificationErrors)


class TestCase_CheckRequireLoginToSubmitVideo(unittest.TestCase):
    
# Open the desired browser and set up the test
    def setUp(self):
        self.verificationErrors = []
        self.selenium = selenium("localhost", 4444, testvars.MCTestVariables["Browser"], testvars.MCTestVariables["TestSite"])
        self.selenium.start()

# The user actions executed in the test scenario
    def CheckRequireLoginToSubmitVideo(self,sel,theme):
        print "Running CheckRequireLoginToSubmitVideo test... with theme No."+str(theme)
#       Change site settings
        sitesettings.CheckRequireLoginToSubmitVideo(self,sel,theme)

    def test_CheckRequireLoginToSubmitVideo(self):
        sel = self.selenium
#       Repeat for each theme from No.1 to No.4
        for theme in range(1,5):
            # Log in as Admin
            loginlogout.LogInAsAdmin(self,sel)
            # Change theme
            sitesettings.ChangeTheme(self,sel,theme)
            # Change site settings
            TestCase_CheckRequireLoginToSubmitVideo.CheckRequireLoginToSubmitVideo(self,sel,theme)

# Close the browser, log errors, perform cleanup    
    def tearDown(self):
        self.selenium.stop()
# the command on the previous line should close the browser
        self.assertEqual([], self.verificationErrors)
