"""
   This module provides a class library for a GUI label field widget bound to an Epics PV. The PV is monitored
   and the field is updated when the PV changes

Author:         Hugo Slepicka
Created:        Apr. 20, 2014
Modifications:
"""

import time

from epics import PV
from qtpy import QtCore, QtWidgets


class QtEpicsMotorWidget(QtWidgets.QWidget):
    """
    This module provides a class library for a GUI label field widget bound to an Epics PV. The PV is monitored
    and the field is updated when the PV changes

    """

    changeColor = QtCore.Signal(str)

    def __init__(self, pvname, parent, input_width, precision=2, editable=False):
        """

        Inputs:
           pvname:
              The name of the epics process variable.
           parent:
              The container to place the entry widget.
           input_width:
           precision:
           highlight_on_change:

        Example:
          detstat_file = epicsPVLabel("x12c_comm:datafilename",filestat_frame,70)
          detstat_file.getEntry().pack(side=LEFT,fill=X,expand=YES)


        """
        super(QtEpicsMotorWidget, self).__init__()
        self.precision = precision
        self.editable = editable
        # self.applyOnEnter = applyOnEnter
        self.entry_var = ""

        # Creates the PV
        self.entry_pv = PV(pvname + ".RBV", connection_callback=self._conCB)
        self.base_pv = PV(pvname)

        if self.editable:
            self.entry = QtWidgets.QLineEdit(parent)
        else:
            self.entry = QtWidgets.QLabel(parent)

        if input_width != 0:
            self.entry.setFixedWidth(input_width)
        time.sleep(0.05)

        try:  # because the connection CB handles the timeout for PVs that don't exist
            self._set_entry_var_with_precision(self.entry_pv.get())
            self.entry.setText(self.entry_var)
        except Exception:
            self.entry_var = "-----"
            self.entry.setText(self.entry_var)
            self.changeColor.emit("white")
            return

        self.changeColor.connect(self.setColor)
        self.entry_pv.add_callback(self._entry_pv_movingCb)
        self.entry_dmov_pv = PV(pvname + ".DMOV")
        self.entry_dmov_pv.add_callback(self._entry_pv_dmovCb)

    def _conCB(self, conn, **kwargs):

        if conn:
            self.changeColor.emit("blue")
        else:
            self.entry_var = "-----"
            self.entry.setText(self.entry_var)
            self.changeColor.emit("white")

    def _entry_pv_movingCb(self, value, **kwargs):
        self._set_entry_var_with_precision(value)
        self.entry.setText(self.entry_var)

    def _entry_pv_dmovCb(self, value, **kwargs):
        if value == 1:
            self.changeColor.emit("None")
        else:
            self.changeColor.emit("yellow")

    def _set_entry_var_with_precision(self, inval):
        try:
            val = float(inval)
            if self.precision == 0:
                self.entry_var = "%.0f" % val
            elif self.precision == 1:
                self.entry_var = "%.1f" % val
            elif self.precision == 2:
                self.entry_var = "%.2f" % val
            elif self.precision == 3:
                self.entry_var = "%.3f" % val
            elif self.precision == 4:
                self.entry_var = "%.4f" % val
            else:
                self.entry_var = "%.5f" % val
        except TypeError:
            # TODO: check this waveform_to_string function
            self.entry_var = "Type Error"  # waveform_to_string(inval)
            pass
        except ValueError:
            # TODO: check this waveform_to_string function
            self.entry_var = "Value Error"  # waveform_to_string(inval)
            pass

    def getEntry(self):
        return self.entry

    def getBasePV(self):
        return self.base_pv

    def getField(self):
        return self.entry_var

    def setField(self, value):
        self.entry_var = value

    def setColor(self, color_s="pink"):
        self.entry.setStyleSheet("background-color: %s;" % color_s)
