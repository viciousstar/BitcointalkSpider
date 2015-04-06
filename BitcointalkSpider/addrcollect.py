import json
import re
from validator import validate
f = open("userdata.json")
lines = f.readlines()
out = open("address.json", "w")
pattern = re.compile(r'[13][a-km-zA-HJ-NP-Z0-9]{26,33}')
count = 0
mbcount = 0
fake = 0
for line in lines:
    data = json.loads(line)
    name = data["name"]
    results = pattern.findall('\n'.join(data["bitcoinAddress"]))
    address = []
    for addr in results:
    	if addr not in address:
    		if validate(addr):
    			address.append(addr)
    			count += 1
    		else:
    			fake += 1
    if len(address) != 0:
	    out.write(json.dumps({'name': name, 'address': address}) + '\n')
	    mbcount += 1
f.close()
out.close()
print count + fake, "addresses extracted from", len(lines), "records, from which", count, "addresses for", mbcount, "members validated to be Bitcoin(or bitcoin-like) address." 