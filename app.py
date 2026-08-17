import streamlit as st
from fpdf import FPDF

st.set_page_config(page_title="Generator Ofert PDF", page_icon="📄")

st.title("📄 Generator Ofert PDF")
st.write("Wypełnij poniższe pola, aby wygenerować i pobrać ofertę.")

# Formularz danych
nazwa_klienta = st.text_input("Nazwa klienta / firmy")
nazwa_uslugi = st.text_input("Usługa / Produkt")
cena = st.number_input("Cena", min_value=0.0, value=150.0, step=10.0)
opis = st.text_area("Szczegóły oferty / Opis")

if st.button("Generuj dokument PDF"):
    if not nazwa_klienta or not nazwa_uslugi:
        st.warning("Uzupełnij nazwę klienta i nazwę usługi.")
    else:
        # Tworzenie PDF
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Helvetica", style="B", size=16)
        pdf.cell(0, 10, text="OFERTA HANDLOWA", new_x="LMARGIN", new_y="NEXT", align="C")
        pdf.ln(10)
        
        pdf.set_font("Helvetica", size=12)
        pdf.cell(0, 8, text=f"Dla: {nazwa_klienta}", new_x="LMARGIN", new_y="NEXT")
        pdf.cell(0, 8, text=f"Usluga: {nazwa_uslugi}", new_x="LMARGIN", new_y="NEXT")
        pdf.cell(0, 8, text=f"Cena: {cena:.2f}", new_x="LMARGIN", new_y="NEXT")
        pdf.ln(5)
        
        pdf.multi_cell(0, 8, text=f"Opis:\n{opis}")
        
        # Pobieranie bajtów pliku PDF
        pdf_bytes = bytes(pdf.output())
        
        st.success("Oferta gotowa do pobrania!")
        st.download_button(
            label="📥 Pobierz plik PDF",
            data=pdf_bytes,
            file_name=f"Oferta_{nazwa_klienta}.pdf",
            mime="application/pdf"
        )
