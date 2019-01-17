import csv
from guizero import App, Text, Combo
def you_chose(selected_value):
    with open('stationList.csv') as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        for rows in readCSV:
            if selected_value ==  rows[2]:
                print (selected_value) 
                setLat = rows[1]
                setLong = rows[0]
comboMenuStation=[]
with open('stationList.csv') as csvfile:
    readCSV= readCSV = csv.reader(csvfile, delimiter=',')
    for rows in readCSV:
        comboMenuStation.append(rows[2])
app = App()
instructions = Text(app, text="Choose a goblet")
combo = Combo(app, options=comboMenuStation, command=you_chose)
result = Text(app)
app.display()
