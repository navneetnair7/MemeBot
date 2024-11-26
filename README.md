# Meme Recommendation System

This project is a **Meme Recommendation System** built using **Next.js** for the frontend, **Flask** for the backend, and AWS services (like S3 and Textract) for image storage and text extraction. The system allows users to upload memes, extract text from those memes, and recommend memes based on a keyword provided by the user.

### Table of Contents

1. [Project Overview](#project-overview)
2. [Tech Stack](#tech-stack)
3. [Features](#features)
4. [Architecture](#architecture)
5. [Future Scope](#future-scope)
6. [Installation & Setup](#installation--setup)
7. [Contributing](#contributing)
8. [License](#license)

---

## Project Overview

This project allows users to upload meme images, and the system extracts text from those images using **AWS Textract**. The user can then enter a keyword, and the system will recommend memes that contain the extracted text matching that keyword.

In the future, the system will be enhanced to understand the **semantic meaning** of images, enabling **prompt-based recommendations** based on image content and text.

---

## Tech Stack

- **Frontend:** 
  - Next.js (React-based framework)
  
- **Backend:** 
  - Flask (Python web framework)

- **Cloud Services:** 
  - **AWS EC2** (Hosting the entire application)
  - **AWS S3** (Storing meme images)
  - **AWS Textract** (Extracting text from meme images)

- **Recommendation Engine:**
  - Text-based (TF-IDF based similarity using extracted text)
  - Future: Semantic-based (using image features and textual content)

---

## Features

1. **Image Upload:** 
   - Users can upload meme images to the system.
   
2. **Text Extraction:** 
   - AWS Textract extracts any readable text from the uploaded meme images.
   
3. **Keyword-based Recommendations:** 
   - Users can enter a keyword, and the system will recommend memes containing matching text extracted from the images.
   
4. **Future Feature - Semantic Search:** 
   - Moving forward, the system will recommend memes based on the **semantic meaning** of the images, not just the text, enabling more flexible and accurate meme recommendations. 
   
   - **Example:** A user could input a prompt like "funny dog memes," and the system will understand the meaning behind the text and image, returning contextually relevant memes (even if the exact keywords aren't matched).

---

## Architecture

### 1. **Frontend (Next.js):**
   - Provides a user-friendly interface to upload images and input keywords.
   - Displays recommended memes based on user input.

### 2. **Backend (Flask):**
   - Handles image uploads, calling AWS services (Textract, Rekognition), and serving the recommendation engine.
   - Handles business logic for text extraction and semantic matching.

### 3. **AWS Services:**
   - **S3:** Meme images are stored here.
   - **Textract:** Extracts text from meme images.

### 4. **Recommendation Engine (Future):**
   - Combines both text-based extraction and semantic analysis of images to recommend the most relevant memes based on keywords or complex prompts.

---

## Future Scope

1. **Semantic Meaning Extraction:**
   - Integrating **CLIP** or similar models to understand the contextual meaning of images (e.g., objects, emotions, and themes) for richer recommendations.
   
2. **Prompt-based Meme Recommendations:**
   - Users will be able to input complex prompts like “memes of sad dogs” or “funny cat memes,” and the system will generate recommendations based on both the **text** and **semantic context** of the images.

3. **Performance Optimizations:**
   - Improving the speed and efficiency of the recommendation engine using **vector search** techniques such as **Faiss** or **Milvus** to perform high-speed similarity searches on the image and text embeddings.

4. **Model Fine-tuning:**
   - Fine-tuning models like **CLIP** to specifically understand meme contexts and improve recommendation accuracy over time.

---

## Installation & Setup

### Prerequisites

- **Node.js** and **npm** (for the frontend)
- **Python 3.x** (for the backend)
- AWS account with access to **S3**, **Textract**, and **Rekognition**
- **Flask** and necessary Python libraries for backend setup

### Steps

#### 1. Clone the repository:
```bash
git clone https://github.com/yourusername/meme-recommendation-system.git
cd ca-project
```

#### 2. Set up the Frontend (Next.js):

```bash
cd frontend
npm install
npm run dev
```

#### 3. Set up the Backend (Flask):

```bash
python -m venv venv
./venv/Scripts/activate
pip install -r requirements.txt
python main.py
```
