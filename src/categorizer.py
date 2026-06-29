
class Categorizer:
    # Rule-based categorization mapping keywords to a primary category
    RULES = {
        "Government & Identity": [
            "aadhaar", "aadhar", "pan ", "pan.", "passport", "voter", "driving", "licence", "license", "dl", "ration", 
            "mool niwas", "domicile", "bhamashah", "jan aadhar", "caste", "obc", "ncl", "birth certificate"
        ],
        "Education": [
            "degree", "marksheet", "transcript", "diploma", "10th", "12th", "8th", "9th", "11th", 
            "university", "college", "alumni", "jee", "score", "result", "student", "t.c", "tc", "school"
        ],
        "Finance & Banking": [
            "invoice", "receipt", "tax", "bank", "statement", "salary", "investment", "mutual fund", 
            "debit", "credit", "passbook", "possbook", "bob", "sbi", "hdfc", "icici"
        ],
        "Property & Vehicle": [
            "agreement", "lease", "rent", "deed", "sale", "insurance", "property", "rc", "bike", "car", "vehicle"
        ],
        "Medical": [
            "prescription", "report", "blood test", "scan", "mri", "xray", "discharge", "vaccination"
        ],
        "Utility": [
            "gas", "electricity", "water", "bill"
        ],
        "Personal Images": [
            "pic", "photo", "sign", "signature"
        ],
        "Career": [
            "resume", "cv", "offer letter", "relieving", "experience", "appraisal", "payslip", "promotion"
        ],
        "Code & Development": [
            ".py", ".ipynb", ".js", ".html", ".css", ".cpp", ".java", "script", "notebook", "dataset"
        ]
    }

    @staticmethod
    def categorize(filename: str) -> str:
        lower_name = filename.lower()
        
        # Check against rules
        for category, keywords in Categorizer.RULES.items():
            for keyword in keywords:
                if keyword in lower_name:
                    return category
                    
        return "Uncategorized"
