from __future__ import annotations

from typing import Any, SupportsFloat

import gym
import numpy
import cv2

from emi.controls import Controls
from emi.settings import Settings
from emi.window import Window


class AoS2Environment(gym.Env):
    Observation = numpy.ndarray
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
            shape=(768, 1366, 4)
        )

        self.window = Window(Settings.game_name)

    def reset(
            self,
            *,
            seed: int | None = None,
            return_info: bool = False,
            options: dict | None = None
    ) -> ResetResult:
        observation = self.__get_observation()
        extra_info = self.__get_extra_info()
        if return_info:
            return observation, extra_info
        return observation

    def step(self, action: Action) -> StepResult:
        pressed_buttons = self.__buttons_to_controls(action)

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
        cv2.imshow(Settings.opencv_window_name, frame)
        cv2.waitKey(1)

    @classmethod
    def __buttons_to_controls(cls, buttons: numpy.ndarray) -> list[Controls]:
        return [
            Controls(i + 1)
            for i, is_pressed in enumerate(buttons)
            if is_pressed
        ]

    def __get_observation(self) -> Observation:
        return 0

    def __get_extra_info(self) -> ExtraInfo:
        return {}