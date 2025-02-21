## 👨‍💻 Authors

**Thomas Liyajabale Waliba**  
**Augustine Ofobi Aborah**  
**Brktawit Haftu Belay**


# 📌 Lost Item Reporting System
A web-based application designed for police stations, schools, third-party organizations, or any entity that manages lost and found items.

## 📖 Overview
This Lost Item Reporting System is designed to help institutions like police stations, schools, airports, companies, and third-party organizations efficiently track and manage lost items. Unlike a traditional "Lost & Found" system where users report missing items, this system allows users to report only the items they found. Admins (e.g., a police officer, school administrator, or office manager) oversee the system, manage reports, and return lost items to the rightful owners.

## 🌟 Features

### 🛠️ Admin Functionalities
- ✅ Manage Categories: Create, update, and delete item categories.
- ✅ View All Reported Items: Admins can see all found items reported.
- ✅ Manage Reported Items: Admins can Create, update, and delete all the reported items
- ✅ Ensure Secure Handling: Lost items are only returned after proper verification.

### 🙋‍♂️ User Functionalities (Finders) 
- ✅ Report Found Items: Users can submit a form to register an item they found.
- ✅ Manage Their Own Reports: Users can edit or delete their own reported items.

### 📊 ETL (Extract, Transform, Load) Process
🔗 Data Sources: Kaggle database and User-generated data

The system incorporates an ETL (Extract, Transform, Load) process to manage data effectively:
- ✅ Extract: Publicly available datasets related to lost and found reports are sourced from the Kaggle database.
- ✅ Transform: The extracted data is then cleaned, filtered, categories assigned, locations geocoded and formatted to ensure it aligns with the database schema of the application.
- ✅ Load: Finally, the processed data is integrated into the system for use.

### 🗺️ Geospatial Features
- ✅ Location Tracking: When an item is reported, it can be pinned on a map.
- ✅ Integrated with OpenStreetMap: Users can add lost item locations interactively.
- ✅ Uses PostGIS to store found item locations.

### 🔐 Security & Access Control
- ✅ Admin-Only Reports: Only admins can see all reported items.
- ✅ Users Cannot View Lost Items: They must visit the office to claim their lost belongings.
- ✅ Secure User Authentication: Users and admins log in with unique credentials.

### 🔍 Search and Filter Functionality
The system includes a general search functionality that allows users to search for reported items by keywords. Additionally, users can filter reported items by category, enabling them to easily find specific items based on their type or classification.

### 📄 Pagination
To enhance user experience, the system implements pagination for the list of reported items. Users can view the reported items in batches of 10 items per page, allowing for easier navigation and quicker access to specific entries. Users can navigate through the pages using provided controls to view additional items.

## 📂 Folder Structure
lost-and-found/ ├── etl/ │ ├── extract/ │ │ └── fetch_kaggle_data.py # Downloads dataset │ ├── transform/ │ │ ├── drop_unnecessary_fields.py # Cleans dataset │ │ ├── assign_categories.py # Auto-assigns categories │ │ ├── add_coordinates.py # Adds geospatial mapping │ │ └── station_coordinates.py # For storing station coordinates dictionary │ ├── load/ │ │ └── insert_to_db.py # Loads data into database │ ├── data/ │ │ ├── raw/ # Original dataset │ │ └── processed/ # Transformed dataset │ └── main_etl.py # ETL execution script ├── routes/ │ ├── items.py # Routes for item management │ ├── categories.py # Routes for category management │ ├── login.py
│ ├── logout.py │ ├── protected.py
│ └── register.py
├── models/ │ ├── user_model.py # User schema │ ├── item_model.py # Item schema │ └── category_model.py # Category schema ├── templates/ │ ├── about.html # About us page ├── base.html # Main template │ ├── home.html # Home page │ ├── login.html # Login page │ ├── register.html # Register page │ ├── manage_items.html # Item management UI │ ├── manage_categories.html # Category management UI │ └── add_item.html
├── static/ │ ├── css/style.css # Custom styles │ ├── js/add_location.js │ ├── js/delete_categories.js │ ├── js/delete_items.js │ ├── js/fetch_items.js │ ├── js/login.js │ ├── js/manage_categories.js │ ├── js/register.js │ └── js/update_items.js ├── database/ │ └── db.py # Database connection ├── app.py # Main application entry point ├── requirements.txt # installed dependencies └── README.md # Documentation

## 🛠️ Technologies Used

| Component      | Technology                               |
|----------------|------------------------------------------|
| Frontend       | HTML, css, Bootstrap, JavaScript              |
| Backend        | Python (Flask), Flask-SQLAlchemy         |
| Database       | PostgreSQL with PostGIS                  |
| Geospatial     |GeoAlchemy2, Leaflet.js                   |
| ETL Pipeline   | Pandas, SQLAlchemy                       |
| Data Sources   | Kaggle datasets, user-generated reports  |
| Tools          | Miniforge, Postman, pgAdmin4, VS Code    |


## 💻 Installation & Setup

1. **Clone the Repository**
```bash
git clone https://github.com/brktawit/Lost-and-Found
   cd Lost-and-Found
```

2. **Set Up a Virtual Environment**
```bash
python -m venv venv
source venv\Scripts\activate  # On Linux use:  venv/bin/activate
```

3. **Install Dependencies**
```bash
pip install -r requirements.txt
```

4. **Set Up Database**
- Ensure PostgreSQL with PostGIS is installed.
- Create a database named Trial (or modify the database configuration in app.py).
- Run migrations:
```bash
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

5. **Run the ETL process**
```bash
python etl/main_etl.py
```

6. **Run the Application**
```bash
flask run
```
The app will be available at: http://127.0.0.1:5000/

## 🔑 User Roles & Access

| User Role | Access                                                |
|-----------|------------------------------------------------------|
| Admin     | Manages categories, views and manages all reports |
| User      | Reports items they found, edits/deletes their own reports   |

## 🚀 API Endpoints

| Endpoint          | Method | Description                    | Access                      |
|-------------------|--------|--------------------------------|-----------------------------|
| /login/           | POST   | User login                    | Public                      |
| /logout/          | GET    | Logout user                   | Authenticated Users         |
| /register/        | POST   | Register a new user           | Public                      |
| /items/           | GET    | Get list of found items       | Authenticated Users         |
| /items/add_item   | POST   | Report a found item           | Authenticated Users         |
| /items/<id>      | PUT    | Edit a reported item          | Item Owner / Admin          |
| /items/<id>      | DELETE | Delete a reported item        | Item Owner / Admin          |
| /categories/      | POST   | Add a new category            | Admin                       |
| /categories/<id>  | PUT    | Edit category name            | Admin                       |
| /categories/<id>  | DELETE | Delete a category             | Admin                       |

## 📌 Notes
Lost item retrieval is handled physically at the organization’s office.










