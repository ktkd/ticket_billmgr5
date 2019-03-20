#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ticket alerting for billmanager
"""
import time
import json
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
import requests
import urllib3
import ticketsbill5.config as cfg


# urllib3.disable_warnings()


class Ticket:
    """
    Ticket class
    """

    def __init__(self, msg_id, title, tk_id, client, is_unread):
        self.msg_id = msg_id
        self.is_unread = is_unread
        self.title = title
        self.tk_id = tk_id
        self.client = client


def requests_retry_session(
        retries=10,
        backoff_factor=1,
        status_forcelist=(500, 502, 504),
        session=None):
    """
    :param retries: cont retries
    :param backoff_factor: A backoff factor to apply between attempts.
    :param status_forcelist:  A set of HTTP status codes that we should force a retry on.
    :param session: Session HTTPAdapter
    :return: session
    """
    session = session or requests.Session()
    retry = Retry(
        total=retries,
        read=retries,
        connect=retries,
        backoff_factor=backoff_factor,
        status_forcelist=status_forcelist,
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    return session


def get_tickets():
    """
    Function to get xml body and parse it
    :return:
    """
    response = requests_retry_session().get(f'{cfg.CONF.tickets_url}'
                                            f'&func=ticket'
                                            f'&out=xml'
                                            f'&authinfo={cfg.CONF.tickets_user}'
                                            f'%3A{cfg.CONF.tickets_pass}').content
    soup = BeautifulSoup(response, "xml")
    soap_tickets = soup.find_all("elem")
    ticket_list = []
    for ticket in soap_tickets:
        msg_id = ticket.find_all("id")[0].string
        client = ticket.find_all("client")[0].string
        tk_id = ticket.find_all("ticket")[0].string
        title = ticket.find_all("name")[0].string
        try:
            unread = ticket.find_all("unread")[0].string
        except:
            unread = "off"
        if unread == "on":
            is_unread = True
        else:
            is_unread = False
        ticket_list.append(Ticket(msg_id, tk_id, title, client, is_unread))
    return ticket_list


def get_tickets_ids(tickets_id):
    """
    function to get tickets ID
    """
    ids = {}
    for ticket in tickets_id:
        ids[int(ticket.msg_id)] = ticket
    return ids


def rocket_hook(tickets_act, message, user, ticketid, dbsid):
    """
    Webhook for Rocket.Chat
    :param tickets_act:
    :param message:
    :param user:
    :param ticketid:
    :return:
    """
    if cfg.CONF.tickets_webhook == 'yes':
        http = urllib3.PoolManager()
        http.request('POST',
                     f'{cfg.CONF.tickets_webhook_url}/{cfg.CONF.tickets_webhook_token}',
                     body=json.dumps({
                         "text": f"Active tickets: {tickets_act}",
                         "attachments": [
                             {
                                 "title": f"Ticket: {ticketid}",
                                 "title_link":
                                     f"{cfg.CONF.tickets_url}"
                                     f"elid={dbsid}"
                                     f"&plid="
                                     f"&startform=ticket.edit",
                                 "text": f"User: {user},\nMessage: {message}",
                                 "color": "#7C0A02"
                             }
                         ]
                     }),
                     headers={'Content-Type': 'application/json'})


def log_hook(tickets_act, message, user, ticketid, dbsid):
    """
    Hook to write stdout log
    :param tickets_act:
    :param message:
    :param user:
    :param ticketid:
    :return:
    """
    if cfg.CONF.tickets_print == 'yes':
        print(f'=== \n'
              f'{time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())} \n'
              f'Open tickets:{tickets_act} \n'
              f'Ticket ID:{ticketid} \n'
              f'Database ID:{dbsid} \n'
              f'User:{user} \n'
              f'Message:{message} \n')


def main():
    """
    main code block
    :return:
    """
    old = get_tickets_ids(get_tickets()).keys()
    diff = []
    while True:
        try:
            tickets = get_tickets()
        except:
            continue
        new = get_tickets_ids(tickets)
        newid = new.keys()
        diff = set(newid) - set(old)
        newtickets = []
        for i in diff:
            if new[i].is_unread:
                newtickets.append(new[i])
        for messages in newtickets:
            rocket_hook(str(len(tickets)),
                        messages.tk_id,
                        messages.client,
                        messages.title,
                        messages.msg_id)
            log_hook(str(len(tickets)),
                     messages.tk_id,
                     messages.client,
                     messages.title,
                     messages.msg_id)
        old = newid
        time.sleep(int(cfg.CONF.tickets_timeout))


if __name__ == '__main__':
    main()
