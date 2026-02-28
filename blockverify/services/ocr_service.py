"""
services/ocr_service.py
OCR text extraction service using Gemma AI.

Provides a unified interface for OCR:
    - Uses real Gemma AI API when GEMMA_API_KEY is set.
    - Falls back to mock OCR when key is 'mock' or missing.

To switch from mock to real API:
    1. Get a Gemma API key from Google AI Studio.
    2. Set GEMMA_API_KEY in your .env file.
    3. The service will automatically use the real API.
"""

import os
import hashlib
import logging
from pathlib import Path
from django.conf import settings

logger = logging.getLogger(__name__)


class MockOCR:
    """
    Mock OCR implementation for development/testing.
    Extracts a deterministic pseudo-text from the file contents
    so that the same file always produces the same OCR output.
    """

    @staticmethod
    def extract_text(file_path):
        """
        Generate mock OCR text from file.
        Uses file bytes to create reproducible output.

        Args:
            file_path (str): Path to the certificate file.

        Returns:
            str: Mock extracted text.
        """
        try:
            with open(file_path, 'rb') as f:
                content = f.read()

            # Generate deterministic "extracted text" from file content
            file_hash = hashlib.md5(content).hexdigest()
            file_name = Path(file_path).stem
            file_size = len(content)

            mock_text = (
                f"[Mock OCR Output]\n"
                f"Document: {file_name}\n"
                f"File Size: {file_size} bytes\n"
                f"Content Fingerprint: {file_hash}\n"
                f"---\n"
                f"CERTIFICATE OF ACHIEVEMENT\n"
                f"This is to certify that the student has successfully\n"
                f"completed the required coursework and examinations.\n"
                f"Document ID: {file_hash[:12].upper()}\n"
                f"Verification Code: BV-{file_hash[:8].upper()}\n"
            )
            return mock_text

        except Exception as e:
            logger.error(f"Mock OCR extraction failed: {e}")
            return f"[OCR Error] Could not process file: {e}"


class GemmaOCR:
    """
    Real Gemma AI OCR implementation.
    Uses Google's Generative AI API for text extraction.
    """

    def __init__(self, api_key):
        self.api_key = api_key

    def extract_text(self, file_path):
        """
        Extract text from certificate using Gemma AI.

        Args:
            file_path (str): Path to the certificate file.

        Returns:
            str: Extracted text from the document.
        """
        try:
            import google.generativeai as genai

            genai.configure(api_key=self.api_key)
            model = genai.GenerativeModel('gemini-1.5-flash')

            # Read the file
            file_ext = Path(file_path).suffix.lower()

            if file_ext in ['.pdf']:
                # Upload PDF to Gemini
                uploaded_file = genai.upload_file(file_path)
                response = model.generate_content([
                    "Extract all text from this document. "
                    "Return only the extracted text, no commentary.",
                    uploaded_file
                ])
            elif file_ext in ['.png', '.jpg', '.jpeg', '.gif', '.bmp', '.webp']:
                # Upload image to Gemini
                uploaded_file = genai.upload_file(file_path)
                response = model.generate_content([
                    "Extract all text from this image. "
                    "Return only the extracted text, no commentary.",
                    uploaded_file
                ])
            else:
                return f"[Unsupported file type: {file_ext}]"

            return response.text

        except ImportError:
            logger.warning(
                "google-generativeai not installed. "
                "Falling back to mock OCR."
            )
            return MockOCR.extract_text(file_path)

        except Exception as e:
            logger.error(f"Gemma AI OCR failed: {e}")
            # Fallback to mock on API error
            logger.info("Falling back to mock OCR.")
            return MockOCR.extract_text(file_path)


class OCRService:
    """
    Unified OCR service interface.

    Automatically selects the appropriate OCR backend
    based on the GEMMA_API_KEY environment variable.

    Usage:
        text = OCRService.extract_text('/path/to/certificate.pdf')
    """

    _engine = None

    @classmethod
    def _get_engine(cls):
        """Get or initialize the OCR engine."""
        if cls._engine is None:
            api_key = getattr(settings, 'GEMMA_API_KEY', 'mock')
            if api_key and api_key != 'mock':
                cls._engine = GemmaOCR(api_key)
                logger.info("Using Gemma AI OCR engine.")
            else:
                cls._engine = MockOCR()
                logger.info("Using Mock OCR engine.")
        return cls._engine

    @classmethod
    def extract_text(cls, file_path):
        """
        Extract text from a certificate file.

        Args:
            file_path (str): Absolute path to the certificate file.

        Returns:
            str: Extracted text from the document.
        """
        engine = cls._get_engine()
        text = engine.extract_text(file_path)
        logger.info(
            f"OCR extracted {len(text)} characters from "
            f"{Path(file_path).name}"
        )
        return text

    @classmethod
    def reset_engine(cls):
        """Reset the engine (useful for testing or config changes)."""
        cls._engine = None
