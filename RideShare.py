
import mysql.connector




conn = mysql.connector.connect(host = 'localhost',
                               user = 'root',
                               password = 'YourPCpassword',
                               auth_plugin = 'mysql_native_password',
                               database = 'RideShare'
                               )

cur_obj = conn.cursor()

def create_account():
    account_type = input("Are you a new rider or driver? (rider/driver): ").lower()
    if account_type == "rider":
        name = input("Enter your name: ")
        email = input("Enter your email: ")
        phone = input("Enter your phone number: ")
        cur_obj.execute("INSERT INTO Rider (name, email, phone_number) VALUES (%s, %s, %s)", (name, email, phone))
        conn.commit()
        print("Rider account created successfully!")
    elif account_type == "driver":
        name = input("Enter your name: ")
        email = input("Enter your email: ")
        phone = input("Enter your phone number: ")
        car_details = input("Enter your car details: ")
        cur_obj.execute("INSERT INTO Driver (name, email, phone_number, car_details) VALUES (%s, %s, %s, %s)", (name, email, phone, car_details))
        conn.commit()
        print("Driver account created successfully!")

# More functions for log-in, viewing rides, activating/deactivating driver mode, finding drivers, and rating...



# Function to log into an existing account
def login_account(account_type):
    if account_type == "rider":
        rider_id = input("Enter your Rider ID: ")
        cur_obj.execute("SELECT * FROM Rider WHERE rider_id = %s", (rider_id,))
        rider = cur_obj.fetchone()
        if rider:
            print(f"Welcome, {rider[1]}!")
            rider_menu(rider_id)
        else:
            print("Rider not found.")
    elif account_type == "driver":
        driver_id = input("Enter your Driver ID: ")
        cur_obj.execute("SELECT * FROM Driver WHERE driver_id = %s", (driver_id,))
        driver = cur_obj.fetchone()
        if driver:
            print(f"Welcome, {driver[1]}!")
            driver_menu(driver_id)
        else:
            print("Driver not found.")

# Function to display the driver menu
def driver_menu(driver_id):
    while True:
        print("\nDriver Menu:")
        print("1. View Rating")
        print("2. View Rides")
        print("3. Activate/Deactivate Driver Mode")
        print("4. Logout")
        choice = input("Choose an option: ")

        if choice == '1':
            view_driver_rating(driver_id)
        elif choice == '2':
            view_driver_rides(driver_id)
        elif choice == '3':
            toggle_driver_mode(driver_id)
        elif choice == '4':
            break
        else:
            print("Invalid choice. Please try again.")

# Function to display the rider menu
def rider_menu(rider_id):
    while True:
        print("\nRider Menu:")
        print("1. View Rides")
        print("2. Find a Driver")
        print("3. Rate my Driver")
        print("4. Logout")
        choice = input("Choose an option: ")

        if choice == '1':
            view_rider_rides(rider_id)
        elif choice == '2':
            find_driver(rider_id)
        elif choice == '3':
            rate_driver(rider_id)
        elif choice == '4':
            break
        else:
            print("Invalid choice. Please try again.")

# Function for drivers to view their rating
def view_driver_rating(driver_id):
    cur_obj.execute("SELECT AVG(rating) FROM Ride WHERE driver_id = %s", (driver_id,))
    rating = cur_obj.fetchone()[0]
    if rating:
        print(f"Your current rating is: {rating:.2f}")
    else:
        print("No ratings available yet.")

# Function for drivers to view all rides they have given
def view_driver_rides(driver_id):
    cur_obj.execute("SELECT * FROM Ride WHERE driver_id = %s", (driver_id,))
    rides = cur_obj.fetchall()
    if rides:
        for ride in rides:
            print(f"Ride ID: {ride[0]}, Rider ID: {ride[1]}, Pickup: {ride[3]}, Dropoff: {ride[4]}, Timestamp: {ride[5]}, Rating: {ride[6]}")
    else:
        print("No rides available.")

# Function for drivers to toggle their availability
def toggle_driver_mode(driver_id):
    cur_obj.execute("SELECT driver_mode FROM Driver WHERE driver_id = %s", (driver_id,))
    current_mode = cur_obj.fetchone()[0]
    new_mode = not current_mode
    cur_obj.execute("UPDATE Driver SET driver_mode = %s WHERE driver_id = %s", (new_mode, driver_id))
    conn.commit()
    status = "active" if new_mode else "inactive"
    print(f"Driver mode is now {status}.")

