from PySide2 import QtCore, QtWidgets, QtUiTools, QtGui
from maya import OpenMayaUI as omui
from shiboken2 import wrapInstance
import subprocess
import maya.cmds as mc
#import pymel.core as pm
import os

ptr = omui.MQtUtil.mainWindow()
parentWindow = wrapInstance(int(ptr), QtWidgets.QMainWindow)

mapGeneratorFile = r'C:\Users\Mohammed\Documents\Python\hair utility map tool\randomMapGenerator.py'
defaultImage = r'C:\Users\Mohammed\Documents\Python\hair utility map tool\profilePic_400x400.jpg'
savedMapFile = r'C:\Users\Mohammed\Documents\Python\hair utility map tool\randomMap.jpg'


class HumpUiTool(QtWidgets.QDialog):
    uiInstance = None

    @classmethod
    def loadUI(cls):
        if not cls.uiInstance:
            cls.uiInstance = HumpUiTool()

        if cls.uiInstance.isHidden():
            cls.uiInstance.show()
        else:
            cls.uiInstance.raise_()
            cls.uiInstance.activateWindow()

        pass

    def __init__(self, parent=parentWindow):
        super(HumpUiTool, self).__init__(parent)

        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self)
        self.verticalLayout_2.setContentsMargins(15, -1, 15, -1)

        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.verticalLayout.setContentsMargins(-1, -1, 0, -1)

        self.noisePixMap = QtGui.QPixmap(defaultImage)
        pixMapResize = self.noisePixMap.scaled(300, 300, aspectMode=QtCore.Qt.KeepAspectRatio,
                                               mode=QtCore.Qt.FastTransformation)

        self.noiseLabel = QtWidgets.QLabel()
        self.noiseLabel.setPixmap(pixMapResize)

        self.verticalLayout.addWidget(self.noiseLabel)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        self.verticalLayout_5 = QtWidgets.QVBoxLayout()

        self.horizontalLayout = QtWidgets.QHBoxLayout()

        spacerItem = QtWidgets.QSpacerItem(67, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)

        # 0% Label --------------------------------------------------------------------------------------
        self.label = QtWidgets.QLabel('0%')
        self.horizontalLayout.addWidget(self.label)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)

        # 100% Label --------------------------------------------------------------------------------------
        self.label_2 = QtWidgets.QLabel('100%')
        self.horizontalLayout.addWidget(self.label_2)
        self.verticalLayout_5.addLayout(self.horizontalLayout)

        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setContentsMargins(0, -1, 0, -1)

        # LCD Widget --------------------------------------------------------------------------------------
        self.percentSliderNumber = QtWidgets.QLCDNumber()
        self.percentSliderNumber.setSegmentStyle(QtWidgets.QLCDNumber.Flat)
        self.horizontalLayout_4.addWidget(self.percentSliderNumber)

        # Percentage Slider --------------------------------------------------------------------------------------
        self.percentSlider = QtWidgets.QSlider()
        self.percentSlider.setMaximum(100)
        self.percentSlider.setSingleStep(True)
        self.percentSlider.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalLayout_4.addWidget(self.percentSlider)

        self.verticalLayout_5.addLayout(self.horizontalLayout_4)
        self.verticalLayout_2.addLayout(self.verticalLayout_5)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()

        # Generate Button --------------------------------------------------------------------------------------
        self.generatepushButton = QtWidgets.QPushButton('Generate')
        self.horizontalLayout_2.addWidget(self.generatepushButton)

        spacerItem2 = QtWidgets.QSpacerItem(32, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)

        # Apply Button--------------------------------------------------------------------------------------
        self.horizontalLayout_2.addItem(spacerItem2)
        self.applyPushButton = QtWidgets.QPushButton('Apply')
        self.horizontalLayout_2.addWidget(self.applyPushButton)

        # Load Attributes Label --------------------------------------------------------------------------------------
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.label_5 = QtWidgets.QLabel('select XGen description and press Load Attributes')
        self.verticalLayout_3.addWidget(self.label_5)

        # Load Attributes Button--------------------------------------------------------------------------------------
        self.loadAttributesPushButton = QtWidgets.QPushButton('Load Attributes')
        self.loadAttributesPushButton.clicked.connect(self.loadAttributesButtonPressed)
        self.verticalLayout_3.addWidget(self.loadAttributesPushButton)

        # clear List button Layout setup
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.dispModListLineEdit = QtWidgets.QLineEdit('shows selected Modifier')
        self.dispModListLineEdit.setDisabled(True)


        self.clearListpushButton = QtWidgets.QPushButton('clear list')

        self.horizontalLayout_7.addWidget(self.dispModListLineEdit)
        self.horizontalLayout_7.addWidget(self.clearListpushButton)
        self.verticalLayout_3.addLayout(self.horizontalLayout_7)

        self.verticalLayout_2.addLayout(self.verticalLayout_3)
        spacerItem3 = QtWidgets.QSpacerItem(20, 5, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.verticalLayout_2.addItem(spacerItem3)

        # Choose XGen Attr to Modify Label--------------------------------------------------------------------------------------
        self.label_4 = QtWidgets.QLabel('Choose XGen attribute  ato modify:')
        self.verticalLayout_2.addWidget(self.label_4)

        # List Widget--------------------------------------------------------------------------------------
        self.listWidget = QtWidgets.QListWidget()
        self.listWidget.itemClicked.connect(self.widgetItemPressed)
        self.verticalLayout_2.addWidget(self.listWidget)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()

        self.label_3 = QtWidgets.QLabel('choose folder to save generated map')

        self.horizontalLayout_6.addWidget(self.label_3)
        self.verticalLayout_2.addLayout(self.horizontalLayout_6)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()

        self.saveFilePushButton = QtWidgets.QPushButton()
        self.saveFilePushButton.setIcon(QtGui.QIcon(':fileOpen'))

        self.horizontalLayout_3.addWidget(self.saveFilePushButton)
        self.saveFolderlineEdit = QtWidgets.QLineEdit()

        self.horizontalLayout_3.addWidget(self.saveFolderlineEdit)
        self.verticalLayout_2.addLayout(self.horizontalLayout_3)
        self.setMinimumWidth(330)
        self.setMaximumWidth(330)
        self.connections()
        self.attributeVariable = None
        self.saveFolderDirectory = None
        self.selectedModifierAttr = None
        self.selectedObject = None
        self.mapGenerated = False

    def connections(self):
        self.percentSlider.valueChanged.connect(self.updateLcdDisplay)
        self.generatepushButton.clicked.connect(self.generateImage)
        self.saveFilePushButton.clicked.connect(self.saveFileButtonPressed)
        self.applyPushButton.clicked.connect(self.applyButtonPressed)
        self.clearListpushButton.clicked.connect(self.clearModifierList)


    def clearModifierList(self):
        self.listWidget.clear()

    def generateImage(self, slider_value='hello'):
        """this function runs an external map generation program responsible for generating
        the noise map. It takes the value of the percentage slider and
        passes it as an argument to the external program to determine how the map
        is generated"""

        slider_value = self.percentSlider.value()
        externalMapGeneration = subprocess.check_output(['python', mapGeneratorFile, '--perVal', '{}'.format(
            slider_value), '--mapFile', '{}'.format(savedMapFile)])  # , stderr=subprocess.PIPE, stdout=subprocess.PIPE)

        self.noisePixMap.load(savedMapFile)
        pixMapResize = self.noisePixMap.scaled(300, 300, aspectMode=QtCore.Qt.KeepAspectRatio,
                                               mode=QtCore.Qt.FastTransformation)
        # the map is generated and stored in the savedMapFile Variable
        # which is then rescaled and then used to update the Label Widget that displays it to the UI
        self.generatedNoiseMap = QtGui.QPixmap(savedMapFile)
        rescaledNoiseMap = self.generatedNoiseMap.scaled(300, 300, aspectMode=QtCore.Qt.KeepAspectRatio,
                                                         mode=QtCore.Qt.FastTransformation)

        self.noiseLabel.setPixmap(rescaledNoiseMap)


        self.mapGenerated = True

    def updateLcdDisplay(self, slider_value):
        self.percentSliderNumber.display(slider_value)

    def saveFileButtonPressed(self):
        self.initialDirectory = r'C:\Users\Mohammed\Documents\Python'
        self.saveFolderDirectory = QtWidgets.QFileDialog.getExistingDirectory()
        # shows a greyed-out string of the directory chosen
        self.saveFolderlineEdit.setText(self.saveFolderDirectory)
        self.saveFolderlineEdit.setDisabled(True)

    def loadAttributesButtonPressed(self):
        '''This function takes an Xgen shape oject or a modifier of the Xgen
         shape and returns a list of attributes
        that textures could be plugged into'''
        # check if  selection is an xgen shape or modifier
        self.selectedObject = mc.ls(selection=True)
        if len(self.selectedObject) <= 0:
            print('No item selected')
            return
        # check if selected item is an xgen modifier
        for selItems in self.selectedObject:
            if 'xgm' not in mc.nodeType(selItems):
                print('please select Xgen modifier')
                return
            else:
                print('xgen item selected')

        self.xGenAttributes = mc.listAttr(self.selectedObject[0], k=True)
        self.listWidgetSetup(self.xGenAttributes)
        self.dispModListLineEdit.setText(self.selectedObject[0])

    def listWidgetSetup(self, xGenAttr):
        # Set visual Properties of the text in the ListWidget Items
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setFamily('Helvetica light')
        self.listWidget.setFont(font)

        # add items to list widget
        self.listWidget.clear()
        self.listWidget.addItems(xGenAttr)

    def widgetItemPressed(self, clickedItem):
        self.selectedModifierAttr = clickedItem.text()
        print(self.selectedModifierAttr)
        # set attribute for selected list widget item

    def applyButtonPressed(self):

        # list attributes of selection
        if not self.saveFolderDirectory :
            print('No save folder selected. please choose folder')
            return

        elif self.mapGenerated == False:
            print('no map generated, please generate map')

        elif not self.selectedObject:
            print('No Xgen Attribute selected please load and select an Xgen attribute' )
            return

        else:
            modifierName = self.selectedObject[0]
            modifierAttr = self.selectedModifierAttr
            self.nodeName = 'noiseMap_{}_{}'.format(modifierName, modifierAttr)

            self.connectTexturetoModifier(modifierName, modifierAttr,self.nodeName)


    def connectTexturetoModifier(self, mod_name, mod_attr, node_name):
        ''' This function creates and connects the file Node that holds the
        generated noise texture. It first checks if a file Node for the selected
        modifier exist, and creates one for it
        item'''
        if not self.mapGenerated :
            print('please first select attribute then press generate to apply noise')
            return

        if self.selectedModifierAttr == None :
            print('please load and select a single Attribute')
            return


        renamedSavedMap = r'{}\{}.jpg'.format(self.saveFolderDirectory,node_name)
        if os.path.exists(renamedSavedMap):
            os.remove(renamedSavedMap)
        if not savedMapFile:
            print('please press the generate button to proceed')
            return
        os.rename(savedMapFile,renamedSavedMap)
        # print('testing{}'.format(node_name))
        # create File Node
        # But first check if file Node exists, if it does, delete it and create a new one(i.e replace it)
        try:
            if mc.objExists(self.fileNode):
                print('try block ran, fileNode exists or error occured. moving on')
                mc.setAttr('{}.{}'.format(node_name,'fileTextureName'), renamedSavedMap, type='string')


        except:
            self.fileNode = mc.shadingNode('file', name=node_name, asTexture=True)
            print('except block ran. node object created for the first time')
            mc.setAttr('{}.{}'.format(node_name, 'fileTextureName'), renamedSavedMap, type='string')

        mc.connectAttr('{}.{}'.format(self.fileNode, 'outAlpha'), '{}.{}'.format(mod_name, mod_attr), f=True)



        self.mapGenerated = False


        # connects the created FileNodes out Alpha(fileNode.outAlpha to the selected xgen modifier attribute
        # (e.g NoiseModifier.Frequency or NoiseModifier.Magnitude)

        # print('connect command done')




    def testWidgets(self, value):
        print(value.text())


# HumpUiTool.loadUI()


try:
    ui.close()
    ui.deleteLater()

except:
    pass
ui = HumpUiTool()
ui.show()


