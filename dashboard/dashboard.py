import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Set the page layout to wide for better use of space
st.set_page_config(layout='wide', page_title="Sales Dashboard")

sns.set(style='darkgrid')

# Load data
all_df = pd.read_csv("dashboard/all_data.csv")

# Function to aggregate top-performing product categories
def create_best_category_df(df):
    sum_category_df = all_df.groupby(by="product_category_name_english").order_item_id.count().sort_values(ascending=True).reset_index()
    sum_category_df.rename(columns={
        "product_category_name_english": "product_category",
        "order_item_id": "total_order"
    }, inplace=True)
    return sum_category_df.tail(5)

def create_worst_category_df(df):
    sum_category_df = all_df.groupby(by="product_category_name_english").order_item_id.count().sort_values(ascending=False).reset_index()
    sum_category_df.rename(columns={
        "product_category_name_english": "product_category",
        "order_item_id": "total_order"
    }, inplace=True)
    return sum_category_df.tail(5)

# Function to aggregate city distribution
def create_city_distribution_df(df):
    city_distribution_df = df.groupby(by="customer_city").order_id.count().sort_values(ascending=False).reset_index()
    city_distribution_df.rename(columns={
        "customer_city": "city",
        "order_id": "total_order"
    }, inplace=True)
    return city_distribution_df.head(5)

best_category_df = create_best_category_df(all_df)
worst_category_df = create_worst_category_df(all_df)
city_distribution_df = create_city_distribution_df(all_df)

best_category = best_category_df.iloc[-1]['product_category']
worst_category = worst_category_df.iloc[-1]['product_category']
best_city = city_distribution_df.iloc[0]['city']

st.title("Sales Dashboard")
st.markdown("### Key Insights")

st.markdown(f"""
- **Best Performing Category:** {best_category}  
- **Worst Performing Category:** {worst_category}  
- **City with Most Orders:** {best_city}
""")

col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("Best Performing Categories")
    fig, ax = plt.subplots(figsize=(10, 7))
    
    colors = sns.color_palette("Blues", len(best_category_df))
    
    ax.barh(best_category_df['product_category'], best_category_df['total_order'], color=colors)
    ax.set_xlabel('Total Orders', fontsize=20)  
    ax.set_ylabel(None)
    ax.set_title('Product Categories by Sales', fontsize=24)  
    
    ax.tick_params(axis='y', labelsize=16)  
    ax.tick_params(axis='x', labelsize=16)  
    
    st.pyplot(fig)

with col2:
    st.markdown("<h4 style='text-align: center;'>Worst Performing Categories</h4>", unsafe_allow_html=True)
    
    fig, ax = plt.subplots(figsize=(10, 7))
    
    colors = sns.color_palette("Blues", len(worst_category_df))
    
    ax.barh(worst_category_df['product_category'], worst_category_df['total_order'], color=colors)
    ax.set_xlabel('Total Orders', fontsize=20)  
    ax.set_ylabel(None)
    ax.set_title('Product Categories by Sales', fontsize=24)  
    
    ax.tick_params(axis='y', labelsize=16)  
    ax.tick_params(axis='x', labelsize=16)  
    
    st.pyplot(fig)

with col3:
    st.subheader("City Distribution")
    
    fig, ax = plt.subplots(figsize=(15, 7))
    
    sns.barplot(y="total_order", x="city", data=city_distribution_df, palette="Blues_r")
    
    ax.set_xlabel("Number of Sales", fontsize=20)  
    ax.set_title("Top 5 Cities by Sales", fontsize=24)  
    
    ax.tick_params(axis='y', labelsize=16)  
    ax.tick_params(axis='x', labelsize=16)  
    
    st.pyplot(fig)