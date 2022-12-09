from pymongo import (
    MongoClient,
    errors
)


def main():
    CONNECTION_STRING = "mongodb+srv://pcbuilder:pcbuilder@pcbuilder.pbtoqu6.mongodb.net/?retryWrites=true&w=majority"

    client = MongoClient(CONNECTION_STRING)
    db = client.pcbuilder
    test_collection = db.processor

    print(db)

    #''' Per inserire:
    example = {
        "_id" : "i5-11600",
        "name" : "core",
        "brand" : "intel",
        "n_core" : 6,
        "freq_turbo" : 4.8,
        "freq_base" : 2.8,
        "cache" : "12MB",
        "price" : 205,
    }

    try:
        test_collection.insert_one(example)
    except errors.DuplicateKeyError as e:
        print("Duplicate Key Error - document is probably already inserted")
    
    #''' 

    #for x in test_collection.find(): #Stampa tutti i processori inseriti
    #   print(x)

    # Fai una query: trova i processori della marca amd
    cursor = db.processor.find({"brand": "amd"})

    for x in cursor:
        print(x)
    
    # Eliminare un document dal db:
    #db.processor.delete_one({"brand" : "intel"})
    
    print("\n====================\n")

    cursor = db.processor.find(); # Query che ritorna tutti i processori
    for x in cursor: 
        print(x)

    client.close()


    


    
if __name__ == "__main__":
    main()