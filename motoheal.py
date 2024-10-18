from flask import Flask, render_template, request
import pymysql

motoheal = Flask(__name__)

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


@motoheal.route('/parts', methods = ['POST' , 'GET'])
def parts():
    if request.method == 'GET':
        return render_template('parts.html')




@motoheal.route('/services', methods = ['POST' , 'GET'])
def services():
    if request.method == 'GET':
        return render_template('services.html')




@motoheal.route('/customer_reviews', methods = ['POST' , 'GET'])
def customers():
    if request.method == 'GET':
        return render_template('customer_reviews.html')




@motoheal.route('/search', methods = ['POST' , 'GET'])
def search():
    if request.method == 'GET':
        return render_template('search.html')




@motoheal.route('/aboutus', methods = ['POST' , 'GET'])
def aboutus():
    if request.method == 'GET':
        return render_template('aboutus.html')





@motoheal.route('/faqs', methods = ['POST' , 'GET'])
def faqs():
    if request.method == 'GET':
        return render_template('faqs.html')




@motoheal.route('/contactus', methods = ['POST' , 'GET'])
def contactus():
    if request.method == 'GET':
        return render_template('ucontactus.html')
    




@motoheal.route('/blog', methods = ['POST' , 'GET'])
def blog():
    if request.method == 'GET':
        return render_template('blog.html')
















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
    



motoheal.run(debug=True)



