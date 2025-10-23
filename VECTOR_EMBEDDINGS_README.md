# Vector Embeddings for Electronics Store Q&A System

This system creates vector embeddings from your few shots data and stores them in a Chroma database for efficient similarity search and question matching.

## 🚀 Quick Start

### 1. Install Dependencies
```bash
# Activate your virtual environment
.\venv\Scripts\Activate.ps1

# Install required packages (if not already installed)
pip install chromadb sentence-transformers torch torchvision
```

### 2. Create Vector Embeddings
```bash
python vector_embeddings.py
```

This will:
- Create embeddings from your `few_shots.py` data
- Store them in a Chroma database (`./chroma_db/`)
- Test the search functionality

### 3. Run Examples
```bash
# See comprehensive examples
python example_usage.py

# Try the integration demo
python qa_integration.py
```

## 📁 Files Created

- `vector_embeddings.py` - Main vector embedding manager
- `example_usage.py` - Comprehensive usage examples
- `qa_integration.py` - Integration with your Q&A system
- `./chroma_db/` - Chroma database directory (created automatically)

## 🔧 How It Works

### VectorEmbeddingManager Class

The main class that handles:
- **Embedding Generation**: Uses SentenceTransformer model (`all-MiniLM-L6-v2`)
- **Chroma Database**: Stores embeddings with metadata
- **Similarity Search**: Finds similar questions using cosine similarity

### Key Methods

```python
from vector_embeddings import VectorEmbeddingManager

# Initialize
manager = VectorEmbeddingManager()

# Create embeddings from few shots
manager.create_embeddings_from_few_shots()

# Search for similar questions
results = manager.search_similar_questions("How many Samsung phones?", n_results=3)

# Get collection info
info = manager.get_collection_info()
```

## 🎯 Integration with Your Q&A System

### Basic Usage
```python
from qa_integration import ElectronicsQA

# Initialize
qa_system = ElectronicsQA()

# Get SQL suggestion
suggestion = qa_system.suggest_sql_query("How many laptops do we have?")
print(suggestion['suggested_sql'])
print(suggestion['confidence'])
```

### Advanced Usage
```python
# Find similar questions
similar = qa_system.find_similar_questions("Samsung phones", top_k=5)

# Get best match with threshold
best_match = qa_system.get_best_match("Apple products", threshold=0.6)
```

## 📊 What Gets Embedded

For each entry in `few_shots.py`, the system creates embeddings from:
- **Combined Text**: `"Question: {question}\nSQL Query: {sql_query}"`
- **Metadata**: All original fields (question, SQL, answer, etc.)

## 🔍 Search Results Format

```python
{
    'documents': [['Question: ...\nSQL Query: ...']],
    'metadatas': [[{
        'question': 'How many Samsung phones do we have in stock?',
        'sql_query': 'SELECT SUM(stock_quantity) FROM products WHERE brand = "Samsung" AND category = "Phone"',
        'sql_result': 'Result of the SQL query',
        'answer': '125',
        'index': 0
    }]],
    'distances': [[0.482]],  # Lower = more similar
    'ids': [['few_shot_0']]
}
```

## ⚙️ Configuration

### Customize Database Path
```python
manager = VectorEmbeddingManager(
    db_path="./my_custom_db",
    collection_name="my_collection"
)
```

### Adjust Similarity Threshold
```python
# In qa_integration.py
best_match = qa_system.get_best_match(question, threshold=0.7)  # Higher = stricter
```

## 🎨 Example Queries and Results

| User Question | Best Match | Similarity | SQL Query |
|---------------|------------|------------|-----------|
| "How many Samsung phones?" | "How many Samsung phones do we have in stock?" | 0.523 | `SELECT SUM(stock_quantity) FROM products WHERE brand = 'Samsung' AND category = 'Phone'` |
| "Total laptop value?" | "What is the total price of all laptops in inventory?" | 0.570 | `SELECT SUM(price * stock_quantity) FROM products WHERE category = 'Laptop'` |
| "Products with discounts?" | "Which products have discounts greater than 10%?" | 0.689 | `SELECT p.brand, p.category, p.model_name, d.pct_discount FROM products p JOIN discounts d ON p.product_id = d.product_id WHERE d.pct_discount > 10` |

## 🔄 Adding New Examples

1. Add new entries to `few_shots.py`
2. Run `python vector_embeddings.py` to update embeddings
3. The system will automatically include new examples in searches

## 🛠️ Troubleshooting

### Common Issues

1. **Import Errors**: Make sure you're in the virtual environment
2. **Empty Results**: Check if embeddings were created successfully
3. **Low Similarity**: Consider adding more diverse examples to `few_shots.py`

### Reset Database
```python
manager = VectorEmbeddingManager()
manager.reset_collection()  # Deletes all data
manager.create_embeddings_from_few_shots()  # Recreate
```

## 📈 Performance

- **Embedding Model**: `all-MiniLM-L6-v2` (fast, good quality)
- **Search Speed**: Sub-second for 10 examples
- **Storage**: ~1MB for 10 examples with metadata
- **Memory**: ~50MB for model + database

## 🔮 Future Enhancements

- Add more embedding models (e.g., `all-mpnet-base-v2` for better quality)
- Implement hybrid search (vector + keyword)
- Add query expansion and reformulation
- Support for multiple languages
- Real-time embedding updates

## 📝 Notes

- The system uses cosine similarity for matching
- Similarity scores range from 0 (no similarity) to 1 (identical)
- Threshold of 0.5 is recommended for production use
- The database persists between runs
- All metadata from `few_shots.py` is preserved