# Function for riders to view all their rides
def view_rider_rides(rider_id):
    cur_obj.execute("SELECT * FROM Ride WHERE rider_id = %s", (rider_id,))
    rides = cur_obj.fetchall()
    if rides:
        for ride in rides:
            print(f"Ride ID: {ride[0]}, Driver ID: {ride[2]}, Pickup: {ride[3]}, Dropoff: {ride[4]}, Timestamp: {ride[5]}, Rating: {ride[6]}")
    else:
        print("No rides available.")

# Function for riders to find an available driver
def find_driver(rider_id):
    cur_obj.execute("SELECT driver_id FROM Driver WHERE driver_mode = TRUE")
    driver = cur_obj.fetchone()
    if driver:
        driver_id = driver[0]
        pickup = input("Enter your pickup location: ")
        dropoff = input("Enter your dropoff location: ")
        cur_obj.execute("INSERT INTO Ride (rider_id, driver_id, pickup_location, dropoff_location, ride_timestamp) VALUES (%s, %s, %s, %s, NOW())",
                       (rider_id, driver_id, pickup, dropoff))
        conn.commit()
        print(f"Ride created! Driver {driver_id} will pick you up at {pickup}.")
    else:
        print("No drivers available right now. Please try again later.")

# Function for riders to rate their driver
def rate_driver(rider_id):
    cur_obj.execute("SELECT * FROM Ride WHERE rider_id = %s ORDER BY ride_timestamp DESC LIMIT 1", (rider_id,))
    recent_ride = cur_obj.fetchone()
    if recent_ride:
        print(f"Most recent ride - Ride ID: {recent_ride[0]}, Driver ID: {recent_ride[2]}, Pickup: {recent_ride[3]}, Dropoff: {recent_ride[4]}, Timestamp: {recent_ride[5]}")
        confirm = input("Is this the correct ride to rate? (yes/no): ").lower()
        if confirm == 'no':
            ride_id = input("Enter the Ride ID you want to rate: ")
            cur_obj.execute("SELECT * FROM Ride WHERE ride_id = %s AND rider_id = %s", (ride_id, rider_id))
            ride = cur_obj.fetchone()
            if ride:
                print(f"Ride ID: {ride[0]}, Driver ID: {ride[2]}, Pickup: {ride[3]}, Dropoff: {ride[4]}, Timestamp: {ride[5]}")
            else:
                print("Invalid Ride ID.")
                return
        else:
            ride_id = recent_ride[0]

        rating = float(input("Enter your rating for this ride (1-5): "))
        cur_obj.execute("UPDATE Ride SET rating = %s WHERE ride_id = %s", (rating, ride_id))
        conn.commit()
        print("Thank you for your feedback!")
    else:
        print("No rides available to rate.")

# Main function
def main():
    while True:
        user_type = input("Are you an existing rider, driver, or new user? (rider/driver/new): ").lower()
        if user_type == "new":
            create_account()
        elif user_type == "rider" or user_type == "driver":
            login_account(user_type)
        else:
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    main()



main()













conn.close()





# More functions for log-in, viewing rides, activating/deactivating driver mode, finding drivers, and rating...



# Function to log into an existing account
def login_account(account_type):
    if account_type == "rider":
        rider_id = input("Enter your Rider ID: ")
        cur_obj.execute("SELECT * FROM Rider WHERE rider_id = %s", (rider_id,))
        rider = cur_obj.fetchone()
        if rider:
            print(f"Welcome, {rider[1]}!")
            rider_menu(rider_id)
        else:
            print("Rider not found.")
    elif account_type == "driver":
        driver_id = input("Enter your Driver ID: ")
        cur_obj.execute("SELECT * FROM Driver WHERE driver_id = %s", (driver_id,))
        driver = cur_obj.fetchone()
        if driver:
            print(f"Welcome, {driver[1]}!")
            driver_menu(driver_id)
        else:
            print("Driver not found.")

# Function to display the driver menu
def driver_menu(driver_id):
    while True:
        print("\nDriver Menu:")
        print("1. View Rating")
        print("2. View Rides")
        print("3. Activate/Deactivate Driver Mode")
        print("4. Logout")
        choice = input("Choose an option: ")

        if choice == '1':
            view_driver_rating(driver_id)
        elif choice == '2':
            view_driver_rides(driver_id)
        elif choice == '3':
            toggle_driver_mode(driver_id)
        elif choice == '4':
            break
        else:
            print("Invalid choice. Please try again.")

# Function to display the rider menu
def rider_menu(rider_id):
    while True:
        print("\nRider Menu:")
        print("1. View Rides")
        print("2. Find a Driver")
        print("3. Rate my Driver")
        print("4. Logout")
        choice = input("Choose an option: ")

        if choice == '1':
            view_rider_rides(rider_id)
        elif choice == '2':
            find_driver(rider_id)
        elif choice == '3':
            rate_driver(rider_id)
        elif choice == '4':
            break
        else:
            print("Invalid choice. Please try again.")

