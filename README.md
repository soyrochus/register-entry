# Register Entry

Register entry is a Python GTK3 program to register entry into buildings (due to COVID)

## Installation

Obtain a clone of this repository
Use the package manager [pip](https://pip.pypa.io/en/stable/) to install [pipenv](https://pipenv.pypa.io/en/latest/). Use pipenv to install the application dependencies.

```bash
pip install pipenv

pipenv sync
```
## Usage

The script's intended usage is on a simple Windows or Linux device, ideally with a touch screen. The user can call up the on-screen keyboard by pressing the button marked with the keyboard sign (⌨).

![Register Entry](./register-entry.png)

The script reads a list of names from the file *"employees.xlsx"* to show them into the list-box for easy selection. Manual entry is also supported. Both selected as well as manually entered names will be written to the file *"registered.xlsx"* with the date/time of entry. Both Excel files need be stored in the current working directory. 

Additional input parameters (in the script is is the number of masks taken) can be easily customized in the custom dialog *ExtraDataDialog*, called from *run_extra_data_dialog*. 

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[BSD-3-Clause](https://choosealicense.com/licenses/bsd-3-clause-clear/)
