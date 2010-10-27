#=======================================================================
#
#                       USERS TESTS
#
#=======================================================================
#
#   Includes the following test cases:
#     1. TestCase_AddNewAdmin_271
#     2. TestCase_AddNewUser_270
#     3. TestCase_EditUser_291
#     4. TestCase_DeleteUser_272
#     5. TestCase_CreateNewUserUsernameAndPassword_280
#     6. TestCase_CreateNewUserWithoutUsername_274
#     7. TestCase_CreateNewUserWithoutPassword_273
#     8. TestCase_UsernameDoesntAcceptMax1Chars_283
#     9. TestCase_NewUserUsernameMaxMax2MinChars_281
#     10. TestCase_EditUserProfile_539
#     11. TestCase_ViewProfile_540
#     12. TestCase_ViewUser_290

from selenium import selenium
import unittest, time, re, os, loginlogout, testvars, users, mclib, sitesettings

# ----------------------------------------------------------------------

class TestCase_AddNewAdmin_271(unittest.TestCase):
    # Open the desired browser and set up the test
    def setUp(self):
        self.verificationErrors = []
        self.selenium = selenium("localhost", testvars.MCTestVariables["Port"], testvars.MCTestVariables["Browser"], testvars.MCTestVariables["TestSite"])
        self.selenium.start()
    # The user actions executed in the test scenario
    def test_AddNewAdmin_271(self):
        sel = self.selenium
        # Log in as Admin
        loginlogout.LogInAsAdmin(self,sel)
        # This is information for add user edit fields
#        username = "vitalii1"
        username = "newTestAdmin"
        password = "123456"
        email = "admin1@test.com"
        role = "1" # "1"-Admin, "0"-User
        # This function returns the row number for the desired username
        # on /users page.
        # Returns row number if the us username is found and 0 otherwise.
        if users.UserRow(self,sel,username)!=0:
            print "Duplicate user found. Deleting it..."
            # This function delete user
            users.DeleteUser(self,sel,username,0)
        # This function add user
        users.AddUser(self,sel,username,email,role,password)
        print "Logging out..."
        # This function log out
        loginlogout.LogOut(self,sel)
        print "Logging in as user: "+username
        # This function login as just created user
        loginlogout.LogInBasic(self,sel,username,password)
        # Check user logon as admin
        if sel.is_element_present(testvars.MCTestVariables["ViewAdmin"])==True or sel.is_element_present(testvars.MCTestVariables["ViewAdminBlueTheme"])==True:
            print "Logged as Admin"
        else:
            mclib.AppendErrorMessage(self,sel,"User "+username+" does not have Administrator privileges")
    # Close the browser, log errors, perform cleanup   
    def tearDown(self):
        self.selenium.stop()
    # the command on the previous line should close the browser
        self.assertEqual([], self.verificationErrors)

class TestCase_AddNewUser_270(unittest.TestCase):
    # Open the desired browser and set up the test
    def setUp(self):
        self.verificationErrors = []
        self.selenium = selenium("localhost", testvars.MCTestVariables["Port"], testvars.MCTestVariables["Browser"], testvars.MCTestVariables["TestSite"])
        self.selenium.start()
# The user actions executed in the test scenario
    def test_AddNewUser_270(self):
        sel = self.selenium
        # Log in as Admin
        loginlogout.LogInAsAdmin(self,sel)
        # This is information for add user edit fields
#        username = "vitalii"
        username = "newTestUser"
        password = "123456"
        email = "user1@test.com"
        # To select User role type "0"
        # To select Admin role type "1"
        role = "0" 
        # This function returns the row number for the desired username
        # on /users page.
        # Returns row number if the us username is found and 0 otherwise.
        if users.UserRow(self,sel,username)!=0:
            print "Duplicate user found. Deleting it..."
            # This function delete user
            users.DeleteUser(self,sel,username,0)
        # This function add user
        users.AddUser(self,sel,username,email,role,password)
        print "Logging out..."
        # This function log out
        loginlogout.LogOut(self,sel)
        print "Logging in as user: "+username
        # This function login as just created user
        loginlogout.LogInBasic(self,sel,username,password)
        # Check user logon as user
        if sel.is_element_present(testvars.MCTestVariables["ViewAdmin"])==True:
            print "Log in as User failed"
        else:
            print "Logged as User"
    # Close the browser, log errors, perform cleanup   
    def tearDown(self):
        self.selenium.stop()
    # the command on the previous line should close the browser
        self.assertEqual([], self.verificationErrors)

