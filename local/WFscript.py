import pandas as pd
import csv



pd.set_option("display.max_rows", None, "display.max_columns", None)
data = pd.read_csv("beforeweek.csv")
# print(data)


prev = {}

def grab_numbers(dfrow,dic):
    dic[dfrow["Unnamed: 0"]] = dfrow


for x in data.index:
    if "Total" in data.iloc[x][0]:
#         print(data.iloc[x])
        grab_numbers(data.iloc[x],prev)
del prev["Hardlines Total"]
# print(prev)


afterdata = pd.read_csv("afterweek.csv")
after = {}
for x in afterdata.index:
    if "Total" in afterdata.iloc[x][0]:
        grab_numbers(afterdata.iloc[x],after)
del after["Hardlines Total"]
# print(after)


def get_sign(number):
    if number>= 0:
        return "+"
    else:
        return "-"
def get_percent_sign(percent):
    if type(percent) in [int,float]:
        percent = str(percent)
    if len(percent) > 1 and percent[0] == "-":
        return percent
    else:
        return "+"+percent
import sys
from subprocess import STDOUT
file = open("out.txt", "w+")
# file = ""
sys.stdout = file
for dep in prev.keys():
    previous = prev[dep]
    thisweek = after[dep]
    print(dep)
    newsalesnum = int(thisweek['Sales $'].split("$")[1].replace(",",""))/1000000
    lastsalesnum = int(previous['Sales $'].split("$")[1].replace(",",""))/1000000
    diff = newsalesnum-lastsalesnum
    sign = get_sign(diff)
    print("\t•${}mm in Sales $, {}${}mm".format(round(newsalesnum,1),sign,round(abs(diff),2)))

#     print(thisweek["Comp %.1"][:-1])
#     print(previous["Comp %.1"][:-1])
    compbps = round((float(thisweek["Comp %.1"][:-1]) - float(previous["Comp %.1"][:-1]))*100)
    sign = get_sign(compbps)
    print("\t\t•Comp of {}, {}{}bps".format(get_percent_sign (thisweek["Comp %.1"]), sign, abs(compbps)))

    twoyrcompbps = round((float(thisweek["Comp % (2YR)"][:-1]) - float(previous["Comp % (2YR)"][:-1]))*100)
    sign = get_sign(twoyrcompbps)
    print("\t"*2 + "•2yr comp of {}, {}{}bps".format(get_percent_sign(thisweek["Comp % (2YR)"]), sign, abs(twoyrcompbps)))


    fourweektwoyrcompbps = round((float(thisweek["Comp % (r4W 2YR)"][:-1]) - float(previous["Comp % (r4W 2YR)"][:-1]))*100)
    sign = get_sign(fourweektwoyrcompbps)
    print("\t"*2 + "•4week, 2yr comp of {}, {}{}bps".format(get_percent_sign(thisweek["Comp % (r4W 2YR)"]), sign, abs(fourweektwoyrcompbps)))


    newunits = int(thisweek['Sales Units'].replace(",",""))/1000000
    lastunits = int(previous['Sales Units'].replace(",",""))/1000000
    diff = newunits - lastunits
    sign = get_sign(diff)
    print("\t•{}mm in Units, {}mm".format(round(newunits,1), get_percent_sign(round(diff,2))))

    compbps = round((float(thisweek["Comp %.2"][:-1]) - float(previous["Comp %.2"][:-1]))*100)
    sign = get_sign(compbps)
    print("\t\t•Comp of {}, {}{}bps".format(get_percent_sign (thisweek["Comp %.2"]), sign, abs(compbps)))

    twoyrcompbps = round((float(thisweek["Comp % (2YR).1"][:-1]) - float(previous["Comp % (2YR).1"][:-1]))*100)
    sign = get_sign(twoyrcompbps)
    print("\t"*2 + "•2yr comp of {}, {}{}bps".format(get_percent_sign(thisweek["Comp % (2YR).1"]), sign, abs(twoyrcompbps)))


    fourweektwoyrcompbps = round((float(thisweek["Comp % (r4W 2YR).1"][:-1]) - float(previous["Comp % (r4W 2YR).1"][:-1]))*100)
    sign = get_sign(fourweektwoyrcompbps)
    print("\t"*2 + "•4week, 2yr comp of {}, {}{}bps".format(get_percent_sign(thisweek["Comp % (r4W 2YR).1"]), sign, abs(fourweektwoyrcompbps)))


    print("\t•In Stock of {}, {}bps".format(thisweek["In Stock %"], get_percent_sign(str(thisweek["In Stock BPS v LW"]))))


    LYbps = round((float(thisweek["In Stock % v LY"][:-1]) - float(previous["In Stock % v LY"][:-1]))*100)
    sign = get_sign(LYbps)
    print("\t"*2 + "•vLY of {}, {}{}bps".format(get_percent_sign(thisweek["In Stock % v LY"]),sign, abs(LYbps)))


print("\n\n")
print("Your weekly forecast should be above")
print("\t- Thanks, Suraaj Samanta from Summer 2021")
file.close()
sys.stdout = sys.__stdout__
print(file)


