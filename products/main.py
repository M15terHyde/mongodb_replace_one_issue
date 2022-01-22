# Fix import issues
from sys import path as syspath
from sys import stderr
from os import path as ospath
syspath.append( ospath.dirname(ospath.abspath(__file__)).rsplit('\\', 1)[0]  )

from fastapi import FastAPI, Response
from pymongo import MongoClient, GEOSPHERE
from pydantic import BaseModel
from sys import stderr
import json
#import jsonpickle



import logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(levelname)7s: %(message)s',
    stream=stderr,
)
log = logging.getLogger('')

import pprint
pp = pprint.PrettyPrinter(indent=2)



# Define service hostnames and ports
mongo_url = 'mongo'#'mongo'



# Connect to mongo database
log.info("Connecting to database...")
# Note: 'localhost' tells the api container to connect to itself, not to the mongo container.
# mongo is the docker service name of the mongodb containter. We're connected via docker-compose networks
client = MongoClient(mongo_url, 27017)#, username='root', password='password')
log.info("Connected to database")
allprods = client.products.allproducts



app = FastAPI()



@app.on_event("startup")
async def startup_event():
    # Verify 2dsphere index of the products.allproducts for fast lookups
    if 'geoindex' not in allprods.index_information():
        log.info("GEOSPHERE index geoindex does not exist. Creating.")
        allprods.create_index( [("latlong", GEOSPHERE)], name='geoindex' )

    log.info("... complete")



# Health check
@app.get("/hi")
async def hi():
    return Response(content= 'hi', media_type="text/html")



class Product(BaseModel):
    foreignAPIAuthority: str
    productID: str
    locationID: str
    latlong: list # [lat, long] = [float, float]
    datetime: str
    aisleLocations: list | None = None
    categories: list | None = None
    brand: str | None = None
    description: str
    images: list
    prices: list # [amount, currency] = [float, string]
    fulfillmentType: list | None = None
    countryOfOrigin: str | None = None

'''
Insert a single location document that conforms to the Location data model.
Returns the '_id' field of the document replaced or inserted.
If the document didn't previously exist then it is upserted (inserted) and this new document's '_id' is returned as JSON
If the document did previously exist then it replaces the old one and this replacement's '_id' is returned as JSON.
'''
@app.post("/addone")
async def addone( product: Product ):
    log.info( "addone:\n{}".format(product.__dict__) )

    # Add to MongoDB
    # Using replace_one(upsert=True) instead of insert_one ensures duplicates aren't created for the same foreignAPIAuthority,locationID,productID pairing.
    ret = allprods.replace_one(
        {
            'foreignAPIAuthority': product.foreignAPIAuthority,
            'locationID': product.locationID,
            'productID': product.productID,
        },
        product.__dict__,
        upsert=True,
    )
    print( "replace_one result: {}".format(ret.raw_result) )
    if ret.upserted_id is not None:
        resp = str(ret.upserted_id)
        print("upserted_id: "+resp)
    else:
        resp = str(allprods.find_one({'foreignAPIAuthority': product.foreignAPIAuthority, 'locationID': product.locationID})['_id'])
        print("modified item id: "+str(resp))

    return Response(content= json.dumps(resp), media_type="application/json")



########################################################################################
# Drivers for Testing
########################################################################################

@app.delete("/testing_cleanup")
async def testing_cleanup():
    
    # All 'TEST' docs should be deleted
    docs = []
    for doc in allprods.find( {'foreignAPIAuthority':'TEST'} ):
        docs.append( str(doc['_id']) )

    # delete from mongo
    res = allprods.delete_many( {'foreignAPIAuthority':'TEST'} )

    return {'found':len(docs), 'deleted':res.deleted_count, }