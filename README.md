# AoS2 bot

An ambitious and funny thesis project that wasn't very successful. ![:ohh_yeah:](https://steamcommunity-a.akamaihd.net/economy/emoticon/:ohh_yeah:)

Initial idea (proof of concept): Reinforcement learning bot that gathers observations using Computer Vision.
The target game was my beloved [Acceleration of SUGURI 2](https://store.steampowered.com/app/390710/Acceleration_of_SUGURI_2/).

Results: Only some poor detection. ![:ohh_yeah:](https://steamcommunity-a.akamaihd.net/economy/emoticon/:ohh_yeah:)

It's not gonna receive any updates because the methodology is counter-productive.
It was a fun and crazy experiment that's not really worth the effort.

## How to run

### Prerequisites

- Python 3.10
- `conda` (`Anaconda3` in my case)
- A beefy computer ![:ohh_yeah:](https://steamcommunity-a.akamaihd.net/economy/emoticon/:ohh_yeah:)

Clone this repository and go to the root folder.

### Environment

#### Python

Create an environment with `conda env create --file conda-env.yaml`.
Let it run for a couple of stargates until it installs stuff. ![:ohh_yeah:](https://steamcommunity-a.akamaihd.net/economy/emoticon/:ohh_yeah:)

Do `conda activate -n aos2bot`, then run `pip install -r requirements-dev.txt`.
You may want to omit `-dev` if you don't care about code quality and stuff.

If something wrong happens to Tesseract, install it with `winget install tesseract-ocr`.

#### User config

Create a copy of `.env.example` named `.env` and adjust values as you see fit.

### Game assets

I modified the game files for stuff to work better.
I am not quite sure if it's legal to post these assets considering that I don't own them,
so for safety they aren't present in the repository.

Use [AoS2 ripper](https://github.com/MergeCommits/aos2ripper) to manually replace backgrounds
and maybe some other particles as you see fit.

What I did (it may not be a full list because I forgor'd):

- Replaced backgrounds with black textures.
- Removed some particles from timer.
- Made heat text background black (it still was transparent).
- Removed particles from character folders.
- Removed shield halo and stuff like that.

### Running the app

Open the game and change settings as follows:

- Language: **Japanese** or **Russian**
- Advanced Effects: **OFF**
- High contrast mode: **ON**
- P1 color: <span style="color:blue">**BLUE**</span>.
- P2 color: <span style="color:red">**RED**</span>.
- Display Armor Points: **ON**
- Display AP As Percentage: **OFF**
- Display Attack Indicator: **ON**

With the environment activated, execute `python -m src` in the terminal.
To stop, press `Ctrl+C`.

## Issues

### Screen borders

The window should NOT clip with physical screen borders,
otherwise some parts of the window won't update.
It will cause computer vision to fail.

### Foreground window

The window _has to_ be in foreground (active) for inputs to work.

AoS2 really (really) wants you to use DirectInput.
However, you cannot directly send simulated keystrokes to the game's window when it's in background.

If you somehow minimize the window by accident, you should be safe
because I made a little thing to disable input simulation in that case.
Still, just in case, you have been warned.

### Fonts

*Nationalyze* is the worst font. ![:ohh_yeah:](https://steamcommunity-a.akamaihd.net/economy/emoticon/:ohh_yeah:)

Russian language font is recommended for better OCR results.
Japanese might work too but it's too small.
