import os
from datetime import datetime

#####
# Execution time
#####

startTime = datetime.now()

# code here

print("Execution time: " + str(datetime.now() - startTime).split('.')[0])
print(f"Execution time for {os.path.basename(__file__)}: {str(datetime.now() - startTime).split('.')[0]}")

# Ignore warnings

warnings.filterwarnings("ignore", module="lightgbm")

###
# Debug
###

import pdb
pdb.set_trace()

# get code and move to a new python session
# !import code; code.interact(local=vars())

# Save data to JSON
with open("temp/dev_masterdata/masterdata_cvt.json", 'w') as json_file:
    json.dump(master_data, json_file, indent=4)

# Load data from JSON file
with open("temp/dev_masterdata/masterdata_cvt.json", 'r') as json_file:
    master_data = json.load(json_file)

# Save Master Data
import json
# company_id = website.code.lower() # 'e.g., fc'
company_id = 'cl'
with open(f"temp/dev_masterdata/masterdata_{company_id}.json", 'w') as json_file:
    json.dump(master_data, json_file)
    
# Debug
import pdb
pdb.set_trace()

# Exactly the same as pdb.set_trace:
breakpoint() 

# virtual environment
python -m venv venv

.venv\Scripts\activate

# get variables, methods and values from an unknown object
vars(obj)
dir(obj) # or simply dir()