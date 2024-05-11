import sys

if "PyQt5" in sys.modules:
    from PyQt5 import QtCore, QtWidgets, QtGui
    from PyQt5.QtCore import Qt, pyqtSignal as Signal

else:
    from PySide2 import QtCore, QtWidgets, QtGui
    from PySide2.QtCore import Signal, Qt


class RangeSlider(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.first_position = 1
        self.second_position = 8

        self.opt = QtWidgets.QStyleOptionSlider()
        self.opt.minimum = 0
        self.opt.maximum = 10

        self.setTickPosition(QtWidgets.QSlider.TicksAbove)
        self.setTickInterval(1)

        self.setSizePolicy(
            QtWidgets.QSizePolicy(
                QtWidgets.QSizePolicy.Expanding,
                QtWidgets.QSizePolicy.Fixed,
                QtWidgets.QSizePolicy.Slider,
            )
        )

    def setRangeLimit(self, minimum: int, maximum: int):
        self.opt.minimum = minimum
        self.opt.maximum = maximum

    def setRange(self, start: int, end: int):
        self.first_position = start
        self.second_position = end

    def getRange(self):
        return (self.first_position, self.second_position)

    def setTickPosition(self, position: QtWidgets.QSlider.TickPosition):
        self.opt.tickPosition = position

    def setTickInterval(self, ti: int):
        self.opt.tickInterval = ti

    def paintEvent(self, event: QtGui.QPaintEvent):

        painter = QtGui.QPainter(self)

        # Draw rule
        self.opt.initFrom(self)
        self.opt.rect = self.rect()
        self.opt.sliderPosition = 0
        self.opt.subControls = (
            QtWidgets.QStyle.SC_SliderGroove | QtWidgets.QStyle.SC_SliderTickmarks
        )

        #   Draw GROOVE
        self.style().drawComplexControl(QtWidgets.QStyle.CC_Slider, self.opt, painter)

        #  Draw INTERVAL

        color = self.palette().color(QtGui.QPalette.Highlight)
        color.setAlpha(160)
        painter.setBrush(QtGui.QBrush(color))
        painter.setPen(Qt.NoPen)

        self.opt.sliderPosition = self.first_position
        x_left_handle = (
            self.style()
            .subControlRect(
                QtWidgets.QStyle.CC_Slider, self.opt, QtWidgets.QStyle.SC_SliderHandle
            )
            .right()
        )

        self.opt.sliderPosition = self.second_position
        x_right_handle = (
            self.style()
            .subControlRect(
                QtWidgets.QStyle.CC_Slider, self.opt, QtWidgets.QStyle.SC_SliderHandle
            )
            .left()
        )

        groove_rect = self.style().subControlRect(
            QtWidgets.QStyle.CC_Slider, self.opt, QtWidgets.QStyle.SC_SliderGroove
        )

        selection = QtCore.QRect(
            x_left_handle,
            groove_rect.y(),
            x_right_handle - x_left_handle,
            groove_rect.height(),
        ).adjusted(-1, 1, 1, -1)

        painter.drawRect(selection)

        # Draw first handle

        self.opt.subControls = QtWidgets.QStyle.SC_SliderHandle
        self.opt.sliderPosition = self.first_position
        self.style().drawComplexControl(QtWidgets.QStyle.CC_Slider, self.opt, painter)

        # Draw second handle
        self.opt.sliderPosition = self.second_position
        self.style().drawComplexControl(QtWidgets.QStyle.CC_Slider, self.opt, painter)

    def mousePressEvent(self, event: QtGui.QMouseEvent):

        self.opt.sliderPosition = self.first_position
        self._first_sc = self.style().hitTestComplexControl(
            QtWidgets.QStyle.CC_Slider, self.opt, event.pos(), self
        )

        self.opt.sliderPosition = self.second_position
        self._second_sc = self.style().hitTestComplexControl(
            QtWidgets.QStyle.CC_Slider, self.opt, event.pos(), self
        )

    def mouseMoveEvent(self, event: QtGui.QMouseEvent):

        distance = self.opt.maximum - self.opt.minimum

        pos = self.style().sliderValueFromPosition(
            0, distance, event.pos().x(), self.rect().width()
        )

        if self._first_sc == QtWidgets.QStyle.SC_SliderHandle:
            if pos <= self.second_position:
                self.first_position = pos
                self.update()
                return

        if self._second_sc == QtWidgets.QStyle.SC_SliderHandle:
            if pos >= self.first_position:
                self.second_position = pos
                self.update()

    def sizeHint(self):
        """ override """
        SliderLength = 84
        TickSpace = 5

        w = SliderLength
        h = self.style().pixelMetric(
            QtWidgets.QStyle.PM_SliderThickness, self.opt, self
        )

        if (
            self.opt.tickPosition & QtWidgets.QSlider.TicksAbove
            or self.opt.tickPosition & QtWidgets.QSlider.TicksBelow
        ):
            h += TickSpace

        return (
            self.style()
            .sizeFromContents(
                QtWidgets.QStyle.CT_Slider, self.opt, QtCore.QSize(w, h), self
            )
            .expandedTo(QtWidgets.QApplication.globalStrut())
        )
