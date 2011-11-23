# Module PLAYLISTS.PY
# includes:
#   * subroutine VerifyPlaylistsPageIsDisabled(self,sel) - verifies that Playlists page
#                has been disabled for the current user
#   * subroutine VerifyPlaylistsPageIsEnabled(self,sel) - verifies that Playlists page
#                has been enabled for the current user


from selenium import selenium

import unittest, time, re, platform, os
import testvars, loginlogout, mclib


# =======================================
# =  VERIFY PLAYLISTS PAGE IS DISABLED  =
# =======================================

# This subroutine verifies that Playlists page has been disabled for the current user

def VerifyPlaylistsPageIsDisabled(self,sel):
    sel.open(testvars.MCTestVariables["PlaylistsPage"])
    sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])
    if sel.is_text_present("Page not found")==False:
        mclib.AppendErrorMessage(self,sel,"Playlists page has not been disabled properly - does not return 404 Error")
        print sel.get_html_source()
    else:
        print "OK - page disabled, test passed"



# =======================================
# =  VERIFY PLAYLISTS PAGE IS ENABLED  =
# =======================================

# This subroutine verifies that Playlists page has been enabled for the current user

def VerifyPlaylistsPageIsEnabled(self,sel):
    sel.open(testvars.MCTestVariables["PlaylistsPage"])
    sel.wait_for_page_to_load(testvars.MCTestVariables["TimeOut"])
    if sel.is_text_present("Page not found"):
        mclib.AppendErrorMessage(self,sel,"Playlists page has not been enabled properly - 404 Error")
    elif sel.is_text_present("Goodies | Playlists")==False:
        mclib.AppendErrorMessage(self,sel,"Unexpected page found")
        print sel.get_html_source()
    else:
        print "OK - page enabled, test passed"