class TestCase_EditUser_291(unittest.TestCase):
    # Open the desired browser and set up the test
    def setUp(self):
        self.verificationErrors = []
        self.selenium = selenium("localhost", testvars.MCTestVariables["Port"], testvars.MCTestVariables["Browser"], testvars.MCTestVariables["TestSite"])
        self.selenium.start()
    # The user actions executed in the test scenario
    def test_EditUser_291(self):
        sel = self.selenium
        # Log in as Admin
        loginlogout.LogInAsAdmin(self,sel)
        # This is information for add user edit fields
        username = "newTestUser2"
        newusername = "modifiedTestUser2"
        password = "123456"
        name = "John Doe"
        email = "john.doe@test.com"
        # To select User role type "0"
        # To select Admin role type "1"
        role = "1"
        location = "Greenland"  
        website = "www.google.ca"
        logo = "photo3.jpg"
        description = "Hello"
        # Check if user appeared
        if users.UserRow(self,sel,username)!=0:
            print "Found user "+username+". Deleting it..."
            users.DeleteUser(self,sel,username,0)
        if newusername!="":
            if users.UserRow(self,sel,newusername)!=0:
                print "Found user "+newusername+". Deleting it..."
                users.DeleteUser(self,sel,newusername,0)
        # Add user <username>                
        users.AddUser(self,sel,username,email,role,password)
        # Now modify this user account
        users.EditUser(self,sel,username,newusername,name,email,role,location,website,description,logo,password)
        # Attempt to login to the system with the modified account
        if newusername!="":
            userlogin = newusername
        else:
            userlogin = username
        if users.UserRow(self,sel,userlogin)!=0:
            print "User "+username+" successfully edited"
            # Log out
            loginlogout.LogOut(self,sel)
            print "Logging in as user: "+userlogin+"..."
            # Log in as just created user
            loginlogout.LogInBasic(self,sel,userlogin,password)
    # Close the browser, log errors, perform cleanup   
    def tearDown(self):
        self.selenium.stop()
    # the command on the previous line should close the browser
        self.assertEqual([], self.verificationErrors)

class TestCase_DeleteUser_272(unittest.TestCase):
    # Open the desired browser and set up the test
    def setUp(self):
        self.verificationErrors = []
        self.selenium = selenium("localhost", testvars.MCTestVariables["Port"], testvars.MCTestVariables["Browser"], testvars.MCTestVariables["TestSite"])
        self.selenium.start()
    # The user actions executed in the test scenario
    def test_DeleteUser_272(self):
        sel = self.selenium
        # Log in as Admin
        loginlogout.LogInAsAdmin(self,sel)
        # Adding a new user withe the following parameters
#        username = "vitalii5"
        username = "newTestUser3"
        password = "123456"
        email = "user3@test.com"
        # To select User role type "0"
        # To select Admin role type "1"
        role = "0"        
        # This function add user
        users.AddUser(self,sel,username,email,role,password)
        # Now deleting the recently created user
        users.DeleteUser(self,sel,username,0)
        # Close the browser, log errors, perform cleanup   
    def tearDown(self):
        self.selenium.stop()
# the command on the previous line should close the browser
        self.assertEqual([], self.verificationErrors)

class TestCase_CreateNewUserUsernameAndPassword_280(unittest.TestCase):
    def setUp(self):
        self.verificationErrors = []
        self.selenium = selenium("localhost", testvars.MCTestVariables["Port"], testvars.MCTestVariables["Browser"], testvars.MCTestVariables["TestSite"])
        self.selenium.start()

# The user actions executed in the test scenario
    def test_CreateNewUserUsernameAndPassword_280(self):
        sel = self.selenium
        # Log in as Admin
        loginlogout.LogInAsAdmin(self,sel)
        # This is information for add user edit fields
#        username = "vitalii"
        username = "newTestUser3"
        password = "123456"
        email = ""
        # To select User role type "0"
        # To select Admin role type "1"
        role = "" 
        # This function returns the row number for the desired username
        # on /users page.
        # Returns row number if the us username is found and 0 otherwise.
        if users.UserRow(self,sel,username)!=0:
            print "Duplicate user found. Deleting it..."
            # This function delete user
            users.DeleteUser(self,sel,username,0)
            print "User deleted: "+username
        # This function add user
        users.AddUser(self,sel,username,email,role,password)
        print "Logging out..."
        # This function log out
        loginlogout.LogOut(self,sel)
        print "Logging in as user: "+username
        # This function login as just created user
        loginlogout.LogInBasic(self,sel,username,password)
# Close the browser, log errors, perform cleanup   
    def tearDown(self):
        self.selenium.stop()
# the command on the previous line should close the browser
        self.assertEqual([], self.verificationErrors)

