import copy

import PySide2
from PySide2 import QtGui, QtWidgets, QtCore
from PySide2.QtWidgets import QLabel, QPushButton, QFrame, QSizePolicy
import algorithmes.resolution.dpll, global_module, algorithmes.resolution.cdcl_SN3.cdcl
import networkx
import matplotlib.pyplot
from grave import plot_network
from grave.style import use_attributes

globals()['state'] = 0
globals()['titleBar'] = True

class TopUi(QFrame):
    def __init__(self, parent, appelant):
        super().__init__(parent)

        self.mainWindow = appelant

        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)

        sizePolicy1 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Expanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)

        # Barres superieur
        vbox_barresSup = QtWidgets.QVBoxLayout()


        # BARRE DES ACTIONS :

        barreDActions_frame = QFrame()
        barreDActions_frame.setObjectName("barreDActions_frame")
        barreDActions_frame.setFrameShape(QFrame.NoFrame)
        barreDActions_frame.setMinimumHeight(35)

        self.execution = QPushButton()
        self.execution.setMaximumWidth(35)
        self.execution.setMinimumHeight(35)
        self.execution.setObjectName("execution")
        self.execution.clicked.connect(self.executer)

        self.execution_pas_a_pas = QPushButton()
        self.execution_pas_a_pas.setMaximumWidth(35)
        self.execution_pas_a_pas.setMinimumHeight(35)
        self.execution_pas_a_pas.setObjectName("execution_pas_a_pas")

        box_boutons_action = QtWidgets.QHBoxLayout()
        box_boutons_action.setContentsMargins(0, 0, 0, 0)
        box_boutons_action.setSpacing(0)

        box_boutons_action.addWidget(self.execution)
        box_boutons_action.addWidget(self.execution_pas_a_pas)

        frame_boutons_action = QFrame()
        frame_boutons_action.setLayout(box_boutons_action)
        frame_boutons_action.setMaximumWidth(70)

        frame_ba_complement = QFrame()

        hbox_actions = QtWidgets.QHBoxLayout()
        hbox_actions.setContentsMargins(0, 0, 0, 0)
        hbox_actions.setSpacing(0)

        hbox_actions.addWidget(frame_ba_complement)
        hbox_actions.addWidget(frame_boutons_action)

        barreDActions_frame.setLayout(hbox_actions)
        vbox_barresSup.addWidget(barreDActions_frame)
        vbox_barresSup.setStretch(-1, 1)

        # FIN DE LA BARRE D'ACTIONS

        # Unification de la barre des titres et de la barre d'actions

        vbox_barresSup.setContentsMargins(0, 0, 0, 0)                       # Configuration du layout
        vbox_barresSup.setSpacing(0)

        self.frame_barresSup = QFrame()                                     # Enrobage dans une frame
        self.frame_barresSup.setObjectName("frame_barresSup")
        self.frame_barresSup.setFrameShape(QFrame.NoFrame)
        self.frame_barresSup.setObjectName("frame_barresSup")
        self.frame_barresSup.setLayout(vbox_barresSup)

        # FIN

        # Controle du menu toggle
        button_toggle_menu = QPushButton()
        button_toggle_menu.setObjectName("button_toggle_menu")

        button_toggle_menu.clicked.connect(lambda: self.toggleMenu(250))

        button_toggle_menu.setSizePolicy(sizePolicy)
        sizePolicy.setHeightForWidth(button_toggle_menu.sizePolicy().hasHeightForWidth())

        box_toggle_menu = QtWidgets.QGridLayout()                           # Enrobage du boutton dans une box
        box_toggle_menu.addWidget(button_toggle_menu)

        box_toggle_menu.setContentsMargins(0, 0, 0, 0)                      # Configuration du layout
        box_toggle_menu.setSpacing(0)

        frame_toggle_menu = QFrame()                                        # Enrobage du boutton dans une frame
        frame_toggle_menu.setFrameShape(QFrame.NoFrame)
        frame_toggle_menu.setLayout(box_toggle_menu)

        frame_toggle_menu.setMinimumSize(QtCore.QSize(0, 0))
        frame_toggle_menu.setMaximumSize(QtCore.QSize(70, 70))

        # Unification
        hbox_uiSup = QtWidgets.QHBoxLayout()
        hbox_uiSup.addWidget(frame_toggle_menu)
        hbox_uiSup.addWidget(self.frame_barresSup)

        hbox_uiSup.setContentsMargins(0, 0, 0, 0)                           # Configuration du layout unifié
        hbox_uiSup.setSpacing(0)


        self.setLayout(hbox_uiSup)

        self.setMinimumSize(QtCore.QSize(0, 100))

        self.setFrameShape(QFrame.NoFrame)

    def toggleMenu(self, maxWidth):
        width = self.mainWindow.trameinf.barreLater_frame.width()
        maxExtend = maxWidth
        standard = 70

        # SET MAX WIDTH
        if width == 70:
            widthExtended = maxExtend
            self.mainWindow.trameinf.home_button.setText("Home")
            self.mainWindow.trameinf.affichage_principal.setText("Show")
            self.mainWindow.trameinf.parametres.setText("Parametres")
            """self.mainWindow.trameinf.algorithmes.setText("Algorithmes")
            self.mainWindow.trameinf.heuristiques.setText("Heuristiques")"""
        else:
            widthExtended = standard
            self.mainWindow.trameinf.home_button.setText("")
            self.mainWindow.trameinf.affichage_principal.setText("")
            self.mainWindow.trameinf.parametres.setText("")
            """self.mainWindow.trameinf.algorithmes.setText("")
            self.mainWindow.trameinf.heuristiques.setText("")"""

        self.animation = QtCore.QPropertyAnimation(self.mainWindow.trameinf.barreLater_frame, b"minimumWidth")
        self.animation.setDuration(300)
        self.animation.setStartValue(width)
        self.animation.setEndValue(widthExtended)
        self.animation.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
        self.animation.start()

    def mousePressEvent(self, event):
        self.start = self.mapToGlobal(event.pos())
        self.pressing = True

    def mouseMoveEvent(self, event):
        if self.pressing:
            self.end = self.mapToGlobal(event.pos())
            self.movement = self.end - self.start
            self.mainWindow.setGeometry(self.mapToGlobal(self.movement).x(),
                                      self.mapToGlobal(self.movement).y(),
                                      self.mainWindow.width(),
                                      self.mainWindow.height())
            self.start = self.end

    def mouseReleaseEvent(self, event: PySide2.QtGui.QMouseEvent):
        self.pressing = False

    def btn_close_clicked(self):
        self.mainWindow.close()

    def maximize_restore_clicked(self):
        status = globals()['state']
        if status == 0:
            self.mainWindow.showMaximized()
            globals()['state'] = 1
            self.btn_maximize_restore.setToolTip("Restore")
            self.btn_maximize_restore.setIcon(QtGui.QIcon(u":/16x16/icons/16x16/cil-window-restore.png"))
        else:
            self.mainWindow.showNormal()
            globals()['state'] = 0
            self.btn_maximize_restore.setToolTip("Maximize")
            self.btn_maximize_restore.setIcon(QtGui.QIcon(u":/16x16/icons/16x16/cil-window-maximize.png"))

    def btn_min_clicked(self):
        self.mainWindow.showMinimized()

    def executer(self):
        global formule
        global sdp
        global algorithmes
        #if al
        if global_module.algo_dico['dpll'] == True:
            algorithmes.resolution.dpll.dpll(copy.deepcopy(global_module.formule))
        if global_module.algo_dico['cdcl'] == True:
            algorithmes.resolution.cdcl_SN3.cdcl.cdcl(copy.deepcopy(global_module.formule))
        print(global_module.sdp)
        #self.mainWindow.trameinf.frame_principale.affichage.sdp.append(global_module.sdp.__str__())

        """art = plot_network(global_module.graph, ax=global_module.ax, node_style=use_attributes(),
                           edge_style=use_attributes())"""
        #matplotlib.pyplot.show()

        self.mainWindow.trameinf.frame_principale.affichage.creation()