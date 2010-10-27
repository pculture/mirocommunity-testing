# Module CATEGORIES.PY
# includes:
#   * function CategoryRow(self,sel,cat) - returns the row in the table on /admin/categories
#                where the desired category (Cat) is placed and zero if <cat> not found
#   * function GetCategoryList(self,sel) - returns the list of all the categories in the list
#                of categories
#   * function GetFullCategoryData(self,sel) - returns the full data on all the categories
#                (name,slug,description)
#   * subroutine AddCategory(self,sel,cat,slug,description,sub,parent) - adds a category <cat>
#                with slug <slug> (optional), description <description> (optional),
#                sub = 1/0 - subcategory/top-level category, parent - name of parent category
#   * subroutine AddDuplicateCategory(self,sel,cat,slug) - attempts to add a duplicate category
#                to the list.
#                cat - category name (mandatory)
#                slug - category slug, string, optional
#   * subroutine BulkDeleteCategories(self,sel,categoryList) - deletes categories from the
#                categoryList via bulk action
#   * subroutine DeleteAllCategories(self,sel) - deletes all categories
#   * subroutine DeleteCategory(self,sel,cat) - deletes a selected category from the list
#   * subroutine EditCategory(self,sel,cat,newname,newslug,newdescription,newlogo) - updates 
#                an existing category <cat> with new data: <newname>, <newslug>, <newdescription>,
#                <newlogo>(all optional)
#   * subroutine RestoreAllCategoriesFromBackup(self,sel,categoriesList) - restores all the
#                categories from full backup <categoriesList>


from selenium import selenium

import unittest, time, re, os
import testvars, mclib

# =======================================
# =      FIND CATEGORY IN THE LIST      =
# =======================================

# This function returns the row number for the desired category
# on /categories page.
# Returns row number if the cat category is found and 0 otherwise.
# For a subcategory, submit the name in u"\u2014<category_name>" format

def CategoryRow(self,sel,cat):
    sel.open(testvars.MCTestVariables["CategoriesPage"])
    category=""
    no=1
    categoryTableCell="//div[@id='labels']/form/table/tbody/tr[1]/td[2]"
    while sel.is_element_present(categoryTableCell):
        category_untrimmed = sel.get_text(categoryTableCell)
        category = category_untrimmed.replace(' Edit | Delete | View','')
        if category==cat:
            break
        no=no+1
        categoryTableCell="//div[@id='labels']/form/table/tbody/tr["+str(no)+"]/td[2]"
    if category==cat:
        return no
    else:
        return 0


# =======================================
# =       REMEMBER ALL CATEGORIES       =
# =======================================

# This function returns all categories (including subcategories) in the list.

def GetCategoryList(self,sel):
    print "Retrieving the current list of categories..."
    sel.open(testvars.MCTestVariables["CategoriesPage"])
    sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])
    categoryList=['']
    no=1
    categoryTableCell="//div[@id='labels']/form/table/tbody/tr[1]/td[2]"
    while sel.is_element_present(categoryTableCell):
        category_untrimmed = sel.get_text(categoryTableCell)
        category = category_untrimmed.replace(' Edit | Delete | View','')
        categoryList.append(category)
        no=no+1
        categoryTableCell="//div[@id='labels']/form/table/tbody/tr["+str(no)+"]/td[2]"
    if no>1:
        categoryList.remove("")
    return categoryList

    
def GetFullCategoryData(self,sel):
    print "Retrieving the current list of categories..."
    sel.open(testvars.MCTestVariables["CategoriesPage"])
    sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])
    categoryList=['']
    no=1
    categoryTableCell="//div[@id='labels']/form/table/tbody/tr[1]/td[2]"
    descriptionTableCell="//div[@id='labels']/form/table/tbody/tr[1]/td[3]"
    slugTableCell="//div[@id='labels']/form/table/tbody/tr[1]/td[4]"
    while sel.is_element_present(categoryTableCell):
        categoryItem=['']
        category_untrimmed = sel.get_text(categoryTableCell)
        category = category_untrimmed.replace(' Edit | Delete | View','')
        description = sel.get_text(descriptionTableCell)
        slug = sel.get_text(slugTableCell)
        categoryItem.append(category)
        categoryItem.append(description)
        categoryItem.append(slug)
        categoryItem.remove("")
        categoryList.append(categoryItem)
        no=no+1
        categoryTableCell="//div[@id='labels']/form/table/tbody/tr["+str(no)+"]/td[2]"
        descriptionTableCell="//div[@id='labels']/form/table/tbody/tr["+str(no)+"]/td[3]"
        slugTableCell="//div[@id='labels']/form/table/tbody/tr["+str(no)+"]/td[4]"
    if no>1:
        categoryList.remove("")
    return categoryList




# =======================================
# =             ADD CATEGORY            =
# =======================================

