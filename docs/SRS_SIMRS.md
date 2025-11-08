simrs/
│
├── docs/        → SRS, UML, Diagrams
├── src/         → Flask code (later)
├── tests/       → pytest scripts (later)
├── assets/      → diagrams, screenshots
└── README.md
Software Requirements Specification (SRS)

Project: Smart Incident Management & Response System (SIMRS)
Prepared by: Swetha Dixit| Deliverable      | Description                               | Format       |
| ---------------- | ----------------------------------------- | ------------ |
| SRS Document     | Functional + Non-Functional Requirements  | Markdown/PDF |
| Use Case Diagram | Actors + System Interactions              | PNG          |
| Class Diagram    | Object relationships + patterns           | PNG          |
| GitHub Repo      | Initialized and organized for next sprint | Online       |

Course: 3CS201PC302 – Software Engineering and System Design
Date: November 2025

1. Introduction

Purpose:
The purpose of SIMRS is to provide a centralized platform for reporting, tracking, and resolving incidents in real-time. It improves organizational responsiveness through automation, notifications, and analytics.

Scope:
The system allows users to log incidents, assign priorities, update statuses, and view dashboards. It notifies concerned personnel via web alerts or email/SMS and supports integration with mapping APIs for location-based visualization.

Definitions & Abbreviations:

Incident: Any abnormal event requiring attention.

SIMRS: Smart Incident Management & Response System.

API: Application Programming Interface.

CI/CD: Continuous Integration / Continuous Deployment.

References:
IEEE 830 standard, Flask documentation, GitHub Actions guide, OMDb and Google Maps API docs.

2. Overall Description

Product Perspective:
SIMRS is a client–server web application built on the MVC architecture using Flask and JavaScript. It interacts with third-party APIs for alerts and location data.

Product Functions:

User registration and authentication

Incident reporting with category, priority, and location

Admin dashboard for managing incidents

Automatic notification system (Observer pattern)

Analytics visualization (resolved vs pending incidents)

User Characteristics:

Admins – manage all incidents and users.

Employees – report incidents.

Technicians – resolve incidents.

Constraints:

Internet connection required for API calls.

Response latency ≤ 3 seconds for core actions.

Deployment using free tier hosting (Render/Vercel).

Assumptions & Dependencies:

Users have browser access.

API keys available for external services.

3. Specific Requirements

Functional Requirements:

ID	Requirement	Priority
FR1	User Login and Role Management	High
FR2	Create Incident Record (title, desc, priority, location)	High
FR3	View/Edit/Delete Incident	High
FR4	Send Notification to Subscribers	Medium
FR5	Visualize Incident Map (Google API)	Medium
FR6	Generate Reports/Stats	Low

Non-Functional Requirements:

Reliability ≥ 99% uptime (for conceptual system)

Usability – simple responsive UI

Security – input validation + hashed passwords

Maintainability – modular Python structure

Portability – works on Linux (Flask server)

4. External Interface Requirements

User Interface: Web dashboard (HTML/CSS/JS)

Hardware: Standard browser & Internet connection

Software: Flask, SQLite/MySQL, GitHub Actions, Ubuntu 22.04

Communications: REST APIs (HTTP/HTTPS)

5. System Features

Detailed text for each FR (FR1–FR6) — describing inputs, process, outputs.
Example for FR2:

Input: Incident title, description, category, priority, location
Process: Store in DB, trigger notifications
Output: Success message + incident ID

6. Other Requirements

System to support role-based access control.

Future scope: integration with IoT sensors for automatic alerts.

7. Appendices

Include references, authorship, and revision history table.