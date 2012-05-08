#=======================================================================
#
#                       CUSTOMIZE DESIGN TESTS
#
#=======================================================================
#
# Includes the following test cases:
#     1. TestCase_EditSiteTitle_303
#     2. TestCase_MaxLengthSiteTitle_304
#     3. TestCase_EditSiteTagline_305
#     4. TestCase_MaxLengthSiteTagline_306
#     5. TestCase_EditAboutUs_307
#         TestCase_ChangeSiteSettings_303
#     2. TestCase_ChangeOrganization_253
#     3. TestCase_UploadLogo_243
#     4. TestCase_UploadBackground_244
#     5. TestCase_DeleteBackground_245
#     6. TestCase_AddCustomCSS_251
#     7. TestCase_DisplaySubmitVideo_249
#     8. TestCase_CheckRequireLoginToSubmitVideo_250


from selenium import selenium
import unittest, time, re, loginlogout, sitesettings, testvars
import mclib
import sys

# ----------------------------------------------------------------------


class TestCase_EditSiteTitle_303(unittest.TestCase):
    
# Open the desired browser and set up the test
    def setUp(self):
        self.verificationErrors = []
        self.selenium = selenium("localhost", testvars.MCTestVariables["Port"], testvars.MCTestVariables["Browser"], testvars.MCTestVariables["TestSite"])
        self.selenium.start()

# The user actions executed in the test scenario
    def EditSiteTitle_303(self,sel,theme):
        print ""
        print "Running EditSiteTitle test... with theme No."+str(theme)
#       Change site settings
        newtitle = "Dalmatia in Theme "+str(theme)
        sitesettings.EditSiteTitle(self,sel,theme,newtitle)

    def test_EditSiteTitle_303(self):
        sel = self.selenium
#       Log in as Admin
        loginlogout.LogInAsAdmin(self,sel)
#       Repeat for each theme from No.1 to No.4
        for theme in range(1,2):
            sitesettings.ChangeTheme(self,sel,theme)
            TestCase_EditSiteTitle_303.EditSiteTitle_303(self,sel,theme)
        
# Close the browser, log errors, perform cleanup    
    def tearDown(self):
        self.selenium.stop()
# the command on the previous line should close the browser
        self.assertEqual([], self.verificationErrors)

class TestCase_MaxLengthSiteTitle_304(unittest.TestCase):
    
# Open the desired browser and set up the test
    def setUp(self):
        self.verificationErrors = []
        self.selenium = selenium("localhost", testvars.MCTestVariables["Port"], testvars.MCTestVariables["Browser"], testvars.MCTestVariables["TestSite"])
        self.selenium.start()

# The user actions executed in the test scenario
    def MaxLengthSiteTitle_304(self,sel,theme, valid_title):
        print ""
        print "Running MaxLengthSiteTitle test... with theme No."+str(theme)
#       Change site settings
        sitesettings.EditSiteTitle(self,sel,theme,valid_title)

    def test_MaxLengthSiteTitle_304(self):
        sel = self.selenium
#       Log in as Admin
        loginlogout.LogInAsAdmin(self,sel)
#       Repeat for each theme from No.1 to No.4
        for theme in range(1,2):
            sitesettings.ChangeTheme(self,sel,theme)
            # Create a title with a timestamp
            timestamp = time.strftime("%d-%m-%Y %H:%M:%S", time.localtime())
            valid_title = 'MiroCommunity Title-SeleniumRC-' + timestamp
            # If necessary, extend the title to match the maximum permitted length
            while len(valid_title) < testvars.MCTestVariables["MaxSiteTitle"]:
                valid_title = valid_title+'X'
            TestCase_MaxLengthSiteTitle_304.MaxLengthSiteTitle_304(self,sel,theme,valid_title)
        # Attempt to enter max+1 characters into Site Title field
        sitesettings.NavigateToSettingsPage(self,sel)
        invalid_title = valid_title + str(theme)
        if sel.is_element_present("id_title")==False:
            mclib.AppendErrorMessage(self,sel,"Site Title edit field not found")
        else:
            print ""
            print ""
            print "Attempting to type an invalid long string into Site Title field..."
            sel.click("id_title")
            sel.type("id_title", invalid_title)
            typed_value = sel.get_value("id_title")
            if typed_value==invalid_title:
                mclib.AppendErrorMessage(self,sel,"Site Title accepts strings exceeding the maximum length")
            else:
                print "Cannot type overly long strings to Site Title field"
                print "Attempted to type: "+invalid_title
                print "-- Actually typed: "+typed_value
                print "OK"
        
