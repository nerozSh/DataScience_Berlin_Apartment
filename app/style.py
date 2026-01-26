css = """
<style>
    /* Hauptbackground */
    .stApp {
        background-color: #FFE8CC;
        font-family: "Segoe UI", sans-serif;
        display: flex;
        flex-direction: column;
        min-height: 100vh; /* Seite nimmt volle Höhe ein */
    }

    /* Content Bereich */
    .main > div:first-child {
        flex: 1; /* Content dehnt sich aus, Footer unten */
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #FFD8A8;
    }

    /* Buttons */
    div.stButton > button {
        background: #FFA500;
        color: white;
        border: none;
        padding: 0.6rem 1.2rem;
        font-size: 1rem;
        border-radius: 10px;
        cursor: pointer;
        transition: background-color 0.3s ease;
    }
    div.stButton > button:hover {
        background: #FF8C00;
    }


</style>

"""
