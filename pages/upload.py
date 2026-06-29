import streamlit as st
from utils.state import navigate_to

def render_upload_screen():
    """Renders the image upload dashboard (Screen 2)."""

    with st.container():
        st.markdown("""
        <h2 style="font-size:1.65rem;font-weight:800;text-align:center;margin-bottom:0.4rem;
                   font-family:'Inter',sans-serif;color:#0A1628;letter-spacing:-0.03em;">
            Upload Skin Photo
        </h2>
        <p style="color:#8A9BB5;text-align:center;margin-bottom:1.75rem;font-size:0.9rem;
                  font-family:'Inter',sans-serif;line-height:1.5;">
            Provide a high-resolution, well-lit photo of the target skin area for accurate AI analysis.
        </p>
        """, unsafe_allow_html=True)

        # Tips row
        st.markdown("""
        <div style="display:flex;gap:0.75rem;justify-content:center;flex-wrap:wrap;margin-bottom:1.75rem;">
            <span class="stat-pill">Good Lighting</span>
            <span class="stat-pill">High Resolution</span>
            <span class="stat-pill">Face Centred</span>
            <span class="stat-pill">No Filters</span>
        </div>
        """, unsafe_allow_html=True)

        # Initialize uploader key to force reset when cleared
        if "uploader_key" not in st.session_state:
            st.session_state.uploader_key = 100

        # File uploader widget
        uploaded_file = st.file_uploader(
            "Click to browse, or drag and drop an image here",
            type=["jpg", "jpeg", "png"],
            key=f"file_uploader_{st.session_state.uploader_key}",
        )

        # Handle uploaded file
        if uploaded_file is not None:
            st.session_state.uploaded_image = uploaded_file.read()
            st.session_state.pop("analysis_result", None)
            st.session_state.uploaded_image_name = uploaded_file.name
            size_bytes = len(st.session_state.uploaded_image)
            if size_bytes > 1024 * 1024:
                st.session_state.uploaded_image_size = f"{size_bytes / (1024*1024):.2f} MB"
            else:
                st.session_state.uploaded_image_size = f"{size_bytes / 1024:.1f} KB"

        # Show preview if image is loaded
        if st.session_state.uploaded_image is not None:
            st.write("")

            col_preview, col_meta = st.columns([1, 2])
            with col_preview:
                import base64
                img_b64 = base64.b64encode(st.session_state.uploaded_image).decode()
                st.markdown(
                    f'<img src="data:image/jpeg;base64,{img_b64}" style="width:100%;aspect-ratio:1;object-fit:cover;border-radius:20px;border:2px solid rgba(77,159,255,0.2);box-shadow:0 8px 24px rgba(10,22,40,0.12);" />',
                    unsafe_allow_html=True
                )

            with col_meta:
                st.markdown(f"""
                <div style="padding:0.5rem 0;">
                    <div style="display:flex;align-items:center;gap:0.5rem;margin-bottom:0.75rem;">
                        <span style="width:10px;height:10px;border-radius:50%;background:#22C55E;flex-shrink:0;"></span>
                        <span style="font-weight:700;color:#0A1628;font-family:'Inter',sans-serif;font-size:0.95rem;
                                     word-break:break-all;">
                            {st.session_state.uploaded_image_name}
                        </span>
                    </div>
                    <div style="display:flex;gap:0.75rem;flex-wrap:wrap;margin-bottom:1.25rem;">
                        <span class="stat-pill">{st.session_state.uploaded_image_size}</span>
                        <span class="stat-pill">Ready</span>
                    </div>
                    <p style="color:#8A9BB5;font-size:0.82rem;font-family:'Inter',sans-serif;line-height:1.5;margin-bottom:0;">
                        Image loaded successfully. You can replace or remove it before continuing.
                    </p>
                </div>
                """, unsafe_allow_html=True)

                col_act_1, col_act_2 = st.columns(2)
                with col_act_1:
                    if st.button("Replace Image", type="secondary", key="replace_img_btn"):
                        st.session_state.uploaded_image = None
                        st.session_state.pop("analysis_result", None)
                        st.session_state.uploaded_image_name = None
                        st.session_state.uploaded_image_size = None
                        st.session_state.uploader_key += 1
                        st.rerun()
                with col_act_2:
                    if st.button("Remove Image", type="secondary", key="remove_img_btn"):
                        st.session_state.uploaded_image = None
                        st.session_state.pop("analysis_result", None)
                        st.session_state.uploaded_image_name = None
                        st.session_state.uploaded_image_size = None
                        st.session_state.uploader_key += 1
                        st.rerun()

            st.markdown("<hr class='dl-divider'>", unsafe_allow_html=True)

            col_cont_1, col_cont_2, col_cont_3 = st.columns([1, 1, 1])
            with col_cont_2:
                if st.button("Continue to Image Check", type="primary", key="continue_upload_btn"):
                    navigate_to("verification")
                    st.rerun()
        else:
            st.write("")
            col_back_1, col_back_2, col_back_3 = st.columns([1.2, 1, 1.2])
            with col_back_2:
                if st.button("Back", type="secondary", key="back_to_welcome"):
                    navigate_to("welcome")
                    st.rerun()
