from sys import path as syspath
from sys import stderr
from os import path as ospath

syspath.append( ospath.dirname(ospath.abspath(__file__)).rsplit('\\', 1)[0]  )

import asyncio
from sys import stderr
import logging
from support import asyncSupport
#from pymongo import MongoClient, GEOSPHERE
import json
from copy import deepcopy
from datetime import datetime, timedelta
from time import sleep



logging.basicConfig(
    level=logging.DEBUG,
    format='%(levelname)7s: %(message)s',
    stream=stderr,
)
log = logging.getLogger('')



async def healthcheck(locationsURL=None, locationsPort=None):
    locationsurl = 'localhost'
    locationsport = 80
    if locationsURL:
        locationsurl = locationsURL
    if locationsPort:
        locationsport = locationsPort
    
    path = 'hi'
    url = 'http://{0}:{1}/{2}'.format(locationsurl, locationsport, path)
    # build the request to insert the doc
    urlObjs = [{
        'url': url,
        'data': None,
        'headers': {}
    }]
    await asyncSupport.batchGetURLs(urlObjs)
    print(urlObjs[0]['data'])

    if urlObjs[0]['data'] == 'hi':
        print("HEALTHCHECK PASS")
    else:
        print("HEALTHCHECK FAIL")



# Testing: addone
# Insert a document
async def test1(locationsURL=None, locationsPort=None):
    
    locationsurl = 'localhost'
    locationsport = 80
    if locationsURL:
        locationsurl = locationsURL
    if locationsPort:
        locationsport = locationsPort

    # Insert a document
    class Product():
        def __init__(self):
            foreignAPIAuthority = ''
            productID = ''
            locationID = ''
            latlong = ''
            datetime = ''
            aisleLocations = []
            categories = []
            brand = ''
            description = ''
            images = []
            price = ''
            fulfillmentType = []
            countryOfOrigin = ''
    
    # Make valid first two products
    myprod = Product()
    myprod.foreignAPIAuthority = 'TEST'
    myprod.productID= '1234'
    myprod.locationID= '1'
    myprod.latlong = [0.0, 0.0]
    myprod.datetime = datetime.now().isoformat()
    myprod.aisleLocations= ['blah blah', '111']
    myprod.categories= ['dairy', 'breakfast']
    myprod.brand = 'Test Brand'
    myprod.description = '1 Gallon of milk'
    myprod.images = [
        {'size':'small', 'url':'https:testnet.com/img_small'},
        {'size':'medium', 'url':'https:testnet.com/img_medium'},
        {'size':'large', 'url':'https:testnet.com/img_large'},
    ]
    myprod.prices = [3.49, 'USD']
    myprod.fulfillmentType = ['in-store']
    myprod.countryOfOrigin = 'USA'
    # Make another product at the same location
    myprod2 = deepcopy(myprod)
    myprod2.productID = '1235'
    
    # Make duplicates of myprod & myprod2 with only a minor change
    myprod3 = deepcopy(myprod)
    myprod3.brand = 'Updated brand'
    myprod4 = deepcopy(myprod2)
    myprod4.brand = 'Updated brand'

    # Make another 2 products at a different location.
    # The location should not exist. This will test /validate for valid products at non-existant location
    # locationID = 9999, productID = 1234, 1235
    myprod5 = deepcopy(myprod)
    myprod5.locationID = '9999'
    myprod5.latlong = [0.00001, 0.00001]
    myprod5.datetime = (datetime.fromisoformat(myprod5.datetime) - timedelta(days=1, seconds=1)).isoformat()
    myprod6 = deepcopy(myprod5)
    myprod6.productID = '1235'

    # Make another 2 products at a different location. Make them outdated
    # The products should not exist. This will test /validate for non-existant products at existant location
    # locationID = 2, productID = 9999, 9998
    myprod7 = deepcopy(myprod)
    myprod7.locationID = '2'
    myprod7.latlong = [-0.00001, 0.00001]
    myprod7.productID = '9999'
    myprod7.datetime = (datetime.fromisoformat(myprod7.datetime) - timedelta(days=1, seconds=1)).isoformat()
    myprod8 = deepcopy(myprod7)
    myprod8.productID = '9998'

    # Make another 2 products at a different location. Make them outdated
    # The products and location should exist. This will test /validate for existing products and locations.
    # locationID = 3, productID = 1234, 1235
    myprod9 = deepcopy(myprod)
    myprod9.locationID = '3'
    myprod9.latlong = [0.00001, -0.00001]
    myprod9.productID = '1234'
    myprod9.datetime = (datetime.fromisoformat(myprod9.datetime) - timedelta(days=1, seconds=1)).isoformat()
    myprod10 = deepcopy(myprod9)
    myprod10.productID = '1235'


    data1 = json.dumps(myprod.__dict__)
    data2 = json.dumps(myprod2.__dict__)
    data3 = json.dumps(myprod3.__dict__)
    data4 = json.dumps(myprod4.__dict__)
    data5 = json.dumps(myprod5.__dict__)
    data6 = json.dumps(myprod6.__dict__)
    data7 = json.dumps(myprod7.__dict__)
    data8 = json.dumps(myprod8.__dict__)
    data9 = json.dumps(myprod9.__dict__)
    data10 = json.dumps(myprod10.__dict__)
    log.info(data1)
    log.info(data2)
    log.info(data3)
    log.info(data4)
    log.info(data5)
    log.info(data6)
    log.info(data7)
    log.info(data8)
    log.info(data9)
    log.info(data10)

    path = 'addone'
    url = 'http://{0}:{1}/{2}'.format(locationsurl, locationsport, path)
    # build the request to insert the doc
    urlObjs = [
    { 'url': url, 'data': data1, 'headers': {'Content-Type': 'application/json'} },
    { 'url': url, 'data': data2, 'headers': {'Content-Type': 'application/json'} },
    { 'url': url, 'data': data3, 'headers': {'Content-Type': 'application/json'} },
    { 'url': url, 'data': data4, 'headers': {'Content-Type': 'application/json'} },
    { 'url': url, 'data': data5, 'headers': {'Content-Type': 'application/json'} },
    { 'url': url, 'data': data6, 'headers': {'Content-Type': 'application/json'} },
    { 'url': url, 'data': data7, 'headers': {'Content-Type': 'application/json'} },
    { 'url': url, 'data': data8, 'headers': {'Content-Type': 'application/json'} },
    { 'url': url, 'data': data9, 'headers': {'Content-Type': 'application/json'} },
    { 'url': url, 'data': data10, 'headers': {'Content-Type': 'application/json'} },
    ]
    for urlObj in urlObjs:
        sleep(.1)
        await asyncSupport.batchPostURLs([urlObj])

    objID1 = json.loads(urlObjs[0]['data'])
    objID2 = json.loads(urlObjs[1]['data'])
    objID3 = json.loads(urlObjs[2]['data'])
    objID4 = json.loads(urlObjs[3]['data'])
    objID5 = json.loads(urlObjs[4]['data'])
    objID6 = json.loads(urlObjs[5]['data'])
    objID7 = json.loads(urlObjs[6]['data'])
    objID8 = json.loads(urlObjs[7]['data'])
    objID9 = json.loads(urlObjs[8]['data'])
    objID10 = json.loads(urlObjs[9]['data'])
    log.info("product1 inserted objectID: {}".format(objID1))
    log.info("product2 inserted objectID: {}".format(objID2))
    log.info("product3 inserted objectID: {}".format(objID3))
    log.info("product4 inserted objectID: {}".format(objID4))
    log.info("product5 inserted objectID: {}".format(objID5))
    log.info("product6 inserted objectID: {}".format(objID6))
    log.info("product7 inserted objectID: {}".format(objID7))
    log.info("product8 inserted objectID: {}".format(objID8))
    log.info("product9 inserted objectID: {}".format(objID9))
    log.info("product10 inserted objectID: {}".format(objID10))

    # Were the items inserted?
    if objID1 is not None and objID1 != '' \
    and objID2 is not None and objID2 != ''\
    and objID3 is not None and objID3 != ''\
    and objID4 is not None and objID4 != ''\
    and objID5 is not None and objID5 != ''\
    and objID6 is not None and objID6 != ''\
    and objID7 is not None and objID7 != ''\
    and objID8 is not None and objID8 != ''\
    and objID9 is not None and objID9 != ''\
    and objID10 is not None and objID10 != '':
        print('TEST1: Insert Feature: PASS')
    else:
        print('TEST1: Insert Feature: FAIL')
    
    # Only one product may have the same foreignAPIAuthority & locationID & productID
    if objID1 == objID3 and objID1 != objID2 and objID2 == objID4:
        print("TEST1: Non-duplication: PASS")
    else:
        print("TEST1: Non-duplication: FAIL")

    return [objID3, objID4]



