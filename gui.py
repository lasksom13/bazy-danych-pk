from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (QApplication, QDialog, QGridLayout, 
        QLabel, QLineEdit, QPushButton, QRadioButton,
        QStyleFactory, QTabWidget, QVBoxLayout, QWidget, 
        QButtonGroup)

import random
import time

from web_scrapping import WebScrapper
from mongodb_base import MongoDB
from postgres_base import Postgres



def testFunction(value):
    print("WORKS!" + str(value))
    return value

def randomNumber():
    return random.randint(1, 10000)

class DatabaseApp(QDialog):
    def __init__(self, parent=None):
        super(DatabaseApp, self).__init__(parent)

        self.numberOfRecords = 0
        self.postgres = Postgres()
        self.mongodb = MongoDB()
        ### CASSANDRA_TODO ###
        self.cassandra = "123"

        self.setWindowTitle("Database Performance")
        self.resize(800, 400)

        self.originalPalette = QApplication.palette()

        self.createMainTabWidget()

        self.label_numberOfRecords = QLabel()
        self.updateNumberOfRecords(0)

        mainLayout = QGridLayout()
        mainLayout.addWidget(self.mainTabWidget)
        mainLayout.addWidget(self.label_numberOfRecords)

        self.setLayout(mainLayout)

        self.changeStyle('windowsvista')

    def updateNumberOfRecords(self, _number):
        self.numberOfRecords += _number
        self.label_numberOfRecords.setText(f"Current number of records : {self.numberOfRecords}")

    def createDatabase(self, _numberOfRecords):
        self.mainTabWidget.setDisabled(True)
        
        # create db function
        # self.postgres.start_database()
        # self.mongodb.start_database()
        ### CASSANDRA_TODO ###

        time.sleep(5)

        # create table
        self.postgres.create_table()
        self.mongodb.create_table()
        ### CASSANDRA_TODO ###

        
        print(self.postgres.list_tables())
        print(self.mongodb.list_tables())

        # update number of records
        self.updateNumberOfRecords(0)

        self.mainTabWidget.setDisabled(False)
        
        self.tab1Label_status.setText("Created!")

    def deleteDatabase(self):
        self.mainTabWidget.setDisabled(True)

        # delete db function
        self.postgres.drop_table()
        self.mongodb.drop_table()

        # update number of records
        self.updateNumberOfRecords(-self.numberOfRecords)
        self.tab1Label_status.setText("Deleted!")

        self.mainTabWidget.setDisabled(False)

    def simpleTest(self):
        self.mainTabWidget.setDisabled(True)

        if self.tab2radioButton_Insert.isChecked():
            postgres_output = self.postgres.test_time_for_insert(int(self.tab2LineEdit_NumberOfRecordsToTest.text()))
            mongodb_output = self.mongodb.test_time_for_insert(int(self.tab2LineEdit_NumberOfRecordsToTest.text()))
            cassandra_output = "TODO"
            self.tab2Label_TestOutput.setText(f"[PostgreSQL] It took {postgres_output} seconds to insert {self.tab2LineEdit_NumberOfRecordsToTest.text()} records.\n" +
            f"[MongoDB] It took {mongodb_output} seconds to insert {self.tab2LineEdit_NumberOfRecordsToTest.text()} records.\n"
            f"[MongoDB] It took {cassandra_output} seconds to insert {self.tab2LineEdit_NumberOfRecordsToTest.text()} records.\n")
            self.updateNumberOfRecords(int(self.tab2LineEdit_NumberOfRecordsToTest.text()))

        elif self.tab2radioButton_Modify.isChecked():
            postgres_output = self.postgres.test_time_for_modify(int(self.tab2LineEdit_NumberOfRecordsToTest.text()))
            mongodb_output = self.mongodb.test_time_for_modify(int(self.tab2LineEdit_NumberOfRecordsToTest.text()))
            cassandra_output = "TODO"
            self.tab2Label_TestOutput.setText(f"[PostgreSQL] It took {postgres_output} seconds to modify {self.tab2LineEdit_NumberOfRecordsToTest.text()} records.\n" +
            f"[MongoDB] It took {mongodb_output} seconds to modify {self.tab2LineEdit_NumberOfRecordsToTest.text()} records.\n" +
            f"[MongoDB] It took {cassandra_output} seconds to modify {self.tab2LineEdit_NumberOfRecordsToTest.text()} records.\n")
        
        elif self.tab2radioButton_Delete.isChecked():
            postgres_output = self.postgres.test_time_for_delete(int(self.tab2LineEdit_NumberOfRecordsToTest.text()))
            mongodb_output = self.mongodb.test_time_for_delete(int(self.tab2LineEdit_NumberOfRecordsToTest.text()))
            cassandra_output = "TODO"
            self.tab2Label_TestOutput.setText(f"[PostgreSQL] It took {postgres_output} seconds to delete {self.tab2LineEdit_NumberOfRecordsToTest.text()} records.\n" +
            f"[MongoDB] It took {mongodb_output} seconds to delete {self.tab2LineEdit_NumberOfRecordsToTest.text()} records.\n" +
            f"[Cassandra] It took {cassandra_output} seconds to delete {self.tab2LineEdit_NumberOfRecordsToTest.text()} records.")
            self.updateNumberOfRecords(-int(self.tab2LineEdit_NumberOfRecordsToTest.text()))
        
        
        self.tab2LineEdit_NumberOfRecordsToTest.setText("")
        
        self.mainTabWidget.setDisabled(False)
        
        

    def statisticsTest(self):
        self.mainTabWidget.setDisabled(True)

        column = self.tab3buttonGroup_columnNames.checkedButton().text().split()[0]
        statistic = self.tab3buttonGroup_testTypes.checkedButton().text()

        if statistic == "MAXIMUM VALUE":
            postgres_output = self.postgres.test_time_for_max(column)
            mongodb_output = self.mongodb.test_time_for_max(column)
            cassandra_output = ["TODO"]#self.cassandra.test_time_for_max(column)
        elif statistic == "MINIMUM VALUE":
            postgres_output = self.postgres.test_time_for_min(column)
            mongodb_output = self.mongodb.test_time_for_min(column)
            cassandra_output = ["TODO"]#self.cassandra.test_time_for_min(column)
        elif statistic == "MEDIAN":
            postgres_output = self.postgres.test_time_for_median(column)
            mongodb_output = self.mongodb.test_time_for_median(column)
            cassandra_output = ["TODO"]#self.cassandra.test_time_for_median(column)
        elif statistic == "COUNT ROWS":
            postgres_output = self.postgres.get_record_amount()
            mongodb_output = self.mongodb.get_record_amount()
            cassandra_output = ["TODO"]#self.cassandra.get_record_amount(column)
        elif statistic == "DATA DISTRIBUTION":
            postgres_output = self.postgres.test_time_for_data_distribution(column)
            mongodb_output = self.mongodb.test_time_for_data_distribution(column)
            cassandra_output = ["TODO"]# self.cassandra.test_time_for_data_distribution(column)
        
        self.tab3Label_TestOutput.setText(f"[PostgreSQL] It took {postgres_output[0]} seconds to perform {self.tab3buttonGroup_testTypes.checkedButton().text()} on {self.tab3buttonGroup_columnNames.checkedButton().text()} column.\n" + 
            f"[MongoDB] It took {mongodb_output[0]} seconds to perform {self.tab3buttonGroup_testTypes.checkedButton().text()} on {self.tab3buttonGroup_columnNames.checkedButton().text()} column.\n"
            f"[Cassandra] It took {cassandra_output[0]} seconds to perform {self.tab3buttonGroup_testTypes.checkedButton().text()} on {self.tab3buttonGroup_columnNames.checkedButton().text()} column.\n")

        self.mainTabWidget.setDisabled(False)

    def webScrapping(self):
        self.mainTabWidget.setDisabled(True)

        web_scrapper = WebScrapper(self.tab5LineEdit_linkToIMDB.text())
        self.tab5Label_webScrapperOutput.setText(f"Added to databases: {web_scrapper.__dict__()}")

        self.updateNumberOfRecords(1)
        self.tab5LineEdit_linkToIMDB.setText("")

        self.mainTabWidget.setDisabled(False)

    def customQuery(self, _database, _query):
        self.mainTabWidget.setDisabled(True)

        if _database == "postgres":
            test_output = self.postgres.test_time_for_user_query()
            self.tab4Label_testOutput.setText(f"[PostgreSQL] It took {test_output[0]} seconds to perform custom query.")
        elif _database == "mongodb":
            test_output = self.mongodb.test_time_for_user_query()
            self.tab4Label_testOutput.setText(f"[PostgreSQL] It took {test_output[0]} seconds to perform custom query.")
        elif _database == "cassandra":
            test_output = ["TODO"] # self.cassandra.test_time_for_user_query()
            self.tab4Label_testOutput.setText(f"[PostgreSQL] It took {test_output[0]} seconds to perform custom query.")

        self.mainTabWidget.setDisabled(False)



    def createMainTabWidget(self):
        self.mainTabWidget = QTabWidget()

        self.createTab1()
        self.createTab2()
        self.createTab3()
        self.createTab4()
        self.createTab5()

        self.mainTabWidget.addTab(self.tab1, "DB Creation")
        self.mainTabWidget.addTab(self.tab2, "Basic Tests")
        self.mainTabWidget.addTab(self.tab3, "Statistics")
        self.mainTabWidget.addTab(self.tab4, "Custom Query")
        self.mainTabWidget.addTab(self.tab5, "Web Scrapping")


    def createTab1(self):
        self.tab1 = QWidget()
        self.tab1Layout = QVBoxLayout()
        
        self.tab1Label_status = QLabel()

        self.tab1Button_IniciateDb = QPushButton("Create Table")
        self.tab1Button_IniciateDb.clicked.connect(self.createDatabase)

        self.tab1Button_DeleteDb = QPushButton("Delete Table")
        self.tab1Button_DeleteDb.clicked.connect(self.deleteDatabase) # delete db

        self.tab1Layout.addWidget(self.tab1Button_IniciateDb)
        self.tab1Layout.addWidget(self.tab1Button_DeleteDb)
        self.tab1Layout.addWidget(self.tab1Label_status)
        self.tab1Layout.addStretch(1)

        self.tab1.setLayout(self.tab1Layout)

    def createTab2(self):
        self.tab2 = QWidget()
        self.tab2Layout = QVBoxLayout()

        self.tab2Label_TypeOfOperation = QLabel("What operation would you like to test?")
        self.tab2radioButton_Insert = QRadioButton("INSERT")
        self.tab2radioButton_Modify = QRadioButton("MODIFY")
        self.tab2radioButton_Delete = QRadioButton("DELETE")
        self.tab2radioButton_Insert.setChecked(True)

        self.tab2LineEdit_NumberOfRecordsToTest = QLineEdit()
        self.tab2LineEdit_NumberOfRecordsToTest.setPlaceholderText("Number of records to perform action on")

        self.tab2Button_RunTest = QPushButton("Start Test")
        self.tab2Button_RunTest.clicked.connect(self.simpleTest)

        self.tab2Label_TestOutput = QLabel()
        

        self.tab2Layout.addWidget(self.tab2Label_TypeOfOperation)
        self.tab2Layout.addWidget(self.tab2radioButton_Insert)
        self.tab2Layout.addWidget(self.tab2radioButton_Modify)
        self.tab2Layout.addWidget(self.tab2radioButton_Delete)
        self.tab2Layout.addWidget(self.tab2LineEdit_NumberOfRecordsToTest)
        self.tab2Layout.addWidget(self.tab2Button_RunTest)
        self.tab2Layout.addWidget(self.tab2Label_TestOutput)
        self.tab2Layout.addStretch(1)

        self.tab2.setLayout(self.tab2Layout)

    
    def createTab3(self):
        self.tab3 = QWidget()
        self.tab3Layout = QGridLayout()

        self.tab3Label_TestOutput = QLabel()

        self.tab3Layout_columnNames = QVBoxLayout()
        self.tab3Label_columnToTest = QLabel("What column would you like to test?")
        self.tab3radioButton_tconst = QRadioButton("tconst [String]")
        self.tab3radioButton_titleType = QRadioButton("titleType [String]")
        self.tab3radioButton_primaryTitle = QRadioButton("primaryTitle [String]")
        self.tab3radioButton_originalTitle = QRadioButton("originalTitle [String]")
        self.tab3radioButton_isAdult = QRadioButton("isAdult [Boolean]")
        self.tab3radioButton_startYear = QRadioButton("startYear [Datetime]")
        self.tab3radioButton_endYear = QRadioButton("endYear [Datetime]")
        self.tab3radioButton_runtimeMinutes = QRadioButton("runtimeMinutes [Integer]")
        self.tab3radioButton_genres = QRadioButton("genres [String Array]")
        self.tab3radioButton_runtimeMinutes.setChecked(True)

        self.tab3buttonGroup_columnNames = QButtonGroup()
        self.tab3buttonGroup_columnNames.addButton(self.tab3radioButton_tconst)
        self.tab3buttonGroup_columnNames.addButton(self.tab3radioButton_titleType)
        self.tab3buttonGroup_columnNames.addButton(self.tab3radioButton_primaryTitle)
        self.tab3buttonGroup_columnNames.addButton(self.tab3radioButton_originalTitle)
        self.tab3buttonGroup_columnNames.addButton(self.tab3radioButton_isAdult)
        self.tab3buttonGroup_columnNames.addButton(self.tab3radioButton_startYear)
        self.tab3buttonGroup_columnNames.addButton(self.tab3radioButton_endYear)
        self.tab3buttonGroup_columnNames.addButton(self.tab3radioButton_runtimeMinutes)
        self.tab3buttonGroup_columnNames.addButton(self.tab3radioButton_genres)
        
    
        self.tab3Layout_testTypes = QVBoxLayout()
        self.tab3Label_testTypes = QLabel("What test would you like to perform?")
        self.tab3radioButton_max = QRadioButton("MAXIMUM VALUE")
        self.tab3radioButton_min = QRadioButton("MINIMUM VALUE")
        self.tab3radioButton_median = QRadioButton("MEDIAN")
        self.tab3radioButton_countRows = QRadioButton("COUNT ROWS")
        self.tab3radioButton_dataDistribution = QRadioButton("DATA DISTRIBUTION")
        self.tab3radioButton_max.setChecked(True)

        self.tab3buttonGroup_testTypes = QButtonGroup()
        self.tab3buttonGroup_testTypes.addButton(self.tab3radioButton_max)
        self.tab3buttonGroup_testTypes.addButton(self.tab3radioButton_min)
        self.tab3buttonGroup_testTypes.addButton(self.tab3radioButton_median)
        self.tab3buttonGroup_testTypes.addButton(self.tab3radioButton_countRows)
        self.tab3buttonGroup_testTypes.addButton(self.tab3radioButton_dataDistribution)

        self.tab3Button_RunTest = QPushButton("Start Test")
        self.tab3Button_RunTest.clicked.connect(self.statisticsTest)

        self.tab3Layout_columnNames.addWidget(self.tab3Label_columnToTest)
        self.tab3Layout_columnNames.addWidget(self.tab3radioButton_tconst)
        self.tab3Layout_columnNames.addWidget(self.tab3radioButton_titleType)
        self.tab3Layout_columnNames.addWidget(self.tab3radioButton_primaryTitle)
        self.tab3Layout_columnNames.addWidget(self.tab3radioButton_originalTitle)
        self.tab3Layout_columnNames.addWidget(self.tab3radioButton_startYear)
        self.tab3Layout_columnNames.addWidget(self.tab3radioButton_endYear)
        self.tab3Layout_columnNames.addWidget(self.tab3radioButton_runtimeMinutes)
        self.tab3Layout_columnNames.addWidget(self.tab3radioButton_genres)
        self.tab3Layout_columnNames.addStretch(1)

        self.tab3Layout_testTypes.addWidget(self.tab3Label_testTypes)
        self.tab3Layout_testTypes.addWidget(self.tab3radioButton_max)
        self.tab3Layout_testTypes.addWidget(self.tab3radioButton_min)
        self.tab3Layout_testTypes.addWidget(self.tab3radioButton_median)
        self.tab3Layout_testTypes.addWidget(self.tab3radioButton_countRows)
        self.tab3Layout_testTypes.addWidget(self.tab3radioButton_dataDistribution)
        self.tab3Layout_testTypes.addStretch(1)

        
        self.tab3Layout.addLayout(self.tab3Layout_columnNames, 1, 1)
        self.tab3Layout.addLayout(self.tab3Layout_testTypes, 1, 2, alignment=Qt.AlignmentFlag.AlignCenter)
        self.tab3Layout.addWidget(self.tab3Button_RunTest, 2, 1, 1, 2)
        self.tab3Layout.addWidget(self.tab3Label_TestOutput, 3, 1, 1, 2)

        self.tab3.setLayout(self.tab3Layout)

    def createTab4(self):
        self.tab4 = QWidget()
        self.tab4Layout = QVBoxLayout()
        self.tab4ButtonLayout = QGridLayout()
        
        self.tab4Label_testOutput = QLabel()
        self.tab4LineEdit_customQuery = QLineEdit()
        self.tab4LineEdit_customQuery.setPlaceholderText("Custom Query")

        self.tab4Button_PostgreSQL = QPushButton("Test PostgreSQL")
        self.tab4Button_MongoDB = QPushButton("Test MongoDB")
        self.tab4Button_Cassandra = QPushButton("Test Cassandra")
        
        self.tab4Button_PostgreSQL.clicked.connect(lambda: self.customQuery("postgres", self.tab4LineEdit_customQuery.text()))
        self.tab4Button_MongoDB.clicked.connect(lambda: self.customQuery("mongodb", self.tab4LineEdit_customQuery.text()))
        self.tab4Button_Cassandra.clicked.connect(lambda: self.customQuery("cassandra", self.tab4LineEdit_customQuery.text()))

        self.tab4ButtonLayout.addWidget(self.tab4Button_PostgreSQL, 0, 0)
        self.tab4ButtonLayout.addWidget(self.tab4Button_MongoDB, 0, 1)
        self.tab4ButtonLayout.addWidget(self.tab4Button_Cassandra, 0, 2)

        self.tab4Layout.addWidget(self.tab4LineEdit_customQuery)
        self.tab4Layout.addLayout(self.tab4ButtonLayout)
        self.tab4Layout.addWidget(self.tab4Label_testOutput)
        self.tab4Layout.addStretch(1)

        self.tab4.setLayout(self.tab4Layout)

    def createTab5(self):
        self.tab5 = QWidget()
        self.tab5Layout = QVBoxLayout()

        self.tab5LineEdit_linkToIMDB = QLineEdit()
        self.tab5LineEdit_linkToIMDB.setPlaceholderText("Link to a movie/show on IMDB")

        self.tab5Button_addToDatabase = QPushButton("Add to Databases")
        self.tab5Button_addToDatabase.clicked.connect(self.webScrapping)

        self.tab5Label_webScrapperOutput = QLabel()
        self.tab5Label_webScrapperOutput.setWordWrap(True)

        self.tab5Layout.addWidget(self.tab5LineEdit_linkToIMDB)
        self.tab5Layout.addWidget(self.tab5Button_addToDatabase)
        self.tab5Layout.addWidget(self.tab5Label_webScrapperOutput)
        self.tab5Layout.addStretch(1)

        self.tab5.setLayout(self.tab5Layout)


    def changeStyle(self, styleName):
        QApplication.setStyle(QStyleFactory.create(styleName))
        self.changePalette()

    def changePalette(self):
        QApplication.setPalette(self.originalPalette)


if __name__ == '__main__':

    import sys

    app = QApplication(sys.argv)
    gallery = DatabaseApp()
    gallery.show()
    sys.exit(app.exec())