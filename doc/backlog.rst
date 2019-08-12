################
discodoc backlog
################

Prio 1
======
- [x] Obtain output format from commandline
- [x] Check paging re. multiple posts
- [o] Resolve format <=> formatter intertwingulation
- [o] Slides: beamer, reveal.js
- [o] Multi-topic acquisition
- [o] Obtain title from command line

Prio 2
======
- [o] Obtain and propagate metadata suitable for pandoc from Discourse
- [o] Obtain and propagate more Discourse topic metadata into document (visually and metadata)
- [o] Obtain PANDOC_OPTIONS from environment
- [o] Topic download progress bar
- [o] Select specific posts per single topic
- [o] Select specific posts across multiple topics

Prio 3
======
- [o] Select style: document, conversation, etc.
- [o] Style "conversation"
    - Print author names and post metadata
    - Add separators between single posts
- [o] Currently, fetching is limited to 1000 posts per topic.
  Fetch all posts by iterating through them, see https://github.com/pfaffman/discourse-downloader/blob/7be37ea26eb1d81a961a085a126e09c7a8d4a7cf/discourse-downloader#L111
