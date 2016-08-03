# -*- coding: utf-8 -*-
# Author: Per Fallgren, 22-07-2016
from lxml import etree
from urllib.request import urlopen
import time
import smtplib
import sys

# User Constants
MAIL_TO = ""                    # Mail address to send the e-mail notification to
MAIL_FROM = ""                  # Mail address to send the e-mail notification from
PASSWORD = ""                   # Password for the sender mail
WAIT_TIME = 300                 # Amount of time in seconds between
SMTP_HOST = "smtp.gmail.com"    # SMTP host location (standard is for Gmail)
SMTP_PORT = 587                 # SMTP host port (standard is for Gmail)
DEBUG_MODE = False

old_item_id = "init_id"
is_first_occurrence = True


def main(url):
    if not url:
        print("Provided URL is empty - exiting")
        sys.exit()
    if not MAIL_TO or not MAIL_FROM or not PASSWORD:
        print("One or many constants not set - exiting")
        sys.exit()

    while True:
        # Find the item
        response = urlopen(url)
        parser = etree.HTMLParser()
        tree = etree.parse(response, parser)
        new_item_id = tree.xpath('//article[@itemtype="http://schema.org/Offer"]/@id')[0]

        if DEBUG_MODE:
            print("Found item with id: [" + new_item_id + "]")

        # If new item is found
        if new_item_id != old_item_id:
            old_item_id = new_item_id

            if is_first_occurrence:
                is_first_occurrence = False
                continue

            if DEBUG_MODE:
                title = tree.xpath("//*[@id=" + new_item_id + "]/div/h1/a/@title")[0]
                print("Found new item with title: [" + title + "]")

            # Create message
            content = url
            message = "Subject: %s\n\n%s" % ("New article at blocket", content)

            # Send message to user
            server = smtplib.SMTP(SMTP_HOST)
            server.starttls()
            server.login(MAIL_FROM, PASSWORD)
            server.sendmail(MAIL_FROM, MAIL_TO, message)
            server.quit()

            if DEBUG_MODE:
                print("Mail sent to: [" + MAIL_TO + "]")

        time.sleep(WAIT_TIME)

if __name__ == "__main__":
    main(sys.argv[1])
