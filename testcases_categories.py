#=======================================================================
#
#                             CATEGORIES TESTS
#
#=======================================================================
#
# Includes the following test cases:
#     1. TestCase_DeleteAllCategories
#     2. TestCase_AddCategories
#     3. TestCase_AddSubCategories
#     4. TestCase_AddNonASCIICategories
#     5. TestCase_AddDuplicateCategory
#     6. TestCase_EditCategory
#     7. TestCase_BulkDeleteCategories
#     8. TestCase_RestoreAllCategories

from selenium import selenium
import unittest, time, re, mclib, loginlogout, sitesettings, categories, testvars
import sys

# ----------------------------------------------------------------------

class TestCase_DeleteAllCategories(unittest.TestCase):
    
# Open the desired browser and set up the test
    def setUp(self):
        self.verificationErrors = []
        self.selenium = selenium("localhost", testvars.MCTestVariables["Port"], testvars.MCTestVariables["Browser"], testvars.MCTestVariables["TestSite"])
        self.selenium.start()

    def test_DeleteAllCategories(self):
        sel = self.selenium
#       Log in as Admin
        loginlogout.LogInAsAdmin(self,sel)
        # Make a full backup of all the categories existing on the page
        testvars.initialCategories=categories.GetFullCategoryData(self,sel)
        print "Memorized the existing list of categories:"
        print testvars.initialCategories
        categories.DeleteAllCategories(self,sel)
        print "Deleted all the categories"

# Close the browser, log errors, perform cleanup    
    def tearDown(self):
        self.selenium.stop()
# the command on the previous line should close the browser
        self.assertEqual([], self.verificationErrors)



class TestCase_AddCategories(unittest.TestCase):
    
# Open the desired browser and set up the test
    def setUp(self):
        self.verificationErrors = []
        self.selenium = selenium("localhost", testvars.MCTestVariables["Port"], testvars.MCTestVariables["Browser"], testvars.MCTestVariables["TestSite"])
        self.selenium.start()

    def test_AddCategories(self):
        sel = self.selenium
#       Log in as Admin
        loginlogout.LogInAsAdmin(self,sel)
        for item in testvars.newCategories:
            categories.AddCategory(self, sel, item, item, "", 0, "")

# Close the browser, log errors, perform cleanup    
    def tearDown(self):
        self.selenium.stop()
# the command on the previous line should close the browser
        self.assertEqual([], self.verificationErrors)



class TestCase_AddSubCategories(unittest.TestCase):
    
# Open the desired browser and set up the test
    def setUp(self):
        self.verificationErrors = []
        self.selenium = selenium("localhost", testvars.MCTestVariables["Port"], testvars.MCTestVariables["Browser"], testvars.MCTestVariables["TestSite"])
        self.selenium.start()

    def test_AddSubCategories(self):
        sel = self.selenium
#       Log in as Admin
        loginlogout.LogInAsAdmin(self,sel)
        for item in testvars.newSubcategories:
            categories.AddCategory(self, sel, item, item, item+" films", 1, "film")

# Close the browser, log errors, perform cleanup    
    def tearDown(self):
        self.selenium.stop()
# the command on the previous line should close the browser
        self.assertEqual([], self.verificationErrors)


class TestCase_AddNonASCIICategories(unittest.TestCase):
    
# Open the desired browser and set up the test
    def setUp(self):
        self.verificationErrors = []
        self.selenium = selenium("localhost", testvars.MCTestVariables["Port"], testvars.MCTestVariables["Browser"], testvars.MCTestVariables["TestSite"])
        self.selenium.start()

    def test_AddNonASCIICategories(self):
        sel = self.selenium
#       Log in as Admin
        loginlogout.LogInAsAdmin(self,sel)
        for item in testvars.newNonASCIICategories:
            categories.AddCategory(self, sel, item[0], item[1], "", 0, "")

# Close the browser, log errors, perform cleanup    
    def tearDown(self):
        self.selenium.stop()
# the command on the previous line should close the browser
        self.assertEqual([], self.verificationErrors)


class TestCase_AddDuplicateCategory(unittest.TestCase):
    
# Open the desired browser and set up the test
    def setUp(self):
        self.verificationErrors = []
        self.selenium = selenium("localhost", testvars.MCTestVariables["Port"], testvars.MCTestVariables["Browser"], testvars.MCTestVariables["TestSite"])
        self.selenium.start()

# The user actions executed in the test scenario
    def test_AddDuplicateCategory(self):
        sel = self.selenium
#       Log in as Admin
        loginlogout.LogInAsAdmin(self,sel)
        # Attempt to add a duplicate category
        categories.AddDuplicateCategory(self,sel,"art","")

# Close the browser, log errors, perform cleanup    
    def tearDown(self):
        self.selenium.stop()
# the command on the previous line should close the browser
        self.assertEqual([], self.verificationErrors)


class TestCase_EditCategory(unittest.TestCase):
    
