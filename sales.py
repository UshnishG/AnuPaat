import streamlit as st
import pandas as pd
import plotly.express as px
import openai

# Set your OpenAI API key here
openai.api_key = "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"



st.set_page_config(page_title="Sales Analysis | Anupaat",
                    page_icon="📈",
                    layout="wide",
                    initial_sidebar_state="expanded")

# Custom CSS to position the logo
custom_css = ''' 
<style>
.Logo {
    position: absolute;
    top: 5px;
    left: 10px;
    color : orange;
    font-size: 30;
    font-weight: bold;
    marginn: 120px
    }
body {
    background: #07095E;
    color: white; /* Set text color to white for better contrast */
}
</style>
'''
st.markdown(custom_css, unsafe_allow_html=True)

# Add the logo
st.markdown('<div class="Logo">Anupaat</div>', unsafe_allow_html=True)


# # Custom CSS
# st.markdown(
#     """
#     <style>
#     .main {
#         background-color: #fff;
#         padding: 20px;
#     }
#     </style>
#     """,
#     unsafe_allow_html=True
# )

# Function to visualize data
def visualize_data(df):
    st.title('Inventory Sales Data Analysis')

    # Display dataset
    st.subheader('Dataset')
    st.write(df)

    # Outlet Size vs Outlet Sales
    st.subheader('Outlet Size vs Outlet Sales')
    fig_outlet_size_sales = px.bar(df, x='Outlet_Size', y='Item_Outlet_Sales', title='Outlet Size vs Outlet Sales', barmode="group")
    st.plotly_chart(fig_outlet_size_sales)
    highest_item_outlet_size = df.loc[df['Item_Outlet_Sales'].idxmax(), 'Outlet_Size']
    lowest_item_outlet_size = df.loc[df['Item_Outlet_Sales'].idxmin(), 'Outlet_Size']
    st.write(f"Highest Sold Item (Outlet Size): {highest_item_outlet_size}, Lowest Sold Item (Outlet Size): {lowest_item_outlet_size}")

    # Sales of All Items in Medium-sized Outlet
    st.subheader('Sales of All Items in Medium-sized Outlet')
    medium_outlet_df = df[df['Outlet_Size'] == 'Medium']
    fig_sales_all_items = px.bar(medium_outlet_df, x='Item_Type', y='Item_Outlet_Sales', title='Sales of All Items in Medium-sized Outlet')
    st.plotly_chart(fig_sales_all_items)
    highest_item_medium_outlet = medium_outlet_df.loc[medium_outlet_df['Item_Outlet_Sales'].idxmax(), 'Item_Type']
    lowest_item_medium_outlet = medium_outlet_df.loc[medium_outlet_df['Item_Outlet_Sales'].idxmin(), 'Item_Type']
    st.write(f"Highest Sold Item (Medium-sized Outlet): {highest_item_medium_outlet}, Lowest Sold Item (Medium-sized Outlet): {lowest_item_medium_outlet}")

    # Outlet Type vs Outlet Sales
    st.subheader('Outlet Type vs Outlet Sales')
    fig_outlet_type_sales = px.bar(df, x='Outlet_Type', y='Item_Outlet_Sales', title='Outlet Type vs Outlet Sales')
    st.plotly_chart(fig_outlet_type_sales)
    highest_item_outlet_type = df.loc[df['Item_Outlet_Sales'].idxmax(), 'Outlet_Type']
    lowest_item_outlet_type = df.loc[df['Item_Outlet_Sales'].idxmin(), 'Outlet_Type']
    st.write(f"Highest Sold Outlet Type: {highest_item_outlet_type}, Lowest Sold Outlet Type: {lowest_item_outlet_type}")

    # Item Popularity vs Item Type vs Item MRP
    st.subheader('Item Popularity vs Item Type vs Item MRP')
    fig_item_popularity_type_mrp = px.area(df, x='Item_Type', y='Item_MRP', color='Item_Popularity', title='Item Popularity vs Item Type vs Item MRP')
    st.plotly_chart(fig_item_popularity_type_mrp)
    highest_item_item_mrp = df.loc[df['Item_MRP'].idxmax(), 'Item_Type']
    lowest_item_item_mrp = df.loc[df['Item_MRP'].idxmin(), 'Item_Type']
    st.write(f"Highest MRP Item: {highest_item_item_mrp}, Lowest MRP Item: {lowest_item_item_mrp}")

    # Future Sales Prediction (Using GPT API)
    st.subheader('Future Sales Prediction')
    st.write("Predicting future sales...")
    future_sales_prompt = f"""
    Based on the provided sales data, {highest_item_item_mrp} and {highest_item_medium_outlet} please predict the future sales trend for the upcoming months.
    Provide insights on potential growth areas and any patterns observed in the data. The highest sold item in terms of outlet size is {highest_item_outlet_size}, in medium-sized outlet is {highest_item_medium_outlet}, and in terms of outlet type is {highest_item_outlet_type}. Write 10 15 lines only.
    Kindly keep it  10 points only pointwise so that user can read it properly. Also specifically mention the discounts we can give with min profit.
     """
    try:
        predicted_sales = openai.Completion.create(
            engine="gpt-3.5-turbo-instruct",
            prompt=future_sales_prompt,
            max_tokens=1000
        )
        predicted_sales_text = predicted_sales.choices[0].text.strip()
        st.write(predicted_sales_text)

    # Extracting the predicted sales for each item
        predicted_sales_dict = {}
        for line in predicted_sales_text.split('\n'):
            parts = line.split(':')
            if len(parts) == 2:
                item, sales = parts
                predicted_sales_dict[item.strip()] = float(sales.strip())

        if predicted_sales_dict:
            # Finding the highest sold item
            highest_sold_item = max(predicted_sales_dict, key=predicted_sales_dict.get)
            st.write(f"Highest sold item by future prediction: {highest_sold_item}")

        # Draw graph for predicted sales of all items
            fig_predicted_sales = px.bar(x=list(predicted_sales_dict.keys()), y=list(predicted_sales_dict.values()), title='Predicted Sales of All Items')
            st.plotly_chart(fig_predicted_sales)
        else:
            st.write("")

    except Exception as e:
        st.error("An error occurred while generating future sales prediction.")
        st.error(e)



    # Loyalty Program Suggestions (Using GPT API)
    st.subheader('Loyalty Program Suggestions')
    st.write("Ask GPT for suggestions on loyalty programs to increase customer retention.")
    loyalty_program_prompt = f"""
    Based on the provided sales data, {highest_item_item_mrp} and {highest_item_medium_outlet} please predict the future sales trend for the upcoming months.
    Provide insights on potential growth areas and any patterns observed in the data. The highest sold item in terms of outlet size is {highest_item_outlet_size}, in medium-sized outlet is {highest_item_medium_outlet}, and in terms of outlet type is {highest_item_outlet_type}.
    tailored to increase customer retention and drive sales growth. The lowest sold item in terms of outlet size is {lowest_item_outlet_size}, in medium-sized outlet is {lowest_item_medium_outlet}, and in terms of outlet type is {lowest_item_outlet_type}. Write only 5 Plans.
    """
    try:
        loyalty_programs = openai.Completion.create(
            engine="gpt-3.5-turbo-instruct",
            prompt=loyalty_program_prompt,
            max_tokens=1000
        )
        st.write(loyalty_programs.choices[0].text.strip())
    except Exception as e:
        st.error("An error occurred while generating loyalty program suggestions.")
        st.error(e)

    # Summary Tables
    st.subheader('Summary Tables')
    # Summary statistics for numerical columns
    st.write("Summary Statistics for Numerical Columns")
    st.write(df.describe())

    # Pivot table for Outlet Type vs Item Type
    st.write("Pivot Table: Outlet Type vs Item Type")
    pivot_table_outlet_item = pd.pivot_table(df, index='Outlet_Type', columns='Item_Type', values='Item_Outlet_Sales', aggfunc='sum', fill_value=0)
    st.write(pivot_table_outlet_item)

    # Line-by-line summary
    st.subheader("Line-by-line Summary")
    st.write("- Dataset: Displayed the dataset.")
    st.write("- Outlet Size vs Outlet Sales: Plotted a bar chart showing the relationship between outlet size and outlet sales. Highlighted the highest and lowest sold items.")
    st.write("- Sales of All Items in Medium-sized Outlet: Plotted a bar chart showing sales of all items in medium-sized outlets. Highlighted the highest and lowest sold items.")
    st.write("- Outlet Type vs Outlet Sales: Plotted a bar chart showing the relationship between outlet type and outlet sales. Highlighted the highest and lowest sold items.")
    st.write("- Item Popularity vs Item Type vs Item MRP: Plotted an area chart showing the relationship between item popularity, item type, and item MRP. Highlighted the highest and lowest priced items.")
    st.write("- Future Sales Prediction: Predicted future sales based on the provided sales data. Highlighted the highest sold item by future prediction.")
    st.write("- Loyalty Program Suggestions: Generated suggestions on loyalty programs to increase customer retention.")
    st.write("- Summary Statistics for Numerical Columns: Displayed summary statistics for numerical columns.")
    st.write("- Pivot Table: Outlet Type vs Item Type: Generated a pivot table showing the relationship between outlet type and item type.")

def main():
    st.title("Inventory Sales Data Analysis")
    st.write("Upload your CSV file here:")
    github="https://github.com/Ushnish2021/HackNova"
    st.markdown(f'<a href="{github}">Data Set in GitHub Repo</a>', unsafe_allow_html=True)
    uploaded_file = st.file_uploader("Choose a file", type=['csv'])

    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)
            visualize_data(df)
        except Exception as e:
            st.error("An error occurred while reading the file.")
            st.error(e)

if __name__ == "__main__":
    main()
