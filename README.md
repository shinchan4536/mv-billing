# 🛒 M.V. Billing System — Enterprise POS

> A full-stack, dual-shop Point of Sale (POS) and inventory management system built specifically for the Indian retail market. Engineered with Python and Django, this system digitizes physical ledger workflows, handles complex automated tax calculations, and provides live business analytics.

---

## 🚀 Key Features

### 🏪 Dual-Shop Architecture
Distinct point-of-sale interfaces for two different retail environments — **Paint** and **Electricals** — running on a single unified backend.

### 🧾 Automated GST Tax Engine
An intelligent **inclusive tax** mathematical engine that automatically extracts and splits **CGST/SGST** based on government-mandated HSN codes — no manual entry required.

### 📊 Live Analytics Command Center
A real-time dashboard leveraging **Django ORM aggregation** to track:
- Daily revenue
- Invoice volume
- Low-stock threshold alerts

### 🔐 Enterprise-Grade Security
Implements strict **session timeouts** and **RAM-based session caching** to prevent unauthorized access in a physical retail environment.

### 💻 Zero-Cost Local Kiosk Deployment
Custom **Windows Batch scripting** for a 1-click "App Mode" launch, paired with automated, invisible **cloud database syncing** via Google Drive.

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python, Django, SQLite |
| Frontend | HTML5, CSS3, JavaScript, Bootstrap 5 |
| Deployment | Windows Batch Scripting, Google Drive Cloud Sync |

---

## 📸 System Previews

> 📌 *Upload screenshots of your POS screen, the printed receipt, and the live dashboard here.*

| POS Interface | Printed Receipt | Live Dashboard |
|---|---|---|
| *(screenshot)* | *(screenshot)* | *(screenshot)* |

---

## ⚙️ Local Installation

### Prerequisites
- Python 3.8+
- pip

### Steps

**1. Clone the repository**
```bash
git clone https://github.com/yourusername/mv-billing.git
cd mv-billing
```

**2. Install dependencies**
```bash
pip install django
```

**3. Apply database migrations**
```bash
python manage.py migrate
```

**4. Start the development server**
```bash
python manage.py runserver
```

**5. Open in your browser**
```
http://127.0.0.1:8000
```

---

## 🪟 Windows Kiosk Launch (App Mode)

For a 1-click launch in Chrome's App Mode (no browser UI, kiosk-style):

1. Run the included `.bat` file from the project root.
2. The script starts the Django server and opens the POS in App Mode automatically.
3. Google Drive sync runs silently in the background to keep the SQLite database backed up to the cloud.

---

## 📁 Project Structure

```
mv-billing/
├── billing/              # Core Django app (models, views, templates)
├── paint_shop/           # Paint retail POS module
├── electrical_shop/      # Electricals retail POS module
├── templates/            # Shared HTML templates (Bootstrap 5)
├── static/               # CSS, JS, and assets
├── db.sqlite3            # Local SQLite database
├── manage.py
├── launch.bat            # Windows 1-click kiosk launcher
└── requirements.txt
```

---

## 🧮 GST Engine — How It Works

The billing engine uses the **inclusive tax back-calculation formula** to extract GST from MRP prices:

```
Tax Amount = (MRP × GST Rate) / (100 + GST Rate)
CGST = SGST = Tax Amount / 2
```

HSN codes stored in the product database automatically determine the applicable GST slab (0%, 5%, 12%, 18%, or 28%), making the billing process fully compliant and hands-free.

---

## 📈 Roadmap

- [ ] Barcode scanner integration
- [ ] UPI / QR payment support
- [ ] Multi-user role management (Admin, Cashier)
- [ ] PDF invoice generation and WhatsApp delivery
- [ ] PostgreSQL migration for multi-device deployments

---

## 🤝 Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you'd like to change.

---

## 📄 License

[MIT](LICENSE)

---

> Built with ❤️ for Indian retail businesses — bridging the gap between physical ledgers and digital efficiency.
