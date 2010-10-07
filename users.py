# Module USERS.PY
# includes:
#   * function UserRow(self,sel,username) - returns the row number for the desired username
#              on /users page, zero if the user not found
#   * function UserRowInCompleteListOfAuthors(self,sel,username) - returns the row number for
#              the desired username on /users/?show=all page, zero if the user not found
#   * subroutine DeleteUser(self,sel,username,allusers) - deletes user <username> from the list of
#                "human" users, if allusers==0, or from the complete list of users/authors, if
#                allusers==1
#   * subroutine FillAddUserPopUp(self,sel,username,email,role,password) - opens Add a User pop-up
#                and fills out all the fields with appropriate values
#   * subroutine AddUser(self,sel,username,email,role,password) - adds a user with <username>
#                and password <password>. Role can take values 1 for Admin or 0 for User
#   * subroutine EditUser(self,sel,username,newusername,name,email,role,location,website,description,logo,password) -
#                modifies the user profile, inserting new values for all the fields
#   * subroutine EditUserProfile(self,sel,name,username,email,location,website,description)
#   * subroutine ViewProfile(self,sel)
#   * subroutine ViewUser(self,sel,username,name,location,website,description,image)
#   * subroutine ViewUserCheck(self,sel,theme,username,name,location,website,description,image)



from selenium import selenium

import unittest, time, re, os
import testvars, mclib, sitesettings

# =======================================
# =      FIND USER IN THE LIST          =
# =======================================

# This function returns the row number for the desired username
# on /users page.
# Returns row number if the username is found and 0 otherwise.

def UserRow(self,sel,username):
    us=username
    sel.open(testvars.MCTestVariables["UserPage"])
    sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])
    username=""    
    no=1
    usernameTableCell="//div[@id='labels']/form/table/tbody/tr[1]/td[2]"
    while sel.is_element_present(usernameTableCell):
        username_untrimmed = sel.get_text(usernameTableCell)
        username = username_untrimmed.replace(' Edit | Delete | View','')
        if username==us:
            break
        no=no+1
        usernameTableCell="//div[@id='labels']/form/table/tbody/tr["+str(no)+"]/td[2]"
    if username==us:
        return no
    else:
        return 0


# ==================================================
# = FIND USER/AUTHOR IN THE COMPLETE LIST OF USERS =
# ==================================================

# This function returns the row number for the desired username
# on /users/?show=all page.
# Returns row number if the username is found and 0 otherwise.

def UserRowInCompleteListOfAuthors(self,sel,username):
    us=username
    sel.set_timeout(150000)
    sel.open(testvars.MCTestVariables["UserPage"]+"?show=all")
    sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])
    username=""    
    no=1
    usernameTableCell="//div[@id='labels']/form/table/tbody/tr[1]/td[2]"
    while sel.is_element_present(usernameTableCell):
        username_untrimmed = sel.get_text(usernameTableCell)
        username = username_untrimmed.replace(' Edit | Delete | View','')
        if username==us:
            break
        no=no+1
        usernameTableCell="//div[@id='labels']/form/table/tbody/tr["+str(no)+"]/td[2]"
    if username==us:
        return no
    else:
        return 0
    
# =======================================
# =             DELETE USER             =
# =======================================

def DeleteUser(self,sel,username,allusers):
    if allusers==0:    usRow = UserRow(self,sel,username)
    elif allusers==1:    usRow = UserRowInCompleteListOfAuthors(self,sel,username)
    else:    self.fail("Wrong value of ALLUSERS parameter passed to function DeleteUser")
    if usRow==0:
        mclib.AppendErrorMessage(self,sel,"Username "+username+" not found. Cannot delete it.")
    else:
        if allusers==0:    sel.open(testvars.MCTestVariables["UserPage"])
        else:    sel.open(testvars.MCTestVariables["UserPage"]+"/?show=all")
        elementDelete = "//div[@id='labels']/form/table/tbody/tr["+str(usRow)+"]/td[2]/div/a[2]"
        if sel.is_element_present(elementDelete)==False:
            mclib.AppendErrorMessage(self,sel,"Delete link not found for username "+username)
        else:
            print "Deleting user "+username+"..."
            sel.click(elementDelete)
            sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])
            print "Checking that the user was deleted..."
            if (allusers==0 and UserRow(self,sel,username))==0:
                print "OK"
            elif (allusers==1 and UserRowInCompleteListOfAuthors(self,sel,username))==0:
                print "OK"
            else:
                print mclib.AppendErrorMessage(self,sel,"Could not delete username "+username)


