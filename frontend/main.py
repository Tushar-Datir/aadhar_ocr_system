import streamlit as st

from api import (
    scan_aadhaar,
    get_documents,
    delete_document
)


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Aadhaar OCR",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown(
    """
    <style>

    .block-container {
        max-width: 1400px;
        padding-top: 2rem;
    }

    .app-title {
        font-size: 2.2rem;
        font-weight: 700;
        margin-bottom: 0;
    }

    .app-subtitle {
        color: #6b7280;
        font-size: 1rem;
        margin-bottom: 2rem;
    }

    .metric-card {
        padding: 1.2rem;
        border-radius: 12px;
        border: 1px solid #e5e7eb;
        background: white;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
    }

    .metric-title {
        color: #6b7280;
        font-size: 0.9rem;
    }

    .metric-value {
        font-size: 2rem;
        font-weight: 700;
    }

    .section-title {
        font-size: 1.4rem;
        font-weight: 650;
        margin-top: 1rem;
        margin-bottom: 1rem;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.title("📄 Aadhaar OCR")

    st.caption(
        "Document Intelligence System"
    )

    st.divider()

    page = st.radio(
        "Navigation",
        [
            "🏠 Dashboard",
            "📄 Scan Aadhaar",
            "📋 Documents"
        ]
    )

    st.divider()

    st.caption(
        "FastAPI + Tesseract + PostgreSQL"
    )


# =========================================================
# DASHBOARD
# =========================================================

if page == "🏠 Dashboard":

    st.markdown(
        '<div class="app-title">Dashboard</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="app-subtitle">'
        'Overview of your Aadhaar OCR documents'
        '</div>',
        unsafe_allow_html=True
    )

    try:

        result = get_documents()

        documents = result.get(
            "documents",
            []
        )

        total = len(documents)

        valid = sum(
            1
            for document in documents
            if document.get("is_valid")
        )

        invalid = total - valid

        col1, col2, col3 = st.columns(3)

        with col1:

            st.metric(
                "Total Documents",
                total
            )

        with col2:

            st.metric(
                "Valid Documents",
                valid
            )

        with col3:

            st.metric(
                "Invalid Documents",
                invalid
            )

        st.divider()

        st.markdown(
            '<div class="section-title">'
            'Recent Documents'
            '</div>',
            unsafe_allow_html=True
        )

        if documents:

            for document in documents[:5]:

                col1, col2, col3, col4 = st.columns(
                    [2.5, 1.2, 1.5, 1]
                )

                with col1:

                    st.write(
                        f"**{document.get('name') or 'Unknown'}**"
                    )

                with col2:

                    st.write(
                        document.get("gender") or "-"
                    )

                with col3:

                    st.write(
                        document.get("date_of_birth") or "-"
                    )

                with col4:

                    if document.get("is_valid"):

                        st.success(
                            "Valid"
                        )

                    else:

                        st.error(
                            "Invalid"
                        )

        else:

            st.info(
                "No documents have been scanned yet."
            )

    except Exception as e:

        st.error(
            f"Unable to connect to API: {e}"
        )


# =========================================================
# SCAN AADHAAR
# =========================================================

elif page == "📄 Scan Aadhaar":

    st.markdown(
        '<div class="app-title">Scan Aadhaar</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="app-subtitle">'
        'Upload an Aadhaar document for OCR extraction'
        '</div>',
        unsafe_allow_html=True
    )

    col1, col2 = st.columns(2)

    # -----------------------------------------------------
    # Front Image
    # -----------------------------------------------------

    with col1:

        st.subheader("Front Side")

        front_file = st.file_uploader(
            "Upload front image",
            type=[
                "jpg",
                "jpeg",
                "png"
            ],
            key="front_upload"
        )

        if front_file:

            st.image(
                front_file,
                caption="Front Side",
                width=450
            )

    # -----------------------------------------------------
    # Back Image
    # -----------------------------------------------------

    with col2:

        st.subheader("Back Side")

        st.caption(
            "Optional — required for address extraction"
        )

        back_file = st.file_uploader(
            "Upload back image",
            type=[
                "jpg",
                "jpeg",
                "png"
            ],
            key="back_upload"
        )

        if back_file:

            st.image(
                back_file,
                caption="Back Side",
                width=450
            )

    st.divider()

    # -----------------------------------------------------
    # Scan
    # -----------------------------------------------------

    if st.button(
        "🔍 Scan Document",
        type="primary",
        use_container_width=True
    ):

        if front_file is None:

            st.warning(
                "Please upload the front side first."
            )

        else:

            with st.spinner(
                "Processing document with OCR..."
            ):

                try:

                    result = scan_aadhaar(
                        front_file,
                        back_file
                    )

                    st.session_state[
                        "scan_result"
                    ] = result

                    st.success(
                        "Document scanned successfully!"
                    )

                except Exception as e:

                    st.error(
                        f"OCR processing failed: {e}"
                    )

    # -----------------------------------------------------
    # OCR Result
    # -----------------------------------------------------

    if "scan_result" in st.session_state:

        result = st.session_state[
            "scan_result"
        ]

        data = result.get(
            "data",
            {}
        )

        information = data.get(
            "information",
            {}
        )

        validation = data.get(
            "validation",
            {}
        )

        st.divider()

        st.markdown(
            '<div class="section-title">'
            'Extracted Information'
            '</div>',
            unsafe_allow_html=True
        )

        col1, col2 = st.columns(2)

        with col1:

            st.text_input(
                "Name",
                value=information.get(
                    "name"
                ) or "",
                disabled=True
            )

            st.text_input(
                "Gender",
                value=information.get(
                    "gender"
                ) or "",
                disabled=True
            )

            st.text_input(
                "Date of Birth",
                value=information.get(
                    "date_of_birth"
                ) or "",
                disabled=True
            )

        with col2:

            st.text_input(
                "Aadhaar Number",
                value=information.get(
                    "aadhaar_number"
                ) or "",
                disabled=True
            )

            st.text_area(
                "Address",
                value=information.get(
                    "address"
                ) or "Not available",
                disabled=True
            )

        # -------------------------------------------------
        # Validation
        # -------------------------------------------------

        st.markdown(
            '<div class="section-title">'
            'Validation Results'
            '</div>',
            unsafe_allow_html=True
        )

        checks = [
            (
                "Name",
                validation.get("name")
            ),
            (
                "Gender",
                validation.get("gender")
            ),
            (
                "Date of Birth",
                validation.get("date_of_birth")
            ),
            (
                "Aadhaar Number",
                validation.get("aadhaar_number")
            )
        ]

        cols = st.columns(4)

        for col, (label, status) in zip(
            cols,
            checks
        ):

            with col:

                if status:

                    st.success(
                        f"✓ {label}"
                    )

                else:

                    st.error(
                        f"✗ {label}"
                    )

        st.divider()

        if validation.get(
            "is_valid",
            False
        ):

            st.success(
                "✅ Document validation successful"
            )

        else:

            st.error(
                "❌ Document validation failed"
            )


# =========================================================
# DOCUMENTS
# =========================================================

elif page == "📋 Documents":

    st.markdown(
        '<div class="app-title">Documents</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="app-subtitle">'
        'Previously scanned Aadhaar documents'
        '</div>',
        unsafe_allow_html=True
    )

    if st.button("🔄 Refresh"):

        st.rerun()

    try:

        result = get_documents()

        documents = result.get(
            "documents",
            []
        )

        if not documents:

            st.info(
                "No documents found."
            )

        else:

            st.write(
                f"**{len(documents)} document(s) found**"
            )

            st.divider()

            for document in documents:

                document_id = document.get(
                    "id"
                )

                name = (
                    document.get("name")
                    or "Unknown"
                )

                with st.expander(
                    f"📄 #{document_id} — {name}"
                ):

                    col1, col2 = st.columns(2)

                    with col1:

                        st.write(
                            "**Name:**",
                            name
                        )

                        st.write(
                            "**Gender:**",
                            document.get(
                                "gender"
                            ) or "-"
                        )

                        st.write(
                            "**Date of Birth:**",
                            document.get(
                                "date_of_birth"
                            ) or "-"
                        )

                        st.write(
                            "**Aadhaar:**",
                            document.get(
                                "aadhaar_number"
                            ) or "-"
                        )

                    with col2:

                        st.write(
                            "**Address:**",
                            document.get(
                                "address"
                            ) or "Not available"
                        )

                        st.write(
                            "**Created:**",
                            document.get(
                                "created_at"
                            ) or "-"
                        )

                        if document.get(
                            "is_valid"
                        ):

                            st.success(
                                "Document Valid"
                            )

                        else:

                            st.error(
                                "Document Invalid"
                            )

                    st.divider()

                    if st.button(
                        "🗑️ Delete Document",
                        key=f"delete_{document_id}"
                    ):

                        try:

                            delete_document(
                                document_id
                            )

                            st.success(
                                "Document deleted successfully."
                            )

                            st.rerun()

                        except Exception as e:

                            st.error(
                                f"Delete failed: {e}"
                            )

    except Exception as e:

        st.error(
            f"Unable to load documents: {e}"
        )