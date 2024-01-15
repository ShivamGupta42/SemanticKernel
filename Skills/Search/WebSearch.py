class WebSearchEngineSkill:
    """
    A search engine skill.
    """

    from semantic_kernel.orchestration.sk_context import SKContext
    from semantic_kernel.skill_definition import sk_function

    def __init__(self, connector) -> None:
        self._connector = connector

    @sk_function(
        description="Perform web searches based on the provided statement",
        name="searchAsync",
        input_description="Search statement",
    )
    async def search_async(self, query: str) -> str:
        result = await self._connector.search_async(query, num_results=5, offset=0)
        return str(result)