from fastapi import APIRouter, UploadFile, HTTPException, Form
from services.pdf_parser import extract_text
from services.llm import analyze
import json

router = APIRouter(prefix='/analyze')

@router.post('/')
async def analyze_document(file: UploadFile, detail: str = Form('medium')):
    if file.content_type != 'application/pdf':
        raise HTTPException(400, 'Only PDFs accepted')
    if detail not in ('short', 'medium', 'long'):
        detail = 'medium'
    raw = await file.read()
    text = extract_text(raw)
    result = await analyze(text, detail)
    return json.loads(result)