# Close the browser, log errors, perform cleanup    
    def tearDown(self):
        self.selenium.stop()
# the command on the previous line should close the browser
        self.assertEqual([], self.verificationErrors)


class TestCase_EditSiteTagline_305(unittest.TestCase):
    
# Open the desired browser and set up the test
    def setUp(self):
        self.verificationErrors = []
        self.selenium = selenium("localhost", testvars.MCTestVariables["Port"], testvars.MCTestVariables["Browser"], testvars.MCTestVariables["TestSite"])
        self.selenium.start()

# The user actions executed in the test scenario
    def EditSiteTagline_305(self,sel,theme):
        print ""
        print "Running EditSiteTagline test... with theme No."+str(theme)
#       Change site settings
        timestamp = time.strftime("%d-%m-%Y %H:%M:%S", time.localtime())
        newtagline = 'Create your own site to share videos with friends-' + timestamp + '. Theme '+str(theme)
        sitesettings.EditSiteTagline(self,sel,theme,newtagline)

    def test_EditSiteTagline_305(self):
        sel = self.selenium
#       Log in as Admin
        loginlogout.LogInAsAdmin(self,sel)
#       Repeat for each theme from No.1 to No.4
        for theme in range(1,2):
            sitesettings.ChangeTheme(self,sel,theme)
            TestCase_EditSiteTagline_305.EditSiteTagline_305(self,sel,theme)
        
# Close the browser, log errors, perform cleanup    
    def tearDown(self):
        self.selenium.stop()
# the command on the previous line should close the browser
        self.assertEqual([], self.verificationErrors)


class TestCase_MaxLengthSiteTagline_306(unittest.TestCase):
    
# Open the desired browser and set up the test
    def setUp(self):
        self.verificationErrors = []
        self.selenium = selenium("localhost", testvars.MCTestVariables["Port"], testvars.MCTestVariables["Browser"], testvars.MCTestVariables["TestSite"])
        self.selenium.start()

# The user actions executed in the test scenario
    def MaxLengthSiteTagline_306(self,sel,theme, valid_tagline):
        print ""
        print "Running MaxLengthSiteTagline test... with theme No."+str(theme)
#       Change site settings
        sitesettings.EditSiteTagline(self,sel,theme,valid_tagline)

    def test_MaxLengthSiteTagline_306(self):
        sel = self.selenium
#       Log in as Admin
        loginlogout.LogInAsAdmin(self,sel)
#       Repeat for each theme from No.1 to No.4
        for theme in range(1,2):
            sitesettings.ChangeTheme(self,sel,theme)
            # Create a title with a timestamp
            valid_tagline = 'MC Theme' + str(theme)+' 123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 123456789 1234567890'
            # If necessary, extend the title to match the maximum permitted length
            while len(valid_tagline) < testvars.MCTestVariables["MaxSiteTagline"]:
                valid_tagline = valid_tagline+'X'
            TestCase_MaxLengthSiteTagline_306.MaxLengthSiteTagline_306(self,sel,theme,valid_tagline)
        # Attempt to enter max+1 characters into Site Title field
        sitesettings.NavigateToSettingsPage(self,sel)
        invalid_tagline = valid_tagline + str(theme)
        if sel.is_element_present("id_tagline")==False:
            mclib.AppendErrorMessage(self,sel,"Site Tagline edit field not found")
        else:
            print ""
            print ""
            print "Attempting to type an invalid long string into Site Tagline field..."
            sel.click("id_tagline")
            sel.type("id_tagline", invalid_tagline)
            typed_value = sel.get_value("id_tagline")
            if typed_value==invalid_tagline:
                mclib.AppendErrorMessage(self,sel,"Site Tagline accepts strings exceeding the maximum length")
            else:
                print "Cannot type overly long strings to Site Tagline field"
                print "Attempted to type: "+invalid_tagline
                print "-- Actually typed: "+typed_value
                print "OK"
        
