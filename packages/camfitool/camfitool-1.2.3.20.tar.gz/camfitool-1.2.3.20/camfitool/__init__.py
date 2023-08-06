__author__ = "Alim Kerem Erdogmus"
__version__ = "v1.2.3"
__email__ = "kerem.erdogmus@inovasyonmuhendislik.com"
__status__ = "beta"

from .class_fi_realtime_ui import RealtimeImageFault
from .class_fi_offline_ui import OfflineImageFault
from .offline_fault_injector_ui import main
from .realtime_fault_injector_ui import RealtimeFaultInjector
from .ui_interface import Ui_MainWindow
from camfitool import camfitool_main

import sys
from PyQt5 import QtWidgets

def main():
    app = QtWidgets.QApplication(sys.argv)
    window = camfitool_main.MainWindow()
    sys.exit(app.exec_())
    
main()