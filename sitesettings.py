# Module SITESETTINGS.PY
# includes:
#   * subroutine ChangeTheme(self,sel,theme) - sets the desired theme
#   * function ThemeScanner(self,sel,theme) - detects the currently set theme
#   * subroutine EditSiteTitle(self,sel,theme,newtitle) - changes the site title to <newtitle>
#   * subroutine EditSiteTagline(self,sel,theme,newtagline) - changes the site tagline to <newtagline>
#   * subroutine EditAboutUs(self,sel,theme,newabouttext) - changes About Us text to <newabouttext>
#   * subroutine ModifySiteSettings(self,sel,theme) - changes the site settings
#          (title, tagline, about) and verifies that they save and display correctly
#   * subroutine ModifyOrganizationSettings(self,sel,theme) - changes organization
#          settings and verifies that they are displayed correctly
#   * subroutine UploadSiteLogo(self,sel,theme,newlogo) - uploads <newlogo> graphic 
#          file from the test suite graphic directory as a site logo
#   * subroutine UploadBackgroundImage(self,sel,theme,background) - uploads <background>
#          file from the test suite graphic directory as a background image
#   * subroutine DeleteBackgroundImage(self,sel) - deletes the background from 
#          the front pages
#   * subroutine AddCustomCSS(self,sel,customcss) - adds custom CSS to the site 
#           settings and verifies that it was applied correctly
#   * subroutine DeleteCustomCSS(self,sel) - deletes custom CSS from the site settings
#           and verifies that the front pages do not contain custom styling
#   * subroutine DisplaySubmitVideo(self,sel,theme) - makes Submit Video button displayed
#           on the front pages
#   * subroutine HideSubmitVideo(self,sel,theme) - hides Submit Video button on the
#           front pages
#   * subroutine CheckRequireLoginToSubmitVideo(self,sel,theme) - checks 'Require Users to
#           Login to Submit a Video' check box and checks that Submit a Video button is
#           shown only to logged users
#   * subroutine UncheckRequireLoginToSubmitVideo(self,sel) - unchecks Require Users
#           to Login to Submit a Video check box
#   * subroutine CheckUseOriginalDate(self,sel) - checks Use Original Date check box
#   * subroutine EnablePlaylists(self,sel,option) - enables or disables playlists
#           <option> can take values "Yes", "No", or "Admins Only"



from selenium import selenium

import unittest, time, re, platform, os
import testvars, loginlogout, mclib

def NavigateToSettingsPage(self,sel):
    sel.open(testvars.MCTestVariables["SettingsPage"])
    try: self.failUnless(sel.is_text_present("Design and Content"))
    except AssertionError, e: self.fail("Not logged in as an Administrator")


# =======================================
# =            CHANGE THEME             =
# =======================================

# This subroutine changes the theme to the value defined by 'theme'
# parameter as follows:
# 1 - list theme
# 2 - scrolling theme
# 3 - category theme
# 4 - blue theme

def ChangeTheme(self,sel,theme):
    if theme==1:
        sel.open(testvars.MCTestVariables["ListThemeLink"])
    elif theme==2:
        sel.open(testvars.MCTestVariables["ScrollingThemeLink"])
    elif theme==3:
        sel.open(testvars.MCTestVariables["CategoryThemeLink"])
    elif theme==4:
        sel.open(testvars.MCTestVariables["BlueThemeLink"])
    else:
        self.verificationErrors.append("Incorrect theme passed to ChangeTheme subroutine. theme="+str(theme))


# =======================================
# =         DETECT CURRENT THEME        =
# =======================================

# This function returns the number corresponding to the currently
# set theme as follows:
# 1 - list theme
# 2 - scrolling theme
# 3 - category theme
# 4 - blue theme

def ThemeScanner(self,sel):
    res=0
    if sel.is_element_present("//div[@id='slider2']")==True:
        if sel.get_text("//div[@id='content']/div[2]/div")=="Categories":
            res=3
        else:
            res=2
    elif sel.is_element_present("//div[@id='chained']")==True:
        res=4
    else:
        res=1
    return res
    
# ===================================
# =          EDIT SITE TITLE        =
# ===================================
 
# This subroutine changes the site title to <newtitle>

def EditSiteTitle(self,sel,theme,newtitle):
    NavigateToSettingsPage(self,sel)
# Type the values into edit fields
    if sel.is_element_present("id_title")==False:
        mclib.AppendErrorMessage(self,sel,"Site Title edit field not found")
    else:
        sel.click("id_title")
        sel.type("id_title", newtitle)
        if sel.is_element_present("submit_settings")==False:
            mclib.AppendErrorMessage(self,sel,"Save Changes button not found")
        else:
            # Click Save
            sel.click("submit_settings")
            sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])
    # ------ Workaround for blank page bug
            sel.open(testvars.MCTestVariables["CategoriesPage"])
            time.sleep(3)
            sel.open(testvars.MCTestVariables["SettingsPage"])
            sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])
    # --------- End of workaround insert
            print "Changed site title to: "+newtitle
           # Check that the TITLE in the admin interface is present, visible and correct
            elementTitle="//div[@id='logo']/a/span"
            print "Checking site title in the administrator interface..."
            if sel.is_element_present(elementTitle)==False:
                mclib.AppendErrorMessage(self,sel,"Title is not present in the Administrator interface")
            elif sel.is_visible(elementTitle)==False:
                mclib.AppendErrorMessage(self,sel,"Title is not visible in the Administrator interface")
            elif sel.get_text(elementTitle)!=newtitle:
                mclib.AppendErrorMessage(self,sel,"Wrong site title in the administrator interface.")
                print "Expected title is "+newtitle
                print "- Actual title is "+sel.get_text(elementTitle)
            else:
                print "OK"
        