# Remove the TEST items from the DB
async def cleanup(locationsURL=None, locationsPort=None):
    log.info("Cleaning up")

    locationsurl = 'localhost'
    locationsport = 80
    if locationsURL:
        locationsurl = locationsURL
    if locationsPort:
        locationsport = locationsPort
    
    # build the request
    path = 'testing_cleanup'
    url = 'http://{0}:{1}/{2}?'.format(locationsurl, locationsport, path)
    urlObjs = [{
        'url': url,
        #'data':,
        'headers': {
            'Content-Type': 'application/json',
        },
    }]
    await asyncSupport.batchDeleteURLs(urlObjs)
    ret = json.loads(urlObjs[0]['data'])
    log.info(ret)

    if ret['deleted'] > 0:
        print("CLEANUP PASS")
    else:
        print("CLEANUP FAIL")
        print("DELETE MANUALLY: mongo.products.allproducts.ObjectId('{}')".format(id))



def main():
    log.debug("Getting event loop")
    event_loop = asyncio.get_event_loop()

    log.info("Performing healthcheck")
    event_loop.run_until_complete( healthcheck() )

    # Remove any existing test docs
    log.info("Cleaning up")
    event_loop.run_until_complete( cleanup() )

    log.info("Running test1")
    locationMongoIDs = event_loop.run_until_complete( test1() )

    # Remove the inserted test docs
    log.info("Cleaning up")
    event_loop.run_until_complete( cleanup() )


if __name__ == '__main__':
    main()
