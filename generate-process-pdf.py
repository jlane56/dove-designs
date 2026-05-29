"""
The Dove Design Co. — Project Process PDF Generator
Usage: python3 generate-process-pdf.py [current_stage]
  current_stage: 1–10 (default: 0 = no stage highlighted, for sharing as overview)
Example: python3 generate-process-pdf.py 4
"""

import sys
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor, white, black
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# ── Brand Colors ──────────────────────────────────────────────
CREAM       = HexColor('#F8F0DD')
WHITE       = HexColor('#FCF8EE')
CHARCOAL    = HexColor('#535344')
TAUPE       = HexColor('#98A091')
GOLD        = HexColor('#AB8552')
GOLD_LIGHT  = HexColor('#D4B483')
BORDER      = HexColor('#DDD5C0')
DARK_BG     = HexColor('#3E3E32')

# ── Stages ────────────────────────────────────────────────────
STAGES = [
    (
        "Discovery Call",
        "A 30–45 minute conversation where we learn everything about your business, your goals, and what success looks like. No pitch — just listening."
    ),
    (
        "Proposal",
        "We send a detailed scope document outlining every page, every feature, the timeline, and the investment. You review, ask questions, and approve."
    ),
    (
        "Contract + Deposit",
        "The agreement is signed and the first payment (50%) is made. This is our green light. Work does not begin until both are complete."
    ),
    (
        "Content Collection",
        "You provide all copy, photos, and brand assets. We give you a checklist and a deadline. This phase sets the pace for everything that follows."
    ),
    (
        "Design",
        "We build out the visual direction — layout, typography, color, imagery. You review and give feedback before a single line of code is written."
    ),
    (
        "Development",
        "Your approved design gets hand-coded into a real, fast, responsive website. Every page. Every interaction. Built from scratch, no templates."
    ),
    (
        "Internal Review",
        "Before you see anything, we test everything ourselves — mobile, forms, links, speed, and cross-browser. We catch our own mistakes first."
    ),
    (
        "Client Review",
        "We send you a private staging link to click through. You have two rounds of revisions included. Feedback is collected and applied."
    ),
    (
        "Final Approval + Payment",
        "You sign off on the finished site. The final invoice (50%) is due before launch. Once cleared, we're ready to go live."
    ),
    (
        "Launch + Handoff",
        "Your domain is pointed, the site goes live, and we walk you through everything. You're handed the keys to your new online home."
    ),
]

