from io import DEFAULT_BUFFER_SIZE
import pandas as pd
def array_to_String(array_list):
    Result_String = ''
    for value in array_list:
        if Result_String == '':
            Result_String = value
        else:
            Result_String = Result_String + ' , '+value
    return Result_String


json_file = 'D:\Documents\Python\input\json_sample.json'
df = pd.read_json(json_file)
print(df.head(10))
df["systemOwner_String"] = df.systemOwner.apply(array_to_String)
df["systemStakeholder_String"] =df.systemStakeholder.apply(array_to_String)
df["businessAnalyst_String"] =df.businessAnalyst.apply(array_to_String)
df["technicalOwner_String"] =df.technicalOwner.apply(array_to_String)
print(df.head(10))
csv_file = 'D:\Documents\Python\input\json_csv.csv'
df.to_csv(csv_file)