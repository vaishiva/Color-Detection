import streamlit as st
import cv2
import pandas as pd
import numpy as np
from PIL import Image

# Load color database
@st.cache_data
def load_colors():
    return pd.read_csv('colors.csv')

def closest_color(rgb, colors_df):
    colors_arr = colors_df[['red','green','blue']].values
    deltas = np.sqrt(np.sum((colors_arr - rgb)**2, axis=1))
    return colors_df.iloc[np.argmin(deltas)]

def main():
    st.title("🎨 Pixel Color Inspector")
    
    uploaded_file = st.file_uploader("Upload Image", type=['jpg','png','jpeg'])
    colors_df = load_colors()
    
    if uploaded_file:
        image = Image.open(uploaded_file)
        img_array = np.array(image)
        
        st.image(image, caption='Uploaded Image', use_column_width=True)
        
        if st.checkbox("Click on image to pick color"):
            click_data = st.empty()
            color_display = st.empty()
            
            with st.spinner("Loading image analyzer..."):
                rgb_img = cv2.cvtColor(img_array, cv2.COLOR_BGR2RGB)
                height, width = rgb_img.shape[:2]
                
                # Create interactive canvas
                x = st.slider("X Coordinate", 0, width-1, width//2)
                y = st.slider("Y Coordinate", 0, height-1, height//2)
                
                # Get pixel color
                b, g, r = rgb_img[y,x]
                closest = closest_color((r,g,b), colors_df)
                
                # Display results
                click_data.markdown(f"""
                **Selected Pixel:** ({x}, {y})  
                **RGB:** ({r}, {g}, {b})  
                **HEX:** #{r:02x}{g:02x}{b:02x}  
                **Closest Color:** {closest['name']} (ΔE: {np.sqrt(np.sum(([r,g,b] - closest[['red','green','blue']])**2)):.1f})
                """)
                
                color_display.markdown(
                    f'<div style="width:100%; height:100px; background-color:rgb({r},{g},{b}); border-radius:10px;"></div>',
                    unsafe_allow_html=True
                )

if __name__ == "__main__":
    main()
