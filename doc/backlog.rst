################
discodoc backlog
################

Prio 1
======
- [x] Obtain output format from commandline
- [x] Check paging re. multiple posts
- [x] Resolve format <=> formatter intertwingulation
- [x] Check presentation/slide rendering: beamer, reveal.js
- [x] To respect privacy, skip all whisper posts when collecting cooked HTML fragments
- [x] Adjust margins of PDF document created through latex renderer
- [x] Multi-topic acquisition by obtaining multiple urls from the command line
- [o] Add "--enumerate" option to interpolate sequential number into output filename (prefix)
- [o] Add "--combine" option to combine content from multiple topics into single document

Prio 1.5
========
- [o] Add "--index-url" option to ask discodoc to fetch a list of content URLs to process
  from the designated posts on the referenced topic through the given index-url.
- [o] Obtain title from command line

Prio 2
======
- [o] Obtain and propagate metadata suitable for pandoc from Discourse
- [o] Optionally tag artefact by putting document revision and/or most recent edit date into output filename (suffix)
- [o] Obtain and propagate more Discourse topic metadata into document (visually and metadata)
- [o] Obtain PANDOC_OPTIONS from environment
- [o] Topic download progress bar
- [o] Select specific posts per single topic
- [o] Select specific posts across multiple topics
- [o] Obtain output-path from environment
- [o] Use pandoc's ``--request-header=`` option for propagating Discourse's ``Api-Key`` header?
- [o] Fold ``yarn install``'ed artefacts into release package to make it self-contained

Prio 3
======
- [o] Select style: document, conversation, etc.
- [o] Style "conversation"
    - Print author names and post metadata
    - Add separators between single posts
- [o] Currently, fetching is limited to 1000 posts per topic.
  Fetch all posts by iterating through them, see https://github.com/pfaffman/discourse-downloader/blob/7be37ea26eb1d81a961a085a126e09c7a8d4a7cf/discourse-downloader#L111
- [o] Control pandoc's ``--self-contained`` and ``--table-of-contents`` options individually
- [o] Add resource caching to speed up repeated invocations on top of the same data
- [o] Add "--allow-whisper" to override the default behavior of skipping whisper posts
