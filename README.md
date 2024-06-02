# Data-Query-with-RAG-OpenAI-Embeddings-and-Vector-Database

This repository contains a project that demonstrates how to use Retrieval-Augmented Generation (RAG) with OpenAI's GPT-4 model and Pinecone vector database to query a dataset stored in a CSV file. The project involves creating vector embeddings from the data in the CSV file and then querying the vector embeddings data using natural language queries.

Table of Contents
- Introduction

- Prerequisites

- Installation

- Usage

- Ingesting Data and Creating Embeddings

- Querying the Data

- How It Works

- Chunking the CSV Data

- Leveraging OpenAI's GPT-4 LLM

- Customizing for Your CSV File
  
- License

# Introduction

This project showcases the use of natural language processing techniques to query data stored in a CSV file. By leveraging OpenAI's GPT-4 model and Pinecone's vector database, we can create embeddings for the data and use these embeddings to retrieve accurate responses to user queries.

# Prerequisites

Before you begin, ensure you have the following:

- Python 3.8 or higher
- OpenAI API key
- Pinecone API key
- A CSV file containing your data

Set your OpenAI and Pinecone API keys as environment variables:

export OPENAI_API_KEY='your-openai-api-key'

export PINECONE_API_KEY='your-pinecone-api-key'

export PINECONE_HOST='your-pinecone-host'

# Usage
**Ingesting Data and Creating Embeddings**
1. Place your CSV file in the project directory. Update the csv_path variable in best-chunks-insert-embeddings.py to the path of your CSV file.

2. Modify the column titles in the read_csv_data function to match the columns in your CSV file. See the Customizing for Your CSV File section for details.

3. Run the script to read the data, generate embeddings, and store them in Pinecon

#python create-chunks-embeddings-store-vectordb-csv-dataset.py

**Querying the Data**