# Close the browser, log errors, perform cleanup    
    def tearDown(self):
        self.selenium.stop()
# the command on the previous line should close the browser
        self.assertEqual([], self.verificationErrors)


class TestCase_EditAboutUs_307(unittest.TestCase):
    
# Open the desired browser and set up the test
    def setUp(self):
        self.verificationErrors = []
        self.selenium = selenium("localhost", testvars.MCTestVariables["Port"], testvars.MCTestVariables["Browser"], testvars.MCTestVariables["TestSite"])
        self.selenium.start()

# The user actions executed in the test scenario
    def EditAboutUs_307(self,sel,theme):
        print ""
        print "Running EditAboutUs test... with theme No."+str(theme)
#       Change site settings
        timestamp = time.strftime("%d-%m-%Y %H:%M:%S", time.localtime())
        newabouttext = 'Miro was first launched in 2005 as DTV, with the name being changed to Democracy Player in 2006.' + timestamp
        sitesettings.EditAboutUs(self,sel,theme,newabouttext)

    def test_EditAboutUs_307(self):
        sel = self.selenium
#       Log in as Admin
        loginlogout.LogInAsAdmin(self,sel)
#       Repeat for each theme from No.1 to No.4
        for theme in range(1,2):
            sitesettings.ChangeTheme(self,sel,theme)
            TestCase_EditAboutUs_307.EditAboutUs_307(self,sel,theme)
        
# Close the browser, log errors, perform cleanup    
    def tearDown(self):
        self.selenium.stop()
# the command on the previous line should close the browser
        self.assertEqual([], self.verificationErrors)


class TestCase_AboutUsHTML_309(unittest.TestCase):
    
# Open the desired browser and set up the test
    def setUp(self):
        self.verificationErrors = []
        self.selenium = selenium("localhost", testvars.MCTestVariables["Port"], testvars.MCTestVariables["Browser"], testvars.MCTestVariables["TestSite"])
        self.selenium.start()

# The user actions executed in the test scenario
    def AboutUsHTML_309(self,sel,theme, newabouttext):
        print ""
        print "Running AboutUsHTML test... with theme No."+str(theme)
#       Change site settings
        sitesettings.EditAboutUs(self,sel,theme,newabouttext)

    def test_AboutUsHTML_309(self):
        sel = self.selenium
#       Log in as Admin
        loginlogout.LogInAsAdmin(self,sel)
#       Repeat for each theme from No.1 to No.4
        for theme in range(1,2):
            sitesettings.ChangeTheme(self,sel,theme)
            # Create a title with a timestamp
            timestamp = time.strftime("%d-%m-%Y %H:%M:%S", time.localtime())
            newabouttext = timestamp+' This is the testing site for Miro Community <b style="COLOR: red">Title in bold</b> <h5 >Title in h5</h5> <h8>Title in h8</h8>'
            # If necessary, extend the title to match the maximum permitted length
            TestCase_AboutUsHTML_309.AboutUsHTML_309(self,sel,theme,newabouttext)
        
# Close the browser, log errors, perform cleanup    
    def tearDown(self):
        self.selenium.stop()
# the command on the previous line should close the browser
        self.assertEqual([], self.verificationErrors)


class TestCase_ChangeSiteSettings_303(unittest.TestCase):
    
# Open the desired browser and set up the test
    def setUp(self):
        self.verificationErrors = []
        self.selenium = selenium("localhost", testvars.MCTestVariables["Port"], testvars.MCTestVariables["Browser"], testvars.MCTestVariables["TestSite"])
        self.selenium.start()

# The user actions executed in the test scenario
    def ChangeSiteSettings(self,sel,theme):
        print ""
        print "Running ChangeSiteSettings test... with theme No."+str(theme)
#       Change site settings
        sitesettings.ModifySiteSettings(self,sel,theme)

    def test_ChangeSiteSettings_303(self):
        sel = self.selenium
#       Log in as Admin
        loginlogout.LogInAsAdmin(self,sel)
