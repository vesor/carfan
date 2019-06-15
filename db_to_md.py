
import tinydb
from datetime import datetime

db = tinydb.TinyDB('tinydb.json')

qr = tinydb.Query()
result = db.search(qr.score >= 0)
#print (len(result))
with open('db.md','w') as f:
    f.write('| car | car_age | Normal TVOC | Normal HCHO | High TVOC | High HCHO | Drive TVOC | Drive HCHO |\n')
    f.write('| --- | --- | --- | --- | --- | --- | --- | --- |\n')
    for rc in result:
        car_age = '-'
        if 'test_date' in rc:
            d1 = datetime.strptime(rc['test_date'], '%Y-%m')
            if 'car_date' in rc:
                d2 = datetime.strptime(rc['car_date'], '%Y-%m')
                months, days = divmod((d1 - d2).days, 30)
                car_age = '{:d}m'.format(months)
            elif 'model_date' in rc:
                d2 = datetime.strptime(rc['model_date'], '%Y-%m')
                months, days = divmod((d1 - d2).days, 30)
                car_age = '{:d}m(est.)'.format(months)
            

        normal_tvoc = '-' if 'TVOC' not in rc['normal_mode'] else str(rc['normal_mode']['TVOC'])
        high_tvoc = '-' if 'TVOC' not in rc['hightemp_mode'] else str(rc['hightemp_mode']['TVOC'])
        drive_tvoc = '-' if 'TVOC' not in rc['drive_mode'] else str(rc['drive_mode']['TVOC'])
        f.write('| ' + rc['car_name'] + ' | ' + car_age + ' | ' \
            + normal_tvoc + ' | ' + str(rc['normal_mode']['HCHO']) + ' | ' \
            + high_tvoc + ' | ' + str(rc['hightemp_mode']['HCHO']) + ' | ' \
            + drive_tvoc + ' | ' + str(rc['drive_mode']['HCHO']) + ' |\n')
