from flask import *
import pymysql

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



@motoheal.route('/singlecar/<car_id>')
def singlecar(car_id):
    connection = db_connection()

    sql = "SELECT * FROM `cars` WHERE car_id = %s"

    cursor = connection.cursor()
    cursor.execute(sql, car_id)
    car = cursor.fetchone()

    # category = car[1]
    # sql2 = "SELECT * FROM 'cars' WHERE make = %s"
    # cursor2 = connection.cursor()
    # cursor2.execute(sql2, category)
    # similar = cursor2.fetchall()

    return render_template("singlecar.html", car = car )


@motoheal.route('/vehicles', methods = ['GET'])
def vehicles():
    connection = db_connection()

    # vehicles Query
    sql = "SELECT * FROM `vehicles`"

    cursor = connection.cursor()
    cursor.execute(sql)
    vehicles = cursor.fetchall()
    return render_template('vehicles.html', vehicles = vehicles)
    
    

@motoheal.route('/singlevehicle/<id>')
def single_vehicle(id):
    connection = db_connection()
    cursor = connection.cursor()
    sql = "SELECT * FROM `vehicles` WHERE id = %s"  # Fetch single vehicle by ID
    cursor.execute(sql, (id,))
    singlevehicle = cursor.fetchone()

    return render_template("singlevehicle.html", singlevehicle=singlevehicle)




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


# Route for single rental service page
@motoheal.route('/singlerental/<id>')
def single_rental(id):
    connection = db_connection()
    cursor = connection.cursor()
    sql = "SELECT * FROM `rental_services` WHERE id = %s"  # Fetch single rental by ID
    cursor.execute(sql, (id,))
    singlerental = cursor.fetchone()

    return render_template("singlerental.html", singlerental=singlerental)





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

    return render_template("singleaccessory.html", singleaccessory=singleaccessory)





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














motoheal.run(debug=True)



