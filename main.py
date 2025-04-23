from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, RedirectResponse, FileResponse, PlainTextResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn
import os

app = FastAPI(
    title="GPT워터마크제거",
    description="GPT에서 생성된 텍스트의 워터마크를 감지하고 제거하는 서비스",
    version="1.0.0"
)

# 정적 파일 및 템플릿 설정
app.mount("/static", StaticFiles(directory="static"), name="static")

# 다국어 지원을 위한 설정
LANGUAGES = ["ko", "en", "ja"]


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    """사용자 언어에 따라 적절한 페이지로 리다이렉트"""
    # 브라우저 언어 감지
    accept_language = request.headers.get("accept-language", "")
    # 기본 언어는 한국어
    default_lang = "ko"

    if accept_language:
        # 간단한 언어 감지 로직
        for lang in LANGUAGES:
            if lang in accept_language.lower():
                return RedirectResponse(url=f"/{lang}/")

    # 기본 언어로 리다이렉트
    return RedirectResponse(url=f"/{default_lang}/")


@app.get("/ko/", response_class=HTMLResponse)
async def korean_page():
    """한국어 페이지 제공"""
    return FileResponse("index.html")


@app.get("/en/", response_class=HTMLResponse)
async def english_page():
    """영어 페이지 제공"""
    return FileResponse("en.html")


@app.get("/ja/", response_class=HTMLResponse)
async def japanese_page():
    """일본어 페이지 제공"""
    return FileResponse("ja.html")


@app.get("/sitemap.xml", response_class=HTMLResponse)
async def sitemap():
    """사이트맵 제공"""
    return FileResponse("sitemap.xml")


@app.get("/rss.xml", response_class=HTMLResponse)
async def rss():
    """RSS 피드 제공"""
    return FileResponse("rss.xml")


@app.get("/robots.txt", response_class=PlainTextResponse)
async def robots():
    """로봇 텍스트 파일 제공"""
    return """User-agent: *
Allow: /
Allow: /ko/
Allow: /en/
Allow: /ja/
Sitemap: https://gptmark.loeaf.com/sitemap.xml
"""


if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)