# This procedure adds a new category (or subcategory) to the list.
#     cat - category name (mandatory)
#     slug - category slug, string, optional
#     description - category description, string, optional
#     sub - whether or not category has a parent category (mandatory)
#           sub=1 - subcategory
#           sub=0 - top-level category
#     parent - the name of the parent category,
#              string, optional, ignored if sub==0 

def AddCategory(self,sel,cat,slug,description,sub,parent):
    #Check if the parent category is available
    if (sub==1) and (parent!=""):
        if CategoryRow(self,sel,parent)==0:
            print parent+" category not found. Cannot create subcategory "+cat
            return 0
    # If the new category is a subcategory, prepend its name with an em dash in Unicode
    if sub==1:
        testCat=u'\u2014'+cat
    else:
        testCat=cat
    #Check if the category already exists
    if CategoryRow(self,sel,testCat)!=0:
        print testCat+" category already exists. Skipping add category procedure"
        return 0
    else:
        print "Adding a new category "+testCat
        sel.open(testvars.MCTestVariables["CategoriesPage"])
        sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])
        buttonAddCategory = "//div[@id='content']/a/span"
        if sel.is_element_present(buttonAddCategory)==True:
            sel.click(buttonAddCategory)
            time.sleep(3)
            if sel.is_visible("//div[@id='label_sidebar']")==False:
                self.verificationErrors.append("Add category pop-up does not display")
                print testvars.preE+"Add category pop-up does not display"
            else:
                # Enter category name
                if sel.is_element_present("id_name")==True:
                    sel.click("id_name")
                    #sel.type_keys("id_name", cat)
                    sel.type("id_name",cat) #A workaround for a known bug in Selenium, which prevents some
                                            # characters from being typed
                else:
                    self.verificationErrors.append("Edit field for category name not found")
                    print testvars.preE+"Edit field for category name not found"
                # Enter category slug
                if sel.is_element_present("id_slug")==True:
                    if slug!="":
                        testSlug = slug
                    else:
                        testSlug = cat
                    sel.type("id_slug", testSlug)
                else:
                    self.verificationErrors.append("Edit field for category slug not found")
                    print testvars.preE+"Edit field for category slug not found"
                # Enter category description
                if sel.is_element_present("id_description")==True:
                    if description=="":
                        testDescription = "<b>" + cat + "</b> is the description of this item"
                    else:
                        testDescription = description
                    sel.type("id_description", testDescription)
                else:
                    mclib.AppendErrorMessage(self,sel,"Edit field for category description not found")
                    print testvars.preE+"Edit field for category description not found"
                # Check if it is a subcategory; if yes, specify parent
                if sub==1:
                    listCategoryParent="id_parent"
                    if sel.is_element_present(listCategoryParent)==True:
                        sel.select("id_parent", parent)
                    else:
                        self.verificationErrors.append("List of available parent categories not found")
                        print testvars.preE+"List of available parent categories not found"
                # Save changes
                buttonSubmit = "submit"
                if sel.is_element_present(buttonSubmit)==True:
                    sel.click("submit")
                else:
                    mclib.AppendErrorMessage(self,sel,"Save button on Add Category pop-up not found")
        sel.refresh()
        sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])
# Check if the new category is present in the list
        rowNo = CategoryRow(self,sel,testCat)
        if rowNo==0:   # not found
            mclib.AppendErrorMessage(self,sel,testCat+" category was not added to the list")
        else:
            labelDescription = "//div[@id='labels']/form/table/tbody/tr["+str(rowNo)+"]/td[3]"
            labelSlug = "//div[@id='labels']/form/table/tbody/tr["+str(rowNo)+"]/td[4]"
            #Check category description
            if sel.is_element_present(labelDescription)!=True:
                mclib.AppendErrorMessage(self,sel,"Category description not found")
            elif sel.get_text(labelDescription)!=mclib.remove_html_tags(testDescription):
                mclib.AppendErrorMessage(self,sel,"Wrong category description text displayed")
                print "Expected category description: "+mclib.remove_html_tags(testDescription)
                print "- Actual category description: "+sel.get_text(labelDescription)
            #Check category slug
            if sel.is_element_present(labelSlug)!=True:
                mclib.AppendErrorMessage(self,sel,"Category slug not found")
            elif sel.get_text(labelSlug)!=testSlug:
                mclib.AppendErrorMessage(self,sel,"Wrong category slug text displayed")
                print "Expected category slug: "+testSlug
                print "- Actual category slug: "+sel.get_text(labelSlug)
        return 1


# =======================================
# =        ADD DUPLICATE CATEGORY       =
# =======================================

# This procedure attempts to add a duplicate category to the list.
#     cat - category name (mandatory)
#     slug - category slug, string, optional

