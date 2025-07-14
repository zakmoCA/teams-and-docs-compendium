# RAG Agent for Company Docs/Teams-Meetings Contents 

Designing as an internal Company tool alongside an [N8N workflow/automation](https://n8n.io/) (chat-interface based), with potential expansion to include a client-facing web UI. In time it will function as a compendium of all internal company knowledge via a queryable chat-assistant to that end.

## Scope

This initial prototype will be entirely CLI-based. Also serves as my introduction to RAG and Agentic-Applications and will be the first such project. 

It can also be useful as a source of truth for the desired logic/functionality here which will have already been tried and tested + also being useful through n8n extensibility via transposing this projects logic into n8n code nodes/appropriate expressions and queries.


## Rationale

Potential for this code-native version to maybe have utility for company in future, but remains to be seen + will be maintaining development of both versions in parallel in any case. 

Building as RAG-capabilities for querying internal knowledge management systrems go brrr and will make life easier all round, simply put automation of this content curation/refinement and storage frees up time taken to do so manually in addition to marked efficiency gains in retrieval of relevant information.

And not least of all because because *text is the universal interface,* and now bringing that to life via chat/agentic capabilities means any non-LLM based such system becomes in essence a deadweight loss in terms of potential team productivity, comparatively.


## Completed

- [x] MSAL device login (token caching)
- [x] Fetch calendar events with Graph API
- [x] Auto-scan all ms-teams meetings/chats
- [x] Download SharePoint-hosted teams attachments
- [x] Log meetings/chats names + download URLs

### RAG Pipeline
- [x] GPT summarisation of ingested docs
- [x] Chunk + embed with OpenAI models
- [x] In-memory vector store + GPT querying
- [x] Build/test basic query interface (`src/query_RAG.py`)

## In Progress

- [ ] Merge ms-teams content into unified RAG index
- [ ] Normalise attachment/meeting output flows

## Todos

### Meeting Audio
- [ ] Locate/download ms-teams recordings
- [ ] Transcribe (maybe Whisper)
- [ ] Parse to structured blocks

### RAG Pipeline
- [ ] Full pipeline hooked up: ms-teams → meetings-transcript → summaries → chunks → embeddings
- [ ] Proper index store (Pinecone maybe)
- [ ] Natural language query interface (CLI or web-based)
- [ ] Implement analogous N8N workflows and deploy.


This project can potentially be further expanded/utilised even after the corresponding n8n-workflows are deployed.
- Continue development in parallel
- Preserve feature parity and extensibility between this codebase and the n8n workflows

## Current Functionality

### Ingestion

```bash
# running ingestion pipeline (extract + summarise + embed local docs)
$ python3 src/run_ingestion.py

📂 Found 3 documents in parsed_docs/
📝 Summarising: Company Executive Recruitment Case Study... # meetings chat
📝 Summarising: details.pdf... # my chats
📝 Summarising: Screenshot 2025-07-10 at 12.42.32 pm.png... # my chats
✅ Summaries saved to summarise/summaries/

🧠 Chunking and embedding summaries...
✅ Indexed 48 chunks into vector store
```


### Microsoft Graph Status/Summary Check

```bash
# ✅ run Microsoft Graph API general status checks for posterity
$ python3 src/api_clients.py

🔐 Go to https://microsoft.com/devicelogin and enter code: xxxx-xxxx # MSAL device login w/token-caching
✅ Calendar Events:
- Weekly Review (Entire Team) at 2025-03-21T05:00:00.0000000
✅ Recent Files: 5 items
✅ Presence Status: Available
✅ Recent Emails: 5 threads
✅ Online Meetings: 3 sessions
✅ Frequent Contacts: 5 people

✅ Microsoft Graph status check complete
```

### Download Teams Attachments

```bash
# 📎 running ms-teams attachments downloader module to download any attachments
$ python3 teams/attachments_downloader.py

🔐 Go to https://microsoft.com/devicelogin and enter code: xxxx-xxxx # MSAL device login w/token-caching
💬 Found 5 chats. Scanning for attachments...

🧵 Chat: Weekly Review (Entire Team)
📎 Downloaded: Company Executive Recruitment Case Study (1) 1.pdf

🧵 Chat: Company Updates & News
🧵 Chat: None
📎 Downloaded: details.pdf

🧵 Chat: Teams meeting
🧵 Chat: None
📎 Downloaded: Screenshot 2025-07-10 at 12.42.32 pm.png

✅ All attachments fetched.
```

### RAG Query Module (CLI-based)

```bash
# 🔍 run RAG query module ---> ask GPT questions in CLI about indexed content, in natural language
$ python3 src/query_RAG.py

🤖 Ask a question: What’s the latest update from the company? # my prompt

# 🔄🔍🔄 ...parses indexed docs knowledge-base under the hood...

📌 Summary: Company shared a new executive recruitment strategy and status update.......TBC. # prompt response output: brief description/summary of company updates from GPT etc

✅ Answer generated via GPT
```

## Tbc...