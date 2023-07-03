from src.primitives import Rectangle


class _Player1UiDescription1366x768:
    HealthPosition = Rectangle(92, 36).with_size(220, 20)
    MeterBarsPosition = Rectangle(170, 64).with_size(130, 40)
    HeatPosition = Rectangle(358, 67).with_size(60, 34)
    DashCancelIconPosition = Rectangle(576, 90).with_size(60, 25)


class _Player2UIDescription1366x768:
    HealthPosition = Rectangle(1058, 36).with_size(220, 20)
    MeterBarsPosition = Rectangle(1070, 64).with_size(130, 40)
    HeatPosition = Rectangle(972, 69).with_size(60, 30)
    DashCancelIconPosition = Rectangle(728, 90).with_size(60, 25)


class UiDescription1366x768:
    p1 = _Player1UiDescription1366x768()
    p2 = _Player2UIDescription1366x768()
    Position = Rectangle(0, 0).with_size(1366, 140)
    TimerPosition = Rectangle(618, 0).with_size(128, 80)
