# otterli-test-app
Test framework for the Otterli app's API backend, as well as the front end (watch this space!)

Important: This is for demo purposes only.

# Pre-requisites

1. Python >= 3.9.13 installed

2. Create a virtual env

    > python -m venv .venv

3. Activate the virtual env

4. Install the `requirements.txt`

    > pip install -r requirements.txt


# To access the Otterli API server 

1. Generate a `.env` file

    > touch .env

2. Add the following variables in to the `.env`

    - STAGING_API_KEY = `<STAGING_API_KEY>`

    - STAGING_URL = `<STAGING_URL>`

    - LOCAL_API_KEY = `<LOCAL_API_KEY>`

    - LOCAL_URL = `<LOCAL_URL>`
