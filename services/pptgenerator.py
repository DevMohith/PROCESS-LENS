import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN

def generate_ppt(title: str, summary: str, bullets: list, kpis: dict, filename: str, output_dir: str = "./outputs") -> str:
    os.makedirs(output_dir, exist_ok=True)
    path = os.path.join(output_dir, filename)

    prs = Presentation()

    #title slide
    slide_layout = prs.slide_layouts[0]
    slide = prs.slides.add_slide(slide_layout)
    slide.shapes.title.text = title
    slide.placeholders[1].text = summary

    #kpi slide will be generated here on looping through paras
    slide = prs.slides.add_slide(prs.slide_layouts[1])
    slide.shapes.title.text = "Key Metrics (Last 7 days)"
    tf = slide.shapes.placeholders[1].text_frame
    tf.clear()
    for k, v in kpis.items():
        p = tf.add_paragraph() if tf.text else tf.paragraphs[0]
        p.text = f"{k}: {v}"
        p.level = 0

    # Bottlenecks slide will be writtened in bullets
    slide = prs.slides.add_slide(prs.slide_layouts[1])
    slide.shapes.title.text = "Bottlenecks & Actions"
    tf = slide.shapes.placeholders[1].text_frame
    tf.clear()
    for b in bullets:
        p = tf.add_paragraph() if tf.text else tf.paragraphs[0]
        p.text = f"• {b}"
        p.level = 0

    # solutions slide
    slide = prs.slides.add_slide(prs.slide_layouts[5])
    slide.shapes.title.text = "Next Steps"
    body = slide.shapes.placeholders[1].text_frame
    body.clear()
    for line in [
        "1) Validate data assumptions with process owners",
        "2) Pilot quick wins (SLA alerts, approval auto-routing)",
        "3) Re-measure cycle time & rework after 2 weeks"
    ]:
        p = body.add_paragraph() if body.text else body.paragraphs[0]
        p.text = line
        p.level = 0

    prs.save(path)
    return path
