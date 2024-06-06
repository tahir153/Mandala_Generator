import streamlit as st
import random
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from RandomMandala import random_mandala
from io import BytesIO

# Color scheme dictionary with user-friendly names
color_scheme_dict = {
    "Black and White": 'gray',
    "Viridis (Green-Yellow-Purple)": 'viridis',
    "Plasma (Yellow-Orange-Purple)": 'plasma',
    "Inferno (Yellow-Orange-Red-Black)": 'inferno',
    "Magma (Pink-Red-Black)": 'magma',
    "Cividis (Yellow-Blue)": 'cividis',
    "Earth Tones": 'gist_earth',
    "Rainbow": 'rainbow'
}

# Design type dictionary with user-friendly names
design_type_dict = {
    "Filled": 'fill',
    "Line": 'line',
    "Bezier Curve": 'bezier',
    "Filled Bezier Curve": 'bezier_fill',
    "Random": 'random'
}

# Set up the Streamlit interface
st.title("Advanced Random Mandala Generator")

# User inputs for the parameters
diversity = st.slider("Diversity (Seed Value)", 1, 100, 33)
n_images = st.slider("Number of Images", 1, 50, 16)
figsize_x = st.slider("Figure Size X", 4.0, 10.0, 6.0)
figsize_y = st.slider("Figure Size Y", 4.0, 10.0, 6.0)
color_scheme_name = st.selectbox("Color Scheme", list(color_scheme_dict.keys()))
color_scheme = color_scheme_dict[color_scheme_name]
design_type_name = st.selectbox("Design Type", list(design_type_dict.keys()))
design_type = design_type_dict[design_type_name]
complexity = st.slider("Complexity (Number of Elements)", 2, 20, 6)
rotational_symmetry_order = st.slider("Rotational Symmetry Order", 3, 9, 6)
number_of_elements = st.slider("Number of Elements", 1, 10, 4)
symmetric_seed = st.selectbox("Symmetry", ["Yes", "No"])

# Convert symmetric_seed to boolean
symmetric_seed = True if symmetric_seed == "Yes" else False

# Button to generate the mandalas
if st.button("Generate Mandalas"):
    random.seed(diversity)

    # Generate each mandala with the specified parameters
    mandala_images = []
    for i in range(n_images):
        fig = plt.figure(figsize=(figsize_x, figsize_y), dpi=120)
        rs = list(range(1, random.choice([3, 4, 5, 6]) + 1))
        rs.sort()
        rs.reverse()

        fig = random_mandala(
            connecting_function=design_type,
            color_mapper=getattr(cm, color_scheme),
            symmetric_seed=symmetric_seed,
            radius=rs,
            rotational_symmetry_order=rotational_symmetry_order,
            number_of_elements=number_of_elements,
            figure=fig
        )
        ax = fig.axes[-1]
        ax.set_axis_off()

        # Convert the figure to a BytesIO object
        buf = BytesIO()
        fig.savefig(buf, format="png")
        buf.seek(0)
        mandala_images.append(buf)
        plt.close(fig)

    # Display each mandala and provide a download button
    cols = st.columns(3)
    for idx, img_buf in enumerate(mandala_images):
        col = cols[idx % 3]
        with col:
            st.image(img_buf, caption=f"Mandala {idx + 1}")
            st.download_button(
                label=f"Download Mandala {idx + 1}",
                data=img_buf,
                file_name=f"mandala_{idx + 1}.png",
                mime="image/png"
            )

# streamlit run mandala_generator.py