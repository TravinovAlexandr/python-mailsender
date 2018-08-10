#!/usr/bin/env python
# -*- coding: utf-8 -*-

import gtk
import sys
import mailzip
import os
import errno
import mailsendersmtp

class MailSenderGui(gtk.Window):
    
    def __init__(self):

        #app globals
        self.path = ""
        self.configs = []
        self.pathToConfig = os.environ["MAILSENDER"] + "mailsender.conf"
        self.isConfigFileFound = self.configInit(self.pathToConfig)
        
        gtk.Window.__init__(self)
        self.set_size_request(450, 97)
        self.set_position(gtk.WIN_POS_CENTER)
        self.set_resizable(False)
        self.set_title("Mail Sender")
        #layout
        fixed  = gtk.Fixed()
        #widgets
        label = gtk.Label("Path to the target directory or the file.")
        self.textField = gtk.Entry()
        buttonOk = gtk.Button("Ok")
        buttonSelect = gtk.Button("SelectFile")
        buttonExit = gtk.Button("Exit")
        buttonConfig = gtk.Button("Config")
        #adding
        fixed.put(label, 5, 10)
        fixed.put(self.textField, 5, 30)
        fixed.put(buttonOk, 5, 62)
        fixed.put(buttonSelect, 40, 62)
        fixed.put(buttonExit, 408, 62)
        fixed.put(buttonConfig, 347, 62)
        #handlers
        fixed.connect("destroy", lambda quit: gtk.main_quit())
        buttonOk.connect("clicked", self.buttonOkClick)
        buttonSelect.connect("clicked", self.selectFile)
        buttonExit.connect("clicked", lambda exit: gtk.main_quit())
        buttonConfig.connect("clicked", self.showConfigWindow)
        #settings
        self.textField.set_width_chars(54)

        self.add(fixed)
        self.show_all()
        
    #File selection
    def selectFile(self, widget):
        self.filew = gtk.FileSelection("Select File")
        self.filew.connect("destroy", lambda cancel: self.filew.destroy())
        self.filew.ok_button.connect("clicked", self.definePath)
        self.filew.cancel_button.connect("clicked", lambda cancel: self.filew.destroy())
        self.filew.show_all()

    #Config window
    def showConfigWindow(self, widget):

        self.configWin = gtk.Window()
        self.configWin .set_size_request(400, 400)
        self.configWin .set_position(gtk.WIN_POS_CENTER)
        self.configWin .set_title("Mail Sender")
        self.configWin .set_resizable(False)
        self.configWin .set_keep_above(True)
        
        fixLay = gtk.Fixed()

        maiLabel = gtk.Label("1. Insert your email.")
        passwordLabel = gtk.Label("2. Insert your password.")
        destLabel = gtk.Label("3. Insert destination emaill.")
        subjectLabel = gtk.Label("4. Insert subject.")
        serverLabel = gtk.Label("5. Insert server.")
        portLabel = gtk.Label("6. Insert port.")
        self.mailEntry = gtk.Entry()
        self.passwordEntry = gtk.Entry()
        self.destEntry = gtk.Entry()
        self.subjectEntry = gtk.Entry()
        self.serverEntry = gtk.Entry()
        self.portEntry = gtk.Entry()
        okButton = gtk.Button("Ok")
        cancelButton = gtk.Button("Cancel")
        self.radioConfigBut = gtk.CheckButton("Save changes")

        self.mailEntry.set_width_chars(46)
        self.passwordEntry.set_width_chars(46)
        self.destEntry.set_width_chars(46)
        self.subjectEntry.set_width_chars(46)
        self.serverEntry.set_width_chars(46)
        self.portEntry.set_width_chars(46)

        fixLay.put(maiLabel, 10, 10)
        fixLay.put(self.mailEntry, 10 , 30)
        fixLay.put(passwordLabel, 10, 60)
        fixLay.put(self.passwordEntry, 10 , 80)
        fixLay.put(destLabel, 10, 110)
        fixLay.put(self.destEntry, 10 , 130)

        fixLay.put(subjectLabel, 10, 160)
        fixLay.put(self.subjectEntry, 10 , 180)
        fixLay.put(serverLabel, 10, 210)
        fixLay.put(self.serverEntry, 10 , 230)
        fixLay.put(portLabel, 10, 260)
        fixLay.put(self.portEntry, 10 , 280)

        fixLay.put(okButton, 10 , 317)
        fixLay.put(cancelButton, 60 , 317)
        fixLay.put(self.radioConfigBut , 275, 320)

        self.configFieldsInit()

        cancelButton.connect("clicked", lambda can: self.configWin .destroy())
        okButton.connect("clicked", self.configOkButton)

        self.configWin .add(fixLay)
        self.configWin .show_all()

    #Main init of config entries
    def configFieldsInit(self):
        if self.isConfigFileFound == True:
            try:
                self.mailEntry.set_text(self.configs[0])
                self.passwordEntry.set_text(self.configs[1])
                self.destEntry.set_text(self.configs[2])
                self.subjectEntry.set_text(self.configs[3])
                self.serverEntry.set_text(self.configs[4])
                self.portEntry.set_text(self.configs[5])
            except:
                print("{0} Config file has wrong structure.".format(sys.argv[0]))
                self.showWarn("Config file has wrong structure.")
        else:
            self.radioConfigBut.set_sensitive(False)
            print("{0} Config file was not found. Input settings manually.".format(sys.argv[0]))
            self.showWarn("Config file was not found.\nInput settings manually.")

    #ConfigOk button handler    
    def configOkButton(self, widget):
        r = None
        w = None
        self.configs = []
        self.configs.append(self.mailEntry.get_text())
        self.configs.append(self.passwordEntry.get_text())
        self.configs.append(self.destEntry.get_text())
        self.configs.append(self.subjectEntry.get_text())
        self.configs.append(self.serverEntry.get_text())
        self.configs.append(self.portEntry.get_text())
        
        if self.radioConfigBut.get_active() == True:
            try:
                r = open(self.pathToConfig, "r")
                lines = r.readlines()
                lines[0] = lines[0][: lines[0].find("=") +1 ] + self.configs[0] + "\n"
                lines[1] = lines[1][: lines[1].find("=") +1 ] + self.configs[1] + "\n"
                lines[2] = lines[2][: lines[2].find("=") +1 ] + self.configs[2] + "\n"
                lines[3] = lines[3][: lines[3].find("=") +1 ] + self.configs[3] + "\n"
                lines[4] = lines[4][: lines[4].find("=") +1 ] + self.configs[4] + "\n"
                lines[5] = lines[5][: lines[5].find("=") +1 ] + self.configs[5] + "\n"
                w = open(self.pathToConfig, "w")
                w.writelines(lines)
            except IOError as err:
                if err.errno == errno.EEXIST:
                    print("{0}: Config file is not found: {1}".format(sys.argv[0], self.pathToConfigs))
                    self.showError("Config file is not found: {0}".format(self.pathToConfigs))
                if err.errno == 13:
                    print("{0}: Permission denied: {1}".format(sys.argv[0], self.pathToConfigs))
                    self.showError("Permission denied: {0}".format(self.pathToConfigs))
            finally:
                try:
                    r.close()
                    w.close()
                except:
                    pass
        self.configWin.destroy()
                
    #MessageBox1
    def showWarn(self, message):
        dialog = gtk.MessageDialog(self, 
        gtk.DIALOG_DESTROY_WITH_PARENT, gtk.MESSAGE_WARNING, 
        gtk.BUTTONS_CLOSE, message)
        dialog.run()
        dialog.destroy()
    #2
    def showInfo(self, message):
        dialog = gtk.MessageDialog(self, 
        gtk.DIALOG_DESTROY_WITH_PARENT, gtk.MESSAGE_INFO, 
        gtk.BUTTONS_CLOSE, message)
        dialog.run()
        dialog.destroy()
    #3    
    def showError(self, message):
        dialog = gtk.MessageDialog(self, 
        gtk.DIALOG_DESTROY_WITH_PARENT, gtk.MESSAGE_ERROR,
        gtk.BUTTONS_CLOSE, message)
        dialog.run()
        dialog.destroy()
    
    #SelectWindow OkButton handler
    def definePath(self, widget):
        self.path = self.filew.get_filename()
        self.textField.set_text(self.path)
        self.filew.destroy()

    #Configs init in constructor
    def configInit(self, pathToConfigs):
        r = None
        try:
            r = open(pathToConfigs, "r")
            lines = r.readlines()
            self.configs.append(lines[0][lines[0].find("=") + 1 : -1])
            self.configs.append(lines[1][lines[1].find("=") + 1 : -1])
            self.configs.append(lines[2][lines[2].find("=") + 1 : -1])
            self.configs.append(lines[3][lines[3].find("=") + 1 : -1])
            self.configs.append(lines[4][lines[4].find("=") + 1 : -1])
            self.configs.append(lines[5][lines[5].find("=") + 1 : -1])
            return True
        except IOError as err:
            #FileNotFoundError
            if err.errno == 2:
                print("{0}: Config file is not found: {1}".format(sys.argv[0], self.pathToConfig ))
                self.showError("Config file is not found: {0}".format(self.pathToConfig ))
                self.log("Config file is not found.")

                return False
        except:    
            print("{0}: Config file has wrong structure {1}".format(sys.argv[0], self.pathToConfig))
            self.showError("Config file has wrong structure: {0}".format(self.pathToConfig))
            self.log("Config file has wrong structure// {0}".format(self.pathToConfig))
            return False
        finally:
            try:
                r.close()
            except:
                pass

    #MainWindowButtonOk handler 
    def buttonOkClick(self, widget):
        self.path = self.textField.get_text()
        self.path = self.path.strip()
        if self.path != "":
            if os.path.isdir(self.path) == True:
                returnCode = mailzip.makeArhiveFromDir(self.path)
                if str(returnCode).find("tmp") != -1:
                    tmpName = returnCode + self.path[ self.path.rfind("/") :] + ".zip"
                    smtpRetCode = mailsendersmtp.sendEmailWithAttachment(tmpName, self.configs)
                    if smtpRetCode == 0:
                        print("{0}: Email saccessesfuly sended.".format(sys.argv[0]))
                        self.showInfo("Email saccessesfuly sended.")
                        mailzip.removeTmpDir(returnCode)
                    else:
                        print("{0}: Email was not sended.".format(sys.argv[0]))
                        self.showInfo("Email was not sended.")
                        mailzip.removeTmpDir(returnCode)
                        self.log("Email was not sended.//{0}//{1}".format(self.configs ,self.path))
                elif returnCode == -1:
                    print("{0}: Dir is already exists: {1}".format(sys.argv[0],  self.path[ self.path.rfind("/") :]))
                    self.showWarn("Dir is already exists:\n/tmp{0}".format(self.path[ self.path.rfind("/") :]))
                    self.log("Dir is already exists.//{0}//tmp{1}".format(self.configs ,self.path[ self.path.rfind("/") :]))
                elif returnCode == -2:
                    print("{0}: Some file(s) in {1} is not readable".format(sys.argv[0],  self.path))
                    self.showWarn("Some file(s) is not readable\n{0}".format(self.path))
                    self.log("Some file(s) is not readable.//{0}//{1}".format(self.configs ,self.path))
                elif returnCode == -3:
                    self.textField.set_text("")
                    print("{0}: Dir is not readable: {1}".format(sys.argv[0], self.path))
                    self.showWarn("Dir is not readable:\n{0}".format(self.path))
                    self.log("Dir is not readable.//{0}//{1}".format(self.configs , self.path))
            else:
                returnCode = mailzip.makeArhiveFromFile(self.path)
                if str(returnCode).find("tmp") != -1:
                    tmpName = returnCode + self.path[ self.path.rfind("/") :] + ".zip"
                    smtpRetCode = mailsendersmtp.sendEmailWithAttachment(tmpName, self.configs)
                    if smtpRetCode == 0:
                        print("{0}: Email saccessesfuly sended.".format(sys.argv[0]))
                        self.showInfo("Email  saccessesfuly sended.")
                        mailzip.removeTmpDir(returnCode)
                    else:
                        print("{0}: Email was not sended..".format(sys.argv[0]))
                        self.showInfo("Email was not sended.")
                        mailzip.removeTmpDir(returnCode)
                        self.log("Email was not sended.//{0}//{1}".format(self.configs ,self.path))
                elif returnCode == -1:
                    print("{0}: Dir is already exists: {1}".format(sys.argv[0],  self.path[ self.path.rfind("/") :]))
                    self.showWarn("Dir is already exists:\n/tmp{0}".format("/tmp" + self.path[ self.path.rfind("/") :]))
                    self.log("Dir is already exists.//{0}//tmp{1}".format(self.configs ,self.path[ self.path.rfind("/") :]))
                elif returnCode == -2:
                    print("{0}: Can not zip file: {1}".format(sys.argv[0], self.path))
                    self.showWarn("Can not zip file:\n{0}".format(self.path))
                    self.log("Can not zip file.//{0}//{1}".format(self.configs ,self.path))
                elif returnCode == -3:
                    self.textField.set_text("")
                    print("{0}: File is not readable: {1}".format(sys.argv[0], self.path))
                    self.showWarn("File is not readable:\n{0}".format(self.path))
                    self.log("File is not readable.//{0}//{1}".format(self.configs , self.path))
        else:
            self.textField.set_text("")
            self.showWarn("Path is not defined.")
            print("{0}: Path is not defined.".format(sys.argv[0]))

    #Logger
    def log(self, message):
        try:
            import logging
            from time import gmtime, strftime
            pathToLogFile = os.environ["MAILSENDER"] + "mailsender.log"
            logging.basicConfig(filename=pathToLogFile, level=logging.ERROR)
            logging.error(strftime("%Y-%m-%d %H:%M:%S", gmtime()) + "//" + message)
        except OSError as err:
            if err.errno == 2:
                print("{0}: Log file not found: {1}".format(sys.argv[0], pathToLogFile))
            if err.errno == 13:
                 print("{0}: Permissions denied: {1}".format(sys.argv[0], pathToLogFile))