# Track Errors in Flask with AppSignal

This repository demonstrates how to use AppSignal to track errors in a Flask application.

Read the article on [AppSignal's blog](#).

## Development Setup

1. Create a new virtual environment and activate it:
   
    ```sh
    $ python -m venv venv && source venv/bin/activate
    ```

1. Install the dependencies:

    ```sh
    $ pip install -r requirements.txt
    ```
   
1. Create a *.env* file with the following contents:

    ```sh
    APPSIGNAL_PUSH_API_KEY=<your_push_api_key>
    ```
   
1. Initialize the database:

    ```sh
    $ python init_db.py
    ```
   
1. Run the development server:

    ```sh
    $ flask run
    ```
   
1. Visit [http://localhost:5000/](http://localhost:5000/) in your favorite web browser.
