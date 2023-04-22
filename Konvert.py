import json
import os
import pathlib
import sys
import webbrowser

import PySide6
from PySide6.QtGui import QIcon, QFont
from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QGridLayout,
    QPlainTextEdit,
    QComboBox,
    QPushButton,
    QHBoxLayout,
    QLabel,
    QFileDialog,
)

from utils import global_path
from src.utils import font

from src import converter

global_path.set_proj_abs_path(os.path.abspath(__file__))

SUPPORTING_FORMATS = ["jpg"]
SUPPORTING_FORMATS.sort()


class Konvert_Window(QWidget):
    def __init__(self):
        super(Konvert_Window, self).__init__()
        font.load_font(w=self)
        with open(global_path.get_proj_abs_path("config/config.json"), "r") as j:
            self.config = json.load(j)

        self.GRID = QGridLayout()

        self.TargetTextBox = QPlainTextEdit()
        self.TargetTextBox.setReadOnly(True)
        self.TargetTextBox.setFont(QFont(self.Pretendard_Regular, 12))

        self.OptionBox = QHBoxLayout()
        self.OptionBox_Output_Format = QComboBox()
        self.OptionBox_Output_Format.setFont(QFont(self.Pretendard_Regular, 20))

        self.OptionBox_Reset_Button = QPushButton("Reset")
        self.OptionBox_Reset_Button.clicked.connect(lambda: self.Reset_Button_Clicked())
        self.OptionBox_Reset_Button.setFont(QFont(self.Pretendard_Regular, 20))

        self.OptionBox_Start_Button = QPushButton("Start")
        self.OptionBox_Start_Button.clicked.connect(lambda: self.Start_Button_Clicked())
        self.OptionBox_Start_Button.setFont(QFont(self.Pretendard_Regular, 20))

        self.OptionBox_OUTPUT_Loc_Button = QPushButton("OUTPUT_LOCATION")
        self.OptionBox_OUTPUT_Loc_Button.clicked.connect(
            lambda: self.OUTPUT_LOC_BUTTON_CLICKED()
        )
        self.OptionBox_OUTPUT_Loc_Button.setFont(QFont(self.Pretendard_Regular, 20))
        self.FILE_DIALOG = QFileDialog()

        self.StatusCMDBox = QPlainTextEdit()
        self.StatusCMDBox.setReadOnly(True)
        self.StatusCMDBox.setFont(QFont(self.Pretendard_Regular, 12))

        for i in SUPPORTING_FORMATS:
            self.OptionBox_Output_Format.addItem(i)

        self.FOOTER_BOX = QHBoxLayout()

        self.FOOTER_LABEL = QLabel(
            f"Copyright (c) 2023- shiüo :: Konvert v{self.config['version']}"
        )
        self.FOOTER_LABEL.setFont(QFont(self.Pretendard_Bold, 10))

        self.FOOTER_GITHUB_BUTTON = QPushButton("Github")
        self.FOOTER_GITHUB_BUTTON.setFont(QFont(self.Pretendard_Regular, 10))
        self.FOOTER_GITHUB_BUTTON.clicked.connect(lambda: self.FOOTER_GITHUB_CLICKED())

        self.FOOTER_WEB_BUTTON = QPushButton("Web")
        self.FOOTER_WEB_BUTTON.setFont(QFont(self.Pretendard_Regular, 10))

        self.FOOTER_DISCORD_BUTTON = QPushButton("Discord")
        self.FOOTER_DISCORD_BUTTON.setFont(QFont(self.Pretendard_Regular, 10))
        self.FOOTER_DISCORD_BUTTON.clicked.connect(
            lambda: self.FOOTER_DISCORD_CLICKED()
        )

        # Variables
        self.Target_Location = set()
        self.Status_CMD_Content = ""
        self.OUTPUT_DIR = ""

        self.setWindowTitle("Konvert")
        self.setWindowIcon(QIcon(global_path.get_proj_abs_path("assets/Konvert.png")))
        self.setMinimumSize(640, 360)
        self.resize(1280, 720)
        self.setAcceptDrops(True)
        self.initUI()

    def initUI(self):
        with open(
            file=global_path.get_proj_abs_path("assets/stylesheet.txt"), mode="r"
        ) as f:
            self.setStyleSheet(f.read())

        self.OptionBox.addWidget(self.OptionBox_Output_Format)
        self.OptionBox.addWidget(self.OptionBox_Reset_Button)
        self.OptionBox.addWidget(self.OptionBox_Start_Button)
        self.OptionBox.addWidget(self.OptionBox_OUTPUT_Loc_Button)

        self.FOOTER_BOX.addWidget(self.FOOTER_LABEL)
        self.FOOTER_BOX.addWidget(self.FOOTER_GITHUB_BUTTON)
        self.FOOTER_BOX.addWidget(self.FOOTER_WEB_BUTTON)
        self.FOOTER_BOX.addWidget(self.FOOTER_DISCORD_BUTTON)

        # Final
        self.GRID.addWidget(self.TargetTextBox, 0, 0, 1, 1)
        self.GRID.addLayout(self.OptionBox, 1, 0, 1, 1)
        self.GRID.addWidget(self.StatusCMDBox, 2, 0, 1, 1)
        self.GRID.addLayout(self.FOOTER_BOX, 3, 0, 1, 1)
        self.setLayout(self.GRID)

    def Reset_Button_Clicked(self):
        self.Status_CMD_Content += f"{len(self.Target_Location)} items cleared." + "\n"
        self.Target_Location.clear()
        self.TargetTextBox.setPlainText("\n".join(self.Target_Location))

        self.StatusCMDBox.setPlainText(self.Status_CMD_Content)
        self.StatusCMDBox.verticalScrollBar().setValue(
            self.StatusCMDBox.verticalScrollBar().maximum()
        )

    def Start_Button_Clicked(self):
        if len(self.Target_Location) > 0:
            if self.OUTPUT_DIR:
                for i in self.Target_Location:
                    suffix = "".join(pathlib.Path(i).suffixes)
                    location = i[: len(i) - len(suffix)]
                    save_location = os.path.join(
                        self.OUTPUT_DIR, pathlib.Path(location).name
                    )
                    A = converter.convert(
                        in_format=suffix[1:],
                        out_format=self.OptionBox_Output_Format.currentText(),
                        loc=location,
                        save_loc=save_location,
                    )
                    if A:
                        self.Status_CMD_Content += (
                            f"{i} -> {save_location}.{self.OptionBox_Output_Format.currentText()}"
                            + "\n"
                        )
                    else:
                        self.Status_CMD_Content += f"Failed to convert {i}" + "\n"

                    self.StatusCMDBox.setPlainText(self.Status_CMD_Content)
                    self.StatusCMDBox.verticalScrollBar().setValue(
                        self.StatusCMDBox.verticalScrollBar().maximum()
                    )

            else:
                self.Status_CMD_Content += (
                    f"Please specify the location to export the file to." + "\n"
                )

                self.StatusCMDBox.setPlainText(self.Status_CMD_Content)
                self.StatusCMDBox.verticalScrollBar().setValue(
                    self.StatusCMDBox.verticalScrollBar().maximum()
                )

        else:
            self.Status_CMD_Content += f"Empty." + "\n"

            self.StatusCMDBox.setPlainText(self.Status_CMD_Content)
            self.StatusCMDBox.verticalScrollBar().setValue(
                self.StatusCMDBox.verticalScrollBar().maximum()
            )

    def OUTPUT_LOC_BUTTON_CLICKED(self):
        f = self.FILE_DIALOG.getExistingDirectory(self, "Select Directory")
        if f:
            self.OUTPUT_DIR = f
            self.Status_CMD_Content += f"OUTPUT_DIR = {f}" + "\n"

            self.StatusCMDBox.setPlainText(self.Status_CMD_Content)
            self.StatusCMDBox.verticalScrollBar().setValue(
                self.StatusCMDBox.verticalScrollBar().maximum()
            )

    def FOOTER_GITHUB_CLICKED(self):
        webbrowser.open("https://github.com/shiueo/konvert")

    def FOOTER_DISCORD_CLICKED(self):
        webbrowser.open("https://discord.gg/NXwVfdcygM")

    def dragEnterEvent(self, event: PySide6.QtGui.QDragEnterEvent) -> None:
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event: PySide6.QtGui.QDropEvent) -> None:
        files = [i.toLocalFile() for i in event.mimeData().urls()]
        for f in files:
            self.Target_Location.add(f)
        self.TargetTextBox.setPlainText("\n".join(self.Target_Location))
        self.TargetTextBox.verticalScrollBar().setValue(
            self.TargetTextBox.verticalScrollBar().maximum()
        )


if __name__ == "__main__":
    Konvert_QApplication = QApplication()
    Konvert_GUI = Konvert_Window()
    Konvert_GUI.show()
    sys.exit(Konvert_QApplication.exec())
