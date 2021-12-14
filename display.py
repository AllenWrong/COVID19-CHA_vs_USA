import os

import streamlit as st
from 生成结果 import start

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
        start(time_unit, n_components)
        st.text("**运行完毕！**")

        load_result_log = st.text("")
        load_result_log.write("**加载结果...**")
        path = os.path.join("./Img", time_unit)
        image = os.listdir(path)
        # for img in image:
        #     if img.startswith(lang_type):
        #         fig_title = img.split(",")[1]
        #         st.write("**" + fig_title + "**")
        #         st.image(os.path.join(path, img))
        # load_result_log.write("**加载完毕！**")

    else:
        col1, col2 = st.columns(2)

        load_result_log = st.text("")
        load_result_log.write("**加载结果...**")
        path = os.path.join("Best-Img", time_unit)
        image = os.listdir(path)

        cha_list = []
        eng_list = []
        for img in image:
            # if img.startswith("CHA"):
            #     cha_list.append(os.path.join(path, img))
            # else:
                # eng_list.append(os.path.join(path, img))

            if img.startswith("CHA"):
                with col1:
                    st.write("<span>",unsafe_allow_html=True)
                    fig_title = img.split(".")[0]
                    st.write("**" + fig_title + "**")
                    st.image(os.path.join(path, img))
            else:
                with col2:
                    fig_title = img.split(".")[0]
                    st.write("**" + fig_title + "**")
                    st.image(os.path.join(path, img))
                    st.write("</span>", unsafe_allow_html=True)
            # st.columns()

        load_result_log.write("**加载完毕！**")