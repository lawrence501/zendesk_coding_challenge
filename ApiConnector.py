import json
import requests
import Utils as util

class ApiConnector:
    def __init__(self):
        self.allUrl = "https://lawrencemacdonald.zendesk.com/api/v2/tickets.json"
        self.singleUrlPrefix = "https://lawrencemacdonald.zendesk.com/api/v2/tickets/"
        self.singleUrlSuffix = ".json"
        self.username = "lawrencemajmacdonald@gmail.com"
        self.password = "2178122707"

    """
    getAllTickets: gets every ticket from the Zendesk account and
                   returns them as a list of dictionaries
    returns: a list of dictionaries, each one containing a
             ticket's contents, in normal cases, an error message on failure
    """
    def getAllTickets(self):
        currUrl = self.allUrl
        tickets = []
        
        # loop through paginated tickets
        infiniteLoopChecker = 0
        while True:
            if infiniteLoopChecker > 100: # we'd probably hit rate limit first if there actually are this many tickets
                return util.withError("Sorry! This program cannot fetch tickets from accounts with more than 10,000 tickets. Please contact your system administrator.")
            
            # GET request
            gjRet = self.getJson(currUrl)
            if not gjRet["status"]:
                return gjRet
            jsonDict = gjRet["data"]["json"] #tickets, count, next_page, previous_page

            # check for another page
            tickets.extend(jsonDict["tickets"])
            if jsonDict["next_page"] is not None:
                currUrl = jsonDict["next_page"]
            else:
                return util.withData({"tickets": tickets})

            infiniteLoopChecker += 1

    def getJson(self, url):
        resp = requests.get(url, auth=(self.username, self.password))
        # check for unexpected statuses
        if resp.status_code != 200:
            feRet = self.formatError(resp.status_code)
            if feRet["status"]:
                return util.withError(feRet["data"]["errMsg"])
            else: # shouldn't be possible, but just in case
                return feRet
            
        return util.withData({"json": resp.json()})

    """
    getTicket: gets a ticket from the Zendesk account and returns it
               as a dictionary
    params: ticketId, a string containing the id of the ticket to get
    returns: a dictionary representing the ticket in normal cases,
             an error message on failure
    """
    def getTicket(self, ticketId):
        url = self.singleUrlPrefix + str(ticketId) + self.singleUrlSuffix

        # GET request
        resp = requests.get(url, auth=(self.username, self.password))

        # check for unexpected statuses and stop trying on fail
        if resp.status_code != 200:
            feRet = self.formatError(resp.status_code)
            if feRet["status"]:
                return util.withError(feRet["data"]["errMsg"])
            else:
                return feRet

        ticketDict = resp.json()["ticket"]
        return util.withData({"ticket": ticketDict})

    """
    formatError: formats an error message from an unsuccessful
                 HTTP response code
    params: code, an integer of the HTTP response code
    returns: the formatted error message
             
    Note: these messages assume that this program is being
    created for employees at a company who have easy access to their system
    administrator's contact information
    """
    def formatError(self, code):
        if code == 401: # unauthorised
            errText = "We couldn't validate your username and password"
            errSuggest = "Please review your credentials in ApiConnector.py and try again"
        elif code == 404: # not found
            errText = "Zendesk couldn't find that ticket"
            errSuggest = "Double check what you entered and try again"
        elif code == 429: # rate limit exceeded
            errText = "You've tried to fetch your tickets too many times in a minute"
            errSuggest = "Please wait at least 1 minute, and then try again"
        elif code >= 500: # Zendesk-side error
            errText = "Zendesk had an issue when trying to fetch your tickets"
            errSuggest = "Please wait a few minutes, and then try again"
        else: # unknown - errSuggest assumes
            errText = "We've encountered an unexpected error"
            errSuggest = "Please try again later. If it is not resolved, please contact your system administrator"

        # construct full error message
        error = "Status: " + str(code) + "\nSorry! " + errText + ". " + errSuggest + "."
        return util.withData({"errMsg": error})

#cnx = ApiConnector()
#gtRet = cnx.getTicket(5)
#gatRet = cnx.getAllTickets()
#print(gatRet["data"]["tickets"][0])
#for ticket in gtRet["data"]["tickets"]:
#    print(ticket["id"])
