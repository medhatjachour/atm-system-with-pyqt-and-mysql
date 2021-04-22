import sys
import platform
import mysql.connector
import datetime  
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from system import Ui_MainWindow as Main
from system import chngpnflg
from msgBox import Ui_MainWindow as msgbox
from returMessage import Ui_MainWindow as returnmsg

langue = False
arabic = False
english = False
operation = False
withdrawl = False
deposit = False


pinCounter = 0
depositFlag = False  # to chick if it's deposit or cashwithdrawl
counterFlag = 1  # for return in which he clicked at deposit

cardType = 0

counter = 0

#############################DATABASE##########################################
db = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="0000",
    database="atm")
control = db.cursor()
###############################################################################
cardNumber = ""
pin0 = ""
balanc = None

def checkLuhn(cardNo):
    nDigits = len(cardNo)
    nSum = 0
    isSecond = False

    for i in range(nDigits - 1, -1, -1):
        d = ord(cardNo[i]) - ord('0')
 
        if (isSecond == True):
            d = d * 2

        # We add two digits to handle
        # cases that make two digits after
        # doubling
        nSum += d // 10
        nSum += d % 10

        isSecond = not isSecond

    if (nSum % 10 == 0):
        return True
    else:
        return False

def validation(number_str):
	global cardType
	if (checkLuhn(number_str)):
		if len(number_str) == 16:
			if number_str[0] == "4":
				cardType = 1
			elif number_str[0] == "5" and "0" < number_str[1] < "6":
				cardType = 2
			else:
				cardType = 0
	else:
	    print("Invalid card number")

class System(QMainWindow):
	"""docstring for SplashScreen"""

	def __init__(self):
		QMainWindow.__init__(self)
		self.ui = Main()
		self.ui.setupUi(self)
		self.showMsgBox = MsgBox()
# Reomve the title bar
		self.shadow = QGraphicsDropShadowEffect(self)
		self.shadow.setBlurRadius(20)
		self.shadow.setXOffset(0)
		self.shadow.setYOffset(0)
		self.shadow.setColor(QColor(0, 0, 0, 60))
# operation and Language and start
		self.ui.arabicbtn.clicked.connect(self.arabicFun)
		self.ui.englishbtn.clicked.connect(self.englishFun)
		self.ui.drawchose.clicked.connect(self.withdrawlFun)
		self.ui.depochose.clicked.connect(self.depositFun)
		self.ui.Continue.clicked.connect(self.startFun)
# English loogin
		# if the Card is wrong it will return to main
		self.ui.enterCArdLogin.clicked.connect(self.enterCardEng)
		self.ui.pushButtonaccept_3.clicked.connect(self.Acceptpineng)
		self.ui.backbtn.clicked.connect(self.backFun)
		self.ui.pushButtoncancel.clicked.connect(self.backFun)
# main english btn
		self.ui.cashWithdrawal.clicked.connect(self.mnCashWithDraw)
		self.ui.depositbtn.clicked.connect(self.mnTrasnfer)
		self.ui.ChangePINbtn.clicked.connect(self.mnChangePin)
		self.ui.pushButton_6.clicked.connect(self.mnDeposit)
		self.ui.pushButtonemnter.clicked.connect(self.depositbuttonentr)  # for deposi
# Arabic log in btns
		self.ui.enterCArdLogin_2.clicked.connect(self.enterCardArab)
		self.ui.pushButtonaccept_4.clicked.connect(self.Acceptpinarab)
		self.ui.backbtn_2.clicked.connect(self.backFun)
		self.ui.pushButtoncancel_2.clicked.connect(self.backFun)
# main arabic btn
		self.ui.cashWithdrawal_2.clicked.connect(self.mnCashWithDrawAR)
		self.ui.depositbtn_2.clicked.connect(self.mnTrasnferAR)
		self.ui.ChangePINbtn_2.clicked.connect(self.mnChangePinAR)
		self.ui.depositbtn_3.clicked.connect(self.mnDepositAR)
		self.ui.pushButtonemnter_2.clicked.connect(self.depositbuttonentrAr)  # for deposi

