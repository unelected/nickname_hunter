
# nickname\_hunter

A CLI script to politely simulate an attempt to take the desired nickname(s) in the online game **Mafia Online**.

The script periodically checks the availability of specified nicknames and notifies you in the console once any of them becomes available.
It works in a passive way — simply waiting until another player voluntarily changes their nickname — and **does not interfere with gameplay or other users**.

---

## Features

* Track one or multiple nicknames simultaneously.
* Configurable via a simple JSON file.
* Console notifications when a nickname is released.
* Safe and non-intrusive: no influence on other players.

---

## Installation

Clone this repository and install the required dependencies:

```bash
git clone https://github.com/unelected/nickname_hunter.git
cd nickname_hunter
pip install -r requirements.txt
```

---

## Configuration

All settings are defined in `config.json`.

Example:

```json
{
  "entertainers": [
    ["email1@example.com", "password1"],
    ["email2@example.com", "password2"]
  ],
  "trackeds": [
    ["nickname_id_1", ""],
    ["nickname_id_2", ""]
  ]
}
```

* `entertainers`: List of Mafia Online accounts (email/password) used for checking nickname availability.
* `trackeds`: List of nickname IDs you want to monitor.

---

## Usage

Run the script from the command line:

```bash
python nickname_hunter.py
```

The script will read your `config.json`, start monitoring the nicknames, and print notifications to the console when any becomes available.

---

## License

This project is licensed under the terms of the **GNU Affero General Public License v3.0 only (AGPL-3.0-only)**.
See the [LICENSE](./LICENSE) file for full details.

### Note on MIT-licensed code

This project also contains portions of code originally published under the **MIT License**.
While the project as a whole is distributed under AGPL-3.0-only, the MIT-licensed parts remain available under their original terms.
See [LICENSE.MIT](./LICENSE.MIT) for details.
