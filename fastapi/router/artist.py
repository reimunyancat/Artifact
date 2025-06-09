from fastapi import APIRouter, Query, HTTPException
from entity.artist import Artist, Music
from datetime import date
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain.tools import DuckDuckGoSearchRun
import os

# OpenAI API 키 설정
os.environ["OPENAI_API_KEY"] = ""  # 자신의 키로 교체

router = APIRouter(prefix="/artist", tags=["artist"])

# LangChain 구성
search = DuckDuckGoSearchRun()

template = """You are a helpful assistant.

Using the context below, write a JSON summary about the artist {question}.

Context:
{context}

Format:
{{
  "artist_name": "...",
  "introduction": "...",
  "feature": ["...", "..."],
  "musics": [
    {{
      "name": "...",
      "publish_date": "YYYY-MM-DD",
      "music_link": "...",
      "album_name": "...",
      "genre": "..."
    }}
  ]
}}
"""

prompt = ChatPromptTemplate.from_template(template)
model = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)
parser = StrOutputParser()

chain = (
    {"question": RunnablePassthrough(), "context": RunnablePassthrough()}
    | prompt
    | model
    | parser
)

# 엔드포인트
@router.get("/search", response_model=Artist)
async def search_artist(artist_name: str = Query(..., title="Artist name")):
    context = search.run(f"{artist_name} biography")
    result = chain.invoke({
        "question": artist_name,
        "context": context
    })
    
    try:
        # 문자열을 파싱해서 JSON 응답 객체로 변환
        import json
        return Artist.parse_obj(json.loads(result))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI 응답 파싱 실패: {str(e)}")
