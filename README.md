#  EPCET Academic Regulation RAG Assistant

A Retrieval-Augmented Generation (RAG) based academic regulation assistant developed for **East Point College of Engineering & Technology (EPCET)**.

The system allows students to ask questions about academic regulations in natural language. Instead of relying only on the language model's general knowledge, the application retrieves relevant information from the official academic regulations document and uses it as context for generating the answer.

---

##  Project Overview

Academic regulations contain a large amount of information covering attendance, examinations, grading, promotion, eligibility, academic requirements, and other institutional rules.

Finding specific information manually in a lengthy regulations document can be time-consuming.

This project addresses that problem by implementing a **Retrieval-Augmented Generation pipeline**:

```text
User Question
      ↓
Semantic Search
      ↓
ChromaDB Vector Database
      ↓
Relevant Regulation Sections
      ↓
Gemini LLM
      ↓
Grounded Answer
      ↓
Answer + Retrieved Sources