######################## _________ ###########-_________##########_________#####
# operation and Language and start
	def arabicFun(self):
		global langue
		global arabic
		global english
		langue = True
		arabic = True
		english = False

	def englishFun(self):
		global langue
		global arabic
		global english
		langue = True
		arabic = False
		english = True

	def withdrawlFun(self):
		global operation
		global withdrawl
		global deposit
		global depositFlag
		depositFlag = True
		operation = True
		withdrawl = True
		deposit = False

	def depositFun(self):
		global operation
		global withdrawl
		global deposit
		operation = True
		withdrawl = False
		deposit = True

	def startFun(self):
		global langue
		global operation
		self.ui.arabicbtn.setStyleSheet("QPushButton\n"
		    "{\n"
		    "    font: 18pt \"MS Shell Dlg 2\";\n"
		    "    border:0px;\n"
		    "    color:#fff;\n"
		    "    background-color: rgb(42, 55, 67);\n"
		    "}\n")
		self.ui.englishbtn.setStyleSheet("QPushButton\n"
		    "{\n"
		    "    font: 18pt \"MS Shell Dlg 2\";\n"
		    "    border:0px;\n"
		    "    color:#fff;\n"
		    "    background-color: rgb(42, 55, 67);\n"
		    "}\n")
		self.ui.drawchose.setStyleSheet("QPushButton\n"
		    "{\n"
		    "    font: 18pt \"MS Shell Dlg 2\";\n"
		    "    border:0px;\n"
		    "    color:#fff;\n"
		    "    background-color: rgb(42, 55, 67);\n"
		    "}\n")
		self.ui.depochose.setStyleSheet("QPushButton\n"
		    "{\n"
		    "    font: 18pt \"MS Shell Dlg 2\";\n"
		    "    border:0px;\n"
		    "    color:#fff;\n"
		    "    background-color: rgb(42, 55, 67);\n"
		    "}\n")
		if langue == True and operation == True:
			if arabic == True and withdrawl == True:
				self.ui.cashWithdrawal.setStyleSheet("QPushButton{\n"
					"border:0px;\n"
					"Text-align:left;\n"

					"color: rgb(255, 255, 255);\n"
					"    border:1px solid rgb(98, 119, 144);\n"
					"    border-radius:6px;\n"
					"    background-color: rgb(98, 119, 144);\n"
					"    font: 20pt \"MS Shell Dlg 2\";\n"
					"}\n")
				self.ui.HomeStack.setCurrentIndex(3)  # main widget
				self.ui.stackedWidget_2.setCurrentIndex(1)
				operation = False
				langue = False
			elif english == True and withdrawl == True:
				self.ui.cashWithdrawal.setStyleSheet("QPushButton{\n"
					"border:0px;\n"
					"Text-align:left;\n"
					"color: rgb(255, 255, 255);\n"
					"    border:1px solid rgb(98, 119, 144);\n"
					"    border-radius:6px;\n"
					"    background-color: rgb(98, 119, 144);\n"
					"    font: 20pt \"MS Shell Dlg 2\";\n"
					"}\n")
				self.ui.HomeStack.setCurrentIndex(1)  # main widget
				self.ui.stackedWidget_2.setCurrentIndex(1)
				operation = False
				langue = False
			elif arabic == True and deposit == True:
				self.ui.HomeStack.setCurrentIndex(4)  # main widget
				self.ui.ControlStackWidget_2.setCurrentIndex(2)
				self.ui.depositbtn_3.setStyleSheet("QPushButton{\n"
					"border:0px;\n"
					"Text-align:left;\n"
					"color: rgb(255, 255, 255);\n"
					"    border:1px solid rgb(98, 119, 144);\n"
					"    border-radius:6px;\n"
					"    background-color: rgb(230, 126, 34);\n"
					"    font: 20pt \"MS Shell Dlg 2\";\n"
					"}\n")
				operation = False
				langue = False
			elif english == True and deposit == True:
				self.ui.HomeStack.setCurrentIndex(2)  # main widget
				self.ui.ControlStackWidget.setCurrentIndex(2)
				self.ui.pushButton_6.setStyleSheet("QPushButton{\n"
					"border:0px;\n"
					"Text-align:left;\n"
					"color: rgb(255, 255, 255);\n"
					"    border:1px solid rgb(98, 119, 144);\n"
					"    border-radius:6px;\n"
					"    background-color: rgb(230, 126, 34);\n"
					"    font: 20pt \"MS Shell Dlg 2\";\n"
					"}\n")
				operation = False
				langue = False
		elif langue == False:
			self.showMsgBox.show()
			self.showMsgBox.ui.label_2.setText("Language")
			self.showMsgBox.ui.label_4.setText("you forget to choose a language")
			self.showMsgBox.ui.label_3.setText(
			    "choose your preffred language english or عربي")
		elif operation == False:
			self.showMsgBox.show()
			self.showMsgBox.ui.label_2.setText("operation")
			self.showMsgBox.ui.label_4.setText("you forget to choose an operation")
			self.showMsgBox.ui.label_3.setText(
			    "choose your preffred operation cashWithdrawal or deposit")
# english login fun

	def backFun(self):
		global langue
		global arabic
		global english
		global operation
		global withdrawl
		global deposit
		global pinCounter
		global depositFlag
		global counterFlag
		langue = False
		arabic = False
		english = False
		operation = False
		withdrawl = False
		deposit = False
		pinCounter = 0
		depositFlag = False  # to chick if it's deposit or cashwithdrawl
		counterFlag = 1
		self.ui.cashWithdrawal.setStyleSheet("QPushButton{\n"
					"border:0px;\n"
					"Text-align:left;\n"
					"color: rgb(255, 255, 255);\n"
					"    border-radius:6px;\n"
					"    background-color: rgb(30, 37, 45);\n"
					"    font: 20pt \"MS Shell Dlg 2\";\n"
					"}\n")
		self.ui.cashWithdrawal_2.setStyleSheet("QPushButton{\n"
					"border:0px;\n"
					"Text-align:left;\n"
					"color: rgb(255, 255, 255);\n"
					"    border-radius:6px;\n"
					"    background-color: rgb(30, 37, 45);\n"
					"    font: 20pt \"MS Shell Dlg 2\";\n"
					"}\n")
		self.ui.depositbtn_2.setStyleSheet("QPushButton{\n"
					"border:0px;\n"
					"Text-align:left;\n"
					"color: rgb(255, 255, 255);\n"
					"    border-radius:6px;\n"
					"    background-color: rgb(30, 37, 45);\n"
					"    font: 20pt \"MS Shell Dlg 2\";\n"
					"}\n")
		self.ui.ChangePINbtn_2.setStyleSheet("QPushButton{\n"
					"border:0px;\n"
					"Text-align:left;\n"
					"color: rgb(255, 255, 255);\n"
					"    border-radius:6px;\n"
					"    background-color: rgb(30, 37, 45);\n"
					"    font: 20pt \"MS Shell Dlg 2\";\n"
					"}\n")
		self.ui.depositbtn.setStyleSheet("QPushButton{\n"
					"border:0px;\n"
					"Text-align:left;\n"
					"color: rgb(255, 255, 255);\n"
					"    border-radius:6px;\n"
					"    background-color: rgb(30, 37, 45);\n"
					"    font: 20pt \"MS Shell Dlg 2\";\n"
					"}\n")
		self.ui.ChangePINbtn.setStyleSheet("QPushButton{\n"
					"border:0px;\n"
					"Text-align:left;\n"
					"color: rgb(255, 255, 255);\n"
					"    border-radius:6px;\n"
					"    background-color: rgb(30, 37, 45);\n"
					"    font: 20pt \"MS Shell Dlg 2\";\n"
					"}\n")
		self.ui.pushButton_6.setStyleSheet("QPushButton{\n"
					"border:0px;\n"
					"Text-align:left;\n"
					"color: rgb(255, 255, 255);\n"
					"    border-radius:6px;\n"
					"    background-color: rgb(30, 37, 45);\n"
					"    font: 20pt \"MS Shell Dlg 2\";\n"
					"}\n")
		self.ui.depositbtn_3.setStyleSheet("QPushButton{\n"
					"border:0px;\n"
					"Text-align:left;\n"
					"color: rgb(255, 255, 255);\n"
					"    border-radius:6px;\n"
					"    background-color: rgb(30, 37, 45);\n"
					"    font: 20pt \"MS Shell Dlg 2\";\n"
					"}\n")

		self.ui.HomeStack.setCurrentIndex(0)
		self.ui.stackedWidget_2.setCurrentIndex(1)
		self.ui.stackedWidget_3.setCurrentIndex(1)
		self.ui.cardvalue.setText("")
		self.ui.pinvalue.setText("")
		self.ui.cardvalue_2.setText("")
		self.ui.pinvalue_2.setText("")

	def enterCardEng(self):
		global cardNumber
		cardNumber = self.ui.cardvalue.text()
		validation(cardNumber)
		control.execute("SELECT card_num FROM bank")
		cards = control.fetchall()
		card = [i[0] for i in cards]
		if cardNumber in card:
			self.ui.stackedWidget_2.setCurrentIndex(0)
		else:
			self.ui.cardvalue.setText("")
			self.ui.pinvalue.setText("")
			self.ui.pineeror.setText("")
			self.ui.HomeStack.setCurrentIndex(0)
			self.showMsgBox.show()
			self.showMsgBox.ui.label_2.setText("Card Not Valid")
			self.showMsgBox.ui.label_4.setText("please check your card")
			self.showMsgBox.ui.label_3.setText("you can re-enter the card or call 19033")

	def Acceptpineng(self):
		global cardType

		if cardType == 0:
			pass
		elif cardType == 1:
			self.ui.label_48.setText("Visa")
			self.ui.label_11.setText("Visa")
		elif cardType == 2:
			self.ui.label_48.setText("MasterCard")
			self.ui.label_11.setText("MasterCard")
		global pinCounter
		global depositFlag
		global pin0
		global balanc
		pin = self.ui.pinvalue.text()
		control.execute(
			"SELECT pin FROM bank WHERE card_num = (%s)", (cardNumber,))
		pin0 = control.fetchone()
		pin0 = pin0[0]
		if pin == pin0 and pinCounter < 4:
			pinCounter = 0
			depositFlag = True
			self.ui.HomeStack.setCurrentIndex(2)
			control.execute(
				"SELECT client_name FROM bank WHERE card_num = (%s)", (cardNumber,))
			name = control.fetchone()
			self.ui.NameLAbel.setText(name[0])#######
			self.ui.NumberLbl.setText(cardNumber)#######
			control.execute(
				"SELECT balance FROM bank WHERE card_num = (%s)", (cardNumber,))
			balanc = control.fetchone()
			balanc = balanc[0]
			self.ui.balanceLable.setText(str(balanc))#######
			self.ui.balanceLable_4.setText(str(balanc))#######
			self.ui.ControlStackWidget.setCurrentIndex(counterFlag)
			self.ui.cardvalue.setText("")
			self.ui.pinvalue.setText("")
		else:
			pinCounter = pinCounter + 1
			self.ui.pinvalue.setText("")
			self.ui.pineeror.setText(
			    "Please Enter avalid Pin ," + str(4 - pinCounter) + " remaining try")
		if pinCounter == 4:
			pinCounter = 0
			self.ui.cardvalue.setText("")
			self.ui.pinvalue.setText("")
			self.ui.pineeror.setText("")
			self.ui.HomeStack.setCurrentIndex(0)
			self.ui.stackedWidget_2.setCurrentIndex(1)
			self.showMsgBox.show()
			self.showMsgBox.ui.label_2.setText("PIN isn't Valid")
			self.showMsgBox.ui.label_4.setText("please check your PIN")
			self.showMsgBox.ui.label_3.setText(
			    "your pin is De-Activate please call 19033 or go to client services")
