def pdf_context(pdf_text):
    if not pdf_text:
        return ""

    return f"The user uploaded this PDF:\n{pdf_text[:5000]}"