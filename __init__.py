from flask import Flask, render_template, request, \
    redirect, url_for, flash, jsonify
# from queries import *
from package import *
from flask import session as login_session
import random
import string
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests

app = Flask(__name__)

CLIENT_ID = json.loads(open('client_secrets.json', 'r')
                       .read())['web']['client_id']
APPLICATION_NAME = "Restaurant Menu Application"


# Create anti-forgery state token
@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in range(32))
    login_session['state'] = state
    # return "The current session state is %s" % login_session['state']
    return render_template('login.html', STATE=state)


@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json
                                 .dumps('Current user is already connected.'),
                                 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']
    # ADD PROVIDER TO LOGIN SESSION
    login_session['provider'] = 'google'

    # See if a user exists, if it doesn't make a new one
    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ''' " style = "width: 300px; height: 300px;
    border-radius: 150px;-webkit-border-radius: 150px;
    -moz-border-radius: 150px;"> '''
    flash("you are now logged in as %s" % login_session['username'])
    print("done!")
    return output


# DISCONNECT - Revoke a current user's token and reset their login_session
@app.route('/gdisconnect')
def gdisconnect():
    access_token = login_session['access_token']
    print('In gdisconnect access token is %s', access_token)
    print('User name is: ')
    print(login_session['username'])
    if access_token is None:
        print('Access Token is None')
        response = make_response(json.dumps('Current user not connected.'),
                                 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    url = '''https://accounts.google.com/o
    /oauth2/revoke?token=%s''' % login_session['access_token']
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    print('result is ')
    print(result)
    if result['status'] == '200':
        # del login_session['access_token']
        # del login_session['gplus_id']
        # del login_session['username']
        # del login_session['email']
        # del login_session['picture']
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        print("this is the status " + result['status'])
        response = make_response(json
                                 .dumps('''Failed to revoke token
                                  for given user.'''), 400)
        response.headers['Content-Type'] = 'application/json'
        return response


@app.route('/')
@app.route('/restaurants/')
def restaurantsList():
    restaurants = getRestaurantsQuery()

    return render_template('restaurants.html', restaurants=restaurants)


@app.route('/restaurants/JSON')
def restaurantsListJSON():
    restaurants = getRestaurantsQuery()

    return jsonify(Restaurants=[i.serialize for i in restaurants])


@app.route('/restaurants/menus/JSON')
def restaurantsMenusListJSON():
    restaurants = getRestaurantsQuery()
    # group = {}
    menus = []

    for r in restaurants:
        dic = r.serializeMenuItems
        items = getRestaurantItems(r)
        dic['menuItems'] = [i.serialize for i in items]
        # print([i.serialize for i in items])

        # print(dic['menuItems'])
        menus.append(dic)
    # print(menus)

    return jsonify(Restaurants=[i for i in menus])


@app.route('/restaurants/<int:restaurant_id>/')
def restaurantMenu(restaurant_id):
    restaurant = getRestaurant(restaurant_id)
    items = getRestaurantItems(restaurant)

    if 'username' not in login_session:
        return render_template('publicmenu.html',
                               restaurant=restaurant, items=items)
    else:
        return render_template('menu.html', restaurant=restaurant, items=items)


@app.route('/restaurants/<int:restaurant_id>/menu/JSON')
def restaurantMenuJSON(restaurant_id):
    restaurant = getRestaurant(restaurant_id)
    items = getRestaurantItems(restaurant)
    return jsonify(MenuItems=[i.serialize for i in items])


@app.route('/restaurants/<int:restaurant_id>/menu/<int:menu_id>/JSON')
def restaurantItemSON(restaurant_id, menu_id):
    item = getItem(menu_id, restaurant_id)
    return jsonify(MenuItem=item.serialize)


@app.route('/restaurants/<int:restaurant_id>/new/', methods=['GET', 'POST'])
def newMenuItem(restaurant_id):

    if 'username' not in login_session:
        return redirect('/login')
    if request.method == 'POST':
        createNewMenuItem(request.form['name'], request.form['description'],
                          request.form['course'], request.form['price'],
                          restaurant_id, login_session['user_id'])
        flash("new menu item created!")
        return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))
    else:
        restaurant = getRestaurant(restaurant_id)
        return render_template('newmenuitem.html', restaurant=restaurant)


@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/edit/',
           methods=['GET', 'POST'])
def editMenuItem(restaurant_id, menu_id):
    item = getItem(menu_id, restaurant_id)
    creator = getUserInfo(item.user_id)

    if login_session['user_id'] != creator.id \
            or 'username' not in login_session:
        return "You are not authorized to edit menu item"
    if request.method == 'POST':
        renameMenuItem(request.form['name'], request.form['description'],
                       request.form['course'], request.form['price'],
                       menu_id, restaurant_id)
        flash("Menu Item has been edited")
        return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))
    else:
        restaurant = getRestaurant(restaurant_id)
        return render_template('editmenuitem.html', restaurant=restaurant,
                               menu=getItem(menu_id, restaurant_id))


@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/delete/',
           methods=['GET', 'POST'])
def deleteMenuItem(restaurant_id, menu_id):
    item = getItem(menu_id, restaurant_id)
    creator = getUserInfo(item.user_id)

    if login_session['user_id'] != creator.id \
            or 'username' not in login_session:
        return "You are not authorized to delete menu item"
    if request.method == 'POST':
        deleteItemQuery(menu_id)
        flash("Menu Item has been deleted")
        return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))
    else:
        restaurant = getRestaurant(restaurant_id)
        return render_template('deletemenuitem.html', restaurant=restaurant,
                               menu=getItem(menu_id, restaurant_id))


# Disconnect based on provider
@app.route('/disconnect')
def disconnect():
    if 'provider' in login_session:
        if login_session['provider'] == 'google':
            gdisconnect()
            del login_session['access_token']
            del login_session['gplus_id']
            del login_session['username']
            del login_session['email']
            del login_session['picture']
            # del login_session['gplus_id']
            # del login_session['access_token']
        flash("You have successfully been logged out.")
        return redirect(url_for('restaurantsList'))
    else:
        flash("You were not logged in")
        return redirect(url_for('restaurantsList'))


@app.route('/menuItems')
def menuItems():
    items = getAllMenuItems()

    output = ''
    for item in items:
        output += item.name
        output += '<br/>'
        output += item.price
        output += '<br/>'
        output += item.description
        output += '<br/><br/>'

    return output


if __name__ == "__main__":
    app.secret_key = "super_secret_key"
    app.debug = True
    app.run()
