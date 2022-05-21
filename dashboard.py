import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.figure_factory as ff
import plotly.express as px

# set wide page layout
st.set_page_config(layout="wide")

# Import dataset
datacovid = pd.read_excel('datasetcovidjktid.xlsx')

# Dataset selection
covid_JKT = datacovid.loc[:,['Variant_Suspect','Day','JKT_DAILY_POSITIVE','JKT_DAILY_DEATH','JKT_DAILY_HOSPITALIZED',       'JKT_DAILY_POSTRATE','JKT_DAILY_TESTED','Risk','Risk_Criteria']]
covid_ABG = datacovid.loc[datacovid.Variant_Suspect == 'Alpha-Beta-Gamma', ['Day', 'JKT_DAILY_POSITIVE',
                                                                            'JKT_DAILY_DEATH', 'JKT_DAILY_HOSPITALIZED', 'JKT_DAILY_POSTRATE', 'JKT_DAILY_TESTED', 'Risk', 'Risk_Criteria']]
covid_Delta = datacovid.loc[datacovid.Variant_Suspect == 'Delta', ['Day', 'JKT_DAILY_POSITIVE',
                                                                   'JKT_DAILY_DEATH', 'JKT_DAILY_HOSPITALIZED', 'JKT_DAILY_POSTRATE', 'JKT_DAILY_TESTED', 'Risk', 'Risk_Criteria']]
covid_Omicron = datacovid.loc[datacovid.Variant_Suspect == 'Omicron', ['Day', 'JKT_DAILY_POSITIVE',
                                                                       'JKT_DAILY_DEATH', 'JKT_DAILY_HOSPITALIZED', 'JKT_DAILY_POSTRATE', 'JKT_DAILY_TESTED', 'Risk', 'Risk_Criteria']]

#Ticks for heatmaps and pairplot
ticks =['Day','Daily Positive','Daily Death','Daily Hospitalized','Daily Positivity Rate','Daily Tested','Risk']

# Title
with st.container():
    st.title("DASHBOARD COVID 19 - CASE STUDY DKI JAKARTA")

# Opening Summary
with st.container():
    st.header('DATA SUMMARY')
    col2, col3, col4, col5 = st.columns(4)

    # summary
    with col2:
        st.write('#### Initial Observation Date:')
        # get first row data from Tanggal column
        startdate = datacovid['Tanggal'].iloc[0]
        st.write(startdate.strftime('%d-%m-%Y'))
        st.write('#### Last Observation Date:')
        totalobsday = len(datacovid.Tanggal)  # total observation day
        # get last row data from Tanggal column
        lastdate = datacovid['Tanggal'].iloc[totalobsday-1]
        st.write(lastdate.strftime('%d-%m-%Y'))

    with col3:
        st.write('#### Total Tested:')
        st.write("{:,.0f}".format(datacovid.JKT_DAILY_TESTED.sum()))
        st.write('#### Highest Positivity Rate:')
        st.write("{:.2f}".format(datacovid.JKT_DAILY_POSTRATE.max()))

    with col4:
        st.write('#### Total Positive Case:')
        st.write("{:,}".format(datacovid.JKT_DAILY_POSITIVE.sum()))
        st.write('#### Highest Daily Positive Case:')
        st.write("{:,}".format(datacovid.JKT_DAILY_POSITIVE.max()))

    with col5:
        st.write('#### Total Death Case:')
        st.write("{:,}".format(datacovid.JKT_DAILY_DEATH.sum()))
        st.write('#### Highest Daily Death Case:')
        st.write("{:,}".format(datacovid.JKT_DAILY_DEATH.max()))

# Historical Timeline Graph
with st.container():
    st.header('TIMELINE CURVE')
    st.write('#### Type of Covid-19 Variant:')
    st.write("""
    1. Alpha - Beta - Gamma (First Wave)
    2. Delta (Second Wave)
    3. Omicron (Third Wave)
    Above variant is considered as Variant of Concern (VOC) as per WHO.
    """)

    # create column formatting
    col1, col2 = st.columns(2)
    # define value of X and Y
    x = datacovid.Tanggal
    value1 = datacovid.JKT_DAILY_POSITIVE
    value2 = datacovid.JKT_DAILY_DEATH
    value3 = datacovid.JKT_DAILY_HOSPITALIZED
    sizefont = 5

    with col1:
        # This column is for historical Graphic

        # create selectbox
        histselect = st.selectbox(
            'Please select data label for timeline data',
            ('Positive Case', 'Death Case', 'Hospitalized Case')
        )

        # create parameter from selectbox
        if histselect == 'Positive Case':
            colorgraph = 'tab:red'
            yvalue = value1
            labely = 'Daily Positive'
        elif histselect == 'Death Case':
            colorgraph = 'tab:blue'
            yvalue = value2
            labely = 'Daily Death'
        else:
            colorgraph = 'tab:green'
            yvalue = value3
            labely = 'Daily Hospitalized'

        fig1 = plt.figure(figsize=(4, 3))
        color = colorgraph
        plt.title('Historical Timeline', fontsize=6)
        plt.xlabel('Date', fontsize=sizefont)
        plt.ylabel(labely, fontsize=sizefont)
        plt.fill_between(x, yvalue, color=color)
        plt.tick_params(axis='y')
        plt.xticks(fontsize=sizefont)
        plt.yticks(fontsize=sizefont)
        st.pyplot(fig1)

    with col2:
        varselect = st.selectbox(
            'Please select data label comparison of each variant',
            ('Positive Case', 'Death Case', 'Hospitalized Case')
        )

        if varselect == 'Positive Case':
            y1 = covid_ABG.JKT_DAILY_POSITIVE
            y2 = covid_Delta.JKT_DAILY_POSITIVE
            y3 = covid_Omicron.JKT_DAILY_POSITIVE
            labely = 'Daily Positive'
        elif varselect == 'Death Case':
            y1 = covid_ABG.JKT_DAILY_DEATH
            y2 = covid_Delta.JKT_DAILY_DEATH
            y3 = covid_Omicron.JKT_DAILY_DEATH
            labely = 'Daily Death'
        else:
            y1 = covid_ABG.JKT_DAILY_HOSPITALIZED
            y2 = covid_Delta.JKT_DAILY_HOSPITALIZED
            y3 = covid_Omicron.JKT_DAILY_HOSPITALIZED
            labely = 'Daily Hospitalized'

        x1 = covid_ABG.Day
        x2 = covid_Delta.Day
        x3 = covid_Omicron.Day

        fig2 = plt.figure(figsize=(4, 3))
        plt.title('Variant Observation', fontsize=6)
        plt.fill_between(x1, y1, 'b', label="Daily Alpha-Beta-Gamma", alpha=1, linewidth=0.5)
        plt.fill_between(x2, y2, 'r', label="Daily Delta", alpha=0.7, linewidth=0.5)
        plt.fill_between(x3, y3, 'g', label="Daily Omicron", alpha=0.6, linewidth=0.5)
        plt.xlabel('Day', fontsize=sizefont)
        plt.ylabel(labely, fontsize=sizefont)
        plt.legend(fontsize=sizefont)
        plt.xticks(fontsize=sizefont)
        plt.yticks(fontsize=sizefont)
        st.pyplot(fig2)

