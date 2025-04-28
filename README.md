# FactorNet - Professional Online Invoicing System

FactorNet is a powerful and user-friendly **online invoicing platform** built with Django.  
It allows individuals, freelancers, and businesses to create, manage, and issue invoices easily and securely.

## ✨ Why FactorNet?

- Simple and beautiful UI
- Full control over your customers and invoices
- Responsive design for all devices
- Easy integration via RESTful API
- Persian calendar support (Shamsi dates)
- Draw and save your digital signature directly on the platform
- Secure access for authenticated users only

## 🚀 Features

- User authentication (Login / Logout)
- Customer management (Add, Edit, Delete, List)
- Invoice management (Create, Edit, View, Delete)
- Invoice items management
- Automatic invoice numbering
- Calculation of taxes, discounts, and total amounts
- Persian datepicker for invoice dates
- User profile management:
  - Update full name, email, address
  - Upload company logo
  - Draw or update digital signature
- Responsive and mobile-friendly design
- Secure REST API (with authenticated access)
- Modern and clean dashboard

## 🖼️ Screenshots

> Coming soon! This section will be updated in future releases.

- **Login Page**
- **User Dashboard**
- **Invoice Detail Page**
- **Signature Drawing**

## ⚙️ Tech Stack

- **Backend:** Django, Django REST Framework
- **Frontend:** HTML5, CSS3, JavaScript
- **Other Tools:**
  - MDS Datepicker (for Jalali/Persian calendar)
  - Canvas API (for signature drawing)

## 📥 Installation Guide

1. **Clone the Repository:**

```bash
git clone <https://github.com/radman1007/FactorNet>
cd factornet
```

2. **Create and Activate Virtual Environment:**

```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

3. **Install Dependencies:**

```bash
pip install -r requirements.txt
```

4. **Apply Migrations:**

```bash
python manage.py migrate
```

5. **Create Superuser (Optional but recommended):**

```bash
python manage.py createsuperuser
```

6. **Run Development Server:**

```bash
python manage.py runserver
```

7. **Open the Website:**

```
http://127.0.0.1:8000/
```

## 🛡️ API Access

All API endpoints (for Customers, Invoices, InvoiceItems) are protected and only available for **authenticated users**.  
Each user can only access **their own invoices and customers**.

Example API URL:

```
http://127.0.0.1:8000/invoice/api/invoices/
```

**Coming Soon:**
- API Documentation (Swagger / Redoc)
- API Tokens for secure integrations

## 🔥 Future Plans

- Download invoice as PDF
- Send invoices via email
- Payment gateway integration
- Full multi-language support (Persian and English)
- Subscription and premium plans

## 📄 License

This project is currently private and under active development.

---

Made with love by [Radman] ❤️
