import streamlit as st
import pandas as pd
import os
import subprocess

# Set Streamlit page configuration to wide mode
st.set_page_config(layout="wide")

# Streamlit app title
st.title("Backtest Report")

# Display mode selection in the sidebar
display_mode = st.sidebar.radio("表示モードを選択してください", ["1画面", "2画面"])

# Input for stock code in the sidebar
code = st.sidebar.text_input("銘柄コード")

# Folder paths for CSV files
folder_paths = {
    "tech_matome": "data/tech_matome",
    "all_data": "data/all"  # Add the folder path for all data
}

# Graph folder path
graph_folder_path = "data/html"

def load_csv_files(folder):
    """Load all CSV files in the folder."""
    try:
        csv_files = [f for f in os.listdir(folder) if f.endswith('.csv')]
        if not csv_files:
            st.write(f"{folder}内にCSVファイルが見つかりませんでした。")
        return csv_files
    except Exception as e:
        st.write(f"エラーが発生しました: {e}")
        return []

def display_file_simple(file, folder, code):
    """Display CSV file content as a DataFrame and link to corresponding graph."""
    if str(code) in file:
        file_path = os.path.join(folder, file)
        
        # Check if the file exists and is not empty
        if not os.path.exists(file_path):
            st.write(f"Error: {file} does not exist.")
            return
        if os.path.getsize(file_path) == 0:
            st.write(f"Error: {file} is empty.")
            return
        
        try:
            df = pd.read_csv(file_path)
        except pd.errors.EmptyDataError:
            st.write(f"Error: {file} contains no data.")
            return
        except Exception as e:
            st.write(f"Error: Failed to read {file}. Exception: {e}")
            return
        
        # Set index to '_strategy' if it exists
        if "_strategy" in df.columns:
            df.set_index("_strategy", inplace=True)
        else:
            st.write(f"Warning: '_strategy' column not found in the DataFrame.")
        
        st.write(f"### {file}")
        st.write(df)
        
        # Construct graph file path
        graph_file_name = "modified_" + file.split("_")[0] + '_1d.html'
        graph_file_path = os.path.join(graph_folder_path, graph_file_name)
        
        if os.path.exists(graph_file_path):
            st.markdown(f"[View corresponding graph file]({graph_file_path})")
        else:
            st.write(f"Corresponding graph file not found: {graph_file_name}")

def display_tech_matome():
    """Display tech_matome table directly."""
    st.header("tech_matome")
    tech_matome_files = load_csv_files(folder_paths["tech_matome"])
    
    if tech_matome_files:
        for tech_matome_file in tech_matome_files:
            file_path = os.path.join(folder_paths["tech_matome"], tech_matome_file)
            
            # Check if the file exists and is not empty
            if not os.path.exists(file_path):
                st.write(f"Error: {tech_matome_file} does not exist.")
                continue
            if os.path.getsize(file_path) == 0:
                st.write(f"Error: {tech_matome_file} is empty.")
                continue
            
            try:
                df = pd.read_csv(file_path)
                # Set index to 'Name' column if specified
                if "Name" in df.columns:
                    df.set_index("Name", inplace=True)
                else:
                    st.write(f"Warning: Index column 'Name' not found in the DataFrame.")
                
                st.write(f"### {tech_matome_file}")
                st.write(df)
                
                # Construct graph file path
                graph_file_name = "modified_" + tech_matome_file.split("_")[0] + '_1d.html'
                graph_file_path = os.path.join(graph_folder_path, graph_file_name)
                
                if os.path.exists(graph_file_path):
                    st.markdown(f"[View corresponding graph file]({graph_file_path})")
                else:
                    st.write(f"Corresponding graph file not found: {graph_file_name}")
                    
            except pd.errors.EmptyDataError:
                st.write(f"Error: {tech_matome_file} contains no data.")
                continue
            except Exception as e:
                st.write(f"Error: Failed to read {tech_matome_file}. Exception: {e}")
    else:
        st.write(f"{folder_paths['tech_matome']}内にCSVファイルが見つかりませんでした。")

def search_and_display_files(code, folder_paths):
    """Search for the code in the folder and display the corresponding files."""
    folder_path = folder_paths["tech_matome"]
    if folder_path and os.path.exists(folder_path):
        st.write(f"## Searching in tech_matome")
        csv_files = load_csv_files(folder_path)
        if csv_files:
            for csv_file in csv_files:
                display_file_simple(csv_file, folder_path, code)
        else:
            st.write(f"{folder_path}内にCSVファイルが見つかりませんでした。")
    else:
        st.write(f"有効なフォルダパスを入力してください: {folder_path}")

def search_all_data(code):
    """Search for the code in all_data folder and display results."""
    folder_path = folder_paths["all_data"]
    if folder_path and os.path.exists(folder_path):
        st.write(f"## Search Results in all_data")
        csv_files = load_csv_files(folder_path)
        search_results = []
        for csv_file in csv_files:
            file_path = folder_path + "/" +  csv_file
            try:
                df = pd.read_csv(file_path)
                if str(code) in str(csv_file):
                    if "_strategy" in df.columns:
                        df.set_index("_strategy", inplace=True)
                    st.write(csv_file)
                    search_results.append(df)
            except pd.errors.EmptyDataError:
                continue
            except Exception as e:
                st.write(f"Error: Failed to read {file_path}. Exception: {e}")

        if search_results:
            combined_df = pd.concat(search_results, ignore_index=False)
            st.write(combined_df)
        else:
            st.write("No results found.")
    else:
        st.write(f"Folder path does not exist: {folder_path}")



def pull_from_github():
    """Pull the latest changes from the GitHub repository."""
    try:
        result = subprocess.run(["git", "pull"], capture_output=True, text=True, check=True)
        st.write(f"GitHubからの更新が成功しました")
    except subprocess.CalledProcessError as e:
        st.write(f"GitHubからの更新に失敗しました")

# Add a button to reload data
update_data = st.sidebar.button("GitHubからデータを更新")

# Update data from GitHub if button is clicked
if update_data:
    pull_from_github()

# Display content based on the selected display mode
if display_mode == "1画面":
    # Check if a stock code is provided
    if code:
        search_all_data(code)
    else:
        # Always display tech_matome table if no code is provided
        display_tech_matome()

elif display_mode == "2画面":
    # Create two columns
    col1, col2 = st.columns(2)

    # Display tech_matome page on the left
    with col1:
        display_tech_matome()

    # Display search results or prompt to enter code on the right
    with col2:
        st.header("検索結果")
        if code:
            search_all_data(code)
        else:
            st.write("銘柄コードを入力してください。")
