from selenium import selenium

import unittest, time, re
import testvars, mclib      

# =======================================
# =      FIND USER IN THE LIST          =
# =======================================

# This function returns the row number for the desired username
# on /users page.
# Returns row number if the us username is found and 0 otherwise.

def UserRow(self,sel,username):
    us=username
    sel.open(testvars.MCTestVariables["UserPage"])
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
def DeleteUser(self,sel,username):
    usRow = UserRow(self,sel,username)
    if usRow!=0:
        sel.open(testvars.MCTestVariables["UserPage"])
        elementDelete = "//div[@id='labels']/form/table/tbody/tr["+str(usRow)+"]/td[2]/div/a[2]"
        if sel.is_element_present(elementDelete):
            sel.click(elementDelete)
        else:
            self.verificationErrors.append("Delete link not found for username")
            print testvars.preE+"Delete link not found for username "+username
            time.sleep(2)
        if UserRow(self, sel, username)==0:
            print testvars.preE+"Could not delete username "+username
    else:
        print testvars.preE+"Could not find username "+username

# =======================================
# =             ADD USER                =
# =======================================
def AddUser(self,sel,username,email,role,password):
    #Check if the username already exists
    if UserRow(self,sel,username)!=0:
        print "user already exists. Skipping add user procedure"
        return 0
    else:
        print "Adding a new username "+username
        sel.open(testvars.MCTestVariables["UserPage"])
        buttonAddUser = "//div[@id='label_sidebar']/a/span"
        if sel.is_element_present(buttonAddUser)==True:           
            sel.click(buttonAddUser)
            time.sleep(2)
            if sel.is_visible("//div[@id='label_sidebar']")==False:
                self.verificationErrors.append("Add user pop-up does not display")
                print testvars.preE+"Add user pop-up does not display"
            else:
                # Enter username
                if sel.is_element_present("id_username")==True:
                    sel.click("id_username")
                    #sel.type_keys("id_username", us)
                    sel.type("id_username",username)
                else:
                    self.verificationErrors.append("Edit field for user's username not found")
                    print testvars.preE+"Edit field for user's username not found"
                    # Enter user's email address
                if sel.is_element_present("id_email")==True:
                    sel.click("id_email")
                    #sel.type_keys("id_email", email)
                    sel.type("id_email",email)
                else:
                    self.verificationErrors.append("Edit field for user's email not found")
                    print testvars.preE+"Edit field for user's email not found"
                    # Enter user's role
                if sel.is_element_present("id_role_0")==True:
                    if role=="":
                        sel.click("id_role_0")
                    else:
                        sel.click("id_role_"+role)
                else:
                    self.verificationErrors.append("Edit field for user's role not found")
                    print testvars.preE+"Edit field for user's role not found"
                    # Enter user's password
                if sel.is_element_present("id_password_f")==True:
                    sel.click("id_password_f")
                    #sel.type_keys("id_password_f", password)
                    sel.type("id_password_f",password)
                else:
                    self.verificationErrors.append("Edit field for user's passwordf not found")
                    print testvars.preE+"Edit field for user's passwordf not found"
                    # Enter user's password confirm
                if sel.is_element_present("id_password_f2")==True:
                    sel.click("id_password_f2")
                    #sel.type_keys("id_password_f2", password)
                    sel.type("id_password_f2",password)
                else:
                    self.verificationErrors.append("Edit field for user's passwordf2 not found")
                    print testvars.preE+"Edit field for user's passwordf2 not found"
                    # Save changes
                buttonSubmit = "submit"
                if sel.is_element_present(buttonSubmit)==True:
                    sel.click("submit")
                else:
                    self.verificationErrors.append("Save button on Add User pop-up not found")
                    print testvars.preE+"Save button on Add User pop-up not found"
        sel.refresh()
        sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])
        # Check if the new user is present in the list
        rowNo = UserRow(self,sel,username)
        if rowNo==0:   # not found
            print testvars.preE+username+"user was not added to the list"
        else:
            print "User added to the list"