class TestCase_CreateNewUserWithoutUsername_274(unittest.TestCase):
   # Open the desired browser and set up the test
    def setUp(self):
        self.verificationErrors = []
        self.selenium = selenium("localhost", testvars.MCTestVariables["Port"], testvars.MCTestVariables["Browser"], testvars.MCTestVariables["TestSite"])
        self.selenium.start()
    # The user actions executed in the test scenario
    def test_CreateNewUserWithoutUsername_274(self):
        sel = self.selenium
        # Log in as Admin
        loginlogout.LogInAsAdmin(self,sel)
        # This is information for add user edit fields
        username = ""
        password = "123456"
        email = "test5@test.com"
        role = "0" # "0" - User, "1" - Admin
        website = "www.google.com"
        # This function add user
        users.FillAddUserPopUp(self,sel,username,email,role,password)
        # Check if user appeared
        if users.UserRow(self,sel,username)!=0:
            mclib.AppendErrorMessage(self,sel,"Unexpectedly could create a user with username left blank. TEST FAILED")
        else:
            print "Could not create a user with Username (mandatory field) left blank. TEST PASSED"
# Close the browser, log errors, perform cleanup   
    def tearDown(self):
        self.selenium.stop()
# the command on the previous line should close the browser
        self.assertEqual([], self.verificationErrors)

class TestCase_CreateNewUserWithoutPassword_273(unittest.TestCase):
    # Open the desired browser and set up the test
    def setUp(self):
        self.verificationErrors = []
        self.selenium = selenium("localhost", testvars.MCTestVariables["Port"], testvars.MCTestVariables["Browser"], testvars.MCTestVariables["TestSite"])
        self.selenium.start()
    # The user actions executed in the test scenario
    def test_CreateNewUserWithoutPassword_273(self):
        sel = self.selenium
        # Log in as Admin
        loginlogout.LogInAsAdmin(self,sel)
        # This is information for add user edit fields
#        username = "vitalii2"
        username = "newTestUser4"
        password = ""
        email = "test6@test.com"
        role = "0" # "1" - Admin, "0" - User
        website = "www.google.com"
        # This function returns the row number for the desired username
        # on /users page.
        # Returns row number if the us username is found and 0 otherwise.
        if users.UserRowInCompleteListOfAuthors(self,sel,username)!=0:
            print "Duplicate user found. Deleting it..."
            # This function delete user
            users.DeleteUser(self,sel,username,1)
            print "User deleted: "+username
        # This function add user
        users.FillAddUserPopUp(self,sel,username,email,role,password)
        # Check if user appeared in the list
        print "Checking if the user was successfully created..."
        if users.UserRowInCompleteListOfAuthors(self,sel,username)==0:
            mclib.AppendErrorMessage(self,sel,"Could not create a user with PASSWORD (optional field) blank")
        else:
            print "OK"
            # Attempt to log in with the new account
            loginlogout.LogOut(self,sel)
            sel.open(testvars.MCTestVariables["LoginPage"])
            sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])
            time.sleep(1)
            sel.click("id_username")
            sel.type("id_username", username)
            time.sleep(1)
            sel.click("//input[@value='Log In']")
            sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])
            if sel.is_text_present("This field is required.") and sel.is_element_present(testvars.MCTestVariables["LogoutFootlink"])==False:
                print "Could not login as a 'non-human' (passwordless) user. TEST PASSED"
            else:
                mclib.AppendErrorMessage(self,sel,"Managed to login as a passwordless user "+username+". TEST FAILED")
            
# Close the browser, log errors, perform cleanup   
    def tearDown(self):
        self.selenium.stop()
# the command on the previous line should close the browser
        self.assertEqual([], self.verificationErrors)

class TestCase_UsernameDoesntAcceptMax1Chars_283(unittest.TestCase):
    # Open the desired browser and set up the test
    def setUp(self):
        self.verificationErrors = []
        self.selenium = selenium("localhost", testvars.MCTestVariables["Port"], testvars.MCTestVariables["Browser"], testvars.MCTestVariables["TestSite"])
        self.selenium.start()
    # The user actions executed in the test scenario
    def test_UsernameDoesntAcceptMax1Chars_283(self):
        sel = self.selenium
        # Log in as Admin
        loginlogout.LogInAsAdmin(self,sel)
        # This is information for add user edit fields
        username = "1234567890123456789012345678901"
        password = "123456"
        email = "oversizeuser@test.com"
        role = "0"  # "1"-Admin, "0"-User
        if users.UserRow(self,sel,username)!=0:
            print "Duplicate user found. Deleting it..."
            # This function delete user
            users.DeleteUser(self,sel,username,0)
            print "User deleted: "+username
        # This function add user
