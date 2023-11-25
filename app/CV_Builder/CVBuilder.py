import logging
from .FileIO import FileIO
from .PromptInterface import CV_Chat
import uuid
logger = logging.getLogger(__name__)

def do_generate_cv_and_cl(old_cv, job_description:str):
    # constant  
    max_try = 5
    CV_template_path = 'Templates/CV_template.txt'
    CoverLetter_template_path = 'Templates/CoverLetter_template.txt'
    CoverLetterInstr_path = 'Templates/CoverLetterInstruct.txt'
    # Read files
    # old_cv = ' '.join(format(ord(x), 'b') for x in old_cv_str)
    old_cv = FileIO.read_old_cv_binary(old_cv)

    cv_template = FileIO.read_file(CV_template_path)
    CoverLetter_template = FileIO.read_file(CoverLetter_template_path)
    CoverLetterInstr = FileIO.read_file(CoverLetterInstr_path)

    # Build CV and cover letter
    task_id = str(uuid.uuid4())
    if all([old_cv, cv_template, CoverLetter_template, CoverLetterInstr,job_description]):
        cv_build_success = False
        for i in range(0,max_try):
            logger.info("Building CV...")
            new_cv_content = CV_Chat.generate_cv(old_cv,cv_template,job_description)
            logger.info("Checking CV...")
            new_cv_content = CV_Chat.latex_verify(new_cv_content)
            if new_cv_content is not None:
                cv_build_success = True
                break
            logger.warning("identified an error, rebuilding CV...")
        if cv_build_success:
            FileIO.generate_pdf(new_cv_content,f'CV_Builder/Output/newCV-{task_id}')
        else:
            logger.error("problem in building a valid CV...")
            return None

        cl_build_success = False
        for i in range(0,max_try):
            logger.info("Building Cover Letter...")
            cover_letter = CV_Chat.generate_cl(job_description,CoverLetter_template,CoverLetterInstr, old_cv)
            logger.info("Checking Cover Letter...")
            cover_letter = CV_Chat.latex_verify(cover_letter)
            if cover_letter is not None:
                cl_build_success = True
                break
            logger.warning("identified an error, rebuilding Cover Letter...")
        if cl_build_success:
            FileIO.generate_pdf(cover_letter,f'CV_Builder/Output/CoverLetter-{task_id}')
        else:
            logger.error("problem in building a valid Cover Letter...")
            return None
    return task_id
