

import os
import pandas as pd

def convert_txt_to_spreadsheet(input_file, output_format='excel', separator=None):
    """
    Converts a .txt file into a structured .csv or .xlsx file.
    
    Parameters:
    - input_file (str): Path to your source .txt file.
    - output_format (str): 'excel' or 'csv'.
    - separator (str): Optional separator (e.g., ',', '\t'). If None, it auto-detects.
    """
    if not os.path.exists(input_file):
        print(f"Error: The file '{input_file}' was not found. Please check the path.")
        return

    print(f"Reading '{input_file}'...")
    
    # Auto-detection layout if no separator is specified
    if separator is None:
        with open(input_file, 'r', encoding='utf-8') as f:
            first_line = f.readline()
            if '\t' in first_line:
                separator = '\t'
                print("-> Auto-detected separator: TAB")
            elif ',' in first_line:
                separator = ','
                print("-> Auto-detected separator: COMMA")
            elif ';' in first_line:
                separator = ';'
                print("-> Auto-detected separator: SEMICOLON")
            else:
                separator = r'\s+'  # multiple whitespaces
                print("-> Defaulting separator to: Whitespace / Spaces")

    try:
        # Read text file into a pandas DataFrame
        # engine='python' ensures robust parsing for space variations
        df = pd.read_csv(input_file, sep=separator, engine='python')
        
        # Strip spaces from column headers
        df.columns = df.columns.str.strip()
        
        # Clean string data across rows
        for col in df.select_dtypes(include=['object']).columns:
            df[col] = df[col].str.strip()

        base_name = os.path.splitext(input_file)[0]

        if output_format.lower() in ['excel', 'xlsx']:
            output_file = f"{base_name}.xlsx"
            # Excel output with an attractive engine setup
            df.to_excel(output_file, index=False, engine='openpyxl')
            print(f"Success! Saved accurately as Excel: '{output_file}'")
            
        elif output_format.lower() in ['csv']:
            output_file = f"{base_name}.csv"
            df.to_csv(output_file, index=False, encoding='utf-8')
            print(f"Success! Saved accurately as CSV: '{output_file}'")
            
        else:
            print("Unknown output format specified. Choose 'excel' or 'csv'.")
            
    except Exception as e:
        print(f"An error occurred during parsing: {e}")
        print("\nIf your file doesn't have regular column alignments, it might be plain unstructured rows.")
        print("Falling back to writing line-by-line into a single-column table...")
        
        # Fallback approach for completely unaligned / unstructured txt files
        try:
            with open(input_file, 'r', encoding='utf-8') as f:
                lines = [line.strip() for line in f.readlines()]
            df_fallback = pd.DataFrame(lines, columns=['Raw Text Content'])
            
            if output_format.lower() in ['excel', 'xlsx']:
                df_fallback.to_excel(f"{base_name}.xlsx", index=False)
                print(f"Success (Fallback style)! Saved as: '{base_name}.xlsx'")
            else:
                df_fallback.to_csv(f"{base_name}.csv", index=False)
                print(f"Success (Fallback style)! Saved as: '{base_name}.csv'")
        except Exception as fallback_error:
            print(f"Fallback also failed: {fallback_error}")

if __name__ == "__main__":
    # --- CONFIGURATION ---
    # Place your txt file name here:
    INPUT_TXT_FILE = "data.txt" 
    
    # Choose your desired target format: 'excel' or 'csv'
    TARGET_FORMAT = "excel" 
    
    # Explicit separator if you know it (e.g., ',' or '\t'). 
    # Leave as None to let the script guess it automatically!
    EXPLICIT_SEP = None 
    # ---------------------
    
    # Create a dummy sample data.txt file if it doesn't exist yet, for instant user testing
    if not os.path.exists(INPUT_TXT_FILE):
        with open(INPUT_TXT_FILE, 'w', encoding='utf-8') as sample_f:
            sample_f.write("ID\tName\tDepartment\tSalary\n")
            sample_f.write("101\tAlice Smith\tEngineering\t95000\n")
            sample_f.write("102\tBob Jones\tMarketing\t78000\n")
            sample_f.write("103\tCharlie Brown\tDesign\t82000\n")
        print(f"Created a sample '{INPUT_TXT_FILE}' file for you to test out.")

    convert_txt_to_spreadsheet(INPUT_TXT_FILE, output_format=TARGET_FORMAT, separator=EXPLICIT_SEP)