#        users.FillAddUserPopUp(self,sel,username,email,role,password)
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
                    typedUsername = sel.get_value("id_username")
                    if typedUsername == username:
                        mclib.AppendErrorMessage(self,sel,"Username edit fields accepts strings longer than 30 characters.")
                    elif typedUsername == username[:-1]:
                        print "Username edit field trims all input to 30 permitted characters."
                        print "Attempted to type: "+username
                        print "-- Actually typed: "+typedUsername
                    else:
                        print "Unexpected string found in Username edit field"
                        print "Expected string: "+username
                        print "- Actual string: "+typedUsername
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
                sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])
                if users.UserRow(self,sel,username)!=0:
                    mclib.AppendErrorMessage(self,sel,"User with too long username found in the list: "+username+". TEST FAILED")
                else:
                    print "Could not add a user with an excessively long username. TEST PASSED"
# Close the browser, log errors, perform cleanup   
    def tearDown(self):
        self.selenium.stop()
# the command on the previous line should close the browser
        self.assertEqual([], self.verificationErrors)

class TestCase_NewUserUsernameMaxMax2MinChars_281(unittest.TestCase):
    # Open the desired browser and set up the test
    def setUp(self):
        self.verificationErrors = []
        self.selenium = selenium("localhost", testvars.MCTestVariables["Port"], testvars.MCTestVariables["Browser"], testvars.MCTestVariables["TestSite"])
        self.selenium.start()
    # The user actions executed in the test scenario
    def test_NewUserUsernameMaxMax2MinChars_281(self):
        sel = self.selenium
        # Log in as Admin
        loginlogout.LogInAsAdmin(self,sel)
        # This is information for add user edit fields
        username = "123456789012345678901234567890"
        password = "123456"
        email = "testuser@test.com"
        # To select User role type "0"
        # To select Admin role type "1"
        role = "0"      
        # This function returns the row number for the desired username
        # on /users page.
        # Returns row number if the us username is found and 0 otherwise.
        if users.UserRow(self,sel,username)!=0:
            print "Duplicate user found. Deleting it..."
            # This function delete user
            users.DeleteUser(self,sel,username,0)
            print "User deleted: "+username
        # This function add user
        users.AddUser(self,sel,username,email,role,password)
        print "Logging out..."
        # This function check and log out
        if users.UserRow(self,sel,username)!=0:
            loginlogout.LogOut(self,sel)
        else:
            users.AddUser(self,sel,username,email,role,password)
        print "Logging in as user: "+username
        # This function login as just created user
        loginlogout.LogInBasic(self,sel,username,password)
        sel.click("link=Logout "+username)
        sel.wait_for_page_to_load("10000")
    ##### Creating user with 15 chars in the 'Username' field #####
        loginlogout.LogInAsAdmin(self,sel)
        username = "123456789012345"
        if users.UserRow(self,sel,username)!=0:
            print "Duplicate user found. Deleting it..."
            users.DeleteUser(self,sel,username,0)
            print "User deleted: "+username
        users.AddUser(self,sel,username,email,role,password)
        print "Logging out..."
        if users.UserRow(self,sel,username)!=0:
            loginlogout.LogOut(self,sel)
        else:
            users.AddUser(self,sel,username,email,role,password)
        print "Logging in as user: "+username
        loginlogout.LogInBasic(self,sel,username,password)
        sel.click("link=Logout "+username)
        sel.wait_for_page_to_load("10000")
    ##### Creating user with 1 chars in the 'Username' field #####
        loginlogout.LogInAsAdmin(self,sel)
        username = "1"
        if users.UserRow(self,sel,username)!=0:
            print "Duplicate user found. Deleting it..."
            users.DeleteUser(self,sel,username,0)
            print "User deleted: "+username
        users.AddUser(self,sel,username,email,role,password)
        print "Logging out..."
        if users.UserRow(self,sel,username)!=0:
            loginlogout.LogOut(self,sel)
        else:
            users.AddUser(self,sel,username,email,role,password)
        print "Logging in as user: "+username
        loginlogout.LogInBasic(self,sel,username,password)
        sel.click("link=Logout "+username)
        sel.wait_for_page_to_load("10000")
    # Close the browser, log errors, perform cleanup   
    def tearDown(self):
        self.selenium.stop()
    # the command on the previous line should close the browser
        self.assertEqual([], self.verificationErrors)