#       Repeat for each theme from No.1 to No.4
        for theme in range(1,2):
            sitesettings.ChangeTheme(self,sel,theme)
            TestCase_ChangeSiteSettings_303.ChangeSiteSettings(self,sel,theme)
        
# Close the browser, log errors, perform cleanup    
    def tearDown(self):
        self.selenium.stop()
# the command on the previous line should close the browser
        self.assertEqual([], self.verificationErrors)


class TestCase_ChangeOrganization_253(unittest.TestCase):
    
# Open the desired browser and set up the test
    def setUp(self):
        self.verificationErrors = []
        self.selenium = selenium("localhost", testvars.MCTestVariables["Port"], testvars.MCTestVariables["Browser"], testvars.MCTestVariables["TestSite"])
        self.selenium.start()

# The user actions executed in the test scenario
    def ChangeOrganizationSettings(self,sel,theme):
        print "Running ChangeOrganizationSettings test... with theme No."+str(theme)
#       Change site settings
        sitesettings.ModifyOrganizationSettings(self,sel,theme)

    def test_ChangeOrganizationSettings_253(self):
        sel = self.selenium
#       Log in as Admin
        loginlogout.LogInAsAdmin(self,sel)
#       Repeat for each theme from No.1 to No.4
        for theme in range(1,2):
            sitesettings.ChangeTheme(self,sel,theme)
            # Change site settings
            TestCase_ChangeOrganization_253.ChangeOrganizationSettings(self,sel,theme)

# Close the browser, log errors, perform cleanup    
    def tearDown(self):
        self.selenium.stop()
# the command on the previous line should close the browser
        self.assertEqual([], self.verificationErrors)


class TestCase_UploadLogo_243(unittest.TestCase):
    
# Open the desired browser and set up the test
    def setUp(self):
        self.verificationErrors = []
        self.selenium = selenium("localhost", testvars.MCTestVariables["Port"], testvars.MCTestVariables["Browser"], testvars.MCTestVariables["TestSite"])
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
        
    def test_UploadLogo_243(self):
        sel = self.selenium
#       Log in as Admin
        loginlogout.LogInAsAdmin(self,sel)
#       Repeat for each theme from No.1 to No.4
        for theme in range(1,2):
            sitesettings.ChangeTheme(self,sel,theme)
            TestCase_UploadLogo_243.UploadLogo(self,sel,theme)
        
# Close the browser, log errors, perform cleanup    
    def tearDown(self):
        self.selenium.stop()
# the command on the previous line should close the browser
        self.assertEqual([], self.verificationErrors)


class TestCase_UploadBackground_244(unittest.TestCase):
    
# Open the desired browser and set up the test
    def setUp(self):
        self.verificationErrors = []
        self.selenium = selenium("localhost", testvars.MCTestVariables["Port"], testvars.MCTestVariables["Browser"], testvars.MCTestVariables["TestSite"])
        self.selenium.start()

# The user actions executed in the test scenario
    def UploadBackground(self,sel,theme):
        print ""
        print "Running UploadBackground test... with theme No."+str(theme)
        newbkgr = "background4.jpg"
        print "Uploading file: "+newbkgr
#       Upload new background image
        sitesettings.UploadBackgroundImage(self,sel,theme,newbkgr)
        
    def test_UploadBackground_244(self):
        sel = self.selenium
#       Log in as Admin
        loginlogout.LogInAsAdmin(self,sel)
#       Repeat for each theme from No.1 to No.4
        for theme in range(1,2):
            sitesettings.ChangeTheme(self,sel,theme)
            TestCase_UploadBackground_244.UploadBackground(self,sel,theme)
        

# Close the browser, log errors, perform cleanup    
    def tearDown(self):
        self.selenium.stop()
# the command on the previous line should close the browser
        self.assertEqual([], self.verificationErrors)


class TestCase_DeleteBackground_245(unittest.TestCase):
    
# Open the desired browser and set up the test
    def setUp(self):
        self.verificationErrors = []
        self.selenium = selenium("localhost", testvars.MCTestVariables["Port"], testvars.MCTestVariables["Browser"], testvars.MCTestVariables["TestSite"])
        self.selenium.start()

