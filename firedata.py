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

def readWindReads(readSource):
    windreads_ref = db.collection(u'wind-reads')
    query = windreads_ref.where(u'_infoSourceName', u'==', readSource).order_by(u'_scrapTimeStamp', direction=firestore.firestore.Query.DESCENDING).limit(6)
    #query = windreads_ref.limit(5)
    result = query.get()
    for doc in result:
         print(u'{} => {}'.format(doc.id, doc.to_dict()))
    print(result)