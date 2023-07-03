from __future__ import annotations

import logging
from typing import Any

import cv2
import gym
import numpy

from src.bot.controls import Controls
from src.bot.vision import ArenaData, InterfaceData
from src.settings import Settings
from src.windows.hook_listener_thread import WindowsHookListenerThread
from src.windows.window import Window


class AoS2Environment(gym.Env):
    metadata = {"render_modes": ["human", None]}

    def __init__(self) -> None:
        self.action_space = gym.spaces.MultiBinary(len(Controls))
        self.observation_space = gym.spaces.Box(low=0, high=256, shape=(768, 1366, 3))

        self.window = Window(Settings.game.name)
        self.hook_listener_thread = WindowsHookListenerThread(self.window.focus_change_callback)
        self.pressed_buttons: list[Controls] = []

    def reset(
        self,
        *,
        seed: int | None = None,  # noqa: ARG002
        options: dict | None = None,  # noqa: ARG002
    ) -> tuple[int, dict[str, Any]]:
        if not self.hook_listener_thread.is_alive():
            self.hook_listener_thread.start()

        observation = self.__get_observation()
        extra_info = self.__get_extra_info()
        return observation, extra_info

    def step(self, action: numpy.ndarray) -> tuple[int, float, bool, bool, dict[str, Any]]:
        self.__press_buttons(action)

        observation = self.__get_observation()
        reward = 0
        is_done = False
        is_truncated = False
        extra_info = self.__get_extra_info()
        return observation, reward, is_done, is_truncated, extra_info

    def render(self, mode: str | None = None) -> None:
        if mode != "human":
            return

        self.window.update()
        frame = self.window.last_frame

        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        interface = InterfaceData(gray_frame)
        arena = ArenaData(frame)

        logging.info("p1 hp: %s, objects found: %s", interface.p1_health, len(arena.detections))

        cv2.imshow(Settings.opencv_window_name, frame)
        cv2.waitKey(1)

    @classmethod
    def __buttons_to_controls(cls, buttons: numpy.ndarray) -> list[Controls]:
        return [Controls(i + 1) for i, is_pressed in enumerate(buttons) if is_pressed == 1]

    def __press_buttons(self, action_sample: numpy.ndarray) -> None:
        buttons_to_press = self.__buttons_to_controls(action_sample)
        self.window.set_new_inputs(buttons_to_press)

    @classmethod
    def __get_observation(cls) -> int:
        return 0

    @classmethod
    def __get_extra_info(cls) -> dict[str, Any]:
        return {}
