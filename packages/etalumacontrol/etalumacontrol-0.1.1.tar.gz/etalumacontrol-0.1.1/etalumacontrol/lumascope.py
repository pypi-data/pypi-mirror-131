# pyright: reportMissingImports=false

import os
import clr
import sys
import time
import platform
from PIL import Image
from .CypressFX import FX2
from .definitions import RSC_DIR, LIB_DIR, LED_WHITE

# load appropriate dll
(bits, linkage) = platform.architecture()
if bits == "64bit":
    sys.path.append(os.path.join(LIB_DIR, 'x64'))
else:
    sys.path.append(os.path.join(LIB_DIR, 'x86'))
LUMAUSB_DLL = clr.AddReference('LumaUSB')

from LumaUSB_ns import LumaUSB
from LumaUSB_ns import VideoParameters


class CameraError(Exception):
    pass


class LumaScope(object):
    '''
    This class provides access to the microscope and LEDs. For interacting with
    the stage, including focusing, see :class:`EtalumaStage`.

    If the microscope is in an uninitialized, i.e., its firmware has not been
    uploaded, firmware will be uploaded upon instantiation.

    This class supports the context manager, and thus the following code will
    ensure that resources are properly disposed handled::

        with LumaScope() as lumascope:
            # perform microscope operations

    Although the camera can also be closed manually using the :meth:`close`
    method::

        lumascope = LumaScope()
        try:
            # perform miscope operations
        finally:
            lumascope.close()

    For convenience, this object can be instantiated using the following
    optional parameters:

    * *resolution* -- the resolution of the image. See :attr:`resolution`.
    * *gain* -- the global gain. See :attr:`gain`.
    * *shutter* -- the shutter speed in milliseconds. See :attr:`shutter`.
    '''

    MAX_GLOBAL_GAIN = LumaUSB.MAX_GLOBAL_GAIN_PARAMETER_VALUE
    MIN_GLOBAL_GAIN = LumaUSB.RECOMMENDED_MIN_GLOBAL_GAIN_PARAMETER_VALUE
    _shutter = 0
    _gain = MIN_GLOBAL_GAIN

    def __init__(self, resolution: int = 1600, gain: int = MIN_GLOBAL_GAIN, shutter: int = 150) -> None:
        # check for initialized microscope
        fx2 = FX2.with_vid_pid(LumaUSB.VID_CYPRESS, LumaUSB.PID_LSCOPE)
        if fx2 is None:
            # uninitialized microscope found; upload firmware
            fx2 = FX2.with_vid_pid(LumaUSB.VID_CYPRESS, LumaUSB.PID_FX2_DEV)
            t = 0
            try:
                fx2.load_intelhex_firmware(os.path.join(RSC_DIR, 'Lumascope600.hex'))
            except IOError as e:
                raise CameraError('Unable to upload firmware to device: ' + str(e))
            while fx2 := FX2.with_vid_pid(LumaUSB.VID_CYPRESS, LumaUSB.PID_LSCOPE) is None:
                time.sleep(0.5)
                if (t := t + 1) > 20:
                    raise CameraError('Timeout while initializing microscope')

        self.hw = LumaUSB(LumaUSB.VID_CYPRESS, LumaUSB.PID_LSCOPE, resolution, resolution)
        self.vid_params = VideoParameters()

        # set everything up and start video streaming
        self.hw.InitImageSensor()
        self.resolution = resolution
        self.gain = gain
        self.shutter = shutter
        self.hw.ISOStreamStart()
        self.hw.StartStreaming()

        # wait for image stream to become available
        while self.get_raw_image_buffer() is None:
            time.sleep(0.1)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    def close(self):
        '''
        Turn off LEDs and stop streaming.
        '''
        for led in range(0x41, 0x45):
            self.set_led(brightness=0, led_no=led)
        self.hw.StopStreaming()
        self.hw.ISOStreamStop()

    @property
    def gain(self) -> int:
        '''
        Sets or returns the global gain of the image sensor. Valid values are
        between ``MIN_GLOBAL_GAIN`` and ``MAX_GLOBAL_GAIN``. The minimum value
        is derived from the corresponding value in the Etaluma SDK, which is
        described like this: "If the gain goes below this value it was
        empirically observed that the image sensor cannot saturate no matter
        the intensity of the light source. 
        '''
        return self._gain

    @gain.setter
    def gain(self, value: int):
        if value < self.MIN_GLOBAL_GAIN or value > self.MAX_GLOBAL_GAIN:
            raise CameraError('Global gain outside allowed range')
        else:
            if not self.hw.SetGlobalGain(value):
                raise CameraError('Could not set global gain')
            self._gain = value

    @property
    def resolution(self):
        '''
        Sets or returns the camera resolution. The image is always square so
        only a single integer is given or returned. Valid values are 100-1900 in
        multiples of 4.
        '''
        return self.vid_params.width

    @resolution.setter
    def resolution(self, resolution: int):
        self.vid_params.width = self.vid_params.height = resolution
        if not self.hw.SetWindowSize(resolution):
            raise CameraError('Could not set resolution')

    @property
    def shutter(self) -> int:
        '''
        Sets or retrieves the shutter speed in milliseconds.

        If the shutter speed cannot be determined, this attribute is 0.
        '''
        return self._shutter
        # XXX: figure out why below code doesn't work
        # ret, val = self.hw.ImageSensorRegisterRead(LumaUSB.IMAGE_SENSOR_SHUTTER_WIDTH_LOWER, int())
        # if ret:
        #     return val
        # else:
        #     return 0

    @shutter.setter
    def shutter(self, speed: int) -> bool:
        if speed > 0 and speed <= LumaUSB.MAX_IMAGE_SENSOR_EXPOSURE:
            if not self.hw.ImageSensorRegisterWrite(LumaUSB.IMAGE_SENSOR_SHUTTER_WIDTH_LOWER, speed):
                raise CameraError('Unable to set desired shutter speed')
            else:
                # XXX: temporary workaround for failing to read register
                self._shutter = speed
        else:
            raise CameraError('Exposure speed out of range')

    def set_led(self, brightness: int, led_no: int = LED_WHITE) -> bool:
        '''
        Set brightness of selected LED. Returns ``False`` if this fails.

        Arguments:
        * *led_no* -- LED number. Valid values are 0x41-0x44, where 0x41-0x43
          are LEDs F1-F3 and 0x44 is white (A-D in ASCII hexadecimal).
        * *brightness* -- desired brightness (0-255).
        '''
        if led_no >= 0x41 and led_no <= 0x44 and \
            brightness >= 0 and brightness <= 255:
            return self.hw.LedControllerWrite(led_no, brightness)
        else:
            return False

    def get_image(self):
        '''
        Return the current buffer as a ``PIL`` (i.e., ``Pillow``) Image object.
        
        If an image cannot be retrieved, returns ``None``.
        '''
        if (buffer := self.get_raw_image_buffer()) is not None:
            return Image.frombytes('RGB', (self.resolution, self.resolution), buffer)
        else:
            return None

    def get_raw_image_buffer(self):
        '''
        Return the contents of the image buffer as bytes, or ``None``.
        '''
        (status, buffer) = self.hw.GetLatest24bppBuffer(None)
        buffer = bytes(buffer)

        # there's a bug in certain versions of the SDK that causes the last line
        # of the buffer to not be returned. add a black line to the bottom of
        # the image if this is the case.
        if len(buffer) < self.resolution**2 * 3:
            buffer += bytes(self.resolution * 3)

        if not status:
            return None
        else:
            return buffer
