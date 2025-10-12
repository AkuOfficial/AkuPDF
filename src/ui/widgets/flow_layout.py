from PySide6.QtCore import Qt, QRect, QSize, QPoint
from PySide6.QtWidgets import QLayout, QLayoutItem


class FlowLayout(QLayout):
    """Layout that arranges widgets in a flow, wrapping to next line when needed."""

    def __init__(self, parent=None, margin=0, spacing=-1):
        super().__init__(parent)
        self._item_list = []
        self._h_spacing = spacing
        self._v_spacing = spacing
        self.setContentsMargins(margin, margin, margin, margin)

    def addItem(self, item):
        self._item_list.append(item)

    def horizontalSpacing(self):
        return self._h_spacing if self._h_spacing >= 0 else self._smart_spacing()

    def verticalSpacing(self):
        return self._v_spacing if self._v_spacing >= 0 else self._smart_spacing()

    def count(self):
        return len(self._item_list)

    def itemAt(self, index):
        if 0 <= index < len(self._item_list):
            return self._item_list[index]
        return None

    def takeAt(self, index):
        if 0 <= index < len(self._item_list):
            return self._item_list.pop(index)
        return None

    def expandingDirections(self):
        return Qt.Orientations(Qt.Orientation.Horizontal)

    def hasHeightForWidth(self):
        return True

    def heightForWidth(self, width):
        return self._do_layout(QRect(0, 0, width, 0), True)

    def setGeometry(self, rect):
        super().setGeometry(rect)
        self._do_layout(rect, False)

    def sizeHint(self):
        return self.minimumSize()

    def minimumSize(self):
        size = QSize()
        for item in self._item_list:
            size = size.expandedTo(item.minimumSize())
        margin = self.contentsMargins().left()
        size += QSize(2 * margin, 2 * margin)
        return size

    def _do_layout(self, rect, test_only):
        x = rect.x()
        y = rect.y()
        line_height = 0
        h_space = self.horizontalSpacing()
        v_space = self.verticalSpacing()

        for item in self._item_list:
            widget = item.widget()
            space_x = h_space
            space_y = v_space

            next_x = x + item.sizeHint().width() + space_x
            if next_x - space_x > rect.right() and line_height > 0:
                x = rect.x()
                y = y + line_height + space_y
                next_x = x + item.sizeHint().width() + space_x
                line_height = 0

            if not test_only:
                item.setGeometry(QRect(QPoint(x, y), item.sizeHint()))

            x = next_x
            line_height = max(line_height, item.sizeHint().height())

        return y + line_height - rect.y()

    def _smart_spacing(self):
        return 10
