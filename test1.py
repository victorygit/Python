str1 = ",p1,p2"
str2 = "p2,p1"
list1 = str1.split(",")
list2 = str2.split(",")
if list1.sort() == list2.sort():
    print ("correct")