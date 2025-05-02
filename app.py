import streamlit as st
import pandas as pd
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import datetime
import os
import base64

st.set_page_config(page_title="Reporte de Servicio", layout="centered")

# --- Control de acceso ---
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

st.title("📋 Reporte de Servicio Técnico")

# --- Formulario ---
with st.form("formulario_servicio"):
    cliente = st.text_input("Cliente")
    direccion = st.text_input("Dirección")
    contacto = st.text_input("Contacto")
    tecnico = st.text_input("Técnico Encargado")

    col1, col2 = st.columns(2)
    with col1:
        fecha_llamado = st.date_input("Fecha Llamado", value=datetime.date.today())
        fecha_servicio = st.date_input("Fecha Servicio", value=datetime.date.today())
    with col2:
        hl1, hl2 = st.columns([1, 1])
        with hl1:
            hora_llamado_hora = st.selectbox("Hora", list(range(0, 24)), index=9, key="hl_hora")
        with hl2:
            hora_llamado_minuto = st.selectbox("Min", list(range(0, 60, 5)), index=0, key="hl_min")

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

    df = pd.DataFrame([datos])
    csv_path = "historial_reportes.csv"
    df.to_csv(csv_path, mode='a', header=not os.path.exists(csv_path), index=False)

    timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    pdf_filename = f"reporte_servicio_{timestamp}.pdf"
    c = canvas.Canvas(pdf_filename, pagesize=letter)
    c.setStrokeGray(0.7)
    c.setLineWidth(1)
    c.rect(25, 25, 560, 740, stroke=1, fill=0)  # marco decorativo
    c.setFont("Helvetica-Bold", 14)
    c.drawString(200, 770, "REPORTE DE SERVICIO")
    c.setFont("Helvetica", 10)
    y = 740

    def draw_field(canvas, label, value, y_pos):
        canvas.drawString(40, y_pos, f"{label}:")
        canvas.line(140, y_pos - 2, 580, y_pos - 2)
        canvas.drawString(150, y_pos, str(value))
        return y_pos - 20

    def draw_section_title(canvas, title, y_pos):
        canvas.setFillGray(0.9)
        canvas.rect(30, y_pos - 2, 550, 18, fill=1, stroke=0)
        canvas.setFillColorRGB(0, 0, 0)
        canvas.setFont("Helvetica-Bold", 12)
        canvas.drawString(40, y_pos, title)
        return y_pos - 20

    y = draw_section_title(c, "Datos del Cliente", y)
    c.setFont("Helvetica", 10)
    for campo in ["Cliente", "Dirección", "Contacto", "Técnico"]:
        c.setStrokeGray(0.85)
        c.setLineWidth(0.3)
        y = draw_field(c, campo, datos[campo], y)

    y = draw_section_title(c, "Tiempos del Servicio", y)
    c.setFont("Helvetica", 10)
    for campo in ["Fecha llamado", "Hora llamado", "Fecha servicio", "Hora inicio"]:
        c.setStrokeGray(0.85)
        c.setLineWidth(0.3)
        y = draw_field(c, campo, datos[campo], y)

    y = draw_section_title(c, "Datos del Equipo", y)
    c.setFont("Helvetica", 10)
    for campo in ["Modelo", "Versión", "Serie", "Horas uso"]:
        c.setStrokeGray(0.85)
        c.setLineWidth(0.3)
        y = draw_field(c, campo, datos[campo], y)

    y = draw_section_title(c, "Detalle del Problema", y)
    c.setFont("Helvetica", 10)
    for campo in ["Problema", "Falla", "Acciones", "Comentarios"]:
        c.setFont("Helvetica-Bold", 10)
        c.setFillGray(0.9)
        c.rect(30, y - 3, 550, 16, fill=1, stroke=0)
        c.setFillColorRGB(0, 0, 0)
        c.drawString(40, y, f"{campo}:")
        y -= 20

        text_lines = datos[campo].splitlines()
        c.setFont("Helvetica", 10)
        for line in text_lines:
            c.drawString(60, y, line.strip())
            y -= 13
        y -= 10

        # Firmas
    y = 60
    c.setFont("Helvetica", 10)
    c.drawString(50, y, "Realizado por:")
    c.line(130, y, 250, y)
    c.drawString(400, y, "Recepcionado por:")
    c.line(500, y, 580, y)

    c.showPage()
    c.save()

    with open(pdf_filename, "rb") as f:
        pdf_bytes = f.read()
        b64 = base64.b64encode(pdf_bytes).decode()
        href = f'<a href="data:application/pdf;base64,{b64}" download="{pdf_filename}">📥 Descargar PDF</a>'
        st.markdown(href, unsafe_allow_html=True)

    st.success("✅ Reporte guardado correctamente.")