# main English

	def mnCashWithDraw(self):
		global counterFlag
		counterFlag = 1
		if depositFlag == True:
			self.ui.ControlStackWidget.setCurrentIndex(1)
		else:
			self.ui.HomeStack.setCurrentIndex(1)

	def mnTrasnfer(self):
		global counterFlag
		counterFlag = 3
		if depositFlag == True:
			self.ui.ControlStackWidget.setCurrentIndex(3)
		else:
			self.ui.HomeStack.setCurrentIndex(1)

	def mnChangePin(self):
		global counterFlag
		counterFlag = 4
		if depositFlag == True:
			self.ui.ControlStackWidget.setCurrentIndex(4)
		else:
			self.ui.HomeStack.setCurrentIndex(1)

	def mnDeposit(self):
		self.ui.ControlStackWidget.setCurrentIndex(2)

	def depositbuttonentr(self):
		monyvalueenter = self.ui.lineEditEnterMony.text()
		text = self.ui.labelcheckmony.text()
		# qTimer ==> start
		self.timer = QtCore.QTimer()
		self.timer.timeout.connect(self.progress)
		# timer in ms
		self.timer.start(20)
		# change disc
		QtCore.QTimer.singleShot(0, lambda: self.ui.label_22.setText(
		    "<strong>Counting </strong> Money  "))
		QtCore.QTimer.singleShot(1800, lambda: self.ui.label_22.setText(
		    "<strong> Comparing </strong> Money "))

	def progress(self):
		global counter
		monyvalueenter = self.ui.lineEditEnterMony.text()
		# set value to progress bar
		self.ui.progressBar.setValue(counter)
		# close splash scren and open app
		if counter > 100:
			# stop timer
			self.ui.labelcheckmony.setText(monyvalueenter)
			self.timer.stop()
			# increse counter
		counter = counter + 1

# arabic login fun

	def enterCardArab(self):
		global cardNumber
		cardNumber = self.ui.cardvalue_2.text()
		validation(cardNumber)
		control.execute("SELECT card_num FROM bank")
		cards = control.fetchall()
		card = [i[0] for i in cards]
		if cardNumber in card:
			self.ui.stackedWidget_3.setCurrentIndex(0)
		else:
			self.ui.cardvalue_2.setText("")
			self.ui.HomeStack.setCurrentIndex(0)
			self.showMsgBox.show()
			self.showMsgBox.ui.label_2.setText("البطاقةة ليست متاحه")
			self.showMsgBox.ui.label_4.setText("من فضلك تاكد من البطاقة")
			self.showMsgBox.ui.label_3.setText("من الممكن اعادة ادخال البطاقه او الاتصال بخدمة العملاء 19903")
		
	def Acceptpinarab(self):
		global cardType
		if cardType == 0:
			pass
		elif cardType == 1:
			self.ui.label_48.setText("Visa")
			self.ui.label_11.setText("Visa")
		elif cardType == 2:
			self.ui.label_48.setText("MasterCard")
			self.ui.label_11.setText("MasterCard")
		global pinCounter
		global depositFlag
		global pin0
		global balanc
		pin = self.ui.pinvalue_2.text()
		control.execute(
			"SELECT pin FROM bank WHERE card_num = (%s)", (cardNumber,))
		pin0 = control.fetchone()
		pin0 = pin0[0]
		if pin == pin0 and pinCounter < 4:
			depositFlag = True
			self.ui.HomeStack.setCurrentIndex(4)
			control.execute(
				"SELECT client_name FROM bank WHERE card_num = (%s)", (cardNumber,))
			name = control.fetchone()
			self.ui.NameLAbel_2.setText(name[0])#######
			self.ui.NumberLbl_2.setText(cardNumber)#######
			control.execute(
				"SELECT balance FROM bank WHERE card_num = (%s)", (cardNumber,))
			balanc = control.fetchone()
			balanc = balanc[0]
			self.ui.balanceLable_2.setText(str(balanc))#######
			self.ui.balanceLable_3.setText(str(balanc))#######
			self.ui.ControlStackWidget_2.setCurrentIndex(counterFlag)
			self.ui.cardvalue_2.setText("")
			self.ui.pinvalue_2.setText("")

		else:
			pinCounter = pinCounter + 1
			self.ui.pinvalue_2.setText("")
			self.ui.pineeror_2.setText("من فضلك ادخل  ال PIN ,"+ str(4 - pinCounter) + " محاولات متبقية")
		if pinCounter == 4:
			pinCounter = 0
			self.ui.cardvalue_2.setText("")
			self.ui.pinvalue_2.setText("")
			self.ui.pineeror_2.setText("")
			self.ui.HomeStack.setCurrentIndex(0)
			self.ui.stackedWidget_3.setCurrentIndex(1)
			self.showMsgBox.show()
			self.showMsgBox.ui.label_2.setText("PIN isn't Valid")
			self.showMsgBox.ui.label_4.setText("please check your PIN")
			self.showMsgBox.ui.label_3.setText("your pin is De-Activate please call 19033 or go to client services")
