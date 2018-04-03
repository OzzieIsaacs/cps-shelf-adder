import requests
import csv

username = 'admin'
password = ''
shelf_id = '1'
booklist = 'booklist.csv'
serveradress = 'http://127.0.0.1:8083'

error=False
r = requests.post(serveradress+'/login?next=/', data = {'username':username,'password':password,'submit':'', 'remember_me':'on', 'next':'/'})
headers = {'Referer': serveradress+'/'}
if "login" in r.text:
    error=True
if r.status_code == 200 and not error:
    with open(booklist) as csvfile:
        reader = csv.DictReader(csvfile)
        for current_row in reader:
            add=requests.get(serveradress+'/shelf/add/'+shelf_id+'/'+current_row['id'],cookies=r.cookies,headers=headers)
            if add.status_code != 200:
                print('Failed to add book with id %s to shelf %s'%(current_row['id'],shelf_id))
            else:
                print('Book with id %s was sucessfully add to shelf'%(current_row['id']))
else:
    print('Could not log in to calibre-web')



