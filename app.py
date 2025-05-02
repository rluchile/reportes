import streamlit as st
import pandas as pd
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import datetime
import os
import base64
import re

st.set_page_config(page_title="Reporte de Servicio", layout="centered")

# --- Control de acceso básico ---
USER = "admin"
PASS = "1234"

with st.sidebar:
    st.header("🔐 Iniciar sesión")
    username = st.text_input("Usuario")
    password = st.text_input("Contraseña", type="password")
    login = st.button("Ingresar")

if not (username == USER and password == PASS):
    st.warning("Ingrese usuario y contraseña para continuar.")
    st.stop()

# --- Título ---
st.title("📋 Reporte de Servicio Técnico")

# --- Formulario ---
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
        fecha_llamado = st.date_input("Fecha Llamado", value=datetime.date.today())
        hl1, hl2 = st.columns([1, 1])
        with hl1:
        hora_llamado_hora = st.selectbox("Hora", list(range(0, 24)), index=9, key="hl_hora")
        with hl2:
        hora_llamado_minuto = st.selectbox("Min", list(range(0, 60, 5)), index=0, key="hl_min")

        fecha_servicio = st.date_input("Fecha Servicio", value=datetime.date.today())
        hi1, hi2 = st.columns([1, 1])
        with hi1:
        hora_inicio_hora = st.selectbox("Hora", list(range(0, 24)), index=12, key="hi_hora")
        with hi2:
        hora_inicio_minuto = st.selectbox("Min", list(range(0, 60, 5)), index=0, key="hi_min")


        hora_llamado = f"{hora_llamado_hora:02d}:{hora_llamado_minuto:02d}"
        hora_inicio = f"{hora_inicio_hora:02d}:{hora_inicio_minuto:02d}"

    modelo = st.text_input("Modelo")
    version = st.text_input("Versión Software")
    serie = st.text_input("N° de Serie")
    horas = st.text_input("Horas de uso")

    problema = st.text_area("Problema reportado por el cliente")
    falla = st.text_area("Descripción de la falla")
    acciones = st.text_area("Acciones tomadas")
    comentarios = st.text_area("Comentarios adicionales")

    submitted = st.form_submit_button("Guardar reporte")

# --- Procesar formulario ---
if submitted:
    # Validación de formato de hora
    formato_hora = r'^[0-2][0-9]:[0-5][0-9]$'
    if not re.match(formato_hora, hora_llamado) or not re.match(formato_hora, hora_inicio):
        st.error("❌ Las horas deben estar en formato HH:MM (ej: 09:30).")
        st.stop()

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

    # Guardar en CSV
    df = pd.DataFrame([datos])
    csv_path = "historial_reportes.csv"
    df.to_csv(csv_path, mode='a', header=not os.path.exists(csv_path), index=False)

    # Generar PDF
    timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    pdf_filename = f"reporte_servicio_{timestamp}.pdf"
    c = canvas.Canvas(pdf_filename, pagesize=letter)
    c.setFont("Helvetica-Bold", 14)
    c.drawString(200, 770, "REPORTE DE SERVICIO")
    c.setFont("Helvetica", 10)
    y = 740

    def draw_field(canvas, label, value, y_pos):
        canvas.drawString(40, y_pos, f"{label}:")
        canvas.drawString(150, y_pos, str(value))
        return y_pos - 18

    c.setFont("Helvetica-Bold", 12)
    c.drawString(40, y, "Datos del Cliente")
    y -= 15
    c.setFont("Helvetica", 10)
    y = draw_field(c, "Cliente", datos["Cliente"], y)
    y = draw_field(c, "Dirección", datos["Dirección"], y)
    y = draw_field(c, "Contacto", datos["Contacto"], y)
    y = draw_field(c, "Técnico Encargado", datos["Técnico"], y)

    y -= 10
    c.setFont("Helvetica-Bold", 12)
    c.drawString(40, y, "Tiempos del Servicio")
    y -= 15
    c.setFont("Helvetica", 10)
    y = draw_field(c, "Fecha llamado", datos["Fecha llamado"], y)
    y = draw_field(c, "Hora llamado", datos["Hora llamado"], y)
    y = draw_field(c, "Fecha servicio", datos["Fecha servicio"], y)
    y = draw_field(c, "Hora inicio", datos["Hora inicio"], y)

    y -= 10
    c.setFont("Helvetica-Bold", 12)
    c.drawString(40, y, "Datos del Equipo")
    y -= 15
    c.setFont("Helvetica", 10)
    y = draw_field(c, "Modelo", datos["Modelo"], y)
    y = draw_field(c, "Versión", datos["Versión"], y)
    y = draw_field(c, "Serie", datos["Serie"], y)
    y = draw_field(c, "Horas uso", datos["Horas uso"], y)

    y -= 10
    c.setFont("Helvetica-Bold", 12)
    c.drawString(40, y, "Detalle del Problema")
    y -= 15
    c.setFont("Helvetica", 10)

    for campo in ["Problema", "Falla", "Acciones", "Comentarios"]:
        c.drawString(40, y, f"{campo}:")
        y -= 15
        texto = datos[campo]
        for linea in texto.splitlines():
            c.drawString(60, y, linea.strip())
            y -= 13
        y -= 10

    c.showPage()
    c.save()

    # Botón de descarga
    with open(pdf_filename, "rb") as f:
        pdf_bytes = f.read()
        b64 = base64.b64encode(pdf_bytes).decode()
        href = f'<a href="data:application/pdf;base64,{b64}" download="{pdf_filename}">📥 Descargar PDF</a>'
        st.markdown(href, unsafe_allow_html=True)

    st.success("✅ Reporte guardado correctamente.")

# --- Mostrar historial dentro de la app ---
with st.expander("📂 Ver historial de reportes"):
    if os.path.exists("historial_reportes.csv"):
        historial = pd.read_csv("historial_reportes.csv")
        st.dataframe(historial)
    else:
        st.info("Aún no hay reportes guardados.")
