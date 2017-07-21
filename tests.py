import unittest
import requests
import sys
from Main import *
from ApiConnector import *
import Utils as util
from unittest.mock import MagicMock
from unittest.mock import mock_open
from unittest.mock import patch
#from tkinter import *

class DummyStdout(object):
    def write(self, x):
        pass

class MainTests(unittest.TestCase):
    # Tests for formatDatetimeForDisplay
    def test_formatDatetimeForDisplay_sunnyDay(self):
        ret = formatDatetimeForDisplay("2010-01-01T06:06:06Z")
        self.assertTrue(ret["status"] and ret["data"]["display"] == "01/01/2010 at 06:06")
        
    def test_formatDatetimeForDisplay_badFormat(self):
        ret = formatDatetimeForDisplay("2010-01-01Z06:06:06Z")
        self.assertFalse(ret["status"])

    #def test_formatDatetimeForDisplay_badFormat2(self):
    #    ret = formatDatetimeForDisplay("2010-01-01T06:06:06T")
    #    self.assertFalse(ret["status"])

    def test_formatDatetimeForDisplay_badFormat3(self):
        ret = formatDatetimeForDisplay("cat")
        self.assertFalse(ret["status"])
        
    #def test_formatDatetimeForDisplay_badDate(self):
    #    ret = formatDatetimeForDisplay("201001-01T06:06:06Z")
    #    self.assertFalse(ret["status"])

    #def test_formatDatetimeForDisplay_badTime(self):
    #    ret = formatDatetimeForDisplay("2010-01-01T0606:06Z")
    #    self.assertFalse(ret["status"])

    # Tests for processInput
    def test_processInput_sunnyDay(self):
        with patch('Main.processShowAll') as m:
            m.return_value = util.ok()
            ret = processInput("show all")
            self.assertTrue(ret["status"])

    def test_processInput_badCommand(self):
        with patch('Main.processShowAll') as m:
            m.return_value = util.ok()
            ret = processInput("show alll")
            self.assertFalse(ret["status"])

    # Tests for processShowAll
    def test_processShowAll_sunnyDay(self):
        with patch('ApiConnector.ApiConnector.getAllTickets') as m:
            m.return_value = util.withData({"tickets": [{'url': 'https://lawrencemacdonald.zendesk.com/api/v2/tickets/1.json', 'id': 1, 'external_id': None, 'via': {'channel': 'sample_ticket', 'source': {'from': {}, 'to': {}, 'rel': None}}, 'created_at': '2017-07-17T06:37:44Z', 'updated_at': '2017-07-17T06:37:45Z', 'type': 'incident', 'subject': 'Sample ticket: Meet the ticket', 'raw_subject': 'Sample ticket: Meet the ticket', 'description': 'Hi Lawrence,\n\nEmails, chats, voicemails, and tweets are captured in Zendesk Support as tickets. Start typing above to respond and click Submit to send. To test how an email becomes a ticket, send a message to support@lawrencemacdonald.zendesk.com.\n\nCurious about what your customers will see when you reply? Check out this video:\nhttps://demos.zendesk.com/hc/en-us/articles/202341799\n', 'priority': 'normal', 'status': 'open', 'recipient': None, 'requester_id': 114397672514, 'submitter_id': 114397378194, 'assignee_id': 114397378194, 'organization_id': None, 'group_id': 114094490434, 'collaborator_ids': [], 'forum_topic_id': None, 'problem_id': None, 'has_incidents': False, 'is_public': True, 'due_at': None, 'tags': ['sample', 'support', 'zendesk'], 'custom_fields': [], 'satisfaction_rating': None, 'sharing_agreement_ids': [], 'fields': [], 'brand_id': 114094247114, 'allow_channelback': False}]})
            with patch('Main.formatDatetimeForDisplay') as n:
                n.return_value = util.withData({"display": "17/07/2017 at 06:37"})
                savedStdout = sys.stdout
                sys.stdout = DummyStdout()
                ret = processShowAll()
                sys.stdout = savedStdout
                self.assertTrue(ret["status"])

    # Tests for processShowSingle
    def test_processShowSingle_sunnyDay(self):
        with patch('ApiConnector.ApiConnector.getTicket') as m:
            m.return_value = util.withData({"ticket": {'url': 'https://lawrencemacdonald.zendesk.com/api/v2/tickets/1.json', 'id': 1, 'external_id': None, 'via': {'channel': 'sample_ticket', 'source': {'from': {}, 'to': {}, 'rel': None}}, 'created_at': '2017-07-17T06:37:44Z', 'updated_at': '2017-07-17T06:37:45Z', 'type': 'incident', 'subject': 'Sample ticket: Meet the ticket', 'raw_subject': 'Sample ticket: Meet the ticket', 'description': 'Hi Lawrence,\n\nEmails, chats, voicemails, and tweets are captured in Zendesk Support as tickets. Start typing above to respond and click Submit to send. To test how an email becomes a ticket, send a message to support@lawrencemacdonald.zendesk.com.\n\nCurious about what your customers will see when you reply? Check out this video:\nhttps://demos.zendesk.com/hc/en-us/articles/202341799\n', 'priority': 'normal', 'status': 'open', 'recipient': None, 'requester_id': 114397672514, 'submitter_id': 114397378194, 'assignee_id': 114397378194, 'organization_id': None, 'group_id': 114094490434, 'collaborator_ids': [], 'forum_topic_id': None, 'problem_id': None, 'has_incidents': False, 'is_public': True, 'due_at': None, 'tags': ['sample', 'support', 'zendesk'], 'custom_fields': [], 'satisfaction_rating': None, 'sharing_agreement_ids': [], 'fields': [], 'brand_id': 114094247114, 'allow_channelback': False}})
            with patch('Main.formatDatetimeForDisplay') as n:
                n.return_value = util.withData({"display": "17/07/2017 at 06:37"})
                savedStdout = sys.stdout
                sys.stdout = DummyStdout()
                ret = processShowSingle(1)
                sys.stdout = savedStdout
                self.assertTrue(ret["status"])

