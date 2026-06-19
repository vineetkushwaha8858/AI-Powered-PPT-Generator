import os
from pptx import Presentation

def get_template_dir():
    # template_service.py location se ek level upar jaake templates folder ko locate karo
    return os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "templates"))

def get_available_templates():
    templates_dir = get_template_dir()
    print("TEMPLATES_FOLDER_PATH:", templates_dir)
    print("Templates found:", os.listdir(templates_dir))
    template_names = {
        1: "Business Template", 2: "Academic Template", 3: "Creative Template",
        4: "Professional Template", 5: "Modern Template", 6: "Corporate Template",
        7: "Educational Template", 8: "Tech Template", 9: "Medical Template",
        10: "Marketing Template"
    }
    available_templates = {}
    for i in range(1, 11):
        template_path = os.path.join(templates_dir, f"template{i}.pptx")
        if os.path.exists(template_path):
            available_templates[i] = {
                "name": template_names.get(i, f"Template {i}"),
                "file": f"template{i}.pptx"
            }
    return available_templates

def get_template_path(template_number: int) -> str:
    templates_dir = get_template_dir()
    current_templates = get_available_templates()
    if template_number in current_templates:
        return os.path.join(templates_dir, current_templates[template_number]['file'])
    else:
        if current_templates:
            first_template = min(current_templates.keys())
            return os.path.join(templates_dir, current_templates[first_template]['file'])
        else:
            return os.path.join(templates_dir, f"template{template_number}.pptx")

def analyze_template(template_path):
    try:
        prs = Presentation(template_path)
        return {
            "layouts": [
                {"layout_index": i, "layout_name": l.name}
                for i, l in enumerate(prs.slide_layouts)
            ]
        }, prs
    except Exception as e:
        print("Error analyzing template:", e)
        return None, None
