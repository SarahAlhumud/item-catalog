# item-catalog

# Project Overview
item-catalog is a flask application that provides a list of items within a variety of restaurants as well as provide a user registration and authentication system. Registered users will have the ability to post, edit and delete their own items.

# How to start?
## First, fork the VM Configuration:
Log into your personal Github account, and fork the [Udacity Fullstack Nanodegree](https://github.com/udacity/fullstack-nanodegree-vm) repo

## Second, clone the remote to your local machine:
From the terminal, run the following command (be sure to replace <username> with your GitHub username): git clone http://github.com/<username>/fullstack-nanodegree-vm fullstack-vm

## Third, run the VM, login to VM, logout from VM and shutdown VM:
To run VM, change the directory to `fullstack-vm` then run the vm using the following commands:
```
cd fullstack-vm
vagrant up
```
to log from your terminal into vm write the following command:
` vagrant ssh `
to logout from vm, write the following command in vm:
` exit `
to shutdown the vm, exit from vm then write the following command in your terminal:
` vagrant halt `

## Forth, download item-catalog app:
install [item-catalog](https://github.com/SarahAlhumud/item-catalog/) application, and move it to `fullstack-vm/vagrant` directory.

## Fifth, run item-catalog app:
### 1. initialize database:
```
python database_setup.py
```
### 2. populate database:
```
python lotsofmenus.py
```
### 3. run Flask web server:
```
python project.py
```


The homepage displays all available restaurants.
http://localhost:5000/
http://localhost:5000/restaurants/
