from emi.math import Rect


class _Player1UiDescription1366x768:
    HealthPosition = Rect(92, 36).with_size(220, 20)
    MeterBarsPosition = Rect(170, 64).with_size(130, 40)
    HeatPosition = Rect(358, 67).with_size(60, 34)
    DashCancelIconPosition = Rect(576, 90).with_size(60, 25)


class _Player2UIDescription1366x768:
    HealthPosition = Rect(1058, 36).with_size(220, 20)
    MeterBarsPosition = Rect(1070, 64).with_size(130, 40)
    HeatPosition = Rect(972, 69).with_size(60, 30)
    DashCancelIconPosition = Rect(728, 90).with_size(60, 25)


class UiDescription1366x768:
    p1 = _Player1UiDescription1366x768()
    p2 = _Player2UIDescription1366x768()
    Position = Rect(0, 0).with_size(1366, 140)
    TimerPosition = Rect(618, 0).with_size(128, 80)