# Open the desired browser and set up the test
    def setUp(self):
        self.verificationErrors = []
        self.selenium = selenium("localhost", testvars.MCTestVariables["Port"], testvars.MCTestVariables["Browser"], testvars.MCTestVariables["TestSite"])
        self.selenium.start()

    def test_EditCategory(self):
        sel = self.selenium
#       Log in as Admin
        loginlogout.LogInAsAdmin(self,sel)
        initcat = "food"
        cat = "fish"
        desc = "Fish are food not Friends!"
        print "Updating category: "+initcat
        # Update category
        categories.EditCategory(self,sel,initcat,cat,"",desc,"fish_logo.gif")
        # Check that the category has really been updated
        rowNo = categories.CategoryRow(self,sel,cat)
        if rowNo==0:    # new category name not found
            mclib.AppendErrorMessage(self,sel,"Could not find the new category name in the list of categories")
            print categories.GetCategoryList(self,sel)
        else:
            # Check description in the list of categories
            actualDescription = sel.get_text("//div[@id='labels']/form/table/tbody/tr["+str(rowNo)+"]/td[3]")
            print "Checking category "+cat+" in the list of categories"
            if actualDescription!=desc:
                mclib.AppendErrorMessage(self,sel,"Updated description text is not displayed")
            # Open View Category page
            linkView = "//div[@id='labels']/form/table/tbody/tr["+str(rowNo)+"]/td[2]/div/a[3]"
            print "Checking category page for category: "+cat
            if sel.is_element_present(linkView)==True:
                sel.click(linkView)
                sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])
                # Check category name
                print "Checking category name on category page"
                if sel.is_element_present("//div[@id='category_info']/h1")==True:
                    if sel.get_text("//div[@id='category_info']/h1")!=cat:
                        mclib.AppendErrorMessage(self,sel,"Wrong category name on category page for "+cat)
                else:
                    mclib.AppendErrorMessage(self,sel,"Category text is not displayed on category page for "+cat)
                # Check category description
                print "Checking category description on category page"
                if sel.is_element_present("//div[@id='category_info']/div")==True:
                    if sel.get_text("//div[@id='category_info']/div")!=desc:
                        mclib.AppendErrorMessage(self,sel,"Wrong category description on category page for "+cat)
                else:
                    mclib.AppendErrorMessage(self,sel,"Category description is not displayed on category page for "+cat)
                # Checking category logo
                print "Checking category logo on category page"
                logoText = "//img[contains(@src,'"+testvars.MCTestVariables["CategoriesLogoURL"]+"/"+"fish_logo.gif')]"
                if sel.is_element_present("//div[@id='category_info']/img")==True:
                    if sel.get_text(logoText)!="":
                        mclib.AppendErrorMessage(self,sel,"Wrong logo image on category page for "+cat)
                else:
                    mclib.AppendErrorMessage(self,sel,"Category logo image is not displayed on category page for "+cat)
            else:
                mclib.AppendErrorMessage(self,sel,"View category link is not displayed for "+cat)

# Close the browser, log errors, perform cleanup    
    def tearDown(self):
        self.selenium.stop()
# the command on the previous line should close the browser
        self.assertEqual([], self.verificationErrors)



class TestCase_BulkDeleteCategories(unittest.TestCase):
    
# Open the desired browser and set up the test
    def setUp(self):
        self.verificationErrors = []
        self.selenium = selenium("localhost", testvars.MCTestVariables["Port"], testvars.MCTestVariables["Browser"], testvars.MCTestVariables["TestSite"])
        self.selenium.start()

    def test_BulkDeleteCategories(self):
        sel = self.selenium
#       Log in as Admin
        loginlogout.LogInAsAdmin(self,sel)
        # Delete the three top categories from the list
#        newList = categories.GetCategoryList(self,sel)
        newList = [testvars.newCategories[1],testvars.newCategories[6]]
        print "Deleting the following categories with the use of bulk action:"
#        print newList[1:3]
#        categories.BulkDeleteCategories(self,sel,newList[1:3])
        categories.BulkDeleteCategories(self,sel,newList)

# Close the browser, log errors, perform cleanup    
    def tearDown(self):
        self.selenium.stop()
# the command on the previous line should close the browser
        self.assertEqual([], self.verificationErrors)


class TestCase_RestoreAllCategories(unittest.TestCase):
    
# Open the desired browser and set up the test
    def setUp(self):
        self.verificationErrors = []
        self.selenium = selenium("localhost", testvars.MCTestVariables["Port"], testvars.MCTestVariables["Browser"], testvars.MCTestVariables["TestSite"])
        self.selenium.start()

    def test_RestoreAllCategories(self):
        sel = self.selenium
#       Log in as Admin
        loginlogout.LogInAsAdmin(self,sel)
        # Delete all the remaining test categories 
        categories.DeleteAllCategories(self,sel)
        print "Deleted all the categories"
        # Restore all the initial categories from the backup
        categories.RestoreAllCategoriesFromBackup(self,sel,testvars.initialCategories)
        print "Restoring complete"

# Close the browser, log errors, perform cleanup    
    def tearDown(self):
        self.selenium.stop()
# the command on the previous line should close the browser
        self.assertEqual([], self.verificationErrors)
