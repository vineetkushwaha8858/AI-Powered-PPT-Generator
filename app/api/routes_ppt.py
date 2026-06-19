from fastapi import APIRouter, Form, HTTPException, BackgroundTasks
from fastapi.responses import FileResponse
import os, uuid, tempfile


from app.services.ppt_service import FastPresentationGenerator
from app.services.template_service import get_available_templates, get_template_path, analyze_template
from app.core.utils import cleanup_temp_file



router = APIRouter()

@router.post("/generate-presentation")
async def generate_presentation_with_popup(
    background_tasks: BackgroundTasks,
    template_number: int = Form(...),
    topic: str = Form(...),
    num_slides: int = Form(...)
):
    try:
        current_templates = get_available_templates()
        if not current_templates:
            raise HTTPException(status_code=404, detail="No template files found")
        if template_number not in current_templates:
            available_nums = list(current_templates.keys())
            raise HTTPException(status_code=400, detail=f"Template {template_number} not found. Available: {available_nums}")
        # Fix: Allow min 2 slides instead of 3
        if num_slides < 2 or num_slides > 20:
            raise HTTPException(status_code=400, detail="Number of slides must be between 2 and 20")
        template_path = get_template_path(template_number)
        if not os.path.exists(template_path):
            raise HTTPException(status_code=404, detail=f"Template file not found: {template_path}")
        unique_id = str(uuid.uuid4())[:8]
        generator = FastPresentationGenerator()
        final_slides, professional_topic = generator.generate_presentation_fast(topic, template_path, num_slides)
        output_filename = f"presentation_T{template_number}_{unique_id}.pptx"
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pptx") as temp_file:
            temp_path = temp_file.name
            template_info, prs = analyze_template(template_path)
            if not template_info:
                raise HTTPException(status_code=500, detail="Failed to analyze template")
            from app.services.ppt_service import remove_all_slides, find_layout, apply_formatting
            remove_all_slides(prs)
            for slide_data in final_slides:
                layout = prs.slide_layouts[find_layout(template_info, slide_data["type"])]
                slide = prs.slides.add_slide(layout)
                apply_formatting(slide, slide_data)
            prs.save(temp_path)
            background_tasks.add_task(cleanup_temp_file, temp_path)
            return FileResponse(
                path=temp_path,
                media_type='application/vnd.openxmlformats-officedocument.presentationml.presentation',
                filename=output_filename
            )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating presentation: {str(e)}")
