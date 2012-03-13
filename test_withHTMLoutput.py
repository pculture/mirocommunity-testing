# -*- coding: utf-8 -*-
from selenium import selenium
#import system emodules
import unittest, time, re, os, shutil
import litmusresult
import StringIO
import sys
import HTMLTestRunner
# import MC Test Suite modules
import loginlogout, sitesettings, testvars
import testcases_users, testcases_customize, testcases_categories, testcases_manage, testcases_bulkedit, testcases_queue, testcases_comments, testcases_submit
import testcases_login

#================================
from optparse import OptionParser
parser = OptionParser()
parser.add_option("-s", "--sauce", action="store_true", dest="sauce",
                  help='Runs the test on saucelabs.com using specified browser')
parser.add_option("-b", "--browser", action="store",
                  choices=('firefox','chrome','opera', 'safari', 'iexplore', 'googlechrome'),type="choice",
                  dest="browser", default="firefox",
                  help='Possible browser choices: firefox,chrome,opera, safari, iexplore, googlechrome'
                  )

parser.add_option("-p", "--port", action="store", type="int", dest="port")
parser.add_option("-l", "--litmus",action="store_true",dest="litmus",
                  help='Sends test output directly to litmus.pculture.org')
parser.add_option("-i", "--buildid", action="store", dest="buildid",
                  default=time.strftime("%Y%m%d", time.gmtime()) + "99",
                  help="specify the build id of the litmus testrun results to display there")

(options, args) = parser.parse_args()
testbrowser = options.browser
testport = options.port
testsauce = options.sauce
#testsite = options.site
testbuildid = options.buildid
testlitmus = options.litmus

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
#-LOGIN-------------------------------------------------------------------------------------------------------
            unittest.defaultTestLoader.loadTestsFromTestCase(testcases_login.TestCase_LoginWithFacebookAccount_596),
            unittest.defaultTestLoader.loadTestsFromTestCase(testcases_login.TestCase_LoginWithTwitterAccount_597),
            unittest.defaultTestLoader.loadTestsFromTestCase(testcases_login.TestCase_LoginWithOpenIDAccount_598),
            unittest.defaultTestLoader.loadTestsFromTestCase(testcases_login.TestCase_LoginWithGoogleAccount_599),
            unittest.defaultTestLoader.loadTestsFromTestCase(testcases_login.TestCase_SignUpAndLogin_600),
#-USERS-------------------------------------------------------------------------------------------------------
            unittest.defaultTestLoader.loadTestsFromTestCase(testcases_users.TestCase_AddNewAdmin_271),
            unittest.defaultTestLoader.loadTestsFromTestCase(testcases_users.TestCase_AddNewUser_270),
            unittest.defaultTestLoader.loadTestsFromTestCase(testcases_users.TestCase_EditUser_291),
            unittest.defaultTestLoader.loadTestsFromTestCase(testcases_users.TestCase_DeleteUser_272),
            unittest.defaultTestLoader.loadTestsFromTestCase(testcases_users.TestCase_CreateNewUserUsernameAndPassword_280),
            unittest.defaultTestLoader.loadTestsFromTestCase(testcases_users.TestCase_CreateNewUserWithoutUsername_274),
# bug        unittest.defaultTestLoader.loadTestsFromTestCase(testcases_users.TestCase_CreateNewUserWithoutPassword_273),
            unittest.defaultTestLoader.loadTestsFromTestCase(testcases_users.TestCase_UsernameDoesntAcceptMax1Chars_283),
            unittest.defaultTestLoader.loadTestsFromTestCase(testcases_users.TestCase_NewUserUsernameMaxMax2MinChars_281),
            unittest.defaultTestLoader.loadTestsFromTestCase(testcases_users.TestCase_EditUserProfile_539),
            unittest.defaultTestLoader.loadTestsFromTestCase(testcases_users.TestCase_ViewProfile_540),
            unittest.defaultTestLoader.loadTestsFromTestCase(testcases_users.TestCase_ViewUser_290),
