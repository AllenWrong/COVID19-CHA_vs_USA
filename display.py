import os

import streamlit as st
from 生成结果 import main

st.sidebar.write("**时间单位**")
time_unit = st.sidebar.selectbox("", ["季", "半年", "年"])
st.sidebar.write("**成分的个数**")
n_components = st.sidebar.selectbox("", [1, 2, 3, 4])

st.sidebar.write("**只展示结果**")
only_visual = st.sidebar.selectbox("", ["是", "否"])
only_visual = only_visual == "是"

flag = st.sidebar.button("运行")

if flag:
    if not only_visual:
        st.write("**正在运行...**")
        main(time_unit, n_components)
        st.text("**运行完毕！**")
    else:
        load_result_log = st.text("")
        load_result_log.write("**加载结果...**")
        image = os.listdir("./Img")
        for img in image:
            st.image(os.path.join("./Img", img))
        load_result_log.write("**加载完毕！**")