# 🛒 Electronics Store Q&A System

An intelligent question-answering system that allows store managers to query their electronics inventory database using natural language. Built with **vector embeddings**, **Chroma database**, **LangChain**, **Google Gemini**, and **Streamlit**.

![Electronics Store](electronics_store.png)

## 🎯 Project Overview

This LLM-powered application enables natural language interaction with a PostgreSQL database containing electronics inventory, sales, and pricing data. The system uses **vector embeddings** for intelligent question matching and **few-shot learning** to generate accurate SQL queries from natural language questions.

## 🖼️ Dashboard

**Dashboard View 1**
![Dashboard 1](https://raw.githubusercontent.com/UNKNOWNAR/Electronics-Store-Q-A-System/master/dashboard-1.jpg)

**Dashboard View 2**
![Dashboard 2](https://raw.githubusercontent.com/UNKNOWNAR/Electronics-Store-Q-A-System/master/dashboard-2.jpg)

**Dashboard View 3**
![Dashboard 3](https://raw.githubusercontent.com/UNKNOWNAR/Electronics-Store-Q-A-System/master/dashboard-3.jpg)

### ✨ Key Features

- **🔍 Vector Embeddings**: Intelligent similarity search using Chroma database
- **💬 Natural Language Processing**: Ask questions in plain English
- **💻 SQL Generation**: Automatic SQL query generation from similar examples
- **📊 Real-time Execution**: Execute queries and view results instantly
- **✏️ Editable SQL Queries**: Edit and customize the generated SQL queries before execution
- **🎨 Modern UI**: Beautiful Streamlit interface with confidence scoring
- **⚡ Fast Search**: Sub-second response times with caching

### Sample Questions
- "How many Samsung phones do we have in stock?"
- "What's the total value of all laptops?"
- "Which products have discounts over 10%?"
- "How much revenue can we make from Apple products?"
- "What's the average price of smartwatches?"

## 🛠️ Tech Stack

- **LLM:** Google Gemini Pro
- **Vector Database:** Chroma DB
- **Embeddings:** Sentence Transformers (all-MiniLM-L6-v2)
- **Framework:** LangChain
- **Database:** PostgreSQL
- **UI:** Streamlit
- **Language:** Python 3.10+

## 🚀 Quick Start

### 1. Clone the Repository
```bash
git clone https://github.com/UNKNOWNAR/Electronics-Store-Q-A-System.git
cd Electronics-Store-Q-A-System
```

### 2. Set Up Virtual Environment
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows
.\venv\Scripts\Activate.ps1
# Linux/Mac
source venv/bin/activate
```

### 3. Install Dependencies
```bash
# Install all requirements
pip install -r requirements.txt
```

### 4. Set Up Environment Variables
Create a `.env` file in the project root:
```env
# Database Configuration
DB_HOST=localhost
DB_NAME=electronics_store
DB_USER=postgres
DB_PASSWORD=your_password
DB_PORT=5432

# Google Gemini API Key
GOOGLE_API_KEY=your_api_key_here
```

### 5. Set Up Database
```bash
# Test database connection
python database_setup.py

# Create database schema
# Run the SQL script: database/db_creation_electronics_store.sql
```

### 6. Launch the Application
```bash
streamlit run main.py
```

The app will open at `http://localhost:8501`

## 📁 Project Structure

```
Electronics-Store-Q-A-System/
├── main.py                          # Main Streamlit application
├── vector_embeddings.py             # Vector embedding manager
├── qa_integration.py                # Q&A system integration
├── few_shots.py                     # Example questions and SQL
├── config.py                        # Configuration management
├── database_setup.py                # Database utilities
├── gemini.md                        # Gemini configuration file
├── requirements.txt                 # Core dependencies
├── README.md                        # This file
└── database/
    └── db_creation_electronics_store.sql  # Database schema
```

## 🎮 How to Use

### 1. **Ask Questions**
- Type natural language questions about your electronics store
- Use the example questions in the sidebar for quick testing
- The system will find similar questions and generate SQL

### 2. **Review and Edit SQL**
- See confidence scores for match quality
- Review and edit the generated SQL query in the text box
- Execute queries to see actual database results
- Explore similar questions for reference

### 3. **Adjust Settings**
- Use the similarity threshold slider to control matching strictness
- Monitor system information in the sidebar
- Check database connection status

## 🔧 Vector Embeddings System

### How It Works
1. **Question Processing**: User question → Vector embedding
2. **Similarity Search**: Find similar questions in Chroma database
3. **SQL Generation**: Use best match to generate SQL query
4. **Confidence Scoring**: Rate match quality (0-100%)

### Features
- **Fast Search**: Sub-second similarity matching
- **Intelligent Matching**: Semantic understanding of questions
- **Confidence Scoring**: Quality indicators for results
- **Persistent Storage**: Chroma database with metadata
- **Easy Updates**: Add new examples to improve matching

## 💾 Database Schema

### Products Table
- `product_id` (Primary Key)
- `brand` (Apple, Samsung, Dell, HP, Lenovo, etc.)
- `category` (Laptop, Phone, Tablet, Headphones, etc.)
- `model_name`
- `specs` (Storage, RAM, etc.)
- `price`
- `stock_quantity`

### Discounts Table
- `discount_id` (Primary Key)
- `product_id` (Foreign Key)
- `pct_discount`

## 📊 Database Overview

![Database Overview](https://raw.githubusercontent.com/UNKNOWNAR/Electronics-Store-Q-A-System/master/database-overview.jpg)

## 🎯 Example Workflows

### Basic Question
1. **Input**: "How many Samsung phones do we have?"
2. **Match**: "How many Samsung phones do we have in stock?" (95% confidence)
3. **SQL**: `SELECT SUM(stock_quantity) FROM products WHERE brand = 'Samsung' AND category = 'Phone'`
4. **Result**: Interactive table showing the count

### Complex Query
1. **Input**: "Show me products with big discounts"
2. **Match**: "Which products have discounts greater than 10%?" (85% confidence)
3. **SQL**: Complex JOIN query with filtering
4. **Result**: Table of discounted products with details

## 🔧 Configuration

### Database Connection
Update your `.env` file with your database credentials:
```env
DB_HOST=localhost
DB_NAME=electronics_store
DB_USER=postgres
DB_PASSWORD=your_password
DB_PORT=5432
```

### Vector Database
The system automatically uses:
- **Path**: `./chroma_db`
- **Collection**: `electronics_qa`
- **Model**: `all-MiniLM-L6-v2`

### Similarity Threshold
Adjust matching sensitivity:
- **Lower values**: More permissive, more matches
- **Higher values**: More strict, fewer but better matches

## 🛠️ Development

### Adding New Examples
1. Add new entries to `few_shots.py`
2. Restart the app (embeddings auto-update)
3. Test with new questions

### Customizing the System
- Modify `config.py` for system settings
- Update `vector_embeddings.py` for embedding logic
- Enhance `qa_integration.py` for Q&A functionality

### Testing
```bash
# Test vector embeddings
python vector_embeddings.py

# Test database connection
python database_setup.py
```

## ✨ Recent Changes

- **Editable SQL Queries**: Users can now edit the generated SQL query before execution.
- **Bug Fix**: Fixed a bug where the application would crash due to an incorrect database engine being used.

## 🛠️ Troubleshooting

### Common Issues

1. **"No similar questions found"**
   - Lower the similarity threshold
   - Add more examples to `few_shots.py`
   - Try rephrasing your question

2. **Database connection failed**
   - Check your `.env` file configuration
   - Ensure PostgreSQL is running
   - Verify database exists and is accessible

3. **Vector embeddings not found**
   - Run `python vector_embeddings.py` first
   - Check if `./chroma_db` directory exists

4. **Streamlit won't start**
   - Check if port 8501 is available
   - Try `streamlit run main.py --server.port 8502`

### Performance Tips
- **First run**: May be slower due to model loading
- **Subsequent runs**: Much faster with caching
- **Large databases**: Consider query timeouts for complex queries

## 📊 Performance Metrics

- **Question Processing**: ~200ms
- **Vector Search**: ~50ms
- **SQL Generation**: ~10ms
- **Query Execution**: Varies by complexity
- **UI Rendering**: ~100ms

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📝 License

This project is open source and available under the MIT License.

## 👨‍💻 Author

**UNKNOWNAR**
- GitHub: [@UNKNOWNAR](https://github.com/UNKNOWNAR)
- Repository: [Electronics-Store-Q-A-System](https://github.com/UNKNOWNAR/Electronics-Store-Q-A-System)

## 🙏 Acknowledgments

- Inspired by the AtliQ T-shirts project from Codebasics
- Built with LangChain, Google Gemini, and Streamlit
- Vector embeddings powered by Chroma DB and Sentence Transformers
- UI components and styling inspired by modern web design principles

## 📞 Support

For issues or questions:
1. Check the troubleshooting section
2. Review the console output for errors
3. Test database connection with `database_setup.py`
4. Verify vector embeddings with `vector_embeddings.py`
5. Open an issue on GitHub

---

⭐ **Star this repo if you find it helpful!**

🛒 **Electronics Store Q&A System** - Powered by Vector Embeddings & AI