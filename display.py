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

        # Display graphs
        self.showGraphs()


    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)        
        
        windowLayout = QGridLayout()


        self.categorySelectorGroupBox = QGroupBox("Category")
        self.statsGroupBox = QGroupBox("Stats")
        self.plotLine1GroupBox1 = QGroupBox("Podium per country")
        self.plotLine1GroupBox2 = QGroupBox("Line1 Block 2")
        self.plotLine1GroupBox3 = QGroupBox("Line1 Block 3")

        self.plotLine2GroupBox1 = QGroupBox("Line2 Block 1")
        self.plotLine2GroupBox2 = QGroupBox("Line2 Block 2")
        self.plotLine2GroupBox3 = QGroupBox("Line2 Block 3")

        self.bottomGroupBox = QGroupBox("Last Race")


        windowLayout.addWidget(self.plotLine1GroupBox1,0,2,2,3)
        windowLayout.addWidget(self.plotLine1GroupBox2,0,5,2,3)
        windowLayout.addWidget(self.plotLine1GroupBox3,0,8,2,3)

        windowLayout.addWidget(self.plotLine2GroupBox1,2,2,2,3)
        windowLayout.addWidget(self.plotLine2GroupBox2,2,5,2,3)
        windowLayout.addWidget(self.plotLine2GroupBox3,2,8,2,3)

        windowLayout.addWidget(self.categorySelectorGroupBox,0,0,4,2)
        windowLayout.addWidget(self.bottomGroupBox,5,0,2,11)

        self.setLayout(windowLayout)
        self.show()

    def fillCategories(self):
        availablesCategories = list(self.config["resultsStruct"].keys())
        print(availablesCategories)
        availablesCategories.insert(0,"All")


        # Set default category "All"
        self.category = "Slalom"
        self.categoryList = QListWidget()

        for category in availablesCategories:
            self.categoryList.addItem(str(category))

        self.categoryList.itemClicked.connect(self.categorySelectedEvent)

        self.categorySelector = QVBoxLayout()
        self.categorySelector.addWidget(self.categoryList)
        self.categorySelectorGroupBox.setLayout(self.categorySelector)


    def categorySelectedEvent(self):
        newCategory = self.categoryList.currentItem().text()
        print(f"Update selected category from {self.category} to {newCategory}")
        self.category = newCategory
        self.resetGraphs()


    def showGraphs(self):
        self.createCountryPodium()


    def resetGraphs(self):
        # Reset podium per country
        while (self.tableWidget.rowCount() > 0):
            self.tableWidget.removeRow(0)
        self.fillCountryPodium()


    def createCountryPodium(self):
        self.tableWidget = QTableWidget()
        self.tableWidget.setHorizontalHeaderLabels(["Country"," 1st Places ", " 2nd Places ", " 3rd Places "])
        self.fillCountryPodium()

        self.tableWidget.resizeColumnToContents(1)
        self.tableWidget.resizeColumnToContents(2)
        self.tableWidget.resizeColumnToContents(3)

        self.countryPodium = QVBoxLayout()
        self.countryPodium.addWidget(self.tableWidget)

        self.plotLine1GroupBox1.setLayout(self.countryPodium)

    def fillCountryPodium(self):
        data = dataVisualisation.countryPodiumTable(self.results,self.category)
        self.tableWidget.setRowCount(len(data))
        self.tableWidget.setColumnCount(4)

        for i,country in enumerate(data):
            self.tableWidget.setItem(i,0, QTableWidgetItem(country.name))
            self.tableWidget.setItem(i,1, QTableWidgetItem(str(country.first)))
            self.tableWidget.setItem(i,2, QTableWidgetItem(str(country.second)))
            self.tableWidget.setItem(i,3, QTableWidgetItem(str(country.third)))


        

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())