# =======================================
# =        FILL ADD USER POP-UP         =
# =======================================

def FillAddUserPopUp(self,sel,username,email,role,password):
    print "Adding a new username "+username
    sel.open(testvars.MCTestVariables["UserPage"])
    buttonAddUser = "//div[@id='label_sidebar']/a/span"
    if sel.is_element_present(buttonAddUser)==True:           
        sel.click(buttonAddUser)
        time.sleep(2)
        if sel.is_visible("//div[@id='label_sidebar']")==False:
            mclib.AppendErrorMessage(self,sel,"Add user pop-up does not display")
        else:
            # Enter username
            if sel.is_element_present("id_username")==True:
                sel.click("id_username")
                sel.type("id_username",username)
            else:
                mclib.AppendErrorMessage(self,sel,"Edit field for user's username not found")
            # Enter user's email address
            if sel.is_element_present("id_email")==True:
                sel.click("id_email")
                sel.type("id_email",email)
            else:
                mclib.AppendErrorMessage(self,sel,"Edit field for user's email not found")
            # Enter user's role
            if sel.is_element_present("id_role_0")==True:
                if role=="":
                    sel.click("id_role_0")
                else:
                    sel.click("id_role_"+role)
            else:
                mclib.AppendErrorMessage(self,sel,"Radio buttons for user's role not found")
            # Enter user's password
            if sel.is_element_present("id_password_f")==True:
                sel.click("id_password_f")
                sel.type("id_password_f",password)
            else:
                mclib.AppendErrorMessage(self,sel,"Edit field for user's password not found")
            # Enter user's password confirmation
            if sel.is_element_present("id_password_f2")==True:
                sel.click("id_password_f2")
                sel.type("id_password_f2",password)
            else:
                mclib.AppendErrorMessage(self,sel,"Edit field for user's password confirmation not found")
            # Save changes
            buttonSubmit = "submit"
            if sel.is_element_present(buttonSubmit)==True:
                sel.click("submit")
            else:
                mclib.AppendErrorMessage(self,sel,"Save button on Add User pop-up not found")
#            sel.refresh()
            sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])


# =======================================
# =             ADD USER                =
# =======================================

def AddUser(self,sel,username,email,role,password):
    #Check if the username already exists
    if UserRow(self,sel,username)!=0:
        print "User already exists. Skipping add user procedure"
        return 0
    else:
        FillAddUserPopUp(self,sel,username,email,role,password)
        # Check if the new user is present in the list
        rowNo = UserRow(self,sel,username)
        if rowNo==0:   # not found
            mclib.AppendErrorMessage(self,sel,username+"user was not added to the list")
        else:
            print "User was successfully added to the list"

                    
# =======================================
# =             EDIT USER               =
# =======================================

