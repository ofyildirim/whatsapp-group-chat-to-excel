import pandas as pd
import re

def startsWithDateAndTime(s):
    # regex pattern for date.(Works only for android. IOS Whatsapp export format is different. Will update the code soon
    s = ''.join(filter(None, s.split("[")))
    s = ''.join(filter(None, s.split("]")))
    pattern = r'(?=\d{1,2}.\d{1,2}.\d{2}(?:\d{2})?\s\d{2}(?:\d{2})?:\d{1,2}:\d{1,2})'
    result = re.match(pattern, s)
    if result:
        return True
    return False

def getDataPoint(line):
    n = 2
    splitLine = line.split()
    dateTime = ' '.join(splitLine[:n])
    dateTime = ''.join(filter(None, dateTime.split("[")))
    dateTime = ''.join(filter(None, dateTime.split("]")))
    authorMessage = ' '.join(splitLine[n:])
    if ": " in authorMessage:
        n = 1
        splitted = authorMessage.split(": ")
        author = ''.join(splitted[:n])
        message = ''.join(splitted[n:])
    else:
        author = "-"
        message = authorMessage
    return dateTime, author, message

parsedData = [] # List to keep track of data so it can be used by a Pandas dataframe
# Upload your file here
conversationPath = '__PATH__' # chat file

with open(conversationPath, encoding="utf-8") as fp:
    fp.readline() # Skipping first line of the file because contains information related to something about end-to-end encryption
    messageBuffer = []
    dateTime, author = None, None
    while True:
        line = fp.readline()
        if not line:
            break
        line = line.strip()
        if startsWithDateAndTime(line):
            if len(messageBuffer) > 0:
                parsedData.append([dateTime, author, ' '.join(messageBuffer)])
            messageBuffer.clear()
            dateTime, author, message = getDataPoint(line)
            messageBuffer.append(message)
        else:
            messageBuffer.append(line)

df = pd.DataFrame(parsedData, columns=['Date - Time', 'Author', 'Message']) # Initialising a pandas Dataframe.
df["Date - Time"] = pd.to_datetime(df["Date - Time"])

df.to_excel("wp_group_chat.xlsx", index=False)