# --- Historial de reportes ---
with st.expander("📂 Ver historial de reportes"):
    if os.path.exists("historial_reportes.csv"):
        historial = pd.read_csv("historial_reportes.csv")
        st.dataframe(historial)

        st.markdown("---")
        fila_borrar = st.number_input("Selecciona el número de fila para eliminar (0 a N-1):", min_value=0, max_value=len(historial)-1, step=1, key="fila_borrar")
        if st.button("🗑️ Eliminar fila seleccionada"):
            historial.drop(index=fila_borrar, inplace=True)
            historial.to_csv("historial_reportes.csv", index=False)
            st.success("✅ Fila eliminada correctamente. Recarga la página para ver los cambios.")

        confirmar_borrado = st.checkbox("⚠️ Confirmo que deseo eliminar todo el historial")
        if st.button("🗑️ Borrar todos los registros del historial"):
            if confirmar_borrado:
                os.remove("historial_reportes.csv")
                st.warning("✅ Historial eliminado. Actualiza la página para ver los cambios.")
            else:
                st.error("Debes confirmar que deseas eliminar el historial.")

        st.markdown("---")
        selected_index = st.number_input("Selecciona el número de fila para reimprimir (0 a N-1):", min_value=0, max_value=len(historial)-1, step=1, key="reimpresion")
        st.info(f"🧾 Cliente: {historial.iloc[selected_index]['Cliente']} | Fecha Servicio: {historial.iloc[selected_index]['Fecha servicio']}")-1, step=1)
        if st.button("🖨️ Generar PDF del reporte seleccionado"):
            datos = historial.iloc[selected_index].to_dict()

            timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
            pdf_filename = f"reporte_servicio_{timestamp}_reimpreso.pdf"
            c = canvas.Canvas(pdf_filename, pagesize=letter)
            c.setStrokeGray(0.7)
            c.setLineWidth(1)
            c.rect(25, 25, 560, 740, stroke=1, fill=0)  # marco decorativo
            c.setFont("Helvetica-Bold", 14)
            c.drawString(200, 770, "REPORTE DE SERVICIO")
            c.setFont("Helvetica", 10)
            y = 740

            def draw_field(canvas, label, value, y_pos):
                canvas.drawString(40, y_pos, f"{label}:")
                canvas.line(140, y_pos - 2, 580, y_pos - 2)
                canvas.drawString(150, y_pos, str(value))
                return y_pos - 20

            def draw_section_title(canvas, title, y_pos):
                canvas.setFillGray(0.9)
                canvas.rect(30, y_pos - 2, 550, 18, fill=1, stroke=0)
                canvas.setFillColorRGB(0, 0, 0)
                canvas.setFont("Helvetica-Bold", 12)
                canvas.drawString(40, y_pos, title)
                return y_pos - 20

            y = draw_section_title(c, "Datos del Cliente", y)
            c.setFont("Helvetica", 10)
            for campo in ["Cliente", "Dirección", "Contacto", "Técnico"]:
                c.setStrokeGray(0.85)
                c.setLineWidth(0.3)
                y = draw_field(c, campo, datos[campo], y)

            y = draw_section_title(c, "Tiempos del Servicio", y)
            for campo in ["Fecha llamado", "Hora llamado", "Fecha servicio", "Hora inicio"]:
                y = draw_field(c, campo, datos[campo], y)

            y = draw_section_title(c, "Datos del Equipo", y)
            for campo in ["Modelo", "Versión", "Serie", "Horas uso"]:
                y = draw_field(c, campo, datos[campo], y)

            y = draw_section_title(c, "Detalle del Problema", y)
            for campo in ["Problema", "Falla", "Acciones", "Comentarios"]:
                c.setFont("Helvetica-Bold", 10)
                c.setFillGray(0.9)
                c.rect(30, y - 3, 550, 16, fill=1, stroke=0)
                c.setFillColorRGB(0, 0, 0)
                c.drawString(40, y, f"{campo}:")
                y -= 20

                text_lines = str(datos[campo]).splitlines()
                c.setFont("Helvetica", 10)
                for line in text_lines:
                    c.drawString(60, y, line.strip())
                    y -= 13
                y -= 10

            y = 60
            c.setFont("Helvetica", 10)
            c.drawString(50, y, "Realizado por:")
            c.line(130, y, 250, y)
            c.drawString(400, y, "Recepcionado por:")
            c.line(500, y, 580, y)

            c.showPage()
            c.save()

            with open(pdf_filename, "rb") as f:
                pdf_bytes = f.read()
                b64 = base64.b64encode(pdf_bytes).decode()
                href = f'<a href="data:application/pdf;base64,{b64}" download="{pdf_filename}">📥 Descargar PDF del historial</a>'
                st.markdown(href, unsafe_allow_html=True)
    else:
        st.info("Aún no hay reportes guardados.")