# Function for drivers to view their rating
def view_driver_rating(driver_id):
    cur_obj.execute("SELECT AVG(rating) FROM Ride WHERE driver_id = %s", (driver_id,))
    rating = cur_obj.fetchone()[0]
    if rating:
        print(f"Your current rating is: {rating:.2f}")
    else:
        print("No ratings available yet.")

# Function for drivers to view all rides they have given
def view_driver_rides(driver_id):
    cur_obj.execute("SELECT * FROM Ride WHERE driver_id = %s", (driver_id,))
    rides = cur_obj.fetchall()
    if rides:
        for ride in rides:
            print(f"Ride ID: {ride[0]}, Rider ID: {ride[1]}, Pickup: {ride[3]}, Dropoff: {ride[4]}, Timestamp: {ride[5]}, Rating: {ride[6]}")
    else:
        print("No rides available.")

# Function for drivers to toggle their availability
def toggle_driver_mode(driver_id):
    cur_obj.execute("SELECT driver_mode FROM Driver WHERE driver_id = %s", (driver_id,))
    current_mode = cur_obj.fetchone()[0]
    new_mode = not current_mode
    cur_obj.execute("UPDATE Driver SET driver_mode = %s WHERE driver_id = %s", (new_mode, driver_id))
    conn.commit()
    status = "active" if new_mode else "inactive"
    print(f"Driver mode is now {status}.")

# Function for riders to view all their rides
def view_rider_rides(rider_id):
    cur_obj.execute("SELECT * FROM Ride WHERE rider_id = %s", (rider_id,))
    rides = cur_obj.fetchall()
    if rides:
        for ride in rides:
            print(f"Ride ID: {ride[0]}, Driver ID: {ride[2]}, Pickup: {ride[3]}, Dropoff: {ride[4]}, Timestamp: {ride[5]}, Rating: {ride[6]}")
    else:
        print("No rides available.")

# Function for riders to find an available driver
def find_driver(rider_id):
    cur_obj.execute("SELECT driver_id FROM Driver WHERE driver_mode = TRUE")
    driver = cur_obj.fetchone()
    if driver:
        driver_id = driver[0]
        pickup = input("Enter your pickup location: ")
        dropoff = input("Enter your dropoff location: ")
        cur_obj.execute("INSERT INTO Ride (rider_id, driver_id, pickup_location, dropoff_location, ride_timestamp) VALUES (%s, %s, %s, %s, NOW())",
                       (rider_id, driver_id, pickup, dropoff))
        conn.commit()
        print(f"Ride created! Driver {driver_id} will pick you up at {pickup}.")
    else:
        print("No drivers available right now. Please try again later.")

# Function for riders to rate their driver
def rate_driver(rider_id):
    cur_obj.execute("SELECT * FROM Ride WHERE rider_id = %s ORDER BY ride_timestamp DESC LIMIT 1", (rider_id,))
    recent_ride = cur_obj.fetchone()
    if recent_ride:
        print(f"Most recent ride - Ride ID: {recent_ride[0]}, Driver ID: {recent_ride[2]}, Pickup: {recent_ride[3]}, Dropoff: {recent_ride[4]}, Timestamp: {recent_ride[5]}")
        confirm = input("Is this the correct ride to rate? (yes/no): ").lower()
        if confirm == 'no':
            ride_id = input("Enter the Ride ID you want to rate: ")
            cur_obj.execute("SELECT * FROM Ride WHERE ride_id = %s AND rider_id = %s", (ride_id, rider_id))
            ride = cur_obj.fetchone()
            if ride:
                print(f"Ride ID: {ride[0]}, Driver ID: {ride[2]}, Pickup: {ride[3]}, Dropoff: {ride[4]}, Timestamp: {ride[5]}")
            else:
                print("Invalid Ride ID.")
                return
        else:
            ride_id = recent_ride[0]

        rating = float(input("Enter your rating for this ride (1-5): "))
        cur_obj.execute("UPDATE Ride SET rating = %s WHERE ride_id = %s", (rating, ride_id))
        conn.commit()
        print("Thank you for your feedback!")
    else:
        print("No rides available to rate.")

# Main function
def main():
    while True:
        user_type = input("Are you an existing rider, driver, or new user? (rider/driver/new): ").lower()
        if user_type == "new":
            create_account()
        elif user_type == "rider" or user_type == "driver":
            login_account(user_type)
        else:
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    main()



main()













conn.close()



