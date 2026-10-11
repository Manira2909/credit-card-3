from fastapi import APIRouter
from fastapi.responses import FileResponse
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
import os
from datetime import datetime

router = APIRouter()

# FAKE DATA FOR TESTING - DB ku badhil
def get_month_transactions(user_id: int, year: int, month: int):
    # Ippo test ku fake data, naalaiku DB connect pannalam
    return [
        {"amount": 1500, "status": "SUCCESS", "date": datetime.now(), "masked_number": "**** **** **** 1234"},
        {"amount": 6000, "status": "SUCCESS", "date": datetime.now(), "masked_number": "**** **** **** 5678"},
        {"amount": 200, "status": "FAILED", "date": datetime.now(), "masked_number": "**** **** **** 1234"},
    ]

@router.get("/statement/{year}/{month}")
def generate_statement(year: int, month: int):
    # Auth illaama test pannrom
    user_id = 1
    user_email = "test@gmail.com"

    transactions = get_month_transactions(user_id, year, month)

    os.makedirs("temp", exist_ok=True)
    filename = f"temp/statement_{user_id}_{month}_{year}.pdf"
    
    c = canvas.Canvas(filename, pagesize=letter)

    c.setFillColor(colors.HexColor("#1e40af"))
    c.setFont("Helvetica-Bold", 18)
    c.drawString(50, 750, "CREDIT CARD MONTHLY STATEMENT")

    c.setFillColor(colors.black)
    c.setFont("Helvetica", 10)
    c.drawString(50, 730, f"User: {user_email}")
    c.drawString(50, 715, f"Period: {month}/{year}")
    c.line(50, 705, 550, 705)

    y = 680
    c.setFont("Helvetica-Bold", 10)
    c.drawString(50, y, "DATE")
    c.drawString(150, y, "AMOUNT")
    c.drawString(250, y, "STATUS")
    c.drawString(350, y, "CARD")
    y -= 20

    total = 0
    c.setFont("Helvetica", 9)
    for t in transactions:
        date_str = t['date'].strftime('%d-%m-%Y')
        c.drawString(50, y, date_str)
        c.drawString(150, y, f"Rs. {t['amount']}")
        c.drawString(250, y, t['status'])
        c.drawString(350, y, t['masked_number'])
        if t['status'] == 'SUCCESS':
            total += float(t['amount'])
        y -= 18

    y -= 20
    c.line(50, y, 550, y)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y-20, f"Total Spending: Rs. {total}")
    c.save()

    return FileResponse(path=filename, media_type='application/pdf', filename=f"Statement_{month}_{year}.pdf")