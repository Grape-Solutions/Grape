# AUTHOR : AKSHAT @Akshat-UNT

# import sys
# from PyQt5 import QtGui
# from PyQt5.QtCore import *
# from PyQt5.QtWidgets import *
# from PyQt5.QtWebEngineWidgets import *

# def application_():
#     class MainWindow(QMainWindow):
#         def __init__(self):
#             super(MainWindow, self).__init__()
#             self.browser = QWebEngineView()
#             self.browser.setUrl(QUrl('https://grapesearch.netlify.app/search'))
#             self.setCentralWidget(self.browser)
#             self.showMaximized()

#             # navbar
#             self.setWindowIcon(QtGui.QIcon('Images\\ico.png'))
#             navbar = QToolBar()
#             self.addToolBar(navbar)

#             back_btn = QAction('Back', self)
#             back_btn.triggered.connect(self.browser.back)
#             navbar.addAction(back_btn)

#             forward_btn = QAction('Forward', self)
#             forward_btn.triggered.connect(self.browser.forward)
#             navbar.addAction(forward_btn)

#             reload_btn = QAction('Reload', self)
#             reload_btn.triggered.connect(self.browser.reload)
#             navbar.addAction(reload_btn)

#             home_btn = QAction('Home', self)
#             home_btn.triggered.connect(self.navigate_home)
#             navbar.addAction(home_btn)

#             self.url_bar = QLineEdit()
#             self.url_bar.returnPressed.connect(self.navigate_to_url)
#             navbar.addWidget(self.url_bar)

#             self.browser.urlChanged.connect(self.update_url)

#         def navigate_home(self):
#             self.browser.setUrl(QUrl('https://grapesearch.netlify.app/search'))

#         def navigate_to_url(self):
#             url = self.url_bar.text()
#             self.browser.setUrl(QUrl(url))

#         def update_url(self, q):
#             self.url_bar.setText(q.toString())


#     app = QApplication(sys.argv)
#     QApplication.setApplicationName('Grape 🔎')
#     window = MainWindow()
#     app.exec_()

# ------------------- TABBED --------------------------------
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtPrintSupport import *
import os
import sys
def application_():
    # main window
    class MainWindow(QMainWindow):

        # constructor
        def __init__(self, *args, **kwargs):
            super(MainWindow, self).__init__(*args, **kwargs)
            self.tabs = QTabWidget()
            self.tabs.setDocumentMode(True)
            self.tabs.tabBarDoubleClicked.connect(self.tab_open_doubleclick)
            self.tabs.currentChanged.connect(self.current_tab_changed)
            self.tabs.setTabsClosable(True)
            self.tabs.tabCloseRequested.connect(self.close_current_tab)
            self.setCentralWidget(self.tabs)
            self.status = QStatusBar()
            self.setStatusBar(self.status)
            navtb = QToolBar("Navigation")
            self.addToolBar(navtb)
            back_btn = QAction("Back", self)
            back_btn.setStatusTip("Back to previous page")
            back_btn.triggered.connect(lambda: self.tabs.currentWidget().back())
            navtb.addAction(back_btn)
            next_btn = QAction("Forward", self)
            next_btn.setStatusTip("Forward to next page")
            next_btn.triggered.connect(lambda: self.tabs.currentWidget().forward())
            navtb.addAction(next_btn)
            reload_btn = QAction("Reload", self)
            reload_btn.setStatusTip("Reload page")
            reload_btn.triggered.connect(lambda: self.tabs.currentWidget().reload())
            navtb.addAction(reload_btn)
            home_btn = QAction("Home", self)
            home_btn.setStatusTip("Go home")
            home_btn.triggered.connect(self.navigate_home)
            navtb.addAction(home_btn)
            navtb.addSeparator()
            self.urlbar = QLineEdit()
            self.urlbar.returnPressed.connect(self.navigate_to_url)
            navtb.addWidget(self.urlbar)
            stop_btn = QAction("Stop", self)
            stop_btn.setStatusTip("Stop loading current page")
            stop_btn.triggered.connect(lambda: self.tabs.currentWidget().stop())
            navtb.addAction(stop_btn)
            self.add_new_tab(QUrl('https://grapesearch.netlify.app/search'), 'Homepage')
            self.show()
            self.setWindowTitle("Grape 🔎")
        def add_new_tab(self, qurl = None, label ="Blank"):

            # if url is blank
            if qurl is None:
                # creating a google url
                qurl = QUrl('https://grapesearch.netlify.app/search')

            # creating a QWebEngineView object
            browser = QWebEngineView()

            # setting url to browser
            browser.setUrl(qurl)

            # setting tab index
            i = self.tabs.addTab(browser, label)
            self.tabs.setCurrentIndex(i)

            # adding action to the browser when url is changed
            # update the url
            browser.urlChanged.connect(lambda qurl, browser = browser:
                                    self.update_urlbar(qurl, browser))

            # adding action to the browser when loading is finished
            # set the tab title
            browser.loadFinished.connect(lambda _, i = i, browser = browser:
                                        self.tabs.setTabText(i, browser.page().title()))

        # when double clicked is pressed on tabs
        def tab_open_doubleclick(self, i):

            # checking index i.e
            # No tab under the click
            if i == -1:
                # creating a new tab
                self.add_new_tab()

        # when tab is changed
        def current_tab_changed(self, i):

            # get the curl
            qurl = self.tabs.currentWidget().url()

            # update the url
            self.update_urlbar(qurl, self.tabs.currentWidget())

            # update the title
            self.update_title(self.tabs.currentWidget())

        # when tab is closed
        def close_current_tab(self, i):

            # if there is only one tab
            if self.tabs.count() < 2:
                # do nothing
                return

            # else remove the tab
            self.tabs.removeTab(i)

        # method for updating the title
        def update_title(self, browser):

            # if signal is not from the current tab
            if browser != self.tabs.currentWidget():
                # do nothing
                return

            # get the page title
            title = self.tabs.currentWidget().page().title()

            # set the window title
            self.setWindowTitle("% s - Search!" % title)

        # action to go to home
        def navigate_home(self):

            # go to google
            self.tabs.currentWidget().setUrl(QUrl("https://grapesearch.netlify.app/search"))

        # method for navigate to url
        def navigate_to_url(self):

            # get the line edit text
            # convert it to QUrl object
            q = QUrl(self.urlbar.text())

            # if scheme is blank
            if q.scheme() == "":
                # set scheme
                q.setScheme("http")

            # set the url
            self.tabs.currentWidget().setUrl(q)

        # method to update the url
        def update_urlbar(self, q, browser = None):

            # If this signal is not from the current tab, ignore
            if browser != self.tabs.currentWidget():

                return

            # set text to the url bar
            self.urlbar.setText(q.toString())

            # set cursor position
            self.urlbar.setCursorPosition(0)

    # creating a PyQt5 application
    app = QApplication(sys.argv)

    # setting name to the application
    app.setApplicationName("Grape 🔎")

    # creating MainWindow object
    window = MainWindow()

    # loop
    app.exec_()
