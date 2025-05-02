import streamlit as st
import pandas as pd
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import datetime
import os
import base64

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

    # Generar PDF (estilo estructurado)
    timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    pdf_filename = f"reporte_servicio_{timestamp}.pdf"
    c = canvas.Canvas(pdf_filename, pagesize=letter)
    c.setFont("Helvetica-Bold", 14)
    c.drawString(200, 770, "REPORTE DE SERVICIO")

    c.setFont("Helvetica", 10)

    y = 740
    def draw_field(label, value):
        nonlocal y
        c.drawString(40, y, f"{label}:")
        c.drawString(150, y, str(value))
        y -= 18

    # Sección 1 - Datos generales
    y -= 10
    c.setFont("Helvetica-Bold", 12)
    c.drawString(40, y, "Datos del Cliente")
    y -= 15
    c.setFont("Helvetica", 10)
    draw_field("Cliente", datos["Cliente"])
    draw_field("Dirección", datos["Dirección"])
    draw_field("Contacto", datos["Contacto"])
    draw_field("Técnico Encargado", datos["Técnico"])

    y -= 10
    c.setFont("Helvetica-Bold", 12)
    c.drawString(40, y, "Tiempos del Servicio")
    y -= 15
    c.setFont("Helvetica", 10)
    draw_field("Fecha llamado", datos["Fecha llamado"])
    draw_field("Hora llamado", datos["Hora llamado"])
    draw_field("Fecha servicio", datos["Fecha servicio"])
    draw_field("Hora inicio", datos["Hora inicio"])

    y -= 10
    c.setFont("Helvetica-Bold", 12)
    c.drawString(40, y, "Datos del Equipo")
    y -= 15
    c.setFont("Helvetica", 10)
    draw_field("Modelo", datos["Modelo"])
    draw_field("Versión", datos["Versión"])
    draw_field("Serie", datos["Serie"])
    draw_field("Horas uso", datos["Horas uso"])

    # Sección grande (multilínea)
    y -= 10
    c.setFont("Helvetica-Bold", 12)
    c.drawString(40, y, "Detalle del Problema")
    y -= 15
    c.setFont("Helvetica", 10)
    text_fields = ["Problema", "Falla", "Acciones", "Comentarios"]
    for field in text_fields:
        c.drawString(40, y, f"{field}:")
        y -= 15
        text = datos[field]
        for line in text.splitlines():
            c.drawString(60, y, line.strip())
            y -= 13
        y -= 10

    c.showPage()
    c.save()
