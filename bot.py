import json
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, 
    Table, TableStyle, HRFlowable
)
from reportlab.lib.enums import TA_LEFT, TA_CENTER

# ============================================
# APNA JSON DATA YAHAN PASTE KARO
# ============================================
data = [
    {
        "id": 1,
        "section": "A - Profit & Loss",
        "question": "A wrist watch purchased for Rs.3,000 sold for Rs.3,500. Find profit %.",
        "options": {"a": "20.50%", "b": "18.33%", "c": "16.66%", "d": "19.58%"},
        "correct_answer": "c",
        "correct_value": "16.66%",
        "solution": {
            "steps": [
                "Profit = SP - CP = 3500 - 3000 = Rs.500",
                "Profit% = (500/3000) x 100 = 16.66%"
            ],
            "trick": "Direct formula: Profit% = (Profit/CP) x 100"
        }
    },
    # ... BAAKI QUESTIONS YAHAN ADD KARO
]

# ============================================
# STYLES DEFINE KARO
# ============================================
def get_styles():
    styles = {}
    
    # Header style
    styles['header'] = ParagraphStyle(
        'header',
        fontName='Helvetica-Bold',
        fontSize=11,
        textColor=colors.white,
        alignment=TA_CENTER,
        spaceAfter=4,
        spaceBefore=4,
    )
    
    # Section header
    styles['section'] = ParagraphStyle(
        'section',
        fontName='Helvetica-Bold',
        fontSize=10,
        textColor=colors.white,
        alignment=TA_LEFT,
        spaceAfter=2,
        spaceBefore=2,
        leftIndent=5,
    )
    
    # Question style
    styles['question'] = ParagraphStyle(
        'question',
        fontName='Helvetica-Bold',
        fontSize=8,
        textColor=colors.black,
        spaceAfter=3,
        spaceBefore=3,
        leftIndent=2,
    )
    
    # Options style
    styles['option'] = ParagraphStyle(
        'option',
        fontName='Helvetica',
        fontSize=8,
        textColor=colors.black,
        spaceAfter=1,
        leftIndent=5,
    )
    
    # Answer style
    styles['answer'] = ParagraphStyle(
        'answer',
        fontName='Helvetica-Bold',
        fontSize=8,
        textColor=colors.HexColor('#B8860B'),
        spaceAfter=2,
        leftIndent=2,
    )
    
    # Solution style
    styles['solution'] = ParagraphStyle(
        'solution',
        fontName='Helvetica-Oblique',
        fontSize=7,
        textColor=colors.HexColor('#555555'),
        spaceAfter=2,
        leftIndent=5,
    )
    
    # Sub header (Time/Marks line)
    styles['subheader'] = ParagraphStyle(
        'subheader',
        fontName='Helvetica-Bold',
        fontSize=8,
        textColor=colors.black,
        alignment=TA_LEFT,
    )
    
    # Instructions
    styles['instructions'] = ParagraphStyle(
        'instructions',
        fontName='Helvetica',
        fontSize=7.5,
        textColor=colors.black,
        alignment=TA_LEFT,
    )
    
    return styles


# ============================================
# QUESTION CELL CONTENT BANAO
# ============================================
def make_question_cell(q, styles):
    """Ek question ka content list return karta hai"""
    content = []
    
    # Question number + text
    q_text = f"★ Q{q['id']}. {q['question']}"
    content.append(Paragraph(q_text, styles['question']))
    
    # Options - 2 per row
    opts = list(q['options'].items())
    opt_rows = []
    for i in range(0, len(opts), 2):
        row = []
        row.append(f"(a) {opts[i][1]}" if i == 0 else f"(c) {opts[i][1]}")
        if i+1 < len(opts):
            row.append(f"(b) {opts[i+1][1]}" if i == 0 else f"(d) {opts[i+1][1]}")
        else:
            row.append("")
        opt_rows.append(row)
    
    # Fix option labels properly
    option_items = list(q['options'].items())
    
    # Row 1: (a) and (b)
    row1_text = ""
    row2_text = ""
    
    if len(option_items) >= 2:
        row1_text = (
            f"(a) {option_items[0][1]}          "
            f"(b) {option_items[1][1]}"
        )
    if len(option_items) >= 4:
        row2_text = (
            f"(c) {option_items[2][1]}          "
            f"(d) {option_items[3][1]}"
        )
    
    content.append(Paragraph(row1_text, styles['option']))
    if row2_text:
        content.append(Paragraph(row2_text, styles['option']))
    
    # Answer
    ans_text = (
        f"Ans: ({q['correct_answer']}) "
        f"{q['correct_value']}"
    )
    content.append(Paragraph(ans_text, styles['answer']))
    
    # Solution steps (short)
    sol_steps = q['solution']['steps']
    sol_text = " | ".join(sol_steps[:2])  # sirf first 2 steps
    if len(sol_text) > 120:
        sol_text = sol_text[:120] + "..."
    content.append(Paragraph(sol_text, styles['solution']))
    
    return content


