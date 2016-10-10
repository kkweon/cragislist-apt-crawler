import pymongo

mongo = pymongo.MongoClient()
file_name = "result.csv"

low_price = 1500
high_price = 2300

bedroom = 1
conditions = {
    'price': {
        '$gte': str(low_price),
        '$lte': str(high_price)
    },
    'bedroom': str(bedroom)
}

result = mongo.apt.craigslist.find(conditions)

with open("fieldName.txt") as f:
    column_names = [x.strip() for x in f.readlines() if len(x.strip()) > 0]

with open(file_name, "w") as f:
    f.write(",".join(column_names) + "\n")
    count = 0
    for item in result:
        count += 1
        row = []
        for c_name in column_names:
            try:
                row.append(str(item[c_name]).strip())
            except KeyError:
                row.append('')

        f.write(",".join(row) + "\n")

print("Total {} Rows Written to {}!".format(count, file_name))