# main arabic
	def mnCashWithDrawAR(self):
		global counterFlag
		counterFlag = 1
		if depositFlag == True:
			self.ui.ControlStackWidget_2.setCurrentIndex(1)
		else:
			self.ui.HomeStack.setCurrentIndex(3)
	def mnTrasnferAR(self):
		global counterFlag
		counterFlag = 3
		if depositFlag == True:
			self.ui.ControlStackWidget_2.setCurrentIndex(3)
		else:
			self.ui.HomeStack.setCurrentIndex(3)
	def mnChangePinAR(self):
		global counterFlag
		counterFlag = 4
		if depositFlag == True:
			self.ui.ControlStackWidget_2.setCurrentIndex(4)
		else:
			self.ui.HomeStack.setCurrentIndex(3)
	def mnDepositAR(self):
		self.ui.ControlStackWidget_2.setCurrentIndex(2)
	def depositbuttonentrAr(self):
		monyvalueenter = self.ui.lineEditEnterMony_2.text()
		text = self.ui.labelcheckmony_2.text()
		# qTimer ==> start
		self.timer = QtCore.QTimer()
		self.timer.timeout.connect(self.progressAr)
		# timer in ms
		self.timer.start(20)
		# change disc
		QtCore.QTimer.singleShot(0,lambda:self.ui.label_39.setText("<strong>Counting </strong> Money  "))
		QtCore.QTimer.singleShot(1800,lambda:self.ui.label_39.setText("<strong> Comparing </strong> Money "))
	def progressAr(self):
		global counter
		monyvalueenter = self.ui.lineEditEnterMony_2.text()
		# set value to progress bar
		self.ui.progressBar_2.setValue(counter)
		# close splash scren and open app
		if counter > 100:
			# stop timer
			self.ui.labelcheckmony_2.setText(monyvalueenter)
			self.timer.stop()
			# increse counter
		counter = counter + 1

class MsgBox(QMainWindow):
	"""docstring for SplashScreen"""
	def __init__(self):
		QMainWindow.__init__(self)
		self.ui = msgbox()
		self.ui.setupUi(self)
	# Reomve the title bar
		self.setWindowFlag(QtCore.Qt.FramelessWindowHint )
		self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
	# shadow effect
		self.shadow = QGraphicsDropShadowEffect(self)
		self.shadow.setBlurRadius(30)
		self.shadow.setXOffset(10)
		self.shadow.setYOffset(10)
		self.shadow.setColor(QColor(88,88,88,60))
	# show close
		self.ui.pushButton.clicked.connect(lambda:self.close())
class ReturnMsgBox(QMainWindow):
	"""docstring for SplashScreen"""
	def __init__(self):
		QMainWindow.__init__(self)
		self.ui = returnmsg()
		self.ui.setupUi(self)
	# Reomve the title bar
		self.setWindowFlag(QtCore.Qt.FramelessWindowHint )
		self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
	# shadow effect
		self.shadow = QGraphicsDropShadowEffect(self)
		self.shadow.setBlurRadius(30)
		self.shadow.setXOffset(10)
		self.shadow.setYOffset(10)
		self.shadow.setColor(QColor(88,88,88,60))
	# show close
		self.ui.okButton.clicked.connect(lambda:self.close())
class StartClass(QMainWindow):
	"""docstring for StartClass"""
	def __init__(self,):
		QMainWindow.__init__(self)
		self.ui = Main()
		self.ui.setupUi(self)
		self.startSys = System()
		self.startSys.show()
		self.rtrnMSG = ReturnMsgBox()
		self.msBox = MsgBox()
	# English Accept
		self.startSys.ui.mostcommonaccept.clicked.connect(self.mnwithdrawlAccept) #mostCommon
		self.startSys.ui.pushButtonaccept.clicked.connect(self.withdrawlAccept) #customize
		self.startSys.ui.pushButtonaccepttrnsfer.clicked.connect(self.TrasnferFunAccept) #transfer\
		self.startSys.ui.acceptdeposit.clicked.connect(self.depositbuttonaccept) # for depost
		self.startSys.ui.pushButtontpinchngpn.clicked.connect(self.changePin) # for change
	
	# Arabic Accept
		self.startSys.ui.mostcommonaccept_2.clicked.connect(self.mnwithdrawlAcceptAR) #mostCommon
		self.startSys.ui.pushButtonaccept_2.clicked.connect(self.withdrawlAcceptAR) #customize
		self.startSys.ui.pushButtonaccepttrnsfer_2.clicked.connect(self.TrasnferFunAcceptAr) #customize
		self.startSys.ui.acceptdeposit_2.clicked.connect(self.depositbuttonacceptAr) # for depost
		self.startSys.ui.pushButtontpinchngpn_2.clicked.connect(self.changePinAr) # for change

	# MSG
		self.rtrnMSG.ui.noButton.clicked.connect(self.noAction)
