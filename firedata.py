from contextlib import closing
import firebase_admin
from firebase_admin import credentials, firestore
import json

cred = credentials.Certificate("wind-info-firebase-adminsdk-tfxe3-aa9146d5b8.json.secret")
firebase_admin.initialize_app(cred)
db = firestore.client()

def writeWindReads(jsonRead):
    try:
        # firebase timestamp
        jsonRead['_scrapTimeStamp'] = firestore.firestore.SERVER_TIMESTAMP
    except:
        pass
    finally:
        doc_ref = db.collection(u'wind-reads').document()
        doc_ref.set(jsonRead)

def readWindReads(readSource, limitReads = 6):
    # Get the last 5 wind-reads for a particular source 
    windreads_ref = db.collection(u'wind-reads')
    query = windreads_ref.where(u'_infoSourceName', u'==', readSource).order_by(u'_scrapTimeStamp', direction=firestore.firestore.Query.DESCENDING).limit(limitReads)
    result = query.get()
    docs = list()
    #return [doc.to_dict() for doc in result]
    for doc in result:
        data = doc.to_dict()
        # adding doc.id to the dictionary for later update and identify usage
        data.update({"_id" : doc.id})
        docs.append(data)
    return docs

def setWindAlert(doc_id, wind_change):
    windreads_ref = db.collection(u'wind-reads').document(doc_id)
    windreads_ref.update({
        u'_readAlerted' : True,
        u'_windChanged' : wind_change
    })