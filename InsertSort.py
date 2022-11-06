number = [23,56,2,5,89,34,67,1]

def InsertSort(number_list):
    for i in range(0, len(number_list)):
        for j in range(i, 0, -1):
            if number_list[j] < number_list[j-1]:
                swap = number_list[j-1]
                number_list[j-1] = number_list[j]
                number_list[j] = swap
        print(number_list)


#main
InsertSort(number)
