import requests
import csv
import re
import sys

username = 'admin'
password = 'admin123'
shelf_id = '1'
booklist = 'Meine Bücher.csv'
server_address = 'http://127.0.0.1:8083'

error = False
if not shelf_id.isdigit():
    print('Error: Shelf_id is not a number')
    sys.exit(1)

r = requests.session()
try:
    login_page = r.get(server_address + '/login')
    token = re.search('<input type="hidden" name="csrf_token" value="(.*)">', login_page.text)
    resp = r.post(server_address + '/login?next=/', data={'username':username,
                                                         'password':password,
                                                         'submit': '',
                                                         'remember_me': 'on',
                                                         'next': '/',
                                                         "csrf_token": token.group(1)})
except Exception as e:
    print("Error connecting to calibre-web : %s" % e)
    r.close()
    sys.exit(1)

headers = {'Referer': server_address + '/'}
if "login" in resp.text or resp.status_code != 200:
    print('Error: Could not log in to calibre-web')
    r.close()
    sys.exit(1)
try:
    if sys.version_info.major >= 3:
        csv_f = open(booklist, newline='')
    else:
        csv_f = open(booklist)
except Exception as e:
    print("Error on opening bookslist file: %s" % e)
    r.close()
    sys.exit(1)
with csv_f as csvfile:
    reader = csv.DictReader(csvfile)
    for current_row in reader:
        if "id" or "\ufeffid" in current_row:
            id = current_row.get('id', current_row.get("\ufeffid"))
            if id.isdigit():
                shelf_page = r.get(server_address + '/shelf/create')
                token = re.search('<input type="hidden" name="csrf_token" value="(.*)">', shelf_page.text)
                payload = {"csrf_token": token.group(1)}
                add = r.post(server_address + '/shelf/add/' + shelf_id + '/' + id,
                             data=payload,
                             cookies=r.cookies,
                             headers=headers)
                if add.status_code != 200:
                    print('Error: Failed to add book with id %s to shelf %s' % (id, shelf_id))
                else:
                    message = re.findall(u"id=\"flash_.*class=.*>(.*)</div>", add.content.decode('utf-8'))
                    if not message:
                        print('Error: Book with id %s already in shelf, or shelf not existing' % (id))
                    else:
                        print('Request to add Book with id %s to shelf was successfully send. Calibre-Web Response: %s' % (id, message[0]))
            else:
                print('Error: id %s is not a number' % id)
        else:
            print("No ID-field found in current row of csv file, check for seperation character (has to be ',') and spelling of 'id' field")
            r.close()
            sys.exit(1)
r.close()
print("script finished successfully")