def EditUser(self,sel,username,newusername,name,email,role,location,website,description,logo,password):
    usRow = UserRow(self,sel,username)
    if usRow!=0:
        sel.open(testvars.MCTestVariables["UserPage"])
        elementEdit = "//div[@id='labels']/form/table/tbody/tr["+str(usRow)+"]/td[2]/div/a[1]"
        basicLink = "id_form-"+str(usRow-1)
        if sel.is_element_present(elementEdit):
            sel.click(elementEdit)
            print "Editing profile for user "+username
            # Enter username
            if newusername!="":
                if sel.is_element_present(basicLink+"-username")==True:
                    sel.click(basicLink+"-username")
                    sel.type(basicLink+"-username",newusername)
                else:
                    mclib.AppendErrorMessage(self,sel,"Edit field for USERNAME not found")
            # Enter name
            if name!="":
                if sel.is_element_present(basicLink+"-name")==True:
                    sel.click(basicLink+"-name")
                    sel.type(basicLink+"-name",name)
                else:
                    mclib.AppendErrorMessage(self,sel,"Edit field for NAME not found")
            # Enter user's email address
            if email!="":
                if sel.is_element_present(basicLink+"-email")==True:
                    sel.click(basicLink+"-email")
                    sel.type(basicLink+"-email",email)
                else:
                    mclib.AppendErrorMessage(self,sel,"Edit field for EMAIL not found")
            # Enter user's role
            if sel.is_element_present(basicLink+"-role_0")==True:
                sel.click(basicLink+"-role_"+role)
            else:
                mclib.AppendErrorMessage(self,sel,"Edit field for ROLE not found")
            # Enter user's location
            if location!="":
                if sel.is_element_present(basicLink+"-location")==True:
                    sel.click(basicLink+"-location")
                    sel.type(basicLink+"-location",location)
                else:
                    mclib.AppendErrorMessage(self,sel,"Edit field for LOCATION not found")
            # Enter user's website
            if website!="":
                if sel.is_element_present(basicLink+"-website")==True:
                    sel.click(basicLink+"-website")
                    sel.type(basicLink+"-website",website)
                else:
                    mclib.AppendErrorMessage(self,sel,"Edit field for WEBSITE not found")
            # Enter user's description
            if description!="":
                if sel.is_element_present(basicLink+"-description")==True:
                    sel.click(basicLink+"-description")
                    sel.type(basicLink+"-description",description)
                else:
                    mclib.AppendErrorMessage(self,sel,"Edit field for DESCRIPTION not found")
            # Upload user's logo image
            if logo!="":
                if sel.is_element_present(basicLink+"-logo")==True:
                    sel.click(basicLink+"-logo")
                    sel.type(basicLink+"-logo",os.path.join(testvars.MCTestVariables["GraphicFilesDirectory"],logo))
                else:
                    mclib.AppendErrorMessage(self,sel,"Input field for user LOGO not found")
            # Enter user's password
            if sel.is_element_present(basicLink+"-password_f")==True:
                sel.click(basicLink+"-password_f")
                sel.type(basicLink+"-password_f",password)
            else:
                mclib.AppendErrorMessage(self,sel,"Edit field for PASSWORD not found")
                # Enter user's password confirm
            if sel.is_element_present(basicLink+"-password_f2")==True:
                sel.click(basicLink+"-password_f2")
                sel.type(basicLink+"-password_f2",password)
            else:
                mclib.AppendErrorMessage(self,sel,"Edit field for CONFIRMATION PASSWORD not found")
            # Save changes
            buttonSubmit = testvars.MCTestVariables["SaveChanges"]
            if sel.is_element_present(buttonSubmit)==False:
                mclib.AppendErrorMessage(self,sel,"Save button on Add User pop-up not found")
            else:
                sel.click(buttonSubmit)
                sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])
                # Checking that the user profile was updated correctly
                if newusername!="":
                    usRow = UserRow(self,sel,newusername)
                else:
                    usRow = UserRow(self,sel,username)
                if usRow==0:
                    mclib.AppendErrorMessage(self,sel,"Updated user profile not found in the list of users.")
                else:
                    # Check the values for particular fields
                    if email!="":
                        print "Checking user's email in the list of users..."
                        newEmail = sel.get_text("//div[@id='labels']/form/table/tbody/tr["+str(usRow)+"]/td[3]")
                        if newEmail==email:
                            print newEmail+" - OK"
                        else:
                            mclib.AppendErrorMessage(self,sel,"The email found for this user did not match the expected value")
                            print "Expected email: "+email
                            print "- Actual email: "+newEmail
                    print "Checking user's role in the list of users..."
                    newRole = str(sel.get_text("//div[@id='labels']/form/table/tbody/tr["+str(usRow)+"]/td[4]"))
                    if (role=='0' and newRole=="User") or (role=='1' and newRole=="Admin"):
                        print newRole+" - OK"
                    else:
                        mclib.AppendErrorMessage(self,sel,"The role displayed for the user did not match the assigned role")
                        if role==1: print "Expected role: Admin"
                        else: print "Expected role: User"
                        print "- Actual role: "+newRole
                    # View the updated user's page and check the new values for account parameters
                    if newusername!="":
                        ViewUser(self,sel,newusername,name,location,website,description,logo)
                    else:
                        ViewUser(self,sel,username,name,location,website,description,logo)                        
        else:
            mclib.AppendErrorMessage(self,sel,"Edit link not found for user "+username)
    else:
        mclib.AppendErrorMessage(self,sel,"Could not find username "+username)


