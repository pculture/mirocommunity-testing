#=======================================================================
#
#                       USERS TESTS
#
#=======================================================================
#
#   Includes the following test cases:
#     1. TestCase_AddNewAdmin
#     2. TestCase_AddNewUser
#     3. TestCase_EditUser
#     4. TestCase_DeleteUser
#     5. TestCase_CreateNewUserUsernameAndPassword
#     6. TestCase_CreateNewUserWithoutUsername
#     7. TestCase_CreateNewUserWithoutPassword
#     8. TestCase_UsernameDoesntAcceptMax1Chars
#     9. TestCase_NewUserUsernameMaxMax2MinChars
#     10. TestCase_EditUserProfile
#     11. TestCase_ViewProfile(unittest.TestCase)
#     12. TestCase_ViewUser(unittest.TestCase)

from selenium import selenium
import unittest, time, re, loginlogout, testvars, users, mclib

# ----------------------------------------------------------------------

class TestCase_AddNewAdmin(unittest.TestCase):
    # Open the desired browser and set up the test
    def setUp(self):
        self.verificationErrors = []
        self.selenium = selenium("localhost", testvars.MCTestVariables["Port"], testvars.MCTestVariables["Browser"], testvars.MCTestVariables["TestSite"])
        self.selenium.start()
    # The user actions executed in the test scenario
    def test_AddNewAdmin(self):
        sel = self.selenium
        # Log in as Admin
        loginlogout.LogInAsAdmin(self,sel)
        # This is information for add user edit fields
        username = "vitalii1"
        password = "123456"
        email = "netvetal@ua.fm"
        # To select User role type "0"
        # To select Admin role type "1"
        role = "1" 
        # This function returns the row number for the desired username
        # on /users page.
        # Returns row number if the us username is found and 0 otherwise.
        if users.UserRow(self,sel,username)!=0:
            print "Duplicate user found. Deleting it..."
            # This function delete user
            users.DeleteUser(self,sel,username)
            print "User deleted: "+username
        # This function add user
        users.AddUser(self,sel,username,email,role,password)
        print "Logging out..."
        # This function log out
        loginlogout.LogOut(self,sel)
        print "Logging in as user: "+username
        # This function login as just created user
        loginlogout.LogInBasic(self,sel,username,password)
        # Cheek user logon as admin
        if sel.is_element_present(testvars.MCTestVariables["ViewAdmin"])==True:
            print "Logged as Admin"
        else:
            self.verificationErrors.append("Log in user "+username+" as Admin fail")
            print testvars.preE+"Log in user "+username+" as Admin fail"
    # Close the browser, log errors, perform cleanup   
    def tearDown(self):
        self.selenium.stop()
    # the command on the previous line should close the browser
        self.assertEqual([], self.verificationErrors)

class TestCase_AddNewUser(unittest.TestCase):
    # Open the desired browser and set up the test
    def setUp(self):
        self.verificationErrors = []
        self.selenium = selenium("localhost", testvars.MCTestVariables["Port"], testvars.MCTestVariables["Browser"], testvars.MCTestVariables["TestSite"])
        self.selenium.start()
# The user actions executed in the test scenario
    def test_AddNewUser(self):
        sel = self.selenium
        # Log in as Admin
        loginlogout.LogInAsAdmin(self,sel)
        # This is information for add user edit fields
        username = "vitalii"
        password = "123456"
        email = "netvetal@ua.fm"
        # To select User role type "0"
        # To select Admin role type "1"
        role = "0" 
        # This function returns the row number for the desired username
        # on /users page.
        # Returns row number if the us username is found and 0 otherwise.
        if users.UserRow(self,sel,username)!=0:
            print "Duplicate user found. Deleting it..."
            # This function delete user
            users.DeleteUser(self,sel,username)
            print "User deleted: "+username
        # This function add user
        users.AddUser(self,sel,username,email,role,password)
        print "Logging out..."
        # This function log out
        loginlogout.LogOut(self,sel)
        print "Logging in as user: "+username
        # This function login as just created user
        loginlogout.LogInBasic(self,sel,username,password)
        # Cheek user logon as user
        if sel.is_element_present(testvars.MCTestVariables["ViewAdmin"])==True:
            print "Log in as User fail"
        else:
            print "Logged as User"
    # Close the browser, log errors, perform cleanup   
    def tearDown(self):
        self.selenium.stop()
    # the command on the previous line should close the browser
        self.assertEqual([], self.verificationErrors)