#-SITE-SETTINGS-----------------------------------------------------------------------------------------------
            unittest.defaultTestLoader.loadTestsFromTestCase(testcases_customize.TestCase_EditSiteTitle_303),
            unittest.defaultTestLoader.loadTestsFromTestCase(testcases_customize.TestCase_MaxLengthSiteTitle_304),
            unittest.defaultTestLoader.loadTestsFromTestCase(testcases_customize.TestCase_EditSiteTagline_305),
            unittest.defaultTestLoader.loadTestsFromTestCase(testcases_customize.TestCase_MaxLengthSiteTagline_306),
            unittest.defaultTestLoader.loadTestsFromTestCase(testcases_customize.TestCase_EditAboutUs_307),
            unittest.defaultTestLoader.loadTestsFromTestCase(testcases_customize.TestCase_AboutUsHTML_309),
#            unittest.defaultTestLoader.loadTestsFromTestCase(testcases_customize.TestCase_ChangeSiteSettings_303),
            unittest.defaultTestLoader.loadTestsFromTestCase(testcases_customize.TestCase_ChangeOrganization_253),
            unittest.defaultTestLoader.loadTestsFromTestCase(testcases_customize.TestCase_UploadLogo_243),
            unittest.defaultTestLoader.loadTestsFromTestCase(testcases_customize.TestCase_UploadBackground_244),
            unittest.defaultTestLoader.loadTestsFromTestCase(testcases_customize.TestCase_DeleteBackground_245),
            unittest.defaultTestLoader.loadTestsFromTestCase(testcases_customize.TestCase_AddCustomCSS_251),
            unittest.defaultTestLoader.loadTestsFromTestCase(testcases_customize.TestCase_DisplaySubmitVideo_249),
            unittest.defaultTestLoader.loadTestsFromTestCase(testcases_customize.TestCase_CheckRequireLoginToSubmitVideo_250),
#-CATEGORIES--------------------------------------------------------------------------------------------------
            unittest.defaultTestLoader.loadTestsFromTestCase(testcases_categories.TestCase_DeleteAllCategories),
            unittest.defaultTestLoader.loadTestsFromTestCase(testcases_categories.TestCase_AddCategories_296),
            unittest.defaultTestLoader.loadTestsFromTestCase(testcases_categories.TestCase_AddSubCategories_297),
            unittest.defaultTestLoader.loadTestsFromTestCase(testcases_categories.TestCase_AddNonASCIICategories_477),
# bug           unittest.defaultTestLoader.loadTestsFromTestCase(testcases_categories.TestCase_AddDuplicateCategory_478),
            unittest.defaultTestLoader.loadTestsFromTestCase(testcases_categories.TestCase_EditCategory_299),
            unittest.defaultTestLoader.loadTestsFromTestCase(testcases_categories.TestCase_DeleteSingleCategory_298),
            unittest.defaultTestLoader.loadTestsFromTestCase(testcases_categories.TestCase_BulkDeleteCategories_301),
#-MANAGE-SOURCES------------------------------------------------------------------------------------------
            unittest.defaultTestLoader.loadTestsFromTestCase(testcases_manage.TestCase_AddSourceFeed_257),
            unittest.defaultTestLoader.loadTestsFromTestCase(testcases_manage.TestCase_AddDuplicateFeed_258),
            unittest.defaultTestLoader.loadTestsFromTestCase(testcases_manage.TestCase_AddSourceWithDuplicateVideos_259),
            unittest.defaultTestLoader.loadTestsFromTestCase(testcases_manage.TestCase_EditSource_479),
            unittest.defaultTestLoader.loadTestsFromTestCase(testcases_manage.TestCase_BulkEditSources_264),
            unittest.defaultTestLoader.loadTestsFromTestCase(testcases_manage.TestCase_BulkDeleteSources_265),
            unittest.defaultTestLoader.loadTestsFromTestCase(testcases_manage.TestCase_SearchForVideos_260),
            unittest.defaultTestLoader.loadTestsFromTestCase(testcases_manage.TestCase_SearchVideoByNonASCIITerm_261),
            unittest.defaultTestLoader.loadTestsFromTestCase(testcases_manage.TestCase_AddSearchFeed_262),
            unittest.defaultTestLoader.loadTestsFromTestCase(testcases_manage.TestCase_SortSources_266),
            unittest.defaultTestLoader.loadTestsFromTestCase(testcases_manage.TestCase_SearchInSources_267),
            unittest.defaultTestLoader.loadTestsFromTestCase(testcases_manage.TestCase_FilterSources_268),
