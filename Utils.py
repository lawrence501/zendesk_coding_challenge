# anonymous dictionary structure (for consistent and flexible returns):
#   status: True/False (success/fail)
#   data: dictionary with return data
#   error: error message (always present when status: 0)

def withError(errorStr):
    return {"status": False, "error": errorStr}

def withData(dataDict):
    return {"status": True, "data": dataDict}

def ok():
    return {"status": True}
