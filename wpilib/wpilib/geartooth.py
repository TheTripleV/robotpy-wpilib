#----------------------------------------------------------------------------
# Copyright (c) FIRST 2008-2012. All Rights Reserved.
# Open Source Software - may be modified and shared by FRC teams. The code
# must be accompanied by the FIRST BSD license file in the root directory of
# the project.
#----------------------------------------------------------------------------

import hal

from .counter import Counter
from .livewindow import LiveWindow

class GearTooth(Counter):
    """Alias for counter class.
    Implement the gear tooth sensor supplied by FIRST. Currently there is no
    reverse sensing on the gear tooth sensor, but in future versions we might
    implement the necessary timing in the FPGA to sense direction.
    """

    kGearToothThreshold = 55e-6

    def enableDirectionSensing(self, directionSensitive):
        if directionSensitive:
            self.setPulseLengthMode(GearTooth.kGearToothThreshold)

    def __init__(self, channel, directionSensitive=False):
        """Construct a GearTooth sensor.

        :param channel: The GPIO channel index or DigitalSource that the sensor
            is connected to.
        :param directionSensitive: Enable the pulse length decoding in
            hardware to specify count direction.  Defaults to False.
        """
        super().__init__(channel)
        self.enableDirectionSensing(directionSensitive)
        if hasattr(self.upSource, "getChannel"):
            if directionSensitive:
                hal.HALReport(hal.HALUsageReporting.kResourceType_GearTooth,
                              self.upSource.getChannel(), 0, "D")
            else:
                hal.HALReport(hal.HALUsageReporting.kResourceType_GearTooth,
                              self.upSource.getChannel(), 0)
        LiveWindow.addSensorChannel("GearTooth", self.upSource.getChannel(),
                                    self)

    # Live Window code, only does anything if live window is activated.

    def getSmartDashboardType(self):
        return "Gear Tooth"