# pie chart
with st.container():
    st.header('VARIANT IN PERCENTAGE')

    varnames = ['Alpha-Beta-Gamma', 'Delta', 'Omicron']
    value4positive = [covid_ABG.JKT_DAILY_POSITIVE.sum(),
                      covid_Delta.JKT_DAILY_POSITIVE.sum(),
                      covid_Omicron.JKT_DAILY_POSITIVE.sum()]
    value4death = [covid_ABG.JKT_DAILY_DEATH.sum(),
                   covid_Delta.JKT_DAILY_DEATH.sum(),
                   covid_Omicron.JKT_DAILY_DEATH.sum()]
    value4hospitalize = [covid_ABG.JKT_DAILY_HOSPITALIZED.sum(),
                         covid_Delta.JKT_DAILY_HOSPITALIZED.sum(),
                         covid_Omicron.JKT_DAILY_HOSPITALIZED.sum()]

    col1, col2, col3 = st.columns(3)

    with col1:
        fig3 = plt.figure(figsize=(4, 3))
        explode = (0.05, 0.05, 0.05)
        plt.pie(value4positive, wedgeprops=dict(width=0.7, edgecolor='w'), autopct='%1.1f%%', explode=explode, labels=varnames, shadow=True, startangle=30)
        plt.title('Composition Overall Positive')
        st.pyplot(fig3)

    with col2:
        fig4 = plt.figure(figsize=(4, 3))
        explode = (0.05, 0.05, 0.05)
        plt.pie(value4death, wedgeprops=dict(width=0.7, edgecolor='w'), autopct='%1.1f%%', explode=explode, labels=varnames, shadow=True, startangle=30)
        plt.title('Composition Overall Death')
        st.pyplot(fig4)

    with col3:
        fig5 = plt.figure(figsize=(4, 3))
        explode = (0.05, 0.05, 0.05)
        plt.pie(value4hospitalize, wedgeprops=dict(width=0.7, edgecolor='w'), autopct='%1.1f%%', explode=explode, labels=varnames, shadow=True, startangle=30)
        plt.title('Composition Overall Hospitalized')
        st.pyplot(fig5)

# count plot and box plot
with st.container():
    st.header('BOXPLOT OF VARIANT AND COUNT PLOT OF RISK')
    col1, col2 = st.columns(2)

    with col1:
        fig6 = plt.figure(figsize=(4, 3))
        sns.boxplot(x="Variant_Suspect",
                    y="JKT_DAILY_POSITIVE", data=datacovid)
        plt.xlabel('Variant', fontsize=sizefont+1)
        plt.ylabel('Daily Positive', fontsize=sizefont+1)
        plt.xticks(fontsize=sizefont+1)
        plt.yticks(fontsize=sizefont+1)
        st.pyplot(fig6)

    with col2:
        fig7 = plt.figure(figsize=(4, 3))
        sns.boxplot(x="Variant_Suspect", y="JKT_DAILY_DEATH", data=datacovid)
        plt.xlabel('Variant', fontsize=sizefont+1)
        plt.ylabel('Daily Death', fontsize=sizefont+1)
        plt.xticks(fontsize=sizefont+1)
        plt.yticks(fontsize=sizefont+1)
        st.pyplot(fig7)

# correlation heat map
with st.container():
    st.header('CORRELATION HEATMAP')
    col1, col2 = st.columns(2)

    #create correlation
    corrdata_Delta = covid_Delta.corr()
    corrdata_Omicron = covid_Omicron.corr()

    with col1:
        fig8 = plt.figure()
        sns.heatmap(corrdata_Delta, annot=True, xticklabels=ticks, yticklabels=ticks)
        st.pyplot(fig8)

    with col2:
        fig9 = plt.figure()
        sns.heatmap(corrdata_Omicron, annot=True, xticklabels=ticks, yticklabels=ticks)
        st.pyplot(fig9)

    st.write('')

# Show pair plot

st.header('PAIR PLOT GRAPH ')

show_pairplot = st.checkbox('Show Pair Plot Graph')

if show_pairplot:
    fig10 = sns.pairplot(covid_JKT, hue='Variant_Suspect')
    handles = fig10._legend_data.values()
    labels = fig10._legend_data.keys()
    st.pyplot(fig10)
