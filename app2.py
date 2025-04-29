import streamlit as st
import pandas as pd
import re
from bs4 import BeautifulSoup

# App title
st.title("🏘️ Property Data Scraper")

# Upload the source HTML/text file
uploaded_file = st.file_uploader("Upload the HTML source (sourcecode.txt)", type=["txt", "html"])

if uploaded_file is not None:
    # Read and parse file content
    content = uploaded_file.read().decode("utf-8")
    soup = BeautifulSoup(content, "html.parser")

    # Find all relevant panels (adjust class name as per actual HTML)
    fullpanel = soup.find_all("div", class_="addressPanel flex justify-content-between align-items-center")

    data = []
    for panel in fullpanel:
        panel_text = panel.text.strip()

        beds = re.search(r'(\d+(?:\.\d+)?) Beds', panel_text)
        baths = re.search(r'(\d+(?:\.\d+)?) Baths', panel_text)
        sqft = re.search(r'([\d,]+) sqft', panel_text)
        address = panel_text.split(' Beds')[0]

        data.append({
            'Beds': beds.group(1) if beds else 'N/A',
            'Baths': baths.group(1) if baths else 'N/A',
            'Sqft': sqft.group(1) if sqft else 'N/A',
            'Address': address.strip()
        })

    # Create DataFrame
    df = pd.DataFrame(data)

    # Show data
    st.subheader("🏡 Extracted Property Data")
    st.dataframe(df)

    # Download button for CSV
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button("Download CSV", csv, "output.csv", "text/csv")

else:
    st.info("Please upload a source.txt or HTML file containing the page source.")
