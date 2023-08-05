
# Concatenates the elements in the list and converts them to string values

def clearAndCombineList(mainList = []):
    mainList = str(mainList) 
    newList = str(mainList)
    newList = newList.replace("[","")
    newList = newList.replace("]","")
    newList = newList.replace("'","")
    newList = newList.replace(",","")
    newList = newList.replace(" ","")
    return newList




# Shows the type value of the elements in the list

def getListType(mainList = []):
    k = 0
    for i in mainList: 
        a = i
        i = str(type(i))
        i = i.replace("<","")
        i = i.replace(">","")
        i = i.replace("class","")
        i = i.replace("'","")
        print(i + f" | {k}. Eleman" + f" {a}")
        k = k + 1



# Converts the elements in the list to str

def convertStrLİst(mainList = []):
    newList = []
    for i in mainList:
        i = str(i)
        newList.append(i)
    return newList 



# It only returns int values ​​in the list

def getOnlyInt(mainList = []):
    newList = []
    for i in mainList:
        if(str(type(i)) == "<class 'int'>"):
            newList.append(i)
        else:
            pass
    return newList




# It only returns str values ​​in the list

def getOnlyStr(mainList = []):
    newList = []
    for i in mainList:
        if(str(type(i)) == "<class 'str'>"):
            newList.append(i)
        else:
            pass
    return newList



# It only returns float values ​​in the list

def getOnlyFloat(mainList = []):
    newList = []
    for i in mainList:
        if(str(type(i)) == "<class 'float'>"):
            newList.append(i)
        else:
            pass
    return newList