# Click View Main Site
            #sel.click(testvars.MCTestVariables["ViewMainSiteLink"])
            sel.open(testvars.MCTestVariables["TestSite"])
            sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])
# Check that the TITLE on the main site is present, visible and correct
            if theme==4:
                elementTitle="//div[@id='wrapper']/div[1]/div/div[1]/h1/a"
            else:
                elementTitle="//div[@id='logo']/h1/a/span"
            if sel.is_element_present(elementTitle)==False:
                mclib.AppendErrorMessage(self,sel,"Title is not present on the main site")
            elif sel.is_visible(elementTitle)==False:
                mclib.AppendErrorMessage(self,sel,"Title is not visible on the main site")
            elif sel.get_text(elementTitle)!=newtitle:
                mclib.AppendErrorMessage(self,sel,"Wrong site title on the main site.")
                print "Expected title is "+newtitle
                print "- Actual title is "+sel.get_text(elementTitle)
            else:
                print "OK"


# ===================================
# =        EDIT SITE TAGLINE        =
# ===================================
 
# This subroutine changes the site tagline to <newtagline>

def EditSiteTagline(self,sel,theme,newtagline):
    NavigateToSettingsPage(self,sel)
# Type the values into edit fields
    if sel.is_element_present("id_tagline")==False:
        mclib.AppendErrorMessage(self,sel,"Site Tagline edit field not found")
    else:
        sel.click("id_tagline")
        sel.type("id_tagline", newtagline)
        if sel.is_element_present("submit_settings")==False:
            mclib.AppendErrorMessage(self,sel,"Save Changes button not found")
        else:
            # Click Save
            sel.click("submit_settings")
            sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])
    # ------ Workaround for blank page bug
            sel.open(testvars.MCTestVariables["CategoriesPage"])
            time.sleep(3)
            sel.open(testvars.MCTestVariables["SettingsPage"])
            sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])
    # --------- End of workaround insert
            print "Changed site tagline to: "+newtagline
#----- As of Dec.2010, tagline is no longer displayed in the admin interface
           # Check that the TAGLINE in the admin interface is present, visible and correct
#            elementTagline="//div[@id='logo']/h1/span"
#            print "Checking site tagline in the administrator interface..."
#            if sel.is_element_present(elementTagline)==False:
#                mclib.AppendErrorMessage(self,sel,"Tagline is not present in the Administrator interface")
#            elif sel.is_visible(elementTagline)==False:
#                mclib.AppendErrorMessage(self,sel,"Tagline is not visible in the Administrator interface")
#            elif sel.get_text(elementTagline)!=newtagline:
#                mclib.AppendErrorMessage(self,sel,"Wrong site tagline in the administrator interface.")
#                print "Expected tagline is "+newtagline
#                print "- Actual tagline is "+sel.get_text(elementTagline)
#            else:
#                print "OK"
        
# Click View Main Site
            #sel.click(testvars.MCTestVariables["ViewMainSiteLink"])
            sel.open(testvars.MCTestVariables["TestSite"])
            sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])
# Check that the TAGLINE on the main site is present, visible and correct
            if theme==4:
                elementTagline="//div[@id='wrapper']/div[1]/div/div[1]/p"
            else:
                elementTagline="//div[@id='logo']/h1/span"
            print "Checking site tagline on the main site..."
            if sel.is_element_present(elementTagline)==False:
                mclib.AppendErrorMessage(self,sel,"Tagline is not present on the main site")
            elif sel.is_visible(elementTagline)==False:
                mclib.AppendErrorMessage(self,sel,"Tagline is not visible on the main site")
            elif sel.get_text(elementTagline)!=newtagline:
                mclib.AppendErrorMessage(self,sel,"Wrong site tagline on the main site.")
                print "Expected tagline is "+newtagline
                print "- Actual tagline is "+sel.get_text(elementTagline)
            else:
                print "OK"


# ===================================
# =        EDIT ABOUT US INFO       =
# ===================================
 
# This subroutine changes About Us information to <newabouttext>

def EditAboutUs(self,sel,theme,newabouttext):
    NavigateToSettingsPage(self,sel)
# Type the values into edit fields
    if sel.is_element_present("id_about_html")==False:
        mclib.AppendErrorMessage(self,sel,"About Us edit field not found")
    else:
        sel.click("id_about_html")
        sel.type("id_about_html", newabouttext)
        if sel.is_element_present("submit_settings")==False:
            mclib.AppendErrorMessage(self,sel,"Save Changes button not found")
        else:
            # Click Save
            sel.click("submit_settings")
            sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])
    # ------ Workaround for blank page bug
            sel.open(testvars.MCTestVariables["CategoriesPage"])
            time.sleep(3)
            sel.open(testvars.MCTestVariables["SettingsPage"])
            sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])
    # --------- End of workaround insert
            print "Changed About Us text to: "+newabouttext
        
            # Click View Main Site
            #sel.click(testvars.MCTestVariables["ViewMainSiteLink"])
            sel.open(testvars.MCTestVariables["TestSite"])
            sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])
            # CHECK ABOUT PAGE
            # Navigate to About page
            sel.open("/about")
            sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])
            # Verify About text
            print "Verifying About Us text..."
            trimmedAboutText = mclib.remove_html_tags(newabouttext)
