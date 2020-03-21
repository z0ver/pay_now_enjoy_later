# this file contains all functionality necessary to connect to the database
import mysql.connector

host = "localhost"
user = "root"
passwd = "A1!n3_578"  # extract as env variable


def getDbConnection():
    # Get database connection
    try:
        connection = mysql.connector.connect(host=host, user=user, passwd=passwd, database='test', charset="utf8")
        return connection
    except mysql.connector.Error as error:
        print("Failed to connect to database {}".format(error))


def closeDbConnection(connection):
    # Close database connection
    try:
        connection.close()
    except mysql.connector.Error as error:
        print("Failed to close database connection {}".format(error))


def printServerInformation():
    try:
        connection = getDbConnection()

        if connection.is_connected():
            db_Info = connection.get_server_info()
            print("Connected to MySQL database... MySQL Server version is ", db_Info)
            cursor = connection.cursor()
            cursor.execute("select database();")
            record = cursor.fetchall()
            print("Your connected to - ", record)

        closeDbConnection(connection)
    except mysql.connector.Error as error:
        print("Failed to get server information {}".format(error))
    finally:
        cursor.close()
        connection.close()


def getShopsByZipCode(zipcode):
    try:
        connection = getDbConnection()
        if connection.is_connected():
            cursor = connection.cursor()
            sqlstatement = """SELECT * FROM Shops WHERE zipCode=%s"""
            cursor.execute(sqlstatement, (zipcode,))
            records = cursor.fetchall()
    except mysql.connector.Error as error:
        print("Failed to read data from Shops {}".format(error))
    finally:
        cursor.close()
        connection.close()
        return records  # how to handle empty return?


def getShopsByName(name):
    try:
        connection = getDbConnection()
        if connection.is_connected():
            cursor = connection.cursor()
            sqlstatement = """SELECT * FROM Shops WHERE name=%s"""
            cursor.execute(sqlstatement, (name,))
            records = cursor.fetchall()
    except mysql.connector.Error as error:
        print("Failed to read data from Shops {}".format(error))
    finally:
        cursor.close()
        connection.close()
        return records  # how to handle empty return?


def getOffersByShopID(shop_id):
    try:
        connection = getDbConnection()
        if connection.is_connected():
            cursor = connection.cursor()
            sqlstatement = """SELECT * FROM Offers WHERE shop_ID=%s"""
            cursor.execute(sqlstatement, (shop_id,))
            records = cursor.fetchall()
    except mysql.connector.Error as error:
        print("Failed to read data from Offers {}".format(error))
    finally:
        cursor.close()
        connection.close()
        return records  # how to handle empty return?


def insertUser(emailAddress, firstname, lastname, phoneNumber, passwordHash, passwordSalt, token, isVerified, isOwner):
    try:
        connection = getDbConnection()
        if connection.is_connected():
            cursor = connection.cursor()
            sqlstatement = """INSERT INTO User (emailAddress, firstname, lastname, phoneNumber, passwordHash, passwordSalt, token, isVerified, isOwner) 
                           VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
            data = (emailAddress, firstname, lastname, phoneNumber, passwordHash, passwordSalt, token, False, isOwner)
            cursor.execute(sqlstatement, data)
            connection.commit()

            print(cursor.rowcount, "Record inserted successfully into User table")

    except mysql.connector.Error as error:
        print("Failed to insert customer {}".format(error))
    finally:
        cursor.close()
        connection.close()


def insertCouponForCustomer(offer_ID, customer_ID, original_value, current_value, status, date_of_purchase):
    try:
        connection = getDbConnection()
        if connection.is_connected():
            cursor = connection.cursor()
            sqlstatement = """INSERT INTO Coupons (offer_ID, customer_ID, original_value, current_value, status, date_of_purchase)
                           VALUES (%s, %s, %s, %s, %s, %s)"""
            data = (offer_ID, customer_ID, original_value, current_value, status, date_of_purchase)
            cursor.execute(sqlstatement, data)
            connection.commit()
            print(cursor.rowcount, "Record inserted successfully into Coupons table")

    except mysql.connector.Error as error:
        print("Failed to insert customer {}".format(error))
    finally:
        cursor.close()
        connection.close()

def insertShopDetails(shop_ID,owner_email,name,zipCode,city,street,description,Logo_URL,Link_Website,phoneNumber):
    inserted_row = None
    try:
        connection = getDbConnection()
        if connection.is_connected():
            cursor = connection.cursor()
            sqlstatement = """INSERT INTO Shops (shop_ID,owner_email,name,zipCode,city,street,description,Logo_URL,Link_Website,phoneNumber) 
                            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
            data = (shop_ID,owner_email,name,zipCode,city,street,description,Logo_URL,Link_Website,phoneNumber)
            cursor.execute(sqlstatement, data)
            inserted_row = cursor.lastrowid
            connection.commit()
            print(cursor.rowcount, "Record(s) inserted successfully into Shops table")

    except mysql.connector.Error as error:
        print("Failed to insert shop {}".format(error))
    finally:
        cursor.close()
        connection.close()
    if inserted_row:
        return {'success':True,'inserted_row':inserted_row}
    else:
        return {'success':False,'inserted_row':inserted_row}

def updateShowDetails(shop_ID,field_name,field_value):
    updated_row = None
    try:
        connection = getDbConnection()
        if connection.is_connected():
            cursor = connection.cursor()
            sqlstatement = """UPDATE Shops SET %s = %s WHERE shop_ID=%s"""
            data = (field_name, field_value, shop_ID)
            cursor.execute(sqlstatement, data)
            updated_row = cursor.lastrowid
            connection.commit()
            print(cursor.rowcount, "Record(s) updated successfully in Shops table")
    except mysql.connector.Error as error:
        print("Failed to update shop {}".format(error))
    finally:
        cursor.close()
        connection.close()
    if updated_row:
        return {'success':True,'updated_row':updated_row}
    else:
        return {'success':False,'updated_row':updated_row}

def deleteShop(shop_ID):
    deletion_done = False
    try:
        connection = getDbConnection()
        if connection.is_connected():
            cursor = connection.cursor()
            sqlstatement = """DELETE FROM Shops WHERE shop_ID = %s"""
            data = (shop_ID)
            cursor.execute(sqlstatement, data)
            connection.commit()
            print(cursor.rowcount, "Record deleted successfully in Shops table")
            deletion_done = True
    except mysql.connector.Error as error:
        print("Failed to delete shop {}".format(error))
    finally:
        cursor.close()
        connection.close()
    return {'success': deletion_done}

def deleteCoupon(coupon_ID):
    deletion_done = False
    try:
        connection = getDbConnection()
        if connection.is_connected():
            cursor = connection.cursor()
            sqlstatement = """DELETE FROM coupons WHERE coupons_ID = %s"""
            data = (coupon_ID)
            cursor.execute(sqlstatement, data)
            connection.commit()
            print(cursor.rowcount, "Record deleted successfully in Coupons table")
            deletion_done = True
    except mysql.connector.Error as error:
        print("Failed to delete coupon {}".format(error))
    finally:
        cursor.close()
        connection.close()
    return {'success': deletion_done}




