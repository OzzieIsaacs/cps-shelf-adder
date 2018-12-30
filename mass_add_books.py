import requests
import csv
import re
import sys

username = 'admin'
password = ''
shelf_id = '1'
booklist = 'booklist.csv'
serveradress = 'http://127.0.0.1:8083'

error=False
if shelf_id.isdigit():
    r = requests.post(serveradress+'/login?next=/', data = {'username':username,'password':password,'submit':'', 'remember_me':'on', 'next':'/'})
    headers = {'Referer': serveradress+'/'}
    if "login" in r.text:
        error=True
    if r.status_code == 200 and not error:
                if sys.version_info.major >= 3:
            csv_f =open(booklist,newline='')
        else:
            csv_f =open(booklist)
        with csv_f as csvfile:
            reader = csv.DictReader(csvfile)
            for current_row in reader:
                if "id" in current_row:
                    if current_row['id'].isdigit():
                        add=requests.get(serveradress+'/shelf/add/'+shelf_id+'/'+current_row['id'],cookies=r.cookies,headers=headers)
                        if add.status_code != 200:
                            print('Error: Failed to add book with id %s to shelf %s'%(current_row['id'],shelf_id))
                        else:
                            message = re.findall(u"id=\"flash_.*class=.*>(.*)</div>", add.content.decode('utf-8'))
                            if not message:
                                print('Error: Book with id %s already in shelf, or shelf not exisitend'%(current_row['id']))
                            else:
                                print('Book with id %s was added to shelf with message: %s'%(current_row['id'],message[0]))
                    else:
                        print('Error: id %s is not a number'%current_row['id'])
                else:
                    print("No ID-field found in current row of csv file, check for seperation character (has to be ',') and spelling of 'id' field")
                    exit()
    else:
        print('Error: Could not log in to calibre-web')
else:
    print('Error: Shelf_id is not a number')




