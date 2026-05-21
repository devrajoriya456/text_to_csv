import streamlit as st
import pandas as pd
import io

def parse_text_file(uploaded_file):
    """
    Reads an uploaded text file, auto-detects the delimiter,
    and returns a pandas DataFrame.
    """
    # Read the first line to auto-detect the separator
    # Streamlit uploaded files are bytes-like, so we read and decode
    first_line = uploaded_file.readline().decode('utf-8')
    uploaded_file.seek(0) # Reset file pointer back to the beginning
    
    if '\t' in first_line:
        separator = '\t'
    elif ',' in first_line:
        separator = ','
    elif ';' in first_line:
        separator = ';'
    else:
        separator = r'\s+'  # fallback to whitespace/spaces

    try:
        # Read text into DataFrame
        df = pd.read_csv(uploaded_file, sep=separator, engine='python')
        
        # Clean up whitespaces from headers and string columns
        df.columns = df.columns.str.strip()
        for col in df.select_dtypes(include=['object']).columns:
            df[col] = df[col].str.strip()
            
        return df
    except Exception as e:
        # Fallback approach if columns are completely messy/unaligned
        uploaded_file.seek(0)
        lines = [line.decode('utf-8').strip() for line in uploaded_file.readlines()]
        return pd.DataFrame(lines, columns=['Raw Text Content'])

# --- STREAMLIT UI LAYOUT ---
st.set_page_config(page_title="Text to Spreadsheet Converter", layout="centered")

st.title("Dev's File Converter: .txt to CSV/Excel")
st.write("Upload a structured or plain text file, select your format, and download the converted result.")

st.divider()

# 1. File Upload Component (.txt only)
uploaded_file = st.file_uploader("Choose a .txt file", type=["txt"])

if uploaded_file is not None:
    # Get the original file name without extension
    original_name = uploaded_file.name.rsplit('.', 1)[0]
    
    st.success(f"Successfully loaded: {uploaded_file.name}")
    
    # 2. Format Selection (Radio buttons - user can only choose one)
    output_format = st.radio(
        "Select your desired output format:",
        ["Excel (.xlsx)", "CSV (.csv)"],
        index=0
    )
    
    # 3. Convert Button
    if st.button("Convert File", type="primary"):
        with st.spinner("Processing your data..."):
            # Process the file using our extraction function
            df = parse_text_file(uploaded_file)
            
            # Show data preview in UI so user knows it worked accurately
            st.write("### Data Preview")
            st.dataframe(df.head(10))
            
            # Prepare file buffers for the download button
            if "Excel" in output_format:
                buffer = io.BytesIO()
                # Write to buffer using openpyxl
                df.to_excel(buffer, index=False, engine='openpyxl')
                buffer.seek(0)
                
                st.download_button(
                    label="📥 Download Excel File",
                    data=buffer,
                    file_name=f"{original_name}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
                
            else:
                # Convert to CSV string, then encode to bytes for download
                csv_data = df.to_csv(index=False).encode('utf-8')
                
                st.download_button(
                    label="📥 Download CSV File",
                    data=csv_data,
                    file_name=f"{original_name}.csv",
                    mime="text/csv"
                )
