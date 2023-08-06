import os

# the root directory of the installed package
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

# resource dir, contains lib directory and firmware
RSC_DIR = os.path.join(ROOT_DIR, 'resources')

# directory containing the SDK DLLs, in separate 'x86' and 'x64' subdirectories
LIB_DIR = os.path.join(RSC_DIR, 'lib')

# ID number of the brightfield LED
LED_WHITE = 0x44
