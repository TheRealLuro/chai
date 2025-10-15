# Project: Chai (Chat + AI)

This repository contains the source code for the "Chai" command-line AI chat application, developed as part of the DBT230 course.

## Author

**Name:** Jason Kwiatkowski

## Lab 1: Flat-File Persistence

This lab focuses on building the foundational persistence layer using a simple flat-file (JSON) system. The goal is to establish a performance baseline for file I/O operations, which will serve as a benchmark for subsequent labs involving more advanced database technologies.


## What are two different designs you contemplated for your multiple conversations implementation?

i contemplated using just a single json file and storing the conversations in an array or list, then itterating them. but I ended up doing single json files per convo and then I just iterated over all the files in the user_id folder then getting the chats and listing them.


## A vibe coder wants to make a quick MVP (minimum viable product) over the weekend that handles chat threads with AI models. Do you recommend using JSON files for persistence? Why?

Yeah I would say so, does the job and it is easy to do over a weekend. however if it is an actual product I would say no.


## You are interviewing at OpenAI. The interviewer asks if you would use raw JSON files to store user chats or if you would use a database or other form of persistence and to explain your choice. How would you reply?

data base just from experience using json files, because they can get corrupted and then everything goes bad. And if you use a database its just more secure clean and overall better in my opinion, plus you can use the database for other things for the data.


## What did you notice about performance using this file storage method?
uses quite a bit of power to read the file then update and yeah, if the chats get londer it would be slow.
