import streamlit as st
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

st.title("🏥 Patient Visit History Viewer")

def get_Patients(PatientID):
    conn = sqlite3.connect("hospital.db")
    
    query = """
    SELECT *
    FROM Patients
    WHERE PatientID = ?
    ORDER BY VisitDate ASC
    """
    
    df = pd.read_sql_query(query, conn, params=(PatientID,))
    conn.close()
    return df
PatientID = st.text_input("Enter PatientID", "")

if PatientID:
    df = get_Patients(PatientID)

    if df.empty:
        st.error("❌ No records found for this Patient ID")
    else:
        st.success("✔ Patient data retrieved")

        df["VisitDate"] = pd.to_datetime(df["VisitDate"])

        st.write("🧾 Patient Visit Records")
        st.dataframe(df)
    
    if "SugarLevel" in df.columns:
        st.write("🍬 Sugar Level Trend")

        fig2, ax2 = plt.subplots()
        ax2.plot(df["VisitDate"], df["SugarLevel"], label="Sugar Level", linewidth=2)

        # Add normal sugar line (Fasting normal = 100 mg/dL)
        ax2.axhline(100, color='red', linestyle='--', linewidth=1.5, label="Normal Sugar (100)")

        ax2.set_xlabel("Visit Date")
        ax2.set_ylabel("Sugar (mg/dL)")
        ax2.set_title("Sugar Level Over Time")

        ax2.legend()
        plt.xticks(rotation=45)
        st.pyplot(fig2)

    
    if "Cholesterol" in df.columns:
        st.write("🩸 Cholesterol Trend")

        fig3, ax3 = plt.subplots()
        ax3.plot(df["VisitDate"], df["Cholesterol"], label="Cholesterol", linewidth=2)

        # Add normal cholesterol line (Normal < 200 mg/dL)
        ax3.axhline(200, color='red', linestyle='--', linewidth=1.5, label="Normal Cholesterol (200)")

        ax3.set_xlabel("Visit Date")
        ax3.set_ylabel("Cholesterol (mg/dL)")
        ax3.set_title("Cholesterol Over Time")

        ax3.legend()
        plt.xticks(rotation=45)
        st.pyplot(fig3)

    
    if "BP" in df.columns:
        st.write("❤️ Blood Pressure Trend")

        fig, ax = plt.subplots()
        ax.plot(df["VisitDate"], df["BP"], label="Blood Pressure", linewidth=2)

        # Add normal BP lines (120/80)
        ax.axhline(120, color='green', linestyle='--', linewidth=1.5, label="Normal Systolic (120)")
        ax.axhline(80, color='orange', linestyle='--', linewidth=1.5, label="Normal Diastolic (80)")

        ax.set_xlabel("Visit Date")
        ax.set_ylabel("BP (mmHg)")
        ax.set_title("Blood Pressure Over Time")

        ax.legend()
        plt.xticks(rotation=45)

        st.pyplot(fig)

