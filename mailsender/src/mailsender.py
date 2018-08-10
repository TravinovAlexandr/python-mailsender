#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import mailgui
import gtk

def main():

    if len(sys.argv)  == 2 :
        os.environ["MAILSENDER"] = str(sys.argv[1]) + "/"
        print("\nMAIL SENDER")
        mailgui.MailSenderGui()
        gtk.main()

    else:
        print("{0}: args==1".format(sys.argv[0]))

if __name__ == "__main__":
    sys.exit(main())
    