# Englis
	def mnwithdrawlAccept(self):
		global balanc
		out0 = self.startSys.ui.outComeLabel.text()
		out4 = self.startSys.ui.outComeLabel_4.text()
		text = self.startSys.ui.mostcommonlbl.text()
		IntText = int(text)
		if balanc >= IntText:
			if IntText != 0:
				balanc -= IntText
				control.execute("UPDATE bank SET balance = (%s) WHERE card_num = (%s)", (balanc, cardNumber,))
				db.commit()
				self.startSys.ui.balanceLable.setText(str(balanc))
				self.startSys.ui.balanceLable_4.setText(str(balanc))
				self.startSys.ui.outComeLabel.setText( str(int(text) + int(out0)))  
				self.startSys.ui.outComeLabel_4.setText(str(int(text) + int(out4)))
				self.rtrnMSG.show()
				self.rtrnMSG.ui.label_2.setText("withdrawl Operation is Done")
				self.rtrnMSG.ui.label_4.setText("do wannt to make another Operation ?")
				self.rtrnMSG.ui.label_3.setText("pleae wait for the Cash")
			else:
				self.rtrnMSG.show()
				self.rtrnMSG.ui.label_2.setText("Missing")
				self.rtrnMSG.ui.label_4.setText("please chose the value before making the Operation")
				self.rtrnMSG.ui.label_3.setText("do you want to try again ?")

		else:
			self.rtrnMSG.show()
			self.rtrnMSG.ui.label_2.setText("Error")
			self.rtrnMSG.ui.label_4.setText("There no enaugh Money in your bank account")
			self.rtrnMSG.ui.label_3.setText("do you want to try again ?")

	def withdrawlAccept(self):
		global balanc
		self.rtrnMSG.show()
		out0 = self.startSys.ui.outComeLabel.text()
		out4 = self.startSys.ui.outComeLabel_4.text()
		text = self.startSys.ui.CashValue.text()
		if text != '' and text != ' ':
			IntText = int(text)
			if balanc >= IntText:
				if IntText != 0:
					balanc -= IntText
					control.execute("UPDATE bank SET balance = (%s) WHERE card_num = (%s)", (balanc, cardNumber,))
					db.commit()
					self.startSys.ui.balanceLable.setText(str(balanc))
					self.startSys.ui.balanceLable_4.setText(str(balanc))
					self.startSys.ui.outComeLabel.setText( str(int(text) + int(out0)))  
					self.startSys.ui.outComeLabel_4.setText(str(int(text) + int(out4)))
					self.rtrnMSG.ui.label_2.setText("withdrawl Operation is Done")
					self.rtrnMSG.ui.label_4.setText("do wannt to make another Operation ?")
					self.rtrnMSG.ui.label_3.setText("pleae wait for the Cash")
				else:
					self.rtrnMSG.show()
					self.rtrnMSG.ui.label_2.setText("Missing")
					self.rtrnMSG.ui.label_4.setText("please chose the value before making the Operation")
					self.rtrnMSG.ui.label_3.setText("do you want to try again ?")
			else:
				self.rtrnMSG.show()
				self.rtrnMSG.ui.label_2.setText("Error")
				self.rtrnMSG.ui.label_4.setText("There no enaugh Money in your bank account")
				self.rtrnMSG.ui.label_3.setText("do you want to try again ?")
		else:
			self.rtrnMSG.show()
			self.rtrnMSG.ui.label_2.setText("Missing")
			self.rtrnMSG.ui.label_4.setText("please check the amount ")
			self.rtrnMSG.ui.label_3.setText("do you want to try again ?")


	def TrasnferFunAccept(self):
		global balanc
		cardtrnsNm = self.startSys.ui.lineEdit15dgt.text()
		cardtrnsMony = self.startSys.ui.lineEditvrfynum.text()
		self.startSys.ui.lineEditvrfynum.setText("")
		self.startSys.ui.lineEdit15dgt.setText("")
		control.execute("SELECT card_num FROM bank")
		cards = control.fetchall()
		card = [i[0] for i in cards]
		if cardtrnsNm in card:
			control.execute("SELECT balance FROM bank WHERE card_num = (%s)", (cardtrnsNm,))
			balanc1 = control.fetchone()
			y, z = int(cardtrnsMony), balanc1[0]
			if balanc >= y:
				balanc -= y
				z += y
				control.execute("UPDATE bank SET balance = (%s) WHERE card_num = (%s)", (z, cardtrnsNm,))
				control.execute("UPDATE bank SET balance = (%s) WHERE card_num = (%s)", (balanc, cardNumber,))
				db.commit()
				self.rtrnMSG.show()
				self.rtrnMSG.ui.label_2.setText("Transfer Operation is Done")
				self.rtrnMSG.ui.label_4.setText("do want to make another Operation ?")
				self.rtrnMSG.ui.label_3.setText("you can check the trasnfered account")
				self.startSys.ui.balanceLable.setText(str(balanc))
				self.startSys.ui.balanceLable_4.setText(str(balanc))
				self.startSys.ui.outComeLabel.setText(cardtrnsMony)
				self.startSys.ui.outComeLabel_4.setText(cardtrnsMony)
			else:
				self.msBox.show()
				self.msBox.ui.label_2.setText("Error")
				self.msBox.ui.label_4.setText("There's no enaugh Money to trasnfer")
				self.msBox.ui.label_3.setText("try again please")
		else:
			self.msBox.show()
			self.msBox.ui.label_2.setText("Error")
			self.msBox.ui.label_4.setText("can't find the account")
			self.msBox.ui.label_3.setText("try again please")

	def depositbuttonaccept(self):
		monyvalueenter = self.startSys.ui.lineEditEnterMony.text()
		accountNumber = self.startSys.ui.deposit16dgt.text()
		global counter
		counter = 0
		self.startSys.ui.progressBar.setValue(counter)
		self.rtrnMSG.show()
		self.rtrnMSG.ui.label_2.setText("Done")
		self.rtrnMSG.ui.label_4.setText("The Deposit Operation Is Done Successfully")
		self.rtrnMSG.ui.label_3.setText("check the accoount to make sure")
		control.execute("SELECT card_num FROM bank")
		cards = control.fetchall()
		card = [i[0] for i in cards]
		if accountNumber in card:
			control.execute("SELECT balance FROM bank WHERE card_num = (%s)", (accountNumber,))
			balanc2 = control.fetchone()
			x = balanc2[0]
			control.execute("UPDATE bank SET balance = (%s) WHERE card_num = (%s)", (x + int(monyvalueenter), accountNumber,))
			db.commit()
			self.startSys.ui.deposit16dgt.setText("")
			self.startSys.ui.lineEditEnterMony.setText("")
			self.startSys.ui.labelcheckmony.setText("")
		else:
			self.rtrnMSG.show()
			self.rtrnMSG.ui.label_2.setText("Error")
			self.rtrnMSG.ui.label_4.setText("The account number is not correct")			
			self.rtrnMSG.ui.label_3.setText("please check the account number and try again")			

	def changePin(self):
		global chngpnflg 
		chngpnflg = 0
		global pin0
		mainPin = self.startSys.ui.lineEditoldpin.text()
		if pin0 == mainPin:
			newPin = self.startSys.ui.lineEditnewpin.text()
			if len(newPin) == 4:
				newVrPin = self.startSys.ui.lineEdicnfrmpin.text()
				if newPin == newVrPin:
					self.rtrnMSG.show()
					self.rtrnMSG.ui.label_2.setText("Done")
					self.rtrnMSG.ui.label_4.setText("Pin Changed Successfully")
					self.rtrnMSG.ui.label_3.setText("check the accoount to make sure")
					self.startSys.ui.lineEditnewpin.setText("")
					self.startSys.ui.lineEdicnfrmpin.setText("")
					self.startSys.ui.lineEditoldpin.setText("")
					control.execute("UPDATE bank SET pin = (%s) WHERE pin = (%s)", (newVrPin, pin0,))
					db.commit()
				else:
					self.msBox.show()
					self.msBox.ui.label_2.setText("Error")
					self.msBox.ui.label_4.setText("Pins Don't MAtch")
					self.msBox.ui.label_3.setText("try again please")
					self.startSys.ui.lineEditnewpin.setText("")
					self.startSys.ui.lineEdicnfrmpin.setText("")
					self.startSys.ui.lineEditoldpin.setText("")
			else:
				self.msBox.show()
				self.msBox.ui.label_2.setText("Error")
				self.msBox.ui.label_4.setText("Pin must be 4 digits")
				self.msBox.ui.label_3.setText("try again please")
				self.startSys.ui.lineEditnewpin.setText("")
				self.startSys.ui.lineEdicnfrmpin.setText("")
				self.startSys.ui.lineEditoldpin.setText("")
		else:
			self.msBox.show()
			self.msBox.ui.label_2.setText("Error")
			self.msBox.ui.label_4.setText("Your Pin is not correct")
			self.msBox.ui.label_3.setText("try again please")
			self.startSys.ui.lineEditnewpin.setText("")
			self.startSys.ui.lineEdicnfrmpin.setText("")
			self.startSys.ui.lineEditoldpin.setText("")	
