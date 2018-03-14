# required install package
# pip install oauth2client==1.5.2
# pip install gspread==0.6.2

import gspread
from oauth2client.client import SignedJwtAssertionCredentials
import json

# Below are the indexes of necessary information in the Google Sheet. Need to change if needed

FIRST_NAME = 1
LAST_NAME = 2
EMAIL = 3
TOPIC = 4
SUB_TOPICS = range(5, 10)
SPECIAL_REQUIREMENT = 11
DETAIL_REQUIREMENT = 12


# get the google client - no need to change
def get_google_client():
    with open('google_key.json') as f:
        config = json.load(f)

    creds = SignedJwtAssertionCredentials(
        config['client_email'],
        config['private_key'],
        ['https://spreadsheets.google.com/feeds']
    )
    return gspread.authorize(creds)


# group by technical area
def process_value(values, topics):
    topic = values[TOPIC]
    if topic in topics:
        topics[topic].append(values)
    else:
        topics[topic] = [values]


# get the sub topic from Google sheet
def get_sub_topic(values):
    for i in SUB_TOPICS:
        if values[i]:
            return values[i]
    return ""


# get the sub topic from Google sheet
def get_name(values):
    return values[FIRST_NAME] + " " + values[LAST_NAME]


# write content to file
def write_to_file(topics):
    with open("ecp.md", "w") as f:
        f.write("## 2.3 Exascale Computing Project\n\n")
        for topic in sorted(topics.keys()):

            # Write header for table
            f.write("\n\n### "+topic+"\n\n")
            f.write("Project | POC | Response\n")
            f.write("--- | --- | ---\n")

            ls = []
            # add subtopics and author name to list
            for values in topics[topic]:
                ls.append([get_sub_topic(values), get_name(values)])

            # sort the list by project orders
            ls = sorted(ls, key=lambda x: x[0])

            # write the list to file
            for x in ls:
                f.write(x[0] + " | " + x[1] + " | " + "Response" + "\n")


def run():
    gc = get_google_client()

    # Open file: key in the URL
    doc = gc.open_by_key('1UzakfbtnQunlHAWCs_T5L2P7x9b9QkwDGHGna3n3hfQ')

    # Open tab
    sheet = doc.worksheet("Form Responses 1")

    row_count = sheet.row_count
    topics = {}
    for row in range(2, row_count + 1):
        values = sheet.row_values(row)

        # Blank row
        if not values[0]:
            break
        # process the values collected
        process_value(values, topics)

    # write values into file
    write_to_file(topics)


if __name__ == '__main__':
    run()
