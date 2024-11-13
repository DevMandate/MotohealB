from flask import *
from flask_sqlalchemy import SQLAlchemy
import pymysql
import datetime as dt
booking_date = dt.datetime.now()


motoheal = Flask(__name__)


# we are going to create a secret a secret key that will enamble us to secure our session just incase of an attack. The secret key is just randomized string of values

motoheal.secret_key = "wyeriu346789yq3894yithkagfi7uerjg345qr356ghvnhf"



def db_connection():
    return pymysql.connect(host ='localhost', user ='root' , password = '', database = 'flask_prac')

@motoheal.route("/")
def home():
    connection = db_connection()

    # Toyota Query
    sql = "SELECT * FROM `cars` WHERE make = 'Toyota'"

    cursor = connection.cursor()
    cursor.execute(sql)
    Toyota = cursor.fetchall()
    
    # Nissan Query
    sql2 = "SELECT * FROM `cars` WHERE make = 'Nissan'"
    cursor2 = connection.cursor()
    cursor2.execute(sql2)
    Nissan = cursor2.fetchall()

    # Mercedes Query
    sql3 = "SELECT * FROM `cars` WHERE make = 'Mercedes-Benz'"
    cursor3 = connection.cursor()
    cursor3.execute(sql3)
    Mercedes = cursor3.fetchall()

    # Honda query
    sql4 = "SELECT * FROM `cars` WHERE make = 'Honda'"
    cursor4 = connection.cursor()
    cursor4.execute(sql4)
    Honda = cursor4.fetchall()


    return render_template('index.html', Toyota = Toyota , Nissan = Nissan , Mercedes = Mercedes , Honda = Honda)



@motoheal.route('/singlecar/<car_id>')
def singlecar(car_id):
    connection = db_connection()

    sql = "SELECT * FROM `cars` WHERE car_id = %s"

    cursor = connection.cursor()
    cursor.execute(sql, car_id)
    car = cursor.fetchone()


    category = car[1]
    sql2 = "SELECT * FROM `cars` WHERE make = %s"
    cursor2 = connection.cursor()
    cursor2.execute(sql2, category)
    similar = cursor2.fetchall()

        
    return render_template("singlecar.html", car = car, similar = similar)


# Route to display all car records with edit and delete options
@motoheal.route("/cars")
def cars():
    connection = db_connection()
    sql = "SELECT * FROM `cars`"
    cursor = connection.cursor()
    cursor.execute(sql)
    all_cars = cursor.fetchall()
    return render_template('results.html', cars=all_cars)

# Route for editing a car record
@motoheal.route("/edit_car/<string:car_id>", methods=["GET", "POST"])
def edit_car(car_id):
    connection = db_connection()
    cursor = connection.cursor()

    if request.method == "POST":
        make = request.form["make"]
        model = request.form["model"]
        year = request.form["year"]
        price = request.form["price"]
        transmission = request.form["transmission"]
        fuel_type = request.form["fuel_type"]
        engine_size = request.form["engine_size"]
        image_url = request.form["image_url"]
        description = request.form["description"]
        dealers_id = request.form["dealers_id"]

        sql = """UPDATE `cars` SET make=%s, model=%s, year=%s, price=%s, 
                 transmission=%s, fuel_type=%s, engine_size=%s, image_url=%s, 
                 description=%s, dealers_id=%s WHERE car_id=%s"""
        cursor.execute(sql, (make, model, year, price, transmission, fuel_type,
                             engine_size, image_url, description, dealers_id, car_id))
        connection.commit()
        return redirect(url_for("cars"))

    else:
        sql = "SELECT * FROM `cars` WHERE car_id = %s"
        cursor.execute(sql, (car_id,))
        car = cursor.fetchone()
        return render_template("edit_car.html", car=car)


# Route for deleting a car record
@motoheal.route("/delete_car/<string:car_id>")
def delete_car(car_id):
    connection = db_connection()
    sql = "DELETE FROM `cars` WHERE car_id = %s"
    cursor = connection.cursor()
    cursor.execute(sql, (car_id,))
    connection.commit()
    return redirect(url_for("cars"))



