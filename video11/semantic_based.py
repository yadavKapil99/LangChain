from langchain_openai import OpenAIEmbeddings
from langchain_experimental.text_splitter import SemanticChunker
from common.config import require_key


text = """
Farmers were looking hard in the fields for the first signs of spring. The snow had melted, and the ground was soft and wet. The farmers were eager to get back to work, but they knew that they had to be patient. They had to wait for the right time to plant their crops.

The farmers were also looking for signs of pests and diseases. They knew that if they didn't take care of their crops, they would not have a good harvest. They were determined to do everything they could to ensure that their crops would grow healthy and strong.

IPL is a professional Twenty20 cricket league in India, which is one of the most popular cricket leagues in the world. It was founded by the Board of Control for Cricket in India (BCCI) in 2008. The league features franchises representing different cities in India, and it attracts top players from around the world. The IPL has gained immense popularity due to its fast-paced format, exciting matches, and the involvement of international cricket stars. It has also contributed significantly to the growth of cricket in India and has become a major sporting event with a massive fan following.

Terrorism is a global issue that affects many countries around the world. It involves the use of violence and intimidation to achieve political, religious, or ideological goals. Terrorist groups often target civilians, government institutions, and infrastructure to create fear and disrupt societies. Governments and international organizations work together to combat terrorism through intelligence sharing, law enforcement, and counter-terrorism operations. The fight against terrorism requires a comprehensive approach that addresses the root causes of extremism and promotes peace and security.
"""


# OpenRouter Embedding Model
embeddings = OpenAIEmbeddings(
    model="openai/text-embedding-3-small",
    base_url="https://openrouter.ai/api/v1",
    api_key=require_key("OPENROUTER_API_KEY", "OPEN_ROUTER_API_KEY"),
)


# Semantic Text Splitter
text_splitter = SemanticChunker(
    embeddings=embeddings,
    breakpoint_threshold_type="standard_deviation",
    # breakpoint_threshold_amount=1,
    breakpoint_threshold_amount=0.8,
)


# Split text
chunks = text_splitter.split_text(text)


# Print results
print(f"Number of chunks: {len(chunks)}")

for i, chunk in enumerate(chunks):
    print(f"\n========== CHUNK {i + 1} ==========")
    print(chunk)