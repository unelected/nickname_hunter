
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

The script uses two types of credentials:

1. **`.env` file** — stores the account used for **monitoring nickname availability**.
   Example `.env`:

   ```env
   EMAIL=your_email@example.com
   PASSWORD=your_password
   ```

2. **`config.json`** — stores the list of accounts that will **claim nicknames** once they become available, and the nicknames to track:

```json
{
  "entertainers": [
    ["email1@example.com", "password1"],
    ["email2@example.com", "password2"]
  ],
  "trackeds": [
    ["nickname_id_1", "nickname"],
    ["nickname_id_2", ""]
  ]
}
```

* `entertainers`: List of Mafia Online accounts (email/password) used to **log in and claim nicknames** once they become available.
* `trackeds`: List of nickname IDs you want to monitor and attempt to claim.

---

## Usage

Run the script from the command line:

```bash
python nickname_hunter.py
```
The script will read your config.json, monitor the specified nicknames,
and attempt to claim them automatically once they are released.
Notifications are printed to the console when a nickname is successfully claimed.

---

## ⚠️ Disclaimer:
This script automatically claims released nicknames, but it does not interfere with or harm other players.
It should be used only for testing, development, or personal experiments.

---

## License

This project is licensed under the terms of the **GNU Affero General Public License v3.0 only (AGPL-3.0-only)**.
See the [LICENSE](./LICENSE) file for full details.

### Note on MIT-licensed code

This project also contains portions of code originally published under the **MIT License**.
While the project as a whole is distributed under AGPL-3.0-only, the MIT-licensed parts remain available under their original terms.
See [LICENSE.MIT](./LICENSE.MIT) for details.
