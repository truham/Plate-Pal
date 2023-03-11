from flask import Blueprint, jsonify, request
from flask_login import login_required
from app.models import db, Business, Review, Image
from .auth_routes import validation_errors_to_error_messages
from flask_login import current_user, login_required
from app.forms.businesses_form import BusinessForm
from app.forms.reviews_form import ReviewForm
from app.forms.images_form import ImageForm
from datetime import datetime

business_routes = Blueprint('business', __name__)


# GET ALL BUSINESSES
@business_routes.route('/')
def get_businesses():
    businesses = Business.query.all()
    return {'businesses': [business.to_dict() for business in businesses]}


# GET ALL BUSINESSES BY CURRENT USER
@business_routes.route('/current')
@login_required
def get_businesses_current():
    print("current user", current_user)
    user_id = int(current_user.get_id())
    business_query = db.session.query(
        Business).filter(Business.owner_id == user_id)
    businesses = business_query.all()
    return {'businesses': [business.to_dict() for business in businesses]}


# GET BUSINESS DETAILS BY ID
@business_routes.route('/<int:id>')
def get_business_details(id):
    # Single business
    business = Business.query.get(id).to_dict()

    if not business:
        return "Business does not exist", 404

    # Handle reviews
    review_query = db.session.query(Review).filter(Review.business_id == id)
    business_reviews = review_query.all()
    stars = [review.stars for review in business_reviews]
    avg_rating = sum(stars) / len(business_reviews)
    business['avg_rating'] = avg_rating
    business['number_of_reviews'] = len(business_reviews)

    # Handle images
    images_query = db.session.query(Image).filter(Image.business_id == id)
    images = images_query.all()
    business['images'] = [image.to_dict() for image in images]

    return jsonify(business)


# GET REVIEWS BY BUSINESS ID
@business_routes.route('/<int:id>/reviews')
def get_business_reviews(id):

    review_query = db.session.query(Review).filter(Review.business_id == id)
    business_reviews = [review.to_dict() for review in review_query.all()]

    for review in business_reviews:
        images_query = db.session.query(Image).filter(
            Image.review_id == review['id'])
        images = images_query.all()
        review['images'] = [image.to_dict() for image in images]

    return jsonify(business_reviews)


# CREATE NEW BUSINESS
@business_routes.route('/', methods=['POST'])
@login_required
def create_new_business():
    form = BusinessForm()
    form['csrf_token'].data = request.cookies['csrf_token']
    data = request.get_json()
    if form.validate_on_submit():
        new_business = Business(
            owner_id=int(current_user.get_id()),
            name=data['name'],
            category=data['category'],
            address=data['address'],
            city=data['city'],
            state=data['state'],
            zipcode=data['zipcode'],
            phone_number=data['phone_number'],
            website=data['website'],
            lat=data['lat'],
            lng=data['lng'],
            price=data['price'],
            hours_of_operation=data['hours_of_operation']
        )
        db.session.add(new_business)
        db.session.commit()
        return new_business.to_dict()
    if form.errors:
        return validation_errors_to_error_messages(form.errors)


# CREATE NEW REVIEW
@business_routes.route('/<int:id>/reviews', methods=['POST'])
@login_required
def create_new_review(id):

    business = Business.query.get(id)
    if not business:
        return "Business does not exist", 404

    review_query = db.session.query(Review).filter(Review.business_id == id).filter(
        Review.owner_id == int(current_user.get_id()))
    user_business_reviews = review_query.all()
    if len(user_business_reviews) > 0:
        return "User already has a review for this spot", 403

    form = ReviewForm()
    form['csrf_token'].data = request.cookies['csrf_token']
    data = request.get_json()
    if form.validate_on_submit():
        new_review = Review(
            owner_id=int(current_user.get_id()),
            business_id=id,
            review=data['review'],
            stars=data['stars'],
        )

        db.session.add(new_review)
        db.session.commit()
        return new_review.to_dict()
    if form.errors:
        return validation_errors_to_error_messages(form.errors)


# CREATE NEW IMAGE FOR A BUSINESS
@business_routes.route('/<int:id>/images', methods=['POST'])
@login_required
def create_new_image(id):
    business = Business.query.get(id)
    if not business:
        return "Business does not exist", 404

    form = ImageForm()
    form['csrf_token'].data = request.cookies['csrf_token']
    data = request.get_json()
    if form.validate_on_submit():
        new_image = Image(
            owner_id=int(current_user.get_id()),
            business_id=id,
            url=data['url']
        )
        db.session.add(new_image)
        db.session.commit()
        return new_image.to_dict()
    if form.errors:
        return validation_errors_to_error_messages(form.errors)


# UPDATE BUSINESS
@business_routes.route('/<int:id>', methods=['PUT'])
@login_required
def update_business(id):

    business = Business.query.get(id)
    if not business:
        return "Business does not exist", 404

    data = request.get_json()
    if int(current_user.get_id()) == business.owner_id:
        business.name = data['name']
        business.category = data['category']
        business.address = data['address']
        business.city = data['city']
        business.state = data['state']
        business.zipcode = data['zipcode']
        business.phone_number = data['phone_number']
        business.website = data['website']
        business.lat = data['lat']
        business.lng = data['lng']
        business.price = data['price']
        business.hours_of_operation = data['hours_of_operation']
        business.updated_at = datetime.utcnow()

        db.session.commit()
        return business.to_dict()

    else:
        "Business was unable to be updated", 403


# DELETE A BUSINESS
@business_routes.route('/<int:id>', methods=['DELETE'])
def delete_business(id):
    business = Business.query.get(id)

    if not business:
        return "Business does not exist", 404

    if int(current_user.get_id()) == business.owner_id:
        db.session.delete(business)
        db.session.commit()
        return "Item has been deleted"
    else:
        return "Business was unable to be deleted", 403