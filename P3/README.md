# Project 3: A Real-World Database Application

The purpose of this project is to help people find activity groups in the city of Boston. While there are aspects of our system designed especially for college students, there is no particular demographic other than people who are in Boston and are in search of activity groups, whether it be sports, music, cooking, etc.


## Team Members
- **Robbie Rasor** – Team Lead
- **Charlie Keough** – Development Engineer
- **Max Montes Soza** – Test Engineer
- **Grant Zobel** - Documentation Specialist
- **Jacob Goodgame** - General Developer


## Testing Approach
- **Unit Testing**: Isolated tests for each function. Ensured all pages properly handle GET and / or POST requests and validate input as necessary.
- **Test-Driven Development**: Followed Test-Driven Development. If code pushed by devs failed tests, Test Engineer and Lead went back, examined, and refactored until all tests passed. This allowed for an opportunity to peer review each other's code.

## Notable Features
- Search bar updates while typing
- Search results are accent mark insensitive

## Installation & Setup

### **0. Clone the repository:**
```sh
git clone https://github.com/rasorro/Project_1.git
cd p3
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
    source .venv/Scripts/activate
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

### Initializing the database
```sh
flask --app app init-db
```

### Running the Application
```sh
flask --app app run
```

### Running the Tests
```sh
pytest
```
- View coverage of tests:
    ```sh
    coverage run -m pytest
    ```
