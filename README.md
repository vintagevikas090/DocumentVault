# 📁 DocumentVault

A **privacy-first, fully offline** personal document organizer and management system. Built with Python and Streamlit, it scans your local directories, automatically categorizes files using a rule-based engine, eliminates duplicate storage bloat using smart chunked file hashing, and generates CSV inventories as well as database backups.

> [!IMPORTANT]
> **100% Offline & Private:** This application operates entirely on local threads. It makes no external API calls, sets no cookies, and performs no data tracking. Your documents remain in their original paths on your system—only indexing metadata is saved locally.


---

## 🎥 Demo

Check out the walk-through demo video of the Streamlit dashboard:  
👉 **[Watch Demo Video](assets/demo.mp4)**


---

## ✨ Key Features

*   **⚡ Fast Streamlit Web UI:** A modern, interactive multi-tab dashboard for organizing, filtering, and searching files.
*   **🛡️ Secure File Deduplication:** Avoids duplicate storage bloat. Uses a memory-efficient `SHA-256` hashing scanner that reads files in small chunks (preventing RAM crashes even on multi-GB files).
*   **📂 Auto-Categorization:** Built-in keyword and rules engine tailored for standard documents (Govt IDs like Aadhaar/PAN, Education degree sheets, Finance statement/invoices, Medical records, Code scripts, and more).
*   **📦 ZIP Import & Scan:** Drag-and-drop a `.zip` archive directly into the dashboard. It extracts and indexes the files automatically.
*   **🛡️ Database Restore:** Upload a previously saved backup `.zip` file under the "Import Documents" tab to instantly restore your entire organized history.
*   **📤 Local backups & Exports:**
    *   **Export Spreadsheets:** Instant export of your organized document catalog to a `.csv` file.
    *   **Backup Database:** Create local, compressed `.zip` database backups in one click.
    *   **Danger Zone:** Easily wipe the indexed database clean when you need a fresh start.

---


## 📂 Auto-Categorization Support

The built-in keywords and extensions mapping supports automatic categorization of the following document types:
*   **Government & Identity:** Aadhaar, PAN, Passport, Voter Card, Driving License, Domicile, Domicile Certificate, etc.
*   **Education:** Degrees, Marksheets, Transcripts, Diplomas, School/College results.
*   **Finance & Banking:** Invoices, Receipts, Tax documents, Bank Statements, Salary Slips, Passbooks.
*   **Property & Vehicle:** Rental Agreements, Leases, Deeds, Insurance policies, RC papers, Vehicle deeds.
*   **Medical:** Prescriptions, Medical Reports, Blood Tests, Scans, MRI, X-Rays, Vaccinations.
*   **Utility:** Electricity, Gas, Water Bills.
*   **Personal Images:** Pictures, Photos, Signatures.
*   **Career:** Resumes, CVs, Offer Letters, Relieving letters, Experience certificates, Appraisal letters, Payslips.
*   **Code & Development:** `.py`, `.ipynb`, `.js`, `.html`, `.css`, `.cpp`, `.java` files, scripts, and notebooks.

---

## 🏗️ Project Architecture

The directory structure is organized as follows:

```text
DocumentVault/
├── data/                     
├── src/                      
│   ├── categorizer.py        
│   ├── database.py           
│   ├── deduplicator.py       
│   ├── exporter.py            
│   └── scanner.py           
├── app.py                    
├── requirements.txt  
├── README.md     
└── .gitignore                
```

---

## 🚀 Getting Started

### 1. Installation
Clone the repository and install dependencies:
```bash
git clone https://github.com/vintagevikas090/DocumentVault.git
cd DocumentVault
pip install -r requirements.txt
```

### 2. Run the App
Launch the Streamlit dashboard:
```bash
python -m streamlit run app.py
```
Streamlit will automatically open the web dashboard in your browser at `http://localhost:8501`.

---

## 👤 Author

Developed by **Vikas Prajapat**  
*   GitHub: [@vintagevikas090](https://github.com/vintagevikas090)
