# pyright: reportMissingImports=false

import os
import clr
import sys
import time
import platform
from typing import Union
from .definitions import LIB_DIR

# load appropriate dll
(bits, linkage) = platform.architecture()
if bits == "64bit":
    sys.path.append(os.path.join(LIB_DIR, 'x64'))
else:
    sys.path.append(os.path.join(LIB_DIR, 'x86'))
LUMAUSB_DLL = clr.AddReference('LumaUSB')

from EtalumaStage import StageController


class StageError(Exception):
    pass


class EtalumaStage(object):
    '''
    This class provides access to the motorized stage of an Etaluma microscope.
    When instantiated, the stage will first initialize and home all axes. 

    This class supports the context manager, and thus the following code will
    ensure that resources are properly disposed handled::

        with EtalumaStage() as stage:
            # perform some operations

    The stage may also be used directly as an object, but then its :meth:`close`
    method should manually be called after use::

        try:
            stage = EtalumaStage()
            # perform some operations
        finally:
            stage.close()
    '''
    def __init__(self, _init = True) -> None:
        self.hw = StageController()

        ret, err_msg = self.hw.OpenCommLink(str())
        if not ret:
            raise StageError('Failed to open USB to serial link: ' + err_msg)
        elif not self.hw.IsCommLinkOpen():
            raise StageError('Failed to open USB to serial link: Unknown error')

        if _init:
            ret, err_msg = self.hw.OneStepInitialization(str())
            if not ret:
                raise StageError('Failed to initialize: ' + err_msg)

            # stage is initializing, allow 5 minutes until timeout
            i = 0
            while not self.hw.OneStepInitializationComplete() and (i := i + 1) < 300:
                time.sleep(1)

        # outer bounds for axis travel
        self.axis_range = {'X': range(self.hw.xMaximumAxisTravelMicrosteps, 1),
                           'Y': range(self.hw.yMaximumAxisTravelMicrosteps, 1),
                           'Z': range(0, self.hw.zMaximumAxisTravelMicrosteps)}

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    def close(self):
        '''
        Closes the USB to serial link.
        '''
        self.hw.CloseCommLink()

    @staticmethod
    def mm_to_microsteps(value: float, axis: str = 'X') -> int:
        '''
        Convert a value from millimeters to microsteps.

        Arguments:
        * *value* -- The value to convert.
        '''
        if axis.upper() == 'Z':
            return StageController.ConvertZMicrometersToMicroSteps(value * 1000)
        else:
            return StageController.ConvertMicrometersToMicroSteps(value * 1000)

    @staticmethod
    def _check_axis(axis: str):
        if not isinstance(axis, str):
            raise StageError('Invalid axis specified')
            
        axis = axis.upper()
        if axis not in ['X', 'Y', 'Z']:
            raise StageError('Invalid axis specified')
        
        return axis

    def get_pos(self, axis: str, microsteps: bool = False) -> Union[float, int, bool]:
        '''
        Return the stage's current absolute position.

        Arguments:
        * *axis* -- The axis to query. Valid values are ['x', 'y', 'z'],
          case-independent.
        * *microsteps* -- Whether to return the value in microsteps instead of
          millimeters. Defaults to False.
        '''

        axis = self._check_axis(axis)

        method = 'GetAbsolute' + axis + 'Position'
        if microsteps:
            method = method + 'MicroSteps'
        else:
            method = method + 'Millimeters'

        if microsteps:
            ret, pos = getattr(self.hw, method)(int())
        else:
            ret, pos = getattr(self.hw, method)(float())

        if ret:
            return pos
        else:
            raise StageError('Unable to retrieve current position')

    def move(self, axis: str, pos: Union[int, float], microsteps: int = False, blocking: bool = True) -> None:
        '''
        Moves the stage to the specified absolute position. Raises StageError if
        the position is outside of the allowed range. *Note:* If using LumaView
        to determine values, beware that the Z axis values in LumaView are
        reported in micrometers.

        Arguments:
        * *axis* -- The axis to query. Valid values are ['x', 'y', 'z'],
          case-independent.
        * *pos* -- The absolute position to travel to.
        * *microsteps* -- Specify position in microsteps instead of millimeters.
          Defaults to False.
        * *blocking* -- Specifies whether the method waits until movement is
          complete before returning. Defaults to True. Also see :meth:`stop`.
        '''

        axis = self._check_axis(axis)

        if axis != 'Z' and pos > 0:
            raise StageError('Position outside allowed range')
        elif axis == 'Z' and pos < 0:
            raise StageError('Position outside allowed range')

        if not microsteps:
            pos = self.mm_to_microsteps(pos, axis=axis)

        # check that we're in range
        # XXX: disable for now -- StageController.[x,y,z]MaximumAxisTravelMicrosteps returns values
        # which are more constrained than the actual allowed ranges.
        #if pos not in self.axis_range[axis]:
        #    raise StageError('Requested position out of range')

        # construct name for method to initiate movement
        method = 'Move' + axis + 'StageToAbsolutePositionMicroSteps'

        # this is the function to check if the command has finished
        ctrl_method = axis.lower() + 'ReachedCommandedPosition'

        getattr(self.hw, method)(pos)

        if blocking:
            while not getattr(self.hw, ctrl_method)():
                time.sleep(0.05)

    def stop(self, axis: str) -> bool:
        '''
        Stops the motor for the specified axis. Using this method should only be
        necessary when specifying ``blocking=False`` in :meth:`move`. Returns
        True if the motor was successfully stopped.

        Arguments:
        * *axis* -- The axis to stop. Valid values are ['x', 'y', 'z'],
          case-independent.
        '''

        axis = self._check_axis(axis)

        method = 'Stop' + axis + 'Motor'
        return getattr(self.hw, method)()
