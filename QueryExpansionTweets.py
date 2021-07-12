import streamlit as st
import pandas as pd
import json
st.set_page_config(layout="wide")
@st.cache(allow_output_mutation=True)
def loadData(path):
	#st.write("Cache miss: my_cached_func(", a, ", ", b, ") ran")
	data = json.load(open(path))
	keywords = []
	linked_seed_keywords = {}
	contexts = {}
	for keyword in data["query_expansion_keywords"][2:]:
	    keywords.append([keyword["linked_seed_keywords"][0],keyword["keyword"],float(keyword["frequency_score"]),float(keyword["relevance_score"]),keyword["specificity"]])
	    #print(keywords)
	    for linked_seed_keyword in keyword["linked_seed_keywords"]:	
		    try:
		        linked_seed_keywords[linked_seed_keyword].append(keyword["keyword"])
		    except Exception as e:
		    	linked_seed_keywords[linked_seed_keyword]=[keyword["keyword"]]
	    #print(linked_seed_keywords)
	    for context in keyword["contexts"]:
	        try:
	            contexts[keyword["keyword"]].append([context["context_set"][0],context["content_id"]])
	        except:
	            contexts[keyword["keyword"]] =[[context["context_set"][0],context["content_id"]]]
	    #print(contexts)
	return keywords, linked_seed_keywords, contexts

try:
	st.write("# Query Expansion Using KG (Tweets)")
	col1, col2, col3, col10, col11 = st.beta_columns(5)
	keywords, linked_seed_keywords, contexts = loadData("keyword_expansion_demo_APDO_fulltweets_full.json")
	data = pd.DataFrame(keywords,columns =['linked_seed_keyword','keyword',"Frequecy Score",'Relevance Score','specificity'])
	#data = data.set_index('linked_seed_keyword', append=True).swaplevel(0,1)
	h = list(data["linked_seed_keyword"])
	h.sort()
	with col1:

		selected_indices1 = st.selectbox('Select Periferal / Category:', list(set(list(data["specificity"]))))
	#selected_indices2 = st.multiselect('Select Seed Keyword:', list(set(h)))
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
	#st.write(min(list(data1["Frequecy Score"])))

except Exception as e:
    st.error(e)

