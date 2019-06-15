
import tinydb
import os
import requests

db = tinydb.TinyDB('tinydb.json')

qr = tinydb.Query()
result = db.search(qr['report_scans'].exists())

def check_create_folder(folder):
    assert not os.path.isfile(folder)
    if not os.path.exists(folder):
        os.mkdir(folder)

tmp_folder = 'tmp'
check_create_folder(tmp_folder)

for rc in result:
    rc_folder = os.path.join(tmp_folder, str(rc['id']))
    check_create_folder(rc_folder)
    for i, url in enumerate(rc['report_scans']):
        img_data = requests.get(url).content
        with open(os.path.join(rc_folder, '{:d}.jpg'.format(i)), 'wb') as f:
            f.write(img_data)