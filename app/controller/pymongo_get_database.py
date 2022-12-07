from pymongo import MongoClient


def main():
    CONNECTION_STRING = "mongodb+srv://pcbuilder:pcbuilder@pcbuilder.pbtoqu6.mongodb.net/?retryWrites=true&w=majority"

    client = MongoClient(CONNECTION_STRING)
    db = client.pcbuilder
    test_collection = db.processor

    print(db)

    for x in test_collection.find(): #Stampa tutti i processori inseriti
        print(x)
    
    client.close()


    ''' Per inserire:
    example = {
        "_id" : "000001",
        "item_name" : "i5",
        "brand" : "intel",
        "num" : "11600",
        "n_core" : 6,
        "freq_turbo" : 4.80,
        "freq_base" : 2.80,
        "cache" : "12MB"  
    }

    test_collection.insert_one(example)
    ''' 


    
if __name__ == "__main__":
    main()