# The user actions executed in the test scenario
    def DeleteBackground(self,sel):
        print ""
        print "Running DeleteBackground test..."
#       Delete background
        sitesettings.DeleteBackgroundImage(self,sel)
        
    def test_DeleteBackground_245(self):
        sel = self.selenium
#       Log in as Admin
        loginlogout.LogInAsAdmin(self,sel)
        TestCase_DeleteBackground_245.DeleteBackground(self,sel)
        

# Close the browser, log errors, perform cleanup    
    def tearDown(self):
        self.selenium.stop()
# the command on the previous line should close the browser
        self.assertEqual([], self.verificationErrors)



class TestCase_AddCustomCSS_251(unittest.TestCase):
    
# Open the desired browser and set up the test
    def setUp(self):
        self.verificationErrors = []
        self.selenium = selenium("localhost", testvars.MCTestVariables["Port"], testvars.MCTestVariables["Browser"], testvars.MCTestVariables["TestSite"])
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
        
    def test_AddCustomCSS_251(self):
        sel = self.selenium
#       Log in as Admin
        loginlogout.LogInAsAdmin(self,sel)
        TestCase_AddCustomCSS_251.AddCustomCSS(self,sel)

# Close the browser, log errors, perform cleanup    
    def tearDown(self):
        self.selenium.stop()
# the command on the previous line should close the browser
        self.assertEqual([], self.verificationErrors)



class TestCase_DisplaySubmitVideo_249(unittest.TestCase):
    
# Open the desired browser and set up the test
    def setUp(self):
        self.verificationErrors = []
        self.selenium = selenium("localhost", testvars.MCTestVariables["Port"], testvars.MCTestVariables["Browser"], testvars.MCTestVariables["TestSite"])
        self.selenium.start()

# The user actions executed in the test scenario
    def DisplaySubmitVideo(self,sel,theme):
        print ""
        print "Running DisplaySubmitVideo test... with theme No."+str(theme)
#       Check Display Submit a Video check box 
        sitesettings.DisplaySubmitVideo(self,sel,theme)
#       Uncheck Display Submit a Video check box 
        sitesettings.HideSubmitVideo(self,sel,theme)
        
    def test_DisplaySubmitVideo_249(self):
        sel = self.selenium
#       Log in as Admin
        loginlogout.LogInAsAdmin(self,sel)
#       Repeat for each theme from No.1 to No.4
        for theme in range(1,2):
            sitesettings.ChangeTheme(self,sel,theme)
            TestCase_DisplaySubmitVideo_249.DisplaySubmitVideo(self,sel,theme)

# Close the browser, log errors, perform cleanup    
    def tearDown(self):
        self.selenium.stop()
# the command on the previous line should close the browser
        self.assertEqual([], self.verificationErrors)


class TestCase_CheckRequireLoginToSubmitVideo_250(unittest.TestCase):
    
# Open the desired browser and set up the test
    def setUp(self):
        self.verificationErrors = []
        self.selenium = selenium("localhost", testvars.MCTestVariables["Port"], testvars.MCTestVariables["Browser"], testvars.MCTestVariables["TestSite"])
        self.selenium.start()

# The user actions executed in the test scenario
    def CheckRequireLoginToSubmitVideo(self,sel,theme):
        print "Running CheckRequireLoginToSubmitVideo test... with theme No."+str(theme)
#       Change site settings
        sitesettings.CheckRequireLoginToSubmitVideo(self,sel,theme)

    def test_CheckRequireLoginToSubmitVideo_250(self):
        sel = self.selenium
#       Repeat for each theme from No.1 to No.4
        for theme in range(1,2):
            print ""
            print ""
            # Log in as Admin
            loginlogout.LogInAsAdmin(self,sel)
            # Change theme
            sitesettings.ChangeTheme(self,sel,theme)
            # Change site settings
            TestCase_CheckRequireLoginToSubmitVideo_250.CheckRequireLoginToSubmitVideo(self,sel,theme)

# Close the browser, log errors, perform cleanup    
    def tearDown(self):
        self.selenium.stop()
# the command on the previous line should close the browser
        self.assertEqual([], self.verificationErrors)