class TestCase_EditUser(unittest.TestCase):
    # Open the desired browser and set up the test
    def setUp(self):
        self.verificationErrors = []
        self.selenium = selenium("localhost", testvars.MCTestVariables["Port"], testvars.MCTestVariables["Browser"], testvars.MCTestVariables["TestSite"])
        self.selenium.start()
    # The user actions executed in the test scenario
    def test_EditUser(self):
        sel = self.selenium
        # Log in as Admin
        loginlogout.LogInAsAdmin(self,sel)
        # This is information for add user edit fields
        username = "vitalii4"
        password = "123456"
        name = "Vitalii Kozeratskyi"
        email = "kozeratskyi@gmail.com"
        # To select User role type "0"
        # To select Admin role type "1"
        role = "1"
        location = "B.C."  
        website = "www.google.ca"
        description = "Hello"
        # Cheek if user appeared
        if users.UserRow(self,sel,username)!=0:
            print "User finded start to edit"
            # This function edit user
            users.EditUser(self,sel,username,name,email,role,location,website,description,password)
            print "User "+username+" edited"
        else:
            users.AddUser(self,sel,username,email,role,password)
            print "User "+username+" created"
            users.EditUser(self,sel,username,name,email,role,location,website,description,password)
            print "User "+username+" edited"
        # This function log out
        loginlogout.LogOut(self,sel)
        print "Logging in as user: "+username
        # This function login as just created user
        loginlogout.LogInBasic(self,sel,username,password)
        # Cheek user logon as admin
        if sel.is_element_present(testvars.MCTestVariables["ViewAdmin"])==True:
            print "Logged as Admin"
        else:
            self.verificationErrors.append("Log in user "+username+" as Admin fail")
            print testvars.preE+"Log in user "+username+" as Admin fail"
    # Close the browser, log errors, perform cleanup   
    def tearDown(self):
        self.selenium.stop()
    # the command on the previous line should close the browser
        self.assertEqual([], self.verificationErrors)

class TestCase_DeleteUser(unittest.TestCase):
    # Open the desired browser and set up the test
    def setUp(self):
        self.verificationErrors = []
        self.selenium = selenium("localhost", testvars.MCTestVariables["Port"], testvars.MCTestVariables["Browser"], testvars.MCTestVariables["TestSite"])
        self.selenium.start()
    # The user actions executed in the test scenario
    def test_DeleteUser(self):
        sel = self.selenium
        # Log in as Admin
        loginlogout.LogInAsAdmin(self,sel)
        # This is information for add user edit fields
        username = "vitalii5"
        password = "123456"
        email = "kozeratskyi@gmail.com"
        # To select User role type "0"
        # To select Admin role type "1"
        role = "0"        
        print "Adding user: "+username
        # This function add user
        users.AddUser(self,sel,username,email,role,password)
        # This function delete user
        print "Deleting user: "+username
        users.DeleteUser(self,sel,username)
        print "User "+username+" deleted."
        print "Logging out..."
        # This function log out
        time.sleep(2)
        loginlogout.LogOut(self,sel)
        print "Logging in as user: "+username
        # This function login as just created user
        sel.open(testvars.MCTestVariables["LoginPage"])
        sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])
        sel.window_maximize()
        sel.click("id_username")
        sel.type("id_username", username)
        sel.click("id_password")
        sel.type("id_password", password)
        sel.click("//input[@value='Log In']")
        sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])
        if sel.is_element_present("//input[@value='Log In']")==True:
            print "Login fail"
        else:
            self.verificationErrors.append("Deleting user fail")
            print testvars.preE+"Deleting user fail"
        # Close the browser, log errors, perform cleanup   
    def tearDown(self):
        self.selenium.stop()
# the command on the previous line should close the browser
        self.assertEqual([], self.verificationErrors)

class TestCase_CreateNewUserUsernameAndPassword(unittest.TestCase):
    def setUp(self):
        self.verificationErrors = []
        self.selenium = selenium("localhost", testvars.MCTestVariables["Port"], testvars.MCTestVariables["Browser"], testvars.MCTestVariables["TestSite"])
        self.selenium.start()

# The user actions executed in the test scenario
    def test_CreateNewUserUsernameAndPassword(self):
        sel = self.selenium
        # Log in as Admin
        loginlogout.LogInAsAdmin(self,sel)
        # This is information for add user edit fields
        username = "vitalii"
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
            users.DeleteUser(self,sel,username)
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

