# Emi

## How to run

### Prerequisites

- Python 3.10
- `make`
- A beefy computer ![](https://steamcommunity-a.akamaihd.net/economy/emoticon/:ohh_yeah:)

Clone this repository and go to the root folder.

### Virtual Environment

Create a virtual environment by running `make venv` inside the root folder.
It will automatically install all required packages with few exceptions.

### Tesseract

Install Tesseract: `choco install tesseract`

Install [`tesserocr`](https://github.com/sirfz/tesserocr).

### Environment

Create a copy of `sample.env` named `.env` and adjust values as you see fit.

While keeping the game open in the background, execute `make run` in console.
To stop, press `Ctrl+C`.

## Issues

#### Screen borders

The window should NOT clip with physical screen borders,
otherwise some parts of the window won't update.
It will cause CV to fail.

#### Foreground window

The window _has to_ be in foreground (active) for inputs to work.

AoS2 really (really) wants you to use DirectInput.
However, you cannot directly send simulated keystrokes to the game's window when it's in background.
The workaround was implemented,
so it should just stop simulating all keys when the window is in background.
Still, just in case, you have been warned.