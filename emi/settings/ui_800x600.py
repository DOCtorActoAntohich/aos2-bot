from emi.math import Rect


class _Player1UiDescription800x600:
    HealthPosition = Rect(70, 27).with_size(100, 18)
    MeterBarsPosition = Rect(137, 51).with_size(92, 31)
    HeatPosition = Rect(280, 55).with_size(49, 22)
    DashCancelIconPosition = Rect(326, 76).with_size(48, 17)


class _Player2UIDescription800x600:
    HealthPosition = Rect(630, 27).with_size(100, 18)
    MeterBarsPosition = Rect(570, 51).with_size(92, 31)
    HeatPosition = Rect(491, 55).with_size(49, 22)
    DashCancelIconPosition = Rect(426, 76).with_size(48, 17)


class UiDescription800x600:
    p1 = _Player1UiDescription800x600()
    p2 = _Player2UIDescription800x600()
    Position = Rect(0, 0).with_size(800, 120)
    TimerPosition = Rect(362, 8).with_size(75, 32)
