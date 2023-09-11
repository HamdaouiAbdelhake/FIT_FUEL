# FIT FUEL Web Application
#### Video Demo:
#### Description:

**FIT FUEL** is a web application designed to help users track their daily calorie and macronutrient intake. The app leverages the USDA API to provide accurate and up-to-date information about food macros and calories. It includes user registration and login functionality and is built using HTML, JavaScript, CSS, and Python with the Flask framework. Additionally, the app offers features to download data to a CSV file and reset the day's food data for convenient tracking.

## Features

### User Registration and Login

- **User Registration:** New users can create accounts by providing a username and password. This allows them to store and track their daily food intake over time.

- **User Login:** Registered users can log in with their credentials to access their personalized food tracking data.

### Calorie and Macronutrient Tracking

- **Food Search:** Users can search for foods and retrieve detailed information, including calories, proteins, carbohydrates, and fats, using the USDA API.

- **Food Entry:** Users can add individual food items to their daily intake, specifying the quantity consumed.

- **Daily Totals:** The app calculates and displays the total calories, proteins, carbohydrates, and fats consumed for the day.

### Data Export

- **CSV Download:** Users have the option to download their daily food intake data as a CSV file for easy record-keeping and analysis.

### Reset Daily Data

- **Reset Functionality:** Users can reset their daily food intake data, allowing them to start fresh for the day.

## Technologies Used

- **Front-end:** HTML, JavaScript, CSS
- **Back-end:** Python with Flask framework
- **External API:** USDA API for food information

## Getting Started

To run FIT FUEL locally on your machine, follow these steps:

1. Clone the repository from GitHub.

   ```bash
   git clone https://github.com/HamdaouiAbdelhake/FIT_FUEL
   cd fit-fuel
   ```

2. Install the required dependencies.

    ```bash
    pip install -r requirements.txt
    ```
3. Run application
    ```bash
    flask run
    ```
Access the app in your web browser at http://localhost:5000.

## Usage

- Register for a new account or log in with your existing credentials.

- Use the search feature to find and select the food items you've consumed throughout the day.

- Add the quantity consumed for each food item.

- The app will calculate and display your daily calorie and macronutrient totals.

- Optionally, download your daily food intake data as a CSV file.

- Reset your daily data to start tracking for a new day.

## Credits

- **USDA API**: This app relies on the USDA API to provide accurate food macros and calorie information. Visit the [USDA Food Composition Databases to obtain an API key](https://fdc.nal.usda.gov/api-guide.html).

## Contributors

- [**Abdelhake Hamdaoui**](https://github.com/HamdaouiAbdelhake)

We hope you find **FIT FUEL** helpful in your journey to track your calorie and macronutrient intake and maintain a balanced diet!