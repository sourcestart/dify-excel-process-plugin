from pathlib import Path

from dify_plugin.core.runtime import Session
from dify_plugin.entities.tool import ToolRuntime
from dify_plugin.file.entities import FileType
from dify_plugin.file.file import File

from tools.excel_extractor import ExcelExtractorTool


def main() -> None:
    file_path = Path("test.xls")
    if not file_path.exists():
        raise SystemExit("test.xls not found in project root")

    blob = file_path.read_bytes()

    excel_file = File(
        url="file://test.xls",
        filename="test.xls",
        mime_type="application/vnd.ms-excel",
        size=len(blob),
        type=FileType.DOCUMENT,
    )

    # manually inject blob so ExcelExtractorTool can read content without HTTP
    excel_file._blob = blob

    runtime = ToolRuntime(credentials={}, user_id="debug-user", session_id="debug-session")
    session = Session.empty_session()
    tool = ExcelExtractorTool(runtime=runtime, session=session)

    # ExcelExtractorTool._invoke is a generator of ToolInvokeMessage
    for message in tool.invoke({"excel_content": excel_file}):
        print("message type:", getattr(message, "type", None))
        if getattr(message, "type", None) == "text":
            text = getattr(message, "data", "")
            print("TEXT:\n", text[:500], "...\n")
        elif getattr(message, "type", None) == "blob":
            meta = getattr(message, "meta", {}) or {}
            print("BLOB:", meta.get("file_name"), meta.get("mime_type"))


if __name__ == "__main__":
    main()
