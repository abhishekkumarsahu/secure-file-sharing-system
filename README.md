# Secure File Sharing System (Backend API)

---

## 📚 Project Purpose

This project is a **secure file-sharing system** built using Django REST Framework.  
It allows two types of users:
- **OPS User**: Can upload `.docx`, `.pptx`, `.xlsx` files.
- **Client User**: Can sign up, verify email, view available files, and download them using secure links.

✅ Secure download system using **encrypted links**.  
✅ Email verification system before login.  
✅ Only authorized users can perform specific actions.

---

## ✨ Features

- **Client Signup** with email verification (via token link)
- **Email verification system** before allowing login
- **JWT Authentication** (Access & Refresh tokens)
- **OPS User File Upload** (Only `.docx`, `.pptx`, `.xlsx`)
- **Client User File Listing**
- **Secure Download Links** (token-based, expire after time)
- **Role-based Access Control** (OPS vs Client)
- **Error handling** for unauthorized access
- **Unit Tests** for major APIs
- **Postman Collection** provided

---

## 🛠 Tech Stack

- **Backend**: Django, Django REST Framework
- **Authentication**: JWT (SimpleJWT)
- **Token Security**: Itsdangerous
- **Database**: Default SQLite (easy to switch to PostgreSQL)
- **API Testing**: Postman
- **Deployment**: Render / Heroku ready
- **Language**: Python 3

---

## 💻 How to Run Locally

### 🛠 Setup Instructions

1. Clone the repository
   ```bash
   git clone https://github.com/abhishekkumarsahu/secure-file-sharing-system.git
   cd secure-file-sharing-system
2. Create and activate a virtual environment
    ```bash
    python -m venv venv
    source venv/bin/activate   # On Windows: venv\Scripts\activate

3. Install project requirements
    ```bash
    pip install -r requirements.txt

4. Apply database migrations
    ```bash
    python manage.py makemigrations
    python manage.py migrate
    
5. Run the development server
   ```bash
   python manage.py runserver

6. Base API URL
   ```bash
   http://127.0.0.1:8000/api/
   
---

## Email System Information

- Email Backend: Console email backend (for development).
- Location: Check your terminal output after signup to find the email verification link.
- Production Ready: Easy to switch to SMTP servers (like Gmail) for sending real emails.

---

## 🚀 API Endpoints

- API Action	Endpoint	Method	Auth Required	User Role
- Client SignUp	/api/signup/	POST	❌	New Users
- Verify Email	/api/verify-email/?token=	GET	❌	New Users
- Login (JWT)	/api/login/	POST	❌	Verified Users
- Refresh Token	/api/token/refresh/	POST	❌	Verified Users
- Upload File (OPS only)	/api/upload/	POST	✅	OPS
- List Uploaded Files (Client)	/api/files/	GET	✅	Client
- Generate Secure Download URL	/api/download-link/<file_id>/	GET	✅	Client
- Download File Securely	/api/download-file/?token=<token>	GET	✅	Client

---

## 🧪 Example API Usage (Postman)

### 1. Client Signup
**POST** `/api/signup/`

      ```json
      {
        "username": "clientuser",
        "email": "client@example.com",
        "password": "password123"
      }
  - ➡️ After signup, check your terminal for the email verification link.
  - ➡️ Open the link in your browser to verify the email.

### 2. Client Login (After Email Verified)
**POST** `/api/login/`

    ```json
    {
      "username": "clientuser",
      "password": "password123"
    }
  - ➡️ You will receive Access and Refresh tokens.

### 3. OPS User Upload File

**POST** `/api/upload/`

### Headers:
- `Authorization: Bearer <access_token>`

### Body:
- form-data → Key: `file`
- Select a `.docx`, `.pptx`, or `.xlsx` file

➡️ Only **OPS** users are allowed to upload files.

---

## 4. Client List Files and Download Securely

- **GET** `/api/files/` → List all uploaded files
- **GET** `/api/download-link/<file_id>/` → Generate secure download link
- **GET** `/api/download-file/?token=<token>` → Download file securely

---

## 🧹 Project Highlights

- Strong validation to allow **only OPS users** to upload files.
- Strong validation to allow **only Client users** to download files.
- Only **email-verified users** can login and access the system.
- **Secure encrypted URLs** for file download with time expiration.
- **Role-Based Access Control** implemented clearly and securely.

---

## 🙋‍♂️ Author Info

- **Name**: Abhishek
- **Project**: Secure File Sharing System
- **Role**: Backend Developer (Intern Level)
- **Skills**: Django, DRF, JWT Authentication, Postman API Testing, Git, Production Deployment

---

## 📦 Extras

- 🛠 `requirements.txt` included.
- 📤 Postman Collection (`Secure File Sharing API.postman_collection.json`) provided.
- 📄 `Procfile` included for easy Heroku/Render deployment if needed.
- 🚀 Ready for Docker deployment if needed.
- 🔒 Secure JWT-based authentication and email verification flow implemented.

---

# 📢 Thank You for Reviewing This Project!



   

  
