import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


# Page title
st.title(
    "Airline Passenger Satisfaction Dashboard ✈️ "
)


# Short intro
st.write(
    "This dashboard presents insights from Exploratory Data Analysis (EDA)."
)

# Load data
df = pd.read_csv(
    "Invistico_Airline.csv"
)


c1, c2, c3 = st.columns(3)

with c1:
    st.metric(
        "Rows",
        df.shape[0]
    )

with c2:
    st.metric(
        "Columns",
        df.shape[1]
    )

with c3:
    st.metric(
        "Missing Values",
        df.isnull().sum().sum()
    )



#filter 1
travel_class = st.multiselect(
"Select Class",
df["Class"].unique(),
default=df["Class"].unique()
)

df = (
df[
df["Class"].isin(travel_class)
]
)

# Show dataset
st.header("Dataset Preview")

st.dataframe(
    df.head()
)

# Show shape
st.write(
    "Rows and Columns:",
    df.shape
)
st.divider()
#vis 1
st.header(
    "Overall Satisfaction"
)


st.markdown("""
This visualization shows the total satisfied vs dissatisfied customers.""")


sat = (
    df["satisfaction"].value_counts(normalize=True)*100

)
plt.figure(figsize=(3,3))
plt.pie(
    sat,
    labels=sat.index,
    autopct="%1.1f%%",
    colors=["#ffe0af","#b1d3c8"]
)
st.pyplot(plt)

st.markdown("""
### Insight📝:
The dataset contains a larger proportion of satisfied passengers compared to dissatisfied passengers, indicating generally positive customer experiences among airline passengers.
""")
st.divider()
#vis 2
st.header(
    "Which Service Cotributes the Most to Customer Satisfaction?"
)


st.markdown("""
This visualization shows the most cotributing services to customer satisfaction.""")

ser_col=['Seat comfort', 'Inflight wifi service', 'Inflight entertainment', 'Online support', 
         'Ease of Online booking', 'On-board service', 'Leg room service', 'Baggage handling', 
         'Checkin service', 'Cleanliness', 'Online boarding']

means = (df.groupby("satisfaction")[ser_col].mean())



means.T.plot(kind = "bar", figsize=(10,6), color=[ "#ffe0af", "#b1d3c8"])
plt.ylabel("Average Rating")
plt.title("Average service rating by satisfaction")
st.pyplot(plt)

st.markdown("""
### Insight📝:
The Inflight Entertainment service appears to be the most contributing service to customer satisfaction, whereas seat comport appears to have the least contribution in customer satisfaction.
""")
st.divider()
#vis3
st.header(
    "Does the class type Business/Eco affect the rating ?"
)


st.markdown("""
This visualization shows the effect of class type  on customer satisfaction rate.""")

#create table for the values
#'normalize' converts counts into percentages
cross = pd.crosstab(df["Class"], df["satisfaction"], normalize="index")

#use the table for the visualization
sns.heatmap(cross, annot=True, cmap="Blues")
st.pyplot(plt)

st.markdown("""
### Insight📝:
The class type has a big affect on the customer satisfaction rate. The satisfaction reaches the highest rate when the class is "Business", which clearly shows the affect of class type on customer satisfaction.
""")
st.divider()
#vis 4,5
st.header(
    "Does the Arrival/Departure Delay affect the rating ?"
)


st.markdown("""
These visualizations show the effect of Arrival/Departure Delay on customer satisfaction rate.
""")

df["Arrival_status"]= pd.cut(df["Arrival Delay in Minutes"], bins = [-1, 0, 15, 60, float("inf")], 
                             labels = [ "On Time", "Short Delay", "Moderate Delay", "Long Delay"])

df["Departure_status"]= pd.cut(df["Departure Delay in Minutes"], bins = [-1, 0, 15, 60, float("inf")], 
                             labels = [ "On Time", "Short Delay", "Moderate Delay", "Long Delay"])
