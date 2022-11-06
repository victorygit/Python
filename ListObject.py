from importlib.resources import open_text


class  lifelostRecord:
    def __init__(self, recordstring) -> None:
        #Ref_Date,GEO,SEX,CAUSES,UNIT,Value
        string_list = recordstring[:-1].split(',')        
        self.__ref_Date = int(string_list[0])
        self.__GEO = string_list[1]
        self.__SEX = string_list[2]
        self.__CAUSES = string_list[3]
        self.__UNIT = string_list[4]
        self.__Value = float(string_list[5].strip())
        
    def __str__(self) -> str:
        return (' Ref_Date: '+ str(self.__ref_Date) + ' GEO: '+ self.__GEO + ' SEX: ' + self.__SEX + ' CAUSES: ' + self.__CAUSES + ' UNIT: ' + self.__UNIT + ' Value: ' + str(self.__Value))
    
    def get_value(self):
        return self.__Value
            
    def get_year(self):
        return self.__ref_Date

    
    def get_causes(self):
        return self.__CAUSES

file = open('input/lifeLostbyCauseData.txt','r')
file_content = file.readlines()

Record_list = []
count = 1
for row in file_content:
    if count > 1:
        record = lifelostRecord(row)
        Record_list.append(record)
    count= count + 1

#Total loft Lost
total_life_lost = 0
for record in Record_list:
    total_life_lost = total_life_lost + record.get_value()

print(total_life_lost )

#Total lof0t Lost
year = 2021
life_lost_byyear = 0
for record in Record_list:
    if record.get_year() == year:
        life_lost_byyear = life_lost_byyear + record.get_value()
print(life_lost_byyear )