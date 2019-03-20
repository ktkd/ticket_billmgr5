# Overview:
Here is the small notification app for ispsystem billmanager 5.

This app are check new tickets in billmanager and make alert via webhook. 

# configure:

You should install environment variables-
*tickets_url* - billing system URL
<br> `tickets_user` - billing staff username
<br> `tickets_pass` - billing staff password
<br> `tickets_timeout` - timeout in seconds between checks
<br> `tickets_print` - print tickets in stdout
<br> `tickets_webhook` - trigger a outgoing webhook 
<br> `tickets_webhook_url` - webhook url
<br> `tickets_webhook_token` - webhook private token 
<br>example-

<code>
tickets_url=https://my.ispsystem.com/billmgr?
tickets_user=UserName
tickets_pass=UserPassword
tickets_timeout=10
tickets_print=yes
tickets_webhook=yes
tickets_webhook_url=https://open.rocket.chat/hooks 
tickets_webhook_token=0210aa315fc8890e3cc26fbe4c1e56a62fa3cdd392
</code>

<h5>install:</h5>
python3 setup.py install

<h5>run:</h5>