#            print trimmedAboutText
            mainText = str(sel.get_text("//div[@id='main']"))
            #for i in mainText:
            #    print str(ord(i))+","
            if theme==4:
                elementAbout="//div[@id='main']/p[1]"
#                elementAbout="//div[@id='main']/div[1]/h2"
#            else:
#                elementAbout="//div[@id='main']/h2[1]"
                mainText = mainText.replace('\n','')
            # Check that elementAbout exists
                if sel.is_element_present(elementAbout)==False:
                    mclib.AppendErrorMessage(self,sel,"About Us information is not present on About Us page")
                elif sel.is_visible(elementAbout)==False:
                    mclib.AppendErrorMessage(self,sel,"About Us information is not visible on the About Us page")
                elif sel.get_text(elementAbout)!=newabouttext and mainText.find(trimmedAboutText)==-1:
                    mclib.AppendErrorMessage(self,sel,"Wrong About Us text on About page.")
                    print "Expected text is "+trimmedAboutText
                    print "- Actual text is "+mainText
                else:
                    print "OK"
            else:
                if mainText.find(newabouttext)==-1 and mainText.find(trimmedAboutText)==-1:
                    mclib.AppendErrorMessage(self,sel,"Updated About Us text not found on About page")
                    print "Expected text: "+trimmedAboutText
                    print "Actual text on the main page"+mainText
                else:
                    print "OK"


# ===================================
# =      MODIFY SITE SETTINGS       =
# ===================================
 
# This subroutine changes the site parameters (title, tagline, footer text) to a conventional test string
# containing a timestamp (dd-mm-yyyy hh:mm:ss)

def ModifySiteSettings(self,sel,theme):
#===========MODIFY PARAMETERS===============
    NavigateToSettingsPage(self,sel)
# Set new values for site parameters
    timestamp = time.strftime("%d-%m-%Y %H:%M:%S", time.localtime())
    vTitle = 'MiroCommunity Title-SeleniumRC-' + timestamp
    vTagLine = 'Create your own site to share videos with friends-' + timestamp
    vAboutUs = 'Miro was first launched in 2005 as DTV, with the name being changed to Democracy Player in 2006.' + timestamp
    vFooter=vTitle+' is powered by Miro Community'
#    vFooter=vTitle+' is powered by Miro Community Logout '+testvars.MCTestVariables["AdminLogin"]
# Type the values into edit fields
    sel.click("id_title")
    sel.type("id_title", vTitle)
    sel.click("id_tagline")
    sel.type("id_tagline", vTagLine)
    sel.click("id_about_html")
    sel.type("id_about_html", vAboutUs)
# Click Save
    sel.click("submit_settings")
    sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])
    # ------ Workaround for blank page bug
    sel.open(testvars.MCTestVariables["CategoriesPage"])
    time.sleep(3)
    sel.open(testvars.MCTestVariables["SettingsPage"])
    sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])
    # --------- End of workaround insert
    print "Changed site title, tagline, about text"
    
# ==========CHECKS ON ADMIN INTERFACE===========

# Check that the TITLE in the admin interface is present, visible and correct
    elementTitle="//div[@id='logo']/h1/a"
    if sel.is_element_present(elementTitle)==True:
        if sel.is_visible(elementTitle)==True:
            if sel.get_text(elementTitle)!=vTitle:
                mclib.AppendErrorMessage(self,sel,"Wrong site title in the administrator interface.")
                print "Expected title is "+vTitle
                print "- Actual title is "+sel.get_text(elementTitle)
        else:
            mclib.AppendErrorMessage(self,sel,"Title is not visible in the Administrator interface")
    else:
        mclib.AppendErrorMessage(self,sel,"Title is not present in the Administrator interface")
    
# Check that the TAGLINE in the admin interface is present, visible and correct
    elementTagline="//div[@id='logo']/h1/span"
    if sel.is_element_present(elementTagline)==True:
        if sel.is_visible(elementTagline)==True:
            if sel.get_text(elementTagline)!=vTagLine:
                mclib.AppendErrorMessage(self,sel,"Wrong tagline in the administrator interface.")
                print "Expected tagline is "+VTagLine
                print "- Actual tagline is "+sel.get_text(elementTagline)
        else:
            mclib.AppendErrorMessage(self,sel,"Tagline is not visible in the Administrator interface")
    else:
        mclib.AppendErrorMessage(self,sel,"Tagline is not present in the Administrator interface")

# FOOTER was removed from Admin on Apr 6, 2010
# Check that the FOOTER in the admin interface is present, visible and correct
#    elementFooter="//div[@id='footer']/div[2]/p"
#    if sel.is_element_present(elementFooter)==True:
#        if sel.is_visible(elementFooter)==True:
#            if sel.get_text(elementFooter)!=vFooter:
#                self.verificationErrors.append("Wrong footer text on the administrator interface.")
#                print testvars.preE+"Wrong footer text in the administrator interface"
#                print "Expected footer text is "+vFooter
#                print "- Actual footer text is "+sel.get_text(elementFooter)
#        else:
#            self.verificationErrors.append("Footer is not viisible in the Administrator interface")
#            print "Footer is not visible in the Administrator interface"
#    else:
#        self.verificationErrors.append("Footer is not present in the Administrator interface")
#        print "Footer is not present in the Administrator interface"

    print "Checked title, tagline in administrator interface"
        
