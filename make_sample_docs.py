"""Generate three small sample PDFs so the project runs out of the box.
Replace them with your own notes (put PDFs in sample_docs/ or upload in the app)."""
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak

DOCS = {
    "machine_learning_basics.pdf": [
        ("Machine Learning Basics", [
            "Machine learning is the study of algorithms that improve their performance on a task by learning from data instead of following hand-written rules. The two most common settings are supervised learning and unsupervised learning.",
            "In supervised learning each training example has a label. Regression predicts a continuous number such as the price of a car, while classification predicts a category such as whether a heartbeat is normal or abnormal. Common regression metrics are mean squared error and R squared. Common classification metrics are accuracy, precision, recall and the F1 score.",
            "In unsupervised learning there are no labels. Clustering groups similar examples together, and dimensionality reduction compresses many features into fewer ones. Principal component analysis, called PCA, finds the directions of largest variance and projects the data onto them. PCA is often used before training a classifier on image data such as faces.",
        ]),
        ("Overfitting and Evaluation", [
            "Overfitting happens when a model memorizes the training data and performs poorly on new data. It can be reduced with more data, simpler models, regularization and early stopping. To measure generalization the data is split into a training set and a test set, and cross validation repeats this split several times.",
            "A convolutional neural network, or CNN, uses small sliding filters to detect local patterns. CNNs work well on images and also on one dimensional signals such as ECG recordings, where they learn the shape of a heartbeat. Feature engineering means creating better input columns, for example converting a car's manufacturing year into its age.",
        ]),
    ],
    "rag_explained.pdf": [
        ("Retrieval Augmented Generation", [
            "Retrieval augmented generation, or RAG, combines a search step with a large language model. Instead of relying only on what the model memorized during training, the system first retrieves relevant passages from a document collection and then asks the model to answer using those passages.",
            "A RAG pipeline has four stages. First, documents are loaded and split into chunks of a few hundred words. Second, every chunk is converted into a vector called an embedding, or indexed with a keyword method such as TF-IDF. Third, at question time the system finds the chunks most similar to the question. Fourth, the top chunks are placed in the prompt and the language model writes a grounded answer with citations.",
            "RAG reduces hallucination because the answer is tied to retrieved text. It also lets a system use private or recent documents without retraining the model.",
        ]),
        ("Chunking and Retrieval Choices", [
            "Chunk size is a trade off. Small chunks are precise but may lose context. Large chunks keep context but add noise. Overlap between neighbouring chunks, for example thirty words, prevents an answer from being cut in half at a boundary. Keeping the page number with every chunk makes citations possible.",
            "TF-IDF scores a word highly when it appears often in a chunk but rarely in the whole collection. Embedding search captures meaning, so it can match a question to a passage that uses different words. A vector store such as FAISS or ChromaDB stores embeddings and returns the nearest ones quickly. RAG quality is measured by retrieval hit rate, which asks whether the correct passage was in the top results, and by checking answers against known questions.",
        ]),
    ],
    "digital_marketing_metrics.pdf": [
        ("Paid Advertising Metrics", [
            "Click through rate, or CTR, is the number of clicks divided by the number of impressions. A higher CTR usually means the ad is relevant to the audience. Cost per click, or CPC, is the total spend divided by the number of clicks.",
            "Cost per acquisition, or CPA, is the total spend divided by the number of conversions, where a conversion can be a purchase or a sign up. Return on ad spend, or ROAS, is the revenue generated divided by the ad spend. A ROAS of four means each rupee spent returned four rupees of revenue.",
            "Conversion rate is the number of conversions divided by the number of clicks. Improving the landing page can raise the conversion rate without increasing spend.",
        ]),
        ("Campaign Planning", [
            "Keyword research finds the search terms people use. Match types control how closely a search must match a keyword. Negative keywords stop ads from showing for irrelevant searches. Audience targeting selects people by interest, demographics or past behaviour.",
            "A/B testing compares two versions of an ad or landing page by splitting traffic between them. The version with the better metric wins, provided the sample is large enough. Campaign budgets should be tracked daily, and spend should be compared with the planned budget to avoid overspending.",
        ]),
    ],
}

styles = getSampleStyleSheet()
for filename, pages in DOCS.items():
    doc = SimpleDocTemplate(f"sample_docs/{filename}", pagesize=A4, title=filename)
    story = []
    for i, (title, paras) in enumerate(pages):
        story.append(Paragraph(title, styles["Heading1"]))
        for p in paras:
            story += [Paragraph(p, styles["BodyText"]), Spacer(1, 10)]
        if i < len(pages) - 1:
            story.append(PageBreak())
    doc.build(story)
    print("wrote", filename)
