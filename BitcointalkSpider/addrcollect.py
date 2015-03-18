import json
f = open("userdata.json")
f1 = open("address.txt", "w")
for line in f:
    data = json.loads(line)
    if(len(data["bitcoinAddress"]) != 0):
        f1.write(str(data["bitcoinAddress"]) + ': ' + str(data["name"])+'\n')
