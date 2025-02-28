# Project 1: Online Commerce


## Team Members
- **Robbie Rasor** – Team Lead
- **[Teammate 1]** – Development Engineer
- **Max Montes Soza** – Test Engineer
- **[Teammate 3]** - Documentation Specialist
- **Jacob Goodgame** - General Developer


## Testing Approach
We...:

- **Unit Testing**: Text...
- **Integration Testing**: Text...
- **Test-Driven Development**: Text...

## Notable Features
- **Feature 1**: Good feature. Well done.

## Installation & Setup
- Will need to update before we submit to have info for aviram + ta rather than for us

### **0. Clone the repository:**
```sh
git clone https://github.com/rasorro/Project_1.git
cd Project_1
```
- Your command may be different, check you're able to pull and push before you start working to save a headache at the end. Setting up an ssh key so I could push and commit took a while for me to figure out.

### **1. Create a Virtual Environment (only done once)**
```sh
python3 -m venv .venv
```

### **2. Activate the Virtual Environment (do every time you start working on project)**
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

### Running the Tests
```sh
pytest
```
- View coverage of tests:
    ```sh
    coverage run -m pytest
    ```
