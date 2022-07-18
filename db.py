import mysql.connector
import os


# Connecting to my localhost mysql server
connection = mysql.connector.connect(
    host='localhost',
    database='igbo_alphabets',
    password='@Security21',
    user='root',
    auth_plugin='mysql_native_password'
)
cursor = connection.cursor()

print("DB connected!...")

# a function to convert the image to binary
def convertToBinaryData(filename):
    # Convert digital data to binary format
    with open(filename, 'rb') as file:
        binaryData = file.read()
    return binaryData

# a function that stores the image and letter in the DB
def insertBLOB(name, photo):
    try:
        sql_insert_blob_query = """ INSERT INTO dataset
                          (letter, image) VALUES (%s,%s)"""

        empPicture = convertToBinaryData(photo)

        # Convert data into tuple format
        insert_blob_tuple = (name, empPicture)
        cursor.execute(sql_insert_blob_query, insert_blob_tuple)
        connection.commit()

    except mysql.connector.Error as error:
        print("Failed inserting BLOB data into MySQL table {}".format(error))

# a function that processes the files and then call the Db function
def fileHandler():
    num = 1
    dataset = os.listdir('dataset')

    numbers = ['1', '2', '3', '4', '5', '6', '7', '8', '9']

    while num != (len(dataset)+1):
        data = f'binary\{num}'

        for file in os.listdir(data):
            get_dir = os.path.join(data, file)
            name = os.path.splitext(file)

            if name[0][0] in numbers:
                insertBLOB(str(name[0][1:]), get_dir)
            else:
                insertBLOB(str(name[0][:]), get_dir)
        num += 1

print("Getting the files and adding to DB, please wait...")

for i in range(3):
    fileHandler()

print("Done inserting all Images...")

# closing the sql connection when done
if connection.is_connected():
    cursor.close()
    connection.close()
    print("MySQL connection is closed")

## Runtime is 3 mins 15 secs
## Images are more lightweight after converting to binary