import pymongo

client = pymongo.MongoClient('mongodb://mongodb:27017', connect=False)
db = client.NUS
col = db["ImageRepo"]

labels = 'test, lol'
url = "https://res.cloudinary.com/dtpgi0zck/image/upload/s--fMAvJ-9u--/c_fit,h_580,w_860/v1/EducationHub/photos/sun-blasts-a-m66-flare.jpg"

file1 = open('words.txt', 'r')
words = file1.readlines()

for i in range(10):
  for w in words:
    name = w.strip() + str(i)
    document = {'name': name, 'labels': labels, 'url': url}
    col.insert_one(document)

  
