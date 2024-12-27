# pi-attend

An **Attendance Control System** built with Python, designed to work with simple hardware components such as a Raspberry Pi, PN532 NFC module, passive buzzer, ASCII LCD screen with a keypad, and NTAG215 cards. This system uses **Pocketbase** as a database backend, accessed through its API, and a front-end is planned for future development.

## Features

- **NFC Integration**: Uses the PN532 NFC module for scanning NTAG215 cards to identify users.
- **User Feedback**: Provides visual feedback through a 2-row, 5x8 ASCII LCD screen and audio feedback using a passive buzzer. Custom 5x8 char and custom buzzer melody creation are allowed.
- **Keypad Input**: Allows for simple administrator control through the buttons.
- **Pocketbase Backend**: Centralized database management through Pocketbase, accessed via its RESTful API.
- **Python-Powered**: Python scripts control all components, ensuring flexibility and extensibility.
- **Arduino Integration**: Uses the Nanpy library for seamless communication with the Arduino for LCD and keypad operations.
- **Future Front-End**: A web-based front-end interface is under development (abandoned, for the moment).

## Hardware Requirements

- **Raspberry Pi** (any model with GPIO capabilities)
- **PN532 NFC Module** (supports NTAG215 cards)
- **Passive Buzzer**
- **2-row, 5x8 ASCII LCD Screen with Keypad** (controlled via Arduino UNO-compatible board)
- **NTAG215 NFC Cards** (for user identification)
- **Connecting Cables** (for prototyping)

## Software Requirements

- **Python Libraries**: `RPi.GPIO`, `pynfc`, `nanpy`, `requests`
- **Pocketbase**: Lightweight backend with RESTful API access
- **Arduino Libraries**: Basic serial communication and Nanpy-compatible firmware
- **Operating System**: Raspberry Pi OS (preferred)
