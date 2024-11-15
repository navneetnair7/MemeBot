from flask import Flask, jsonify, request, redirect
import os
import pandas as pd
import re
import boto3
from dotenv import load_dotenv
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from werkzeug.utils import secure_filename
import io

import boto3
from botocore.exceptions import ClientError
from flask_cors import CORS, cross_origin
app = Flask(__name__)
cors = CORS(app) # allow CORS for all domains on all routes.
app.config['CORS_HEADERS'] = 'Content-Type'
# Load environment variables
load_dotenv()

# Initialize the app
# app = Flask(__name__)

# AWS S3 Configuration
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_REGION = os.getenv("AWS_REGION")
AWS_S3_BUCKET_NAME = os.getenv("AWS_S3_BUCKET_NAME")

# Initialize boto3 S3 client
s3_client = boto3.client(
    "s3",
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=AWS_REGION,
)


# Load and preprocess the dataset from S3
def load_df_from_s3():
    try:
        s3_response = s3_client.get_object(Bucket=AWS_S3_BUCKET_NAME, Key="data.csv")
        df = pd.read_csv(s3_response["Body"])
        return df
    except s3_client.exceptions.NoSuchKey:
        return pd.DataFrame(columns=["#", "image_name", "text_corrected"])


# Save the dataframe to S3
def save_df_to_s3(df):
    csv_data = df.to_csv(index=False)
    s3_client.put_object(Body=csv_data, Bucket=AWS_S3_BUCKET_NAME, Key="data.csv")


# Initialize DataFrame
df = load_df_from_s3()


# Apply preprocessing directly to the 'text_corrected' column in place
def preprocess_text(text):
    text = str(text)
    text = text.strip().lower()
    text = re.sub(r"[^a-z\s]", "", text)
    return text


df["text_corrected"] = df["text_corrected"].apply(preprocess_text)

# Initialize the TF-IDF Vectorizer
vectorizer = TfidfVectorizer()
if not df.empty:
    tfidf_matrix = vectorizer.fit_transform(df["text_corrected"])


def recommend_based_on_description(description, top_n=10):
    if df.empty:
        return []
    processed_description = preprocess_text(description)
    new_description_vector = vectorizer.transform([processed_description])
    cosine_similarities = cosine_similarity(
        new_description_vector, tfidf_matrix
    ).flatten()
    top_indices = cosine_similarities.argsort()[-top_n:][::-1]
    return df.iloc[top_indices][["image_name", "text_corrected"]].to_dict(
        orient="records"
    )


# Routes
@app.route("/")
def home():
    return jsonify(message="Welcome to the Meme Recommender Home Page!")


# Route to download meme from S3
@app.route("/download/<filename>")
def download(filename):
    try:
        # Generate a presigned URL to allow access to the file from S3
        s3_url = s3_client.generate_presigned_url(
            "get_object",
            Params={"Bucket": AWS_S3_BUCKET_NAME, "Key": filename},
            ExpiresIn=3600,  # URL expiration time in seconds (1 hour)
        )
        return jsonify({"image_url":s3_url})
    except Exception as e:
        return jsonify(error=str(e)), 500
    

# Search logic for the recommendation system
@app.route("/search")
def search():
    print("Search request received")
    # print(request.args)
    query = request.args.get("searchQuery")
    if not query:
        return jsonify(error="Query parameter is required"), 400

    # Use the recommend function to get results based on the query
    recommended_items = recommend_based_on_description(query)
    # print(recommended_items)
    image_links = []
    for i in recommended_items:
        image_links.append('https://cloud-min-i-project.s3.us-east-1.amazonaws.com/' + i['image_name'])
    print(image_links)
    return jsonify({"recommended_items": image_links})


@app.route("/upload", methods=["POST"])
def upload():
    global df
    if "file" not in request.files :
        return jsonify(error="No file or text_corrected data provided"), 400

    file = request.files["file"]
    text_corrected = request.form["text_corrected"] if "text_corrected" in request.form else "Mr. Bean Save Me"

    if file.filename == "" or not text_corrected:
        return jsonify(error="No file or text_corrected content"), 400

    # Secure the filename and upload to S3
    filename = secure_filename(file.filename)
    file_key = f"memes/{filename}"

    try:
        # Upload image to S3
        s3_client.upload_fileobj(file, AWS_S3_BUCKET_NAME, file_key)
        s3_url = (
            f"https://{AWS_S3_BUCKET_NAME}.s3.{AWS_REGION}.amazonaws.com/{file_key}"
        )

        # Add the new data to the DataFrame with the uploaded image and corrected text
        new_data = {
            "#": len(df) + 1,  # Assuming "#" is just an index or unique identifier
            "image_name": filename,
            "text_corrected": preprocess_text(text_corrected),
        }

        new_row = pd.DataFrame([new_data])

        # Append new row to the dataframe
        df = pd.concat([df, new_row], ignore_index=True)

        # Recalculate the TF-IDF matrix with the new data
        global tfidf_matrix
        tfidf_matrix = vectorizer.fit_transform(df["text_corrected"])

        # Save updated dataframe back to S3
        save_df_to_s3(df)

        return jsonify(
            message="File uploaded successfully.",
            s3_url=s3_url,
        )

    except Exception as e:
        return jsonify(error=str(e)), 500


@app.route("/replace", methods=["POST"])
def replace_csv():
    print(request.files)
    if "file" not in request.files:
        return jsonify(error="No file provided"), 400

    file = request.files["file"]

    if file.filename == "":
        return jsonify(error="No file selected"), 400

    try:
        # Read the CSV file and replace the current df
        print('df')
        global df
        print('before read')
        df = pd.read_csv(file)
        print('read file')
        try:
            df["text_corrected"] = df["text_corrected"].apply(preprocess_text)
        except Exception as e:
            print(e)
        print('df')
        # Recalculate the TF-IDF matrix with the new data
        global tfidf_matrix
        tfidf_matrix = vectorizer.fit_transform(df["text_corrected"])
        print("mat")
        # Save the updated dataframe to S3
        save_df_to_s3(df)
        print('s3')
        return jsonify(message="CSV data replaced successfully.")
    except Exception as e:
        return jsonify(error=str(e)), 500


if __name__ == "__main__":
    app.run(debug=True)
