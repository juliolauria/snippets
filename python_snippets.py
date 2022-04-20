from datetime import datetime

#####
# Execution time
#####

startTime = datetime.now()

# code here

print("tempo de execução: " + str(datetime.now() - startTime).split('.')[0])
