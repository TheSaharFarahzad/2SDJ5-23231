# 2SDJ5-23231
Code Challenge Submission for Parstasmim .co Interview - Sahar Farahzad

## 1. Clone the Repository

To clone the repository initially:

```bash
git clone https://github.com/CodeWithSahar/2SDJ5-23231.git
cd 2SDJ5-23231
```

If you have already cloned the repository and want to update it, use:

```bash
git pull origin master
```

## 2. System Requirements

You'll need Python 3, python3-pip, and python3-venv to be installed on your machine.

## 3. Setup

In this section we explain how you can set up the project without Docker.

### 3.1 Python Environment

For a clean development setup, use a virtual environment:

Windows:
```bash
cd 2SDJ5-23231
python -m venv venv
venv\Scripts\activate
```

Linux:
```bash
cd 2SDJ5-23231
python3 -m venv .venv
source .venv/bin/activate
```

**NOTE**: Ensure you add your virtual environment directory to .gitignore to avoid committing unnecessary files to your repository.

To install all requirements for local development, run the following command:

```bash
pip install -r requirements/local.txt
```

### 3.2 Run Server

If you want to run the app locally, run the following command:

```bash
python manage.py runserver
```

You can see the application in a browser, at [http://localhost:8000](http://localhost:8000).
