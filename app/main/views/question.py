from flask import render_template
from app import content_loader, data_api_client
from ...main import main

from dmcontent.govuk_frontend import from_question, govuk_file_upload, render_question


@main.route("/test/file-upload")
def test_file_upload():
    framework_slug = "g-cloud-12"
    section_id = "modern-slavery"

    content_loader.load_manifest("g-cloud-12", "declaration", "declaration")
    content = content_loader.get_manifest("g-cloud-12", "declaration").filter({}, inplace_allowed=True)
    section = content.get_section(section_id)

    # Testing a specific question - the file upload one
    question = section.questions[0].questions[2]

    #import pdb; pdb.set_trace()

    return render_template(
        "question_test.html",
        section=section,
        question=question,
        declaration_answers=None,
        errors={}
    )
