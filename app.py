import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
from dotenv import load_dotenv
from google import genai

# Load env variables
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    st.error("GEMINI_API_KEY not found. Please add it to your .env file.")
    st.stop()

client = genai.Client(api_key=API_KEY)

# Helper function for Gemini query
def generate_response(prompt):
    response = client.models.generate_content(
        model="gemini-2.5-flash", contents=prompt
    )
    return response.text.strip()

# Streamlit UI
st.title("📊 Excel Data Analytics & Gemini AI Assistant")

uploaded_file = st.sidebar.file_uploader("Upload your Excel file", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)
    st.success(f"Loaded `{uploaded_file.name}` successfully!")

    # Show basic info
    st.write(f"**Dataset shape:** {df.shape[0]} rows × {df.shape[1]} columns")
    st.write(f"**Columns:** {', '.join(df.columns)}")

    # Show summary stats
    st.subheader("Summary Statistics")
    st.dataframe(df.describe(include='all').transpose())

    # Charts section
    st.subheader("Data Visualizations")

    numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
    if numeric_cols:
        col_to_plot = st.selectbox("Select numeric column to visualize", numeric_cols)
        fig, ax = plt.subplots()
        sns.histplot(df[col_to_plot].dropna(), kde=True, ax=ax)
        ax.set_title(f"Distribution of {col_to_plot}")
        st.pyplot(fig)
    else:
        st.write("No numeric columns available for plotting.")

    # Natural language assistant
    st.subheader("Ask the AI Assistant about your data")

    question = st.text_input("Enter your question here")

    if st.button("Get Answer") and question.strip() != "":
        # Prepare context & prompt
        context = f"Dataset columns: {', '.join(df.columns)}.\nSample data:\n{df.head(5).to_string(index=False)}"
        prompt = f"Context:\n{context}\n\nQuestion: {question}\nAnswer:"
        with st.spinner("Getting answer from Gemini AI..."):
            answer = generate_response(prompt)
        st.markdown(f"**Answer:** {answer}")

else:
    st.info("Please upload an Excel file to get started.")