class TestCase_CreateNewUserWithoutUsername(unittest.TestCase):
   # Open the desired browser and set up the test
    def setUp(self):
        self.verificationErrors = []
        self.selenium = selenium("localhost", testvars.MCTestVariables["Port"], testvars.MCTestVariables["Browser"], testvars.MCTestVariables["TestSite"])
        self.selenium.start()
    # The user actions executed in the test scenario
    def test_CreateNewUserWithoutUsername(self):
        sel = self.selenium
        # Log in as Admin
        loginlogout.LogInAsAdmin(self,sel)
        # This is information for add user edit fields
        username = ""
        password = "123456"
        email = "netvetal@ua.fm"
        # To select User role type "0"
        # To select Admin role type "1"
        role = "0" 
        website = "www.google.ca"
        # This function add user
        users.AddUser(self,sel,username,email,role,password)
        # Cheek if user appeared
        if users.UserRow(self,sel,username)!=0:
            print "User added successfuly"
        else:
            print "Username edit field mandatory, create user fail"
# Close the browser, log errors, perform cleanup   
    def tearDown(self):
        self.selenium.stop()
# the command on the previous line should close the browser
        self.assertEqual([], self.verificationErrors)

class TestCase_CreateNewUserWithoutPassword(unittest.TestCase):
    # Open the desired browser and set up the test
    def setUp(self):
        self.verificationErrors = []
        self.selenium = selenium("localhost", testvars.MCTestVariables["Port"], testvars.MCTestVariables["Browser"], testvars.MCTestVariables["TestSite"])
        self.selenium.start()
    # The user actions executed in the test scenario
    def test_CreateNewUserWithoutPassword(self):
        sel = self.selenium
        # Log in as Admin
        loginlogout.LogInAsAdmin(self,sel)
        # This is information for add user edit fields
        username = "vitalii2"
        password = ""
        email = "netvetal@ua.fm"
        # To select User role type "0"
        # To select Admin role type "1"
        role = "0" 
        website = "www.google.ca"
        # This function returns the row number for the desired username
        # on /users page.
        # Returns row number if the us username is found and 0 otherwise.
        if users.UserRow(self,sel,username)!=0:
            print "Duplicate user found. Deleting it..."
            # This function delete user
            users.DeleteUser(self,sel,username)
            print "User deleted: "+username
        # This function add user
        users.AddUser(self,sel,username,email,role,password)
        # Cheek if user appeared
        if users.UserRow(self,sel,username)!=0:
            print "User added successfuly"
        else:
            print "Password edit field mandatory, create user fail"
# Close the browser, log errors, perform cleanup   
    def tearDown(self):
        self.selenium.stop()
# the command on the previous line should close the browser
        self.assertEqual([], self.verificationErrors)

class TestCase_UsernameDoesntAcceptMax1Chars(unittest.TestCase):
    # Open the desired browser and set up the test
    def setUp(self):
        self.verificationErrors = []
        self.selenium = selenium("localhost", testvars.MCTestVariables["Port"], testvars.MCTestVariables["Browser"], testvars.MCTestVariables["TestSite"])
        self.selenium.start()
    # The user actions executed in the test scenario
    def test_UsernameDoesntAcceptMax1Chars(self):
        sel = self.selenium
        # Log in as Admin
        loginlogout.LogInAsAdmin(self,sel)
        # This is information for add user edit fields
        username = "1234567890123456789012345678901"
        password = "123456"
        email = "kozeratskyi@gmail.net"
        # To select User role type "0"
        # To select Admin role type "1"
        role = "0"      
        # This function returns the row number for the desired username
        # on /users page.
        # Returns row number if the us username is found and 0 otherwise.
        if users.UserRow(self,sel,username)!=0:
            print "Duplicate user found. Deleting it..."
            # This function delete user
            users.DeleteUser(self,sel,username)
            print "User deleted: "+username
        print "Adding user: "+username
        # This function add user
        users.AddUser(self,sel,username,email,role,password)
# Close the browser, log errors, perform cleanup   
    def tearDown(self):
        self.selenium.stop()
# the command on the previous line should close the browser
        self.assertEqual([], self.verificationErrors)

class TestCase_NewUserUsernameMaxMax2MinChars(unittest.TestCase):
    # Open the desired browser and set up the test
    def setUp(self):
        self.verificationErrors = []
        self.selenium = selenium("localhost", testvars.MCTestVariables["Port"], testvars.MCTestVariables["Browser"], testvars.MCTestVariables["TestSite"])
        self.selenium.start()
    # The user actions executed in the test scenario
    def test_NewUserUsernameMaxMax2MinChars(self):
        sel = self.selenium
        # Log in as Admin
        loginlogout.LogInAsAdmin(self,sel)
        # This is information for add user edit fields
        username = "123456789012345678901234567890"
        password = "123456"
        email = "kozeratskyi@gmail.com"
        # To select User role type "0"
        # To select Admin role type "1"
        role = "0"      
        # This function returns the row number for the desired username
        # on /users page.
        # Returns row number if the us username is found and 0 otherwise.
        if users.UserRow(self,sel,username)!=0:
            print "Duplicate user found. Deleting it..."
            # This function delete user
            users.DeleteUser(self,sel,username)
            print "User deleted: "+username
        # This function add user
        users.AddUser(self,sel,username,email,role,password)
        print "Logging out..."
        # This function cheek and log out
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
            users.DeleteUser(self,sel,username)
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
            users.DeleteUser(self,sel,username)
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

