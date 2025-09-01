import openai
from typing import List
import tiktoken

class LLMSummarizer:
    def __init__(self, api_key: str, model: str = "gpt-3.5-turbo"):
        openai.api_key = api_key
        self.model = model
        self.encoding = tiktoken.encoding_for_model(model)

    def summarize_text(self, text: str, summary_type: str = "chapter") -> str:
        """Summarize text using LLM"""

        # Chunk text if too long
        chunks = self._chunk_text(text, max_tokens=3000)

        if len(chunks) == 1:
            return self._summarize_chunk(chunks[0], summary_type)
        else:
            # Summarize each chunk then create final summary
            chunk_summaries = []
            for chunk in chunks:
                summary = self._summarize_chunk(chunk, "section")
                chunk_summaries.append(summary)

            # Create final summary from chunk summaries
            combined = "\n\n".join(chunk_summaries)
            return self._summarize_chunk(combined, summary_type)

    def _chunk_text(self, text: str, max_tokens: int = 3000) -> List[str]:
        """Split text into chunks that fit within token limits"""
        sentences = text.split('. ')
        chunks = []
        current_chunk = ""

        for sentence in sentences:
            test_chunk = current_chunk + ". " + sentence if current_chunk else sentence

            if len(self.encoding.encode(test_chunk)) <= max_tokens:
                current_chunk = test_chunk
            else:
                if current_chunk:
                    chunks.append(current_chunk)
                current_chunk = sentence

        if current_chunk:
            chunks.append(current_chunk)

        return chunks

    def _summarize_chunk(self, text: str, summary_type: str) -> str:
        """Summarize a single chunk of text"""

        prompts = {
            "chapter": "Summarize this chapter in a clear, engaging way suitable for audio narration. Focus on key plot points, character development, and important themes:",
            "section": "Provide a concise summary of this text section, highlighting the main ideas and important details:",
            "book": "Create a comprehensive summary of this book content, capturing the essential narrative, themes, and key insights:"
        }

        response = openai.ChatCompletion.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "You are an expert at creating clear, engaging summaries for audiobook narration."},
                {"role": "user", "content": f"{prompts.get(summary_type, prompts['section'])}\n\n{text}"}
            ],
            max_tokens=500,
            temperature=0.7
        )

        return response.choices[0].message.content
