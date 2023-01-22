""" 
AraaniProtocol.py

Utilities to import AraaniProtocol message .xml files in python.

"""

import xml.etree.ElementTree as ET
from typing import List, Optional, Dict

def __find_all(a_str, sub):
    start = 0
    while True:
        start = a_str.find(sub, start)
        if start == -1: return
        yield start
        start += len(sub) # use start += 1 to find overlapping matches


def getMessages(filename: str) -> List[str]:
    """ Gets a list of `Message` elements in file.

    Args:
        filename: path to a file with araani protocol messages.
        
    Returns:
        A list with all message elements in the file.

    Raises:
        FileNotFoundError if file does not exist.
    """

    with open(filename) as f:
        contents = f.read()

    messages = []
    
    startStr = "<Message>"
    stopStr = "</Message>"
    starts = list(__find_all(contents, startStr))
    stops = list(__find_all(contents, stopStr))
    for start, stop in zip(starts, stops):
         messages.append(contents[start:stop+len(stopStr)])

    return messages


def getValidXmlString(filename: str) -> str:
    """ Get all `Message` elements in the originalFile as a valid xml string that can be parsed with an xml parser.

    Args:
        filename: path to a file with araani protocol messages.
        
    Returns:
        A valid xml string with `Message` elements from the input file.

    Raises:
        FileNotFoundError if originalFile does not exist.
    """

    messages = getMessages(filename)

    xmlString = '<?xml version="1.0" encoding="utf-8"?><xml>'
    for msg in messages:
        xmlString += msg
    xmlString += "</xml>"

    return xmlString


def getStateMessageCount(filename:str, targetState: str, targetSrc: Optional[str]=None, targetType: Optional[str]=None) -> int:
    """ Count the number of state messages with target attributes in file.

    Count the number of `Message` elements with child element `State` with 
    attribute `state` equal to targetState,
    attribute `type` equal to targetType, 
    attribute `src`equal to targetSrc.
    If targetType or targetSrc are None, then any value of the respective attribute is counted.

    Args:
        filename: path to file with araani protocol messages.
        targetState: value of attribute `state` to target.
        targetType: value of attribute `type` to target.
        targetSrc: value of attribute `src` to target.
    Returns:
        The number of occurences of the state message with given attributes.
    """
    xmlString = getValidXmlString(filename)

    root = ET.fromstring(xmlString)
    count = 0
    for message in root.findall('Message'):
        for state in message.findall('State'):
            if ((state.attrib['src'] == targetSrc or targetSrc is None)
                and (state.attrib['type'] == targetType or targetType is None)
                and state.attrib['state'] == targetState):
                    count += 1
    return count


def getEventMessageCount(filename: str, targetType: str, targetState: Optional[str]=None, targetSrc: Optional[str]=None) -> int:
    """Count the number of event messages with target attributes in file.

    Count the number of `Message` elements with child element `Event` with 
    attribute `type` equal to targetType, 
    attribute `state` equal to targetState,
    attribute `src`equal to targetSrc.
    If targetState or targetSrc are None, then any value of the respective attribute is counted.

    Args:
        filename: path to file with araani protocol messages.
        targetType: value of attribute `type` to target.
        targetState: value of attribute `state` to target.
        targetSrc: value of attribute `src` to target.

    Returns:
        The number of occurences of the event message with given attributes.
    """
    xmlString = getValidXmlString(filename)
    root = ET.fromstring(xmlString)
    count = 0
    for message in root.findall('Message'):
        for state in message.findall('Event'):
            if ((state.attrib['src'] == targetSrc or targetSrc is None)
                and (state.attrib['type'] == targetType)
                and (state.attrib['state'] == targetState or targetState is None)):
                    count += 1
    return count



def stateMessageCounts(files: List[str], targetStates: List[str], targetSrc: Optional[str]=None, targetType: Optional[str]=None) -> Dict[str,List[int]]:
    """ Count the number of state messages with target attributes for all files.

    Count the number of `Message` elements with child element `State` with; 
    attribute `state` in targetStates,
    attribute `type` equal to targetType, 
    attribute `src`equal to targetSrc;
    for every state in targetStates, and every file in files.

    If targetType or targetSrc are None, 
    then any value of the respective attribute is counted.

    Args:
        files: files with araani protocol messages.
        targetStates: list of values of attribute `state` to target.
        targetType: value of attribute `type` to target.
        targetSrc: value of attribute `src` to target.

    Returns:
        A dictionary with a key for every targetState, 
        and value is a list with the occurence of that state message 
        for every file in files. 
        For example:

        {"Operational Signal": [1,1,1,1,1,1,1],
         "Fire Alarm": [0,0,1,1,0,0]}

    """

    out = {k:[] for k in targetStates}

    for f in files:
        for targetState in targetStates:
            out[targetState].append(getStateMessageCount(f, targetState, targetSrc, targetType))

    return out


def eventMessageCounts(files: List[str], targetTypes: List[str], targetState: Optional[str]=None, targetSrc: Optional[str]=None) -> Dict[str,List[int]]:
    """ Count the number of event messages with target attributes for all files.

    Count the number of `Message` elements with child element `State` with; 
    attribute `type` in targetTypes, 
    attribute `state` equal to targetState,
    attribute `src`equal to targetSrc;
    for every state in targetStates, and every file in files.

    If targetState or targetSrc are None, 
    then any value of the respective attribute is counted.

    Args:
        files: files with araani protocol messages.
        targetTypes: list of values of attribute `type` to target.
        targetState: value of attribute `state` to target.
        targetSrc: value of attribute `src` to target.

    Returns:
        A dictionary with a key for every targetType. 
        and value is a list with the occurence of that event message 
        for every file in files. 
        For example:

        {"Camera Blocking": [1,1,1,1,1,1,1],
         "Light Change": [0,0,1,1,0,0]}

    """
    out = {k:[] for k in targetTypes}

    for f in files:
        for targetType in targetTypes:
            out[targetType].append(getEventMessageCount(f, targetType, targetState, targetSrc))

    return out
