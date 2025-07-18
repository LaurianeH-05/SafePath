SafePath: Drive Smarter, Drive Safer
SafePath is a Flask web application designed to help users find safer driving routes by integrating real-time crime data from Montgomery County, MD. It provides turn-by-turn directions and highlights recent crime incidents along the suggested path, allowing users to make more informed decisions about their travel.

About The Project
This application was built to provide a proof-of-concept for a navigation tool that prioritizes safety. It leverages the Google Maps API for routing and the Socrata Open Data API for crime statistics.

Key Features:

Dynamic Route Planning: Enter a start and end destination to receive driving directions.

Crime Data Integration: Fetches and displays recent crime incidents from the official Montgomery County data portal.

Proximity Alerts: Automatically identifies and lists crimes that have occurred near your proposed route.

User-Sourced Reports: A simple system for users to submit their own safety reports (e.g., poor lighting, suspicious activity), which are stored in a local database.

Safety Tips: A dedicated page with general safety advice.

Getting Started
Follow these steps to get a local copy up and running.

Prerequisites
Before you begin, you will need to set up your environment variables. The application uses the Google Maps API, which requires a key.

Create an environment file:
In the root directory of the project, create a file named .env.

Add your API Key:
Inside the .env file, add your Google Maps API key like this:

GOOGLE_MAPS_API_KEY="YOUR_API_KEY_HERE"

Set a Flask Secret Key:
For the flash() messaging system to work, you need to set a secret key in app.py. Open the app.py file and add a secret key right after the app = Flask(__name__) line:

app = Flask(__name__)
app.secret_key = 'your-very-secret-and-unique-key' # Add this line

Installation
Clone the repository (if applicable) or use your local files.

Create a virtual environment:
It's highly recommended to use a virtual environment to manage project dependencies.

# For Mac/Linux
python3 -m venv venv
source venv/bin/activate

# For Windows
python -m venv venv
.\venv\Scripts\activate

Install dependencies:
Install all the required Python packages from the requirements.txt file.

pip install -r requirements.txt

Usage
Once the installation is complete, you can run the Flask application.

Make sure you are in the root directory of the project.

Run the main application file:

python app.py

The application will start a local development server. You can access it by opening your web browser and navigating to:

http://127.0.0.1:5000

Testing
The project includes a suite of unit tests to ensure the application's core components are working correctly. The tests are located in the tests/ directory.

To run all the tests, navigate to the root directory of the project and execute the following command:

python -m unittest discover tests

This command will automatically discover and run all test files within the tests directory, providing a summary of the results.