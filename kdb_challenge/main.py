from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from kdb_challenge.engine import BM25, SUGGESTIONS_DF
from kdb_challenge.models import SuggestionRequest, SuggestionResponse


app = FastAPI(
    title="BM25 Suggestion Service",
    version="1.0.0",
    description="A simple BM25-powered suggestion API"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


documents = SUGGESTIONS_DF["suggestion"].to_list()
bm25 = BM25(documents, dataframe=SUGGESTIONS_DF)


@app.post("/suggestions", response_model=SuggestionResponse)
def get_suggestions(request: SuggestionRequest):
    try:
        results = bm25.suggest(
            query=request.query,
            top_k=request.top_k
        )

        return SuggestionResponse(
            query=request.query,
            suggestions=results
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))