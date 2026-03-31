from io import BytesIO

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab import platypus as p

def generate_order_pdf(order):
    pdfmetrics.registerFont(TTFont("DejavuSans", "static/fonts/DejaVu-Fonts/DejaVuSans.ttf"))
    buffer = BytesIO()

    mailFontName = "DejavuSans"

    doc = p.SimpleDocTemplate(
        buffer,
        pagesize=A4,
        leftMargin=40,
        rightMargin=40,
        topMargin=40,
        bottomMargin=40,
    )

    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        "TitleCenter",
        parent=styles["Title"],
        alignment=TA_CENTER,
        fontName=mailFontName,
    )

    event_style = ParagraphStyle(
        "EventTitle",
        parent=styles["Heading1"],
        alignment=TA_CENTER,
        textColor=colors.black,
        fontName=mailFontName,
    )

    center_style = ParagraphStyle(
        "CenterText",
        parent=styles["Normal"],
        alignment=TA_CENTER,
        fontName=mailFontName,
    )

    small_style = ParagraphStyle(
        "SmallText",
        parent=styles["Normal"],
        alignment=TA_CENTER,
        fontSize=9,
        textColor=colors.grey,
        fontName=mailFontName,
    )

    elements = []

    tickets = list(order.tickets.select_related("ticket_type__event"))

    for i, t in enumerate(tickets, start=1):
        event = t.ticket_type.event

        ticket_content = []

        # HEADER
        ticket_content.append(p.Paragraph("QRticket", title_style))
        ticket_content.append(p.Spacer(1, 10))

        # EVENT
        ticket_content.append(p.Paragraph(event.name, event_style))
        ticket_content.append(p.Spacer(1, 10))

        ticket_content.append(
            p.Paragraph(
                f"{event.date.strftime('%d %b %Y')} | {event.start_time.strftime('%H:%M')} - {event.end_time.strftime('%H:%M')}",
                center_style,
            )
        )

        ticket_content.append(p.Spacer(1, 5))

        ticket_content.append(
            p.Paragraph(event.venue.name, center_style)
        )

        ticket_content.append(p.Spacer(1, 25))

        # TICKET INFO
        ticket_content.append(
            p.Paragraph(f"<b>{t.ticket_type.name}</b>", center_style)
        )
        ticket_content.append(p.Spacer(1, 5))

        ticket_content.append(
            p.Paragraph(order.buyer_name, center_style)
        )

        ticket_content.append(p.Spacer(1, 25))

        # QR
        qr_path = t.qr_code.path
        qr_img = p.Image(qr_path, width=200, height=200)
        qr_img.hAlign = "CENTER"
        ticket_content.append(qr_img)

        ticket_content.append(p.Spacer(1, 15))

        # FOOTER
        ticket_content.append(
            p.Paragraph(f"Order #{order.id}", small_style)
        )

        ticket_content.append(p.Spacer(1, 5))

        ticket_content.append(
            p.Paragraph("Present this QR code at entry", small_style)
        )

        # 🔥 WRAP INTO TABLE (THIS IS THE KEY)
        table = p.Table([[ticket_content]], colWidths=[doc.width])

        table.setStyle(p.TableStyle([
            ("BOX", (0, 0), (-1, -1), 2, colors.black),
            ("INNERPADDING", (0, 0), (-1, -1), 20),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),  # 🔥 key fix
        ]))

        table.hAlign = "CENTER"

        elements.append(table)

        # PAGE BREAK
        if i < len(tickets):
            elements.append(p.PageBreak())

    doc.build(elements)

    buffer.seek(0)
    return buffer