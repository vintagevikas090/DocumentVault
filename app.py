import streamlit as st
import pandas as pd
import os
import tempfile
import zipfile
from src.database import DatabaseManager
from src.scanner import DocumentScanner
from src.exporter import Exporter

st.set_page_config(page_title="DocumentVault", page_icon="📁", layout="wide")

db = DatabaseManager("data/doc_inventory.db")

@st.cache_data
def get_cached_backup_bytes(db_path, mtime):
    import io
    import zipfile
    if not os.path.exists(db_path):
        return b""
    buffer = io.BytesIO()
    try:
        with zipfile.ZipFile(buffer, 'w', zipfile.ZIP_DEFLATED) as zipf:
            zipf.write(db_path, os.path.basename(db_path))
        return buffer.getvalue()
    except Exception:
        return b""

@st.cache_data
def get_cached_csv_data(db_path, mtime):
    import sqlite3
    import pandas as pd
    if not os.path.exists(db_path):
        return b""
    try:
        conn = sqlite3.connect(db_path)
        df = pd.read_sql_query("SELECT * FROM documents", conn)
        conn.close()
        return df.to_csv(index=False).encode('utf-8')
    except Exception:
        return b""

st.title("📁 DocumentVault")
st.markdown("A privacy-first, offline document management system.")


tab_scan, tab_dash, tab_manage = st.tabs(["📥 Add Documents", "📊 Dashboard", "⚙️ Data Management"])

with tab_scan:
    st.header("Import Documents")
    col_scan, col_zip, col_restore = st.columns(3, gap="large")
    
    with col_scan:
        st.subheader("📂 Scan Local Directory")
        st.markdown("Enter a folder path on your computer")
        
        if 'scan_path' not in st.session_state:
            st.session_state.scan_path = os.path.abspath(os.getcwd())
            
        st.session_state.scan_path = st.text_input(
            "Folder Path", 
            value=st.session_state.scan_path, 
            placeholder="e.g. C:\\Users\\Name\\Documents", 
            label_visibility="collapsed"
        )

        if st.button("🚀 Start Scan", type="primary", use_container_width=True):
            if os.path.exists(st.session_state.scan_path):
                with st.spinner("Scanning directory..."):
                    scanner = DocumentScanner(db)
                    scanner.scan_directory(st.session_state.scan_path)
                st.success("Scan completed successfully!")
                st.cache_data.clear()
            else:
                st.error("Directory does not exist. Please check the path.")
                
    with col_zip:
        st.subheader("📦 Upload ZIP Archive")
        st.markdown("Drop a `.zip` file here")
        
        uploaded_zip = st.file_uploader("Upload ZIP", type=["zip"], key="zip_uploader", label_visibility="collapsed")
        if uploaded_zip is not None:
            if st.button("Extract & Scan ZIP", type="primary", use_container_width=True):
                with st.spinner("Extracting and scanning..."):
                    with tempfile.TemporaryDirectory() as tmpdir:
                        zip_path = os.path.join(tmpdir, uploaded_zip.name)
                        with open(zip_path, "wb") as f:
                            f.write(uploaded_zip.getbuffer())
                        
                        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                            zip_ref.extractall(tmpdir)
                        
                        scanner = DocumentScanner(db)
                        scanner.scan_directory(tmpdir)
                    
                st.success("ZIP processed successfully!")
                st.cache_data.clear()

    with col_restore:
        st.subheader("🛡️ Restore DB Backup")
        st.markdown("Drop a backup `.zip` file here")
        
        uploaded_backup = st.file_uploader("Upload Backup ZIP", type=["zip"], key="backup_uploader", label_visibility="collapsed")
        if uploaded_backup is not None:
            if st.button("Restore Database", type="primary", use_container_width=True):
                with st.spinner("Restoring database..."):
                    try:
                        with zipfile.ZipFile(uploaded_backup) as z:
                            if "doc_inventory.db" not in z.namelist():
                                st.error("Invalid backup file. The ZIP file must contain 'doc_inventory.db'.")
                            else:
                                db_data = z.read("doc_inventory.db")
                                os.makedirs(os.path.dirname(db.db_path), exist_ok=True)
                                with open(db.db_path, "wb") as f:
                                    f.write(db_data)
                                st.success("Database restored successfully!")
                                st.cache_data.clear()
                                st.rerun()
                    except Exception as e:
                        st.error(f"Failed to restore database backup: {e}")

