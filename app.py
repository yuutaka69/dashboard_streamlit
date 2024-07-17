import streamlit as st
import pandas as pd
import os

# Set Streamlit page configuration to wide mode
st.set_page_config(layout="wide")

# Streamlit app title
st.title("Backtest Report")

# サイドバーに銘柄コードを入力
code = st.sidebar.text_input("銘柄コード")

# サイドバーにページ選択
pages = ["tech_matome", "ALL", "MACD", "EMA", "EMA_diff", "RSI", "MAX30d"]
page = st.sidebar.radio("ページを選択してください", pages)

# 各ページに対応するフォルダパスの設定
folder_paths = {
    "tech_matome": st.sidebar.text_input("tech_matomeフォルダのパスを入力してください", value="data/tech_matome"),
    "ALL": st.sidebar.text_input("allフォルダのパスを入力してください", value="data/all"),
    "MACD": st.sidebar.text_input("MACDフォルダのパスを入力してください", value="data/MACD"),
    "EMA": st.sidebar.text_input("EMAフォルダのパスを入力してください", value="data/EMA"),
    "EMA_diff": st.sidebar.text_input("EMA_diffフォルダのパスを入力してください", value="data/EMA_diff"),
    "RSI": st.sidebar.text_input("RSIフォルダのパスを入力してください", value="data/RSI"),
    "MAX30d": st.sidebar.text_input("MAX30dフォルダのパスを入力してください", value="data/MAX30d"),
}

# グラフフォルダのパスを入力
graph_folder_path = st.sidebar.text_input("グラフフォルダのパスを入力してください", value="data/html")

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

def display_file_simple(file, folder, code, index_column):
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
        
        # Set index to '_strategy' or 'Name' column if specified
        if index_column in df.columns:
            df.set_index(index_column, inplace=True)
        else:
            st.write(f"Warning: Index column '{index_column}' not found in the DataFrame.")
        
        st.write(f"### {file}")
        
        # Add color bar to columns containing "Win Rate" or "SQN"
        styled_df = df.style
        for column in df.columns:
            if "Win Rate" in column or "SQN" in column:
                styled_df = styled_df.bar(subset=[column], color='#d65f5f' if "Win Rate" in column else '#5fba7d')
        
        st.write(styled_df)
        #st.table(styled_df)
        
        # Construct graph file path
        graph_file_name = "modified_" + file.split("_")[0] + '_1d.html'
        graph_file_path = os.path.join(graph_folder_path, graph_file_name)
        
        if os.path.exists(graph_file_path):
            st.markdown(f"[View corresponding graph file]({graph_file_path})")
        else:
            st.write(f"Corresponding graph file not found: {graph_file_name}")


def search_and_display_all_folders(code, folder_paths):
    """Search for the code in all folders and display the corresponding files."""
    for page, folder_path in folder_paths.items():
        if folder_path and os.path.exists(folder_path):
            st.write(f"## Searching in {page}")
            csv_files = load_csv_files(folder_path)
            if csv_files:
                for csv_file in csv_files:
                    if page == "tech_matome":
                        display_file_simple(csv_file, folder_path, code , "Name")
                    else:
                        display_file_simple(csv_file, folder_path, code, "_strategy")
            else:
                st.write(f"{folder_path}内にCSVファイルが見つかりませんでした。")
        else:
            st.write(f"有効なフォルダパスを入力してください: {folder_path}")

if code:
    search_and_display_all_folders(code, folder_paths)
else:
    if folder_paths[page] and os.path.exists(folder_paths[page]):
        csv_files = load_csv_files(folder_paths[page])
        if csv_files:
            for csv_file in csv_files:
                if page == "tech_matome":
                    display_file_simple(csv_file, folder_paths[page], code , "Name")
                else:
                    display_file_simple(csv_file, folder_paths[page], code, "_strategy")
        else:
            st.write(f"{folder_paths[page]}内にCSVファイルが見つかりませんでした。")
    else:
        st.write("有効なフォルダパスを入力してください。")