# =======================================
# =         EDIT USER PROFILE           =
# =======================================
def EditUserProfile(self,sel,name,username,email,location,website,photo,description):
    #Check if the edit profile page can be opened
    sel.open(testvars.MCTestVariables["TestSite"])
    buttonEditProfile = "link=Your Profile"
    print "Opening user profile page..."
    if sel.is_element_present(buttonEditProfile)==False:
        mclib.AppendErrorMessage(self,sel,"'Your Profile' link on home page is missing")
    else:
        sel.click(buttonEditProfile)
        sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])
        print "OK"
        # Enter name
        if name!="":
            print "Updating user name: "+name
            if sel.is_element_present("id_name")==False:
                mclib.AppendErrorMessage(self,sel,"Edit field for user's NAME not found")
            else:
                sel.click("id_name")
                sel.type("id_name",name)
        # Enter username
        if username!="":
            print "Updating username: "+username
            if sel.is_element_present("id_username")==False:
                mclib.AppendErrorMessage(self,sel,"Edit field for user's USERNAME not found")
            else:
                sel.click("id_username")
                sel.type("id_username",username)
        # Enter user's email address
        if email!="":
            print "Updating user email: "+email
            if sel.is_element_present("id_email")==False:
                mclib.AppendErrorMessage(self,sel,"Edit field for user's EMAIL not found")
            else:
                sel.click("id_email")
                sel.type("id_email",email)
        # Enter user's location
        if location!="":
            print "Updating user location: "+location
            if sel.is_element_present("id_location")==False:
                mclib.AppendErrorMessage(self,sel,"Edit field for user's LOCATION not found")
            else:
                sel.click("id_location")
                sel.type("id_location",location)
        # Enter user's website
        if website!="":
            print "Updating user website: "+website
            if sel.is_element_present("id_website")==False:
                mclib.AppendErrorMessage(self,sel,"Edit field for user's WEBSITE not found")
            else:
                sel.click("id_website")
                sel.type("id_website",website)
        # Upload user's photo
        if photo!="":
            print "Uploading user's photo..."
            if sel.is_element_present("id_logo")==False:
                mclib.AppendErrorMessage(self,sel,"Edit field for user's PHOTO FILE not found")
            else:
                sel.click("id_logo")
                sel.type("id_logo",photo)
        # Enter user's description
        if description!="":
            print "Updating user description: "+description
            if sel.is_element_present("id_description")==False:
                mclib.AppendErrorMessage(self,sel,"Edit field for user's DESCRIPTION not found")
            else:
                sel.click("id_description")
                sel.type("id_description",description)
        # Save changes
        buttonSave = "submit_settings"
        if sel.is_element_present(buttonSave)==False:
            mclib.AppendErrorMessage(self,sel,"Save Changes button on Edit Profile page not found")
        else:
            sel.click(buttonSave)
            sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])
            sel.click("//div[@id='content']/form/div/a/span")
            sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])

    
# =======================================
# =             VIEW Profile            =
# =======================================

def ViewProfile(self,sel):  
    sel.open(testvars.MCTestVariables["ProfilePage"])
    sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])
    # Check if the user profile edit fields edited
    buttonViewProfile = "//div[@id='content']/form/div/a/span"
    if sel.is_element_present(buttonViewProfile)==True:
        sel.click(buttonViewProfile)
        sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])
    else:
        mclib.AppendErrorMessage(self,sel,"'View Profile' button not found")

        
# =======================================
# =             VIEW USER               =
# =======================================

