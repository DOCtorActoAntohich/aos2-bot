from emi.primitives import Rectangle


class _Player1UiDescription800x600:
    HealthPosition = Rectangle(70, 27).with_size(100, 18)
    MeterBarsPosition = Rectangle(137, 51).with_size(92, 31)
    HeatPosition = Rectangle(280, 55).with_size(49, 22)
    DashCancelIconPosition = Rectangle(326, 76).with_size(48, 17)


class _Player2UIDescription800x600:
    HealthPosition = Rectangle(630, 27).with_size(100, 18)
    MeterBarsPosition = Rectangle(570, 51).with_size(92, 31)
    HeatPosition = Rectangle(491, 55).with_size(49, 22)
    DashCancelIconPosition = Rectangle(426, 76).with_size(48, 17)


class UiDescription800x600:
    p1 = _Player1UiDescription800x600()
    p2 = _Player2UIDescription800x600()
    Position = Rectangle(0, 0).with_size(800, 120)
    TimerPosition = Rectangle(362, 8).with_size(75, 32)