# Arabic		
	def mnwithdrawlAcceptAR(self):
		global balanc
		out0 = self.startSys.ui.outComeLabel_2.text()
		out4 = self.startSys.ui.outComeLabel_3.text()
		text = self.startSys.ui.mostcommonlbl_2.text()
		IntText = int(text)
		if balanc >= IntText:
			if IntText != 0:
				balanc -= IntText
				control.execute("UPDATE bank SET balance = (%s) WHERE card_num = (%s)", (balanc, cardNumber,))
				db.commit()
				self.startSys.ui.balanceLable_2.setText(str(balanc))
				self.startSys.ui.balanceLable_3.setText(str(balanc))
				self.startSys.ui.outComeLabel_2.setText( str(int(text) + int(out0)))  
				self.startSys.ui.outComeLabel_3.setText(str(int(text) + int(out4)))
				self.rtrnMSG.show()
				self.rtrnMSG.ui.label_2.setText("withdrawl Operation is Done")
				self.rtrnMSG.ui.label_4.setText("do wannt to make another Operation ?")
				self.rtrnMSG.ui.label_3.setText("pleae wait for the Cash")
			else:
				self.rtrnMSG.show()
				self.rtrnMSG.ui.label_2.setText("Missing")
				self.rtrnMSG.ui.label_4.setText("please chose the value before making the Operation")
				self.rtrnMSG.ui.label_3.setText("do you want to try again ?")
		else:
			self.rtrnMSG.show()
			self.rtrnMSG.ui.label_2.setText("Error")
			self.rtrnMSG.ui.label_4.setText("There no enaugh Money in your bank account")
			self.rtrnMSG.ui.label_3.setText("do you want to try again ?")

	def withdrawlAcceptAR(self):
		global balanc
		out0 = self.startSys.ui.outComeLabel_2.text()
		out4 = self.startSys.ui.outComeLabel_3.text()
		text = self.startSys.ui.CashValue_2.text()
		if text != '' and text != ' ':
			IntText = int(text)
			if balanc >= IntText:
				if IntText != 0:
					balanc -= IntText
					control.execute("UPDATE bank SET balance = (%s) WHERE card_num = (%s)", (balanc, cardNumber,))
					db.commit()
					self.startSys.ui.balanceLable_2.setText(str(balanc))
					self.startSys.ui.balanceLable_3.setText(str(balanc))
					self.startSys.ui.outComeLabel_2.setText( str(int(text) + int(out0)))  
					self.startSys.ui.outComeLabel_3.setText(str(int(text) + int(out4)))
					self.rtrnMSG.show()
					self.rtrnMSG.ui.label_2.setText("withdrawl Operation is Done")
					self.rtrnMSG.ui.label_4.setText("do wannt to make another Operation ?")
					self.rtrnMSG.ui.label_3.setText("pleae wait for the Cash")
				else:
					self.rtrnMSG.show()
					self.rtrnMSG.ui.label_2.setText("Missing")
					self.rtrnMSG.ui.label_4.setText("please chose the value before making the Operation")
					self.rtrnMSG.ui.label_3.setText("do you want to try again ?")
			else:
				self.rtrnMSG.show()
				self.rtrnMSG.ui.label_2.setText("Error")
				self.rtrnMSG.ui.label_4.setText("There no enaugh Money in your bank account")
				self.rtrnMSG.ui.label_3.setText("do you want to try again ?")
		else:
			self.rtrnMSG.show()
			self.rtrnMSG.ui.label_2.setText("Missing")
			self.rtrnMSG.ui.label_4.setText("please check the amount ")
			self.rtrnMSG.ui.label_3.setText("do you want to try again ?")

	def TrasnferFunAcceptAr(self):
		global balanc
		cardtrnsNm = self.startSys.ui.lineEdit15dgt_2.text()
		cardtrnsMony = self.startSys.ui.lineEditvrfynum_2.text()
		self.startSys.ui.lineEditvrfynum_2.setText("")
		self.startSys.ui.lineEdit15dgt_2.setText("")
		control.execute("SELECT card_num FROM bank")
		cards = control.fetchall()
		card = [i[0] for i in cards]
		if cardtrnsNm in card:
			control.execute("SELECT balance FROM bank WHERE card_num = (%s)", (cardtrnsNm,))
			balanc1 = control.fetchone()
			y, z = int(cardtrnsMony), balanc1[0]
			if balanc >= y:
				balanc -= y
				z += y
				control.execute("UPDATE bank SET balance = (%s) WHERE card_num = (%s)", (z, cardtrnsNm,))
				control.execute("UPDATE bank SET balance = (%s) WHERE card_num = (%s)", (balanc, cardNumber,))
				db.commit()
				self.rtrnMSG.show()
				self.rtrnMSG.ui.label_2.setText("Transfer Operation is Done")
				self.rtrnMSG.ui.label_4.setText("do want to make another Operation ?")
				self.rtrnMSG.ui.label_3.setText("please wait for cash")
				self.startSys.ui.balanceLable_2.setText(str(balanc))
				self.startSys.ui.balanceLable_3.setText(str(balanc))
				self.startSys.ui.outComeLabel_2.setText(cardtrnsMony)
				self.startSys.ui.outComeLabel_3.setText(cardtrnsMony)
			else:
				self.msBox.show()
				self.msBox.ui.label_2.setText("Error")
				self.msBox.ui.label_4.setText("There's no enaugh Money to trasnfer")
				self.msBox.ui.label_3.setText("try again please")
		else:
			self.msBox.show()
			self.msBox.ui.label_2.setText("Error")
			self.msBox.ui.label_4.setText("can't find the account")
			self.msBox.ui.label_3.setText("try again please")

	def depositbuttonacceptAr(self):
		monyvalueenter = self.startSys.ui.lineEditEnterMony_2.text()
		accountNumber = self.startSys.ui.deposit16dgt_2.text()
		global counter
		counter = 0
		self.startSys.ui.progressBar_2.setValue(counter)
		self.rtrnMSG.show()
		self.rtrnMSG.ui.label_2.setText("Deposit done Successfully")
		self.rtrnMSG.ui.label_4.setText("do want to make another Operation ?")
		self.rtrnMSG.ui.label_3.setText("check your account information")
		control.execute("SELECT card_num FROM bank")
		cards = control.fetchall()
		card = [i[0] for i in cards]
		if accountNumber in card:
			control.execute("SELECT balance FROM bank WHERE card_num = (%s)", (accountNumber,))
			balanc2 = control.fetchone()
			x = balanc2[0]
			control.execute("UPDATE bank SET balance = (%s) WHERE card_num = (%s)", (x + int(monyvalueenter), accountNumber,))
			db.commit()
			self.startSys.ui.deposit16dgt_2.setText("")
			self.startSys.ui.lineEditEnterMony_2.setText("")
			self.startSys.ui.labelcheckmony_2.setText("")
		else:
			self.rtrnMSG.show()
			self.rtrnMSG.ui.label_2.setText("Error")
			self.rtrnMSG.ui.label_4.setText("The account number is not correct")			
			self.rtrnMSG.ui.label_3.setText("please check the account number and try again")

	def changePinAr(self):
		global chngpnflg 
		chngpnflg = 0
		global pin0
		mainPin = self.startSys.ui.lineEditoldpin_2.text()
		if pin0 == mainPin:
			newPin = self.startSys.ui.lineEditnewpin_2.text()
			if len(newPin) == 4:
				newVrPin = self.startSys.ui.lineEdicnfrmpin_2.text()
				if newPin == newVrPin:
					self.rtrnMSG.show()
					self.rtrnMSG.ui.label_2.setText("Pin Changed Successfully")
					self.rtrnMSG.ui.label_4.setText("Pido you want to make another Operation")
					self.rtrnMSG.ui.label_3.setText("check your account information")
					self.startSys.ui.lineEditnewpin_2.setText("")
					self.startSys.ui.lineEdicnfrmpin_2.setText("")
					self.startSys.ui.lineEditoldpin_2.setText("")
					control.execute("UPDATE bank SET pin = (%s) WHERE pin = (%s)", (newVrPin, pin0,))
					db.commit()
				else:
					self.msBox.show()
					self.msBox.ui.label_2.setText("Error")
					self.msBox.ui.label_4.setText("Pins Don't MAtch")
					self.msBox.ui.label_3.setText("try again please")
					self.startSys.ui.lineEditnewpin_2.setText("")
					self.startSys.ui.lineEdicnfrmpin_2.setText("")
					self.startSys.ui.lineEditoldpin_2.setText("")
			else:
				self.msBox.show()
				self.msBox.ui.label_2.setText("Error")
				self.msBox.ui.label_4.setText("Pin must be 4 digits")
				self.msBox.ui.label_3.setText("try again please")
				self.startSys.ui.lineEditnewpin_2.setText("")
				self.startSys.ui.lineEdicnfrmpin_2.setText("")
				self.startSys.ui.lineEditoldpin_2.setText("")
		else:
			self.msBox.show()
			self.msBox.ui.label_2.setText("Error")
			self.msBox.ui.label_4.setText("Your Pin is not correct")
			self.msBox.ui.label_3.setText("try again please")
			self.startSys.ui.lineEditnewpin_2.setText("")
			self.startSys.ui.lineEdicnfrmpin_2.setText("")
			self.startSys.ui.lineEditoldpin_2.setText("")