def ViewUser(self,sel,username,name,location,website,description,image):
    # Detect current theme
    sel.click(testvars.MCTestVariables["ViewMainSiteLink"])
    sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])
    theme = sitesettings.ThemeScanner(self,sel)
    # Return back to /admin/users page and attempt to view the user's page
    sel.open(testvars.MCTestVariables["UserPage"])
    sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])
    usRow = UserRow(self,sel,username)
    if usRow!=0:
        #sel.open(testvars.MCTestVariables["UserPage"])
        elementView = "//div[@id='labels']/form/table/tbody/tr["+str(usRow)+"]/td[2]/div/a[3]"
        if sel.is_element_present(elementView)==False:
            mclib.AppendErrorMessage(self,sel,"View link not found for user "+username)
        else:
            print "Opening page for user "+username+" for viewing"
            sel.click(elementView)
            sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])
            # Check that username and proper name are correct
            ViewUserCheck(self,sel,theme,username,name,location,website,description,image)
    else:
        mclib.AppendErrorMessage(self,sel,"Could not find user "+username)

        
# =======================================
# =             VIEW USER CHECK         =
# =======================================
#
# <image> should be a file name without a path

def ViewUserCheck(self,sel,theme,username,name,location,website,description,image):
#    print "***********DEBUG: theme "+str(theme)
    # Check username
    print "Checking username and proper name..."
    if theme == 4:
        elementName="//div[@id='category_sidebar']/h1"
    else:
        elementName="//div[@id='author_info']/h1"
    if sel.is_element_present(elementName)==False:
        mclib.AppendErrorMessage(self,sel,"Username not found")
    else:
        currentProfile = sel.get_text(elementName)
        if currentProfile==name+" ("+username+")":
            print currentProfile+" - OK"
        else:
            mclib.AppendErrorMessage(self,sel,"Unexpected user name in the user profile")
            print "Expected name: "+name+" ("+username+")"
            print "- Actual name: "+currentProfile
    # Check location
    if location!="":
        print "Checking location..."
        elementLocation="//div[@id='location']"
        if sel.is_element_present(elementLocation)==False:
            mclib.AppendErrorMessage(self,sel,"Location not found")
        else:
            currentProfile = sel.get_text(elementLocation)
            if currentProfile==location:
                print currentProfile+" - OK"
            else:
                mclib.AppendErrorMessage(self,sel,"Unexpected location found")
                print "Expected location: "+location
                print "- Actual location: "+currentProfile
    # Check website
    if website!="":
        print "Checking website URL..."
        if theme == 4:
            elementWebsite="//div[@id='link']/a"
        else:
            elementWebsite="//div[@id='link']/a"
        if sel.is_element_present(elementWebsite)==False:
            mclib.AppendErrorMessage(self,sel,"Website URL not found")
        else:
            currentProfile = sel.get_text(elementWebsite)
            if currentProfile==website:
                print currentProfile+" - OK"
            else:
                mclib.AppendErrorMessage(self,sel,"Unexpected website URL found")
                print "Expected website URL: "+website
                print "- Actual website URL: "+currentProfile
    # Check profile description
    if description!="":
        print "Checking user profile description..."
        if theme == 4:
            elementDescription="//div[@id='category_sidebar']/div[3]"
        else:
            elementDescription="//div[@id='author_info']/div[3]"
        if sel.is_element_present(elementDescription)==False:
            mclib.AppendErrorMessage(self,sel,"User profile description not found")
        else:    
            currentProfile = sel.get_text(elementDescription)
            if currentProfile==description:
                print currentProfile+" - OK"
            else:
                mclib.AppendErrorMessage(self,sel,"Unexpected user profile description found")
                print "Expected description: "+description
                print "- Actual description: "+currentProfile
    # Check profile image
    if image!="":
        print "Checking the image in the user profile..."
        if theme == 4:
            elementImage="//div[@id='category_sidebar']/img"
        else:
            elementImage="//div[@id='author_info']/img"
        if sel.is_element_present(elementImage)==False:
            mclib.AppendErrorMessage(self,sel,"The image in the user profile not found")
        else:    
            currentProfile = sel.get_attribute(elementImage+"@src")
            # We truncate the last 4 chars from the file name because an umpteenth copy of the same
            # file uploaded to the server contains trailing underscores after file name
            # Example: logo.jpg -> logo______.jpg
            imageTruncated = image[:(len(image)-4)]
            if currentProfile.find(imageTruncated)!=-1:
                print currentProfile+" - OK"
            else:
                mclib.AppendErrorMessage(self,sel,"Unexpected image found in the user profile")
                print "Expected image: "+imageTruncated
                print "- Actual image: "+currentProfile
