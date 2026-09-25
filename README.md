# Python LangChain lessons

All 21 executable JavaScript examples have Python equivalents. Lesson numbers are
preserved; Python files and subpackages use snake_case names.

## Setup

Python 3.11 or newer is required. From this project directory:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e .
```

The editable install lets you run examples as modules or by their file paths.
Select `.venv/bin/python` as your interpreter in your editor.
`requirements.txt` lists the dependencies actually used by these lessons.
`requirements-lock.txt` records the versions verified during migration.
To reproduce those versions, install it before the editable project:

```bash
python -m pip install -r requirements-lock.txt
python -m pip install -e .
```

Your existing `.env` is preserved. For a new checkout, copy `.env.example` to
`.env` and fill in the relevant credentials. Never overwrite an existing `.env`
with the empty example. Shared configuration is in `common/config.py`.

- OpenRouter: `OPENROUTER_API_KEY` or your existing `OPEN_ROUTER_API_KEY`.
- Chat model: `OPENROUTER_MODEL` (default `qwen/qwen3-8b`).
- Embeddings: `OPENROUTER_EMBEDDING_MODEL` (default `openai/text-embedding-3-large`).
- Hugging Face: `HUGGINGFACEHUB_API_TOKEN` or `HF_TOKEN`; optionally `HUGGINGFACE_MODEL`.

Models must be available to your provider account. API examples make billable
network requests when run; importing modules does not make requests. No keys are
embedded in Python source. Hosted Hugging Face chat uses its compatible endpoint,
so local transformers and model downloads are unnecessary.

## Run examples

```bash
source .venv/bin/activate
python -m video3.llms.llm_demo
python -m video3.chat_models.huggingface_api
python -m video3.embedding_models.document_similarity
python -m video4.dynamic_prompt
python -m video4.message
python -m video5.structured_output
python -m video6.structured_output_parser
python -m video7.simple_chain
python -m video7.sequential_chain
python -m video7.parallel_chain
python -m video7.conditional_chain
```

The chatbot accepts `exit`, Ctrl-D, or Ctrl-C. Simple and sequential chains ask
for input. JSON extraction returns null for missing facts; it does not pretend
to search the internet without a search tool.

Local document loading needs no API credentials:

```bash
python -m video10.text_loader --load-only
python -m video10.document_loader
python -m video10.directory_loader
```

Text summarization makes a model request:

```bash
python -m video10.text_loader
```

Each loader accepts an optional file or directory path:

```bash
python -m video10.document_loader "Ashish_resume.pdf"
python -m video10.directory_loader "/path/to/documents" --recursive
python -m video10.text_loader "/path/to/document.txt" --load-only
```

Default paths are relative to the project files, not your terminal's working
directory. Explicit relative arguments are relative to the working directory.
The directory loader reads only PDFs directly in the project root by default.
It skips dependency folders when recursion is enabled. PDF output contains one
Document per page; text is available as `document.page_content`.

## Layout

```text
common/config.py            Shared environment and model setup
video3/llms/                Basic model invocation
video3/chat_models/         Hosted Hugging Face chat
video3/embedding_models/    Single/multiple embeddings and similarity
video4/                     Prompts, messages, history, and streaming
video5/                     Pydantic structured output
video6/                     String, JSON, and Pydantic output parsers
video7/                     Simple, sequential, parallel, conditional chains
video10/                    Text, PDF, and directory loaders
tests/                      Offline migration regression tests
```

PDFs, the essay, and existing text reference notes remain in their original
locations. The reference notes may still describe JavaScript syntax; see
`PYTHON_GUIDE.md` for Python equivalents. Original executable JavaScript files,
Node package manifests, and node_modules are removed after verification.

## Verify without API calls

```bash
python -m unittest discover -s tests -v
python -m pip check
```

Tests exercise document contents and metadata, PDF recursion, typed parsers,
conditional routing, parallel outputs, sequential input flow, history, and
embedding ranking with local data or fake models. Live provider authentication,
model availability, and model-generated factual accuracy are not tested.

## File migration map

| Original JavaScript | Python replacement |
| --- | --- |
| `video3/1.LLMS/1.llmDemo.js` | `video3/llms/llm_demo.py` |
| `video3/2.ChatModels/1.HuugingFaceAPI.js` | `video3/chat_models/huggingface_api.py` |
| `video3/3.EmbeddedModels/1.Embedding.js` | `video3/embedding_models/embedding.py` |
| `video3/3.EmbeddedModels/2.MultipleEmbedding.js` | `video3/embedding_models/multiple_embedding.py` |
| `video3/3.EmbeddedModels/3.DocSimilarity.js` | `video3/embedding_models/document_similarity.py` |
| `video4/DynamicPrompt.js` | `video4/dynamic_prompt.py` |
| `video4/DynamicMessage.js` | `video4/dynamic_message.py` |
| `video4/TypesOfMessage.js` | `video4/types_of_message.py` |
| `video4/Message.js` | `video4/message.py` |
| `video4/MessagePlaceholder.js` | `video4/message_placeholder.py` |
| `video5/structureOP.js` | `video5/structured_output.py` |
| `video6/json-parser.js` | `video6/json_parser.py` |
| `video6/string-output.js` | `video6/string_output.py` |
| `video6/Structured-output-parser.js` | `video6/structured_output_parser.py` |
| `video7/simpleChain.js` | `video7/simple_chain.py` |
| `video7/sequentialChain.js` | `video7/sequential_chain.py` |
| `video7/conditionalChain.js` | `video7/conditional_chain.py` |
| `video7/parallelChain.js` | `video7/parallel_chain.py` |
| `video10/textLoader.js` | `video10/text_loader.py` |
| `video10/documentLoader.js` | `video10/document_loader.py` |
| `video10/directoryLoader.js` | `video10/directory_loader.py` |
