import streamlit as st
import os
import pandas as pd
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from get_branch_info import get_branch_info
from branch_manage import branch_manage
from registration import branch_registration, client_registration


if not firebase_admin._apps:

    
    # 初期済みでない場合は初期化処理を行う
    keys = {
    "type": os.environ.get('type'),
    "project_id": os.environ.get('project_id'),
    "private_key_id": os.environ.get('private_key_id'),
    "private_key": os.environ.get('private_key'),
    "client_email": os.environ.get('client_email'),
    "client_id": os.environ.get('client_id'),
    "auth_uri": os.environ.get('auth_uri'),
    "token_uri": os.environ.get('token_uri'),
    "auth_provider_x509_cert_url": os.environ.get('auth_provider_x509_cert_url'),
    "client_x509_cert_url": os.environ.get('client_x509_cert_url')
    }
    if os.environ.get('env') is None:
        from secret.secret import keys as KEYS
        keys = KEYS
    #print(type(keys))

    #json_open = open('keys.json', 'w')
    #json.dump(keys, json_open, indent=2)
    #json_open.close()
    #json_open = open('keys.json', 'r')
    #json_file = json.load(json_open)
    #print('=========================')
    #print(json_file)
    #print('=========================')

    cred = credentials.Certificate(keys)
    firebase_admin.initialize_app(cred)

st.session_state['db'] = firestore.client()

if 'login' not in st.session_state:
    st.session_state['login'] = 0
if 'password_manage' not in st.session_state:
    st.session_state['PASSWORD_MANAGE'] = os.environ.get('PASSWORD_MANAGE')
    #st.session_state['PASSWORD_MANAGE'] = PASSWORD_MANAGE

if os.environ.get('env') is None:
    from secret.secret import PASSWORD_MANAGE
    st.session_state['PASSWORD_MANAGE'] = PASSWORD_MANAGE

if st.session_state['login'] == 0:

    st.title('クライアント情報管理画面')
    PASS = st.text_input('PASSWORD', type="password")
    LOGIN_BUTTON = st.button('LogIn')
    if LOGIN_BUTTON:
        print(st.session_state['PASSWORD_MANAGE'])
        if PASS == st.session_state['PASSWORD_MANAGE']:
            for k in st.session_state.keys():
                if k != 'db':
                    st.session_state.pop(k)
            st.session_state['login'] = 1
        else:
            st.write('passwordがちげえぞ')
            

if st.session_state['login'] == 1:
    st.write('ログイン完了')
    logout = st.sidebar.button('Logout')
    if logout:
        st.session_state['login'] = 0
    
    if 'branch_dic' not in st.session_state: 
        query = st.session_state['db'].collection('BranchInfo')
        docs = query.get()
        branch_dic = {}
        branch_user_name_list = []
        for doc in docs:
            branch_data = doc.to_dict()
            branch_dic[doc.id] = branch_data['branchName']
            branch_user_name_list.append(branch_data['user_name'])
            #st.write(branch_data)
        #st.write(branch_dic)
        client_query = st.session_state['db'].collection('ClientInfo')
        client_docs = client_query.get()
        client_list = {}
        client_user_name_list = []
    
        for c_doc in client_docs:
            client_data = c_doc.to_dict()

            client_user_name_list.append(client_data['user_name'])
            client_list[client_data['clientName']] = {}
            for bId in client_data['bId']:
                client_list[client_data['clientName']][branch_dic[bId]] = bId
        
        st.session_state['client_list'] = client_list
        st.session_state['branch_dic'] = branch_dic
        st.session_state['branch_user_name_list'] = branch_user_name_list
        st.session_state['client_user_name_list'] = client_user_name_list
    #st.write(st.session_state['client_list'])
    manage_option = st.selectbox('管理オプション', ['-', '店舗管理', 'クライアント新規登録', '店舗新規登録'])
    if manage_option == '店舗管理':
        branch_manage()
    if manage_option =='クライアント新規登録':
        client_registration()
    if manage_option == '店舗新規登録':
        branch_registration()
        
            