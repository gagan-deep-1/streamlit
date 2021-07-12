import streamlit as st
import pandas as pd
import json
st.set_page_config(layout="wide")
@st.cache(allow_output_mutation=True)
def loadData(path):
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

try:
	st.write("# Entities and Aliases")
	entities, aliases, contexts = loadData("alias_detection_demo_APDO_influenster.json")
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
