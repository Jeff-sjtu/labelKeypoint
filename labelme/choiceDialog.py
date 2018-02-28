#
# Copyright (C) 2011 Michael Pitidis, Hussein Abdulwahid.
#
# This file is part of Labelme.
#
# Labelme is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Labelme is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Labelme.  If not, see <http://www.gnu.org/licenses/>.
#

try:
    from PyQt5.QtGui import *
    from PyQt5.QtCore import *
    from PyQt5.QtWidgets import *
    PYQT5 = True
except ImportError:
    from PyQt4.QtGui import *
    from PyQt4.QtCore import *
    PYQT5 = False

from .lib import newIcon, labelValidator

# TODO:
# - Calculate optimal position so as not to go out of screen area.

BB = QDialogButtonBox
#BB = QRadioButton

class ChoiceDialog(QDialog):

    def __init__(self, text="Choose object label", parent=None):
        super(ChoiceDialog, self).__init__(parent)
        self.edit = QLineEdit()
        self.edit.setText(text)
        self.edit.setEnabled(False)
        self.edit.setValidator(labelValidator())
        self.edit.editingFinished.connect(self.postProcess)
        layout = QVBoxLayout()
        layout.addWidget(self.edit)
        self.buttonBox = bb = BB(BB.Save | BB.Ok | BB.Cancel | BB.Discard , Qt.Horizontal, self)
        #bb.button(BB.Ok).setIcon(newIcon('done'))
        #bb.button(BB.Cancel).setIcon(newIcon('undo'))
        bb.button(BB.Ok).setText('Head')
        bb.button(BB.Discard).setText('Empty')
        bb.button(BB.Save).setText('Neck')
        bb.button(BB.Cancel).setIcon(newIcon('undo'))

        bb.button(BB.Ok).clicked.connect(self.head)
        bb.button(BB.Discard).clicked.connect(self.empty)
        bb.button(BB.Save).clicked.connect(self.neck)

        bb.accepted.connect(self.validate)
        bb.rejected.connect(self.reject)
        layout.addWidget(bb)
        self.setLayout(layout)

    def head(self):
        self.edit.setText('Head')
        self.accept()

    def empty(self):
        self.edit.setText('Empty')
        self.accept()

    def neck(self):
        self.edit.setText('Neck')
        self.accept()

    def validate(self):
        if PYQT5:
            if self.edit.text().strip():
                self.accept()
        else:
            if self.edit.text().trimmed():
                self.accept()

    def postProcess(self):
        if PYQT5:
            self.edit.setText(self.edit.text().strip())
        else:
            self.edit.setText(self.edit.text().trimmed())

    def popUp(self, text='', move=True):
        self.edit.setText(text)
        self.edit.setSelection(0, len(text))
        self.edit.setFocus(Qt.PopupFocusReason)
        if move:
            self.move(QCursor.pos())
        return self.edit.text() if self.exec_() else None
