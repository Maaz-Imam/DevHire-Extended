# DevHire-Extended Python Project Setup Guide (Windows)

Welcome to the DevHire-Extended Python project! This guide will walk you through the process of setting up the project on a Windows machine.

## Clone the Repository

1. Fork this repository
2. Open Command Prompt or Git Bash.
3. Navigate to the directory where you want to clone the project.
4. Run the following command to clone the repository:

   ```bash
   git clone https://github.com/your-username/DevHire-Extended.git
   ```

   Replace `your-username` with your GitHub username.

## Create a Virtual Environment

1. Navigate to the project directory using Command Prompt or Git Bash:

   ```bash
   cd DevHire-Extended
   ```

2. Create a virtual environment:

   ```bash
   python -m venv venv
   ```

3. Activate the virtual environment:

   - Command Prompt:

     ```bash
     venv\Scripts\activate
     ```

   - Git Bash:

     ```bash
     source venv/Scripts/activate
     ```

## Install Dependencies

1. With the virtual environment active, install project dependencies using pip:

   ```bash
   pip install -r requirements.txt
   ```

## Setup configuration

1. copy the file DevHireExtended/constants-template.py using:
    ```bash
       cp DevHireExtended/constants-template.py DevHireExtended/constants.py 
    ```
2. Setup your OPENAI key (or any other keys) in that file and access it in production

## Run Django

1. In the Root directory run the following command:
   ```bash
   python3 DevHireExtended/manage.py runserver
   ```