#=============CHECKS ON MAIN SITE===============
# Click View Main Site
    #sel.click(testvars.MCTestVariables["ViewMainSiteLink"])
    sel.open(testvars.MCTestVariables["TestSite"])
    sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])
# Check that the TITLE on the main site is present, visible and correct
    if theme==4:
        elementTitle="//div[@id='wrapper']/div[1]/div/div[1]/h1/a"
        elementTagline="//div[@id='wrapper']/div[1]/div/div[1]/p"
        vFooter=vTitle+' is powered by'
    else:
        elementTitle="//div[@id='logo']/h1/a/span"
        elementTagline="//div[@id='logo']/h1/span"

    if sel.is_element_present(elementTitle)==True:
        if sel.is_visible(elementTitle)==True:
            if sel.get_text(elementTitle)!=vTitle:
                mclib.AppendErrorMessage(self,sel,"Wrong site title on the main site.")
                print "Expected title is "+vTitle
                print "- Actual title is "+sel.get_text(elementTitle)
        else:
            mclib.AppendErrorMessage(self,sel,"Title is not visible on the Main site")
    else:
        mclib.AppendErrorMessage(self,sel,"Title is not present on the Main site")
        
# Check that the TAGLINE on the main site is present, visible and correct
    if sel.is_element_present(elementTagline)==True:
        if sel.is_visible(elementTagline)==True:
            if sel.get_text(elementTagline)!=vTagLine:
                mclib.AppendErrorMessage(self,sel,"Wrong tagline on the main site.")
                print "Expected tagline is "+VTagLine
                print "- Actual tagline is "+sel.get_text(elementTagline)
        else:
            mclib.AppendErrorMessage(self,sel,"Tagline is not visible on the Main site")
    else:
        mclib.AppendErrorMessage(self,sel,"Tagline is not present on the Main site")

# Check that the FOOTER on the main site is present, visible and correct
#    if theme == 4:
    elementFooter="//div[@id='footer']/div[2]/div/span"
#    else:
#        elementFooter="//div[@id='footer']/div[1]"
    if sel.is_element_present(elementFooter)==True:
        if sel.is_visible(elementFooter)==True:
            if sel.get_text(elementFooter)!=vFooter:
                mclib.AppendErrorMessage(self,sel,"Wrong footer text on the Main site.")
                print "Expected footer text is "+vFooter
                print "- Actual footer text is "+sel.get_text(elementFooter)
        else:
            mclib.AppendErrorMessage(self,sel,"Footer is not visible on the Main site")
    else:
        mclib.AppendErrorMessage(self,sel,"Footer is not present on the Main site")

    print "Checked title, tagline, footer on the front end"

#=============CHECK ABOUT PAGE===================
# Navigate to About page
    sel.open("/about")
#    if theme==4:
#        sel.click("link=About")
#    else:
#        sel.click("//ul[@id='nav']/li[7]/a/span")
    sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])
# Verify About text
    if theme==4:
        elementAbout="//div[@id='main']/div[1]/h2"
    else:
        elementAbout="//div[@id='main']/h2[1]"
# Check that elementAbout exists
    if sel.is_element_present(elementAbout)==True:
# Verify text in elementAbout
        if sel.get_text(elementAbout)!=("About " + vTitle):
            mclib.AppendErrorMessage(self,sel,"Wrong About text on About page.")
            print "Expected text is About " + vTitle
            print "- Actual text is "+sel.get_text(elementAbout)
    else:
        mclib.AppendErrorMessage(self,sel,"About element is not present on About page")
# Check that vAboutUs text is present
    if sel.is_text_present(vAboutUs)!=True:
        mclib.AppendErrorMessage(self,sel,"AboutUs text is not found on About page")
    print "Checked title, about text on About page"




# ===================================
# =  MODIFY ORGANIZATION SETTINGS   =
# ===================================
 
# This subroutine changes the organization parameters to conventional test strings
# containing a timestamp (dd-mm-yyyy hh:mm:ss)

def ModifyOrganizationSettings(self,sel,theme):
    NavigateToSettingsPage(self,sel)
    vSideBarBlurb = r'The<i style = "color: red"> Miro Guide</i>, our open content directory, '
    vSideBarBlurb = vSideBarBlurb + r'is browsed by a large and global audience of Miro users '
    vSideBarBlurb = vSideBarBlurb + r'and is also available in any web browser at miroguide.com. '
    vSideBarBlurb = vSideBarBlurb + r'Your media will be showcased with a wide variety of content, '
    vSideBarBlurb = vSideBarBlurb + r'ranging from mainstream (HBO, ABC, NBC), to professionally '
    vSideBarBlurb = vSideBarBlurb + r'produced web content ( Revision3, Next New Networks, Rocketboom), '
    vSideBarBlurb = vSideBarBlurb + r'to public broadcasting (PBS, NPR, LinkTV, Democracy Now!), to '
    vSideBarBlurb = vSideBarBlurb + r'completely independent video feeds. ' + \
time.strftime("%d-%m-%Y %H:%M:%S", time.localtime())
    vFooterBlurb = r'<i style = "color: red">Miro</i> works best when there you have got '
    vFooterBlurb = vFooterBlurb + r'an RSS feed. If that sounds confusing, do not worry, many services '
    vFooterBlurb = vFooterBlurb + r'create an RSS feed automatically (blip.tv, YouTube, Google Video, '
    vFooterBlurb = vFooterBlurb + r'and many others). Try out this web app to see if you have already '
    vFooterBlurb = vFooterBlurb + r'got one. ' + time.strftime("%d-%m-%Y %H:%M:%S", time.localtime())
    sel.type("id_sidebar_html", vSideBarBlurb)
    sel.type("id_footer_html", vFooterBlurb)
    sel.click("submit_settings")
    sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])
    print "Changed organization settings (SideBarBlurb, FooterBlurb)"
    # ------ Workaround for blank page bug
    sel.open(testvars.MCTestVariables["CategoriesPage"])
    sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])
    