cross = (
pd.crosstab(
df["Arrival_status"],
df["satisfaction"],
normalize="index"
)*100
)

cross.plot(
kind="bar",
stacked=True,
figsize=(8,5),
color=[ "#ffe0af", "#b1d3c8"]
)

plt.ylabel("Satisfaction Percentage")
plt.xlabel("Arrival Status")
plt.title(
"Effect of Arrival Delay on Customer Satisfaction"
)

st.pyplot(plt)


cross = (pd.crosstab(df["Departure_status"], df["satisfaction"], normalize = "index")*100)

cross.plot(kind="bar", stacked="True", figsize=(8,5), color=["#ffe0af", "#b1d3c8"])

plt.ylabel("Satisfaction Percentage")
plt.xlabel("Departure Status")
plt.title("Effect of Departure Delay on Customer Satisfaction")
st.pyplot(plt)
st.markdown("""
### Insight📝:
Both Arrival and Departure Delays affects the satisfaction rate negatively. The more Delay time, the more dissatisfied ratings the flight get.
""")
st.divider()
#vis 6
st.header(
    "Does the Customer Type Affect the Rating ?"
)


st.markdown("""
This visualization shows the effect of customer type on the satisfaction rate.
""")

df["customer_encoded"] = (df["Customer Type"].map({"disloyal Customer":0, "Loyal Customer":1}) )

cross = (
    pd.crosstab(
        df["customer_encoded"], df["satisfaction"], normalize="index"
    )*100
)


cross.plot(
    kind="barh",
    stacked=True,
    figsize=(8, 5),
    color=[ "#ffe0af", "#b1d3c8"]
)

plt.yticks(
    [0,1],
    ["Disloyal", "Loyal"]
)
plt.ylabel("Customer Type")
plt.xlabel("Satisfaction Percentages")
plt.title("Effect of Customer Type on Satisfaction")
plt.legend(title="Satisfaction")
st.pyplot(plt)
st.markdown("""
### Insight📝:
This visualization shows that loyal customers tend to report higher satisfaction rates, whereas disloyal customers appear more likely to be dissatisfied.
""")
st.divider()
#vis 7
st.header(
    "Does the Flight Distance Affect the Rating ?"
)


st.markdown("""
This visualization shows the effect of flight distance on the satisfaction rate.
""")
df["Distance Group"] = pd.cut(
    df["Flight Distance"],
    bins=[0,1000,3000,6000],
    labels=["Short", "Medium", "Long"]
)

cross=(
    pd.crosstab(
        df["Distance Group"],
        df["satisfaction"],
        normalize="index"
    )*100
)

cross.plot(
    kind="barh",
    stacked=True,
    color=["#ffe0af","#b1d3c8"]

)
plt.title("Customer Satisfaction Across Flight Distances")
plt.ylabel("Distance")
st.pyplot(plt)
st.markdown("""
### Insight📝:
This visualization shows that short-distance flights have the highest satisfaction rates, whereas medium- and long-distance flights appear to have lower satisfaction levels.""")
st.divider()
#vis 8
st.header(
    "Which Age Group Shows the Highest Dissatisfaction?"
)


st.markdown("""
This visualization explores whether customer dissatisfaction is concentrated within specific age groups.
""")
#Grouping passengers by age 
df["Age Group"]= pd.cut(df["Age"], bins = [0,20,40,60,100], labels=["<20", "20-40", "40-60", ">60"])

#visualizing the dissatisfied passengers by age 
age_profile = (
    df[
        df["satisfaction"]=="dissatisfied"]
        ["Age Group"].value_counts(
            normalize=True

        )*100
    
)
age_profile.plot(
kind="barh",
color="#ffe0af"
)

plt.xlabel("Percentage")

plt.title(
"Dissatisfied Customers by Age Group"
)
plt.ylabel("Age")
st.pyplot(plt)
st.markdown("""
### Insight📝:
This visualization shows that dissatisfaction was more concentrated among certain age groups (20-40), indicating that passenger experience may vary across age categories.""")

