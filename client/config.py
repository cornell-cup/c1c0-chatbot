DEBUG: bool            = True  # Print debug messages if True.
EMBEDDING_MODEL: str   = 'text-embedding-3-large'  # OpenAI embedding to use.
CHAT_MODEL: str = "gpt-3.5-turbo"
FUZZY_THRESHOLD: float = 60  # Minimum score to consider a fuzzy match.

SPECIFIC_THRESHOLD: float = 0.35 #threshold is for more specific examples or categories for requests or questions
GENERAL_THRESHOLD: float = 0.2 #threshold is for more general examples or categories for requests or questions
VERY_GENERAL_THRESHOLD: float = 0.15

LABEL_THRESHOLD: float = 0.3

