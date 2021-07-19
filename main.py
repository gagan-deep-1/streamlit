import streamlit as st
import pandas as pd
import json
st.set_page_config(layout="wide")
def loadDataQE(path):
    data = json.load(open(path))
    keywords = []
    linked_seed_keywords = {}
    contexts = {}
    for keyword in data["query_expansion_keywords"][2:]:
        keywords.append([keyword["linked_seed_keywords"][0],keyword["keyword"],float(keyword["frequency_score"]),float(keyword["relevance_score"]),keyword["specificity"]])
        for linked_seed_keyword in keyword["linked_seed_keywords"]: 
            try:
                linked_seed_keywords[linked_seed_keyword].append(keyword["keyword"])
            except Exception as e:
                linked_seed_keywords[linked_seed_keyword]=[keyword["keyword"]]
        for context in keyword["contexts"]:
            try:
                contexts[keyword["keyword"]].append([context["context_set"][0],context["content_id"]])
            except:
                contexts[keyword["keyword"]] =[[context["context_set"][0],context["content_id"]]]
    return keywords, linked_seed_keywords, contexts
def loadDataEA(path):
    #st.write("Cache miss: my_cached_func(", a, ", ", b, ") ran")
    data = json.load(open(path))
    entities = []
    aliases = {}
    contexts = {}
    for entity in data["aliases"]:
        entities.append([entity["entity"],entity["entity_relevance_score"],entity["entity_frequency_score"],entity["entity_support_count"]])
        try:
            aliases[entity["entity"]].append([entity["alias"],entity["alias_relevance_score"],entity["alias_frequency_score|entity"],entity["alias_support_count"]])
        except:
            aliases[entity["entity"]] = [[entity["alias"],entity["alias_relevance_score"],entity["alias_frequency_score|entity"],entity["alias_support_count"]]]
        for context in entity["contexts"]:
            try:
                contexts[entity["alias"]].append([context["context"],context["node_id"]])
            except:
                contexts[entity["alias"]] =[[context["context"],context["node_id"]]]
    return entities, aliases, contexts
def dashBoardQE(path, heading):
    try:
        st.write(heading)
        col1, col2, col3, col10, col11 = st.beta_columns(5)
        keywords, linked_seed_keywords, contexts = loadDataQE(path)
        data = pd.DataFrame(keywords,columns =['linked_seed_keyword','keyword',"Frequecy Score",'Relevance Score','specificity'])
        #data = data.set_index('linked_seed_keyword', append=True).swaplevel(0,1)
        h = list(data["linked_seed_keyword"])
        h.sort()
        with col1:
            selected_indices1 = st.selectbox('Select Periferal / Category:', list(set(list(data["specificity"]))))
        with col2:
            container = st.beta_container()
            all_options = st.checkbox("Select all Seed Keywords",value = True)
            if all_options:
                selected_indices2 = container.multiselect("Select Seed Keyword:",
                     ["Selected all"],["Selected all"])
                if selected_indices2:           
                    selected_indices2 = list(set(h))
            else:
                selected_indices2 =  container.multiselect("Select Seed Keyword:",
                    list(set(h)))   
        with col10:
            values1 = st.slider(
                'Select a range of values',
                0.0, 1.0,(0.0, 1.0))
        with col11:
            values2 = st.slider(
                'Select a range of values2',
                0.0, 1.0, (0.0, 1.0))

        data1 = data.loc[(data['specificity'] == selected_indices1) &  (data['linked_seed_keyword'].isin(selected_indices2)) & (data["Frequecy Score"] >= values1[0]) & (data["Frequecy Score"] <= values1[1]) & (data["Relevance Score"] >= values2[0]) & (data["Relevance Score"] <= values2[1]) ]
        with col3:
            selected_indices3 = st.selectbox('Select Keyword:', list(data1["keyword"]))#list(contexts.keys()))
        st.write("##### Seed Keyword => Expanded Keyword")
        data1 = data1.sort_values(by = 'linked_seed_keyword' ,ascending = True)[['linked_seed_keyword','keyword',"Frequecy Score",'Relevance Score']]
        data2 = pd.DataFrame(contexts[selected_indices3],columns =['context set',"context id"])
        col4, col5 = st.beta_columns(2)
        st.dataframe(data=data1, height=300,width = 1150)
        st.write("##### Context")
        st.table(data=data2)#, height=300, width = 700)
    except Exception as e:
        st.error(e)
def dashBoardEA(path, heading):
    try:
        st.write(heading)
        entities, aliases, contexts = loadDataEA(path)
        col1, col2 = st.beta_columns(2)
        data = pd.DataFrame(entities,columns =['Entity',"Relevance",'Frequency','CNT'])
        data1 = data
        #data1 = data1.style.set_properties(**{'font-size': '14pt',})
        with col1:
            selected_indices = st.selectbox('Select Entity:', list(set(list(data["Entity"]))))
            st.write("##### Entity Table")
            st.dataframe(data=data1, height=300)
        data2 = pd.DataFrame(aliases[selected_indices],columns =['Alias',"Relevance(Alias)",'Frequency','Entity support count'])

        with col2:
            selected_indices1 = st.selectbox('Select Alias:', list(set(list(data2["Alias"]))))
            #xdata2 = data2.style.set_properties(**{'font-size': '14pt',})
            st.write("##### Alias Table for entity : ",selected_indices, data2)
        data3 = pd.DataFrame(contexts[selected_indices1],columns =['context',"node id"])
        st.write("#### Contexts for Alias:",selected_indices1)
        #data3 = data3.style.set_properties(**{'font-size': '14pt',})
        st.table(data3)
        #st.write("Context Table", data3)
    except Exception as e:
        st.error(e
        )
st.markdown(
    '<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@4.5.3/dist/css/bootstrap.min.css" integrity="sha384-TX8t27EcRE3e/ihU7zmQxVncDAy5uIKz4rEkgIXeMed4M0jlfIDPvg6uqKI2xXr2" crossorigin="anonymous">',
    unsafe_allow_html=True,
)
query_params = st.experimental_get_query_params()
tabs = ["Query Expansion Influenster","Entities n Aliases Influenster","Query Expansion Tweets", "Entities n Aliases Tweets"]
if "tab" in query_params:
    active_tab = query_params["tab"][0]
else:
    active_tab = "Entities n Aliases Influenster"

if active_tab not in tabs:
    st.experimental_set_query_params(tab="Entities n Aliases Influenster")
    active_tab = "Entities n Aliases Influenster"

li_items = "".join(
    f"""
    <li class="nav-item">
        <a class="nav-link{' active' if t==active_tab else ''}" href="/?tab={t}">{t}</a>
    </li>
    """
    for t in tabs
)
tabs_html = f"""
    <ul class="nav nav-tabs">
    {li_items}
    </ul>
"""

st.markdown(tabs_html, unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

if active_tab == "Entities n Aliases Influenster":
    dashBoardEA("JSONdata/alias_detection_demo_APDO_influenster.json","# Entities and Aliases (influenster)")

elif active_tab == "Query Expansion Influenster":
    dashBoardQE("JSONdata/keyword_expansion_demo_APDO_influenster_full.json","# Query Expansion Using KG (influenster)")


elif active_tab == "Query Expansion Tweets":
    dashBoardQE("JSONdata/keyword_expansion_demo_APDO_fulltweets_full.json","# Query Expansion Using KG (Tweets)")
elif active_tab == "Entities n Aliases Tweets":
    dashBoardQE("JSONdata/alias_detection_demo_APDO_fulltweets.json","# Entities and Aliases(Tweets)")
else:
    st.error("Something has gone terribly wrong.")