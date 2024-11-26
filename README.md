# Adaptive Shield Assignment

This repository contains the home assessment for Adaptive Shield. It demonstrates the functionality of a web scraper and a Flask-based application to map collateral adjectives to animals, presenting the results in a simple UI.

---

## Getting Started

Follow the instructions below to set up and run the application.

### Prerequisites

Ensure you have Python installed on your machine. You can install the required dependencies using `pip`.

### Setup Instructions

1. Clone this repository to your local machine:

   ```bash
   git clone <repository-url>
   cd adaptive-shield-assignment
   ```

2. Install the necessary dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. **Run the scraper:**
   Execute the `scraper.py` file to gather and process the data. This step is crucial, as it prepares the results for the web application:

   ```bash
   python scraper.py
   ```

4. Start the Flask application:
   ```bash
   python -m flask run
   ```
   By default, the application will run on `127.0.0.1:{port}`. Open your browser and navigate to `/` for the interface.

---

## Features and Notes

- **Result Mapping:**  
  The mapping of collateral adjectives to animals is saved in the `RESULT.txt` file.

- **Image Downloads:**  
  Downloaded images are stored in the `/tmp` directory.

  - The image downloader uses 4 threads for efficiency. This configuration balances speed and resource usage but can be adjusted if needed.

- **Handling Missing Data:**  
  Animals without specified collateral adjectives are excluded from the mapping. This decision aligns with the task's objective but can be revised upon request.

---

## Preview

Below is a preview of the user interface:

<img width="1399" alt="Preview of the UI" src="https://github.com/user-attachments/assets/5a3ee928-fcc9-4138-bbbf-ef3b9ea661e6">

---

Feel free to contact me for any clarifications or additional requirements.
