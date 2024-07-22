# HardPick

HardPick is a web application designed to help you find the best computer within your budget. By leveraging the power of Python, Node.js, and Flask, HardPick ensures a seamless and efficient experience for users looking to make informed purchasing decisions.

## Table of Contents

- [Features](#features)
- [How it works](#how-it-works)
- [Installation](#installation)
- [Usage](#usage)
- [Technologies Used](#technologies-used)
- [Contributing](#contributing)


## Features

- **User-Friendly Interface**: Easy-to-navigate interface to input budget and preferences.
- **Real-Time Data**: Fetches the latest computer hardware data.
- **Budget Optimization**: Recommends the best computer configuration within your specified budget.
- **Multi-Platform**: Accessible via desktop and mobile devices.

## How it works:
The front-end web application is built using JavaScript. Users input their desired PC specifications and budget, which are then sent as a request to an API built with Flask. This API scrapes various sites in Tunisia that sell PCs, benchmarks the components by scraping other websites, and assigns a score to each component. Based on these scores, the application renders a final result, recommending the best computer configuration within the user's budget.

## Installation

### Prerequisites

- Python 3.x
- Node.js and npm
- Flask
- beautifulSoup

### Steps

1. Clone the repository:
    ```bash
    git clone https://github.com/Amine-Zitoun/hardpick.git
    cd hardpick
    ```

2. Set up the backend:
    ```bash
    cd backend
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    ```

3. Set up the frontend:
    ```bash
    cd ../frontend
    npm install
    ```

4. Run the application:
    ```bash
    cd ../backend
    flask run
    cd ../frontend
    npm start
    ```

## Usage

1. Open your web browser and navigate to `http://localhost:3000`.
2. Enter your budget and preferences.
3. Get recommendations for the best computer configuration within your budget.

## Technologies Used

- **Python**: Backend processing and data handling.
- **Flask**: Web framework for the backend.
- **Node.js**: JavaScript runtime for the frontend development.
- **React**: (or your chosen front-end framework) for building user interfaces.
- **APIs**: For fetching real-time data on computer hardware.

## Contributing

Contributions are welcome! Please fork this repository and submit a pull request for review.

1. Fork the repository.
2. Create a new branch:
    ```bash
    git checkout -b feature-branch
    ```
3. Make your changes and commit them:
    ```bash
    git commit -m "Description of your changes"
    ```
4. Push to the branch:
    ```bash
    git push origin feature-branch
    ```
5. Submit a pull request.


