# **Film & TV Contract Compliance System**

### **Project by Raghuveer Kattepogu**

---

## **Overview**

This project is a Film and TV Background Extra Contract Compliance System. It is designed to manage background actors, also called extras, in a simple and organized way. In many productions, this work is handled manually using spreadsheets, emails, and paper records. Because of that, mistakes can happen in scheduling, working hours, and payments. This system brings everything into one place so that the process becomes easier, more accurate, and more reliable.

The system allows different users such as extras, coordinators, HR staff, payroll staff, and admin to perform their tasks based on their roles. It also checks rules like working hours, break time, and contract conditions to make sure everything follows proper guidelines.

---

## **Project Objective**

The main goal of this system is to replace manual tracking with a structured software solution. It helps in managing assignments, work sessions, compliance checks, and payroll processing in a clear and consistent way. The system also reduces errors, improves efficiency, and keeps all records safe for future use.

---

## **Key Features**

* User login and role-based access control
* Extra profile management and availability tracking
* Production and scene creation
* Assign extras to scenes with validation checks
* Work session recording with time and break tracking
* Contract acknowledgment before work
* Compliance checking for working hours and rules
* Payroll processing with overtime and calculations
* Dispute submission and resolution
* Report generation in CSV, JSON, and PDF formats
* Audit logging for all actions

---

## **System Roles**

* **Extra / Actor** → Manage profile, view assignments, record work, submit disputes
* **Production Coordinator** → Create productions, assign extras, manage schedules
* **HR Staff** → Validate work sessions and compliance
* **Payroll Staff** → Calculate and process payments
* **System Admin** → Manage users, roles, and system settings

---

## **System Requirements**

* Python 3.8 or higher
* Streamlit (if UI is used)
* SQLite3
* Basic Python libraries

---

## **How to Run the Project**

1. Download or clone the project
2. Open terminal in the project folder
3. Install required packages

```bash
pip install streamlit
```

4. Run the application

```bash
streamlit run FilmandTVContractComplianceSystem.py
```

---

## **System Workflow**

1. User logs into the system
2. Coordinator creates production and scenes
3. Extras are assigned to scenes
4. Extras acknowledge contracts
5. Extras record work sessions
6. System checks compliance rules
7. HR validates work sessions
8. Payroll processes payments
9. Reports are generated
10. Audit logs track all actions

---

## **Database Overview**

The system uses a structured database to store:

* Extras
* Productions
* Scenes
* Assignments
* Work sessions
* Payroll records
* Disputes

All tables are connected using primary keys and foreign keys to maintain data accuracy.

---

## **Future Improvements**

* Add notification system for updates
* Improve UI for better user experience
* Add real-time validation alerts
* Cloud database support
* Advanced reporting dashboard

---

## **Conclusion**

This system provides a complete solution for managing background extras in film and TV production. It improves accuracy, reduces manual work, and ensures compliance with rules and contracts. It is simple to use, reliable, and can be extended further in the future.
