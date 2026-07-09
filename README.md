# 📁 DocumentVault

A **privacy-first, fully offline** personal document organizer and management system. Built with Python and Streamlit, it scans your local directories, physically copies or moves files into a centralized category-structured vault folder (`Organized_Data`), eliminates duplicate storage bloat using smart chunked file hashing, and generates CSV inventories as well as database backups.

> [!IMPORTANT]
> **100% Offline & Private:** This application operates entirely on local threads. It makes no external API calls, sets no cookies, and performs no data tracking. Your documents are safely organized inside a centralized `Organized_Data` vault folder (either copied or moved) structured by their categories, with only indexing metadata saved in a local database.


---

## 🎥 Demo

Check out the walk-through demo video of the Streamlit dashboard:  
👉 **[Watch Demo Video](assets/demo.mp4)**

### 📸 Screenshots

| | |
| --- | --- |
| **Import Documents (Add Documents)** <br> ![Import Documents](assets/image%201.png) | **Dashboard (Metrics & Analytics)** <br> ![Dashboard Overview](assets/image%202.png) |
| **Search & Filtering Documents** <br> ![Search and Filter](assets/image%203.png) | **Data & Database Management** <br> ![Data Management](assets/image%204.png) |



---

## ✨ Key Features

*   **⚡ Modern Sidebar UI:** A clean, sidebar-navigation dashboard for organizing, filtering, searching, and managing your vault.
*   **📁 Category-Structured Vault:** Automatically organizes documents physically into a `Organized_Data` folder with subfolders for each category (e.g. `Government & Identity`, `Education`, `Finance`).
*   **🔄 Copy or Move Modes:** Supports both safe copy mode (leaving originals in place) and move mode (deleting empty directories and cleaning up source folders after the move).
*   **🛡️ Secure File Deduplication:** Avoids duplicate storage bloat. Uses a memory-efficient `SHA-256` hashing scanner that reads files in small chunks (preventing RAM crashes even on multi-GB files). Naming conflicts in the vault are automatically resolved by appending unique short-hash suffixes.
*   **📦 ZIP Import & Scan:** Drag-and-drop a `.zip` archive directly into the dashboard. It extracts and indexes the files into the vault automatically.
*   **🛡️ Database Restore:** Upload a previously saved backup `.zip` file under the "Add Documents" tab to instantly restore your entire organized history.
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
│   ├── doc_inventory.db      # SQLite inventory database
│   └── Organized_Data/       # Centralized category-structured document vault
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
