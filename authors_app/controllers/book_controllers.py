# from flask import Blueprint, request, jsonify
# from authors_app.models import Book
# from authors_app import db
from flask import Blueprint, request, jsonify
from datetime import datetime
from authors_app.extensions import db
from authors_app.models.book import Books


book = Blueprint('book', __name__, url_prefix='/api/v1/book')

@book.route('/register', methods=['POST'])
def register_book():
    try:
        # Extracting request data
       
        title=request.json.get('title')
        description=request.json.get('description')
        price=request.json.get('price')
        image=request.json.get('image')
        #price_unit=request.json.get('price_unit')
        number_of_pages= request.json.get('number_of_pages')
        #genre=request.json.get('genre')
        user_id=request.json.get('user_id')
        # created_at=request.json.get('created_at')
        # updated_at=request.json.get('updated_at')

        # Basic input validation 
        
        if not title:
            return jsonify({"error": 'Your book title is required'})
        
        if not user_id:
            return jsonify({"error": 'Your book user_id is required'})


        if not description:
            return jsonify({"error": 'The description is required'})
        
        
        if not image:
            return jsonify({"error": 'The image is required'})
        
        
        if not number_of_pages:
            return jsonify({"error": 'The number_of_pages is required'})

        if not price:
            return jsonify({"error": 'The price is required'})

        # if not price_unit:
        #     return jsonify({"error": 'The price_unit is required'})

        # if not genre:
        #     return jsonify({"error": 'Please specify the genre'})

        # Creating a new book
        new_book = Books(
           
            title=title,
            description=description,
            price=price,
            #price_unit=price_unit,
            number_of_pages=number_of_pages,
            #genre=genre,
            image=image,
            user_id=user_id
            # created_at=created_at,
            # updated_at=updated_at
        )

        # Adding and committing to the database
        db.session.add(new_book)
        db.session.commit()
        
      

        # Building a response message
        return jsonify({"message": f"Book '{new_book.title}', ID '{new_book.id}' has been uploaded"})

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)})