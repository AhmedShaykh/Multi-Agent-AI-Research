from agents import build_reader_agent, build_search_agent, writer_chain, critic_chain;

def run_research_pipeline(topic: str) -> dict:

    state = {};

    print("\n" + " =" * 50);

    print("Step 1: Search Agent Is Working ...");

    print("=" * 50);

    search_agent = build_search_agent();

    search_result = search_agent.invoke({
        "messages": [("user", f"Find Recent, Reliable & Detailed Information About: {topic}")]
    });

    state["search_results"] = search_result["messages"][-1].content;

    print("\n Search Result: ", state["search_results"]);

    print("\n" + " =" * 50);

    print("Step 2: Reader Agent Is Scraping Top Resources ...");

    print("=" * 50);

    reader_agent = build_reader_agent();

    reader_result = reader_agent.invoke({
        "messages": [("user", f"""
        
    Based on the following search results about **{topic}**, pick the most relevant URL and scrape it for deeper content.

    Search Results:

    {state["search_results"][:800]}

    """
    
    )]});

    state["scraped_content"] = reader_result["messages"][-1].content;

    print("\n Scraped Content: \n", state["scraped_content"]);

    print("\n" + " =" * 50);

    print("Step 3: Writer Is Drafting The Report ...");

    print("=" * 50);

    research_combined = (f"""
        
        SEARCH RESULTS:
        
        {state["search_results"]}


        DETAILED SCRAPED CONTENT:
        
        {state["scraped_content"]}
        
        """);

    state["report"] = writer_chain.invoke({
        "topic": topic,
        "research": research_combined
    });

    print("\n Writer Report\n", state["report"]);

    print("\n" + " =" * 50);

    print("Step 4: Critic Is Reviewing The Report ...");

    print("=" * 50);

    state["feedback"] = critic_chain.invoke({
        "report": state["report"]
    });

    print("\n Critic Report \n", state["feedback"]);

    return state;

if __name__ == "__main__":

    topic = input("\n Enter A Research Topic: ");

    run_research_pipeline(topic);