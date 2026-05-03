class PromptBuilder:

    def build_prompt(
        self,
        query,
        role,
        perspective,
        context_package
    ):

        system_prompt = self._system_prompt(role)

        context_block = self._context_block(context_package)

        instructions = self._instructions()

        prompt = f"""
SYSTEM ROLE
{system_prompt}

CONTEXT
{context_block}

INSTRUCTIONS
{instructions}

QUESTION
{query}
"""

        return prompt


    def _system_prompt(self, role):

        if role == "trusted_advisor":
            return (
                "You are a trusted advisor for insurance regulation "
                "and technology governance."
            )

        return "You are a professional consulting assistant."


    def _context_block(self, context_package):

        blocks = []

        for chunk in context_package.chunks:

            blocks.append(
                f"""
SOURCE: {chunk.doc_id}
CHUNK: {chunk.chunk_id}

{chunk.text}
"""
            )

        return "\n---\n".join(blocks)


    def _instructions(self):

        return """
Use only the information provided in the context.

Do not invent facts.

If the context does not contain enough information,
state that the answer cannot be determined.

Distinguish clearly between regulatory sources
and advisory interpretation.
"""