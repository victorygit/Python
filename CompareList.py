from numpy import sort


list1 = ['Ada', 'Bucky', 'Angelica','Chrissy']
list2 = ['Chrissy','Angelica','Bucky','Ada']
match_list = []
for i in range(0, len(list1)):
    pair = []
    pair.append(list1[i])
    pair.append(list2[i])
    match_list.append(pair)
print(match_list)
# compare
total_match = []
for i in range(0, len(list1)):
    partner1 = []
    print(list1[i])
    for item in match_list:
        if list1[i] in item:
            partner1.append(item)
    print(partner1)
    total_match.append(partner1)
print(total_match)

for item in total_match:
    if item[0].sort() == item[1].sort():
        print('True')
