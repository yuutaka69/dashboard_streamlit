import streamlit as st
import pandas as pd
import os

# Streamlit app title
st.title("Backtest Report")

# サイドバーに銘柄コードを入力
code = st.sidebar.text_input("銘柄コード")

# サイドバーにページ選択
pages = ["tech_matome", "ALL", "MACD", "EMA", "EMA_diff", "RSI", "MAX30d"]
page = st.sidebar.radio("ページを選択してください", pages)

# 各ページに対応するフォルダパスの設定
folder_paths = {
    "tech_matome": st.sidebar.text_input("tech_matomeフォルダのパスを入力してください", value=r"C:\Users\yuuta\Google ドライブ（y.takase@bridge.t.u-tokyo.ac.jp）\CCpjc\analysis\results\tech_matome"),
    "ALL": st.sidebar.text_input("ALLフォルダのパスを入力してください", value=r"C:\Users\yuuta\Google ドライブ（y.takase@bridge.t.u-tokyo.ac.jp）\CCpjc\streamlit\data\ALL"),
    "MACD": st.sidebar.text_input("MACDフォルダのパスを入力してください", value=r"C:\Users\yuuta\Google ドライブ（y.takase@bridge.t.u-tokyo.ac.jp）\CCpjc\streamlit\data\MACD"),
    "EMA": st.sidebar.text_input("EMAフォルダのパスを入力してください", value=r"C:\Users\yuuta\Google ドライブ（y.takase@bridge.t.u-tokyo.ac.jp）\CCpjc\streamlit\data\EMA"),
    "EMA_diff": st.sidebar.text_input("EMA_diffフォルダのパスを入力してください", value=r"C:\Users\yuuta\Google ドライブ（y.takase@bridge.t.u-tokyo.ac.jp）\CCpjc\streamlit\data\EMA_diff"),
    "RSI": st.sidebar.text_input("RSIフォルダのパスを入力してください", value=r"C:\Users\yuuta\Google ドライブ（y.takase@bridge.t.u-tokyo.ac.jp）\CCpjc\streamlit\data\RSI"),
    "MAX30d": st.sidebar.text_input("MAX30dフォルダのパスを入力してください", value=r"C:\Users\yuuta\Google ドライブ（y.takase@bridge.t.u-tokyo.ac.jp）\CCpjc\streamlit\data\MAX30d"),
}

# グラフフォルダのパスを入力
graph_folder_path = st.sidebar.text_input("グラフフォルダのパスを入力してください", value=r"C:\Users\yuuta\Google ドライブ（y.takase@bridge.t.u-tokyo.ac.jp）\CCpjc\streamlit\data\html")

# 選択されたページに対応するフォルダパス
folder_path = folder_paths[page]

def load_csv_files(folder):
    """Load all CSV files in the folder."""
    try:
        csv_files = [f for f in os.listdir(folder) if f.endswith('.csv')]
        if not csv_files:
            st.write("フォルダ内にCSVファイルが見つかりませんでした。")
        return csv_files
    except Exception as e:
        st.write(f"エラーが発生しました: {e}")
        return []

"""
def display_file_with_aggrid(file, folder, code):
    """Display CSV file content using AG Grid and link to corresponding graph."""
    if str(code) in file:
        file_path = os.path.join(folder, file)
        df = pd.read_csv(file_path)
        if df.empty:
            st.write(f"{file} is empty.")
            return
        
        st.write(f"### {file}")
        
        # Display the DataFrame using AG Grid for advanced filtering and sorting
        gb = GridOptionsBuilder.from_dataframe(df)
        gb.configure_pagination(paginationAutoPageSize=True)  # Add pagination
        gb.configure_side_bar()  # Add a sidebar for additional options
        gb.configure_default_column(groupable=True, value=True, enableRowGroup=True, aggFunc="max", editable=True)
        
        # Configure fixed columns
        if "Name" in df.columns:
            gb.configure_column("Name", pinned="left")  # Pin 'Name' column to the left
        if "Code" in df.columns:
            gb.configure_column("Code", pinned="left")  # Pin 'Code' column to the left
        
        gridOptions = gb.build()
        
        AgGrid(df, gridOptions=gridOptions, enable_enterprise_modules=True)
"""

def display_file_simple(file, folder, code, index_column):
    """Display CSV file content as a DataFrame and link to corresponding graph."""
    if str(code) in file:
        file_path = os.path.join(folder, file)
        df = pd.read_csv(file_path)
        
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
        graph_file_path = os.path.join(graph_folder_path, graph_file_name)
        
        if os.path.exists(graph_file_path):
            st.markdown(f"[View corresponding graph file]({graph_file_path})")
        else:
            st.write(f"Corresponding graph file not found: {graph_file_name}")

if folder_path and os.path.exists(folder_path):
    csv_files = load_csv_files(folder_path)
    if csv_files:
        for csv_file in csv_files:
            if page == "tech_matome":
                display_file_simple(csv_file, folder_path, code , "Name")
                #display_file_with_aggrid(csv_file, folder_path, code)
            else:
                display_file_simple(csv_file, folder_path, code, "_strategy")
    else:
        st.write("フォルダ内にCSVファイルが見つかりませんでした。")
else:
    st.write("有効なフォルダパスを入力してください。")
