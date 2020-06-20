import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk
import plotly.express as px
import datetime
import matplotlib.pyplot as plt 
import time as time




def main():


	lat_long  = pd.read_csv("C:/Users/lenovo india/Desktop/covid 19 india/lat_long.csv")

	lat_long.rename(columns= {'Latitude (generated)':'latitude', 'Longitude (generated)':'longitude'},inplace=True)
	lat_long.set_index('State / Union Territory', inplace=True)

	covid_data = pd.read_csv("C:/Users/lenovo india/Desktop/covid 19 india/covid_data_daily.csv")
	covid_data.drop(['ConfirmedIndianNational','ConfirmedForeignNational','Sno','Number of Records'], axis = 1 ,inplace=True)
		
	covid_last = covid_data[2882:2918]
	covid_last.set_index('State/UnionTerritory', inplace= True)
	merged_data = covid_last.join(lat_long, how="inner")

	covid_data['Dates'] = covid_data['Date'].str.cat(covid_data['Time'], sep =" ")
	covid_data['Dates'] = pd.to_datetime(covid_data['Dates'], format = '%d-%m-%Y %I:%M %p')
	covid_data.set_index('Dates', inplace=True)
	confirmed_cases = covid_data.resample('D').agg({'Confirmed':'sum', 'Cured':'sum','Death':'sum'})
	
	
	merged_data['Recovery Rate'] = (merged_data['Cured']/merged_data['Confirmed'])*100
	merged_data['Fatality Rate'] = (merged_data['Deaths']/merged_data['Confirmed'])*100

	sorted_merged_data = merged_data.sort_values(by=['Confirmed'], ascending = False)


	menu = ["Home","State Trends"]
	choice = st.sidebar.selectbox("Menu", menu)

	if choice == "Home":
		st.title("🦠😷🔬Covid-19 in India: Analysis")
		st.markdown("This is a streamlit application to analyze the spread"
				" and trends of Corona Virus in India")
		st.subheader("Home")
		with st.spinner('In progress...'):
			time.sleep(5)
		st.map(merged_data[["latitude", "longitude"]].dropna(how='any'))

		st.write(" ### Cumulative Count for all Confirmed Cases, Cured & Deaths")
		st.line_chart(data = confirmed_cases['Confirmed'])

		st.write("### Top 10 States w.r.t. Confirmed Cases as on June 11, 2020")
		

		sorted_merged_data['State/UnionTerritory'] = sorted_merged_data.index

		bar_plot = px.bar(sorted_merged_data.head(10), x='Confirmed', y='State/UnionTerritory')
		st.plotly_chart(bar_plot)
		st.bar_chart(sorted_merged_data.head(10))

		defaultcols = ['Cured',	'Deaths', 'Confirmed','Recovery Rate', 'Fatality Rate']
		#if st.checkbox("Show raw data", False):
		cols = st.multiselect("Choose different parameters", merged_data.columns.tolist(), default=defaultcols)
		st.dataframe(sorted_merged_data[cols].head(10).style.highlight_max(axis=0))

		#st.table(covid_data)

	elif choice == "State Trends":

		state_level = pd.read_csv(r"C:\Users\lenovo india\Desktop\covid 19 india\state_level_daily.csv")
		district_data = pd.read_csv(r"C:\Users\lenovo india\Desktop\covid 19 india\district_level_latest.csv")
		state_level['Date'] = pd.to_datetime(state_level['Date'], format = '%d-%b-%y')

		state_list = state_level['State_Name'].unique()
		#state_list = state_list.sort()
		
		state_list = np.delete(state_list, [34,35])  # removing total and state unassigned row

		#st.write(state_list)
		
		choice = st.sidebar.selectbox("Select State", state_list)

		st.title("🦠😷🔬Covid-19 in {}: Analysis".format(choice))
		st.markdown("This is a streamlit application to analyze the spread"
				" and trends of Corona Virus in India")
		#if st.sidebar.button('Select State'):
		#	st.sidebar.selectbox("Select State to view data of that state only", state_list)
		state_line_chart = state_level[state_level['State_Name'] == choice]
		state_line_chart.set_index('Date', inplace=True)

		#st.header("Trends for {}".format(choice))

		#st.markdown("### Confirmed: **_ {}_ **         Active: **_ {}_ **".format(state_line_chart.Confirmed.sum(),state_line_chart.Confirmed.sum()-state_line_chart.Recovered.sum()-state_line_chart.Deceased.sum()))
		#st.markdown("### Recovered: **_ {}_ **         Deceased: **_ {}_ **".format(state_line_chart.Recovered.sum(),state_line_chart.Deceased.sum()))

		st.write("Confirmed:", state_line_chart.Confirmed.sum(), "Active: ", state_line_chart.Confirmed.sum()-state_line_chart.Recovered.sum()-state_line_chart.Deceased.sum())
		st.write("Recovered:",  state_line_chart.Recovered.sum(), "Deceased: ", state_line_chart.Deceased.sum())

		st.subheader("Daily Cases")
		st.line_chart(data = state_line_chart['Confirmed'])

		#st.table(district_data);
		defaultcols = ['State',	'District', 'Confirmed','Active', 'Recovered', 'Deceased']
		#if st.checkbox("Show raw data", False):
		cols = st.multiselect("Choose different parameters", defaultcols, default=defaultcols)
		st.dataframe(district_data[district_data['State']==choice][cols])

		


if __name__ == '__main__':
	main()