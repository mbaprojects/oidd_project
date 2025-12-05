import streamlit as st
import pandas as pd
from pathlib import Path

# Set the title and favicon that appear in the Browser's tab bar.
st.set_page_config(
    page_title='Meta Ray-Ban Brand Presence',
    page_icon=':sunglasses:', # This is an emoji shortcode. Could be a URL too.
)

# -----------------------------------------------------------------------------
# Declare some useful functions.

@st.cache_data
def get_brand_data():
    """Load augmented eyewear domains data from a CSV file.

    This uses caching to avoid having to read the file every time. If we were
    reading from an HTTP endpoint instead of a file, it's a good idea to set
    a maximum age to the cache with the TTL argument: @st.cache_data(ttl='1d')
    """

    # Load the augmented eyewear domains data
    DATA_FILENAME = Path(__file__).parent/'data/eyewear_domains_augmented.csv'
    eyewear_df = pd.read_csv(DATA_FILENAME)

    return eyewear_df

eyewear_df = get_brand_data()

# -----------------------------------------------------------------------------
# Draw the actual page

# Set the title that appears at the top of the page.
'''
# :sunglasses: Meta Ray-Ban Brand Presence Dashboard

Explore where Meta Ray-Ban and competing eyewear brands are appearing across the web.
This dashboard shows citation data, sources, and query information across different
channels and earned media.
'''

# Add some spacing
''
''

# Natural Language Summary
st.info("""
### Dashboard Summary

This analysis examines the digital presence and brand awareness of Meta Ray-Ban smart glasses 
across the web. Our data reveals that **YouTube dominates with 13% of all citations**, making it 
the most significant channel for brand discovery and product information.

**Key Findings:**
- **Ray-Ban.com leads** among official brand pages with 8.3% of citations, indicating strong brand loyalty and direct traffic
- **Meta.com captures 7.7%** of citations, attracting tech-savvy audiences interested in the ecosystem and platform details
- **Earned media channels significantly outpace social media**, suggesting professional reviews and tech publications drive credibility
- **Audience segmentation shows** general consumers focus on YouTube and Best Buy, while tech enthusiasts gravitate toward specialized review sites
- **Top competitors** like Solos Glasses and Vuzix target the same tech-forward audience segments

The dashboard reveals a dual audience: mainstream consumers discovering the product through video content, and 
sophisticated tech buyers reading in-depth comparisons and reviews.
""")

''
''

st.header('Featured YouTube Videos', divider='gray')
st.info('If you cannot see the YouTube videos below, please enable third-party cookies in your browser (Chrome: click the eye or cookie icon in the address bar and allow cookies for this site).')

st.subheader('Top Ray-Ban Smart Glasses Reviews & Demos')

# Create 4 columns for the top 4 videos
col1, col2 = st.columns(2)

youtube_videos = [
    {"title": "Ray-Ban Meta Smart Glasses - Full Review", "video_id": "oorky5Z0wGI"},
    {"title": "Ray-Ban Smart Glasses Hands-On Demo", "video_id": "wv8_Cm5ouZI"},
    {"title": "Ray-Ban Meta Glasses vs Competitors", "video_id": "Onn9NHmft78"},
    {"title": "Ray-Ban Smart Glasses Features & Setup", "video_id": "gZ9IsB72nVk"}
]

for i, video in enumerate(youtube_videos):
    col = col1 if i % 2 == 0 else col2
    with col:
        st.write(f"**{video['title']}**")
        st.video(f"https://www.youtube.com/watch?v={video['video_id']}")

''
''

st.header('Brand Presence Overview', divider='gray')

# Display top domains by citations
top_n = st.slider('Number of top domains to display:', min_value=5, max_value=20, value=10)
top_domains = eyewear_df.nlargest(top_n, '# of times Cited')

# Bar chart of citations by domain
st.subheader('Top Domains by Citation Count')
st.bar_chart(
    top_domains.set_index('Domain')['# of times Cited']
)

