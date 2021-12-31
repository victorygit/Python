import pandas as pd
import matplotlib.pyplot as plt
df = pd.DataFrame([[1,2],[2,4],[3,9],[4,16]], columns= ["a","b"])
print(df)
df.plot(kind = 'line', x = 'a', y = 'b')
plt.show()
