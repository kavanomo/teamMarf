# Functions for passing messages to and from the GUI

def sendMessage(arguments):
    """
    Receive parameters to be sorted, compile the message and send it to the pi
    :param arguments:
    :return:
    """
    message = {"type":0, "data": {}}