# Check footbar at the administrator interface - UPDATE: FOOTER REMOVED FROM ADMIN PAGES
    elementFooterBlurb="//div[@id='footer']/div[1]"
#    if sel.is_element_present(elementFooterBlurb)==True:
#        if mclib.remove_html_tags(sel.get_text(elementFooterBlurb))!=mclib.remove_html_tags(vFooterBlurb):
#            self.verificationErrors.append("Wrong Footer blurb text on About page.")
#            print testvars.preE+"Wrong Footer blurb text in Administrator interface"
#            print "Expected text is " + mclib.remove_html_tags(vFooterBlurb)
#            print "- Actual text is "+mclib.remove_html_tags(sel.get_text(elementFooterBlurb))
#    else:
#        self.verificationErrors.append("Footer blurb is not present in Administrator interface")
#        print testvars.preE+"Footer blurb is not present in Administrator interface"
    
# Check at the Main site
    #sel.click(testvars.MCTestVariables["ViewMainSiteLink"])
    sel.open(testvars.MCTestVariables["TestSite"])
    sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])
    #SideBarBlurb is displayed only on List Theme (No.1)
    elementSideBarBlurb="about"
    if theme==1:
        if sel.is_element_present(elementSideBarBlurb)==True:
            if mclib.remove_html_tags(sel.get_text(elementSideBarBlurb))!=mclib.remove_html_tags(vSideBarBlurb):
                self.verificationErrors.append("Wrong SideBar blurb text on the Main site.")
                print testvars.preE+"Wrong SideBar blurb text the Main site"
                print "Expected text is " + mclib.remove_html_tags(vSideBarBlurb)
                print "- Actual text is "+mclib.remove_html_tags(sel.get_text(elementSideBarBlurb))
        else:
            self.verificationErrors.append("SideBar blurb is not present on the Main site")
            print testvars.preE+"SideBar blurb is not present on the Main site"

    #SideBarBlurb is displayed only on Blue Theme (No.4)
    elementFooterBlurb="//div[@id='footer']/div[1]"
    if theme==4:
        if sel.is_element_present(elementFooterBlurb)==True:
            if mclib.remove_html_tags(sel.get_text(elementFooterBlurb))!=mclib.remove_html_tags(vFooterBlurb):
                self.verificationErrors.append("Wrong Footer blurb text on the Main site.")
                print testvars.preE+"Wrong Footer blurb text the Main site"
                print "Expected text is " + mclib.remove_html_tags(vFooterBlurb)
                print "- Actual text is "+mclib.remove_html_tags(sel.get_text(elementFooterBlurb))
        else:
            self.verificationErrors.append("Footer blurb is not present on the Main site")
            print testvars.preE+"Footer blurb is not present on the Main site"
    
# Check at the About page
    sel.open("/about/")
    if theme==4:
        if sel.is_element_present(elementFooterBlurb)==True:
            if mclib.remove_html_tags(sel.get_text(elementFooterBlurb))!=mclib.remove_html_tags(vFooterBlurb):
                self.verificationErrors.append("Wrong Footer blurb text on About page.")
                print testvars.preE+"Wrong Footer blurb text on About page"
                print "Expected text is About " + mclib.remove_html_tags(vFooterBlurb)
                print "- Actual text is "+mclib.remove_html_tags(sel.get_text(elementFooterBlurb))
        else:
            self.verificationErrors.append("Footer blurb is not present on About page")
            print testvars.preE+"Footer blurb is not present on About page"


# ===================================
# =       UPLOAD SITE LOGO          =
# ===================================
 
# This subroutine uploads a new graphic file as a site logo

def UploadSiteLogo(self,sel,theme,newlogo):
    NavigateToSettingsPage(self,sel)
    logofile = os.path.join(testvars.MCTestVariables["GraphicFilesDirectory"],newlogo)
    print "Uploading logo from file: "+logofile
    if sel.is_element_present("id_logo")==True:
        sel.type("id_logo", logofile)
    else:
        mclib.AppendErrorMessage(self,sel,"Edit field for site logo file name not found")
    sel.click("submit_settings")
    sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])
    sel.open(testvars.MCTestVariables["SettingsPage"])
    sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])
    # For the purpose of checking actual site logo file name 
    # we truncate the last 4 chars from the file name because an umpteenth copy of the same
    # file uploaded to the server contains trailing underscores after the file name
    # Example: logo.jpg -> logo______.jpg
    lll = newlogo[:(len(newlogo)-4)]
    # Check that the image is displayed on admin page
    print "Checking site logo image on admin page"
    if sel.is_element_present("//div[@id='logo']/a/img")==False:
