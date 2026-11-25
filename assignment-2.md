# Assignment 2

## 1. Self-assessment

| Area | Rating |
| --- | --- |
| LLMs | B |
| Deep Learning | B |
| AI | B |
| Machine Learning | B |

B means I can code under supervision.

## 2. How I would build an LLM chatbot

1. **Chat UI and authentication.** The user signs in and receives an authentication token. The backend validates the token to identify the user and lists the conversations they can access. Each conversation has a thread ID. When the user selects a chat and sends a message, the backend checks their access to that thread and loads its recent messages.
2. **Prompt and retrieval.** The backend sends the system instructions, recent history, and new message as separate parts of the model input. I would give the new message the user role to keep it separate from system instructions. This helps preserve the instruction boundary, but prompt injection is still possible, so the backend should enforce access and tool permissions. If the question needs information from our documents, I would use a retrieval layer to fetch relevant passages from a vector database and add them to the context.
3. **LLM and tool calls.** The LLM generates a reply based on the prompt and the context. If it needs live information, the model can request one of the tools defined by the backend. The backend validates the request, calls the API, and sends the result back to the model so it can finish the reply.
4. **Streaming and history.** The backend streams the reply to the chat UI as it is generated. It stores the user message and the assistant's reply under the thread ID, with source links on the reply when it uses retrieved passages.

## 3. Vector databases and what I would choose

An embedding model turns text into a vector, which is a list of numbers. A vector might have 1,536 dimensions, depending on the model. A vector database stores these vectors and lets me look up similar ones. For text, I would use an embedding model suited to cosine similarity. I would embed the question with the same model as the documents and compare the angle between the vectors. A higher cosine similarity means the vectors point in more similar directions, so the passages are more likely to be relevant.

### Example: An internal IT support chatbot

Suppose a company has 500 employees and around 20,000 searchable passages across its IT help articles and PDFs. The problem is that employees ask questions in their own words, while the help articles use more specific terms. For example, someone might ask "I got a new phone and now I can't log in." The chatbot should find the article titled "Reset your multi-factor authentication device," answer from the relevant passage, and link to the article.

I would start with **PostgreSQL and pgvector**, assuming the company already uses PostgreSQL. When a document is added or updated, I would split it into passages and store each passage with its embedding, source link, and access metadata. At query time, I would search passages the user is allowed to access, rank them by cosine similarity, and send the top results to the LLM.

### How I would choose an index as usage grows

I would use the number of active users to estimate peak concurrent searches and queries per second. I would also look at the number and dimensions of the vectors, the available memory, and how fresh the results need to be. A small corpus can still get heavy traffic, and a large corpus can make searches expensive even with few users. For the example above, I would start with exact search and measure latency under expected traffic before adding an approximate index.

| Approach | How it works and when I would use it |
| --- | --- |
| **HNSW** (Hierarchical Navigable Small World) | Builds a graph of nearby vectors and follows its links to find good matches. I'd test it when the corpus or traffic grows and I need fast searches with high recall. It generally uses more memory and takes longer to build than IVFFlat. |
| **IVFFlat** (inverted file with full vectors) | Groups vectors into clusters and only searches the clusters closest to the query. I'd test it when the corpus grows and memory or index build time matters. Probing more clusters can improve recall at the cost of slower searches. |
| **PQ** (product quantization) | Splits each vector into parts and encodes each part with a short code. I'd look at an index such as IVF-PQ if the corpus gets large enough that keeping full vectors in the search index costs too much memory. Compression can change the ranking, so I'd measure recall against exact search and consider reranking the best candidates using full vectors. IVF-PQ would require a search engine or library that supports it, such as Faiss. |

I would make the final choice by comparing search latency, memory use, and how many of the exact top results each approximate index still returns.

[pgvector indexing documentation](https://github.com/pgvector/pgvector#indexing) · [Faiss product quantization documentation](https://github.com/facebookresearch/faiss/wiki/Faiss-indexes#indexes-based-on-product-quantization-codes)
