# Project: Chai (Chat + AI)

This repository contains the source code for the "Chai" command-line AI chat application, developed as part of the DBT230 course.

## Author

**Name:** Jason Kwiatkowski

## Lab 2: Questions

## Question 1: Performance Analysis (5 points)
Run performance_test.py and record the results. What did you observe about:
📊 KEY FINDINGS:

1. INCREMENTAL APPENDS (Real-time Chat):
   ----------------------------------------------------------------------------
   At 10 messages:  Flat File is 97.73x faster
   At 100 messages: Flat File is 110.77x faster
   • Flat File @ 10 msgs:  1.45ms per append
   • MongoDB @ 10 msgs:    141.96ms per append
   • Flat File @ 100 msgs: 1.39ms per append
   • MongoDB @ 100 msgs:   153.51ms per append

   Analysis:
   • Flat files are surprisingly fast for small conversations
   • MongoDB has network/TCP overhead even when running locally
   • JSON parsing and file I/O are highly optimized in modern systems
   • At 100 messages, flat file performance degrades (0.95x slower)
   • MongoDB stays more consistent (1.08x slower)

2. SCALING CHARACTERISTICS:
   ----------------------------------------------------------------------------
   When conversation grows 10x (from 10 to 100 messages):
   • Flat File slows down by: 0.95x
   • MongoDB slows down by:   1.08x

   ✓ Both systems scale similarly at this size

3. BULK WRITES (Import/Migration):
   ----------------------------------------------------------------------------
   Flat File is 17.07x FASTER for bulk operations
   • Flat File @ 1000 msgs: 0.0162s
   • MongoDB @ 1000 msgs:   0.2758s
   • Why: Single large write favors flat files' simple write model
           Network overhead and document parsing add cost to MongoDB

4. COLD START (Initial Setup):
   ----------------------------------------------------------------------------
   Flat File is 487.03x FASTER for cold starts
   • Flat File: 0.0019s
   • MongoDB:   0.9375s
   • Why: Flat files have zero setup; MongoDB requires connection
           and index creation

5. READ PERFORMANCE (Loading Conversation):
   ----------------------------------------------------------------------------
   Flat File is 13729.95x FASTER for reading full conversations
   • Flat File @ 100 msgs: 0.03ms
   • MongoDB @ 100 msgs:   435.24ms
   • Note: Both are fast; difference is network vs disk I/O


================================================================================
FLAT FILE ADVANTAGES:
================================================================================
✓ Simplicity: Zero infrastructure, no setup required
✓ Cold Starts: Instant initialization, no connection overhead
✓ Small Scale: Faster than MongoDB for <50 message conversations
✓ Bulk Writes: Single large writes are efficient
✓ Portability: Plain JSON files work everywhere
✓ Debugging: Easy to inspect and edit files manually
✓ Cost: Completely free, no hosting or service costs
✓ Version Control: Can commit data files to Git
✓ No Network: Pure disk I/O avoids TCP/connection overhead

❌ Disadvantages:
  • Incremental updates require full file rewrite (O(n) operation)
  • Performance degrades as conversations grow (0.95x slower at 100 msgs)
  • No atomic operations (risk of corruption on crashes)
  • No indexing or query capabilities
  • File system limits (~10,000 files per directory)
  • Concurrent access is problematic
  • Will become significantly slower at 500+ messages

================================================================================
MONGODB ADVANTAGES:
================================================================================
✓ Scalability: Performance stays more consistent as data grows
✓ Better Scaling: Only 1.08x slower at 10x data (vs 0.95x for files)
✓ Indexing: Fast lookups across millions of documents
✓ Queries: Flexible search and aggregation capabilities
✓ Concurrency: Built-in handling of simultaneous access
✓ Atomic Operations: Guaranteed consistency with $push
✓ Replication: Built-in backup and high availability
✓ Advanced Features: Transactions, change streams, aggregations
✓ Production Ready: Handles millions of users

❌ Disadvantages:
  • Setup Complexity: Requires server installation or cloud account
  • Network Overhead: 142.0ms even for simple operations locally
  • Slower for Small Data: 97.73x slower than files for tiny conversations
  • Resource Usage: Requires memory and CPU for database server
  • Cost: Cloud hosting costs for production (~$57/month for M10)
  • Learning Curve: More complex than simple file I/O

================================================================================
THE SURPRISING TRUTH:
================================================================================

For this lab's use case (local development, small conversations),
flat files are actually FASTER than MongoDB!

This demonstrates an important principle in database design:
  'Use the simplest tool that meets your requirements'

However, the story changes as we scale...

================================================================================
WHEN TO USE EACH:
================================================================================

USE FLAT FILES WHEN:
  • Building a quick prototype or MVP (faster development)
  • Single-user application on local machine
  • Small data volume (<100 conversations, <200 messages each)
  • Infrequent updates (batch processing)
  • Need to version control your data
  • Zero infrastructure preferred
  • Want maximum speed for small-scale operations

USE MONGODB WHEN:
  • Conversations will grow to 500+ messages (scaling matters)
  • Multiple users or concurrent access needed
  • Need to search across conversations
  • Building a production application
  • Expect to scale beyond a few thousand records
  • Need data consistency guarantees (atomic operations)
  • Want to add features like: search, analytics, recommendations
  • Planning for horizontal scaling (sharding)

## How append times changed as the number of messages grew for flat files vs MongoDB?
Mongo got slower the more thing were added, which it stayed around 100+ ms and flat file stayed about the same at 1+-ms.Additionally, the more the data grew the slower it got obviously.

## The difference in read times for retrieving the full conversation?

The difference was pretty crazy, but its understandable. because the flat file stored the data on the device so it is device to device. mongo on the other hand was device to network to server then bounce back.

## Question 2: Atomic Operations (5 points)
In MongoDBManager, we use the $push operator in append_message(). Research what "atomic operations" means in the context of databases. Why is this important for a chat application where multiple messages might be added rapidly?

When I looked it up i found that it is an operation that completes entirely or it doesnt with no intermediate states being visible to other operations. It allows for better consisency. Its important in chat apps because there are many users doing a bunch of things at the same time. so $push makes it atomical.

## Question 3: Scalability (5 points)
Imagine your chat application goes viral and now has 1 million users, each with an average of 10 conversation threads containing 500 messages each.

Compare how FlatFileManager and MongoDBManager would handle:

Finding all threads for a specific user
Loading a specific conversation
Storage organization and file system limits

In everyway mongo would be the better choice because we can query instead of iterating over everything. We can fetch by ID. we dont have any filesystem limits. and it just scales better. From what I found and researched.

Question 4: Data Modeling Design Challenge (5 points)
Currently, each conversation is stored as a single document with an embedded array of messages:

{
  "_id": "user_123_work",
  "messages": [...]
}
An alternative design would be to store each message as its own document:

{
  "_id": "msg_001",
  "conversation_id": "user_123_work",
  "role": "user",
  "content": "Hello!",
  "timestamp": "..."
}
Describe:

One advantage of the embedded messages design (what we currently use)

One advantage with the embedded messages design is that its simpler. One document contains everything we need. So we make less queries to the server so we can display the full chat faster.

One advantage of the separate message documents design

However with a separate message design its easier to index messages by info in the messages. and we can limit the size so we dont have to cut off conversations.

A scenario where you would choose the separate 
messages design instead

As i wrote above, we would just use it for that reason or reasons. 

