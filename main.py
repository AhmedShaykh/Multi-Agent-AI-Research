from fastapi import FastAPI, HTTPException;
from pipeline import run_research_pipeline;
from pydantic import BaseModel;
import uvicorn;

app = FastAPI(
    title="AI Research Assistant",
    description="Multi Agent AI Research Assistant",
    version="1.0.0",
);

class ResearchRequest(BaseModel):
    topic: str;

@app.post("/research", tags=["research"])
def research(request: ResearchRequest):

    try:

        result = run_research_pipeline(request.topic);

        return {
            "topic": request.topic,
            "search_results": result["search_results"],
            "scraped_content": result["scraped_content"],
            "report": result["report"],
            "feedback": result["feedback"]
        };

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        );

if __name__ == "__main__":
    uvicorn.run(app, host = "localhost", port = 8000);