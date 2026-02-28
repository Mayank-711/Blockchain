"""
services/hash_service.py
SHA-256 hashing service for certificate files.

Provides deterministic hashing of uploaded documents
for blockchain storage and verification comparison.
"""

import hashlib
import logging

logger = logging.getLogger(__name__)


class HashService:
    """
    Service for generating SHA-256 hashes of certificate files.

    Usage:
        file_hash = HashService.hash_file('/path/to/cert.pdf')
        text_hash = HashService.hash_text('extracted text content')
    """

    @staticmethod
    def hash_file(file_path):
        """
        Generate SHA-256 hash of a file's contents.

        Args:
            file_path (str): Absolute path to the file.

        Returns:
            str: Hex-encoded SHA-256 hash string.
        """
        sha256 = hashlib.sha256()
        try:
            with open(file_path, 'rb') as f:
                # Read in chunks for memory efficiency
                for chunk in iter(lambda: f.read(8192), b''):
                    sha256.update(chunk)
            file_hash = sha256.hexdigest()
            logger.info(f"Generated hash for file: {file_hash[:16]}...")
            return file_hash
        except Exception as e:
            logger.error(f"Failed to hash file {file_path}: {e}")
            raise

    @staticmethod
    def hash_text(text):
        """
        Generate SHA-256 hash of text content.

        Args:
            text (str): Text string to hash.

        Returns:
            str: Hex-encoded SHA-256 hash string.
        """
        text_hash = hashlib.sha256(text.encode('utf-8')).hexdigest()
        return text_hash

    @staticmethod
    def hash_uploaded_file(uploaded_file):
        """
        Generate SHA-256 hash from a Django UploadedFile object.

        Args:
            uploaded_file: Django UploadedFile or InMemoryUploadedFile.

        Returns:
            str: Hex-encoded SHA-256 hash string.
        """
        sha256 = hashlib.sha256()
        # Reset file pointer to beginning
        uploaded_file.seek(0)
        for chunk in uploaded_file.chunks():
            sha256.update(chunk)
        # Reset file pointer again for subsequent reads
        uploaded_file.seek(0)
        return sha256.hexdigest()
