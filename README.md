# Overview:
Here is the small notification app for ispsystem billmanager 5.

This app are check new tickets in billmanager and make alert via webhook. 

# configure:
You should install environment variables-
<br> `tickets_url` - billing system URL
<br> `tickets_user` - billing staff username
<br> `tickets_pass` - billing staff password
<br> `tickets_timeout` - timeout in seconds between checks
<br> `tickets_print` - print tickets in stdout
<br> `tickets_webhook` - trigger a outgoing webhook 
<br> `tickets_webhook_url` - webhook url
<br> `tickets_webhook_token` - webhook private token 


**example:**
<br>`tickets_url=https://my.ispsystem.com/billmgr?`
<br>`tickets_user=UserName`
<br>`tickets_pass=UserPassword`
<br>`tickets_timeout=10`
<br>`tickets_print=yes`
<br>`tickets_webhook=yes`
<br>`tickets_webhook_url=https://open.rocket.chat/hooks`
<br>`tickets_webhook_token=0210aa315fc8890e3cc26fbe4c1e56a62fa3cdd392`

# install: 
python3 setup.py install

# run: 
ticketsbill5
