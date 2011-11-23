#=======================================================================
#
#                              PLAYLIST TESTS
#
#=======================================================================
#
# Includes the following test cases:
#     1. TestCase_DisablePlaylists_550
#     2. TestCase_EnablePlaylistsForAdmins_551
#     2. TestCase_EnablePlaylistsForEveryone_552



from selenium import selenium
import imaplib
import unittest, os, time, re, mclib, testcase_base
import loginlogout, sitesettings, testvars, categories, submitvideos, queue, videopage, playlists
import sys

# ----------------------------------------------------------------------

class TestCase_DisablePlaylists_550(testcase_base.testcase_BaseTestCase):
    
    def test_DisablePlaylists(self):
        sel = self.selenium
#       Log in as Admin
        loginlogout.LogInAsAdmin(self,sel)
        print "Starting test..."
        sitesettings.EnablePlaylists(self,sel,"No")
        print "Going to check if Playlists page is available..."
        print "=== For ADMIN:"
        playlists.VerifyPlaylistsPageIsDisabled(self,sel)
        print "=== For USER:"
        loginlogout.LogOut(self,sel)
        loginlogout.LogInAsUser(self,sel)
        playlists.VerifyPlaylistsPageIsDisabled(self,sel)
        print "=== For ANONYMOUS USER:"
        loginlogout.LogOut(self,sel)
        playlists.VerifyPlaylistsPageIsDisabled(self,sel)
        

class TestCase_EnablePlaylistsForAdmins_551(testcase_base.testcase_BaseTestCase):
    
    def test_EnablePlaylistsForAdmins(self):
        sel = self.selenium
#       Log in as Admin
        loginlogout.LogInAsAdmin(self,sel)
        print "Starting test..."
        sitesettings.EnablePlaylists(self,sel,"Admins Only")
        print "Going to check if Playlists page is available..."
        print "=== For ADMIN:"
        playlists.VerifyPlaylistsPageIsEnabled(self,sel)
        print "=== For USER:"
        loginlogout.LogOut(self,sel)
        loginlogout.LogInAsUser(self,sel)
        playlists.VerifyPlaylistsPageIsDisabled(self,sel)
        print "=== For ANONYMOUS USER:"
        loginlogout.LogOut(self,sel)
        playlists.VerifyPlaylistsPageIsDisabled(self,sel)


class TestCase_EnablePlaylistsForEveryone_552(testcase_base.testcase_BaseTestCase):
    
    def test_EnablePlaylistsForEveryone(self):
        sel = self.selenium
#       Log in as Admin
        loginlogout.LogInAsAdmin(self,sel)
        print "Starting test..."
        sitesettings.EnablePlaylists(self,sel,"Yes")
        print "Going to check if Playlists page is available..."
        print "=== For ADMIN:"
        playlists.VerifyPlaylistsPageIsEnabled(self,sel)
        print "=== For USER:"
        loginlogout.LogOut(self,sel)
        loginlogout.LogInAsUser(self,sel)
        playlists.VerifyPlaylistsPageIsEnabled(self,sel)
        print "=== For ANONYMOUS USER:"
        loginlogout.LogOut(self,sel)
        sel.open(testvars.MCTestVariables["PlaylistsPage"])
        sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])
        if sel.is_text_present("Login/Sign Up")==False:
            mclib.AppendErrorMessage(self,sel,"Anonymous user is not required to log in")
            print sel.get_html_source()
        else:
            print "OK - anonymous user is prompted to log in to view the playlist, test passed"
