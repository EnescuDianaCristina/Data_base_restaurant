import json
import csv
import matplotlib.pyplot as plt
from pathlib import Path
from decimal import Decimal
from datetime import datetime

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Image,
    Table,
    TableStyle
)
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch

from app.db import run_select


OUT_DIR = Path("outputs")
OUT_DIR.mkdir(exist_ok=True)

LOGO_PATH = Path("scripts/logo_fiir.jpg")

BASE_NAME_1 = "Top_users_rezervari"
PDF_PATH_1 = OUT_DIR / f"{BASE_NAME_1}.pdf"
CSV_PATH_1 = OUT_DIR / f"{BASE_NAME_1}.csv"
JSON_PATH_1 = OUT_DIR / f"{BASE_NAME_1}.json"
CHART_PATH_1 = OUT_DIR / f"{BASE_NAME_1}_chart.png"

BASE_NAME_2 = "Top_ingrediente"
PDF_PATH_2 = OUT_DIR / f"{BASE_NAME_2}.pdf"
CSV_PATH_2 = OUT_DIR / f"{BASE_NAME_2}.csv"
JSON_PATH_2 = OUT_DIR / f"{BASE_NAME_2}.json"
CHART_PATH_2 = OUT_DIR / f"{BASE_NAME_2}_chart.png"

def normalize(v):
    if isinstance(v, Decimal):
        x = float(v)
        return int(x) if x.is_integer() else x
    return v


def fetch_data_rezervari():
    sql = """
    SELECT u.username, SUM(r.numar_persoane) total_qty
    FROM rezervari r
    JOIN users u ON u.id = r.user_id
    GROUP BY u.id, u.username
    ORDER BY total_qty DESC
    """
    rows = run_select(sql)
    return [{"name": r[0], "total_qty": normalize(r[1])} for r in rows]

def fetch_data_ingrediente():
    sql = """
    SELECT i.tip_ingredient, SUM(s.nr_ingrediente) cantitate_totala
    FROM ingrediente i
    JOIN stoc s ON s.id_ingredient = i.id
    GROUP BY i.tip_ingredient
    ORDER BY cantitate_totala DESC
    """
    rows = run_select(sql)
    return [{"tip_ingredient": r[0], "cantitate_totala": normalize(r[1])} for r in rows]

def export_csv_rezervari(data):
    with open(CSV_PATH_1, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["name", "total_qty"])
        writer.writeheader()
        writer.writerows(data)

def export_csv_ingrediente(data):
    with open(CSV_PATH_2, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["tip_ingredient", "cantitate_totala"])
        writer.writeheader()
        writer.writerows(data)


