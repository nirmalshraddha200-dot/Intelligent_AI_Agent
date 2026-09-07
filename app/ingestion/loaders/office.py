import logfire
from unstructured.partition.docx import partition_docx
from unstructured.partition.pptx import partition_pptx


def parse_office(file_path: str):
    """Parse DOCX and PPTX files locally."""
    with logfire.span("Office Document Parsing", filename=file_path):
        try:
            if file_path.lower().endswith(".docx"):
                elements = partition_docx(filename=file_path)

            elif file_path.lower().endswith(".pptx"):
                elements = partition_pptx(filename=file_path)

            else:
                raise ValueError(f"Unsupported Office file: {file_path}")

            full_text = "\n".join(str(el) for el in elements)

            print(
                f"Parsed {file_path}: {len(full_text)} characters",
                flush=True
            )

            return full_text

        except Exception as e:
            print(f"Office Parse Failed: {e}", flush=True)
            logfire.error(f"Office Parse Failed: {e}")
            raise