#    if sel.is_element_present("//img[@src='http://s3.mirocommunity.org.s3.amazonaws.com/dalmatia/localtv/site_logos/dalmatia1.jpg']")==False:
        mclib.AppendErrorMessage(self,sel,"Site logo on admin pages not found")
    else:
        logoAttr = sel.get_attribute("//div[@id='logo']/a/img@src")
        if logoAttr.find(lll)==-1:
            mclib.AppendErrorMessage(self,sel,"Wrong site logo image on admin pages")
            print "Expected image source:"+testvars.MCTestVariables["SiteLogoURL"]+"/"+newlogo
            print "- Actual image source:"+logoAttr
    # Go to Main Site
    print "Checking site logo image on Home page"
    #sel.click(testvars.MCTestVariables["ViewMainSiteLink"])
    sel.open(testvars.MCTestVariables["TestSite"])
    sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])
    # This image is not available in Blue Theme (No.4)
    if theme!=4:
        if sel.is_element_present("//div[@id='logo']/a/img")==False:
            mclib.AppendErrorMessage(self,sel,"Site logo on Home page not found")
        else:
            logoAttr = sel.get_attribute("//div[@id='logo']/a/img@src")
            if logoAttr.find(lll)==-1:
                mclib.AppendErrorMessage(self,sel,"Wrong site logo image on Home page")
                print "Expected image source:"+testvars.MCTestVariables["SiteLogoURL"]+"/"+newlogo
                print "- Actual image source:"+logoAttr
    # Navigate to About page
    print "Checking site logo image on About page"
    sel.open("/about")
    if sel.is_element_present("//div[@id='main']/img")==False:
        mclib.AppendErrorMessage(self,sel,"Site logo on About page not found")
    else:
        logoAttr=sel.get_attribute("//div[@id='main']/img@src")
        if logoAttr.find(lll)==-1:
            mclib.AppendErrorMessage(self,sel,"Wrong site logo image on About page")
            print "Expected image source:"+testvars.MCTestVariables["SiteLogoURL"]+"/"+newlogo
            print "- Actual image source:"+logoAttr
        
    
# ===================================
# =     UPLOAD BACKGROUND IMAGE     =
# ===================================
 
# This subroutine uploads a new graphic file as a background image

def UploadBackgroundImage(self,sel,theme,background):
    NavigateToSettingsPage(self,sel)
    bkgrfile = os.path.join(testvars.MCTestVariables["GraphicFilesDirectory"],background)
    print "Uploading a new background image... "+bkgrfile
    if sel.is_element_present("id_background")==True:
        sel.type("id_background", bkgrfile)
        sel.click("submit_settings")
        sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])
        sel.open(testvars.MCTestVariables["SettingsPage"])
        sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])
    else:
        mclib.AppendErrorMessage(self,sel,"Input field for uploading new background image not found")
    # Go to Main Site
    print "Checking background image on Home page"
    #sel.click(testvars.MCTestVariables["ViewMainSiteLink"])
    sel.open(testvars.MCTestVariables["TestSite"])
    sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])
    # Looking for a background image in HTML source
    stringSource = sel.get_html_source()
    # We truncate the last 4 chars from the file name because an umpteenth copy of the same
    # file uploaded to the server contains trailing underscores after file name
    # Example: logo.jpg -> logo______.jpg
    bbb = background[:(len(background)-4)]
    queryText = "background: url(\""+testvars.MCTestVariables["SiteBackgroundURL"]+"/"+bbb
    if stringSource.find(queryText)==-1:
        mclib.AppendErrorMessage(self,sel,"Desired background not uploaded correctly")


# ===================================
# =         DELETE BACKGROUND       =
# ===================================
 
# This subroutine deletes the background of the front pages

def DeleteBackgroundImage(self,sel):
    NavigateToSettingsPage(self,sel)
    print "Deleting background..."
    if sel.is_element_present("delete_background")==False:
        mclib.AppendErrorMessage(self,sel,"Delete Background button not found")
    else:
        sel.click("delete_background")
        sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])
        sel.open(testvars.MCTestVariables["CategoriesPage"])
        time.sleep(2)
        sel.open(testvars.MCTestVariables["SettingsPage"])
        sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])
        sel.click("submit_settings")
        sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])
        # Go to Main Site
        sel.open(testvars.MCTestVariables["CategoriesPage"])
        sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])
        print "Checking that Home page does not have a background image"
        #sel.click(testvars.MCTestVariables["ViewMainSiteLink"])
        sel.open(testvars.MCTestVariables["TestSite"])
        sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])
        # Looking for a background image in HTML source
        stringSource = sel.get_html_source()
        queryText = "background: url(\""+testvars.MCTestVariables["SiteBackgroundURL"]
        if stringSource.find(queryText)==-1:
            print "Background image was successfully deleted"
        else:
            mclib.AppendErrorMessage(self,sel,"Background image was not deleted")
        


# ===================================
# =           ADD CUSTOM CSS        =
# ===================================
 
# This subroutine adds custom CSS to the site settings and verifies
# that the CSS applies correctly

def AddCustomCSS(self,sel,customcss):
    NavigateToSettingsPage(self,sel)
    print "Adding custom CSS..."
    if sel.is_element_present("id_css")==False:
        mclib.AppendErrorMessage(self,sel,"Custom CSS edit field not found")
    else:
        sel.type("id_css",customcss)
        sel.click("submit_settings")
        sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])
        sel.open(testvars.MCTestVariables["SettingsPage"])
        sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])
        # Looking for custom CSS in HTML source - admin
        #sel.click(testvars.MCUI["AdminVideos"])
        sel.open(testvars.MCTestVariables["ReviewQueuePage"])
        sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])
        print "Checking that admin page does not have custom CSS"
        stringSource = sel.get_html_source()
        if stringSource.find(customcss)==-1:
            print "Custom CSS did not add to admin pages - PASS"
        else:
            mclib.AppendErrorMessage(self,sel,"Custom CSS was added to admin pages")
        # Go to Main Site
        #sel.click(testvars.MCTestVariables["ViewMainSiteLink"])
        sel.open(testvars.MCTestVariables["TestSite"])
        sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])
        # Looking for custom CSS in HTML source - front pages
        print "Checking that Home page has custom CSS"
        stringSource = sel.get_html_source()
        if stringSource.find(customcss)!=-1:
            print "Custom CSS was successfully added to front pages"
        else:
            mclib.AppendErrorMessage(self,sel,"Custom CSS was not added to front pages")



