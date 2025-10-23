# Electronics Store Q&A System 💻📱

An intelligent question-answering system that allows store managers to query their electronics inventory database using natural language. Built with LangChain, Google Gemini, and Streamlit.

![Electronics Store](electronics_store.png)

## 🎯 Project Overview

This LLM-powered application enables natural language interaction with a MySQL database containing electronics inventory, sales, and pricing data. Store managers can ask questions in plain English and receive accurate responses generated from SQL queries.

### Sample Questions
- "How many Samsung phones with 256GB storage are in stock?"
- "What is the total inventory value of all laptops?"
- "Show me all Apple products under $1000"
- "How much revenue will we generate if we sell all gaming laptops with current discounts?"

## 🛠️ Tech Stack

- **LLM:** Google Gemini Pro
- **Framework:** LangChain
- **Embeddings:** HuggingFace (sentence-transformers)
- **Vector Store:** Chroma
- **Database:** MySQL
- **UI:** Streamlit
- **Language:** Python 3.8+

## 📋 Features

- Natural language to SQL query conversion
- Few-shot learning for accurate query generation
- Semantic similarity-based example selection
- Support for complex queries with JOINs
- Discount and pricing calculations
- Real-time inventory tracking

## 🚀 Installation

### Prerequisites
- Python 3.8 or higher
- MySQL Server
- Google Gemini API key

### Steps

1. **Clone the repository**
```bash
git clone https://github.com/UNKNOWNAR/electronics-store-qa.git
cd electronics-store-qa
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Get Google Gemini API Key**
   - Visit: https://aistudio.google.com/app/apikey
   - Create a free API key

4. **Configure API Key**
   - Open `langchain_helper.py`
   - Replace `YOUR_API_KEY_HERE` with your actual key, or
   - Set environment variable: 
   ```bash
   # Windows PowerShell
   $env:GOOGLE_API_KEY="your_api_key_here"
   
   # Linux/Mac
   export GOOGLE_API_KEY="your_api_key_here"
   ```

5. **Setup Database**
   - Open MySQL Workbench
   - Run the script: `database/db_creation_electronics_store.sql`
   - Update database credentials in `langchain_helper.py` if needed

## 📂 Project Structure

```
electronics-store-qa/
├── main.py                    # Streamlit UI
├── langchain_helper.py        # LangChain SQL chain logic
├── few_shots.py              # Few-shot examples for training
├── requirements.txt          # Python dependencies
├── .gitignore               # Git ignore rules
├── README.md                # Project documentation
└── database/
    └── db_creation_electronics_store.sql  # Database schema
```

## 🎮 Usage

1. **Start the application**
```bash
streamlit run main.py
```

2. **Open your browser** (usually auto-opens at `http://localhost:8501`)

3. **Ask questions** in natural language about your inventory

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

## 🔧 Configuration

Update database credentials in `langchain_helper.py`:
```python
db_user = "root"
db_password = "your_password"
db_host = "localhost"
db_name = "electronics_store"
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📝 License

This project is open source and available under the MIT License.

## 👨‍💻 Author

**UNKNOWNAR**
- GitHub: [@UNKNOWNAR](https://github.com/UNKNOWNAR)

## 🙏 Acknowledgments

- Inspired by the AtliQ T-shirts project from Codebasics
- Built with LangChain and Google Gemini
- UI powered by Streamlit

---

⭐ Star this repo if you find it helpful!
