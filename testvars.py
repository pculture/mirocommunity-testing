import os

preE="********ERROR: "

global initialCategories
initialCategories = [""]
current_dir = os.getcwd()

MCTestVariables = {"Browser":"*chrome", \
                   "TestSite":"http://dalmatia.mirocommunity.org/", \
                   "ResultOutputDirectory":os.path.join(os.getcwd(), "TestResults"), \
                   "GraphicFilesDirectory":os.path.join(current_dir, "TestInput"), \
                   "TimeOut":"150000", \
                   "AdminLink":"View Admin", \
                   "AdminLogin":"seleniumTestAdmin", \
                   "AdminPassword":"TestAdmin", \
                   "AdminName":"Selene Test-Admin ", \
                   "UserLogin":"seleniumTestUser", \
                   "UserPassword":"selenium", \
                   "UserName":"selene test-user", \
                   "LogoutFootlink":"//ul[@id='footer_links']/li[5]/a", \
                   "FBUsername": "Pat Culture", \
                   "FBLogin":"pculture.qa@gmail.com", \
                   "FBPassword":"TWlyb0NvbW11bml0eQ==", \
                   "TwitterLogin":"PCFQA", \
                   "TwitterPassword":"TWlyb0NvbW11bml0eQ==", \
                   "OpenIDLogin":"PCFQA", \
                   "OpenIDPassword":"TWlyb0NvbW11bml0eQ==", \
                   "TestEmail":"pculture.qa@gmail.com", \
                   "TestEmailPassword":"TWlyb0NvbW11bml0eQ==", \
                   "ListThemeLink":"/admin/themes/set_default/1", \
                   "ScrollingThemeLink":"/admin/themes/set_default/2", \
                   "CategoryThemeLink":"/admin/themes/set_default/3", \
                   "BlueThemeLink":"/admin/themes/set_default/4", \
                   "ViewMainSiteLink":"//div[@id='header']/ul[1]/li/a/span", \
                   "NewVideosListingPage":"/listing/new", \
                   "LoginPage":"/accounts/login/", \
                   "LogoutPage":"/accounts/logout/?next=/", \
                   "FacebookLoginPage":"/accounts/facebook_login/", \
                   "ReviewQueuePage":"/admin/approve_reject", \
                   "ManageSourcesPage":"admin/manage", \
                   "BulkEditPage":"/admin/bulk_edit", \
                   "CategoriesPage":"/admin/categories", \
                   "SettingsPage":"/admin/settings/", \
                   "UserPage":"/admin/users/", \
                   "ProfilePage":"/accounts/profile/", \
                   "PlaylistsPage":"/playlists/", \
                   "ViewAdmin":"//div[@id='header']/a[2]/span", \
                   "ViewAdminBlueTheme":"//div[@id='wrapper']/div[1]/div/ul[2]/li/a/span", \
                   "SaveChanges":"//div[@id='labels']/form/table/tbody/tr[2]/td[1]/div/button", \
                   "EditSaveChanges":"//button[@name='submit' and @value='Save']", \
                   "CategoriesLogoURL":"http://s3.mirocommunity.org.s3.amazonaws.com/dalmatia/localtv/category_logos", \
                   "SiteLogoURL":"http://s3.mirocommunity.org.s3.amazonaws.com/dalmatia/localtv/site_logos", \
                   "SiteBackgroundURL":"http://s3.mirocommunity.org.s3.amazonaws.com/dalmatia/localtv/site_backgrounds", \
                   "MaxSiteTitle":50, \
                   "MaxSiteTagline":250, \
                   "Port":4444, 
                   }

# The following data dictionary contains the references to
# the major user interface controls
# These values can be updated via the following sources:
# Admin buttons (Videos, Settings, Users, Comments)
# https://git.participatoryculture.org/localtv/tree/localtv/templates/localtv/admin/header.html
# Admin|Videos buttons (Review Queue, Manage Sources, Bulk Edit, Categories)
# https://git.participatoryculture.org/localtv/tree/localtv/templates/localtv/admin/video_header.html
# Admin|Settings buttons (Settings, Themes, Pages)
# https://git.participatoryculture.org/localtv/tree/localtv/templates/localtv/admin/settings_header.html

MCUI = {"MainHome":"css=.nav_home", \
        "MainNewVideos":"css=.nav_new", \
        "MainCategories":"css=.nav_cat", \
        "MainFeatured":"css=.nav_feat", \
        "MainPopular":"css=.nav_pop", \
        "MainAbout":"css=.nav_about", \
        "AdminVideos":"css=.sub", \
        "AdminSettings":"css=.design", \
        "AdminUsers":"css=.users", \
        "AdminComments":"css=.comments", \
        "AdminReviewQueue":"css=.sub", \
        "AdminManageSources":"css=.watched", \
        "AdminBulkEdit":"css=.bulkedit", \
        "AdminCategories":"css=.categories", \
        "AdminSettingsSettings":"css=.settings", \
        "AdminSettingsThemes":"css=.themes", \
        "AdminSettingsPages":"css=.flatpages", \
    }

#========================================================================================
#=                                                                                      =
#=                                    TEST  DATA                                        =
#=                                                                                      =
#========================================================================================

# For Categories test suite

newCategories = ["a-feminist-view","travelling", "food",  "art", "film", "books", "nature"]
newSubcategories = [r'drama', r'comedy', r'horror', r'action', r'family', r'children']
#newSubcategories = ["swimming", "diving", "fishing", "hiking", "biking"]
#newNonASCIICategories = [u'\u0161ipak', u'divlja ru\u017Ea', u'pasja dra\u010Da', u'pasja-ru\u017Ea', u'\u044F\u0431\u043B\u043E\u043A\u043E']
newNonASCIICategories = [[u'\u0161ipak','sipak'], [u'divlja ru\u017Ea','divlja-ruza'], [u'pasja dra\u010Da','pasja-draca'], \
                         [u'pasja-ru\u017Ea','pasja-ruza'], [u'\u044F\u0431\u043B\u043E\u043A\u043E','yabloko']]
