import json
import re

import fitz

from src.config import PDF_PATH


CATEGORY_KEYWORDS = {
    "attendance": "attendance",
    "grade": "grading",
    "grading": "grading",
    "cgpa": "grading",
    "sgpa": "grading",
    "credit": "credits",
    "curriculum": "curriculum",
    "examination": "examinations",
    "cie": "examinations",
    "see": "examinations",
    "question paper": "examinations",
    "admission": "admissions",
    "lateral entry": "admissions",
    "withdrawal": "withdrawal",
    "termination": "withdrawal",
    "mentor": "student_support",
    "feedback": "student_support",
    "transfer": "transfer",
    "plagiarism": "examinations",
    "programme": "programme_structure",
    "semester": "programme_structure",
}


def guess_category(title, body):
    text = (title + " " + body[:300]).lower()

    for keyword, category in CATEGORY_KEYWORDS.items():
        if keyword in text:
            return category

    return "general"


TOP_SECTION_RE = re.compile(
    r"\n[ \t]*([1-9]|1[01])\.\s*\n?\s*([A-Z][A-Za-z /,&\-]{3,55})\s*:?\s*\n"
)

SUBSECTION_RE = re.compile(
    r"\n[ \t]*([1-9]|1[01])\.([1-9])\)\s*([A-Za-z][A-Za-z /,&\-:]{2,80})?"
)


class AcademicChunker:

    def __init__(self, pdf_path=PDF_PATH):
        self.pdf_path = pdf_path

    def extract_text(self):
        doc = fitz.open(self.pdf_path)

        pages = []

        for page in doc:
            pages.append(page.get_text())

        doc.close()

        return "\n".join(pages)

    def create_chunks(
        self,
        text,
        doc_version="2024-25",
        doc_name="EPCET Academic Regulations",
    ):

        matches = list(SUBSECTION_RE.finditer(text))

        chunks = []

        if matches:

            for i, match in enumerate(matches):

                start = match.start()

                end = (
                    matches[i + 1].start()
                    if i + 1 < len(matches)
                    else len(text)
                )

                section_number = f"{match.group(1)}.{match.group(2)}"

                title = (match.group(3) or "").strip().rstrip(":")

                body = text[start:end].strip()

                chunks.append(
                    {
                        "id": f"chunk_{len(chunks)+1}",
                        "section_number": section_number,
                        "section_title": title,
                        "text": body,
                        "category": guess_category(title, body),
                        "doc_version": doc_version,
                        "doc_name": doc_name,
                        "contains_table": "Table" in body,
                    }
                )

        top_matches = list(TOP_SECTION_RE.finditer(text))

        covered = {c["section_number"] for c in chunks}

        for i, match in enumerate(top_matches):

            sec_num = match.group(1)

            if any(c.startswith(sec_num + ".") for c in covered):
                continue

            start = match.start()

            end = (
                top_matches[i + 1].start()
                if i + 1 < len(top_matches)
                else len(text)
            )

            title = match.group(2).strip()

            body = text[start:end].strip()

            if len(body) < 20:
                continue

            chunks.append(
                {
                    "id": f"chunk_{len(chunks)+1}",
                    "section_number": sec_num,
                    "section_title": title,
                    "text": body,
                    "category": guess_category(title, body),
                    "doc_version": doc_version,
                    "doc_name": doc_name,
                    "contains_table": "Table" in body,
                }
            )

        chunks.sort(
            key=lambda c: [int(x) for x in c["section_number"].split(".")]
        )

        return chunks

    def process(self):

        text = self.extract_text()

        chunks = self.create_chunks(text)

        return chunks

    def save(self, output_path):

        chunks = self.process()

        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(chunks, f, indent=2, ensure_ascii=False)

        return chunks


if __name__ == "__main__":

    chunker = AcademicChunker()

    chunks = chunker.process()

    print(f"\nTotal Chunks : {len(chunks)}\n")

    for chunk in chunks:
        print(
            f"{chunk['section_number']} - {chunk['section_title']} ({chunk['category']})"
        )