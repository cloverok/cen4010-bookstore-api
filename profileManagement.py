from flask import Blueprint, Flask, jsonify, request
import mysql.connector

profile_bp = Blueprint("profile", __name__)

# todo - merge function w/ to correct db call
def get_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="cm6355582",
        database="bookstore"
    )
 
# Create a user with username, password and optional fields (name, email, address, home address).
#            logic: provided the user fields, create the user in the database.
#     request type: POST
#   parameter sent: user object
#    response data: none
@profile_bp.route('/CreateProfile', methods=['POST'])
def create_profil():
    # get request body
    data = request.get_json()
    
    # validate request body exists
    if data is None:
        return jsonify({"error": "user data JSON is empty"}), 400 
    
    # validate required table data exists
    if not data.get('username') or not data.get('password'):
        return jsonify({"error": "username & password are required"}), 400
    
    # connect to db and add new profile
    conn = get_db()
    cursor = conn.cursor()

    # data.get[] will return & insert None for non-required values missing in JSON data 
    cursor.execute("""INSERT INTO profile (username, password, name, email) VALUES (%s, %s, %s, %s)""", (data['username'], data['password'], data.get('name'), data.get('email')))

    conn.commit()
    cursor.close()

    # return success
    return jsonify({"success": f"profile for { data['username'] } has been created"}), 201

# Retrieve a User Object and its fields by their username.
#            logic: given a specific username, retrieve the user details.
#     request type: GET
#   parameter sent: username
#    response data: JSON user object
@profile_bp.route('/GetProfile/<string:username>', methods=['GET'])
def get_profile(username):
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute("""SELECT * FROM profile WHERE username = %s""", (username,))

    userInfo = cursor.fetchone()     

    cursor.close()

    if userInfo is None:
        return jsonify({"error": "username not found"}), 404

    return jsonify(userInfo), 200

# Update the user and any of their fields except for mail.
#            logic: given the username as a key lookup value, and any other user field, update that user field with the new param value
#     request type: PATCH
#   parameter sent: username
#    response data: none
@profile_bp.route('/UpdateProfile/<username>', methods=['PATCH'])
def update_profile(username):
    # get request body
    data = request.get_json()

    # validate request body exists
    if data is None:
        return jsonify({"error": "user data JSON is empty"}), 400

    # fields allowed to be updated (email excluded per spec)
    changeableFields = ["password", "name", "email"]

    # keep only the provided, allowed fields
    changes = {field: data[field] for field in changeableFields if field in data}

    # validate at least one updatable field was provided
    if changes is None:
        return jsonify({"error": "no updatable fields provided"}), 400

    # connect to db
    conn = get_db()
    cursor = conn.cursor()

    # verify the user exists before updating
    cursor.execute("""SELECT username FROM profile WHERE username = %s""", (username,))
    if cursor.fetchone() is None:
        cursor.close()
        return jsonify({"error": "username not found"}), 404

    # build the SET clause from the whitelist; values stay parameterized
    placeholders = ", ".join(f"{field} = %s" for field in changes)
    values = list(changes.values()) + [username]

    cursor.execute(f"""UPDATE profile SET {placeholders} WHERE username = %s""", values)
    
    conn.commit()
    cursor.close()
    
    return jsonify({"success": f"profile updated"}), 201

# Create Credit Card that belongs to a User
#            logic: Given a user name and credit card details, create a creditcard for that user
#     request type: POST
#   parameter sent: username, credit card object
#    response data: none
@profile_bp.route('/CreateCreditCard/<username>', methods=['POST'])
def create_credit_card(username):
    # get request body
    data = request.get_json()

    # validate request body exists
    if data is None:
        return jsonify({"error": "credit card data JSON is empty"}), 400

    # validate required card data exists (cvv is NOT NULL in the table, so it's required too)
    if not data.get('cardNumber') or not data.get('expirationDate') or not data.get('cvv'):
        return jsonify({"error": "card number, expiration & cvv are required"}), 400

    # connect to db
    conn = get_db()
    cursor = conn.cursor()

    # look up the uid for this username - this doubles as the user existence check
    cursor.execute("""SELECT uid FROM profile WHERE username = %s""", (username,))
    row = cursor.fetchone()
    if row is None:
        cursor.close()
        conn.close()
        return jsonify({"error": "username not found"}), 404

    uid = row[0]

    # insert the card against the uid
    try:
        cursor.execute("""INSERT INTO creditCard (card_number, uid, expiration, cvv) VALUES (%s, %s, %s, %s)""", (data['cardNumber'], uid, data['expirationDate'], data['cvv']))
        conn.commit()
    except mysql.connector.IntegrityError:
        # card_number is the primary key and uid is unique, so a duplicate card or a second card for the same user lands here
        cursor.close()
        conn.close()
        return jsonify({"error": "card already exists or user already has a card"}), 409

    cursor.close()
    conn.close()

    # return success
    return jsonify({"success": f"credit card added for { username }"}), 201

