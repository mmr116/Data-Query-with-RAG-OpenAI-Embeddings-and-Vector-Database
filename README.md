# Data-Query-with-RAG-OpenAI-Embeddings-and-Vector-Database

This repository contains a project that demonstrates how to use Retrieval-Augmented Generation (RAG) framework with OpenAI's GPT-4o model and Pinecone vector database to query a CSV dataset. The project involves creating vector embeddings from the data in the CSV file, storing embeddings in the Pinecone database, and then querying the vector embeddings data using natural language queries.

Table of Contents
- Introduction

- Prerequisites

- Tested Platform and Packages

- Usage

- Ingesting Data and Creating Embeddings

- Querying the Data

- How It Works
  
- License

# Introduction

This project showcases the use of natural language processing techniques to query data stored in a CSV file. By leveraging OpenAI's GPT-4 model and Pinecone's vector database, we can create embeddings for the data and use these embeddings to retrieve accurate responses to user queries.

# Prerequisites

Before you begin, ensure you have the following:

- Python 3.8 or higher
- OpenAI API key
- Pinecone API key
- A CSV file containing your data

**API integration**: For integrating with OpenAI and Pinecone, you need to obtain and configure the respective API keys, host (pinecone) information for these platforms. Set your OpenAI and Pinecone API keys, and Pinecone host as environment variables in Linux. Use the following Linux commands to export these variables:

export OPENAI_API_KEY='your-openai-api-key'

export PINECONE_API_KEY='your-pinecone-api-key'

export PINECONE_HOST='your-pinecone-host'

# Tested Platforms and Packages

- OpenAI API: OpenAI model "text-embedding-ada-002" and "gpt-4o" used for generating embeddings, and LLM support. Ensure you have an OpenAI account with valid API keys. You can obtain your API keys from the OpenAI platform (https://platform.openai.com/) and manage them (https://platform.openai.com/organization/api-keys). Additionally, ensure that your account has sufficient usage quota, as this example requires a paid OpenAI account.
  
- Pinecone environment (Pinecone free account used https://www.pinecone.io/): 1) Pinecone Index is used 2) Dimensions: 1536 3) Host type: Serverless.

- CentOS Linux release 8.5.2111. Create a virtual environment (optional but recommended) to isolate project dependencies.

- python 3.8.8

- pandas 2.0.3

- openai 1.30.3

- pinecone 4.0.0

- numpy 1.24.4

- argparse 1.1



# Usage
**Ingesting Data and Creating Embeddings**
1. Place your CSV file in the project directory. Update the csv_path variables and Pinecone index name in below files:
   
csv_path = "your_csv_file_path" [create-chunks-embeddings-store-vectordb-csv-dataset.py]

pinecone_index_name = "your_pinecone_index_name" [create-chunks-embeddings-store-vectordb-csv-dataset.py]

index_name = "your_pinecone_index_name" [query-prompt-for-vector-embeddings.py]

2. Modify the column titles in the read_csv_data function to match the columns in your CSV file. See the **Customizing for Your CSV File** section for details.

3. You can use OpenAI LLM models based on your needs:

     model="gpt-4o", # You can use gpt-4 or gpt-3.5-turbo or other OpenAI LLM model. [query-prompt-for-vector-embeddings.py]

5. Run the script to read the data, generate embeddings, and store them in Pinecon

#python create-chunks-embeddings-store-vectordb-csv-dataset.py

**Querying the Data**

1. Use the query-prompt-for-vector-embeddings.py script to query the data:

#python query-prompt-for-vector-embeddings.py "Your query here"

Example: python query-prompt-for-vector-embeddings.py "Tell me about the plot of the movie XYZ"

2. Users can continue to enter queries interactively. To exit, type exit.

Enter your next query (or type 'exit' to quit): Which year this movie got released?

# How It Works

**Chunking the CSV Data, Create Vector Embeddings, and Storing Embeddings in the Pinecone Database**

The script "create-chunks-embeddings-store-vectordb-csv-dataset.py" reads the CSV file and combines relevant columns into a single text string for each row. This text string includes details of columns for each row - each row contains distinct information (for example, information for a movie). The combined text for each row is then used to generate embeddings using OpenAI's API. The vector embeddings are stored in a pinecone index.

**Leveraging OpenAI's GPT-4 LLM**

The project leverages OpenAI's GPT-4 large language model (LLM) in two primary ways:

- Generating Embeddings: The text data from each row of the CSV file is used as input to OpenAI's embedding model (text-embedding-ada-002). This model transforms the text into a high-dimensional vector embedding that captures the semantic meaning of the text. These embeddings are then stored in Pinecone's vector database for efficient retrieval.

- Natural Language Querying: When a user submits a query, the script generates an embedding for the query text using the same embedding model. This query embedding is then used to search the Pinecone vector database for the most semantically similar text chunks (i.e., rows from the CSV file). The relevant text chunks are retrieved and passed to OpenAI's GPT-4 model to generate a comprehensive and contextually accurate response to the user's query.

**Combining Context for Enhanced Responses**

To ensure responses are accurate and relevant, the script maintains a context of previous queries and responses. This context is combined with the retrieved text chunks to provide GPT-4 with a comprehensive view of the information. This approach enhances the model's ability to generate detailed and accurate answers that are grounded in the data provided in the CSV file.

**Customizing for Your CSV File**

To ensure the script works correctly with your CSV file, update the columns "create-chunks-embeddings-store-vectordb-csv-dataset.py" to match the columns in your CSV file. Here is an example of how you can customize the function:

#Users should replace columns with the list of column names they want to use - example below
    
columns = ["Rank", "Director", "Genre", "Plot", "Actors", "Ratings"] # Replace columns with column names of your csv file


# License
This project is licensed under the Apache 2.0 License. See the LICENSE file for details.
