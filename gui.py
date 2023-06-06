from PyQt6.QtCore import QDateTime, Qt, QTimer
from PyQt6.QtWidgets import (QApplication, QCheckBox, QComboBox, QDateTimeEdit,
        QDial, QDialog, QGridLayout, QGroupBox, QHBoxLayout, QLabel, QLineEdit,
        QProgressBar, QPushButton, QRadioButton, QScrollBar, QSizePolicy,
        QSlider, QSpinBox, QStyleFactory, QTableWidget, QTabWidget, QTextEdit,
        QVBoxLayout, QWidget, QButtonGroup)
import random

from web_scrapping import WebScrapper

def testFunction(value):
    print("WORKS!" + str(value))
    return value

def randomNumber():
    return random.randint(1, 10000)

class DatabaseApp(QDialog):
    def __init__(self, parent=None):
        super(DatabaseApp, self).__init__(parent)

        self.setWindowTitle("Database Performance")
        self.resize(800, 400)
        

        self.originalPalette = QApplication.palette()

        # styleComboBox = QComboBox()
        # styleComboBox.addItems(QStyleFactory.keys())

        # styleLabel = QLabel("&Style:")
        # styleLabel.setBuddy(styleComboBox)

        # self.useStylePaletteradioButton = QradioButton("&Use style's standard palette")
        # self.useStylePaletteradioButton.setChecked(True)

        # disableWidgetsradioButton = QradioButton("&Disable widgets")

        # self.createTopLeftGroupBox()
        # self.createTopRightGroupBox()
        # self.createBottomLeftTabWidget()
        # self.createBottomRightGroupBox()
        # self.createProgressBar()
        self.createMainTabWidget()

        # styleComboBox.textActivated.connect(self.changeStyle)
        # self.useStylePaletteradioButton.toggled.connect(self.changePalette)
        # disableWidgetsradioButton.toggled.connect(self.topLeftGroupBox.setDisabled)
        # disableWidgetsradioButton.toggled.connect(self.topRightGroupBox.setDisabled)
        # disableWidgetsradioButton.toggled.connect(self.bottomLeftTabWidget.setDisabled)
        # disableWidgetsradioButton.toggled.connect(self.bottomRightGroupBox.setDisabled)
        self.label_numberOfRecords = QLabel()
        self.updateNumberOfRecords()
        # topLayout = QHBoxLayout()
        # topLayout.addWidget(label)
        # topLayout.addWidget(styleComboBox)
        # topLayout.addStretch(1)
        # topLayout.addWidget(self.useStylePaletteradioButton)
        # topLayout.addWidget(disableWidgetsradioButton)

        mainLayout = QGridLayout()
        mainLayout.addWidget(self.mainTabWidget)
        mainLayout.addWidget(self.label_numberOfRecords)
        # mainLayout.addWidget(self.topLeftGroupBox, 1, 0)
        # mainLayout.addWidget(self.topRightGroupBox, 1, 1)
        # mainLayout.addWidget(self.bottomLeftTabWidget)
        # mainLayout.addWidget(self.bottomRightGroupBox, 2, 1)
        # mainLayout.addWidget(self.progressBar, 3, 0, 1, 2)
        # mainLayout.setRowStretch(1, 1)
        # mainLayout.setRowStretch(2, 1)
        # mainLayout.setColumnStretch(0, 1)
        # mainLayout.setColumnStretch(1, 1)
        self.setLayout(mainLayout)

        # self.setWindowTitle("Styles")
        self.changeStyle('windowsvista')

    def updateNumberOfRecords(self):
        self.label_numberOfRecords.setText(f"Current number of records : {str(randomNumber())}")

    def createDatabase(self, _numberOfRecords):
        self.mainTabWidget.setDisabled(True)
        # create db function

        # update number of records
        self.updateNumberOfRecords()

        self.mainTabWidget.setDisabled(False)
        
        self.tab1LineEdit_NumberOfRecordsToAdd.setText("")

    def deleteDatabase(self):
        # delete db function

        # update number of records
        self.updateNumberOfRecords()

    def simpleTest(self):
        if self.tab2radioButton_Insert.isChecked():
            self.tab2Label_TestOutput.setText(f"It took {randomNumber()} seconds to insert {self.tab2LineEdit_NumberOfRecordsToTest.text()} records.")
        elif self.tab2radioButton_Modify.isChecked():
            self.tab2Label_TestOutput.setText(f"It took {randomNumber()} seconds to modify {self.tab2LineEdit_NumberOfRecordsToTest.text()} records.")
        elif self.tab2radioButton_Delete.isChecked():
            self.tab2Label_TestOutput.setText(f"It took {randomNumber()} seconds to insert {self.tab2LineEdit_NumberOfRecordsToTest.text()} records.")

        self.tab2LineEdit_NumberOfRecordsToTest.setText("")
        
        self.updateNumberOfRecords()

    def statisticsTest(self):
        self.tab3Label_TestOutput.setText(f"It took {randomNumber()} seconds to perform {self.tab3buttonGroup_testTypes.checkedButton().text()} on {self.tab3buttonGroup_columnNames.checkedButton().text()} column.")


    def webScrapping(self):
        web_scrapper = WebScrapper(self.tab5LineEdit_linkToIMDB.text())
        self.tab5Label_webScrapperOutput.setText(f"Added to databases: {web_scrapper.__dict__()}")

        self.tab5LineEdit_linkToIMDB.setText("")



    def createMainTabWidget(self):
        self.mainTabWidget = QTabWidget()
        # self.mainTabWidget.setSizePolicy(QSizePolicy.Policy.Preferred,
        #         QSizePolicy.Policy.Ignored)

        self.createTab1()

        self.createTab2()

        self.createTab3()

        self.createTab4()

        self.createTab5()
        # textEdit = QTextEdit()

        # textEdit.setPlainText("Twinkle, twinkle, little star,\n"
        #                       "How I wonder what you are.\n" 
        #                       "Up above the world so high,\n"
        #                       "Like a diamond in the sky.\n"
        #                       "Twinkle, twinkle, little star,\n" 
        #                       "How I wonder what you are!\n")

        # tab2hbox = QHBoxLayout()
        # tab2hbox.setContentsMargins(5, 5, 5, 5)
        # tab2hbox.addWidget(textEdit)
        # tab2.setLayout(tab2hbox)

        self.mainTabWidget.addTab(self.tab1, "DB Creation")
        self.mainTabWidget.addTab(self.tab2, "Basic Tests")
        self.mainTabWidget.addTab(self.tab3, "Statistics")
        self.mainTabWidget.addTab(self.tab4, "Custom Query")
        self.mainTabWidget.addTab(self.tab5, "Web Scrapping")


    def createTab1(self):
        self.tab1 = QWidget()
        self.tab1Layout = QVBoxLayout()
        
        self.tab1LineEdit_NumberOfRecordsToAdd = QLineEdit()
        self.tab1LineEdit_NumberOfRecordsToAdd.setPlaceholderText("Number of records to add")

        self.tab1Button_IniciateDb = QPushButton("Create Databases")
        self.tab1Button_IniciateDb.clicked.connect(self.createDatabase)

        self.tab1Button_DeleteDb = QPushButton("Delete Databases")
        self.tab1Button_DeleteDb.clicked.connect(self.deleteDatabase) # delete db

        self.tab1Layout.addWidget(self.tab1LineEdit_NumberOfRecordsToAdd)
        self.tab1Layout.addWidget(self.tab1Button_IniciateDb)
        self.tab1Layout.addStretch(1)
        self.tab1Layout.addWidget(self.tab1Button_DeleteDb)
        # self.tab1Layout.addWidget(self.tab1Label_NumberOfRecords)

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
        self.tab3radioButton_tconst.setChecked(True)

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
        self.tab3radioButton_countWords = QRadioButton("COUNT WORDS")
        self.tab3LineEdit_wordToCount = QLineEdit()
        self.tab3LineEdit_wordToCount.setPlaceholderText("Word to count")
        self.tab3LineEdit_wordToCount.setFixedWidth(200)
        self.tab3radioButton_dataDistribution = QRadioButton("DATA DISTRIBUTION")
        self.tab3radioButton_max.setChecked(True)

        self.tab3buttonGroup_testTypes = QButtonGroup()
        self.tab3buttonGroup_testTypes.addButton(self.tab3radioButton_max)
        self.tab3buttonGroup_testTypes.addButton(self.tab3radioButton_min)
        self.tab3buttonGroup_testTypes.addButton(self.tab3radioButton_median)
        self.tab3buttonGroup_testTypes.addButton(self.tab3radioButton_countRows)
        self.tab3buttonGroup_testTypes.addButton(self.tab3radioButton_countWords)
        self.tab3buttonGroup_testTypes.addButton(self.tab3radioButton_dataDistribution)

        self.tab3Button_RunTest = QPushButton("Start Test")
        self.tab3Button_RunTest.clicked.connect(self.statisticsTest)

        self.tab3Label_TestOutput = QLabel()

        # self.tab2Label_TypeOfOperation = QLabel("What operation would you like to test?")
        # self.tab2radioButton_Insert = QRadioButton("INSERT")
        # self.tab2radioButton_Modify = QRadioButton("MODIFY")
        # self.tab2radioButton_Delete = QRadioButton("DELETE")
        # self.tab2radioButton_Insert.setChecked(True)

        # self.tab2LineEdit_NumberOfRecordsToTest = QLineEdit()
        # self.tab2LineEdit_NumberOfRecordsToTest.setPlaceholderText("Number of records to perform action on")

        # self.tab2Button_RunTest = QPushButton("Start Test")
        # self.tab2Button_RunTest.clicked.connect(lambda: self.simpleTest(self.tab2LineEdit_NumberOfRecordsToTest.text()))



              
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
        self.tab3Layout_testTypes.addWidget(self.tab3radioButton_countWords)
        self.tab3Layout_testTypes.addWidget(self.tab3LineEdit_wordToCount)
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
        # self.tab4Layout

        self.tab4LineEdit_customQuery = QLineEdit()
        self.tab4LineEdit_customQuery.setPlaceholderText("Custom Query")

        self.tab4Button_PostgreSQL = QPushButton("Test PostgreSQL")
        self.tab4Button_MongoDB = QPushButton("Test MongoDB")
        self.tab4Button_InfluxDB = QPushButton("Test InfluxDB")

        self.tab4Layout.addWidget(self.tab4LineEdit_customQuery)
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
        # if (self.useStylePaletteradioButton.isChecked()):
        #     QApplication.setPalette(QApplication.style().standardPalette())
        # else:
        QApplication.setPalette(self.originalPalette)

    # def advanceProgressBar(self):
    #     self.progressBar.setText(str(randomNumber()))

    # def createTopLeftGroupBox(self):
    #     self.topLeftGroupBox = QGroupBox("Group 1")

    #     radioButton1 = QRadioButton("Radio button 1")
    #     radioButton2 = QRadioButton("Radio button 2")
    #     radioButton3 = QRadioButton("Radio button 3")
    #     radioButton1.setChecked(True)

    #     radioButton = QradioButton("Tri-state check box")
    #     radioButton.setTristate(True)
    #     radioButton.setCheckState(Qt.CheckState.PartiallyChecked)

    #     layout = QVBoxLayout()
    #     layout.addWidget(radioButton1)
    #     layout.addWidget(radioButton2)
    #     layout.addWidget(radioButton3)
    #     layout.addWidget(radioButton)
    #     layout.addStretch(1)
    #     self.topLeftGroupBox.setLayout(layout)

    # def createTopRightGroupBox(self):
    #     self.topRightGroupBox = QGroupBox("Group 2")

    #     defaultPushButton = QPushButton("Default Push Button")
    #     defaultPushButton.setDefault(True)

    #     togglePushButton = QPushButton("Toggle Push Button")
    #     togglePushButton.setCheckable(True)
    #     togglePushButton.setChecked(True)

    #     flatPushButton = QPushButton("Flat Push Button")
    #     flatPushButton.setFlat(True)

    #     layout = QVBoxLayout()
    #     layout.addWidget(defaultPushButton)
    #     layout.addWidget(togglePushButton)
    #     layout.addWidget(flatPushButton)
    #     layout.addStretch(1)
    #     self.topRightGroupBox.setLayout(layout)

    # def createBottomLeftTabWidget(self):
    #     self.bottomLeftTabWidget = QTabWidget()
    #     self.bottomLeftTabWidget.setSizePolicy(QSizePolicy.Policy.Preferred,
    #             QSizePolicy.Policy.Ignored)

    #     tab1 = QWidget()
    #     tableWidget = QTableWidget(10, 10)

    #     tab1hbox = QHBoxLayout()
    #     tab1hbox.setContentsMargins(5, 5, 5, 5)
    #     tab1hbox.addWidget(tableWidget)
    #     tab1.setLayout(tab1hbox)

    #     tab2 = QWidget()
    #     textEdit = QTextEdit()

    #     textEdit.setPlainText("Twinkle, twinkle, little star,\n"
    #                           "How I wonder what you are.\n" 
    #                           "Up above the world so high,\n"
    #                           "Like a diamond in the sky.\n"
    #                           "Twinkle, twinkle, little star,\n" 
    #                           "How I wonder what you are!\n")

    #     tab2hbox = QHBoxLayout()
    #     tab2hbox.setContentsMargins(5, 5, 5, 5)
    #     tab2hbox.addWidget(textEdit)
    #     tab2.setLayout(tab2hbox)

    #     self.bottomLeftTabWidget.addTab(tab1, "&Table")
    #     self.bottomLeftTabWidget.addTab(tab2, "Text &Edit")

    # def createBottomRightGroupBox(self):
    #     self.bottomRightGroupBox = QGroupBox("Group 3")
    #     self.bottomRightGroupBox.setCheckable(True)
    #     self.bottomRightGroupBox.setChecked(True)

    #     lineEdit = QLineEdit('s3cRe7')
    #     lineEdit.setEchoMode(QLineEdit.EchoMode.Password)

    #     spinBox = QSpinBox(self.bottomRightGroupBox)
    #     spinBox.setValue(50)

    #     dateTimeEdit = QDateTimeEdit(self.bottomRightGroupBox)
    #     dateTimeEdit.setDateTime(QDateTime.currentDateTime())

    #     slider = QSlider(Qt.Orientation.Horizontal, self.bottomRightGroupBox)
    #     slider.setValue(40)

    #     scrollBar = QScrollBar(Qt.Orientation.Horizontal, self.bottomRightGroupBox)
    #     scrollBar.setValue(60)

    #     dial = QDial(self.bottomRightGroupBox)
    #     dial.setValue(30)
    #     dial.setNotchesVisible(True)

    #     layout = QGridLayout()
    #     layout.addWidget(lineEdit, 0, 0, 1, 2)
    #     layout.addWidget(spinBox, 1, 0, 1, 2)
    #     layout.addWidget(dateTimeEdit, 2, 0, 1, 2)
    #     layout.addWidget(slider, 3, 0)
    #     layout.addWidget(scrollBar, 4, 0)
    #     layout.addWidget(dial, 3, 1, 2, 1)
    #     layout.setRowStretch(5, 1)
    #     self.bottomRightGroupBox.setLayout(layout)

    # def createProgressBar(self):
    #     self.progressBar = QLabel()
    #     # self.progressBar.setRange(0, 10000)
    #     # self.progressBar.setValue(0)

    #     timer = QTimer(self)
    #     timer.timeout.connect(self.advanceProgressBar)
    #     timer.start(1000)


if __name__ == '__main__':

    import sys

    app = QApplication(sys.argv)
    gallery = DatabaseApp()
    gallery.show()
    sys.exit(app.exec())