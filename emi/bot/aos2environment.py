from __future__ import annotations

from typing import Any, SupportsFloat

import gym
import numpy
import cv2

from emi.bot.controls import Controls
from emi.bot.vision import InterfaceData, OcrError
from emi.settings import Settings
from emi.windows.window import Window
from emi.windows.hook_listener_thread import WindowsHookListenerThread


class AoS2Environment(gym.Env):
    Observation = int
    Action = numpy.ndarray
    Reward = SupportsFloat
    Completed = bool
    ExtraInfo = dict[str, Any]

    ResetResult = Observation | tuple[Observation, ExtraInfo]
    StepResult = tuple[Observation, Reward, Completed, ExtraInfo]

    metadata = {
        "render_modes": ["human", None]
    }

    def __init__(self):
        self.action_space = gym.spaces.MultiBinary(len(Controls))
        self.observation_space = gym.spaces.Box(
            low=0,
            high=256,
            shape=(768, 1366, 3)
        )

        self.window = Window(Settings.game.name)
        self.hook_listener_thread = WindowsHookListenerThread(self.window.focus_change_callback)
        self.pressed_buttons: list[Controls] = []

    def reset(
            self,
            *,
            seed: int | None = None,
            return_info: bool = False,
            options: dict | None = None
    ) -> ResetResult:
        if not self.hook_listener_thread.is_alive():
            self.hook_listener_thread.start()

        observation = self.__get_observation()
        extra_info = self.__get_extra_info()
        if return_info:
            return observation, extra_info
        return observation

    def step(self, action: Action) -> StepResult:
        self.__press_buttons(action)

        observation = self.__get_observation()
        reward = 0
        is_done = False
        extra_info = self.__get_extra_info()
        return observation, reward, is_done, extra_info

    def render(self, mode: str | None = None) -> None:
        if mode != "human":
            return

        self.window.update()
        frame = self.window.last_frame

        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        interface = InterfaceData(gray_frame)
        try:
            p1_heat = interface.p1_heat
        except OcrError:
            p1_heat = -1

        # weird values: 55 119 199 235 253 255
        print(p1_heat)

        cv2.imshow(Settings.opencv_window_name, frame)
        cv2.waitKey(1)

    @classmethod
    def __buttons_to_controls(cls, buttons: numpy.ndarray) -> list[Controls]:
        return [
            Controls(i + 1)
            for i, is_pressed in enumerate(buttons)
            if is_pressed == 1
        ]

    def __press_buttons(self, action_sample: numpy.ndarray) -> None:
        buttons_to_press = self.__buttons_to_controls(action_sample)
        self.window.set_new_inputs(buttons_to_press)

    def __get_observation(self) -> Observation:
        return 0

    def __get_extra_info(self) -> ExtraInfo:
        return {}