def AddDuplicateCategory(self,sel,cat,slug):
    #Check if the category already exists
    if CategoryRow(self,sel,cat)==0:
        print cat+" category does not exist. Skipping Addition of a duplicate category"
        return 0
    else:
        print "Adding a duplicate category "+cat
        sel.open(testvars.MCTestVariables["CategoriesPage"])
        sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])
        buttonAddCategory = "//div[@id='content']/a/span"
        if sel.is_element_present(buttonAddCategory)==True:
            sel.click(buttonAddCategory)
            time.sleep(2)
            if sel.is_visible("//div[@id='label_sidebar']")==False:
                mclib.AppendErrorMessage(self,sel,"Add category pop-up does not display")
            else:
                # Enter category name
                if sel.is_element_present("id_name")==True:
                    sel.click("id_name")
                    sel.type("id_name",cat) 
                else:
                    mclib.AppendErrorMessage(self,sel,"Edit field for category name not found")
                # Enter category slug
                if sel.is_element_present("id_slug")==True:
                    if slug!="":
                        testSlug = slug
                    else:
                        testSlug = cat
                    sel.type("id_slug", testSlug)
                else:
                    mclib.AppendErrorMessage(self,sel,"Edit field for category slug not found")
                # Save changes
                buttonSubmit = "submit"
                if sel.is_element_present(buttonSubmit)==False:
                    mclib.AppendErrorMessage(self,sel,"Save button on Add Category pop-up not found")
                else:
                    print "Checking if the appropriate error message is displayed..."
                    sel.click("submit")
                    time.sleep(3)
                    if sel.is_visible("//div[@id='label_sidebar']")==False:
                        mclib.AppendErrorMessage(self,sel,"Add Category pop-up is not visible")
                    elif sel.is_text_present("Category with this name already exists.")==False:
                        mclib.AppendErrorMessage(self,sel,"Error message alerting on category duplication was not found")
                    else:
                        print "OK"
                        


# =======================================
# =        DELETE ALL CATEGORIES        =
# =======================================

# This procedure deletes all the categories from the list.

def DeleteAllCategories(self,sel):
    sel.open(testvars.MCTestVariables["CategoriesPage"])
    sel.click("toggle_all")
    # Applying bulk delete action
    sel.select("action", "label=Delete")
    sel.click("//button[@type='button']")
    sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])
    # Check if all the categories were actually deleted
    if sel.is_element_present("//div[@id='labels']/form/table/tbody/tr[1]/td[2]")==True:
        self.verificationErrors.append("The category list is not empty after total bulk deletion")
        print testvars.preE+"The category list is not empty after total bulk deletion"


# =======================================
# =      DELETE SELECTED CATEGORY       =
# =======================================

# This procedure deletes a selected category from the list.

def DeleteCategory(self,sel,cat):
    catRow = CategoryRow(self, sel,cat)
    if catRow!=0:
        sel.open(testvars.MCTestVariables["CategoriesPage"])
        sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])
        elementDelete = "//div[@id='labels']/form/table/tbody/tr["+str(catRow)+"]/td[2]/div/a[2]"
        print "Deleting category "+cat+"..."
        if sel.is_element_present(elementDelete):
            sel.click(elementDelete)
        else:
            mclib.AppendErrorMessage(self,sel,"Delete link not found for category")
        sel.click("//button[@name='submit' and @value='Save']")
        sel.refresh()
        sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])
        if CategoryRow(self, sel,cat)!=0:
            mclib.AppendErrorMessage(self,sel,"Could not delete category "+cat)
        else:
            print "OK"
    else:
        mclib.AppendErrorMessage(self,sel,"Could not find category "+cat)
    


# =======================================
# =         BULK DELETE CATEGORY        =
# =======================================

# This procedure deletes categories from the list via bulk action.

def BulkDeleteCategories(self,sel,categoryList):
    sel.open(testvars.MCTestVariables["CategoriesPage"])
    print "Starting bulk deletion of multiple categories:"
    print categoryList
    # Get check box numbers to be checked prior to deletion
    numberList = [0]
    for item in categoryList:
        no = CategoryRow(self,sel,item)
        if no>0:
            numberList.append(no)
        else:
            print item+" not found in the list of categories"
    if len(numberList)>1: 
        numberList.remove(0)
        # Checking check boxes
        for item in numberList:
            # Attention! Rows are numbered starting from 1, check boxes - starting from 0
            categoryCheckBox="id_form-" + str(item-1) + "-BULK"
            sel.click(categoryCheckBox)
            print "Checked table row No.: "+str(item)
        # Applying bulk delete action
        sel.select("action", "label=Delete")
        sel.click("//button[@type='button']")
        print "Clicked Delete button"
        sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])
        # Check if the categories were actually deleted
        print "Checking if the categories were actually deleted"
        for item in categoryList:
            if CategoryRow(self,sel,item)!=0:
                self.verificationErrors.append("The following category was not deleted via bulk action: "+item)
                print testvars.preE+"The following category was not deleted via bulk action: "+item
    else:
        print "Could not apply bulk delete - none of requested items were found"


