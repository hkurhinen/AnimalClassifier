# Setup

If you have not already installed virtualenv tool install it with command:

`pip install virtualenv`

Create new virtual env with command:

`virtualenv venv`

Activate the newly created virtual env with command:

`source venv/bin/activate`

Install dependencies with command:

`pip install -r requirements.txt`


# Usage

For local installation start mqtt server by executing command:

`docker-compose up`

Then start spark MQTT listener by running:

`sh run.sh`

Then use some mqtt client and publish message in format:

`{"image": "/path/to/image/to/classify"}`