# ============================================
# SECTION GROUPING
# ============================================
def group_by_section(data):
    sections = {}
    for q in data:
        sec = q['section']
        if sec not in sections:
            sections[sec] = []
        sections[sec].append(q)
    return sections


# ============================================
# MAIN PDF GENERATOR
# ============================================
def generate_pdf(data, filename="SSC_Maths_Practice.pdf"):
    
    doc = SimpleDocTemplate(
        filename,
        pagesize=A4,
        rightMargin=1*cm,
        leftMargin=1*cm,
        topMargin=1.5*cm,
        bottomMargin=1.5*cm,
    )
    
    styles = get_styles()
    story = []
    
    page_width = A4[0] - 2*cm  # usable width
    
    # ----------------------------------------
    # MAIN TITLE
    # ----------------------------------------
    title_data = [[
        Paragraph(
            "SSC Selection Post — Maths Repeated Concepts Practice Sheet",
            styles['header']
        )
    ]]
    title_table = Table(title_data, colWidths=[page_width])
    title_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#1a3a5c')),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(title_table)
    story.append(Spacer(1, 0.2*cm))
    
    # ----------------------------------------
    # TIME / MARKS ROW
    # ----------------------------------------
    info_data = [[
        Paragraph("<b>Time Allowed:</b> 3 Hrs 20 Min", styles['subheader']),
        Paragraph("<b>Total Questions:</b> 55", styles['subheader']),
        Paragraph("<b>Maximum Marks:</b> 220", styles['subheader']),
    ]]
    info_table = Table(
        info_data, 
        colWidths=[page_width/3]*3
    )
    info_table.setStyle(TableStyle([
        ('BOX', (0,0), (-1,-1), 0.5, colors.grey),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.grey),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#f5f5f5')),
    ]))
    story.append(info_table)
    story.append(Spacer(1, 0.1*cm))
    
    # ----------------------------------------
    # INSTRUCTIONS ROW
    # ----------------------------------------
    inst_data = [[
        Paragraph(
            "<b>Instructions:</b> +4 for correct | "
            "-1 for wrong | ★ = appeared 5+ times | "
            "◆ = appeared 3-4 times across SSC papers",
            styles['instructions']
        )
    ]]
    inst_table = Table(inst_data, colWidths=[page_width])
    inst_table.setStyle(TableStyle([
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor('#FFA500')),
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#FFF8E7')),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(inst_table)
    story.append(Spacer(1, 0.3*cm))
    
    # ----------------------------------------
    # SECTIONS + QUESTIONS (2-column layout)
    # ----------------------------------------
    sections = group_by_section(data)
    col_width = (page_width - 0.3*cm) / 2  # 2 column width
    
    for section_name, questions in sections.items():
        
        # Section Header
        sec_data = [[
            Paragraph(f"SECTION {section_name} [★ 5+ times]", 
                     styles['section'])
        ]]
        sec_table = Table(sec_data, colWidths=[page_width])
        sec_table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#1a5276')),
            ('TOPPADDING', (0,0), (-1,-1), 6),
            ('BOTTOMPADDING', (0,0), (-1,-1), 6),
            ('LEFTPADDING', (0,0), (-1,-1), 8),
        ]))
        story.append(sec_table)
        story.append(Spacer(1, 0.15*cm))
        
        # Questions in pairs (2 columns)
        for i in range(0, len(questions), 2):
            q_left = questions[i]
            q_right = questions[i+1] if i+1 < len(questions) else None
            
            # Left column content
            left_content = make_question_cell(q_left, styles)
            
            # Right column content
            if q_right:
                right_content = make_question_cell(q_right, styles)
            else:
                right_content = [Paragraph("", styles['question'])]
            
            # 2-column table
            row_data = [[left_content, right_content]]
            
            two_col = Table(
                row_data,
                colWidths=[col_width, col_width],
            )
            two_col.setStyle(TableStyle([
                # Border around each cell
                ('BOX', (0,0), (0,0), 0.5, colors.HexColor('#cccccc')),
                ('BOX', (1,0), (1,0), 0.5, colors.HexColor('#cccccc')),
                # Background
                ('BACKGROUND', (0,0), (-1,-1), colors.white),
                # Padding
                ('TOPPADDING', (0,0), (-1,-1), 6),
                ('BOTTOMPADDING', (0,0), (-1,-1), 6),
                ('LEFTPADDING', (0,0), (-1,-1), 6),
                ('RIGHTPADDING', (0,0), (-1,-1), 6),
                # Vertical align top
                ('VALIGN', (0,0), (-1,-1), 'TOP'),
                # Middle divider
                ('LINEAFTER', (0,0), (0,-1), 0.5, colors.HexColor('#cccccc')),
            ]))
            
            story.append(two_col)
            story.append(Spacer(1, 0.15*cm))
        
        story.append(Spacer(1, 0.3*cm))
    
    # ----------------------------------------
    # BUILD PDF
    # ----------------------------------------
    doc.build(story)
    print(f"✅ PDF ready: {filename}")


# ============================================
# RUN KARO
# ============================================
if __name__ == "__main__":
    generate_pdf(data, "SSC_Maths_Practice.pdf")
