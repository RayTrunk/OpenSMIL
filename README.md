# OpenSMIL Signage

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.10%2B-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100%2B-009688.svg)

**OpenSMIL Signage** is an open-source, highly scalable Digital Signage backend fully compliant with the **SMIL 3.0** (Synchronized Multimedia Integration Language) standard. 

It provides a modern API to manage media assets, assemble playlists, and dynamically generate SMIL 3.0 XML files for digital signage players (e.g., BrightSign, IAdea, ViewSonic, or custom a-smil players) to poll and play.

## 🚀 Vision

Many commercial Digital Signage CMS solutions are heavily proprietary. OpenSMIL bridges the gap by offering a robust, community-driven backend that outputs pure, standardized SMIL 3.0. It is designed to be accessible for simple local setups while effortlessly scaling to manage thousands of displays globally.

**Core Languages:** The primary language for the UI and documentation is English, with full native support for German.

## ✨ Key Features

* **SMIL 3.0 Generation:** Dynamically translates visual playlist logic into valid SMIL XML (`<seq>`, `<par>`, `<layout>`, `<region>`).
* **Multi-Tenancy (IAM):** Built-in role-based access control (Admin/Client) using JWT. Clients only see and manage their own players and media.
* **Flexible Media Storage:** * Local filesystem storage for rapid development and small deployments.
  * S3-compatible object storage (e.g., Hetzner, AWS, MinIO) for production environments.
* **Database Agnostic:** Powered by SQLModel. Uses SQLite for zero-config local setups and MariaDB/PostgreSQL for heavy-duty production.
* **Player Polling:** Optimized endpoints to handle thousands of simultaneous hardware requests efficiently.

## 🛠️ Tech Stack

* **Backend Framework:** [FastAPI](https://fastapi.tiangolo.com/) (Python)
* **ORM & Database:** [SQLModel](https://sqlmodel.tiangolo.com/) (SQLAlchemy + Pydantic)
* **Authentication:** OAuth2 with JWT (JSON Web Tokens)
* **Databases:** SQLite3 (Dev/Local) / MariaDB (Production)
* **Storage:** Local / `boto3` for S3-compatible storage

## 📂 Architecture Overview

```text
smil-backend/
├── app/
│   ├── api/          # RESTful endpoints (Players, Media, Playlists, Auth)
│   ├── core/         # Security, JWT, and Configuration
│   ├── models/       # SQLModel database schemas
│   ├── services/     # Business logic (SMIL Builder, Storage Router)
│   └── locales/      # i18n files (en.json, de.json)
├── data/             # SQLite database volume
└── media_local/      # Local storage fallback