# ===================================
# =        DELETE CUSTOM CSS        =
# ===================================
 
# This subroutine clears custom CSS from the site settings and verifies
# that the CSS is removed correctly

def DeleteCustomCSS(self,sel):
    NavigateToSettingsPage(self,sel)
    print "Deleting custom CSS..."
    if sel.is_element_present("id_css")==False:
        mclib.AppendErrorMessage(self,sel,"Custom CSS edit field not found")
    else:
        sel.type("id_css","")
        sel.click("submit_settings")
        sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])
        sel.open(testvars.MCTestVariables["SettingsPage"])
        sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])
        # Looking for custom CSS in HTML source - admin
#        sel.click(testvars.MCUI["AdminVideos"])
        sel.open(testvars.MCTestVariables["ReviewQueuePage"])
        sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])
        # Go to Main Site
        #sel.click(testvars.MCTestVariables["ViewMainSiteLink"])
        sel.open(testvars.MCTestVariables["TestSite"])
        sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])
        # Looking for custom CSS in HTML source - front pages
        print "Checking that Home page does not have custom CSS"
        styleTag = "<style type=\"text/css\">"
        stringSource = sel.get_html_source()
        if stringSource.find(styleTag)==-1:
            print "Custom CSS was successfully removed from front pages"
        else:
            mclib.AppendErrorMessage(self,sel,"Custom CSS was not removed from front pages")


# ===================================
# =    DISPLAY SUBMIT VIDEO NAV     =
# ===================================
 
# This subroutine makes Submit a Video nav button displayed
# on the front page

def DisplaySubmitVideo(self,sel,theme):
    NavigateToSettingsPage(self,sel)
    print "Checking Display 'Submit a Video' check box..."
    if sel.is_element_present("id_display_submit_button")==False:
        mclib.AppendErrorMessage(self,sel,"Display 'Submit a Video' button check box not found")
    else:
        sel.check("id_display_submit_button")
        sel.click("submit_settings")
        sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])
        sel.open(testvars.MCTestVariables["SettingsPage"])
        sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])
        # Go to Main Site
        #sel.click(testvars.MCTestVariables["ViewMainSiteLink"])
        sel.open(testvars.MCTestVariables["TestSite"])
        sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])
        # Looking for Submit a Video button on the front pages
        if theme==4:
            submitButton="link=Submit"           #"//div[@id='nav']/ul/li[6]/a"
            submitCaption="Submit"
        else:
            submitButton="//ul[@id='nav']/li[6]/a/span"
            submitCaption="Submit A Video"
        if sel.is_element_present(submitButton)==False or sel.get_text(submitButton)!=submitCaption:
            mclib.AppendErrorMessage(self,sel,"Submit a Video button was not found on the front pages")
        else:
            print "Submit a Video button successfully found on front pages"



# ===================================
# =      HIDE SUBMIT VIDEO NAV      =
# ===================================
 
# This subroutine hides Submit a Video nav button 
# on the front page

def HideSubmitVideo(self,sel,theme):
    NavigateToSettingsPage(self,sel)
    print "Unchecking Display 'Submit a Video' check box..."
    if sel.is_element_present("id_display_submit_button")==False:
        mclib.AppendErrorMessage(self,sel,"Display 'Submit a Video' button check box not found")
    else:
        sel.uncheck("id_display_submit_button")
        sel.click("submit_settings")
        sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])
        sel.open(testvars.MCTestVariables["SettingsPage"])
        sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])
        # Go to Main Site
        #sel.click(testvars.MCTestVariables["ViewMainSiteLink"])
        sel.open(testvars.MCTestVariables["TestSite"])
        sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])
        # Looking for Submit a Video button on the front pages
        if theme==4:
            submitButton="link=Submit"           #"//div[@id='nav']/ul/li[6]/a"
            submitCaption="Submit"
        else:
            submitButton="//ul[@id='nav']/li[6]/a/span"
            submitCaption="Submit A Video"
        if sel.is_element_present(submitButton)==True and sel.get_text(submitButton)==submitCaption:
            mclib.AppendErrorMessage(self,sel,"Submit a Video button was unexpectedly found on the front pages")
        else:
            print "Submit a Video button not found on front pages - PASS"



# =======================================
# = CHECK REQUIRE LOGIN TO SUBMIT VIDEO =
# =======================================
 
# This subroutine checks Require Users to Login to Submit a Video check box
# and verifies that Submit a Video check box on the front page is displayed 
# only to logged users

