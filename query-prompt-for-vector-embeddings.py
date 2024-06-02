import os
import numpy as np
from pinecone import Pinecone
import argparse
from openai import OpenAI

# Retrieve the Pinecone API key and host from environment variables
pinecone_api_key = os.getenv("PINECONE_API_KEY")
pinecone_host = os.getenv("PINECONE_HOST")
openai_api_key = os.getenv("OPENAI_API_KEY")

# Error handling: Check if the environment variables are set
if not pinecone_api_key:
    raise ValueError("PINECONE_API_KEY environment variable not set!")
if not pinecone_host:
    raise ValueError("PINECONE_HOST environment variable not set!")
if not openai_api_key:
    raise ValueError("OPENAI_API_KEY environment variable not set!")

# Initialize Pinecone instance
pc = Pinecone(api_key=pinecone_api_key)

# Users should replace 'your_pinecone_index_name' with their own Pinecone index name
index_name = "your_pinecone_index_name" # Replace with your pinecone database index name

# Connect to the Pinecone index
index = pc.Index(index_name, host=pinecone_host)

# Initialize OpenAI client with API key from environment variable
client = OpenAI(api_key=openai_api_key)

# Function to generate embeddings for a text query using OpenAI API
def generate_embedding_for_query(query):
    response = client.embeddings.create(
        input=query,
        model="text-embedding-ada-002" # Replace with your desired model
    )
    embedding = response.data[0].embedding
    return embedding

# Function to generate a comprehensive response using OpenAI's GPT model
def generate_response_from_chunks(chunks, user_query, context):
    combined_text = "\n".join(chunk['metadata']['text'] for chunk in chunks)

    prompt = (
    f"You are an AI assistant. Based on the following movie information and the previous context, "
    f"provide a detailed and accurate response to the user's query: '{user_query}'. "
    f"Only use the information provided below and do not include any additional details that are not mentioned in the text.\n\n"
    f"Previous context:\n{context}\n\n"
    f"Here is the movie information:\n\n{combined_text}\n\nResponse:"
    )

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are an AI assistant providing detailed responses based on given texts."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=500
    )
    return response.choices[0].message.content

def main():
    parser = argparse.ArgumentParser(description="Chat with OpenAI GPT model via command line.")
    parser.add_argument('query', type=str, help="The initial query text.")
    args = parser.parse_args()

    user_query = args.query
    context = ""  # Added to maintain the context

    while True:
        query_embedding = generate_embedding_for_query(user_query)
        embedding_dimension = 1536
        query_vector = np.array(query_embedding)

        if query_vector.size < embedding_dimension:
            padded_query_vector = np.pad(query_vector, (0, embedding_dimension - query_vector.size), 'constant')
        else:
            padded_query_vector = query_vector

        results = index.query(vector=padded_query_vector.tolist(), top_k=10, include_metadata=True)
        score_threshold = 0.75
        filtered_matches = [match for match in results['matches'] if match['score'] > score_threshold]

        if filtered_matches:
            # Generate a response using the top matches
            detailed_response = generate_response_from_chunks(filtered_matches, user_query, context)
            print(f"Response: {detailed_response}")
        else:
            print("No relevant results found above the threshold.")

        user_query = input("Enter your next query (or type 'exit' to quit): ")
        if user_query.lower() == 'exit':
            break
        else:
            user_query = f"{user_query}. Answer this from my movie database information provided to you. Don't add any additional information that is not mentioned in the movie database."
            context += f"\nUser query: {user_query}\nResponse: {detailed_response}\n"

if __name__ == "__main__":
    main()
