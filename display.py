import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QHBoxLayout, QGroupBox, QDialog, QVBoxLayout, QGridLayout,QListWidget,QTableWidget,QTableWidgetItem,QAbstractScrollArea
from PyQt5.QtCore import pyqtSlot
import json
import dataVisualisation

class App(QDialog):

    def __init__(self):
        super().__init__()
        self.title = 'FIS results GUI'
        self.left = 100
        self.top = 100
        self.width = 1600
        self.height = 800
        self.initUI()


        with open("config.json","r") as config:
            self.config = json.load(config)
        with open("results.json","r") as results:
            self.results = json.load(results)


        self.fillCategories()
        self.fillEvents()
        # Display graphs
        self.showGraphs()


    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)        
        
        windowLayout = QGridLayout()


        self.categorySelectorGroupBox = QGroupBox("Category")
        self.eventSelectorGroupBox = QGroupBox("Event")

        self.statsGroupBox = QGroupBox("Stats")
        self.plotLine1GroupBox1 = QGroupBox("Podium per country")
        self.plotLine1GroupBox2 = QGroupBox("Line1 Block 2")
        self.plotLine1GroupBox3 = QGroupBox("Line1 Block 3")

        self.plotLine2GroupBox1 = QGroupBox("Race result")
        self.plotLine2GroupBox2 = QGroupBox("Line2 Block 2")
        self.plotLine2GroupBox3 = QGroupBox("Line2 Block 3")

        self.bottomGroupBox = QGroupBox("Last Race")


        windowLayout.addWidget(self.plotLine1GroupBox1,0,2,2,3)
        windowLayout.addWidget(self.plotLine1GroupBox2,0,5,2,3)
        windowLayout.addWidget(self.plotLine1GroupBox3,0,8,2,3)

        windowLayout.addWidget(self.plotLine2GroupBox1,2,2,2,4)
        windowLayout.addWidget(self.plotLine2GroupBox2,2,6,2,2)
        windowLayout.addWidget(self.plotLine2GroupBox3,2,8,2,3)

        windowLayout.addWidget(self.categorySelectorGroupBox,0,0,2,2)
        windowLayout.addWidget(self.eventSelectorGroupBox,2,0,2,2)

        windowLayout.addWidget(self.bottomGroupBox,5,0,2,11)

        self.setLayout(windowLayout)
        self.show()

    def fillCategories(self):
        availablesCategories = list(self.config["resultsStruct"].keys())
        availablesCategories.insert(0,"All")
        # Set default category "All"
        self.category = "All"
        self.categoryList = QListWidget()

        for category in availablesCategories:
            self.categoryList.addItem(str(category))

        self.categoryList.itemClicked.connect(self.categorySelectedCallback)
        self.categorySelector = QVBoxLayout()
        self.categorySelector.addWidget(self.categoryList)
        self.categorySelectorGroupBox.setLayout(self.categorySelector)


    def categorySelectedCallback(self):
        newCategory = self.categoryList.currentItem().text()
        print(f"Update selected category from {self.category} to {newCategory}")
        self.category = newCategory
        self.resetGraphsCategory()


    def fillEvents(self):
        self.availablesEvents = dataVisualisation.getEventsList(self.results)

        self.event = self.availablesEvents[0]
        self.eventList = QListWidget()

        for event in self.availablesEvents:
            # print(event)
            date = "{:02d}".format(event["date"]["day"])+"/"+str(event["date"]["month"])+"/"+str(event["date"]["year"])
            self.eventList.addItem(date+' | '+str(event["place"])+" - "+event["type"])

        self.eventList.itemClicked.connect(self.eventSelectedCallback)
        self.eventSelector = QVBoxLayout()
        self.eventSelector.addWidget(self.eventList)
        self.eventSelectorGroupBox.setLayout(self.eventSelector)


    def eventSelectedCallback(self):
        newEventIndex = self.eventList.currentRow()
        # print(f"Update selected event from {self.event} to {self.availablesEvents[newEventIndex]}")
        self.event = self.availablesEvents[newEventIndex]
        self.resetGraphsEvents()



    def showGraphs(self):
        self.createCountryPodium()
        self.createEventResults()

    def resetGraphsCategory(self):
        # Reset podium per country
        while (self.podiumTable.rowCount() > 0):
            self.podiumTable.removeRow(0)
        self.fillCountryPodium()


    def resetGraphsEvents(self):
        while (self.eventTable.rowCount() > 0):
            self.eventTable.removeRow(0)
        self.fillEventResults()


    def createCountryPodium(self):
        self.podiumTable = QTableWidget()
        self.podiumTable.setHorizontalHeaderLabels(["Country"," 1st Places ", " 2nd Places ", " 3rd Places "])
        self.fillCountryPodium()

        self.podiumTable.resizeColumnToContents(1)
        self.podiumTable.resizeColumnToContents(2)
        self.podiumTable.resizeColumnToContents(3)

        self.countryPodium = QVBoxLayout()
        self.countryPodium.addWidget(self.podiumTable)

        self.plotLine1GroupBox1.setLayout(self.countryPodium)

    def fillCountryPodium(self):
        data = dataVisualisation.countryPodiumTable(self.results,self.category)
        self.podiumTable.setRowCount(len(data))
        self.podiumTable.setColumnCount(4)

        for i,country in enumerate(data):
            self.podiumTable.setItem(i,0, QTableWidgetItem(country.name))
            self.podiumTable.setItem(i,1, QTableWidgetItem(str(country.first)))
            self.podiumTable.setItem(i,2, QTableWidgetItem(str(country.second)))
            self.podiumTable.setItem(i,3, QTableWidgetItem(str(country.third)))



    def createEventResults(self):
        self.eventTable = QTableWidget()
        self.fillEventResults()

        self.eventPodium = QVBoxLayout()
        self.eventPodium.addWidget(self.eventTable)

        self.plotLine2GroupBox1.setLayout(self.eventPodium)

    def fillEventResults(self):

        if self.event['type'] == "Slalom" or self.event['type'] == "Giant Slalom":
            self.eventTable.setHorizontalHeaderLabels([" Athlete ", " Country ", " Run 1 ", " Run 2 ", " Diff (ms) ", " Total "])
            self.eventTable.setColumnCount(6)
            data = dataVisualisation.eventResultTable(self.event)
            self.eventTable.setRowCount(len(data))
          
            for i,athlete in enumerate(data):
                self.eventTable.setItem(i,0, QTableWidgetItem(str(athlete["name"])[0:22]))
                self.eventTable.setItem(i,1, QTableWidgetItem(str(athlete["country"])))
                self.eventTable.setItem(i,2, QTableWidgetItem(str(athlete["run1"])))
                self.eventTable.setItem(i,3, QTableWidgetItem(str(athlete["run2"])))
                self.eventTable.setItem(i,4, QTableWidgetItem(str(athlete["diff"])))
                self.eventTable.setItem(i,5, QTableWidgetItem(str(athlete["total"])))

                self.eventTable.resizeColumnsToContents()


        elif self.event['type'] == "Super G" or self.event['type'] == "Downhill":
            self.eventTable.setHorizontalHeaderLabels([" Athlete ", " Country ", " Time "])
            self.eventTable.setColumnCount(3)
            
            data = dataVisualisation.eventResultTable(self.event)
            self.eventTable.setRowCount(len(data))
          
            for i,athlete in enumerate(data):
                self.eventTable.setItem(i,0, QTableWidgetItem(str(athlete["name"])[0:22]))
                self.eventTable.setItem(i,1, QTableWidgetItem(str(athlete["country"])))
                self.eventTable.setItem(i,2, QTableWidgetItem(str(athlete["time"])))

                self.eventTable.resizeColumnsToContents()

        elif self.event['type'] == "Parallel":
            self.eventTable.setHorizontalHeaderLabels([" Athlete ", " Country "])
            self.eventTable.setColumnCount(2)

            data = dataVisualisation.eventResultTable(self.event)
            self.eventTable.setRowCount(len(data))
          
            for i,athlete in enumerate(data):
                self.eventTable.setItem(i,0, QTableWidgetItem(str(athlete["name"])[0:22]))
                self.eventTable.setItem(i,1, QTableWidgetItem(str(athlete["country"])))
                
                self.eventTable.resizeColumnsToContents()








        

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())