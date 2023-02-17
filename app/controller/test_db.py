from pymongo import MongoClient
from pymongo_interface import PymongoInterface


def main():
    #CONNECTION_STRING = "mongodb+srv://pcbuilder:pcbuilder@pcbuilder.pbtoqu6.mongodb.net/?retryWrites=true&w=majority"
    CONNECTION_STRING = "mongodb+srv://pcbuilderdev:pcbuilderdev@pcbuilder-cluster.2hbnofk.mongodb.net/?retryWrites=true&w=majority"

    client = PymongoInterface(CONNECTION_STRING)
    db = client.get_db()

    #for x in cllct.find(): #Stampa tutti gli elementi della collezione
    #    print(x)

    # Per inserire:
    '''
    example = {
        "_id" : "Dual RTX 3060 V2",
        "brand" : "NVIDIA Geforce",
        "memory_size" : "12GB",
        "power_consumption" : 200,
        "price" : 400,
    }
    '''
    '''
    example = {
        "name" : "LC6850M",
        "brand" : "lc-power",
        "mwe" : 850,
        "price" : 95
    }
    '''

    '''
    example = {
        "_id" : "B660-PLUS D4",
        "name" : "Prime",
        "brand" : "Asus",
        "memory_slots" : 4,
        "memory_standard" : "DDR4",
        "form_factor" : "ATX",
        "socket" : "LGA 1700",
        "price" : 200
    }
    '''
    '''
    example = {
        "name" : "P5",
        "brand" : "Crucial",
        "capacity_T" : 1.0,
        "form_factor": "M.2",
        "price" : 80,
    }
    '''

    cllct = db.gpu
    example1 = {"_id":"Intel Core i5-11600","n_core":{"$numberInt":"6"},"socket":"LGA1200","price":{"$numberInt":"205"},"TDP":{"$numberInt":"65"},"url":"https://www.amazon.it/Processore-Intel-i5-11600-Desktop-LGA1200/dp/B08X5XWNTB/"}
    example2 = {"_id":"Amd Ryzen 5-5600","n_core":{"$numberInt":"6"},"socket":"AM4","price":{"$numberInt":"105"},"TDP":{"$numberInt":"65"},"url":"https://www.amazon.it/Ryzen-5600-Ventola-Wraith-Stealth/dp/B09VCHR1VH"}
    example3 = {"_id":"Intel Core i5-12400F","n_core":{"$numberInt":"6"},"socket":"LGA1200","price":{"$numberInt":"200"},"TDP":{"$numberInt":"65"},"url":"https://www.amazon.it/Intel-i5-12400F-processore-generazione-frequenza/dp/B09MDFH5HY"}

    mb_example1 = {"_id":"ASRock Steel Legend B550M","memory_slots":{"$numberInt":"4"},"memory_standard":"DDR4","form_factor":"micro ATX","socket":"AM4","price":{"$numberInt":"141"}, "url":"https://www.amazon.it/Asrock-B550M-Legend-supporta-generazione/dp/B089W2Q2QC/"}
    mb_example2 = {"_id":"ASUS Prime AB660-PLUS D4","memory_slots":{"$numberInt":"4"},"memory_standard":"DDR4","form_factor":"ATX","socket":"LGA 1700","price":{"$numberInt":"200"}, "url": "https://www.amazon.it/ASUS-LGA1700-Ethernet-Realtek-Surround/dp/B09JM7W3VS/"}

    gpu_example1 = {"_id":"AMD Radeon RX 6600","memory_size":"8GB","power_consumption":{"$numberInt":"140"},"form_factor":"ATX","price":{"$numberInt":"300"}, "url": "https://www.amazon.it/MSI-Radeon-6600-Scheda-video/dp/B09GW3XN7K/"}
    gpu_example2 = {"_id":"AMD Radeon RX 6650 XT","memory_size":"8GB","power_consumption":{"$numberInt":"180"},"price":{"$numberInt":"400"}, "url" : "https://www.amazon.it/MSI-Radeon-6650-MECH-GDDR6/dp/B09YHXT12P/"}
    gpu_example3 = {"_id":"NVIDIA Geforce Dual RTX 3060 V2","memory_size":"12GB","power_consumption":{"$numberInt":"200"},"price":{"$numberInt":"400"}, "url" : "https://www.amazon.it/ASUS-RTX3060-12G-V2-NVIDIA-GeForce-GDDR6/dp/B09665GZW8/"}

    cllct.insert_one(gpu_example3)
    
    client.close()

    
if __name__ == "__main__":
    main()