def CheckRequireLoginToSubmitVideo(self,sel,theme):
    NavigateToSettingsPage(self,sel)
    print "Checking 'Require Users to Login to Submit a Video' check box..."
    if sel.is_element_present("id_display_submit_button")==False:
        mclib.AppendErrorMessage(self,sel,"Display 'Submit a Video' button check box not found")
    else:
        if sel.is_element_present("id_submission_requires_login")==False:
            mclib.AppendErrorMessage(self,sel,"'Require Users to Login to Submit a Video' check box not found")
        else:
            sel.check("id_display_submit_button")
            sel.check("id_submission_requires_login")
            sel.click("submit_settings")
            sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])
            sel.open(testvars.MCTestVariables["SettingsPage"])
            sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])
            # Go to Main Site
            #sel.click(testvars.MCTestVariables["ViewMainSiteLink"])
            sel.open(testvars.MCTestVariables["TestSite"])
            sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])
            print "Logged as Admin - navigating to Home page"
            # Looking for Submit a Video button on the front pages - logged as Admin
            if theme==4:
                submitButton="link=Submit"        
                submitCaption="Submit"
            else:
                submitButton="//ul[@id='nav']/li[6]/a/span"
                submitCaption="Submit A Video"
            print "Logged as Admin: Checking Submit a Video button..."
            if sel.is_element_present(submitButton)==False or sel.get_text(submitButton)!=submitCaption:
                mclib.AppendErrorMessage(self,sel,"Logged as Admin: Submit a Video button was not found on the front pages")
            else:
                sel.click(submitButton)
                time.sleep(2)
                if sel.is_element_present("submit_video")==False:
                    mclib.AppendErrorMessage(self,sel,"Logged as Admin: Submit Video Pop-up did not appear")
                else:
                    #sel.click("//div[@id='submit_video']/div[1]")
                    sel.key_press("submit_video","\\27")           # Press Escape
                    print "OK"
            # Log out
            print "Logging out..."
            loginlogout.LogOut(self,sel)
            print "OK"
            print "Logged out: Checking Submit a Video button..."
            # Looking for Submit a Video button on the front pages - logged out
            if sel.is_element_present(submitButton)==False or sel.get_text(submitButton)!=submitCaption:
                mclib.AppendErrorMessage(self,sel,"Logged out: Submit a Video button was not found on the front pages")
            else:
                sel.click(submitButton)
                time.sleep(2)
                if sel.is_element_present("overlay")==False:
                    mclib.AppendErrorMessage(self,sel,"Logged out: Login Pop-up did not appear")
                else:
                    #sel.click("//div[@id='overlay']/div[1]")
                    sel.key_press("overlay","\\27")
                    print "OK"
            # Log in as user
            print "Logging in as User..."
            loginlogout.LogInAsUser(self,sel)
            print "OK"
            print "Logged as User: Checking Submit a Video button..."
            # Looking for Submit a Video button on the front pages - logged as User
            if sel.is_element_present(submitButton)==False or sel.get_text(submitButton)!=submitCaption:
                mclib.AppendErrorMessage(self,sel,"Logged as User: Submit a Video button was not found on the front pages")
            else:
                sel.click(submitButton)
                time.sleep(2)
                if sel.is_element_present("submit_video")==False:
                    mclib.AppendErrorMessage(self,sel,"Logged as User: Submit Video Pop-up did not appear")
                else:
                    #sel.click("//div[@id='submit_video']/div[1]")
                    sel.key_press("submit_video","\\27")
                    print "OK"



# =========================================
# = UNCHECK REQUIRE LOGIN TO SUBMIT VIDEO =
# =========================================
 
# This subroutine unchecks Require Users to Login to Submit a Video check box

def UncheckRequireLoginToSubmitVideo(self,sel):
    NavigateToSettingsPage(self,sel)
    print "Unchecking 'Require Users to Login to Submit a Video' check box..."
    if sel.is_element_present("id_display_submit_button")==False:
        mclib.AppendErrorMessage(self,sel,"Display 'Submit a Video' button check box not found")
    else:
        if sel.is_element_present("id_submission_requires_login")==False:
            mclib.AppendErrorMessage(self,sel,"'Require Users to Login to Submit a Video' check box not found")
        else:
            sel.check("id_display_submit_button")
            sel.uncheck("id_submission_requires_login")
            sel.click("submit_settings")
            print "Done"
            sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])
            sel.open(testvars.MCTestVariables["SettingsPage"])
            sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])



# =========================================
# =        CHECK USE ORIGINAL DATE        =
# =========================================
 
# This subroutine checks Use Original Date check box

def CheckUseOriginalDate(self,sel):
    NavigateToSettingsPage(self,sel)
    print "Checking 'Use Original Date' check box..."
    if sel.is_element_present("css=input#id_use_original_date")==False:
        mclib.AppendErrorMessage(self,sel,"'Use Original Date' check box not found")
    else:
        sel.check("css=input#id_use_original_date")
        sel.click("submit_settings")
        print "Done"
        sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])
        sel.open(testvars.MCTestVariables["SettingsPage"])
        sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])




# =========================================
# =              ENABLE PLAYLISTS         =
# =========================================
 
# This subroutine enables or disables playlists
# <option> can take values "Yes", "No", or "Admins Only"

def EnablePlaylists(self,sel,option):
    if option!='Yes' and option!='No' and option!='Admins Only':
        mclib.AppendErrorMessage(self,sel,"Wrong parameter passed to EnablePlaylists subroutine")
    else:
        NavigateToSettingsPage(self,sel)
        print "Selecting '"+option+"' from 'Enable Playlists?' drop-down list..."
        if sel.is_element_present("id_playlists_enabled")==False:
            mclib.AppendErrorMessage(self,sel,"'Enable Playlists?' drop-down list not found")
        else:
            sel.select("css=select#id_playlists_enabled","label="+option)
            sel.click("submit_settings")
            print "Done"
            sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])
            sel.open(testvars.MCTestVariables["SettingsPage"])
            sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])