#-REVIEW-QUEUE---------------------------------------------------
            unittest.defaultTestLoader.loadTestsFromTestCase(testcases_queue.TestCase_ApproveVideo_480),
            unittest.defaultTestLoader.loadTestsFromTestCase(testcases_queue.TestCase_FeatureVideo_481),
            unittest.defaultTestLoader.loadTestsFromTestCase(testcases_queue.TestCase_RejectVideo_482),
            unittest.defaultTestLoader.loadTestsFromTestCase(testcases_queue.TestCase_ApprovePage_483),
            unittest.defaultTestLoader.loadTestsFromTestCase(testcases_queue.TestCase_RejectPage_484),
            unittest.defaultTestLoader.loadTestsFromTestCase(testcases_queue.TestCase_EditVideoInQueue_512),
# bug            unittest.defaultTestLoader.loadTestsFromTestCase(testcases_queue.TestCase_RSSVideosAwaitingModeration_513),
            unittest.defaultTestLoader.loadTestsFromTestCase(testcases_queue.TestCase_ClearQueue_511),
#-BULK-EDIT------------------------------------------------------
            unittest.defaultTestLoader.loadTestsFromTestCase(testcases_bulkedit.testcase_BulkEdit_BulkEdit_446),
            unittest.defaultTestLoader.loadTestsFromTestCase(testcases_bulkedit.testcase_BulkEdit_BulkDelete_447),
            unittest.defaultTestLoader.loadTestsFromTestCase(testcases_bulkedit.testcase_BulkEdit_BulkFeature_448),
            unittest.defaultTestLoader.loadTestsFromTestCase(testcases_bulkedit.testcase_BulkEdit_BulkUnfeature_449),
            unittest.defaultTestLoader.loadTestsFromTestCase(testcases_bulkedit.testcase_BulkEdit_EditSingleVideo_452),
            unittest.defaultTestLoader.loadTestsFromTestCase(testcases_bulkedit.testcase_BulkEdit_DeleteSingleVideo_453),
            unittest.defaultTestLoader.loadTestsFromTestCase(testcases_bulkedit.testcase_BulkEdit_UnapproveCurrent_450),
            unittest.defaultTestLoader.loadTestsFromTestCase(testcases_bulkedit.testcase_BulkEdit_UnapproveFeatured_451),
            unittest.defaultTestLoader.loadTestsFromTestCase(testcases_bulkedit.testcase_BulkEdit_SortByTitle_454),
            unittest.defaultTestLoader.loadTestsFromTestCase(testcases_bulkedit.testcase_BulkEdit_SortBySource_455),
            unittest.defaultTestLoader.loadTestsFromTestCase(testcases_bulkedit.testcase_BulkEdit_SortByDatePublished_456),
            unittest.defaultTestLoader.loadTestsFromTestCase(testcases_bulkedit.testcase_BulkEdit_SortByDateImported_457),
#-SUBMIT-VIDEO---------------------------------------------------
            unittest.defaultTestLoader.loadTestsFromTestCase(testcases_submit.TestCase_SubmitVideoAsAdmin_471),
            unittest.defaultTestLoader.loadTestsFromTestCase(testcases_submit.TestCase_SubmitVideoAsLoggedUser_472),
            unittest.defaultTestLoader.loadTestsFromTestCase(testcases_submit.TestCase_SubmitVideoAsUnloggedUser_473),
            unittest.defaultTestLoader.loadTestsFromTestCase(testcases_submit.TestCase_SubmitVideoFromAdminPage_474),
            unittest.defaultTestLoader.loadTestsFromTestCase(testcases_submit.TestCase_SubmitDuplicateVideo_475),
            unittest.defaultTestLoader.loadTestsFromTestCase(testcases_submit.TestCase_SubmitVideoWithEmbedCode_476),