class TestCase_EditUserProfile(unittest.TestCase):
# Open the desired browser and set up the test
    def setUp(self):
        self.verificationErrors = []
        self.selenium = selenium("localhost", testvars.MCTestVariables["Port"], testvars.MCTestVariables["Browser"], testvars.MCTestVariables["TestSite"])
        self.selenium.start()
# The user actions executed in the test scenario
    # The user actions executed in the test scenario
    def test_EditUserProfile(self):
        sel = self.selenium
        # Log in as Admin
        loginlogout.LogInAsAdmin(self,sel)
        # This is information for edit user profile
        name = "Vit"
        username = "vitalii"
        password = "123456"
        location = "BC"
        website = "http://www.google.ca"
        description = "Miro"
        email = "netvetal@ua.fm"
        # To select User role type "0"
        # To select Admin role type "1"
        role = "0"
        if users.UserRow(self,sel,username)!=0:
            print "Duplicate user found. Deleting it..."
            # This function delete user
            users.DeleteUser(self,sel,username)
            print "User deleted: "+username
        # This function add user
        users.AddUser(self,sel,username,email,role,password)
        print "Logging out..."
        time.sleep(2)
        loginlogout.LogOut(self,sel)
        print "Log in as created user"
        loginlogout.LogInBasic(self,sel,username,password)
        print "Starting edit profile "+username
        users.EditUserProfile(self,sel,name,username,email,location,website,description)
        users.ViewUserCheek(self,sel,username,name,location,website,description)
# Close the browser, log errors, perform cleanup   
    def tearDown(self):
        self.selenium.stop()
# the command on the previous line should close the browser
        self.assertEqual([], self.verificationErrors)

class TestCase_ViewProfile(unittest.TestCase):
# Open the desired browser and set up the test
    def setUp(self):
        self.verificationErrors = []
        self.selenium = selenium("localhost", testvars.MCTestVariables["Port"], testvars.MCTestVariables["Browser"], testvars.MCTestVariables["TestSite"])
        self.selenium.start()
# The user actions executed in the test scenario
    def test_ViewProfile(self):
        sel = self.selenium
        # Log in as Admin
        loginlogout.LogInAsAdmin(self,sel)
        username = "xadmin"
        name = "Vitalii"
        description = "Miro"
        location = "BC"
        website = "www.google.ca"
        # Cheek profile edited successful
        users.ViewProfile(self,sel)
        print "Cheeking profile"
        users.ViewUserCheek(self,sel,username,name,location,website,description)
# Close the browser, log errors, perform cleanup   
    def tearDown(self):
        self.selenium.stop()
# the command on the previous line should close the browser
        self.assertEqual([], self.verificationErrors)

class TestCase_ViewUser(unittest.TestCase):
# Open the desired browser and set up the test
    def setUp(self):
        self.verificationErrors = []
        self.selenium = selenium("localhost", testvars.MCTestVariables["Port"], testvars.MCTestVariables["Browser"], testvars.MCTestVariables["TestSite"])
        self.selenium.start()
# The user actions executed in the test scenario
    def test_ViewUser(self):
        sel = self.selenium
        # Log in as Admin
        loginlogout.LogInAsAdmin(self,sel)
        # This is information for add user edit fields
        username = "vitalii1"
        password = "123456"
        name = ""
        email = "netvetal@ua.fm"
        website = ""
        description = ""
        location = ""
        # To select User role type "0"
        # To select Admin role type "1"
        role = "1" 
        # This function returns the row number for the desired username
        # on /users page.
        # Returns row number if the us username is found and 0 otherwise.
        if users.UserRow(self,sel,username)!=0:
            print "User finded, view user"
            # This function view user
            users.ViewUser(self,sel,username)
            users.ViewUserCheek(self,sel,username,name,location,website,description)
        else:
            # This function add user
            users.AddUser(self,sel,username,email,role,password)
            users.ViewUser(self,sel,username)
            users.ViewUserCheek(self,sel,username,name,location,website,description)
            # Check view user
        time.sleep(3)
        # Close the browser, log errors, perform cleanup   
    def tearDown(self):
        self.selenium.stop()
# the command on the previous line should close the browser
        self.assertEqual([], self.verificationErrors)
