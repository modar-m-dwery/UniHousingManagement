# University Housing Management System

## Project Description

The University Housing Management System is designed to manage university housing units. The system includes a set of housing units that consist of floors, with each floor containing multiple rooms. The system allows the administrator to manage these units fully, including adding, deleting, and modifying them. It includes a detailed layout of the housing units in terms of rooms and hallways.

## Roles and Permissions

### Administrator

- **Permissions**: Manage adding, deleting, and modifying housing units, floors, and rooms.
- **Dashboard**: Access to all details related to housing units and workers within them, including viewing reports.

### Staff

#### Senior Unit Supervisor

- **Permissions**: View unit details, manage workers, and follow reports.
- **Dashboard**: Contains unit details and detailed reports.

#### Workers

- **Types of Workers**:
  - Maintenance Workers
  - Cooks
  - Garden Coordinators
- **Permissions**: View tasks assigned to each worker based on their specialization.

### Students

- **Permissions**:
  - Book rooms, where one room can accommodate more than one student.
  - Submit complaints to be addressed by the workers.

## Reports

The system provides detailed reports on all activities and operations conducted within the housing units.

## Technologies Used

- **Backend**: Django
- **Frontend**: HTML, CSS, JavaScript, jQuery

## Getting Started

### Clone the repository:

```bash
git clone https://github.com/modar-m-dwery/UniHousingManagement.git

Navigate to the project directory:

bash

cd UniHousingManagement

Install the requirements:

bash

pip install -r requirements.txt

Run the server:

bash

python manage.py runserver
