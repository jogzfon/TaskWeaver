# TaskWeaver Demo: Biblio System

## Table of Contents
- [Introduction](#introduction)
- [Installation](#installation)
- [Prerequisites](#prerequisites)
- [Usage](#usage)
- [License](#license)

## Introduction
TaskWeaver is a code-first agent framework designed for seamlessly planning and executing data analytics tasks.

This demo utilizes **TaskWeaver** to query a sample database, specifically the *Biblio_system* database (Library Management System). The demo showcases the implementation and use cases of plugins from the TaskWeaver framework. The Large Language Model (LLM) used for this project is GPT-4o mini.

## Installation

1. Clone the Git repositories:
    - [TaskWeaver Repository](https://github.com/jogzfon/TaskWeaver.git)
    - [Frontend Repository](https://github.com/ElijahFernandez/TaskWeaver_frontend.git)

2. Install the required Python packages:
    ```bash
    pip install -r requirements.txt
    ```

3. Set up XAMPP or any database management software of your choice and import the following tables:
    - [Database Tables](https://drive.google.com/drive/folders/1Qqa2iprpSJ1WV7XVbRuwsEaH49I5af-k)

4. Navigate to `tw_backend/app.py` in the TaskWeaver directory and run the code using your IDE:
    ```bash
    python app.py
    ```

5. Navigate to `tw_frontend_next` in the frontend repository, open your terminal, and run:
    ```bash
    npm run dev
    ```

## Prerequisites
- Python 3.7+
- IDE (e.g., PyCharm, VSCode)
- XAMPP or DataGrip
- Node.js
- Next.js
- Flask

## Usage
### Running the Backend
1. Navigate to the backend directory:
    ```bash
    cd TaskWeaver/tw_backend
    ```
2. Run the application:
    ```bash
    python app.py
    ```

### Running the Frontend
1. Navigate to the frontend directory:
    ```bash
    cd TW_NJSn/tw_frontend_next
    ```
2. Start the development server:
    ```bash
    npm run dev
    ```
3. Open your browser and navigate to `http://localhost:3000` to view the application.


## License
This project is licensed under the MIT License. See the LICENSE file for details.
