# pdf_generator.py

import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from datetime import datetime
from PyQt5.QtWidgets import QMessageBox

def generate_ticket_de_caisse(numero_piece, client, moyen_paiement, articles, remise, total_articles, total_tva, total_ttc):
    today = datetime.today().strftime('%Y-%m-%d')
    archive_folder = f"archives/{today}"
    os.makedirs(archive_folder, exist_ok=True)

    file_name = f"{archive_folder}/Ticket_de_Caisse_{numero_piece}.pdf"
    
    # Vérifier si le fichier existe déjà
    if os.path.exists(file_name):
        return None, f"Le ticket de caisse n° {numero_piece} existe déjà."

    doc = SimpleDocTemplate(file_name, pagesize=letter)
    elements = []

    # Header
    header_data = [
        [f"Client: {client}"],
        [f"Moyen de paiement: {moyen_paiement}"],
        [f"Numéro de pièce comptable: 403-{numero_piece}"],
        [f"Date: {datetime.now().strftime('%d-%m-%Y %H:%M:%S')}"]
    ]
    header_table = Table(header_data, colWidths=[6 * inch])
    elements.append(header_table)

    elements.append(Table([[" "]]))  # Empty line

    # Articles Table
    article_data = [["Référence", "Désignation", "Quantité", "Prix HT", "TVA", "Prix TTC/unité", "Total"]]
    for article in articles:
        article_data.append([
            article['reference'], 
            article['designation'], 
            article['quantite'], 
            article['prix_ht'], 
            article['tva'], 
            article['prix_ttc_unite'], 
            article['total']
        ])
    
    article_table = Table(article_data, colWidths=[1 * inch, 1.5 * inch, 0.8 * inch, 1 * inch, 0.8 * inch, 1.2 * inch, 1 * inch])
    article_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    elements.append(article_table)

    elements.append(Table([[" "]]))  # Empty line

    # Summary Table
    summary_data = [
        [f"Remise: {remise}%", "", ""],
        [f"Nombre d'articles: {total_articles}", f"Total TVA: {total_tva}", f"Total TTC: {total_ttc}"]
    ]
    summary_table = Table(summary_data, colWidths=[2 * inch, 2 * inch, 2 * inch])
    elements.append(summary_table)

    doc.build(elements)

    return file_name, None

def show_pdf(file_name):
    import subprocess
    import sys
    if sys.platform == "win32":
        os.startfile(file_name)
    elif sys.platform == "darwin":
        subprocess.Popen(["open", file_name])
    else:
        subprocess.Popen(["xdg-open", file_name])
