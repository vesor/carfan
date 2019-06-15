
import tinydb

extra_data = [ #id, normal, high, drive, (-1 means N/A, unit is ug/m2)  test_date, car_date, model_date, car_mileage 
    # model_date is the date that car model start to sale
    811, 241.4, 1316.8, 201.2, '2017-9', '2016-9', '', -1,
    813, 173.6, 1453.2, 264.7, '2017-9', '2017-3', '', -1,
    848, 591.9, 2243.4, -1, '2017-12', '2017-2', '', 15198,
    851, 1123, 13666.7, 1752.4, '2017-9', '2017-8', '', -1,
    856, -1, 2733.4, 1688, '2017-9', '2017-6', '', 71,
    865, -1, 2987.5, 1817.8, '2017-11', '2017-9', '', 0,
    874, -1, 1592, 763, '2017-11', '2017-7', '', 7528,
    876, 1127.7, -1, -1, '2017-12', '2017-10', '', 2588,
    877, -1, 4952.4, 606.4, '2018-1', '2017-9', '', -1,
    881, -1, 3590.2, 2357.3, '', '', '', -1,
    884, 971.5, -1, -1, '2018-1', '2017-10', '', 1644,
    888, -1, -1, -1, '2018-1', '2017-7', '', 2520,
    890, 14957.4, -1, -1, '2018-2', '2017-12', '', 712,
    891, -1, 11641.4, 794.3, '2018-2', '2017-11', '', -1,
    892, -1, -1, -1, '2018-2', '2017-10', '', 2041,
    895, -1, -1, -1, '2018-4', '', '2016-7', -1,
    896, 376.7, 1780.8, 1087.5, '2018-2', '2017-3', '', -1,
    897, 270.7, -1, -1, '2018-5', '2017-6', '', -1,
    898, 349.4, -1, -1, '2018-5', '2017-1', '', -1,
    899, -1, 1083.4, -1, '2018-5', '', '2017-4', -1,
    900, -1, 2822.5, 552.7, '2018-6', '2016-7', '', -1,
    902, 827.3, -1, -1, '2018-5', '2017-9', '', -1,
    904, 2846.4, -1, -1, '2018-5', '2017-11', '', -1,
    905, -1, -1, -1, '2018-5', '2017-9', '', -1,
    907, 1105.3, 4973.1, 603.2, '2018-6', '2017-2', '', -1,
    910, 1512.4, 6348.6, 942.3, '2018-4', '2018-1', '', -1,
    913, 1362.6, 5686.2, 2651.4, '2018-4', '', '2018-4', -1,
    916, -1, -1, -1, '2018-5', '', '2017-1', -1,
    921, -1, 3044.6, 1676.6, '2018-5', '', '2018-3', -1,
    924, 473.6, 4209.2, 661.2, '2018-7', '2018-5', '', -1,
    925, -1, 16190, 8639.8, '2018-6', '2018-3', '2018-6', -1,
    931, 294, 4273, 682.8, '2018-7', '', '2018-6', -1,
]

def ug_to_mg(value):
    value = int(round(value))
    return value / 1000

db = tinydb.TinyDB('tinydb.json')

qr = tinydb.Query()

RECORD_SIZE = 8
assert len(extra_data) % RECORD_SIZE == 0
for i in range(int(len(extra_data)/RECORD_SIZE)):
    id = extra_data[i*RECORD_SIZE]
    tvoc_normal = extra_data[i*RECORD_SIZE+1]
    tvoc_high = extra_data[i*RECORD_SIZE+2]
    tvoc_drive = extra_data[i*RECORD_SIZE+3]
    test_date = extra_data[i*RECORD_SIZE+4]
    car_date = extra_data[i*RECORD_SIZE+5]
    model_date = extra_data[i*RECORD_SIZE+6]
    car_mileage = extra_data[i*RECORD_SIZE+7]
    
    result = db.search(qr['id'] == id)
    assert len(result) == 1
    rc = result[0]
    if tvoc_normal > 0:
        rc['normal_mode']['TVOC'] = ug_to_mg(tvoc_normal)
    if tvoc_high > 0:
        rc['hightemp_mode']['TVOC'] = ug_to_mg(tvoc_high)
    if tvoc_drive > 0:
        rc['drive_mode']['TVOC'] = ug_to_mg(tvoc_drive)
    if len(test_date) > 0:
        rc['test_date'] = test_date
    if len(car_date) > 0:
        rc['car_date'] = car_date
    if len(model_date) > 0:
        rc['model_date'] = model_date
    if car_mileage > 0:
        rc['car_mileage'] = car_mileage
    db.write_back(result)