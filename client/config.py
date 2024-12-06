DEBUG: bool            = True  # Print debug messages if True.
EMBEDDING_MODEL: str   = 'text-embedding-3-small'  # OpenAI embedding to use.
FUZZY_THRESHOLD: float = 60    # Minimum score to consider a fuzzy match.
LABEL_THRESHOLD: float = 0.4   # Minimum score to consider a label match.
FILE_MODE: bool        = False  # Parse from file if True, else from microphone.
MAC_MODE: bool         = True  # True if on a Mac, false on Linux.