def export_json_rezervari(data):
    with open(JSON_PATH_1, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def export_json_ingrediente(data):
    with open(JSON_PATH_2, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def generate_chart_rezervari(data):
    names = [d["name"] for d in data]
    values = [d["total_qty"] for d in data]

    plt.figure(figsize=(8, 5))
    plt.plot(names, values)
    plt.title("Top users rezervari")
    plt.xlabel("User")
    plt.ylabel("Numar de persoane rezervate")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(str(CHART_PATH_1))
    plt.close()

def generate_chart_ingrediente(data):
    names = [d["tip_ingredient"] for d in data]
    values = [d["cantitate_totala"] for d in data]

    plt.figure(figsize=(8, 5))
    plt.plot(names, values)
    plt.title("Top ingrediente")
    plt.xlabel("Ingrediente")
    plt.ylabel("Cantitate")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(str(CHART_PATH_2))
    plt.close()



def generate_pdf_rezervari(data):
    doc = SimpleDocTemplate(str(PDF_PATH_1), pagesize=A4)
    elements = []

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        name="TitleStyle",
        parent=styles["Heading1"],
        fontSize=18,
        spaceAfter=20
    )

    normal_style = styles["Normal"]


    if LOGO_PATH.exists():
        logo = Image(str(LOGO_PATH), width=1.5 * inch, height=1.5 * inch)
        elements.append(logo)
        elements.append(Spacer(1, 20))


    elements.append(Paragraph("Raport Business Intelligence", title_style))
    elements.append(Spacer(1, 10))

    elements.append(Paragraph("Top users rezervari", styles["Heading2"]))
    elements.append(Spacer(1, 15))


    intro_text = f"""
    Acest raport prezinta analiza numarului total de rezervarii ale userilor in cadrul aplicatiei Gestionare restaurant.
    Datele sunt agregate din tabela users si sunt ordonate descrescator in functie de cantitatea totala de persoane pentru fiecare user.
    Raport generat la data: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
    """
    elements.append(Paragraph(intro_text, normal_style))
    elements.append(Spacer(1, 20))


    table_data = [["Users", "Cantitate"]]
    for d in data:
        table_data.append([d["name"], d["total_qty"]])

    table = Table(table_data, colWidths=[300, 100])
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#2c3e50")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("ALIGN", (1, 1), (-1, -1), "CENTER"),
        ("BACKGROUND", (0, 1), (-1, -1), colors.HexColor("#ecf0f1")),
    ]))

    elements.append(table)
    elements.append(Spacer(1, 25))


    if CHART_PATH_1.exists():
        chart = Image(str(CHART_PATH_1), width=6 * inch, height=4 * inch)
        elements.append(chart)

    doc.build(elements)

def generate_pdf_ingrediente(data):
    doc = SimpleDocTemplate(str(PDF_PATH_2), pagesize=A4)
    elements = []

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        name="TitleStyle",
        parent=styles["Heading1"],
        fontSize=18,
        spaceAfter=20
    )

    normal_style = styles["Normal"]


    if LOGO_PATH.exists():
        logo = Image(str(LOGO_PATH), width=1.5 * inch, height=1.5 * inch)
        elements.append(logo)
        elements.append(Spacer(1, 20))


    elements.append(Paragraph("Raport Business Intelligence", title_style))
    elements.append(Spacer(1, 10))

    elements.append(Paragraph("Top ingrediente", styles["Heading2"]))
    elements.append(Spacer(1, 15))


    intro_text = f"""
    Acest raport prezinta analiza ingredientelor in cadrul aplicatiei Gestionare restaurant.
    Datele sunt agregate din tabela ingrediente si sunt ordonate descrescator in functie de cantitatea totala a ingredientelor dupa tipul de ingredient.
    Raport generat la data: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
    """
    elements.append(Paragraph(intro_text, normal_style))
    elements.append(Spacer(1, 20))


    table_data = [["Ingredient", "Cantitate"]]
    for d in data:
        table_data.append([d["tip_ingredient"], d["cantitate_totala"]])

    table = Table(table_data, colWidths=[300, 100])
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#2c3e50")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("ALIGN", (1, 1), (-1, -1), "CENTER"),
        ("BACKGROUND", (0, 1), (-1, -1), colors.HexColor("#ecf0f1")),
    ]))

    elements.append(table)
    elements.append(Spacer(1, 25))


    if CHART_PATH_2.exists():
        chart = Image(str(CHART_PATH_2), width=6 * inch, height=4 * inch)
        elements.append(chart)

    doc.build(elements)

def main():
    data = fetch_data_rezervari()

    if not data:
        print("Nu exista date.")
        return

    export_csv_rezervari(data)
    export_json_rezervari(data)
    generate_chart_rezervari(data)
    generate_pdf_rezervari(data)

    print("Raportul rezervariilor este complet generat in folderul:", OUT_DIR.resolve())

    data = fetch_data_ingrediente()

    if not data:
        print("Nu exista date.")
        return

    export_csv_ingrediente(data)
    export_json_ingrediente(data)
    generate_chart_ingrediente(data)
    generate_pdf_ingrediente(data)

    print("Raportul rezervariilor este complet generat in folderul:", OUT_DIR.resolve())

if __name__ == "__main__":
    main()
