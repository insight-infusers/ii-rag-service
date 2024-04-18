from pymongo import MongoClient

class DocumentDB:
    def __init__(self, uri="mongodb://localhost:27017"):
        self.client = MongoClient(uri)
        self.db = self.client['your_db']
        self.collection = self.db['documents']

    def store_document(self, document_id, text):
        self.collection.insert_one({"_id": document_id, "text": text})

    def retrieve_document(self, document_id):
        result = self.collection.find_one({"_id": document_id})
        return result['text'] if result else None
