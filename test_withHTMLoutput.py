# -*- coding: utf-8 -*-
from selenium import selenium
#import system modules
import unittest, time, re
import StringIO
import sys
import HTMLTestRunner
# import MC Test Suite modules
import loginlogout, sitesettings, testvars
import testcases_customize, testcases_categories, testcases_manage, testcases_comments

# ------------------------------------------------------------------------
# This is the main test 

class Test_HTMLTestRunner(unittest.TestCase):

# Open the desired browser and set up the test

    def test0(self):
        self.suite = unittest.TestSuite()
        buf = StringIO.StringIO()
        runner = HTMLTestRunner.HTMLTestRunner(buf)
        runner.run(self.suite)
        # didn't blow up? ok.
        self.assert_('</html>' in buf.getvalue())

    def test_main(self):
        # Run HTMLTestRunner. 

        # suite of TestCases
        self.suite = unittest.TestSuite()
        self.suite.addTests([
            unittest.defaultTestLoader.loadTestsFromTestCase(testcases_customize.TestCase_ChangeSiteSettings),
            unittest.defaultTestLoader.loadTestsFromTestCase(testcases_customize.TestCase_ChangeOrganization),
            unittest.defaultTestLoader.loadTestsFromTestCase(testcases_customize.TestCase_UploadLogo),
            unittest.defaultTestLoader.loadTestsFromTestCase(testcases_customize.TestCase_UploadBackground),
            unittest.defaultTestLoader.loadTestsFromTestCase(testcases_customize.TestCase_DeleteBackground),
            unittest.defaultTestLoader.loadTestsFromTestCase(testcases_customize.TestCase_AddCustomCSS),
            unittest.defaultTestLoader.loadTestsFromTestCase(testcases_customize.TestCase_DisplaySubmitVideo),
#-------------------------------------------------------------------------------------------------------------
            unittest.defaultTestLoader.loadTestsFromTestCase(testcases_categories.TestCase_DeleteAllCategories),
            unittest.defaultTestLoader.loadTestsFromTestCase(testcases_categories.TestCase_AddCategories),
            unittest.defaultTestLoader.loadTestsFromTestCase(testcases_categories.TestCase_AddSubCategories),
            unittest.defaultTestLoader.loadTestsFromTestCase(testcases_categories.TestCase_AddNonASCIICategories),
            unittest.defaultTestLoader.loadTestsFromTestCase(testcases_categories.TestCase_AddDuplicateCategory),
            unittest.defaultTestLoader.loadTestsFromTestCase(testcases_categories.TestCase_EditCategory),
            unittest.defaultTestLoader.loadTestsFromTestCase(testcases_categories.TestCase_BulkDeleteCategories),
# --------------------------------------------------------------------------------------------------------
            unittest.defaultTestLoader.loadTestsFromTestCase(testcases_manage.TestCase_AddSourceFeed),
            unittest.defaultTestLoader.loadTestsFromTestCase(testcases_manage.TestCase_AddDuplicateFeed),
            unittest.defaultTestLoader.loadTestsFromTestCase(testcases_manage.TestCase_AddSourceWithDuplicateVideos),
            unittest.defaultTestLoader.loadTestsFromTestCase(testcases_manage.TestCase_EditSource),
            unittest.defaultTestLoader.loadTestsFromTestCase(testcases_manage.TestCase_BulkEditSources),
            unittest.defaultTestLoader.loadTestsFromTestCase(testcases_manage.TestCase_BulkDeleteSources),
            unittest.defaultTestLoader.loadTestsFromTestCase(testcases_manage.TestCase_SearchForVideos),
            unittest.defaultTestLoader.loadTestsFromTestCase(testcases_manage.TestCase_SearchVideoByNonASCIITerm),
            unittest.defaultTestLoader.loadTestsFromTestCase(testcases_manage.TestCase_AddSearchFeed),
            unittest.defaultTestLoader.loadTestsFromTestCase(testcases_manage.TestCase_SortSources),
            unittest.defaultTestLoader.loadTestsFromTestCase(testcases_manage.TestCase_SearchInSources),
            unittest.defaultTestLoader.loadTestsFromTestCase(testcases_manage.TestCase_FilterSources),
#----------------------------------------------------------------
            unittest.defaultTestLoader.loadTestsFromTestCase(testcases_categories.TestCase_RestoreAllCategories),
#----------------------------------------------------------------
            unittest.defaultTestLoader.loadTestsFromTestCase(testcases_comments.testcase_Comments_NoModeration_NoLogin),
            unittest.defaultTestLoader.loadTestsFromTestCase(testcases_comments.testcase_Comments_NoModeration_LoginRequired),
            unittest.defaultTestLoader.loadTestsFromTestCase(testcases_comments.testcase_Comments_ModerationRequired_NoLogin),
            unittest.defaultTestLoader.loadTestsFromTestCase(testcases_comments.testcase_Comments_ModerationRequired_LoginRequired),
            ])

        # Invoke TestRunner
        buf = StringIO.StringIO()
        #runner = unittest.TextTestRunner(buf)       #DEBUG: this is the unittest baseline
        runner = HTMLTestRunner.HTMLTestRunner(
                    stream=buf,
                    title='Miro Community Test Suite',
                    description='Results of test run'
                    )
        runner.run(self.suite)

        # check out the output
        byte_output = buf.getvalue()
        # output the main test results
        filename=testvars.MCTestVariables["ResultOutputDirectory"]+'MC_test_results_'+time.strftime("%d-%m-%Y_%H-%M", time.gmtime())+'_GMT.html'
        f = open(filename, 'w')
        f.write(byte_output)
        f.close()

##############################################################################
# Executing this module from the command line
##############################################################################

import unittest
if __name__ == "__main__":
    if len(sys.argv) > 1:
        argv = sys.argv
    else:
        argv=['test_HTMLTestRunner.py', 'Test_HTMLTestRunner']
    theme=1
    unittest.main(argv=argv)
    #HTMLTestRunner.main(argv=argv)

