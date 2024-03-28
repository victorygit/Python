# importing pandas as pd
import pandas as pd
  
# Creating the first dataframe 
df1 = pd.DataFrame({"A":[1, 5, 3, 4, 2],
                    "B":[3, 2, 4, 3, 4],
                    "C":[2, 2, 7, 3, 4], 
                    "D":[4, 3, 6, 12, 7]} 
)
  
# Creating the second dataframe
df2 = pd.DataFrame({"A":[1, 5, 3, 4, 2],
                    "B":[3, 2, 4, 3, 4],
                    "C":[2, 2, 7, 3, 4], 
                    "D":[4, 3, 6, 12, 7]} 
)
# subtract df2 from df1
df_diff= df1.subtract(df2)
print(df_diff)
#print(df_diff.count())