#-VIDEOPAGE---------------------------------------------------
            unittest.defaultTestLoader.loadTestsFromTestCase(testcases_videopage.TestCase_FeatureVideo_566),
            unittest.defaultTestLoader.loadTestsFromTestCase(testcases_videopage.TestCase_UnfeatureVideo_567),
            unittest.defaultTestLoader.loadTestsFromTestCase(testcases_videopage.TestCase_RejectVideo_568),
            unittest.defaultTestLoader.loadTestsFromTestCase(testcases_videopage.TestCase_ApproveVideo_569),
            unittest.defaultTestLoader.loadTestsFromTestCase(testcases_videopage.TestCase_UpdateThumbnail_570),
            unittest.defaultTestLoader.loadTestsFromTestCase(testcases_videopage.TestCase_EditTitleInline_571),
            unittest.defaultTestLoader.loadTestsFromTestCase(testcases_videopage.TestCase_EditPublicationDate_572),
            unittest.defaultTestLoader.loadTestsFromTestCase(testcases_videopage.TestCase_EditAuthor_573),
            unittest.defaultTestLoader.loadTestsFromTestCase(testcases_videopage.TestCase_EditDescription_574),
            unittest.defaultTestLoader.loadTestsFromTestCase(testcases_videopage.TestCase_EditCategory_575),
            unittest.defaultTestLoader.loadTestsFromTestCase(testcases_videopage.TestCase_EditTags_576),
            unittest.defaultTestLoader.loadTestsFromTestCase(testcases_videopage.TestCase_EditWebsite_577),
            unittest.defaultTestLoader.loadTestsFromTestCase(testcases_videopage.TestCase_AddEditorsComment_578),
            unittest.defaultTestLoader.loadTestsFromTestCase(testcases_videopage.TestCase_PostToFacebook_579),
            unittest.defaultTestLoader.loadTestsFromTestCase(testcases_videopage.TestCase_PostToTwitter_580),
            unittest.defaultTestLoader.loadTestsFromTestCase(testcases_videopage.TestCase_EmailToFriends_581),
            unittest.defaultTestLoader.loadTestsFromTestCase(testcases_videopage.TestCase_AddToPlaylist_582),
            unittest.defaultTestLoader.loadTestsFromTestCase(testcases_videopage.TestCase_DeleteComment_583),
#-RESTORE-CATEGORIES---------------------------------------------
            unittest.defaultTestLoader.loadTestsFromTestCase(testcases_categories.TestCase_RestoreAllCategories),
#-COMMENTS-------------------------------------------------------
            unittest.defaultTestLoader.loadTestsFromTestCase(testcases_comments.testcase_Comments_NoModeration_NoLogin_254),
            unittest.defaultTestLoader.loadTestsFromTestCase(testcases_comments.testcase_Comments_NoModeration_LoginRequired_256),
            unittest.defaultTestLoader.loadTestsFromTestCase(testcases_comments.testcase_Comments_ModerationRequired_NoLogin_541),
            unittest.defaultTestLoader.loadTestsFromTestCase(testcases_comments.testcase_Comments_ModerationRequired_LoginRequired_542),
#-PLAYLISTS------------------------------------------------------
            unittest.defaultTestLoader.loadTestsFromTestCase(testcases_playlists.TestCase_DisablePlaylists_550),
            unittest.defaultTestLoader.loadTestsFromTestCase(testcases_playlists.TestCase_EnablePlaylistsForAdmins_551),
            unittest.defaultTestLoader.loadTestsFromTestCase(testcases_playlists.TestCase_EnablePlaylistsForEveryone_552),
            ])

        # Invoke TestRunner
        # Post the output directly to Litmus
        if testlitmus == True:
            buf = StringIO.StringIO()
            runner = unittest.TextTestRunner(stream=buf)
            for x in self.suite:
                runner.run(x)
                # check out the output
                byte_output = buf.getvalue()
                id_string = str(x)
                stat = byte_output[0]
                try:
                    litmusresult.write_log(id_string,stat,testbuildid,byte_output)
                    litmusresult.send_result()
                finally:
                    buf.truncate(0)

        else: # Post results to HTML page
            buf = StringIO.StringIO()
            runner = HTMLTestRunner.HTMLTestRunner(
                        stream=buf,
                        title='Miro Community Test Suite',
                        description='Results of test run'
                        )
            runner.run(self.suite)

            # check out the output
            byte_output = buf.getvalue()
            # output the main test results
            filename=os.path.join(testvars.MCTestVariables["ResultOutputDirectory"],'MC_test_results_'+time.strftime("%d-%m-%Y_%H-%M", time.gmtime())+'_GMT.html')
            f = open(filename, 'w')
            f.write(byte_output)
            f.close()
            # copy the results to a file called last_run.html
            lastrun = os.path.join(testvars.MCTestVariables["ResultOutputDirectory"],'last_run.html')
            shutil.copyfile(filename,lastrun)
        
##############################################################################
# Executing this module from the command line
##############################################################################

import unittest
if __name__ == "__main__":
#    if len(sys.argv) > 1:
#        argv = sys.argv
#    else:
    argv=['test_HTMLTestRunner.py', 'Test_HTMLTestRunner']
    theme=1
    unittest.main(argv=argv)
    #HTMLTestRunner.main(argv=argv)

