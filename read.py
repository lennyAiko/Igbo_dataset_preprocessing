import mysql.connector
import os


# for creating folders in uppercase
upper_labels = ['A', 'B', 'CH', 'D', 'E', 'F', 'G', 'GB', 'GH', 'GW', 'H', 'I',
          'II', 'J', 'K', 'KP', 'KW', 'L', 'M', 'N', 'NN', 'NW', 'NY', 'O', 'OO',
          'P', 'R', 'S', 'SH', 'T', 'U', 'UU', 'V', 'W', 'Y', 'Z']

# for creating folders in lowercase
lower_labels = ['a', 'b', 'ch', 'd', 'e', 'f', 'g', 'gb', 'gh', 'gw',
                'h', 'i', 'ii', 'j', 'k', 'kp', 'kw', 'l', 'm', 'n', 'nn',
                 'nw', 'ny', 'o', 'oo', 'p', 'r', 's', 'sh', 't', 'u', 'uu',
                 'v', 'w', 'y', 'z']

# Connecting to the DB
connection = mysql.connector.connect(
    host='localhost',
    database='igbo_alphabets',
    user='root',
    password='@Security21',
    auth_plugin='mysql_native_password'
)

cursor = connection.cursor()

# Converting the binary file to an actual image
def write_file(data, filename):
    with open(filename, 'wb') as file:
        file.write(data)

# Reading the file from the DB
def readBLOB(letter):

    sql_fetch_blob_query = """SELECT * from dataset where letter = %s"""

    cursor.execute(sql_fetch_blob_query, (letter,))
    record = cursor.fetchall()
    return record

# For processing files and calling other functions
def fileHandler():
    num = 0
    count = 0

    for i in range(len(upper_labels)):
        os.mkdir(f'sorted/upper/{upper_labels[i]}')
    for i in range(len(lower_labels)):
        os.mkdir(f'sorted/lower/{lower_labels[i]}')

    cursor.execute(f"""select count(letter) from dataset """)
    amount = cursor.fetchall()
    amount = amount[0][0]

    while num != amount:
        record = readBLOB(upper_labels[count])
        for row in record:
            id = row[0]
            char = row[1]
            image = row[2]
            if char.isupper():
                upperphoto = f"sorted/upper/{char}/{id}.png"
                write_file(image, upperphoto)
            else:
                lowerphoto = f"sorted/lower/{char}/{id}.png"
                write_file(image, lowerphoto)
        count += 1
        num += amount/len(upper_labels) ## Total amount / 36

fileHandler()

# close the DB connection when done
if connection.is_connected():
    cursor.close()
    connection.close()
    print("MySQL connection is closed")

## Runtime is in seconds