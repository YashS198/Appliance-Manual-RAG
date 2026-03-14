# Appliance-Manual-RAG
Appliance Manual RAG is a simple AI assistant that helps users find information from appliance manuals. Instead of manually searching through long PDF manuals, users can ask questions and the system retrieves relevant sections from the manuals and generates answers using a language model.

Problem

Many people lose or struggle to navigate appliance manuals for devices such as espresso machines, air fryers, and microwave ovens. When an error code appears or a device stops working, users often search through long manuals or online forums to find solutions.

Solution

This project uses Retrieval-Augmented Generation (RAG) to read appliance manuals and answer questions based on the content of those manuals.

The system works by:
1. Loading appliance manuals in PDF format.
2. Extracting text from the manuals.
3. Splitting the text into smaller sections (chunks).
4. Finding the most relevant sections for a given question.
5. Sending the retrieved context to a language model to generate an answer.

Features
1. Works with multiple appliance manuals
2. Extracts information from PDF documents
3. Retrieves relevant manual sections
4. Generates answers based on manual content
5. Reduces hallucinations by grounding answers in documentation

Technologies Used
1. Python
2. Retrieval-Augmented Generation (RAG)
3. GitHub Models API
4. pdfplumber

Example Question
Can I use metal in a microwave?

Example Output
Metal objects can cause electric arcing inside a microwave. Instead, use oven-safe glass or ceramic cookware without metallic trim.
