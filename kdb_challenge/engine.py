import math
from collections import defaultdict
import pandas as pd

SUGGESTIONS_DF = pd.read_parquet("kdb_challenge/suggestions_challenge.parquet")


class BM25:
    def __init__(
        self,
        documents,
        k1=1.5,
        b=0.75,
        dataframe=None,
        parquet_path="kdb_challenge/suggestions_challenge.parquet",
    ):
        """
        Initialize BM25 for suggestions
        Args:
            documents: List of documents (strings)
            k1: Saturation parameter (Default: 1.5)
            b: Length normalization parameter (Default: 0.75)
            dataframe: Pandas DataFrame with suggestions
            parquet_path: Path to parquet file
        """
        self.documents = documents
        self.k1 = k1
        self.b = b
        self.doc_freqs = []
        self.idf = {}
        self.avg_doc_len = 0
        self.dataframe = dataframe if dataframe is not None else SUGGESTIONS_DF.copy()
        self.parquet_path = parquet_path

        # Ensure 'selection_count' column exists
        if "selection_count" not in self.dataframe.columns:
            self.dataframe["selection_count"] = 0

        self._index()

    def _tokenize(self, text):
        """Split text into tokens"""
        return text.lower().split()

    def _index(self):
        """Index documents"""
        doc_count = len(self.documents)
        total_len = 0
        for doc in self.documents:
            tokens = self._tokenize(doc)
            total_len += len(tokens)
            freqs = defaultdict(int)
            for token in tokens:
                freqs[token] += 1
            self.doc_freqs.append(freqs)

        self.avg_doc_len = total_len / doc_count if doc_count > 0 else 0

        # Calculate IDF
        all_tokens = set()
        for freqs in self.doc_freqs:
            all_tokens.update(freqs.keys())

        for token in all_tokens:
            doc_with_token = sum(1 for f in self.doc_freqs if token in f)
            self.idf[token] = math.log(
                (doc_count - doc_with_token + 0.5) / (doc_with_token + 0.5) + 1
            )

    def score(self, query, doc_index):
        """Calculate BM25 score for a query and document"""
        tokens = self._tokenize(query)
        score = 0
        doc_len = sum(self.doc_freqs[doc_index].values())

        for token in tokens:
            if token not in self.idf:
                continue
            freq = self.doc_freqs[doc_index].get(token, 0)
            idf = self.idf[token]
            # BM25 formula
            numerator = freq * (self.k1 + 1)
            denominator = freq + self.k1 * (
                1 - self.b + self.b * (doc_len / self.avg_doc_len)
            )
            score += idf * (numerator / denominator)

        return score

    def suggest(self, query, top_k=5, min_score=0):
        """
        Return top-K suggestions for a query
        Args:
            query: Search text
            top_k: Number of suggestions
            min_score: Minimum score (optional)
        Returns:
            List of (document, score) tuples
        """
        scores = []
        for idx in range(len(self.documents)):
            score = self.score(query, idx)
            if score >= min_score:
                scores.append({"text": self.documents[idx], "score": score})

        # Sort by score (descending)
        scores.sort(key=lambda x: x["score"], reverse=True)
        return scores[:top_k]

    def count_selection(self, suggestion):
        """
        Count selection of a suggestion and save to parquet
        Args:
            suggestion: The selected suggestion text
        Returns:
            bool: True on success, False on error
        """
        # Find suggestion in DataFrame
        mask = self.dataframe["suggestion"] == suggestion

        if not mask.any():
            print(f"Warning: Suggestion '{suggestion}' not found in DataFrame")
            return False

        # Increment counter
        self.dataframe.loc[mask, "selection_count"] += 1

        # Save to parquet
        self.dataframe.to_parquet(self.parquet_path, index=False)

        return True

    def get_statistics(self):
        """
        Return statistics about suggestions
        Returns:
            DataFrame with suggestions and their selection counts
        """
        return self.dataframe[["suggestion", "selection_count"]].sort_values(
            by="selection_count", ascending=False
        )

    def write_parquet(self, filename):
        """
        Writes the dataframe into a given file(name)
        Args:
            filename: filename to write the dataframe into
        """
        try:
            self.dataframe.to_parquet(filename, index=False)
            return True
        except Exception as e:
            print(f"Error writing to parquet file '{filename}': {e}")
            return False


# Example
if __name__ == "__main__":
    documents = SUGGESTIONS_DF["suggestion"].to_list()

    # Create BM25 index
    bm25 = BM25(documents, dataframe=SUGGESTIONS_DF)

    # Suggestions
    query = "Konto eröffnen"
    suggestions = bm25.suggest(query, top_k=3)

    print(f"Query: '{query}'\n")
    for doc, score in suggestions:
        print(f"Score: {score:.2f} - {doc}")

    # Simulate user selection
    if suggestions:
        selected_suggestion = suggestions[0][0]
        print(f"\nUser selects: '{selected_suggestion}'")
        success = bm25.count_selection(selected_suggestion)
        print(f"Save successful: {success}")

    # Display statistics
    print("\nTop 5 most selected suggestions:")
    print(bm25.get_statistics().head())

    bm25.write_parquet("test.parquet")
