import re
import Utils as util
import ApiConnector as api

"""
formatDatetimeForDisplay: reformats a datetime in Zendesk's API format
                          into a readable one
params: datetime, string in format 'yyyy-mm-ddThh:mm:ssZ' to reformat
returns: readable datetime string in format 'dd/mm/yyyy at hh:mm'
"""
def formatDatetimeForDisplay(datetime):
    try:
        # remove letters
        dtSplit = datetime.split("T")
        dtSplit[1] = dtSplit[1][:-1]

        # format date
        dateRaw = dtSplit[0]
        dateRaw = dateRaw.split("-")
        dateRaw = list(reversed(dateRaw))
        date = "/".join(dateRaw)

        # format time
        timeRaw = dtSplit[1]
        time = timeRaw[:-3]
    except IndexError: # we got bad input
        return util.withError("Sorry! We found an invalid time and date in our information. Please contact your system administrator.")
    
    return util.withData({"display": date + " at " + time})

"""
processInput: does something based on a user-inputted command
params: cmd, string of the user-inputted command to process
returns: whatever the called methods return in normal cases, an error
         message if the command wasn't recognised
"""
def processInput(cmd):
    if cmd == "show all": # show all tickets
        return processShowAll()
    elif re.match("^show [\d]+$", cmd) is not None: # show single ticket
        cmdSplit = cmd.split(" ")
        return processShowSingle(int(cmdSplit[1]))
    elif cmd == "help": # help
        return processHelp()
    else:
        return util.withError("Sorry! That command was not recognised. Please type 'help' without quotes for a list of all available commands.")

"""
processShowAll: prints out a summary of each ticket, in a paginated fashion
                (20 tickets per page)
returns: success in normal cases, an error message on failure
"""
def processShowAll():
    print("\nPlease wait while we fetch your tickets from Zendesk...\n")
    # get tickets
    connector = api.ApiConnector()
    gatRet = connector.getAllTickets()
    if not gatRet["status"]:
        return gatRet

    tickets = gatRet["data"]["tickets"]

    # display tickets for each page (20 per)
    pageStart = 0
    pageEnd = 19
    done = False
    infiniteLoopChecker = 0
    while True:
        if infiniteLoopChecker > 500:
            return util.withError("Sorry! This program cannot fetch tickets from accounts with more than 10,000 tickets. Please contact your system administrator.")
        for i in range(pageStart, pageEnd+1):
            try:
                ticket = tickets[i]

                # reformat created_at for display
                formatRet = formatDatetimeForDisplay(ticket["created_at"])
                if not formatRet["status"]:
                    return formatRet
                createdAt = formatRet["data"]["display"]

                # print ticket summary
                ticketDisplay = "Ticket " + str(ticket["id"]) + " (" + ticket["status"].upper() + "): '" + ticket["subject"] + "', opened by " + str(ticket["submitter_id"]) + " on " + createdAt + "."
                print(ticketDisplay)
            except IndexError:
                done = True
                break

        # prompt for next page, if applicable
        if done or pageEnd == (len(tickets)-1):
            return util.ok()
        else:
            print("\nShowing tickets " + str(pageStart+1) + "-" + str(pageEnd+1) + " of " + str(len(tickets)) + ".")
            dummy = input("Press enter to see more:")
            print("")
            pageStart += 20
            pageEnd += 20

        infiniteLoopChecker += 1

"""
processShowSingle: prints out a detailed version of a single ticket
params: ticketId, a string containing the id of the ticket to display
returns: success in normal cases, an error message on failure
"""
def processShowSingle(ticketId):
    print("\nPlease wait while we fetch your ticket from Zendesk...\n")
    # get tickets
    connector = api.ApiConnector()
    gtRet = connector.getTicket(ticketId)
    if not gtRet["status"]:
        return gtRet

    ticket = gtRet["data"]["ticket"]

    # reformat created_at for display
    formatRet = formatDatetimeForDisplay(ticket["created_at"])
    if not formatRet["status"]:
        return formatRet
    createdAt = formatRet["data"]["display"]

    # print detailed ticket
    print("Ticket " + str(ticket["id"]) + " (" + ticket["status"].upper() + ")")
    print("Created on " + createdAt)
    print("Subject: " + ticket["subject"])
    print("\nDescription:\n" + ticket["description"])
    
    return util.ok()

"""
processShowSingle: displays the various commands available to users
returns: success (can't fail)
"""
def processHelp():
    print("The following commands are available:")
    print("'show all' - displays a summarised version of all your tickets")
    print("'show [ticket id]' - displays a detailed version of the ticket with the (numeric) id [ticket id]")
    print("'quit' - exits the program")
    return util.ok()

if __name__ == "__main__":
    print("Welcome to the Zendesk Ticket Viewer!\nType 'help' without quotes for a list of all available commands.")
    while True:
        # prompt input
        cmd = input("\n---------------------\n\nCommand: ")
        
        if (cmd == "quit"): # exit program
            exit()

        # process each command uniquely, printing any errors that occur
        processRet = processInput(cmd)
        if not processRet["status"]:
            print(processRet["error"])
