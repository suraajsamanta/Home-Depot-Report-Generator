__author__ = 'suraaj'
from flask import Flask, make_response, request
import io
import csv
import pandas as pd


app = Flask(__name__)

def transform(text_file_contents):
    return text_file_contents.replace("=", ",")


@app.route('/')
def form():
    return """
        <html>
        <center>
            <body>
            <center>
                <h1 style="font-size:100px; color:orange"  >Home Depot Weekly Report Generator</h1>
                <p style="font-size:50px"> Remember: The input must be in csv format.</p>
                <p style="font-size:20px"> 1) Open Weekly MyDrill spreadsheet for Last Week and "Enable Editing" <br>
2) Command/Control + A (to select all) <br>3) Cmd/Ctrl + Shift + 9 (to expand everything) <br>4) Click File and then save as a CSV (*.csv) <br>5) Click OK when it says that only the active sheet will be saved <br>6) Repeat 1-5 for This Week </p>
                <form action="/transform" method="post" enctype="multipart/form-data">
                    <p> Enter Last Week's csv data:
                   <input type="file" name="data_file" />
                     Enter This Week's csv data:
                    <input type="file" name="data_file1" /></p>
                    <input type="submit" style="width: 300px;margin-left: 40%; margin-right: 60%" />

                </form>
                </center>
            </body>
            </center>
        </html>
    """

@app.route('/transform', methods=["POST"])
def transform_view():
    f = request.files['data_file']
    g = request.files['data_file1']
    if not f or not g:
        return "File inputs are empty!"
    data = pd.read_csv(f)
    afterdata = pd.read_csv(g)
#start of forecast building
    prev = {}

    def grab_numbers(dfrow,dic):
        dic[dfrow["Unnamed: 0"]] = dfrow


    for x in data.index:
        if "Total" in data.iloc[x][0]:
            grab_numbers(data.iloc[x],prev)
    del prev["Hardlines Total"]




    after = {}
    for x in afterdata.index:
        if "Total" in afterdata.iloc[x][0]:
            grab_numbers(afterdata.iloc[x],after)
    del after["Hardlines Total"]



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


    file = ""

    for dep in prev.keys():
        previous = prev[dep]
        thisweek = after[dep]
        file += "\n"+ dep
        newsalesnum = int(thisweek['Sales $'].split("$")[1].replace(",",""))/1000000
        lastsalesnum = int(previous['Sales $'].split("$")[1].replace(",",""))/1000000
        diff = newsalesnum-lastsalesnum
        sign = get_sign(diff)
        file += ("\n\t•${}mm in Sales $, {}${}mm".format(round(newsalesnum,1),sign,round(abs(diff),2)))


        compbps = round((float(thisweek["Comp %.1"][:-1]) - float(previous["Comp %.1"][:-1]))*100)
        sign = get_sign(compbps)
        file += ("\n\t\t•Comp of {}, {}{}bps".format(get_percent_sign (thisweek["Comp %.1"]), sign, abs(compbps)))

        twoyrcompbps = round((float(thisweek["Comp % (2YR)"][:-1]) - float(previous["Comp % (2YR)"][:-1]))*100)
        sign = get_sign(twoyrcompbps)
        file += ("\n"+"\t"*2 + "•2yr comp of {}, {}{}bps".format(get_percent_sign(thisweek["Comp % (2YR)"]), sign, abs(twoyrcompbps)))


        fourweektwoyrcompbps = round((float(thisweek["Comp % (r4W 2YR)"][:-1]) - float(previous["Comp % (r4W 2YR)"][:-1]))*100)
        sign = get_sign(fourweektwoyrcompbps)
        file += ("\n"+"\t"*2 + "•4week, 2yr comp of {}, {}{}bps".format(get_percent_sign(thisweek["Comp % (r4W 2YR)"]), sign, abs(fourweektwoyrcompbps)))


        newunits = int(thisweek['Sales Units'].replace(",",""))/1000000
        lastunits = int(previous['Sales Units'].replace(",",""))/1000000
        diff = newunits - lastunits
        sign = get_sign(diff)
        file += ("\n"+"\t•{}mm in Units, {}mm".format(round(newunits,1), get_percent_sign(round(diff,2))))

        compbps = round((float(thisweek["Comp %.2"][:-1]) - float(previous["Comp %.2"][:-1]))*100)
        sign = get_sign(compbps)
        file += ("\n"+"\t\t•Comp of {}, {}{}bps".format(get_percent_sign (thisweek["Comp %.2"]), sign, abs(compbps)))

        twoyrcompbps = round((float(thisweek["Comp % (2YR).1"][:-1]) - float(previous["Comp % (2YR).1"][:-1]))*100)
        sign = get_sign(twoyrcompbps)
        file += ("\n"+"\t"*2 + "•2yr comp of {}, {}{}bps".format(get_percent_sign(thisweek["Comp % (2YR).1"]), sign, abs(twoyrcompbps)))


        fourweektwoyrcompbps = round((float(thisweek["Comp % (r4W 2YR).1"][:-1]) - float(previous["Comp % (r4W 2YR).1"][:-1]))*100)
        sign = get_sign(fourweektwoyrcompbps)
        file += ("\n"+"\t"*2 + "•4week, 2yr comp of {}, {}{}bps".format(get_percent_sign(thisweek["Comp % (r4W 2YR).1"]), sign, abs(fourweektwoyrcompbps)))


        file += ("\n"+"\t•In Stock of {}, {}bps".format(thisweek["In Stock %"], get_percent_sign(str(thisweek["In Stock BPS v LW"]))))


        LYbps = round((float(thisweek["In Stock % v LY"][:-1]) - float(previous["In Stock % v LY"][:-1]))*100)
        sign = get_sign(LYbps)
        file += ("\n"+"\t"*2 + "•vLY of {}, {}{}bps".format(get_percent_sign(thisweek["In Stock % v LY"]),sign, abs(LYbps)))


    file += ("\n"+"\n\n")
    file += ("\n"+"Your weekly forecast should be above")
    file += ("\n"+"\t- Thanks, Suraaj Samanta from Summer 2021")


# end of forecast building
    # stream = io.StringIO(f.stream.read().decode("UTF8"), newline=None)
    # # print(stream)
    # csv_input = csv.reader(stream)
    # #print("file contents: ", file_contents)
    # #print(type(file_contents))
    # # print(csv_input)
    # # for row in csv_input:
    # #     print(row)
    # print("okay chill out")
    # stream.seek(0)
    # result = transform(stream.read())
    result = "hello"
    response = make_response(file)
    response.headers["Content-Disposition"] = "attachment; filename=report.txt"
    return response

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001, debug=True)
