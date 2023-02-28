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

### Tesseract OCR

Install Tesseract: `choco install tesseract-ocr`.
Make sure `C:\Program Files\Tesseract-OCR\tessdata` has `eng.traineddata`.

Install [`tesserocr`](https://github.com/sirfz/tesserocr) by downloading `.whl` file that fits your system.

### Environment

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

While keeping the game open in the background, execute `make run` in console.
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
