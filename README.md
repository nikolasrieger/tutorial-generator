# 🚀 Teachify: Automated Content Creation from PDFs & Websites

## Overview

Welcome to the **Teachify** GitHub repository! This project is designed to automatically generate concise tutorials by extracting and processing content from **PDF documents** and **websites**. The tool utilizes natural language processing (NLP) to summarize key information and present it in a structured tutorial format, making content creation faster and more efficient.

With this tutorial generator, users can quickly create tutorials, guides, and instructional materials based on existing documentation or online resources. Whether you need to turn a lengthy manual into a simple guide or create step-by-step instructions from web content, this tool makes the process seamless. 📄🌐

### 🌟 Features

- 📄 **PDF Content Extraction**: Automatically parses and extracts information from uploaded PDF documents.
- 🌐 **Web Page Scraping**: Gathers and summarizes content from websites based on URLs provided.
- 🧠 **Natural Language Processing**: Summarizes extracted text and organizes it into a structured, easy-to-follow tutorial format.
- ⚡ **Fast & Efficient**: Quickly generates concise tutorials, saving you time and effort in manual content creation.

## 🚀 Getting Started

### Prerequisites

To get started, make sure you have the following:

- 🐍 **Python 3.x**: Essential for running the core logic of the tutorial generator.
- 📦 **Libraries**: Install the required Python packages listed in `requirements.txt`.
- 🔊 **Sonic Pi**: Download and install Sonic Pi to create background or transition music.
- 🔑 **Gemini API Key**: Add your Gemini API Key in a `.env` file.

### Installation

For the **frontend**:
1. Install **Node.js** and **npm**.
2. Run `npm install` to set up the frontend dependencies.
3. Start the frontend via `npm start`.

For the **backend**:
1. Set up the virtual environment by running `python -m venv .venv`.
2. Activate the virtual environment:
   - On **Windows**: `.\.venv\Scripts\activate`
   - On **Linux**: `source .venv/bin/activate`
3. Install **Ruby** and its package manager.
4. Run `gem install sonic-pi-cli4` to install the CLI for Sonic Pi (if you are using a Sonic Pi Version lower than 4, use `gem install sonic-pi-cli` instead).
5. Start the Sonic Pi Application in the background (**Note:** You might hear sounds from the background melody being generated while creating a tutorial).
6. Run the backend with `python app.py`.

## ⚖️ License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.