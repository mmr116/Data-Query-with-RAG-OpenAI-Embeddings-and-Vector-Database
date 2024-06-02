import os
import pandas as pd
import openai
from pinecone import Pinecone

# Retrieve the Pinecone API key and host from environment variables
pinecone_api_key = os.getenv("PINECONE_API_KEY")
pinecone_host = os.getenv("PINECONE_HOST")

# Error handling (optional): Check if the environment variables are set
if not pinecone_api_key:
    raise ValueError("PINECONE_API_KEY environment variable not set!")
if not pinecone_host:
    raise ValueError("PINECONE_HOST environment variable not set!")

# Retrieve the OpenAI API key from environment variable (assuming separate variable)
openai_api_key = os.getenv("OPENAI_API_KEY")

# Error handling (optional): Check if the environment variable is set
if not openai_api_key:
    raise ValueError("OPENAI_API_KEY environment variable not set!")

# Function to read data from CSV file
def read_csv_data(csv_path, columns):
    df = pd.read_csv(csv_path)
    # Combine relevant columns to form text data for embeddings
    df['text'] = df.apply(lambda row: ". ".join([f"{col}: {row[col]}" for col in columns]), axis=1)
    return df['text'].tolist()

# Function to generate embeddings for each text using OpenAI API
def generate_embeddings(texts):
    # Initialize OpenAI client with API key from environment variable
    client = openai.OpenAI(api_key=openai_api_key)

    embeddings = []
    for text in texts:
        # Use client object to call the embeddings API
        response = client.embeddings.create(
            input=text,
            model="text-embedding-ada-002"  # Replace with your desired model
        )
        embedding = response.data[0].embedding
        embeddings.append(embedding)
    return embeddings

# Function to store embeddings in Pinecone in batches
def store_embeddings_in_pinecone(embeddings, texts, index_name, batch_size=100):
    embedding_dimension = 1536  # Update based on your OpenAI model or experiment

    print(f"Retrieved Pinecone API key: {pinecone_api_key}")

    pinecone = Pinecone(api_key=pinecone_api_key, environment=pinecone_host)
    index = pinecone.Index(index_name)

    data_points = []
    for i, (text, embedding) in enumerate(zip(texts, embeddings)):
        data_point = {
            "id": f"text_{i+1}",
            "values": embedding,
            "metadata": {"text": text}
        }
        data_points.append(data_point)

        # Upsert in batches
        if len(data_points) >= batch_size:
            index.upsert(data_points)
            data_points = []

    # Upsert any remaining data points
    if data_points:
        index.upsert(data_points)

    print(f"Successfully stored {len(embeddings)} data points in Pinecone")

# Example usage
if __name__ == "__main__":
    # Users should replace 'your_csv_file_path' with the path to their own CSV file
    csv_path = "your_csv_file_path"

    # Users should replace columns with the list of column names they want to use - example below
    columns = ["Rank", "Director", "Genre", "Plot", "Actors", "Ratings"] # Replace columns with column names of your csv file

    # Users should replace 'your_pinecone_index_name' with their own Pinecone index name
    pinecone_index_name = "your_pinecone_index_name" # Replace with your pineconde database index name

    # Step 1: Read data from CSV
    csv_data = read_csv_data(csv_path, columns)
    print("CSV Data:", csv_data)

    # Step 2: Generate embeddings for each row
    embeddings = generate_embeddings(csv_data)
    print("Embeddings:")
    for i, embedding in enumerate(embeddings):
        print(f"Embedding {i+1}:\n{embedding[:20]}\n")  # Print only first 20 elements for brevity

    # Step 3: Store embeddings in Pinecone
    store_embeddings_in_pinecone(embeddings, csv_data, pinecone_index_name)
