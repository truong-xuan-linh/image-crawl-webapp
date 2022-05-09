# import libraries
import tkinter as tk
from tkinter import filedialog
import streamlit as st
from getURLs import getURLs
from save_image import download_images
import unidecode
import pickle


st.set_page_config(page_title="The Ramsey Highlights", layout="wide")
st.markdown(
    """
    <style>
    [data-testid="stSidebar"][aria-expanded="true"] > div:first-child{
        width: 400px;
    }
    [data-testid="stSidebar"][aria-expanded="false"] > div:first-child{
        width: 400px;
        margin-left: -400px;
    }
     
    """,
    unsafe_allow_html=True,
)

with open("./urls.pkl", "rb") as f:
    urls = pickle.load(f)

# Set up tkinter
root = tk.Tk()
root.withdraw()

# Make folder picker dialog appear on top of other windows
root.wm_attributes('-topmost', 1)

# Folder picker button
st.write('Vui lòng chọn đường dẫn lưu ảnh')
clicked = st.button('Folder Picker')
if clicked:
    save_dir = st.text_input('Folder lưu:', filedialog.askdirectory(master=root))
    with open("./save_dir.txt", "w") as f:
        f.write(save_dir)
else:
    with open("./save_dir.txt", "r") as f:
        save_dir = f.read()
    save_dir = st.text_input('Folder lưu:', save_dir)

city_col, popular_col, keyword_col = st.columns(3)
city = city_col.text_input('Tên thành phố')
popular = popular_col.text_input("Tên địa điểm")
keyword = keyword_col.text_input("Từ khóa tìm kiếm")

with open("./checkboxes.pkl", "rb") as f:
    checkbox = pickle.load(f)

col = st.columns(2)
check = 0
if col[0].button("Tìm kiếm"):
    k = 0
    urls = getURLs(keyword)[:150]
    with open("./checkboxes.pkl", "wb") as f:
        pickle.dump([], f)
    with open("./urls.pkl", "wb") as fp:
        pickle.dump(urls, fp)
    for i in range(len(urls)):
        st.session_state[i] = False

def change():
    with open("./checkboxes.pkl", "wb") as f:
        pickle.dump(checkbox,f)
if col[1].button("Lưu"):
    city_name = "-".join(unidecode.unidecode(city).split(" "))
    popular_name = "-".join(unidecode.unidecode(popular).split(" "))
    urls_final = []

    print(checkbox)
    for i in range(len(checkbox)):
        if checkbox[i] == True:
            urls_final.append(urls[i])
    download_images(save_dir, city_name + "_" + popular_name, urls_final)
    
checkbox = [False]*len(urls)



for image_index, url in enumerate(urls):
    if image_index%6 ==0:
        k = 0
        columns = st.columns(6)
        columns2 = st.columns(6)
    
    checkbox[image_index] = columns[k].checkbox(" ", key = image_index, on_change = change)
    
    columns2[k].image(url)
    k=k+1