# Register route
@motoheal.route('/register' ,  methods =['POST' , 'GET'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    else:
        username = request.form['username']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        password1 = request.form['password1']
        password2 = request.form['password2']
        email = request.form['email']
        phone = request.form['phone']
        profile_picture = request.files['profile_picture']
        profile_picture.save("static/images/" + profile_picture.filename)

        if password1 != password2:
            return render_template("register.hmtl", error = 'Passwords do match')
        elif len(password1) < 6:
            return render_template('register.html', error = "Password length must be more than 6" )
        else:
            # Create a db connection
            connection = db_connection()

            # Structure sql query to enter a new user into the database
            sql = "INSERT INTO `users`(`username`, `first_name`, `last_name`, `password`, `email`, `phone_number`, `profile_picture`) VALUES (%s, %s, %s, %s, %s, %s, %s)"

            # create a variable that will hold all the data gotten from the form
            data = (username, first_name, last_name, password1, email, phone, profile_picture.filename)

            # create a cursor
            cursor = connection.cursor()

            # use the cursor to execute the sql
            cursor.execute(sql, data)

            # finish the transaction by use of the commit function
            connection.commit()

            return render_template('register.html', success = "User Registered Successfully")



@motoheal.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    else:
        # get the details entered on the form and store them in a variable
        username = request.form["username"]
        password = request.form["password"]
        # create a db connection
        connection = db_connection()
        # create an sql query. The %s is a placeholder, to be replaced with actual data when we execute the sql
        sql = "SELECT * FROM `users` WHERE username = %s and password=%s"
        # create a varible that will hold the data gotten from the form
        data = (username, password)
        # create a cursor that will help to execute the sql
        cursor = connection.cursor()
        # execute the query
        cursor.execute(sql, data)

        # fetch one person
        user = cursor.fetchone()

        if cursor.rowcount== 0:
            return render_template("login.html", error="Invalid Credentials")
        else:
            session["key"] = username
            session["profile_picture"] = user[6]
            return redirect("/")

@motoheal.route('/logout')
def logout():
    # remobe user from the session
    session.clear()
    return redirect('/')




@motoheal.route('/vehicles', methods=['GET'])
def vehicle_list():
    connection = db_connection()
    cursor = connection.cursor()
    
    # Fetch all vehicles
    sql = "SELECT * FROM vehicles"
    cursor.execute(sql)
    vehicles = cursor.fetchall()
    
    return render_template('vehicles.html', vehicles=vehicles)
    

@motoheal.route('/vehicle-list/edit/<int:id>', methods=['GET', 'POST'])
def edit_vehicle(id):
    connection = db_connection()
    cursor = connection.cursor()
    
    if request.method == 'POST':
        # Get form data
        make = request.form['make']
        model = request.form['model']
        year = request.form['year']
        price = request.form['price']
        mileage = request.form['mileage']
        fuel_type = request.form['fuel_type']
        transmission = request.form['transmission']
        color = request.form['color']
        description = request.form['description']
        image_url = request.form['image_url']
        availability = request.form.get('availability', 'off') == 'on'

        # Update query
        sql = """UPDATE vehicles 
                 SET make=%s, model=%s, year=%s, price=%s, mileage=%s,
                     fuel_type=%s, transmission=%s, color=%s, description=%s,
                     image_url=%s, availability=%s
                 WHERE id=%s"""
        cursor.execute(sql, (make, model, year, price, mileage, fuel_type,
                             transmission, color, description, image_url,
                             availability, id))
        connection.commit()
        
        return redirect(url_for('vehicle_list'))
    else:
        # Fetch vehicle details for edit
        sql = "SELECT * FROM vehicles WHERE id = %s"
        cursor.execute(sql, (id,))
        vehicle = cursor.fetchone()
        
        return render_template('edit_vehicle.html', vehicle=vehicle)

    

@motoheal.route('/vehicle-list/delete/<int:id>', methods=['POST'])
def delete_vehicle(id):
    connection = db_connection()
    cursor = connection.cursor()
    
    # Delete query
    sql = "DELETE FROM vehicles WHERE id = %s"
    cursor.execute(sql, (id,))
    connection.commit()
    
    return redirect(url_for('vehicle_list'))





    

@motoheal.route('/singlevehicle/<id>')
def single_vehicle(id):
    connection = db_connection()
    cursor = connection.cursor()
    sql = "SELECT * FROM `vehicles` WHERE id = %s"  # Fetch single vehicle by ID
    cursor.execute(sql, (id,))
    singlevehicle = cursor.fetchone()

    category = singlevehicle[2]
    sql2 = "SELECT * FROM `vehicles` WHERE make = %s"
    cursor2 = connection.cursor()
    cursor2.execute(sql2, category)
    similar = cursor2.fetchall()

    return render_template("singlevehicle.html", singlevehicle=singlevehicle, similar = similar)




# Route for motorcycles page
@motoheal.route('/motorcycles', methods=['GET'])
def motorcycles():
    connection = db_connection()
    cursor = connection.cursor()
    sql = "SELECT * FROM `motorcycles`"  # Fetch all motorcycles
    cursor.execute(sql)
    motorcycles = cursor.fetchall()  # Retrieve all motorcycles as a list of tuples

    return render_template('motorcycles.html', motorcycles=motorcycles)


# Route for single motorcycle page
@motoheal.route('/singlemotorcycle/<id>')
def single_motorcycle(id):
    connection = db_connection()
    cursor = connection.cursor()
    sql = "SELECT * FROM `motorcycles` WHERE id = %s"  # Fetch single motorcycle by ID
    cursor.execute(sql, (id,))
    singlemotorcycle = cursor.fetchone()

    return render_template("singlemotorcycle.html", singlemotorcycle=singlemotorcycle)





# Route for rental services page
@motoheal.route('/rentals', methods=['GET'])
def rentals():
    connection = db_connection()
    cursor = connection.cursor()
    sql = "SELECT * FROM `rental_services`"  # Fetch all rental services
    cursor.execute(sql)
    rentals = cursor.fetchall()  # Retrieve all rentals as a list of tuples

    return render_template('rentals.html', rentals=rentals)

# Route to display available and unavailable rental services
@motoheal.route('/rentals/availability', methods=['GET'])
def rentals_availability():
    connection = db_connection()
    cursor = connection.cursor()

    # SQL queries to fetch available and unavailable rental services
    available_sql = "SELECT * FROM `rental_services` WHERE `availability` = TRUE"
    unavailable_sql = "SELECT * FROM `rental_services` WHERE `availability` = FALSE"

    cursor.execute(available_sql)
    available_rentals = cursor.fetchall()

    cursor.execute(unavailable_sql)
    unavailable_rentals = cursor.fetchall()

    connection.close()
    
    return render_template('rentals_availability.html', available_rentals=available_rentals, unavailable_rentals=unavailable_rentals)


# Route to edit a rental service
@motoheal.route('/rentals/edit/<int:id>', methods=['GET', 'POST'])
def edit_rental(id):
    connection = db_connection()
    cursor = connection.cursor()
    
    if request.method == 'POST':
        # Retrieve form data
        vehicle_type = request.form['vehicle_type']
        rental_price = request.form['rental_price']
        rental_duration = request.form['rental_duration']
        availability = True if request.form.get('availability') else False
        description = request.form['description']
        image_name = request.form['image_name']

        # Update the rental service record
        update_sql = """UPDATE `rental_services` SET 
                        `vehicle_type` = %s, `rental_price` = %s, 
                        `rental_duration` = %s, `availability` = %s,
                        `description` = %s, `image_url` = %s 
                        WHERE `id` = %s"""
        cursor.execute(update_sql, (vehicle_type, rental_price, rental_duration, availability, description, image_name, id))
        connection.commit()
        connection.close()
        
        return redirect('/rentals/availability')

    # Fetch rental data for the form
    cursor.execute("SELECT * FROM `rental_services` WHERE `id` = %s", (id,))
    rental = cursor.fetchone()
    connection.close()

    return render_template('edit_rental.html', rental=rental)


# Route to delete a rental service
@motoheal.route('/rentals/delete/<int:id>', methods=['GET'])
def delete_rental(id):
    connection = db_connection()
    cursor = connection.cursor()

    delete_sql = "DELETE FROM `rental_services` WHERE `id` = %s"
    cursor.execute(delete_sql, (id,))
    connection.commit()
    connection.close()

    return redirect('/rentals/availability')



# Route for single rental service page
@motoheal.route('/singlerental/<id>', methods=['GET', 'POST'])
def single_rental(id):
    connection = db_connection()
    cursor = connection.cursor()
    sql = "SELECT * FROM `rental_services` WHERE id = %s"  # Fetch single rental by ID
    cursor.execute(sql, (id,))
    singlerental = cursor.fetchone()

    if request.method == 'POST':
        # Retrieve booking form data
        full_name = request.form['full_name']
        email = request.form['email']
        phone = request.form['phone']
        booking_date = dt.datetime.now()  # Use datetime.now() after importing datetime

        # Insert booking data into `rental_bookings` table
        booking_sql = """
            INSERT INTO `rental_bookings` (rental_id, full_name, email, phone, booking_date)
            VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(booking_sql, (id, full_name, email, phone, booking_date))
        connection.commit()

        flash('Your booking has been submitted successfully!', 'success')
        return redirect(url_for('single_rental', id=id))

    return render_template("singlerental.html", singlerental=singlerental)




# Route to display all rental booking details
@motoheal.route('/rentaldetails', methods=['GET'])
def rental_details():
    connection = db_connection()
    cursor = connection.cursor()
    sql = "SELECT * FROM `rental_bookings`"  # Fetch all bookings
    cursor.execute(sql)
    bookings = cursor.fetchall()  # Retrieve all rows

    return render_template("rentaldetails.html", bookings=bookings)







# Route for accessories page
@motoheal.route('/accessories', methods=['GET'])
def accessories():
    connection = db_connection()
    cursor = connection.cursor()
    sql = "SELECT * FROM `accessories`"  # Fetch all accessories
    cursor.execute(sql)
    accessories = cursor.fetchall()  # Retrieve all accessories as a list of tuples

    






    return render_template('accessories.html', accessories=accessories)


# Route for single accessory page
@motoheal.route('/singleaccessory/<id>')
def single_accessory(id):
    connection = db_connection()
    cursor = connection.cursor()
    sql = "SELECT * FROM `accessories` WHERE id = %s"  # Fetch single accessory by ID
    cursor.execute(sql, (id,))
    singleaccessory = cursor.fetchone()

    if singleaccessory is None:
        return "Accessory not found", 404  # Return a 404 error if not found

    category = singleaccessory[2]
    sql2 = "SELECT * FROM `accessories` WHERE category = %s"
    cursor2 = connection.cursor()
    cursor2.execute(sql2, (category,))
    similar = cursor2.fetchall()

    return render_template("singleaccessory.html", singleaccessory=singleaccessory, similar=similar)





@motoheal.route('/blog', methods = ['POST' , 'GET'])
def blog():
    if request.method == 'GET':
        return render_template('blog.html')





@motoheal.route('/news', methods = ['POST' , 'GET'])
def news():
    if request.method == 'GET':
        return render_template('news.html')


@motoheal.route('/contact', methods = ['POST' , 'GET'])
def contact():
    if request.method == 'GET':
        return render_template('contact.html')
    elif request.method == 'POST':
        # Retrieve form data
        full_name = request.form['full_name']
        email = request.form['email']
        subject = request.form['subject']
        message = request.form['message']
        
        # Database connection and insertion
        connection = db_connection()
        cursor = connection.cursor()
        
        # Insert query
        sql = """
            INSERT INTO contact_form_submissions (full_name, email, subject, message)
            VALUES (%s, %s, %s, %s)
        """
        cursor.execute(sql, (full_name, email, subject, message))
        connection.commit()
        
        # Provide user feedback
        flash("Your message has been submitted successfully!", "success")
        
        # Redirect after submission
        return redirect(url_for('contact'))


@motoheal.route('/retrieve_contacts', methods=['GET'])
def retrieve_contacts():
    connection = db_connection()
    cursor = connection.cursor()
    sql = "SELECT * FROM contact_form_submissions"  # Fetch all contact submissions
    cursor.execute(sql)
    contacts = cursor.fetchall()  # Retrieve all rows

    return render_template("retrievecontacts.html", contacts=contacts)










@motoheal.route("/upload", methods = ['POST', 'GET'])
def upload():
    if request.method == 'GET':
        return render_template('upload.html')
    else:
        registration_plate = request.form['carid']
        make = request.form['make']
        model = request.form['model']
        year = request.form['year']
        price = request.form['price']
        transmission = request.form['transmission']
        fuel = request.form['fuel']
        enginecc = request.form['cc']
        image_url = request.files['imageUrl']
        image_url.save("static/images/" + image_url.filename)
        description = request.form['description']
        dealer_id = request.form['dealersId']


        connection = db_connection()


        sql = "INSERT INTO `cars`(`car_id`, `make`, `model`, `year`, `price`, `transmission`, `fuel_type`, `engine_size`, `image_url`, `description`, `dealers_id`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"


        data = (registration_plate, make, model, year, price, transmission, fuel, enginecc, image_url.filename, description, dealer_id)

        cursor = connection.cursor()

        cursor.execute(sql, data)

        connection.commit()
        return render_template('upload.html', success = "Car uploaded successfully ")
    


@motoheal.route("/uploadVehicle", methods=['POST', 'GET'])
def upload_vehicle():
    if request.method == 'GET':
        return render_template('uploadVehicle.html')
    else:
        registration_plate = request.form['vehicle_id']  
        make = request.form['make']
        model = request.form['model']
        year = request.form['year']
        price = request.form['price']
        mileage = request.form['mileage']
        transmission = request.form['transmission']
        fuel = request.form['fuel_type']
        color = request.form['color']
        image_url = request.files['imageUrl']
        image_url.save("static/images/" + image_url.filename)
        description = request.form['description']
        availability = request.form.get('availability', True) 

        connection = db_connection()

        sql = """
        INSERT INTO `vehicles`(
            `vehicle_id`, `make`, `model`, `year`, `price`, `mileage`, 
            `transmission`, `fuel_type`, `color`, `image_url`, `description`, `availability`
        ) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """

        data = (
            registration_plate, make, model, year, price, mileage,
            transmission, fuel, color, image_url.filename, description, availability
        )

        cursor = connection.cursor()

        cursor.execute(sql, data)
        connection.commit()

        return render_template('uploadVehicle.html', success="Vehicle uploaded successfully")



@motoheal.route("/uploadMotorcycle", methods=['POST', 'GET'])
def upload_motorcycle():
    if request.method == 'GET':
        return render_template('uploadMotorcycle.html')
    else:
        make = request.form['make']
        model = request.form['model']
        year = request.form['year']
        price = request.form['price']
        engine_capacity = request.form['engine_capacity']
        type = request.form['type']
        mileage = request.form['mileage']
        fuel_type = request.form['fuel_type']
        image_url = request.files['imageUrl']
        image_url.save("static/images/" + image_url.filename)
        description = request.form.get('description', '')  # Optional field
        availability = request.form.get('availability', True)  # Defaults to True if not specified

        connection = db_connection()

        sql = """
        INSERT INTO `motorcycles`(
            `make`, `model`, `year`, `price`, `engine_capacity`, `type`, `mileage`, 
            `fuel_type`, `image_url`, `description`, `availability`
        ) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """

        data = (
            make, model, year, price, engine_capacity, type, mileage,
            fuel_type, image_url.filename, description, availability
        )

        cursor = connection.cursor()

        cursor.execute(sql, data)
        connection.commit()

        return render_template('uploadMotorcycle.html', success="Motorcycle uploaded successfully")




@motoheal.route("/uploadAccessory", methods=['POST', 'GET'])
def upload_accessory():
    if request.method == 'GET':
        return render_template('uploadAccessory.html')
    else:
        name = request.form['name']
        category = request.form['category']
        price = request.form['price']
        brand = request.form.get('brand', '')  # Optional field
        description = request.form.get('description', '')  # Optional field
        image_url = request.files['imageUrl']
        image_url.save("static/images/" + image_url.filename)
        stock_quantity = request.form['stock_quantity']
        availability = request.form.get('availability', True)

        connection = db_connection()

        sql = """
        INSERT INTO `accessories`(
            `name`, `category`, `price`, `brand`, `description`, `image_url`, `stock_quantity`, `availability`
        ) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """

        data = (
            name, category, price, brand, description, image_url.filename, stock_quantity, availability
        )

        cursor = connection.cursor()

        cursor.execute(sql, data)
        connection.commit()

        return render_template('uploadAccessory.html', success="Accessory uploaded successfully")




@motoheal.route("/uploadRentalService", methods=['POST', 'GET'])
def upload_rental_service():
    if request.method == 'GET':
        return render_template('uploadRentalService.html')
    else:
        vehicle_type = request.form['vehicle_type']
        rental_price = request.form['rental_price']
        rental_duration = request.form['rental_duration']
        availability = request.form.get('availability', True)
        description = request.form.get('description', '')  # Optional field
        image_url = request.files['imageUrl']
        image_url.save("static/images/" + image_url.filename)

        connection = db_connection()

        sql = """
        INSERT INTO `rental_services`(
            `vehicle_type`, `rental_price`, `rental_duration`, `availability`, `description`, `image_url`
        ) 
        VALUES (%s, %s, %s, %s, %s, %s)
        """

        data = (
            vehicle_type, rental_price, rental_duration, availability, description, image_url.filename
        )

        cursor = connection.cursor()

        cursor.execute(sql, data)
        connection.commit()

        return render_template('uploadRentalService.html', success="Rental service uploaded successfully")


# the imports for the mpesa function
import requests
import datetime
import base64
from requests.auth import HTTPBasicAuth

@motoheal.route('/mpesapayment', methods=['POST', 'GET'])
def mpesa_payment():
    if request.method == 'POST':
        phone = str(request.form['phone'])
        amount = str(request.form['amount'])
        # GENERATING THE ACCESS TOKEN
        # create an account on safaricom daraja
        consumer_key = "GTWADFxIpUfDoNikNGqq1C3023evM6UH"
        consumer_secret = "amFbAoUByPV2rM5A"

        api_URL = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"  # AUTH URL
        r = requests.get(api_URL, auth=HTTPBasicAuth(consumer_key, consumer_secret))

        data = r.json()
        access_token = "Bearer" + ' ' + data['access_token']

        #  GETTING THE PASSWORD
        timestamp = datetime.datetime.today().strftime('%Y%m%d%H%M%S')
        passkey = 'bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919'
        business_short_code = "174379"
        data = business_short_code + passkey + timestamp
        encoded = base64.b64encode(data.encode())
        password = encoded.decode('utf-8')

        # BODY OR PAYLOAD
        payload = {
            "BusinessShortCode": "174379",
            "Password": "{}".format(password),
            "Timestamp": "{}".format(timestamp),
            "TransactionType": "CustomerPayBillOnline",
            "Amount": amount,  # use 1 when testing
            "PartyA": phone,  # change to your number
            "PartyB": "174379",
            "PhoneNumber": phone,
            "CallBackURL": "https://modcom.co.ke/job/confirmation.php",
            "AccountReference": "account",
            "TransactionDesc": "account"
        }

        # POPULAING THE HTTP HEADER
        headers = {
            "Authorization": access_token,
            "Content-Type": "application/json"
        }

        url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"  # C2B URL

        response = requests.post(url, json=payload, headers=headers)
        print(response.text)
        return '<h3>Please Complete Payment in Your Phone and we will deliver in minutes</h3>' \
               '<a href='"/"' class="btn btn-dark btn-sm">Back to Products</a>'













motoheal.run(debug=True)