def generate_pdf(current_stage=0, output_path="TDDC-Project-Process.pdf"):
    W, H = letter  # 612 x 792

    c = canvas.Canvas(output_path, pagesize=letter)
    c.setTitle("The Dove Design Co. — Project Process")

    # ── Background ──────────────────────────────────────────
    c.setFillColor(WHITE)
    c.rect(0, 0, W, H, fill=1, stroke=0)

    # ── Header Bar ──────────────────────────────────────────
    c.setFillColor(CHARCOAL)
    c.rect(0, H - 88, W, 88, fill=1, stroke=0)

    # Brand name
    c.setFillColor(CREAM)
    c.setFont("Helvetica", 9)
    c._charSpace = 3
    c.drawString(44, H - 34, "THE DOVE DESIGN CO.")
    c._charSpace = 0

    # Page title
    c.setFillColor(CREAM)
    c.setFont("Helvetica-Bold", 20)
    c.drawString(44, H - 62, "Your Project, Step by Step.")

    # Subtitle
    c.setFillColor(GOLD_LIGHT)
    c.setFont("Helvetica", 9)
    c._charSpace = 1.5
    if current_stage > 0:
        c.drawString(44, H - 76, f"CURRENTLY IN STAGE {current_stage} OF 10")
    else:
        c.drawString(44, H - 76, "10 STAGES FROM FIRST CALL TO LAUNCH")
    c._charSpace = 0

    # ── Gold accent line under header ───────────────────────
    c.setStrokeColor(GOLD)
    c.setLineWidth(2)
    c.line(44, H - 92, W - 44, H - 92)

    # ── Stages ──────────────────────────────────────────────
    START_Y   = H - 116
    ROW_H     = 63
    LEFT      = 44
    DOT_X     = LEFT + 16
    LINE_X    = DOT_X
    TEXT_X    = LEFT + 46
    DOT_R     = 11

    for i, (title, desc) in enumerate(STAGES):
        stage_num = i + 1
        y = START_Y - i * ROW_H

        is_active    = (stage_num == current_stage)
        is_complete  = (current_stage > 0 and stage_num < current_stage)
        is_future    = (current_stage > 0 and stage_num > current_stage)
        is_overview  = (current_stage == 0)

        # ── Connector line between dots ─────────────────────
        if i < len(STAGES) - 1:
            line_top    = y - DOT_R
            line_bottom = y - ROW_H + DOT_R
            if is_complete:
                c.setStrokeColor(GOLD)
                c.setLineWidth(1.5)
            elif is_active:
                c.setStrokeColor(GOLD)
                c.setLineWidth(1)
            else:
                c.setStrokeColor(BORDER)
                c.setLineWidth(1)
            c.line(LINE_X, line_top, LINE_X, line_bottom)

        # ── Row background for active stage ─────────────────
        if is_active:
            c.setFillColor(HexColor('#F2EAD6'))
            c.roundRect(LEFT - 6, y - DOT_R - 6, W - LEFT * 2 + 12, ROW_H - 6, 4, fill=1, stroke=0)

        # ── Dot ─────────────────────────────────────────────
        if is_complete:
            # Filled gold dot with checkmark
            c.setFillColor(GOLD)
            c.circle(DOT_X, y, DOT_R, fill=1, stroke=0)
            c.setFillColor(WHITE)
            c.setFont("Helvetica-Bold", 10)
            c.drawCentredString(DOT_X, y - 3.5, "✓")
        elif is_active:
            # Large gold ring with number
            c.setFillColor(GOLD)
            c.circle(DOT_X, y, DOT_R + 1, fill=1, stroke=0)
            c.setFillColor(WHITE)
            c.setFont("Helvetica-Bold", 9)
            c.drawCentredString(DOT_X, y - 3, str(stage_num))
        elif is_future:
            # Empty ring
            c.setFillColor(WHITE)
            c.setStrokeColor(BORDER)
            c.setLineWidth(1)
            c.circle(DOT_X, y, DOT_R, fill=1, stroke=1)
            c.setFillColor(TAUPE)
            c.setFont("Helvetica", 8)
            c.drawCentredString(DOT_X, y - 3, str(stage_num))
        else:
            # Overview mode — gold outline, number inside
            c.setFillColor(WHITE)
            c.setStrokeColor(GOLD)
            c.setLineWidth(1.2)
            c.circle(DOT_X, y, DOT_R, fill=1, stroke=1)
            c.setFillColor(CHARCOAL)
            c.setFont("Helvetica-Bold", 8)
            c.drawCentredString(DOT_X, y - 3, str(stage_num))

        # ── Stage label ─────────────────────────────────────
        if is_active:
            c.setFillColor(CHARCOAL)
            c.setFont("Helvetica-Bold", 10)
        elif is_complete:
            c.setFillColor(GOLD)
            c.setFont("Helvetica-Bold", 9)
        elif is_future:
            c.setFillColor(TAUPE)
            c.setFont("Helvetica", 9)
        else:
            c.setFillColor(CHARCOAL)
            c.setFont("Helvetica-Bold", 9)

        c.drawString(TEXT_X, y + 2, title.upper() if is_active else title)

        # ── Stage description ────────────────────────────────
        if is_future:
            c.setFillColor(HexColor('#C0B8A8'))
        elif is_complete:
            c.setFillColor(TAUPE)
        else:
            c.setFillColor(TAUPE)
        c.setFont("Helvetica", 7.5)

        # Word wrap description to fit
        max_width = W - TEXT_X - 44
        words = desc.split()
        lines = []
        current_line = []
        for word in words:
            test = ' '.join(current_line + [word])
            if c.stringWidth(test, "Helvetica", 7.5) < max_width:
                current_line.append(word)
            else:
                lines.append(' '.join(current_line))
                current_line = [word]
        if current_line:
            lines.append(' '.join(current_line))

        for j, line in enumerate(lines[:2]):  # max 2 lines
            c.drawString(TEXT_X, y - 10 - j * 11, line)

    # ── Footer ──────────────────────────────────────────────
    c.setFillColor(CHARCOAL)
    c.rect(0, 0, W, 40, fill=1, stroke=0)

    c.setFillColor(TAUPE)
    c.setFont("Helvetica", 7.5)
    c._charSpace = 1
    c.drawString(44, 15, "THEDOVEDESIGNCO.COM")
    c._charSpace = 0

    c.setFillColor(GOLD)
    c.setFont("Helvetica", 7.5)
    c.drawRightString(W - 44, 15, "Questions? hello@thedovedesignco.com")

    # ── Subtle grain overlay effect (diagonal lines) ─────────
    c.setStrokeColor(HexColor('#E8E0CC'))
    c.setLineWidth(0.2)
    # (keeping it clean, skipping grain)

    c.save()
    print(f"✓ PDF saved: {output_path}")

# ── Run ──────────────────────────────────────────────────────
if __name__ == "__main__":
    stage = int(sys.argv[1]) if len(sys.argv) > 1 else 0
    out = f"TDDC-Project-Process{'--Stage-' + sys.argv[1] if len(sys.argv) > 1 else ''}.pdf"
    generate_pdf(current_stage=stage, output_path=f"/Users/justinlane/Claude/dove-designs/{out}")
