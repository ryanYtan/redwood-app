"""
Populates a local database with example data for development
"""
import requests
import psycopg2
import os

connection_string = os.getenv('REDWOOD_SQLALCHEMY_DATABASE_URI', None)
if connection_string is None:
    raise ValueError('No connection string')

conn = psycopg2.connect(connection_string)
cur = conn.cursor()

#add users
user_data = [
    ('suomi123', 'password123'),
    ('tanyu', 'qwerty123'),
    ('richardbest', 'xyz123'),
    ('sergeant_scully', '890123'),
    ('gamecom', 'guhioefeiohe'),
]

#for u, pw in user_data:
#    data = { 'username': u, 'password': pw }
#    res = requests.post('http://localhost:8080/signup', json=data)
#    print(res.content)



#add items
data = [
    ('C8D570C1-6F99-41A0-945E-6AB0DE5FA40E', 'suomi123', 'Mug', 'It is a mug', '', 3.99),
    ('8EC79F89-E511-4BDE-A508-00B946B99BF8', 'suomi123', 'Table', 'Hey, it is a table', '', 200),
    ('C18518DE-6AFB-4FA3-8961-3D3A3A3807F9', 'suomi123', 'smartphone', 'Samsung Galaxy', '', 900),
    ('ED3346A9-A6F8-47E5-8ADB-6DE33DF5A15C', 'suomi123', 'Backpack', 'For backing your pack', '', 120.50),
    ('408A6BEA-4B0D-486E-B0C3-F80768456F75', 'suomi123', 'Socks', 'Freshly used', '', 100),
    ('ED319988-002D-4A2F-9E79-2DF57265DA26', 'tanyu', 'McDonalds', 'Yes, the entire franchise', '', 100000),
    ('ECBEDAAC-0AA6-480C-A585-A37F9F895445', 'tanyu', 'Lawn Chair', 'Never seen one of these have you?', '', 5),
    ('0012794D-6542-4AC6-8DC2-05F8EC510F07', 'tanyu', 'Fire Extinguisher', 'May have been used', '', 1),
    ('3906AB91-C94D-46DC-A3EE-71AB40582EEF', 'tanyu', 'Slippers', 'Torn and broken', '', 2),
    ('1D598446-9C90-449D-846B-885F63908D9C', 'tanyu', 'PS5', 'Best deal, take it or leave it', '', 999),
    ('14276859-0E1F-401C-80CA-B489E89D3F4E', 'richardbest', 'M1 Helmet', 'From European adventures', '', 95),
    ('4E7D9F7C-C922-4E77-BDF5-DB498E4A337F', 'richardbest', '2x4', '2 by 4', '', 5),
    ('31A7B2BE-E214-4686-8A9C-098F7A8E79F1', 'richardbest', 'Pliers', 'Great for the field', '', 4.99),
    ('217993F8-A6AC-4C4D-BB53-AF6BBAE34876', 'richardbest', 'Wine', 'Drunk buddy', '', 998.12),
    ('67FDF930-B602-4044-9D38-A1E411C3CA22', 'richardbest', 'Baseball', 'Signed by JJ Hardy', '', 123.45),
    ('8A95D01D-99E9-4F50-A979-B3FFF6B8E25D', 'richardbest', 'D20 Die', 'Roll for check', '', 30.0),
    ('9AAD6589-81A2-4388-9832-E3AA0943D547', 'richardbest', 'Automatic Door', 'I stole it', '', 535),
    ('DA793688-DC59-40AB-8811-8C6C644DFA24', 'richardbest', 'Wallet', 'I found it on the floor', '', 0.10),
    ('C42F05F4-9C94-4691-829F-68CD75B4D8BB', 'sergeant_scully', 'An Argentinian Peso', 'haha funny joke', '', 9999),
    ('2C868B11-DD28-4306-B897-3F77316DDD86', 'sergeant_scully', 'CD-32', 'Old', '', 1),
    ('F5A4626A-FAF6-45D4-82BE-33006417FCF6', 'sergeant_scully', 'CD from the 80s', 'It may work', '', 2),
    ('84A0CDA8-44F2-4D54-AF72-F38F409FC76A', 'sergeant_scully', 'Torrent', 'Elden Ring horse', '', 888),
]

#for a, b, c, d, e, f in data:
#    cur.execute('INSERT INTO item VALUES (%s, %s, %s, %s, %s, %s)', (a, b, c, d, e, f))
#    conn.commit()

data = [
    ('C8D570C1-6F99-41A0-945E-6AB0DE5FA40E', 'tanyu'),
    ('8EC79F89-E511-4BDE-A508-00B946B99BF8', 'richardbest'),
    ('C18518DE-6AFB-4FA3-8961-3D3A3A3807F9', 'richardbest'),
    ('ED3346A9-A6F8-47E5-8ADB-6DE33DF5A15C', 'sergeant_scully'),
    #('408A6BEA-4B0D-486E-B0C3-F80768456F75', ''),
    ('ED319988-002D-4A2F-9E79-2DF57265DA26', 'richardbest'),
    ('ECBEDAAC-0AA6-480C-A585-A37F9F895445', 'suomi123'),
    ('0012794D-6542-4AC6-8DC2-05F8EC510F07', 'sergeant_scully'),
    #('3906AB91-C94D-46DC-A3EE-71AB40582EEF', ''),
    #('1D598446-9C90-449D-846B-885F63908D9C', ''),
    ('14276859-0E1F-401C-80CA-B489E89D3F4E', 'tanyu'),
    ('4E7D9F7C-C922-4E77-BDF5-DB498E4A337F', 'sergeant_scully'),
    ('31A7B2BE-E214-4686-8A9C-098F7A8E79F1', 'suomi123'),
    ('217993F8-A6AC-4C4D-BB53-AF6BBAE34876', 'suomi123'),
    ('67FDF930-B602-4044-9D38-A1E411C3CA22', 'suomi123'),
    ('8A95D01D-99E9-4F50-A979-B3FFF6B8E25D', 'tanyu'),
    #('9AAD6589-81A2-4388-9832-E3AA0943D547', ''),
    #('DA793688-DC59-40AB-8811-8C6C644DFA24', ''),
    ('C42F05F4-9C94-4691-829F-68CD75B4D8BB', 'richardbest'),
    #('2C868B11-DD28-4306-B897-3F77316DDD86', ''),
    #('F5A4626A-FAF6-45D4-82BE-33006417FCF6', ''),
    #('84A0CDA8-44F2-4D54-AF72-F38F409FC76A', ''),
]

for a, b in data:
    cur.execute('INSERT INTO transaction VALUES (%s, %s)', (b, a))
    conn.commit()
