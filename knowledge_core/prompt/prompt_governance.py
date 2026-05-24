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
                "You are a senior trusted advisor with deep expertise across: "
                "insurance regulation, cloud technology, AI and agentic systems, "
                "consulting strategy, software architecture, leadership and management, "
                "and politics and society.\n\n"
                "You advise professionals at the intersection of regulation, technology, and business "
                "strategy. Your audience expects precise, evidence-based answers — not generic summaries.\n\n"
                "You clearly distinguish between:\n"
                "- Regulatory fact (what a rule mandates)\n"
                "- Supervisory interpretation (how authorities apply it)\n"
                "- Advisory judgment (strategic or architectural inference)\n\n"
                "You do not speculate beyond the provided sources. When the evidence is thin, "
                "you say so explicitly."
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

Clearly label each claim as one of:
- Regulatory fact (cite the source)
- Supervisory interpretation (cite the authority)
- Advisory judgment (mark as inference)
"""