with tab_dash:
    documents = db.get_all_documents()
    if documents:
        df = pd.DataFrame(documents)
        
        m1, m2, m3 = st.columns(3)
        with m1:
            st.metric(label="Total Documents", value=len(df))
        with m2:
            total_size_mb = df['file_size'].sum() / (1024 * 1024)
            st.metric(label="Storage Used", value=f"{total_size_mb:.2f} MB")
        with m3:
            unique_categories = df['category'].nunique()
            st.metric(label="Categories", value=unique_categories)
            
        st.divider()

        st.subheader("🔍 Search Documents")
        search_col, filter_col = st.columns([3, 1])
        
        with search_col:
            search_query = st.text_input("Search by filename...", "")
        
        with filter_col:
            categories = ["All"] + list(df['category'].unique())
            selected_category = st.selectbox("Filter by Category", categories)

        filtered_df = df.copy()
        if search_query:
            filtered_df = filtered_df[filtered_df['filename'].str.contains(search_query, case=False, na=False)]
        if selected_category != "All":
            filtered_df = filtered_df[filtered_df['category'] == selected_category]

        dash_table, dash_chart = st.tabs(["📄 Data Table", "📈 Analytics"])
        
        with dash_table:
            display_df = filtered_df[['id', 'filename', 'category', 'added_date', 'file_size', 'original_path']].copy()
            display_df['file_size'] = (display_df['file_size'] / 1024).round(2).astype(str) + " KB"
            st.dataframe(display_df, use_container_width=True, hide_index=True)
            
        with dash_chart:
            category_counts = df['category'].value_counts().reset_index()
            category_counts.columns = ['Category', 'Count']
            st.bar_chart(category_counts, x='Category', y='Count')
        
    else:
        st.info("No documents found in the database. Go to the **Add Documents** tab to get started!")

with tab_manage:
    st.header("Export & Database Management")
    exporter = Exporter(db)
    
    col_export, col_backup, col_danger = st.columns(3, gap="large")
    
    with col_export:
        st.subheader("📤 Export CSV")
        st.markdown("***Download*** a spreadsheet containing your organized file metadata.")
        
        db_path = db.db_path
        if os.path.exists(db_path):
            mtime = os.path.getmtime(db_path)
            csv_data = get_cached_csv_data(db_path, mtime)
            if csv_data:
                st.download_button(
                    label="📥 Download CSV",
                    data=csv_data,
                    file_name="document_inventory.csv",
                    mime="text/csv",
                    use_container_width=True
                )
            else:
                st.button("📥 Download CSV", disabled=True, use_container_width=True)
        else:
            st.button("📥 Download CSV", disabled=True, use_container_width=True)
            
    with col_backup:
        st.subheader("🛡️ Backup DB")
        st.markdown("Create a safe, compressed `.zip` backup of your SQLite database on ***Your Local System***.")
        
        db_path = db.db_path
        if os.path.exists(db_path):
            mtime = os.path.getmtime(db_path)
            backup_bytes = get_cached_backup_bytes(db_path, mtime)
            if backup_bytes:
                from datetime import datetime
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                st.download_button(
                    label="📦 Create Backup",
                    data=backup_bytes,
                    file_name=f"doc_inventory_backup_{timestamp}.zip",
                    mime="application/zip",
                    use_container_width=True
                )
            else:
                st.button("📦 Create Backup", disabled=True, use_container_width=True)
        else:
            st.button("📦 Create Backup", disabled=True, use_container_width=True)
                
    with col_danger:
        st.subheader("⚠️ Danger Zone")
        st.markdown("Wipe whole data from the database. Be Very Careful. ***This cannot be undone.***")
        if st.button("🗑️ Clear Database", type="secondary", use_container_width=True):
            db.clear_database()
            st.cache_data.clear()
            st.success("Database cleared!")
            st.rerun()