class TestCase_EditUserProfile_539(unittest.TestCase):
# Open the desired browser and set up the test
    def setUp(self):
        self.verificationErrors = []
        self.selenium = selenium("localhost", testvars.MCTestVariables["Port"], testvars.MCTestVariables["Browser"], testvars.MCTestVariables["TestSite"])
        self.selenium.start()
# The user actions executed in the test scenario
    # The user actions executed in the test scenario
    def test_EditUserProfile_539(self):
        sel = self.selenium
        # Log in as Admin
        loginlogout.LogInAsAdmin(self,sel)
        # Check that user newTestUser exists. If not, create a new user
        username = "newTestUser"
        password = "123456"
        if users.UserRow(self,sel,username)==0:
            users.AddUser(self,sel,username,"","0",password)
        # New settings for the user profile
        name = "NewUser"
        newusername = ""
        password = "123456"
        location = "North America"
        website = "http://www.google.ca/"
        description = "Miro Community QA"
        photo = "photo5.jpg"
        email = "user2@test.com"
        # Detect current theme
        sel.click(testvars.MCTestVariables["ViewMainSiteLink"])
        sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])
        theme = sitesettings.ThemeScanner(self,sel)
        print "Logging out..."
        loginlogout.LogOut(self,sel)
        print "Log in as "+username
        loginlogout.LogInBasic(self,sel,username,password)
        print "Editing the profile for "+username
        users.EditUserProfile(self,sel,name,newusername,email,location,website,os.path.join(testvars.MCTestVariables["GraphicFilesDirectory"],photo),description)
        users.ViewUserCheck(self,sel,theme,username,name,location,website,description,photo)
# Close the browser, log errors, perform cleanup   
    def tearDown(self):
        self.selenium.stop()
# the command on the previous line should close the browser
        self.assertEqual([], self.verificationErrors)

class TestCase_ViewProfile_540(unittest.TestCase):
# Open the desired browser and set up the test
    def setUp(self):
        self.verificationErrors = []
        self.selenium = selenium("localhost", testvars.MCTestVariables["Port"], testvars.MCTestVariables["Browser"], testvars.MCTestVariables["TestSite"])
        self.selenium.start()
# The user actions executed in the test scenario
    def test_ViewProfile_540(self):
        sel = self.selenium
        # The profile to be viewed belongs to seleniumTestUser
        username = testvars.MCTestVariables["UserLogin"] 
        name = testvars.MCTestVariables["UserName"] 
        description = "test user for selenium auto testing. Please don't delete." 
        location = "PCF" 
        website = "http://www.seleniumhq.org/" 
        image = "nest-test.jpg"
        print "Viewing user profile in different themes"
        for theme in range(1,5):
            print ""
            print "====== theme "+str(theme)
            # Change theme
            loginlogout.LogInAsAdmin(self,sel)
            sitesettings.ChangeTheme(self,sel,theme)
            loginlogout.LogOut(self,sel)
            # Log in as user
            loginlogout.LogInAsUser(self,sel)
            print "Checking profile"
            users.ViewProfile(self,sel)
            users.ViewUserCheck(self,sel,theme,username,name,location,website,description,image)
            loginlogout.LogOut(self,sel)
# Close the browser, log errors, perform cleanup   
    def tearDown(self):
        self.selenium.stop()
# the command on the previous line should close the browser
        self.assertEqual([], self.verificationErrors)

class TestCase_ViewUser_290(unittest.TestCase):
# Open the desired browser and set up the test
    def setUp(self):
        self.verificationErrors = []
        self.selenium = selenium("localhost", testvars.MCTestVariables["Port"], testvars.MCTestVariables["Browser"], testvars.MCTestVariables["TestSite"])
        self.selenium.start()
# The user actions executed in the test scenario
    def test_ViewUser_290(self):
        sel = self.selenium
        # Log in as Admin
        loginlogout.LogInAsAdmin(self,sel)
        # Viewing seleniumTestUser from /admin/users page
        username = testvars.MCTestVariables["UserLogin"]
        password = testvars.MCTestVariables["UserPassword"]
        name = testvars.MCTestVariables["UserName"] 
        description = "test user for selenium auto testing. Please don't delete." 
        location = "PCF" 
        website = "http://www.seleniumhq.org/" 
        image = "nest-test.jpg"
        role = "0" # "1" - Admin, "0" - User
        if users.UserRow(self,sel,username)!=0:
            users.ViewUser(self,sel,username,name,location,website,description,image)
        else:
            mclib.AppendErrorMessage(self,sel,"User "+username+" not found in the list")
        # Close the browser, log errors, perform cleanup   
    def tearDown(self):
        self.selenium.stop()
# the command on the previous line should close the browser
        self.assertEqual([], self.verificationErrors)
