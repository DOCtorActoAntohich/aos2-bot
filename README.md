# Emi

## How to run

### Prerequisites

- Python 3.10
- `conda` (tested with `Anaconda3`)
- A beefy computer ![](https://steamcommunity-a.akamaihd.net/economy/emoticon/:ohh_yeah:)

Clone this repository and go to the root folder.

### Environment

#### Python

In the root folder, run `conda env update --file conda-env.yaml`
and let it run for a couple of stargates. ![](https://steamcommunity-a.akamaihd.net/economy/emoticon/:ohh_yeah:)

This command should install some cursed dependencies like `tesserocr` and `poetry`.

After it's done, run `poetry install` to install the remaining dependencies.

~~You might need to execute `winget install tesseract-ocr`.~~

#### User config

Create a copy of `sample.env` named `.env` and adjust values as you see fit.

### Running

Put modified game files into the game folder.

Open the game and change settings as follows:

- Language: **Japanese** or **Russian**
- Advanced Effects: **OFF**
- High contrast mode: **ON**
- P1 color: <span style="color:blue">**BLUE**</span>.
- P2 color: <span style="color:red">**RED**</span>.
- Display Armor Points: **ON**
- Display AP As Percentage: **OFF**
- Display Attack Indicator: **ON**

With the environment activated, execute `python -m emi` in the terminal.
To stop, press `Ctrl+C`.

## Issues

#### Screen borders

The window should NOT clip with physical screen borders,
otherwise some parts of the window won't update.
It will cause computer vision to fail.

#### Foreground window

The window _has to_ be in foreground (active) for inputs to work.

AoS2 really (really) wants you to use DirectInput.
However, you cannot directly send simulated keystrokes to the game's window when it's in background.
The workaround was implemented,
so it should just stop simulating all keys when the window is in background.
Still, just in case, you have been warned.

#### Fonts

*Nationalyze* is the worst font. ![](https://steamcommunity-a.akamaihd.net/economy/emoticon/:ohh_yeah:)

Maybe it will be replaced with something more readable (for English).
