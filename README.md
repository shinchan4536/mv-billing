# M.V. Billing System: Enterprise Dual-Shop POS & Real-Time Analytics

A production-ready, full-stack Point of Sale (POS) and inventory management application engineered using Python and Django. This system digitizes and automates manual ledger workflows for a high-volume retail environment managing two distinct business operations under one unified platform.

---

## 🚀 Key Architectural Features

### 1. Dual-Storefront POS Engine
- **Color World (Paint Retail):** Implements automated Indian GST billing compliant with local commercial standards.
- **Electricals Shop:** Provides high-velocity retail logging optimized for non-GST day-to-day transactions.

### 2. Automated GST & Compliance Engine
- Automatically computes base prices from inclusive retail rates using a backend mathematical extraction engine.
- Dynamically identifies and binds products to individual **HSN codes** to calculate exact, split **CGST and SGST** values on printer-optimized tax invoices.

### 3. Live Metrics Analytics Dashboard
- Leverages advanced Django ORM database aggregation (`Sum`, `F` objects) to instantly process live data.
- Dynamically computes and displays operational KPIs: **Today's Total Combined Revenue**, **Active Customer Invoice Volume**, and **Low-Stock Critical Reorder Alerts**.

### 4. Bank-Grade Session Security
- Utilizes short-lived, transient browser cookies configured with a custom 30-minute inactivity timeout.
- Implements a RAM-backed caching session engine (`django.contrib.sessions.backends.cache`). Login sessions reside exclusively in volatile server memory, ensuring all active connections instantly terminate if the local hosting server goes offline.

### 5. Automated Local Kiosk & Cloud Pipeline
- Features a custom, lightweight Windows Batch execution script (`.bat`) that triggers the Django server in the background and launches Google Chrome in full-screen Application Mode (`--app`).
- Paired with background database mirroring (`db.sqlite3`) syncing straight to the cloud for automated, zero-cost disaster recovery and near-zero RPO (Recovery Point Objective).

---

## 🛠️ Technical Stack

| Layer | Technology |
|---|---|
| Backend Engine | Python 3, Django Framework |
| Database Management | SQLite3 (Local Relational Storage Architecture) |
| Frontend UI/UX | Bootstrap 5, Custom CSS3, Vanilla JavaScript |
| Print Engine | CSS Media Queries (`@media print`) optimized for A4 single-sheet layout |
| Automation | Windows Batch Scripting |

---

## 📂 Project Architecture Layout

```text
├── billing/
│   ├── models.py       # Dual inventory & invoice relational database tables
│   ├── views.py        # Core analytics math, aggregations, & transaction processors
│   ├── urls.py         # App-level application endpoints
│   └── templates/      # Rich HTML5 invoice matrices & metrics dashboard
├── core/
│   ├── settings.py     # Cache session configurations & core global constants
│   └── urls.py         # Global routing nexus
├── start_billing.bat   # 1-Click desktop kiosk script launch system
├── manage.py           # Django administrative CLI gateway
└── requirements.txt    # Application software dependencies
```

---

## ⚡ Quick Start & Deployment Guide

### Prerequisites

Ensure Python 3.x and Google Chrome are installed on the local deployment machine.

### 1. Repository Installation

Clone this repository to the designated target directory:

```bash
git clone https://github.com/YOUR_USERNAME/mv-billing-system.git
cd mv-billing-system
```

### 2. Dependency Resolution

Initialize your environment and install the required dependencies:

```bash
pip install django
```

### 3. Database Initialization

Run the schema migrations to instantiate the relational tables:

```bash
python manage.py makemigrations
python manage.py migrate
```

### 4. Create an Administrative User

Generate credentials to access the analytics and management backend portal:

```bash
python manage.py createsuperuser
```

### 5. Production Kiosk Mode

To launch the app as a desktop kiosk native application, verify that your local filepath directory is explicitly mapped inside the `start_billing.bat` script, then simply double-click the file shortcut icon from the desktop interface.

```
Double-click: start_billing.bat
```

---

## 🛡️ License & Acknowledgments

Built as a custom, secure software utility to automate retail tracking pipelines and high-volume billing logic. Designed and engineered for commercial applications.
