import json
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer,
    Table, TableStyle
)
from reportlab.lib.enums import TA_LEFT, TA_CENTER

# ============================================
# COMPLETE DATA
# ============================================
data = [
    { }
]


# ============================================
# STYLES
# ============================================
def get_styles():
    styles = {}
    styles['title'] = ParagraphStyle(
        'title', fontName='Helvetica-Bold', fontSize=11,
        textColor=colors.white, alignment=TA_CENTER,
        spaceAfter=2, spaceBefore=2
    )
    styles['section_hdr'] = ParagraphStyle(
        'section_hdr', fontName='Helvetica-Bold', fontSize=9,
        textColor=colors.white, alignment=TA_LEFT,
        spaceAfter=2, spaceBefore=2, leftIndent=4
    )
    styles['question'] = ParagraphStyle(
        'question', fontName='Helvetica-Bold', fontSize=8,
        textColor=colors.black, spaceAfter=3,
        spaceBefore=3, leftIndent=2
    )
    styles['option'] = ParagraphStyle(
        'option', fontName='Helvetica', fontSize=7.5,
        textColor=colors.black, spaceAfter=1, leftIndent=4
    )
    styles['answer'] = ParagraphStyle(
        'answer', fontName='Helvetica-Bold', fontSize=8,
        textColor=colors.HexColor('#8B6914'),
        spaceAfter=2, leftIndent=2
    )
    styles['solution'] = ParagraphStyle(
        'solution', fontName='Helvetica-Oblique', fontSize=7,
        textColor=colors.HexColor('#444444'),
        spaceAfter=1, leftIndent=4
    )
    styles['info'] = ParagraphStyle(
        'info', fontName='Helvetica-Bold', fontSize=8,
        textColor=colors.black, alignment=TA_LEFT
    )
    styles['inst'] = ParagraphStyle(
        'inst', fontName='Helvetica', fontSize=7.5,
        textColor=colors.black
    )
    return styles


# ============================================
# QUESTION CELL
# ============================================
def make_cell(q, styles):
    content = []
    star = "* " if q['id'] <= 18 else "* "
    content.append(Paragraph(
        f"{star}Q{q['id']}. {q['question']}",
        styles['question']
    ))
    opts = list(q['options'].items())
    if len(opts) >= 2:
        content.append(Paragraph(
            f"(a) {opts[0][1]}     (b) {opts[1][1]}",
            styles['option']
        ))
    if len(opts) >= 4:
        content.append(Paragraph(
            f"(c) {opts[2][1]}     (d) {opts[3][1]}",
            styles['option']
        ))
    content.append(Paragraph(
        f"Ans: ({q['correct_answer']}) {q['correct_value']}",
        styles['answer']
    ))
    sol = " | ".join(q['solution']['steps'])
    if len(sol) > 150:
        sol = sol[:150] + "..."
    content.append(Paragraph(sol, styles['solution']))
    return content


# ============================================
# GROUP BY SECTION
# ============================================
def group_sections(data):
    sections = {}
    order = []
    for q in data:
        s = q['section']
        if s not in sections:
            sections[s] = []
            order.append(s)
        sections[s].append(q)
    return sections, order


# ============================================
# BUILD PDF
# ============================================
def build_pdf(data, filename="SSC_Maths_TwoColumn.pdf"):
    doc = SimpleDocTemplate(
        filename, pagesize=A4,
        rightMargin=0.8*cm, leftMargin=0.8*cm,
        topMargin=1.2*cm, bottomMargin=1.2*cm
    )
    styles = get_styles()
    story = []
    W = A4[0] - 1.6*cm

    # --- TITLE ---
    t = Table([[Paragraph(
        "SSC Selection Post — Maths Repeated Concepts Practice Sheet",
        styles['title']
    )]], colWidths=[W])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#1a3a5c')),
        ('TOPPADDING', (0,0), (-1,-1), 7),
        ('BOTTOMPADDING', (0,0), (-1,-1), 7),
    ]))
    story.append(t)
    story.append(Spacer(1, 0.15*cm))

    # --- INFO ROW ---
    info = Table([[
        Paragraph("<b>Time Allowed:</b> 3 Hrs 20 Min", styles['info']),
        Paragraph("<b>Total Questions:</b> 55", styles['info']),
        Paragraph("<b>Maximum Marks:</b> 220", styles['info']),
    ]], colWidths=[W/3]*3)
    info.setStyle(TableStyle([
        ('BOX', (0,0), (-1,-1), 0.5, colors.grey),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.grey),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#f0f0f0')),
    ]))
    story.append(info)
    story.append(Spacer(1, 0.1*cm))

    # --- INSTRUCTIONS ---
    inst = Table([[Paragraph(
        "<b>Instructions:</b> +4 for correct | -1 for wrong | "
        "* = appeared 5+ times | # = appeared 3-4 times across SSC papers",
        styles['inst']
    )]], colWidths=[W])
    inst.setStyle(TableStyle([
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor('#FFA500')),
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#FFFBF0')),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(inst)
    story.append(Spacer(1, 0.25*cm))

    # --- SECTIONS + QUESTIONS ---
    sections, order = group_sections(data)
    col_w = (W - 0.2*cm) / 2

    for sec in order:
        qs = sections[sec]

        # Section Header
        sh = Table([[Paragraph(
            f"SECTION {sec} [* 5+ times]",
            styles['section_hdr']
        )]], colWidths=[W])
        sh.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#1a5276')),
            ('TOPPADDING', (0,0), (-1,-1), 5),
            ('BOTTOMPADDING', (0,0), (-1,-1), 5),
            ('LEFTPADDING', (0,0), (-1,-1), 6),
        ]))
        story.append(sh)
        story.append(Spacer(1, 0.1*cm))

        # 2-column question pairs
        for i in range(0, len(qs), 2):
            left = make_cell(qs[i], styles)
            right = make_cell(qs[i+1], styles) if i+1 < len(qs) else [Paragraph("", styles['question'])]

            row = Table(
                [[left, right]],
                colWidths=[col_w, col_w]
            )
            row.setStyle(TableStyle([
                ('BOX', (0,0), (0,0), 0.4, colors.HexColor('#bbbbbb')),
                ('BOX', (1,0), (1,0), 0.4, colors.HexColor('#bbbbbb')),
                ('BACKGROUND', (0,0), (-1,-1), colors.white),
                ('VALIGN', (0,0), (-1,-1), 'TOP'),
                ('TOPPADDING', (0,0), (-1,-1), 5),
                ('BOTTOMPADDING', (0,0), (-1,-1), 5),
                ('LEFTPADDING', (0,0), (-1,-1), 5),
                ('RIGHTPADDING', (0,0), (-1,-1), 5),
                ('LINEAFTER', (0,0), (0,-1), 0.4, colors.HexColor('#bbbbbb')),
            ]))
            story.append(row)
            story.append(Spacer(1, 0.1*cm))

        story.append(Spacer(1, 0.2*cm))

    doc.build(story)
    print(f"PDF ready: {filename}")


# ============================================
# RUN
# ============================================
build_pdf(data)
