# item-catalog
Second project in Full Stack Web Developer Nano-Degree.

## Outline
* Project Overview
* Getting started
* Project Pages
* [Json Pages](#json-pages)

## Project Overview
item-catalog is a flask application that provides a list of items within a variety of restaurants as well as provide a user registration and authentication system. Registered users will have the ability to post, edit and delete their own items.

## Getting started
### First, fork the VM Configuration:
Log into your personal Github account, and fork the [Udacity Fullstack Nanodegree](https://github.com/udacity/fullstack-nanodegree-vm) repo

### Second, clone the remote to your local machine:
From the terminal, run the following command (be sure to replace <username> with your GitHub username): 
```
git clone http://github.com/<username>/fullstack-nanodegree-vm fullstack-vm 
```

### Third, run the VM, login to VM, logout from VM and shutdown VM:
To run VM, change the directory to `fullstack-vm` then run the vm using the following commands:
```
cd fullstack-vm
vagrant up
```
to log from your terminal into vm write the following command:
``` 
vagrant ssh
```
to logout from vm, write the following command in vm:
``` 
exit
```
to shutdown the vm, exit from vm then write the following command in your terminal:
``` 
vagrant halt
```

### Forth, download item-catalog app:
install [item-catalog](https://github.com/SarahAlhumud/item-catalog/) application, and move it to `fullstack-vm/vagrant` directory.

### Fifth, run item-catalog app:
After login into VM and change directory to /vagrant/item-catalog
#### 1. initialize database:
```
python database_setup.py
```
#### 2. populate database:
```
python lotsofmenus.py
```
#### 3. run Flask web server:
```
python project.py
```

## Project Pages
### The homepage displays all available restaurants.
http://localhost:5000/
http://localhost:5000/restaurants/

### Page shows all the items available for specific category.
http://localhost:5000/restaurants/1/

### Page to login into application
http://localhost:5000/login

### After logging, a owner user has the ability to add, update, or delete item.
http://localhost:5000/

http://localhost:5000/restaurants/

http://localhost:5000/restaurants/1/

http://localhost:5000/restaurants/1/new/

http://localhost:5000/restaurants/1/1/edit/

http://localhost:5000/restaurants/1/1/delete/


### After logging, a user (not owner) has the ability to add an item.
http://localhost:5000/

http://localhost:5000/restaurants/

http://localhost:5000/restaurants/1/

http://localhost:5000/restaurants/1/new/


## JSON Pages
a. All restaurants with their menu items (JSON format)
http://localhost:5000/restaurants/menus/JSON

b. Specific restaurant with its item (JSON format)
http://localhost:5000/restaurants/1/menu/JSON

c. All restaurants (JSON format)
http://localhost:5000/restaurants/JSON

d. Specific item of specific restaurant (JSON format) 
http://localhost:5000/restaurants/1/menu/1/JSON