# MSG
	def noAction(self):
		global langue
		global arabic
		global english
		global operation
		global withdrawl
		global deposit
		global pinCounter
		global depositFlag
		global counterFlag
		global counter
		global cardType
		global chngpnflg
		chngpnflg = 0
		cardType = 0
		counter = 0
		langue = False
		arabic = False
		english = False
		operation = False 
		withdrawl = False
		deposit = False
		pinCounter = 0
		depositFlag = False  # to chick if it's deposit or cashwithdrawl
		counterFlag = 1
		self.startSys.ui.HomeStack.setCurrentIndex(0)
		self.startSys.ui.stackedWidget_3.setCurrentIndex(1)
		self.startSys.ui.stackedWidget_2.setCurrentIndex(1)
		self.startSys.ui.cardvalue.setText("")
		self.startSys.ui.cardvalue_2.setText("")
		self.startSys.ui.pinvalue_2.setText("")
		self.startSys.ui.pinvalue.setText("")
		self.startSys.ui.pineeror.setText("")
		self.startSys.ui.pineeror_2.setText("")
		self.startSys.ui.CashValue.setText("")
		self.startSys.ui.CashValue_2.setText("")
		self.startSys.ui.mostcommonlbl.setText("0")
		self.startSys.ui.mostcommonlbl_2.setText("0")
		self.startSys.ui.lineEditEnterMony_2.setText("")
		self.startSys.ui.lineEditEnterMony.setText("")
		self.startSys.ui.deposit16dgt.setText("")
		self.startSys.ui.deposit16dgt_2.setText("")
		self.startSys.ui.balanceLable.setText("0")
		self.startSys.ui.balanceLable_2.setText("0")
		self.startSys.ui.balanceLable_3.setText("0")
		self.startSys.ui.balanceLable_3.setText("0")
		self.startSys.ui.outComeLabel.setText("0")
		self.startSys.ui.outComeLabel_2.setText("0")
		self.startSys.ui.outComeLabel_3.setText("0")
		self.startSys.ui.outComeLabel_4.setText("0")
		self.startSys.ui.NameLAbel.setText("Card Owner")
		self.startSys.ui.NameLAbel_2.setText("Card Owner")
		self.startSys.ui.NumberLbl.setText("0000 0000 0000 0000")
		self.startSys.ui.NumberLbl_2.setText("0000 0000 0000 0000")
		self.startSys.ui.label_11.setText("card Type")
		self.startSys.ui.label_48.setText("card Type")
		self.startSys.ui.labelcheckmony.setText("")
		self.startSys.ui.labelcheckmony_2.setText("")
		self.startSys.ui.cashWithdrawal.setStyleSheet("QPushButton{\n"
			"color: rgb(98, 119, 144);\n"
			"/*color: rgb(39, 49, 74);*/\n"
			"border:0px;\n"
			"    font: 18pt \"MS Shell Dlg 2\";\n"
			"Text-align:left;\n"
			"}\n"
			"QPushButton:hover{\n"
			"color: rgb(255, 255, 255);\n"
			"    border:1px solid rgb(98, 119, 144);\n"
			"    border-radius:5px;\n"
			"    background-color: rgb(98, 119, 144);\n"
			"    font: 20pt \"MS Shell Dlg 2\";\n"
			"\n"
			"}")
		self.startSys.ui.ChangePINbtn.setStyleSheet("QPushButton{\n"
			"color: rgb(98, 119, 144);\n"
			"/*color: rgb(39, 49, 74);*/\n"
			"border:0px;\n"
			"    font: 18pt \"MS Shell Dlg 2\";\n"
			"Text-align:left;\n"
			"}\n"
			"QPushButton:hover{\n"
			"color: rgb(255, 255, 255);\n"
			"    border:1px solid rgb(98, 119, 144);\n"
			"    border-radius:5px;\n"
			"    background-color: rgb(98, 119, 144);\n"
			"    font: 20pt \"MS Shell Dlg 2\";\n"
			"\n"
			"}")
		self.startSys.ui.depositbtn.setStyleSheet("QPushButton{\n"
			"color: rgb(98, 119, 144);\n"
			"/*color: rgb(39, 49, 74);*/\n"
			"border:0px;\n"
			"    font: 18pt \"MS Shell Dlg 2\";\n"
			"Text-align:left;\n"
			"}\n"
			"QPushButton:hover{\n"
			"color: rgb(255, 255, 255);\n"
			"    border:1px solid rgb(98, 119, 144);\n"
			"    border-radius:5px;\n"
			"    background-color: rgb(98, 119, 144);\n"
			"    font: 20pt \"MS Shell Dlg 2\";\n"
			"\n"
			"}")
		self.startSys.ui.pushButton_6.setStyleSheet("QPushButton{\n"
			"color: rgb(98, 119, 144);\n"
			"/*color: rgb(39, 49, 74);*/\n"
			"border:0px;\n"
			"    font: 18pt \"MS Shell Dlg 2\";\n"
			"Text-align:left;\n"
			"}\n"
			"QPushButton:hover{\n"
			"color: rgb(255, 255, 255);\n"
			"    border:1px solid rgb(98, 119, 144);\n"
			"    border-radius:5px;\n"
			"    background-color: rgb(230, 126, 34);\n"
			"    font: 20pt \"MS Shell Dlg 2\";\n"
			"\n"
			"}")
		self.startSys.ui.cashWithdrawal_2.setStyleSheet("QPushButton{\n"
			"color: rgb(98, 119, 144);\n"
			"/*color: rgb(39, 49, 74);*/\n"
			"border:0px;\n"
			"    font: 18pt \"MS Shell Dlg 2\";\n"
			"Text-align:left;\n"
			"}\n"
			"QPushButton:hover{\n"
			"color: rgb(255, 255, 255);\n"
			"    border:1px solid rgb(98, 119, 144);\n"
			"    border-radius:5px;\n"
			"    background-color: rgb(98, 119, 144);\n"
			"    font: 20pt \"MS Shell Dlg 2\";\n"
			"\n"
			"}")
		self.startSys.ui.ChangePINbtn_2.setStyleSheet("QPushButton{\n"
			"color: rgb(98, 119, 144);\n"
			"/*color: rgb(39, 49, 74);*/\n"
			"border:0px;\n"
			"    font: 18pt \"MS Shell Dlg 2\";\n"
			"Text-align:left;\n"
			"}\n"
			"QPushButton:hover{\n"
			"color: rgb(255, 255, 255);\n"
			"    border:1px solid rgb(98, 119, 144);\n"
			"    border-radius:5px;\n"
			"    background-color: rgb(98, 119, 144);\n"
			"    font: 20pt \"MS Shell Dlg 2\";\n"
			"\n"
			"}")
		self.startSys.ui.depositbtn_2.setStyleSheet("QPushButton{\n"
			"color: rgb(98, 119, 144);\n"
			"/*color: rgb(39, 49, 74);*/\n"
			"border:0px;\n"
			"    font: 18pt \"MS Shell Dlg 2\";\n"
			"Text-align:left;\n"
			"}\n"
			"QPushButton:hover{\n"
			"color: rgb(255, 255, 255);\n"
			"    border:1px solid rgb(98, 119, 144);\n"
			"    border-radius:5px;\n"
			"    background-color: rgb(98, 119, 144);\n"
			"    font: 20pt \"MS Shell Dlg 2\";\n"
			"\n"
			"}")
		self.startSys.ui.depositbtn_3.setStyleSheet("QPushButton{\n"
			"color: rgb(98, 119, 144);\n"
			"/*color: rgb(39, 49, 74);*/\n"
			"border:0px;\n"
			"    font: 18pt \"MS Shell Dlg 2\";\n"
			"Text-align:left;\n"
			"}\n"
			"QPushButton:hover{\n"
			"color: rgb(255, 255, 255);\n"
			"    border:1px solid rgb(98, 119, 144);\n"
			"    border-radius:5px;\n"
			"    background-color: rgb(230, 126, 34);\n"
			"    font: 20pt \"MS Shell Dlg 2\";\n"
			"\n"
			"}")
		self.rtrnMSG.close()

if __name__== "__main__":
	app = QApplication(sys.argv)
	window = StartClass()
	sys.exit(app.exec_())

