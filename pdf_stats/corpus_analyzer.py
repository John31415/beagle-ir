import os
import PyPDF2
from sklearn.feature_extraction.text import TfidfVectorizer
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import numpy as np
from utils.text_processor import TextPreprocessor
from matplotlib.ticker import MaxNLocator

def text2tokens(text) -> list[str]:
    tp = TextPreprocessor(text)
    tp.text = tp.get_clean_text()
    tp.tokens = tp._tokenize()
    tp.tokens = tp._remove_stop_words()
    return tp.tokens

def gen_cloud_tfidf(docs_tokens, k):
    corpus = [" ".join(tokens) for tokens in docs_tokens]
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(corpus)
    scores = np.asarray(tfidf_matrix.sum(axis=0)).ravel()
    names = vectorizer.get_feature_names_out()
    term_scores = dict(zip(names, scores))
    top_k = dict(sorted(term_scores.items(), key=lambda x: x[1], reverse=True)[:k])
    wc = WordCloud(
        width = 1000, 
        height = 500, 
        background_color = 'white', 
        colormap = 'viridis', 
        max_words = k
    ).generate_from_frequencies(top_k)
    plt.figure(figsize = (10, 5))
    plt.imshow(wc, interpolation = 'bilinear')
    plt.axis("off")
    plt.tight_layout(pad = 0)
    plt.savefig('pdf_stats/wordcloud.png', dpi = 300, bbox_inches = 'tight')
    plt.close()

def plot_histogram(hist):
    ranges = list(hist.keys())
    counts = list(hist.values())
    plt.figure(figsize = (8, 5))
    ax = plt.gca()
    ax.yaxis.set_major_locator(MaxNLocator(integer = True))
    plt.bar(ranges, counts, color = plt.cm.viridis(0.3), edgecolor = "black", linewidth = 0.8)
    plt.xlabel("Rangos de páginas", fontsize = 10, fontweight = 'bold')
    plt.ylabel("Número de documentos", fontsize = 10, fontweight = 'bold')
    plt.title("Distribución del conteo de páginas (PDF)", fontsize = 12)
    plt.xticks(rotation = 45)
    plt.grid(axis = 'y', linestyle = '--', alpha = 0.4)
    plt.tight_layout()
    plt.savefig("pdf_stats/page_distribution.png", dpi = 300)
    plt.close()

def analyze_corpus(corpus_path = "corpus/"):
    pdf_files = [f for f in os.listdir(corpus_path) if f.lower().endswith(".pdf")]
    total_docs = len(pdf_files)
    total_size_bytes = 0
    page_counts = []
    total_tokens = 0
    all_tokens = []
    docs_tokens = []
    chunk_counts = []
    for (i, filename) in enumerate(pdf_files):
        i += 1
        if i % 20 == 0:
            print(i)
        filepath = os.path.join(corpus_path, filename)
        total_size_bytes += os.path.getsize(filepath)
        try:
            with open(filepath, "rb") as f:
                reader = PyPDF2.PdfReader(f)
                num_pages = len(reader.pages)
                page_counts.append(num_pages)
                full_text = ""
                for page in reader.pages:
                    text = page.extract_text()
                    if text:
                        full_text += text + " "
                tokens = text2tokens(full_text)
                docs_tokens.append(tokens)
                token_count = len(tokens)
                total_tokens += token_count
                all_tokens.extend(tokens)
                if token_count <= 500:
                    chunks = 1
                else:
                    chunks = (token_count - 500) // 400 + 1
                chunk_counts.append(chunks)
        except Exception as e:
            print(f"Error processing {filename}: {e}")
            continue
    avg_size_mb = total_size_bytes / (total_docs * 1024 * 1024)
    page_ranges = [(1, 10), (11, 20), (21, 30), (31, 40), (41, 50), (51, float("inf"))]
    hist = {f"{low}-{high if high != float('inf') else '51+'}": 0 for low, high in page_ranges}
    for pages in page_counts:
        for low, high in page_ranges:
            if low <= pages <= high:
                hist[f"{low}-{high if high != float('inf') else '51+'}"] += 1
                break
    avg_tokens = total_tokens / total_docs if total_docs else 0
    total_chunks = sum(chunk_counts)
    avg_chunks = total_chunks / total_docs if total_docs else 0
    vocab_size = len(set(all_tokens))
    print(f"Total documents: {total_docs}")
    print(f"Average PDF size: {avg_size_mb:.2f} MB")
    print(f"Total words/tokens: {total_tokens}")
    print(f"Average words/tokens per document: {avg_tokens:.2f}")
    print(f"Total chunks: {total_chunks}")
    print(f"Average chunks per document: {avg_chunks:.2f}")
    print(f"Total vocabulary (unique terms): {vocab_size}")
    plot_histogram(hist)
    gen_cloud_tfidf(docs_tokens, 30)

analyze_corpus()