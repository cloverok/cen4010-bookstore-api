from flask import Flask

# Create a user with username, password and optional fields (name, email, address, home address).
#            logic: provided the user fields, create the user in the database.
#     request type: POST
#   parameter sent: user object
#    response data: none
@app.route('/CreateProfile', methods=['POST'])
def create_profile_post():
    return

# Retrieve a User Object and its fields by their username.
#            logic: given a specific username, retrieve the user details.
#     request type: GET
#   parameter sent: username
#    response data: JSON user object
@app.route('/GetProfile/<username>', methods=['GET'])
def get_profile(username):
    return

# Update the user and any of their fields except for mail.
#            logic: given the username as a key lookup value, and any other user field, update that user field with the new param value
#     request type: PATCH
#   parameter sent: username
#    response data: none
@app.route('/UpdateProfile/<username>', methods=['PATCH'])
def edit_profile(username):
    return

# Create Credit Card that belongs to a User
#            logic: Given a user name and credit card details, create a creditcard for that user
#     request type: POST
#   parameter sent: username, credit card object
#    response data: none
@app.route('/CreateCreditCard', methods=['POST'])
def create_credit_card():
    return