# =======================================
# =          EDIT  CATEGORY             =
# =======================================

# This procedure modifies the parameters of a category

def EditCategory(self,sel,cat,newname,newslug,newdescription,newlogo):
    print "Checking that the source category exists..."
    catRow = CategoryRow(self,sel,cat)
    if catRow==0: # Source category to be edited not found
        print mclib.AppendErrorMessage(self,sel,"Could not find category "+cat)
        print "Current list of categories: "
        print GetCategoryList(self,sel)
    else: # Source category found - now looking for Edit link
        print "OK"
        sel.open(testvars.MCTestVariables["CategoriesPage"])
        print "Looking for the relevant Edit link..."
        elementEdit = "//div[@id='labels']/form/table/tbody/tr["+str(catRow)+"]/td[2]/div/a[1]"
        if sel.is_element_present(elementEdit)==False:
            mclib.AppendErrorMessage(self,sel,"Edit link for category "+cat+" not found")
        else: # Start editing
            print "OK"
            sel.click(elementEdit)
            time.sleep(2)
            if sel.is_visible("//div[@id='labels']/form/table/tbody/tr["+str(catRow)+"]/td[1]/div/h2")==False:
                mclib.AppendErrorMessage(self,sel,"Edit category pop-up does not display")
            else:
                # Enter category name
                categoryField="id_form-"+str(catRow-1)+"-name"
                if sel.is_element_present(categoryField)==True:
                    #sel.click(categoryField)
                    print "Entering new category name: "+newname
                    sel.type(categoryField, newname)
                else:
                    mclib.AppendErrorMessage(self,sel,"Edit field for category name not found")
                # Enter category slug
                slugField="id_form-"+str(catRow-1)+"-slug"
                if sel.is_element_present(slugField)==True:
                    if newslug!="":
                        print "Entering new slug: "+newslug
                        sel.type(slugField, newslug)
                    else:
                        if newname!="":
                            print "Entering new slug: "+newname
                            sel.type(slugField, newname)
                else:
                    mclib.AppendErrorMessage(self,sel,"Edit field for category slug not found")
                # Enter category description
                descriptionField="id_form-"+str(catRow-1)+"-description"
                if sel.is_element_present(descriptionField)==True:
                    if newdescription!="":
                        print "Entering new description: "+newdescription
                        sel.type(descriptionField, newdescription)
                else:
                    mclib.AppendErrorMessage(self,sel,"Edit field for category description not found")
                logoField="id_form-"+str(catRow-1)+"-logo"
                if sel.is_element_present(logoField):
                    if newlogo!="":
                        print "Selecting new logo image file: "+newlogo
                        sel.type(logoField,os.path.join(testvars.MCTestVariables["GraphicFilesDirectory"],newlogo))
                # Now save changes
                print "Saving changes..."
                buttonUpdate="//div[@id='labels']/form/table/tbody/tr["+str(catRow)+"]/td[1]/div/button"
                if sel.is_element_present(buttonUpdate)==False:
                    mclib.AppendErrorMessage(self,sel,"Save Changes button on Edit Category pop-up not found")
                else:
                    sel.click(buttonUpdate)
                    print "OK"
                    sel.refresh()
                    sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])


# =======================================
# = RESTORE ALL CATEGORIES FROM BACKUP  =
# =======================================

# This procedure restores all the categories from full backup <categoriesList>

def RestoreAllCategoriesFromBackup(self,sel,categoriesList):
    print "Preparing to restore categories from the following backup list: "
    print categoriesList
    sel.open(testvars.MCTestVariables["CategoriesPage"])
    for Item in categoriesList:
        oldCategory=Item[0]
        oldDescription=Item[1]
        oldSlug=Item[2]
#        print oldCategory+"  "+oldDescription+"  "+oldSlug
        if oldCategory[0:1]==u"\u2014\u2014":
            Level=2
            newCategory=oldCategory[2:]
        else:
            if oldCategory[0]==u"\u2014":
                Level=1
                newCategory=oldCategory[1:]
            else:    
                Level=0
                newCategory=oldCategory
        newDescription=oldDescription
        newSlug=oldSlug
        print newCategory+"  "+newDescription+"  "+newSlug
        if Level==0: 
            AddCategory(self,sel,newCategory,newSlug,newDescription,0,"")
            Parent0=newCategory
        elif Level==1:
            AddCategory(self,sel,newCategory,newSlug,newDescription,1,Parent0)
            Parent1=newCategory
        elif Level==2:
            AddCategory(self,sel,newCategory,newSlug,newDescription,1,Parent1)
        else:
            pass # Ignoring all categories at level 4 and below
                
    