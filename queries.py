from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Restaurant, Base, MenuItem, User

engine = create_engine('sqlite:///restaurantmenuwithusers.db?check_same_thread=False')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


# urbanRestaurant = session.query(Restaurant)
# .filter_by(name="Urban Burger").one()
#
# items = session.query(MenuItem).filter_by(restaurant_id=urbanRestaurant.id)
#
# for item in items:
#     print(item.name)
#     print(item.price)
#     print(item.restaurant.name)
#     print('')

# User Helper Functions
def createUser(login_session):
    newUser = User(name=login_session['username'], email=login_session[
                   'email'], picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user


def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None


def getRestaurantsQuery():
    restaurants = session.query(Restaurant).all()

    return restaurants


def getRestaurant(id):
    restaurantName = session.query(Restaurant).filter_by(id=id).one()

    return restaurantName


def createNewRestaurant(restaurantName):
    restaurant1 = Restaurant(name=restaurantName)

    session.add(restaurant1)
    session.commit()


def renameRestaurant(id, name):
    oldRestaurant = session.query(Restaurant).filter_by(id=id).one()
    oldRestaurant.name = name

    session.add(oldRestaurant)
    session.commit()


def deleteRestaurant(id):
    oldRestaurant = session.query(Restaurant).filter_by(id=id).one()

    session.delete(oldRestaurant)
    session.commit()


def getAllMenuItems():
    restaurants = session.query(MenuItem).all()

    return restaurants


def getRestaurantItems(restaurant):
    items = session.query(MenuItem).filter_by(restaurant=restaurant).all()

    return items


def getItem(item_id, restaurant_id):
    item = session.query(MenuItem).filter_by(id=item_id,
                                             restaurant_id=restaurant_id).one()

    return item


def createNewMenuItem(item_name, item_description, item_course,
                      item_price, restaurant_id, user_id):
    item = MenuItem(name=item_name, description=item_description,
                    course=item_course, price=item_price,
                    restaurant_id=restaurant_id, user_id=user_id)

    session.add(item)
    session.commit()


def renameMenuItem(item_name, item_description, item_course,
                   item_price, item_id, restaurant_id):
    item = session.query(MenuItem).filter_by(id=item_id,
                                             restaurant_id=restaurant_id).one()
    if item_name is not "":
        item.name = item_name
    if item_description is not "":
        item.description = item_description
    if item_course is not "":
        item.course = item_course
    if item_price is not "":
        item.price = item_price

    session.add(item)
    session.commit()


def deleteItemQuery(item_id):
    item = session.query(MenuItem).filter_by(id=item_id).one()

    session.delete(item)
    session.commit()
