import streamlit as st
import pandas as pd
import requests
from io import StringIO

# Streamlit app title
st.title("Backtest Report")

# サイドバーに銘柄コードを入力
code = st.sidebar.text_input("銘柄コード")

# サイドバーにページ選択
pages = ["tech_matome", "ALL", "MACD", "EMA", "EMA_diff", "RSI", "MAX30d"]
page = st.sidebar.radio("ページを選択してください", pages)

# GitHub repository and folder settings
github_repo = st.sidebar.text_input("GitHubリポジトリのURLを入力してください", value="https://github.com/yuutaka69/dashboard_streamlit")

folder_paths = {
    "tech_matome": "data",
    "ALL": "data/ALL",
    "MACD": "path/to/MACD",
    "EMA": "path/to/EMA",
    "EMA_diff": "path/to/EMA_diff",
    "RSI": "path/to/RSI",
    "MAX30d": "path/to/MAX30d",
}

# グラフフォルダのパスを入力
graph_folder_path = st.sidebar.text_input("グラフフォルダのパスを入力してください", value="path/to/html")

# 選択されたページに対応するフォルダパス
folder_path = folder_paths[page]

def load_csv_files_from_github(repo, folder):
    """Load all CSV files from the GitHub repository folder."""
    url = f"{repo}/blob/main/{folder}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        files = response.json()
        csv_files = [file['name'] for file in files if file['name'].endswith('.csv')]
        return csv_files
    except Exception as e:
        st.write(f"エラーが発生しました: {e}")
        return []

def display_file_simple_from_github(file, repo, folder, code, index_column):
    """Display CSV file content from GitHub as a DataFrame and link to corresponding graph."""
    if str(code) in file:
        file_url = f"{repo}/raw/main/{folder}/{file}"
        try:
            response = requests.get(file_url)
            response.raise_for_status()
            df = pd.read_csv(StringIO(response.text))
            
            if df.empty:
                st.write(f"{file} is empty.")
                return
            
            # Set index to '_strategy' or 'Name' column if specified
            if index_column in df.columns:
                df.set_index(index_column, inplace=True)
            else:
                st.write(f"Warning: Index column '{index_column}' not found in the DataFrame.")
            
            st.write(f"### {file}")
            st.write(df)

            # Construct graph file path
            graph_file_name = "modified_" + file.split("_")[0] + '_1d.html'
            graph_file_path = f"{repo}/raw/main/{graph_folder_path}/{graph_file_name}"
            
            response = requests.get(graph_file_path)
            if response.status_code == 200:
                st.markdown(f"[View corresponding graph file]({graph_file_path})")
            else:
                st.write(f"Corresponding graph file not found: {graph_file_name}")
        except Exception as e:
            st.write(f"エラーが発生しました: {e}")

if github_repo and folder_path:
    csv_files = load_csv_files_from_github(github_repo, folder_path)
    if csv_files:
        for csv_file in csv_files:
            if page == "tech_matome":
                display_file_simple_from_github(csv_file, github_repo, folder_path, code , "Name")
            else:
                display_file_simple_from_github(csv_file, github_repo, folder_path, code, "_strategy")
    else:
        st.write("フォルダ内にCSVファイルが見つかりませんでした。")
else:
    st.write("有効なGitHubリポジトリURLとフォルダパスを入力してください。")
