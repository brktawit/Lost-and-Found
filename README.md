**Lost and Found Web Application**

**Project Overview**

This project aims to develop a **Lost and Found Web Application** that allows users to report and manage lost items. The system will provide a way to track lost and found items, ensuring that people can recover their belongings more easily.

Additionally, the project will integrate an **ETL (Extract, Transform, Load) process** using publicly available datasets from Kaggle. 

## Objectives

- To create a **user-friendly web platform** for reporting and managing lost items.
- To implement **CRUD operations** to allow users to Create, Read, Update, and Delete lost item records.
- To integrate an **ETL process** for importing external datasets related to lost items.
- To Maintain a **scalable database** to handle both user-generated data and external datasets.
- To implement **user authentication and role-based access**, allowing different user permissions.


## Key Features

### 1. **User Roles & Authentication**
   - **Admin:**
     - Can manage categories (add, delete).
   - **Registered Users:**
     - Can create, update, and delete lost item records.
   - **Guests:**
     - Can view all lost and found items.

### 2. **Lost and Found Item Management**
   - Users can post details about lost items.
   - Ability to update or delete lost item posts.

### 3. **Categories Management**
   - Admin can create and delete categories for better organization.

### 4. **ETL (Extract, Transform, Load) Process**
   - **Extract:** Publicly available datasets related to lost and found reports will be sourced from **Kaggle** database.
   - **Transform:** The data will be **cleaned, filtered, and formatted** to match the database schema of the application.
   - **Load:** Processed data will be **integrated** into the system.

   - **Data Sources:** Kaggle database and user-generated data.


## Technologies to be Used

| Component      | Technology |
|---------------|------------|
| Frontend      | HTML, Bootstrap, JavaScript |
| Backend       | Python (Flask) |
| Database      | PostgreSQL with PostGIS |
| ETL Pipeline  | Pandas, PostgreSQL, SQLAlchemy |
| Data Sources  | Kaggle datasets, user-generated reports |
| Tools         | Miniforge, Postman, pgAdmin4, VS Code |

## Project Scope & Work Plan

### **Phase 1: Research & Planning (Completed)**
- Define project requirements and objectives.
- Choose appropriate technology stack.

### **Phase 2: Backend Development (In Progress)**
- Set up the Flask backend.
- Implement database models and API routes.

### **Phase 3: ETL Pipeline Implementation (Upcoming)**
- Identify relevant datasets from Kaggle.
- Develop data extraction and transformation scripts.
- Load the cleaned data into the database.

### **Phase 4: Frontend Development (In Progress)** 
- Develop login, registration, and homepage UI.
- Implement item posting and management UI.

### **Phase 5: Testing & Refinements**
- Conduct user testing.
- Fix bugs and optimize performance.

## Potential Enhancements
- provide an **interactive map** displaying lost items' locations 
- Improve **UI/UX design** for better user experience.

---

## Authors

**Thomas Waliba**  
**Augustine Ofobi** and,
**Brktawit Haftu**


---

This file outlines the planned features and development stages of our Lost and Found application. Feedback and suggestions are welcome!
