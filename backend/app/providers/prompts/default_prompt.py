from .base import BasePrompt
from app.schemas.search_response import SearchResponse

class DefaultPrompt(BasePrompt):

    def __init__(self) -> None:
        self.system_prompt = """
        You are a highly precise and objective AI assistant. Your core mission is to answer user queries using the provided context.

        ### STRICT OPERATIONAL BOUNDARIES
        1. Answer the user's query using ONLY the provided context.
        2. If the context does not contain the answer, reply exactly:
        "I cannot find the answer in the provided documents."
        3. Never invent facts, links, code, dates, or information.
        4. If multiple context blocks contain relevant information, combine them into a single coherent answer.
        5. Do not infer benefits or conclusions that are not explicitly stated in the provided context.

        ### OUTPUT FORMATTING
        - Use Markdown.
        - Use bullet points when appropriate.
        - Cite the document name at the end of the response when the answer is based on the provided context.
        """

    @property
    def name(self) -> str:
        return "default"

    @property
    def version(self) -> str:
        return "1.0"

    @property
    def description(self) -> str:
        return "Default enterprise RAG prompt."

    async def build(
            self,
            question: str,
            search_response: SearchResponse,
        ) -> str:

            context: list[str] = []

            for item in search_response.results:
                context.append(
                    f"""### DOCUMENT
                Document: {item.document_name}
                Chunk: {item.chunk_index}

                {item.content}

                ---"""
                )

            return f"""{self.system_prompt}

    ### CONTEXT

    {'\n\n'.join(context)}

    ### CHAT HISTORY

    None

    ### USER QUERY

    {question}

    Assistant:"""