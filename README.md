# Project 1

## Setup Instructions

### **1. Create a Virtual Environment**
```sh
python3 -m venv .venv
```

### **2. Activate the Virtual Environment**
- On **macOS/Linux**:
    ```sh
    source .venv/bin/activate
    ```
- On **Windows**
    ```sh
    .venv\scripts\activate
    ```
### **3. Install Dependencies**
```sh
pip install -r requirements.txt
```
## Useful Info

### If you install a new package, update 'requirements.txt':
```sh
pip freeze > requirements.txt
```

### Running the Application
```sh
flask --app flaskr run
```
