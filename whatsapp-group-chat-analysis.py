import pandas as pd
import re


def starts_with_date_and_time(s):
    # regex pattern for date.(Works only for android. IOS Whatsapp export format is different. Will update the code soon
    s = ''.join(filter(None, s.split("[")))
    s = ''.join(filter(None, s.split("]")))
    pattern = r'(?=\d{1,2}.\d{1,2}.\d{2}(?:\d{2})?\s\d{2}(?:\d{2})?:\d{1,2}:\d{1,2})'
    result = re.match(pattern, s)
    if result:
        return True
    return False


def get_data_point(line):
    n = 2
    split_line = line.split()
    date_time = ' '.join(split_line[:n])
    date_time = ''.join(filter(None, date_time.split("[")))
    date_time = ''.join(filter(None, date_time.split("]")))
    author_message = ' '.join(split_line[n:])
    if ": " in author_message:
        n = 1
        split_message = author_message.split(": ")
        author = ''.join(split_message[:n])
        message = ''.join(split_message[n:])
    else:
        author = "-"
        message = author_message
    return date_time, author, message


parsedData = []  # List to keep track of data so it can be used by a Pandas dataframe
# Upload your file here
conversationPath = 'E:\Desktop\Project\Survivor_THY_Teknik_chat.txt'  # chat file

with open(conversationPath, encoding="utf-8") as fp:
    fp.readline()  # Skipping first line of the file because contains information related to something about
    # end-to-end encryption
    messageBuffer = []
    dateTime, author = None, None
    while True:
        line = fp.readline()
        if not line:
            break
        line = line.strip()
        if starts_with_date_and_time(line):
            if len(messageBuffer) > 0:
                parsedData.append([dateTime, author, ' '.join(messageBuffer)])
            messageBuffer.clear()
            dateTime, author, message = get_data_point(line)
            messageBuffer.append(message)
        else:
            messageBuffer.append(line)

df = pd.DataFrame(parsedData, columns=['Date - Time', 'Author', 'Message'])  # Initialising a pandas Dataframe.
df["Date - Time"] = pd.to_datetime(df["Date - Time"])

df.to_excel("wp_group_chat.xlsx", index=False)
