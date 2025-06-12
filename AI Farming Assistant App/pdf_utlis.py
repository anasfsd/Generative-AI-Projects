from fpdf import FPDF
import unicodedata

def clean_text_for_pdf(text):
    """Clean text to be PDF-safe by removing or replacing problematic characters"""
    # Normalize Unicode characters
    text = unicodedata.normalize('NFKD', text)
    # Replace common problematic characters
    replacements = {
        'μ': 'micro',
        '°': ' degrees',
        '℃': 'C',
        '±': '+/-',
        '×': 'x',
        '÷': '/',
        '≤': '<=',
        '≥': '>=',
        '≠': '!=',
        '∞': 'infinity',
        '→': '->',
        '←': '<-',
        '↑': 'up',
        '↓': 'down',
        '↔': '<->',
        '≈': '~=',
        '∑': 'sum',
        '∏': 'product',
        '√': 'sqrt',
        '∫': 'integral',
        '∆': 'delta',
        '∇': 'nabla',
        '∂': 'partial',
        '∝': 'proportional to',
        '∞': 'infinity',
        '∅': 'empty set',
        '∈': 'in',
        '∉': 'not in',
        '⊂': 'subset',
        '⊃': 'superset',
        '∪': 'union',
        '∩': 'intersection',
        '∀': 'for all',
        '∃': 'exists',
        '∄': 'does not exist',
        '∴': 'therefore',
        '∵': 'because'
    }
    for char, replacement in replacements.items():
        text = text.replace(char, replacement)
    return text

def generate_pdf(chat_history, title="AI Climate & Farming Advice"):
    pdf = FPDF()
    pdf.add_page()

    # Use built-in font
    pdf.set_font("helvetica", "B", 16)
    pdf.cell(0, 10, clean_text_for_pdf(title), ln=True, align='C')
    pdf.ln(10)

    # Chat history
    for chat in chat_history:
        # User message
        pdf.set_font("helvetica", "B", 12)
        pdf.cell(0, 10, "User:", ln=True)
        pdf.set_font("helvetica", "", 12)
        # Clean and wrap text
        user_text = clean_text_for_pdf(chat["user"])
        pdf.multi_cell(0, 10, user_text)
        pdf.ln(5)

        # AI response
        pdf.set_font("helvetica", "B", 12)
        pdf.cell(0, 10, "AI Response:", ln=True)
        pdf.set_font("helvetica", "", 12)
        # Clean and wrap text
        ai_text = clean_text_for_pdf(chat["ai"])
        pdf.multi_cell(0, 10, ai_text)
        pdf.ln(10)

    return pdf.output(dest="S").encode("latin-1", "replace") 
