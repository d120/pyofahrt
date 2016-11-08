# pyofahrt
Verwaltungssoftware für die Erstsemesterfahrt

## Deployment

### Installation

* Install `python3`, `python3-pip` and `virtualenv`
* Maybe create a user for the WSGI applications (e.g. `pyofahrt`)
* Clone this repository into a proper directory (e.g. `/srv/pyofahrt`)
* Create MySQL database and proper user
* Create the file `pyofahrt/settings_secrets.py` (ideally from `pyofahrt/settings_secrets.template.txt`) and fill it with the necessary credentials
* Create a virtualenv (e.g. `virtualenv -p python3 venv`)
* For serving WSGI applications, one can install `uwsgi`, create an ini file under `/etc/uwsgi` with a proper configuration and configure the webserver to use `mod-proxy-uwsgi` to make the application accessible. The webserver should also serve the static files. Make sure the application server (uwsgi) sets the proper environment variable for production settings (`DJANGO_SETTINGS_MODULE=pyofahrt.settings_production`).
* Run all the relevant commands from the Updates section

### Updates

When manually executing `manage.py` commands in production, do not forget to either pass the `--settings pyofahrt.settings_production` flag oder set it as an environment variable like `export DJANGO_SETTINGS_MODULE=pyofahrt.settings_production`.

To update an instance of pyofahrt, one can use the included update script `script/update`.

For production instances, one should use something like `sudo -u pyofahrt script/update --prod`.
