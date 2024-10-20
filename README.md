
# LLM Data Extractor

LLM Data Extractor is a FastAPI-based API designed to scrape web pages from a given domain, extract specific information requested by the user using LLMs, and return a structured result containing the extracted information with the corresponding source URLs. 

## How It Works

1. **Input**: 
   - A target URL.
   - A dictionary specifying the data you want to extract from the page and its subpages.

2. **Process**: 
   - The API scrapes the pages of the provided domain.
   - Attempts to extract the requested information by leveraging an LLM.

3. **Output**: 
   - The list of extracted data.
   - Source links for each extracted piece of information.

## Setup

1. **Clone the repository**:
```
git clone https://github.com/Lele-Adri/LLM_data_extractor.git
cd LLM_data_extractor
```

2. **Install the dependencies**:
```
pip install -r requirements.txt
```

3. **Run the application**:
```
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```
or using the makefile:
```
make
```

4. **Access the API documentation**:
   The FastAPI documentation will be available at `http://127.0.0.1:8000/docs` once the server is running.

## Testing

To run tests (from root directory):
```
pytest ./tests/functional/api/test_url_analysis_endpoint.py::test_url_analysis_valid_empty_data
```
or using the makefile:
```
make test-all
```
