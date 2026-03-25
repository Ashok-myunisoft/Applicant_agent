def build_profile(form: dict, resume: str) -> str:

    profile = f"""
Name: {form.get('name')}
Email: {form.get('email')}
Experience: {form.get('experience')} years
Expected CTC: {form.get('expected_ctc')} LPA
Skills: {form.get('skills')}
Education: {form.get('education')}

Resume:
{resume}
"""

    return profile.strip()