# =======================================
# =             EDIT USER               =
# =======================================
def EditUser(self,sel,username,name,email,role,location,website,description,password):
    usRow = UserRow(self,sel,username)
    if usRow!=0:
        sel.open(testvars.MCTestVariables["UserPage"])
        elementEdit = "//div[@id='labels']/form/table/tbody/tr["+str(usRow)+"]/td[2]/div/a[1]"
        if sel.is_element_present(elementEdit):
            sel.click(elementEdit)
            print "Start to edit field"
            # Enter username
            if sel.is_element_present("id_form-1-username")==True:
                sel.click("id_form-1-username")
                #sel.type_keys("id_form-1-username", username)
                sel.type("id_form-1-username",username)
            else:
                self.verificationErrors.append("Edit field for user's username not found")
                print testvars.preE+"Edit field for user's username not found"
            # Enter name
            if sel.is_element_present("id_form-1-name")==True:
                sel.click("id_form-1-name")
                #sel.type_keys("id_form-1-name", name)
                sel.type("id_form-1-name",name)
            else:
                self.verificationErrors.append("Edit field for user's name not found")
                print testvars.preE+"Edit field for user's name not found"
            # Enter user's email address
            if sel.is_element_present("id_form-1-email")==True:
                sel.click("id_form-1-email")
                #sel.type_keys("id_form-1-email", email)
                sel.type("id_form-1-email",email)
            else:
                self.verificationErrors.append("Edit field for user's email not found")
                print testvars.preE+"Edit field for user's email not found"
            # Enter user's role
            if sel.is_element_present("id_form-1-role_0")==True:
                sel.click("id_form-1-role_"+role)
            else:
                self.verificationErrors.append("Edit field for user's role not found")
                print testvars.preE+"Edit field for user's role not found"
            # Enter user's location
            if sel.is_element_present("id_form-1-location")==True:
                sel.click("id_form-1-location")
                #sel.type_keys("id_form-1-location", location)
                sel.type("id_form-1-location",location)
            else:
                self.verificationErrors.append("Edit field for user's location not found")
                print testvars.preE+"Edit field for user's location not found"
            # Enter user's website
            if sel.is_element_present("id_form-1-website")==True:
                sel.click("id_form-1-website")
                #sel.type_keys("id_form-3-website", website)
                sel.type("id_form-1-website",website)
            else:
                self.verificationErrors.append("Edit field for user's website not found")
                print testvars.preE+"Edit field for user's website not found"
            # Enter user's description
            if sel.is_element_present("id_form-1-description")==True:
                sel.click("id_form-1-description")
                #sel.type_keys("id_form-1-description", description)
                sel.type("id_form-1-description",description)
            else:
                self.verificationErrors.append("Edit field for user's description not found")
                print testvars.preE+"Edit field for user's description not found"
            # Enter user's password
            if sel.is_element_present("id_form-1-password_f")==True:
                sel.click("id_form-1-password_f")
                #sel.type_keys("id_form-1-password_f", password)
                sel.type("id_form-1-password_f",password)
            else:
                self.verificationErrors.append("Edit field for user's passwordf not found")
                print testvars.preE+"Edit field for user's passwordf not found"
                # Enter user's password confirm
            if sel.is_element_present("id_form-1-password_f2")==True:
                sel.click("id_form-1-password_f2")
                #sel.type_keys("id_form-1-password_f2", password)
                sel.type("id_form-1-password_f2",password)
            else:
                self.verificationErrors.append("Edit field for user's passwordf2 not found")
                print testvars.preE+"Edit field for user's passwordf2 not found"
            # Save changes
            buttonSubmit = testvars.MCTestVariables["SaveChanges"]
            if sel.is_element_present(buttonSubmit)==True:
                sel.click(buttonSubmit)
            else:
                self.verificationErrors.append("Save button on Add User pop-up not found")
                print testvars.preE+"Save button on Add User pop-up not found"
                sel.refresh()
                sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])
        else:
            self.verificationErrors.append("Edit link not found for username")
            print testvars.preE+"Edit link not found for username "+username
        if UserRow(self, sel, username)==0:
            self.verificationErrors.append("Could not edit username")
            print testvars.preE+"Could not edit username "+username
    else:
        print testvars.preE+"Could not find username "+username

        sel.get_text("//a[contains(text(),'Email')]")

