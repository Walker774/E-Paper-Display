from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from . import db
from flask import Flask, render_template, url_for, redirect
from flask_login import login_user, login_required, logout_user, current_user
from .functions import *
from flask_bcrypt import bcrypt
import requests
from .auth import *

views = Blueprint('views', __name__)

#**********DONE************ main dashboard
@views.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    return render_template('./dashboard.html')

#******DONE********* when an esp sends a get request it ends the request URL with it's ID and this function checks for a file associated with that ID
@views.route('/labels/<label_id>')
def get_label_conf(label_id):
    return_data = decide_update(label_id)#calls the decide_update function that begins the update sequence
    print(return_data)#debugging printline
    return return_data#returns data to esp

#*****DONE******** displays view labels subpage 
@views.route('/view_labels', methods=['GET', 'POST'])
def view_labels():
    label_list = read_File_Names("labels/")
    return render_template('view_labels.html', labels = label_list)

#*********DONE*********** function to return data to view label subpage
@views.route('/view_label_data', methods=['GET','POST'])
def view_label_data():
    label_id = request.form.get("labels")
    label_data = get_label_data(label_id)
    item_file = label_data[1].strip()
    item_name = remove_extension(item_file)
    if (label_data[0][0] == '*'):
        label_up_to_date = "Label up to date"
    else:
        label_up_to_date = "Update pending"
    return render_template('view_label_data.html', nickname = label_id, item_name = item_name, waiting_for_update = label_up_to_date)

#***********DONE************ 1-2 displays edit labels subpage
@views.route('/edit_labels', methods=['GET', 'POST'])
def edit_labels():
    label_list = read_File_Names("labels/")
    return render_template('edit_labels.html', labels = label_list)

#************DONE*********** allows user to change label data
@views.route('/edit_label_data', methods=['POST'])
def edit_label_data():
    label_nick = request.form.get('labels')
    label_data = get_label_data(label_nick)
    item_file = label_data[1].strip()
    item_name = remove_extension(item_file)
    if (label_data[0][0] == '*'):
        label_up_to_date = 'true'
    else:
        label_up_to_date = "false"
    item_list = read_File_Names("items/")
    return render_template('edit_label_data.html', nickname = label_nick, current_item = item_name, update_status = label_up_to_date, items = item_list)      

#************DONE************** saves changes to label data
@views.route('/save_label<form_data>', methods=['GET','POST'])
def save_label_form(form_data):
    new_item = request.form.get('items')
    update_now = request.form.getlist("update_label")
    update = '*\n'
    if (update_now):
        update = '\n'
    save_label(form_data, new_item, update)
    return redirect("edit_labels")

#1-3 displays manage labels subpage 
@views.route('/manage_labels', methods=['GET', 'POST'])
def manage_labels():
    label_list = read_File_Names("labels/")
    return render_template('manage_labels.html', labels = label_list)

#********DONE******* function to update all labels at once
@views.route('/update_all_labels', methods=['GET'])
def update_all_labels():
    update_all()
    return redirect("manage_labels")

#calls function to delete label file
@views.route('/remove_label', methods=['POST', 'GET'])
def remove_label():
    if request.method == 'POST':
        label_selected = request.form.get('labels')
        file = label_selected+".txt"
        print("Attempting to delete:" + file)
        if os.path.exists("./webcontrol/labels/" + file):
            os.remove("webcontrol/labels/" + file)
        else:
            print("The file does not exist")
        return redirect("manage_labels")

    else: 
        label_list = read_File_Names("labels/")
        return render_template("remove_label.html", labels = label_list)

#***********DONE******************
@views.route('/pair_new_label', methods=['GET','POST'])
def pair_new_label():
    item_list = read_File_Names("items/")
    return render_template("pair_new_label.html", items = item_list)
#*************DONE************
@views.route('/save_new_label', methods=['POST'])
def save_new_label():
    label_name = request.form.get('name')
    item_name = request.form.get('items')
    new_label(label_name, item_name)
    return redirect("manage_labels")

#**********DONE**************2-1 displays view items subpage
@views.route('/view_items', methods=['GET', 'POST'])
def view_items():
    item_list = read_File_Names("items/")
    return render_template('view_items.html', items = item_list)

#********DONE*********
@views.route('/view_item_data', methods=['GET', 'POST'])
def view_item_data():
    if request.method == 'POST':
        item_id = request.form.get('items')
        data = get_item_data(item_id+'.txt').splitlines()
        item_name = data[0]
        item_upc = data[1]
        item_price = data[2]
        item_ss = data[3]
        item_se = data[4]
        return render_template('view_item_data.html', item_id = item_id, name = item_name, upc = item_upc, price = item_price, sale_start = item_ss, sale_end = item_se)

#**********DONE*********** 2-2 displays edit items subpage
@views.route('/edit_items', methods=['GET', 'POST'])
def edit_items():
    item_list = read_File_Names("items/")
    return render_template('edit_items.html', items = item_list)

@views.route('/edit_item_data', methods=['GET', 'POST'])
def edit_item_data():
    item_id= request.form.get('items')
    data = get_item_data(item_id+'.txt').split('\n')
    name = data[0]
    print(data[0])
    item_upc = data[1]
    item_price, item_units = data[2].split('/', 1)
    item_units = '/'+item_units
    item_ss = data[3]
    item_se = data[4]
    return render_template('edit_item_data.html', item_id = item_id, name = name, upc = item_upc, price = item_price, unit = item_units, sale_start = item_ss, sale_end = item_se)

@views.route('/save_item<form_data>', methods = ['POST', 'GET'])
def save_item(form_data):
    item_id = form_data
    item_name = request.form.get('name')
    item_upc = request.form.get('upc')
    item_price = request.form.get('price')
    item_units = request.form.get('units')
    item_ss = request.form.get('sale_start')
    item_se = request.form.get('sale_end')
    save_item_file(item_id, item_name, item_upc, item_price, item_units, item_ss, item_se)
    return redirect('edit_items')

#2-3 displays manage items subpage
@views.route('/manage_items', methods=['GET', 'POST'])
def manage_items():
    item_list = read_File_Names("items/")
    return render_template('manage_items.html', items = item_list)

@views.route('/new_item', methods = ['GET','POST'])
def new_item():
    return render_template('new_item.html')

@views.route('/save_new_item', methods=['POST'])
def save_new_item():
    item_id = request.form.get('item_id')
    name = request.form.get('name')
    upc = request.form.get('upc')
    price = request.form.get('price')
    units = request.form.get('units')
    sale_start = request.form.get('sale_start')
    sale_end = request.form.get('sale_end')
    create_new_item(item_id, name, upc, price, units, sale_start, sale_end)
    return redirect('manage_items')

@views.route('/remove_item', methods=['POST', 'GET'])
def remove_item():
    if request.method == 'POST':
        item_selected = request.form.get('items')
        file = item_selected+".txt"
        print("Attempting to delete:" + file)
        if os.path.exists("./webcontrol/items/" + file):
            os.remove("./webcontrol/items/" + file)
        else:
            print("The file does not exist")
        return redirect("manage_items")

    else: 
        item_list = read_File_Names("items/")
        return render_template("remove_item.html", items = item_list)


@views.route('/server_settings', methods=['GET', 'POST'])
def server_settings():
    return render_template('security_settings.html')

@views.route('/security_settings', methods=['GET', 'POST'])
def security():
    return render_template('server_settings.html')

@views.route('/power_options', methods=['GET', 'POST'])
def power_options():
    return render_template('power_options.html')
