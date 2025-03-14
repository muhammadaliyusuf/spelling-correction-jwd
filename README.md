# Spelling Correction using Jaro Winkler Distance Algorithm with Multiprocessing

A web application for spelling correction using Flask with Jaro-Winkler Distance (JWD) algorithm. This application helps enhance search engine functionality by correcting spelling errors in Indonesian and English text.

## Description

This spelling correction application is built using the Flask framework and implements the Jaro-Winkler Distance algorithm. It improves search engine results by identifying and providing correction suggestions for misspelled words. The application uses multiprocessing to handle large datasets efficiently, ensuring fast response times even with extensive vocabulary references.

## Features

- Spelling correction using Jaro-Winkler Distance algorithm (86% accuracy)
- Integration with web application search engines
- Support for both Indonesian and English text
- Fast correction process using Multiprocessing implementation for handling large datasets

## Technologies Used

- Python 3.x
- Flask (Backend)
- HTML, CSS, JavaScript (Frontend)
- Bootstrap
- Jaro-Winkler Distance Algorithm
- Multiprocessing

## Datasets Used

- 61,434 Indonesian vocabulary words ([Indonesian Wordlist KBBI](https://github.com/geovedi/indonesian-wordlist/edit/master/01-kbbi3-2001%20sort-alpha.lst))
- 30,000 High Frequency English Vocabulary ([English Vocabulary](https://github.com/derekchuank/high-frequency-vocabulary))
- 758 Indonesian stopwords ([Indonesian Stoplist](https://www.kaggle.com/datasets/oswinrh/indonesian-stoplist))
- 100 Madura Tourism News

## Installation

### Prerequisites

- Python 3.x
- pip (Python package installer)

### Installation Steps

1. Clone this repository
   ```bash
   git clone https://github.com/muhammadaliyusuf/spelling-correction-jwd.git
   cd spelling-correction-jwd
   ```

2. Create and activate a virtual environment
   ```bash
   python -m venv venv
   source venv/bin/activate  # For Linux/Mac
   venv\Scripts\activate     # For Windows
   ```

3. Install required dependencies
   ```bash
   pip install -r requirements.txt
   ```

4. Run the application (choose one)
   ```bash
   python app-serial.py      # Without multiprocessing
   python app-paralel.py     # With multiprocessing
   ```

5. Open a browser and access the application at `http://localhost:5000`

## Usage

1. Enter the search query or text you want to correct
2. Submit the query to the search engine
3. The application will process the input using the Jaro-Winkler Distance algorithm
4. Search results will include corrections for misspelled words, improving search accuracy

## Project Structure

```
spelling-correction-jwd/
│
├── app-serial.py           # Main Flask application without multiprocessing
├── app-paralel.py          # Main Flask application with multiprocessing
├── requirements.txt        # List of dependencies
├── static/                 # Folder for static files (CSS, JS, etc.)
│   ├── css/...
│   ├── fonts/...
│   ├── img/...
│   ├── js/...
│   └── scss/
├── templates/              # Folder for HTML templates
│   ├── index.html
│   └── result.html
├── models/                 # Folder for spelling correction models
│   └── jarowinklerdistance.py  # Implementation of JWD algorithm
├── utils/                  # Folder for utility functions
│   └── preprocessing.py    # Text preprocessing functions
└── data/                   # Folder for datasets
    ├── 30k-english-vocabulary.txt
    ├── 61434-indonesiawordlist.txt
    ├── stopword-bahasa.txt
    └── madura-tourism-news.csv

```

## Contributing

Contributions are always welcome. Here are the steps to contribute:

1. Fork this repository
2. Create a new branch (`git checkout -b new-feature`)
3. Commit your changes (`git commit -m 'Add new feature'`)
4. Push to the branch (`git push origin new-feature`)
5. Create a Pull Request

## License

This project was created as a requirement for the completion of a Bachelor's degree in Informatics Engineering at Universitas Trunojoyo Madura.

## Contact

Muhammad Ali Yusuf - muhammadaliyusuff22@gmail.com
