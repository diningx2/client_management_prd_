
import streamlit as st
from get_branch_info import get_branch_info
def branch_manage():
    #st.write(st.session_state['client_list'])
    client_options = ['-']
    for n in st.session_state['client_list'].keys():
        client_options.append(n)
    #st.write(st.session_state['branch_dic'])

    client_option = st.selectbox('クライアント名を選んでください', client_options)
    if client_option in st.session_state['client_list'].keys():
        branch_options = ['-']
        for name in st.session_state['client_list'][client_option].keys():
            branch_options.append(name)
        branch_option = st.selectbox('支店名を選んでくれーい', branch_options)

        if branch_option in st.session_state['client_list'][client_option].keys():
            bId = st.session_state['client_list'][client_option][branch_option]
            get_branch_info(branch_option, bId)