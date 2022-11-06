# Using readlines()
file_Input = open('D:\Documents\BI-TEK\OPG\AS7\CatIDHealth_Dev.sql', 'r')
# writing to file
file_Out = open('D:\Temp\TableName.txt', 'w')

Lines = file_Input.readlines()

  
count = 0
# Strips the newline character
for line in Lines:
    table_start_position = line.find("ORSUSR.")
    if table_start_position > 0:
        table_end_position = line.find(" ",table_start_position)
        #print (table_start_position, table_end_position)
        table_name = line[table_start_position:table_end_position]
        print(table_name)
        file_Out.writelines(table_name+"\n")
    count += 1

file_Out.close()

# writing to Step file
file_Out = open('D:\Temp\Step.txt', 'w')
  
count = 0
# Strips the newline character
for line in Lines:
    table_start_position = line.find("stepID")
    if table_start_position > 0:      
        print (line)
        file_Out.writelines(line)
    count += 1


file_Out.close()

# writing to CreateTable file
file_Out = open('D:\Temp\CreateTable.txt', 'w')
  
count = 0
# Strips the newline character
for line in Lines:
    table_start_position = line.find("create table")
    if table_start_position > 0:      
        print (line)
        file_Out.writelines(line)
    count += 1


file_Out.close()