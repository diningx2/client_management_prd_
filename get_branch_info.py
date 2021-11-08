import streamlit as st
from categories import categories
import pandas as pd

category = pd.DataFrame(data=categories)

def get_branch_info(branch_name, bId):
    
    st.title(branch_name)
    branch_data = st.session_state['db'].collection('BranchInfo').document(bId).get().to_dict()
    
    
    prefecture = st.text_input('都道府県', value=branch_data['prefecture'])
    municipality = st.text_input('市町村', value=branch_data['municipality'])
    user_name = st.text_input('user name', value=branch_data['user_name'])
    password = st.text_input('password', value=branch_data['password'])
    home_page_url = st.text_input('ホームページ URL', value=branch_data['sns'][0])
    facebook_url = st.text_input('Facebook URL', value=branch_data['sns'][1])
    line_url = st.text_input('LINE URL', value=branch_data['sns'][2])
    twitter_url = st.text_input('Twitter URL', value=branch_data['sns'][3])
    instagram_url = st.text_input('Instagram URL', value=branch_data['sns'][4])

    dai_value = ['-']
    for v in branch_data['type']:
        print(v)
        for i in range(len(category)):
            if v in category['sho'][i]:
                dai_v = category['dai'][i]
                if dai_v not in dai_value:
                    dai_value.append(dai_v)
    st.dataframe(category)
    dai_options = category['dai'].unique()
    dai_option = st.multiselect('大分類', dai_options, default=dai_value)

    chu_op = ['-']
    for d in dai_option:
        chu = category[category['dai'] == d]['chu']
        for c in chu:
            chu_op.append(c)
    chu_op = list(set(chu_op))

    chu_option = st.multiselect('中分類', chu_op)

    sho_op = ['-']
    for c in chu_option:
        sho = category[category['chu'] == c]['sho']
        for sho_list in sho:
            #sho_list = sho_i.replace('[', '').replace(']', '').replace("'", '').split(',')
            print(sho_list)
            for s in sho_list:
                if s not in sho_op:
                    s = s
                    sho_op.append(s)

    sho_option = st.multiselect('小分類', sho_op)
    branch_type = [i for i in sho_option if i != '-']
    st.write('保存を押すと')
    st.write(branch_data['type'])
    st.write('から')
    st.write(branch_type)
    st.write('へ変更されます。')
    """
    type0 = st.text_input('店舗タイプ1', value=branch_data['type'][0])
    type1 = st.text_input('店舗タイプ2', value=branch_data['type'][1])
    type2 = st.text_input('店舗タイプ3', value=branch_data['type'][2])
    type3 = st.text_input('店舗タイプ4', value=branch_data['type'][3])
    type4 = st.text_input('店舗タイプ5', value=branch_data['type'][4])
    """

    save_button = st.button('保存')
    if save_button and (len(branch_type) < 6):
        branch_data['prefecture'] = prefecture
        branch_data['municipality'] = municipality
        branch_data['user_name'] = user_name
        branch_data['password'] = password
        branch_data['sns'][0] = home_page_url
        branch_data['sns'][1] = facebook_url
        branch_data['sns'][2] = line_url
        branch_data['sns'][3] = twitter_url
        branch_data['sns'][4] = instagram_url

        branch_data['type'] = branch_type
        st.session_state['db'].collection('BranchInfo').document(bId).set(branch_data)
        st.write('保存しました！')
    elif save_button:
        st.write('小分類は5個以下にしてください')