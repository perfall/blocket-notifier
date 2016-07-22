# -*- coding: utf-8 -*-
# Author: Per Fallgren, 22-07-2016
from lxml import etree
from urllib.request import urlopen
import time
import smtplib
import sys

def main(url):
    old_item_number = "default1"
    new_item_number = "default2"
    first = True

    while True:
        response = urlopen(url)
        htmlparser = etree.HTMLParser()
        tree = etree.parse(response, htmlparser)
        new_item_number = tree.xpath('//article[@itemtype="http://schema.org/Offer"]/@id')[0]

        print("CHECKING")
        if new_item_number != old_item_number:
            old_item_number = new_item_number
            if first:
                first = False
                continue
            title = tree.xpath('//*[@id="' + new_item_number + '"]/div/h1/a/@title')[0]
            print(title)

            mailto = '' # Which mail to send the notification to
            mailfrom = '' # Which mail to send the notification from
            password = '' # Password for the sender-mail

            content = url
            message = 'Subject: %s\n\n%s' % ("New article at blocket", content)

            server = smtplib.SMTP('smtp.gmail.com:587')
            server.starttls()
            server.login(mailfrom, password)
            server.sendmail(mailfrom, mailto, message)
            server.quit()
            print("Mail sent")

        time.sleep(300)

if __name__ == "__main__":
    main(sys.argv[1])