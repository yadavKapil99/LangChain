"""Verify migrated lessons locally, without provider API requests."""
import importlib
import io
import json
import pkgutil
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch

from langchain_core.language_models.fake_chat_models import FakeListChatModel
from langchain_core.runnables import RunnableLambda
from pydantic import ValidationError
from pypdf import PdfWriter

from common.config import PROJECT_ROOT
from video3.embedding_models.document_similarity import cosine_similarity, rank_documents
from video4.message_placeholder import prompt_template
from video6.structured_output_parser import parser
from video7.conditional_chain import build_chains as conditional_chains
from video7.parallel_chain import build_chains as parallel_chains
from video7.sequential_chain import build_chain
from video10.directory_loader import load_directory
from video10.document_loader import load_pdf
from video10.text_loader import load_text


class LessonTests(unittest.TestCase):
    def test_all_modules_import_without_network(self):
        with patch("socket.socket.connect", side_effect=AssertionError("Network access during import")):
            for package_name in ("common", "video3", "video4", "video5", "video6", "video7", "video10"):
                package = importlib.import_module(package_name)
                for module in pkgutil.walk_packages(package.__path__, package_name + "."):
                    with self.subTest(module=module.name):
                        importlib.reload(importlib.import_module(module.name))

    def test_text_loader_preserves_essay(self):
        path = PROJECT_ROOT / "video10/textFile.txt"
        docs = load_text(path)
        self.assertEqual(len(docs), 1)
        self.assertEqual(docs[0].page_content, path.read_text())
        self.assertEqual(docs[0].metadata["source"], str(path))

    def test_pdf_loader_page_metadata(self):
        path = PROJECT_ROOT / "Ashish_resume.pdf"
        docs = load_pdf(path)
        self.assertTrue(docs)
        self.assertTrue(any(doc.page_content.strip() for doc in docs))
        self.assertEqual([doc.metadata["page"] for doc in docs], list(range(len(docs))))
        self.assertTrue(all(doc.metadata["source"] == str(path) for doc in docs))

    def test_directory_recursion_and_exclusions(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for relative in ("top.pdf", "nested/inner.pdf", ".venv/skip.pdf", "node_modules/skip.pdf"):
                path = root / relative
                path.parent.mkdir(parents=True, exist_ok=True)
                writer = PdfWriter()
                writer.add_blank_page(width=72, height=72)
                writer.write(path)
            (root / "ignore.txt").write_text("Not a PDF")
            self.assertEqual(len(load_directory(root)), 1)
            recursive = load_directory(root, recursive=True)
            self.assertEqual(len(recursive), 2)
            self.assertEqual({Path(doc.metadata["source"]).name for doc in recursive}, {"top.pdf", "inner.pdf"})

    def test_missing_file_reports_failure(self):
        with self.assertRaises((RuntimeError, FileNotFoundError)):
            load_text(PROJECT_ROOT / "does-not-exist.txt")

    def test_structured_parser_validates_types(self):
        result = parser.invoke('{"name":"Rahul", "age":25, "profession":"Engineer", "skills":["Python"]}')
        self.assertEqual(result.age, 25)
        self.assertEqual(result.skills, ["Python"])
        from langchain_core.exceptions import OutputParserException
        with self.assertRaises(OutputParserException):
            parser.invoke('{"name":"Rahul", "age":"unknown", "profession":"Engineer", "skills":[]}')

    def test_person_schema_nested_and_nullable_fields(self):
        from video5.structured_output import Person
        data = dict(name="Example", age=25, skills=["batting"], stats=dict(matches=1, runs=20, wickets=0),
                    best_performance=None, last_data_update="2026-09-24", is_ready_for_captaincy=False,
                    is_bowler="neg", pros=["teamwork"], cons=[])
        self.assertEqual(Person(**data).stats.runs, 20)
        with self.assertRaises(ValidationError):
            Person(**{**data, "is_bowler": "maybe"})

    def test_history_placeholder_preserves_order(self):
        from langchain_core.messages import HumanMessage, AIMessage
        history = [HumanMessage(content="Earlier question"), AIMessage(content="Earlier answer")]
        messages = prompt_template.format_messages(userRole="travel", chatHistory=history, userInput="Follow-up")
        self.assertEqual([message.type for message in messages], ["system", "human", "ai", "human"])
        self.assertEqual(messages[1:3], history)
        self.assertEqual(messages[-1].content, "Follow-up")

    def test_sequential_chain_passes_report_to_second_prompt(self):
        prompts = []
        def respond(prompt):
            prompts.append(prompt.to_string())
            return "Detailed report about India" if len(prompts) == 1 else "Five bullet summary"
        result = build_chain(RunnableLambda(respond)).invoke({"text": "India"})
        self.assertEqual(result, "Five bullet summary")
        self.assertIn("India", prompts[0])
        self.assertIn("Detailed report about India", prompts[1])

    def test_conditional_classification_and_both_routes(self):
        classifier, _ = conditional_chains(FakeListChatModel(responses=[" Positive \n"]))
        self.assertEqual(classifier.invoke({"text": "Great!"}), "positive")
        _, branch = conditional_chains(RunnableLambda(lambda prompt: prompt.to_string()))
        self.assertIn("friendly positive", branch.invoke({"text": "Great!", "classification": "positive"}))
        self.assertIn("empathetic", branch.invoke({"text": "Broken!", "classification": "negative"}))
        self.assertIn("friendly positive", branch.invoke({"text": "Hello", "classification": "unknown"}))

    def test_parallel_and_merge_chains(self):
        def respond(prompt):
            text = prompt.to_string()
            if "Generate short" in text:
                return "India notes"
            if "Generate 5 MCQs" in text:
                return json.dumps({"questions": [{"question": "Example?", "options": ["A) One"], "answer": "A"}]})
            self.assertIn("India notes", text)
            self.assertIn("Example?", text)
            return json.dumps({"notes": "India notes", "questions": []})
        parallel, merge = parallel_chains(RunnableLambda(respond))
        result = parallel.invoke({"text": "India"})
        self.assertEqual(result["notes"], "India notes")
        self.assertEqual(result["mcqs"]["questions"][0]["answer"], "A")
        final = merge.invoke({"notes": result["notes"], "mcqs": json.dumps(result["mcqs"])})
        self.assertEqual(final["notes"], "India notes")

    def test_embedding_ranking_and_zero_vectors(self):
        self.assertAlmostEqual(cosine_similarity([1, 0], [1, 0]), 1)
        self.assertEqual(cosine_similarity([0, 0], [1, 2]), 0)
        self.assertAlmostEqual(cosine_similarity([1, 0], [-1, 0]), -1)
        result = rank_documents([1, 0], ["different", "similar"], [[0, 1], [1, 0]])
        self.assertEqual(result[0]["document"], "similar")
        with self.assertRaises(ValueError):
            cosine_similarity([1], [1, 2])

    def test_chatbot_exit_does_not_invoke_model(self):
        from video4 import message
        with patch.object(message, "chat_model") as factory, patch("builtins.input", return_value="exit"), redirect_stdout(io.StringIO()):
            message.main()
        factory.return_value.stream.assert_not_called()


if __name__ == "__main__":
    unittest.main()