class ApiConnectorTests(unittest.TestCase):
    # Tests for getAllTickets
    def test_getAllTickets_sunnyDay(self):
        with patch('ApiConnector.ApiConnector.getJson') as m:
            m.return_value = util.withData({"json": {"count": 1, "next_page": None, "previous_page": None, "tickets": [{'url': 'https://lawrencemacdonald.zendesk.com/api/v2/tickets/1.json', 'id': 1, 'external_id': None, 'via': {'channel': 'sample_ticket', 'source': {'from': {}, 'to': {}, 'rel': None}}, 'created_at': '2017-07-17T06:37:44Z', 'updated_at': '2017-07-17T06:37:45Z', 'type': 'incident', 'subject': 'Sample ticket: Meet the ticket', 'raw_subject': 'Sample ticket: Meet the ticket', 'description': 'Hi Lawrence,\n\nEmails, chats, voicemails, and tweets are captured in Zendesk Support as tickets. Start typing above to respond and click Submit to send. To test how an email becomes a ticket, send a message to support@lawrencemacdonald.zendesk.com.\n\nCurious about what your customers will see when you reply? Check out this video:\nhttps://demos.zendesk.com/hc/en-us/articles/202341799\n', 'priority': 'normal', 'status': 'open', 'recipient': None, 'requester_id': 114397672514, 'submitter_id': 114397378194, 'assignee_id': 114397378194, 'organization_id': None, 'group_id': 114094490434, 'collaborator_ids': [], 'forum_topic_id': None, 'problem_id': None, 'has_incidents': False, 'is_public': True, 'due_at': None, 'tags': ['sample', 'support', 'zendesk'], 'custom_fields': [], 'satisfaction_rating': None, 'sharing_agreement_ids': [], 'fields': [], 'brand_id': 114094247114, 'allow_channelback': False}]}})
            test = ApiConnector()
            ret = test.getAllTickets()
            self.assertTrue(ret["status"] and len(ret["data"]["tickets"]) == 1)

    # Tests for getTicket
    def test_getTicket_sunnyDay(self):
        with patch('ApiConnector.ApiConnector.getJson') as m:
            m.return_value = util.withData({"json": {"ticket": {'url': 'https://lawrencemacdonald.zendesk.com/api/v2/tickets/1.json', 'id': 1, 'external_id': None, 'via': {'channel': 'sample_ticket', 'source': {'from': {}, 'to': {}, 'rel': None}}, 'created_at': '2017-07-17T06:37:44Z', 'updated_at': '2017-07-17T06:37:45Z', 'type': 'incident', 'subject': 'Sample ticket: Meet the ticket', 'raw_subject': 'Sample ticket: Meet the ticket', 'description': 'Hi Lawrence,\n\nEmails, chats, voicemails, and tweets are captured in Zendesk Support as tickets. Start typing above to respond and click Submit to send. To test how an email becomes a ticket, send a message to support@lawrencemacdonald.zendesk.com.\n\nCurious about what your customers will see when you reply? Check out this video:\nhttps://demos.zendesk.com/hc/en-us/articles/202341799\n', 'priority': 'normal', 'status': 'open', 'recipient': None, 'requester_id': 114397672514, 'submitter_id': 114397378194, 'assignee_id': 114397378194, 'organization_id': None, 'group_id': 114094490434, 'collaborator_ids': [], 'forum_topic_id': None, 'problem_id': None, 'has_incidents': False, 'is_public': True, 'due_at': None, 'tags': ['sample', 'support', 'zendesk'], 'custom_fields': [], 'satisfaction_rating': None, 'sharing_agreement_ids': [], 'fields': [], 'brand_id': 114094247114, 'allow_channelback': False}}})
            test = ApiConnector()
            ret = test.getTicket(1)
            self.assertTrue(ret["status"] and "ticket" in ret["data"])

if __name__ == "__main__":
    unittest.main()
