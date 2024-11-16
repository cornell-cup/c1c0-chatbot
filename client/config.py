DEBUG: bool     = True  # Print debug messages if True.
FILE_MODE: bool = False # Parse from file if True, else from microphone.
MAC_MODE: bool  = True  # True if on a Mac, false on Linux.

EMBEDDING_MODEL: str   = 'text-embedding-3-large'  # OpenAI embedding to use.
FUZZY_THRESHOLD: float = 60    # Minimum score to consider a fuzzy match.
LABEL_THRESHOLD: float = 0.4   # Minimum score to consider a label match.

CHAT_MODEL: str               = "gpt-4o-mini" # OpenAI model to use for chat.
SPECIFIC_THRESHOLD: float     = 0.35 # Minimum score to categorize a more specialized general request or question.
# BROAD_THRESHOLD: float        = 0.3  # Minimum score to cat
GENERAL_THRESHOLD: float      = 0.1  # Minimum score to recognize a general request