# =======================================
# =         EDIT USER PROFILE           =
# =======================================
def EditUserProfile(self,sel,name,username,email,location,website,description):
    #Check if the edit profile page can be opened
    sel.open(testvars.MCTestVariables["TestSite"])
    buttonEditProfile = "link=Your Profile"
    if sel.is_element_present(buttonEditProfile)==True:           
        sel.click(buttonEditProfile)
        time.sleep(2)
        if sel.is_element_present("link=Your Profile")==False:
            self.verificationErrors.append("Edit profile page does not display")
            print testvars.preE+"Edit profile page does not display"
        else:
            # Enter name
            if sel.is_element_present("id_name")==True:
                sel.click("id_name")
                #sel.type_keys("id_name", name)
                sel.type("id_name",name)
            else:
                self.verificationErrors.append("Edit field for user's name not found")
                print testvars.preE+"Edit field for user's name not found"
            # Enter username
            if sel.is_element_present("id_username")==True:
                sel.click("id_username")
                #sel.type_keys("id_username", us)
                sel.type("id_username",username)
            else:
                self.verificationErrors.append("Edit field for user's username not found")
                print testvars.preE+"Edit field for user's username not found"
                # Enter user's email address
            if sel.is_element_present("id_email")==True:
                sel.click("id_email")
                #sel.type_keys("id_email", email)
                sel.type("id_email",email)
            else:
                self.verificationErrors.append("Edit field for user's email not found")
                print testvars.preE+"Edit field for user's email not found"
                # Enter user's location
            if sel.is_element_present("id_location")==True:
                sel.click("id_location")
                #sel.type_keys("id_location", location)
                sel.type("id_location",location)
            else:
                self.verificationErrors.append("Edit field for user's location not found")
                print testvars.preE+"Edit field for user's location not found"
                # Enter user's website
            if sel.is_element_present("id_website")==True:
                sel.click("id_website")
                #sel.type_keys("id_website", website)
                sel.type("id_website",website)
            else:
                self.verificationErrors.append("Edit field for user's website not found")
                print testvars.preE+"Edit field for user's website not found"
                # Enter user's description
            if sel.is_element_present("id_description")==True:
                sel.click("id_description")
                #sel.type_keys("id_description", description)
                sel.type("id_description",description)
            else:
                self.verificationErrors.append("Edit field for user's description not found")
                print testvars.preE+"Edit field for user's description not found"
                # Save changes
                time.sleep(2)
            if sel.is_element_present("submit_settings")==True:
                sel.click("submit_settings")
            else:
                self.verificationErrors.append("Save button on Add User pop-up not found")
                print testvars.preE+"Save button on Add User pop-up not found"
    else:
        self.verificationErrors.append("Edit field button not found")
        print testvars.preE+"Edit field button not found"
    sel.refresh()
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
        self.verificationErrors.append("View profile button not found")
        print testvars.preE+"View profile button not found"
# =======================================
# =             VIEW USER               =
# =======================================
def ViewUser(self,sel,username):
    usRow = UserRow(self,sel,username)
    if usRow!=0:
        sel.open(testvars.MCTestVariables["UserPage"])
        elementView = "//div[@id='labels']/form/table/tbody/tr["+str(usRow)+"]/td[2]/div/a[3]"
        if sel.is_element_present(elementView):
            sel.click(elementView)
            time.sleep(2)
        else:
            self.verificationErrors.append("View link not found for username "+username)
            print testvars.preE+"View link not found for username "+username
            time.sleep(2)
    else:
        print testvars.preE+"Could not find user "+username
# =======================================
# =             VIEW USER CHECK         =
# =======================================
def ViewUserCheek(self,sel,username,name,location,website,description):
    # Check profile username
    if sel.is_element_present("//div[@id='author_info']/h1")==True:
        currentProfile = sel.get_text("//div[@id='author_info']/h1")
        if currentProfile.find(username)!=-1:
            print "View profile username successful"
        else:
            print "View profile username fail"
            mclib.AppendErrorMessage(self,sel,"View profile username "+username+" fail")
    # Check profile name
    time.sleep(1)
    if sel.is_element_present("//div[@id='author_info']/h1")==True:
        currentProfile = sel.get_text("//div[@id='author_info']/h1")
        if currentProfile.find(name)!=-1:
            print "View profile name successful"
        else:
            print "View profile name fail"
            mclib.AppendErrorMessage(self,sel,"View profile name fail")
    # Check profile location
    time.sleep(1)
    if sel.is_element_present("//div[@id='location']")==True:
        currentProfile = sel.get_text("//div[@id='location']")
        if currentProfile.find(location)!=-1:
            print "View profile location successful"
        else:
            print "View profile location fail"
            mclib.AppendErrorMessage(self,sel,"View profile location fail")
    # Check profile website
    time.sleep(1)
    if sel.is_element_present("//div[@id='link']/a")==True:
        currentProfile = sel.get_text("//div[@id='link']/a")
        if currentProfile.find(website)!=-1:
            print "View profile website successful"
        else:
            print "View profile website fail"
            mclib.AppendErrorMessage(self,sel,"View profile website fail")
    # Check profile description
    time.sleep(1)
    if sel.is_element_present("//div[@id='author_info']/div[3]")==True:
        currentProfile = sel.get_text("//div[@id='author_info']/div[3]")
        if currentProfile.find(description)!=-1:
            print "View profile description successful"
        else:
            print "View profile description fail"
            mclib.AppendErrorMessage(self,sel,"View profile description fail")
