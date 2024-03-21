from flask import Blueprint, request, jsonify, json
from datetime import datetime
from authors_app.extensions import db,bcrypt
from authors_app.models.user import User



auth = Blueprint('auth', __name__, url_prefix='/api/vl/auth')

@auth.route('/register',  methods=['POST'])
#create a function for the user
def register():
 try: 
    first_name= request.json['first_name'] 
    last_name=request.json['last_name']
    email=request.json['email']
    contact=request.json['contact']
    password=request.json['password']
    user_type=request.json['user_type']
    #biography=request.json['biography']
    image=request.json['image']
    
    hashed_password = bcrypt.generate_password_hash(password)
    
    if not first_name:
        return jsonify({"error":"Your first name is required"})
    if not last_name:
        return jsonify({"error":"Your last name is required"})
    if not email:
        return jsonify({"error":"Your email is required"})
    if not contact:
        return jsonify({"error":"Your contact is required"})
    if not user_type:
        return jsonify({"error":"User type is required"})
    if  len(password)<6:
        return jsonify({"error":"Your password must have more than six characters"})
    if not email:
        return jsonify({"error":"Your email is required"})
    
    
    #checking if an object has already been registered
    if User.query.filter_by(email=email).first():
        return jsonify({"error","This email is already registered"})
    if User.query.filter_by(contact=contact).first():
        return jsonify({"error","This contact is already registered"})
    
    # my_dict = {
    #     first_name, last_name,email,contact,user_type,image
    # }
    # serialized_dict = list(my_dict)
    # return jsonify(serialized_dict)
    # if user_type=='author' and not biography:
    #     return jsonify({"Your biography is required"})
    #checking if an object has already been registered
   
   # Creating a new user
    
    new_user = User(first_name=first_name, last_name=last_name, email=email,
                        contact=contact, password=hashed_password, user_type=user_type, image=image
                       )

        # Adding and committing to the database
    db.session.add(new_user)
    db.session.commit()

        # Building a response
    username = new_user.get_full_name()
    return jsonify({'message': 'User registered successfully'})

    
        #     'message': f'{username} has been successfully created as an {new_user.user_type}',
        #      'user': {
        #         'first_name': new_user.first_name,
        #         'last_name': new_user.last_name,
        #         'email': new_user.email,
        #         'contact': new_user.contact,
        #         'type': new_user.user_type,
        #         'created_at': new_user.created_at,
        #     }
        # })

 except Exception as e:
    db.session.rollback()
    return jsonify({'error': str(e)})
    # return jsonify({'error': 'Invalid registration data'})

    
    
  



# Define the login endpoint
@auth.route('/login', methods=["POST"])
def login():
    try:
        # Extract email and password from the request JSON
        data = request.json
        email = data.get("email")
        password = data.get("password")

        # Retrieve the user by email
        user = User.query.filter_by(email=email).first()

        # Check if the user exists and the password is correct
        if user and bcrypt.check_password_hash(user.password, password):
            # Return a success response
            return jsonify({'message': 'Login successful', 'user_id': user.id}), 200
        else:
            # Return an error response if authentication fails
            return jsonify({'error': 'Invalid email or password'}), 401

    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Define the edit user endpoint
@auth.route('/edit/<int:user_id>', methods=["PUT"])
def edit_user(user_id):
    try:
        # Extract user data from the request JSON
        data = request.json
        user = User.query.get(user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404

        # Update user fields if provided in the request
        if 'first_name' in data:
            user.first_name = data['first_name']
        if 'last_name' in data:
            user.last_name = data['last_name']
        if 'email' in data:
            # Check if the new email already exists
            new_email = data['email']
            if new_email != user.email and User.query.filter_by(email=new_email).first():
                return jsonify({'error': 'The email already exists'}), 400
            user.email = new_email
        if 'image' in data:
            user.image = data['image']
        if 'biography' in data:
            user.biography = data['biography']
        if 'user_type' in data:
            user.user_type = data['user_type']
        if 'password' in data:
            password = data['password']
            if len(password) < 6:
                return jsonify({'error': 'Password must have at least 6 characters'}), 400
            user.password = bcrypt.generate_password_hash(password).decode('utf-8')
        if 'contact' in data:
            user.contact = data['contact']

        # Commit the session to save the changes to the database
        db.session.commit()

        # Return a success response
        return jsonify({'message': 'User updated successfully'}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500    
    
## Define the delete user endpoint
@auth.route('/delete/<int:user_id>', methods=["DELETE"])
def delete_user(user_id):
    try:
        user = User.query.get(user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404

        db.session.delete(user)
        db.session.commit() #pushes to the database

        return jsonify({'message': 'User deleted successfully'}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500 

    
        
    
    
    
    
    
    
    
    
    
    

    
    
    