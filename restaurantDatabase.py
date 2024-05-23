import mysql.connector
from mysql.connector import Error

class RestaurantDatabase:
    def __init__(self, host="localhost", port="3306", database="restaurant_reservations", user='root', password='Sammypoo2'):
        self.host = host
        self.port = port
        self.database = database
        self.user = user
        self.password = password
        self.connection = None
        self.connect()

    def connect(self):
        
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                port=self.port,
                database=self.database,
                user=self.user,
                password=self.password)
            if self.connection.is_connected():
                print("Successfully connected to the database")
        except Error as e:
            print("Error while connecting to MySQL", e)

    def close_connection(self):
        
        if self.connection.is_connected():
            self.connection.close()
            print("Database connection closed")

    def add_reservation(self, customer_name, reservation_time, number_of_guests, special_requests):
        
        try:
            cursor = self.connection.cursor()
            query = "CALL addReservation(%s, %s, %s, %s, %s)"
            reservation_data = (customer_name, '', reservation_time, number_of_guests, special_requests)
            cursor.execute(query, reservation_data)
            self.connection.commit()
            print("Reservation added successfully")
        except Error as e:
            print("Error adding reservation:", e)
        finally:
            cursor.close()
            self.close_connection()

    def get_all_reservations(self):
        
        try:
            cursor = self.connection.cursor()
            query = "SELECT * FROM reservations"
            cursor.execute(query)
            records = cursor.fetchall()
            return records
        except Error as e:
            print("Error retrieving reservations:", e)
        finally:
            cursor.close()
            self.close_connection()

    def add_customer(self, customer_name, contact_info):
        
        try:
            cursor = self.connection.cursor()
            query = "INSERT INTO customers (customerName, contactInfo) VALUES (%s, %s)"
            cursor.execute(query, (customer_name, contact_info))
            self.connection.commit()
            print("Customer added successfully")
        except Error as e:
            print("Error adding customer:", e)
        finally:
            cursor.close()
            self.close_connection()

    def get_customer_preferences(self, customer_id):
        
        try:
            cursor = self.connection.cursor()
            query = "SELECT * FROM diningpreferences WHERE customerId = %s"
            cursor.execute(query, (customer_id,))
            preferences = cursor.fetchall()
            return preferences
        except Error as e:
            print("Error retrieving customer preferences:", e)
        finally:
            cursor.close()
            self.close_connection()

    def add_special_request(self, reservation_id, special_requests):
        
        try:
            cursor = self.connection.cursor()
            query = "CALL addSpecialRequest(%s, %s)"
            cursor.execute(query, (reservation_id, special_requests))
            self.connection.commit()
            print("Special request added successfully")
        except Error as e:
            print("Error adding special request:", e)
        finally:
            cursor.close()
            self.close_connection()

    def find_reservations(self, customer_id):
        
        try:
            cursor = self.connection.cursor()
            query = "CALL findReservations(%s)"
            cursor.execute(query, (customer_id,))
            reservations = cursor.fetchall()
            return reservations
        except Error as e:
            print("Error finding reservations:", e)
        finally:
            cursor.close()
            self.close_connection()

    def delete_reservation(self, reservation_id):
        
        try:
            cursor = self.connection.cursor()
            query = "DELETE FROM reservations WHERE reservationId = %s"
            cursor.execute(query, (reservation_id,))
            self.connection.commit()
            print("Reservation deleted successfully")
        except Error as e:
            print("Error deleting reservation:", e)
        finally:
            cursor.close()
            self.close_connection()

    def search_preferences(self, customer_id):
        
        try:
            cursor = self.connection.cursor()
            query = "SELECT * FROM diningpreferences WHERE customerId = %s"
            cursor.execute(query, (customer_id,))
            preferences = cursor.fetchall()
            return preferences
        except Error as e:
            print("Error searching preferences:", e)
        finally:
            cursor.close()
            self.close_connection()

    def view_all_reservations(self):
        
        try:
            cursor = self.connection.cursor()
            query = "SELECT * FROM reservations"
            cursor.execute(query)
            reservations = cursor.fetchall()
            return reservations
        except Error as e:
            print("Error retrieving all reservations:", e)
        finally:
            cursor.close()
            self.close_connection()
