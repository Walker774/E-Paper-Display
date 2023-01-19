import os

def get_label_data(label_id):
    file = open('./webcontrol/labels/'+label_id+'.txt')
    data = file.readlines()
    file.close()
    return data

def get_itemfile(label_id):
    file = open('./webcontrol/labels/'+label_id+'.txt')
    data = file.readlines()
    item_file = data[1].strip()
    file.close()
    return item_file

def remove_extension(file_name):
    no_extension = (os.path.splitext(file_name)[0])
    return no_extension

#reads the data from the item file and returns it
def get_item_data(item_file):
    file = open('./webcontrol/items/'+item_file)
    data = file.readlines()
    file.close()
    return_data = ""
    i = 0
    for i in range(len(data)):
        return_data = return_data+data[i]
        i=i+1
    file.close()
    return return_data

#UNFINISHED - updates the next update date based on the update interval saved to the label file and returns it
#def update_date(curdate, update_interval):
#    date = '*'
#    return date

#checks update date and decides if the label should be updated, if so calls get_label_data with the item_file parameter and returns the result to the views function
def decide_update(label_id):
    file = open('./webcontrol/labels/'+label_id,)
    data = file.readlines()
    item_file = data[1].strip()
    file.close()
    if data[0].strip() == '*':
        return '*'
    else:
        label_data = get_item_data(item_file)
        file = open('./webcontrol/labels/'+label_id, 'w')
        data[0] = '*\n'
        file.writelines(data)
        file.close
        return label_data

def read_File_Names(folder_name):
    path = os.getcwd()
    print(path)
    files = os.listdir("/home/pi/epapercontrollerv5_11_15_2022/EpaperController/webcontrol/"+folder_name)
    num_files = len(files)
    selected_file = 0
    print (files)
    for selected_file in range(num_files):
        files[selected_file] = files[selected_file].replace('.txt','')
    return files

def save_item_file(fileID, itemName, itemUPC, itemPrice, units, startOfSale, endOfSale):
    fileName = fileID+'.txt'
    data = itemName,'\n', itemUPC,'\n', (itemPrice+units),'\n', startOfSale,'\n', endOfSale
    file = open('./webcontrol/items/'+fileName, 'w')
    file.writelines(data)
    file.close

def save_label(labelID, itemName, update_now):
    fileLabel = labelID+'.txt'
    fileItem = itemName+'.txt'
    data = update_now, fileItem
    file = open('./webcontrol/labels/'+fileLabel, 'w')
    file.writelines(data)
    file.close
    
def update_all():
    labels = read_File_Names('labels/')
    for label in labels:
        file = open('./webcontrol/labels/'+label+'.txt', 'r')
        data = file.readlines()
        data[0] = '\n'
        file.close
        file = open('./webcontrol/labels/'+label+'.txt', 'w')
        file.writelines(data)
        file.close

def label_update(labelID, itemName):
    fileName = labelID+'.txt'
    itemFile = itemName+'.txt'
    file = open('./webcontrol/items/'+fileName, 'w' 'r')
    data = file.readlines()
    if itemName != '*':
        data[0] = ' '
        file.writelines(data)
    else:
        data[0] = ' '
        data[1] = itemFile
        file.writelines(data)
    file.close()

def remove_label(label_selected):
    file = label_selected+".txt"
    os.remove(file)

def new_label(name, item_selected):
    file = open('./webcontrol/labels/'+name+'.txt', 'a')
    file.write(' \n'+item_selected+'.txt')
    file.close

def create_new_item(item_id, name, upc, price, units, sale_start, sale_end):
    file = open('./webcontrol/items/'+item_id+'.txt', 'a')
    file.write(name+'\n')
    file.write(upc+'\n')
    file.write(price+units+'\n')
    file.write(sale_start+'\n')
    file.write(sale_end)
    file.close