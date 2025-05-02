import streamlit as st
import pandas as pd
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import datetime
import os

st.set_page_config(page_title="Reporte de Servicio", layout="centered")
st.title("📋 Reporte de Servicio Técnico")

with st.form("formulario_servicio"):
    cliente = st.text_input("Cliente")
    direccion = st.text_input("Dirección")
    contacto = st.text_input("Contacto")
    tecnico = st.text_input("Técnico Encargado")

    col1, col2 = st.columns(2)
    with col1:
        fecha_llamado = st.date_input("Fecha Llamado")
        fecha_servicio = st.date_input("Fecha Servicio")
    with col2:
        hora_llamado = st.text_input("Hora Llamado")
        hora_inicio = st.text_input("Hora Inicio")

    modelo = st.text_input("Modelo")
    version = st.text_input("Versión Software")
    serie = st.text_input("N° de Serie")
    horas = st.text_input("Horas de uso")

    problema = st.text_area("Problema reportado por el cliente")
    falla = st.text_area("Descripción de la falla")
    acciones = st.text_area("Acciones tomadas")
    comentarios = st.text_area("Comentarios adicionales")

    submitted = st.form_submit_button("Guardar reporte")

if submitted:
    datos = {
        "Cliente": cliente,
        "Dirección": direccion,
        "Contacto": contacto,
        "Técnico": tecnico,
        "Fecha llamado": fecha_llamado,
        "Hora llamado": hora_llamado,
        "Fecha servicio": fecha_servicio,
        "Hora inicio": hora_inicio,
        "Modelo": modelo,
        "Versión": version,
        "Serie": serie,
        "Horas uso": horas,
        "Problema": problema,
        "Falla": falla,
        "Acciones": acciones,
        "Comentarios": comentarios
    }

    # Guardar en historial CSV
    df = pd.DataFrame([datos])
    csv_path = "historial_reportes.csv"
    df.to_csv(csv_path, mode='a', header=not os.path.exists(csv_path), index=False)

    # Exportar a PDF
    timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    pdf_filename = f"reporte_servicio_{timestamp}.pdf"
    c = canvas.Canvas(pdf_filename, pagesize=letter)
    c.setFont("Helvetica", 10)

    y = 750
    for campo, valor in datos.items():
        c.drawString(40, y, f"{campo}: {valor}")
        y -= 20
        if y < 40:
            c.showPage()
            c.setFont("Helvetica", 10)
            y = 750

    c.save()

    # Mostrar resultados
    st.success("✅ Reporte guardado correctamente.")
    st.info(f"📄 PDF generado: `{pdf_filename}`")