''
''

st.header('Media Channel Analysis', divider='gray')

# Group by category
category_stats = eyewear_df.groupby('Category').agg({
    '# of times Cited': 'sum',
    '# of URLs': 'sum',
    '# of Queries': 'sum'
}).reset_index()

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        label='Total Citations (Earned)',
        value=f'{category_stats[category_stats["Category"] == "Earned"]["# of times Cited"].values[0]:.0f}'
    )

with col2:
    st.metric(
        label='Total Citations (Social)',
        value=f'{category_stats[category_stats["Category"] == "Social"]["# of times Cited"].values[0]:.0f}'
    )

with col3:
    st.metric(
        label='Overall Unique Domains',
        value=f'{len(eyewear_df)}'
    )

''
''

# Category comparison
st.subheader('Earned vs Social Media Presence')
category_comparison = category_stats.set_index('Category')
st.bar_chart(category_comparison[['# of times Cited', '# of URLs', '# of Queries']])

''
''

st.header('Brand-Specific Analysis', divider='gray')

# Filter for Meta and Ray-Ban domains
meta_brands = eyewear_df[
    eyewear_df['Domain'].str.contains('meta|ray-ban', case=False, na=False)
]

st.subheader('Meta and Ray-Ban Brand Metrics')
if len(meta_brands) > 0:
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric(
            label='Meta.com Citations',
            value=f'{meta_brands[meta_brands["Domain"] == "meta.com"]["# of times Cited"].values[0] if len(meta_brands[meta_brands["Domain"] == "meta.com"]) > 0 else "N/A"}'
        )
    
    with col2:
        st.metric(
            label='Ray-Ban.com Citations',
            value=f'{meta_brands[meta_brands["Domain"] == "ray-ban.com"]["# of times Cited"].values[0] if len(meta_brands[meta_brands["Domain"] == "ray-ban.com"]) > 0 else "N/A"}'
        )
    
    st.dataframe(meta_brands, use_container_width=True)
else:
    st.info("No Meta or Ray-Ban domains found in the dataset")

''
''

st.header('Audience Insights', divider='gray')

# Analyze audience clusters
st.subheader('General vs Tech-Savvy Audience Distribution')
audience_stats = eyewear_df.groupby('Audience Cluster').agg({
    '# of times Cited': 'sum',
    '# of URLs': 'sum',
    '# of Queries': 'sum'
}).reset_index()

col1, col2 = st.columns(2)

with col1:
    general_citations = audience_stats[audience_stats['Audience Cluster'] == 'general']['# of times Cited'].values
    st.metric(
        label='General Audience Citations',
        value=f'{general_citations[0]:.0f}' if len(general_citations) > 0 else 'N/A'
    )

with col2:
    techie_citations = audience_stats[audience_stats['Audience Cluster'] == 'techie']['# of times Cited'].values
    st.metric(
        label='Tech-Savvy Audience Citations',
        value=f'{techie_citations[0]:.0f}' if len(techie_citations) > 0 else 'N/A'
    )

''

st.subheader('Audience Segment Breakdown')
audience_chart_data = eyewear_df.groupby('Audience Cluster')['# of times Cited'].sum()
st.bar_chart(audience_chart_data)

''
''

st.header('Data Explorer', divider='gray')

# Allow filtering by category
selected_category = st.multiselect(
    'Filter by Media Channel:',
    eyewear_df['Category'].unique(),
    eyewear_df['Category'].unique()
)

filtered_df = eyewear_df[eyewear_df['Category'].isin(selected_category)]

# Sort by selected metric
sort_by = st.selectbox(
    'Sort by:',
    ['# of times Cited', '# of URLs', '# of Queries', 'Rank']
)

sorted_df = filtered_df.sort_values(by=sort_by, ascending=False)

st.dataframe(sorted_df, use_container_width=True)
