"""Voice Mapper Service for automatic voice sample discovery and resolution"""

import logging
import time
from pathlib import Path
from typing import Optional, Dict, List
from api.config import VOICE_SAMPLES_DIR, VOICE_CACHE_TTL

logger = logging.getLogger(__name__)


class VoiceMapper:
    """Service for discovering and resolving voice samples"""

    def __init__(self, voice_samples_dir: Path = VOICE_SAMPLES_DIR):
        """
        Initialize voice mapper

        Args:
            voice_samples_dir: Path to directory containing voice samples
        """
        self.voice_samples_dir = Path(voice_samples_dir)
        self._voice_map: Dict[str, Path] = {}
        self._last_scan_time: float = 0
        self._cache_ttl = VOICE_CACHE_TTL

        # Perform initial scan
        self.scan_voice_samples()

    def scan_voice_samples(self) -> None:
        """Scan voice_samples directory and build voice name to path mapping"""
        current_time = time.time()

        # Skip if cache is still valid
        if current_time - self._last_scan_time < self._cache_ttl:
            return

        logger.info(f"Scanning voice samples directory: {self.voice_samples_dir}")

        self._voice_map.clear()

        if not self.voice_samples_dir.exists():
            logger.warning(
                f"Voice samples directory does not exist: {self.voice_samples_dir}"
            )
            self._last_scan_time = current_time
            return

        # Find all MP3 files
        mp3_files = list(self.voice_samples_dir.glob("*.mp3"))

        for mp3_file in mp3_files:
            # Use stem (filename without extension) as the voice name
            voice_name = mp3_file.stem.lower()

            # Skip empty files
            if mp3_file.stat().st_size == 0:
                logger.debug(f"Skipping empty file: {mp3_file.name}")
                continue

            # Add to mapping
            self._voice_map[voice_name] = mp3_file
            logger.debug(f"Registered voice: {voice_name} -> {mp3_file.name}")

        self._last_scan_time = current_time
        logger.info(f"Discovered {len(self._voice_map)} voice samples")

    def get_voice_path(self, voice_name: str) -> Optional[Path]:
        """
        Resolve a voice name to its file path

        Args:
            voice_name: Name of the voice (e.g., 'aimee', 'facu')

        Returns:
            Path to voice file, or None if not found
        """
        # Refresh cache if needed
        self.scan_voice_samples()

        # Normalize voice name (lowercase, remove .mp3 extension if present)
        normalized_name = voice_name.lower()
        if normalized_name.endswith(".mp3"):
            normalized_name = normalized_name[:-4]

        return self._voice_map.get(normalized_name)

    def list_voice_names(self) -> List[str]:
        """
        Get list of available voice names

        Returns:
            List of voice names (without .mp3 extension)
        """
        # Refresh cache if needed
        self.scan_voice_samples()

        return sorted(self._voice_map.keys())

    def get_voice_info(self, voice_name: str) -> Optional[Dict[str, any]]:
        """
        Get metadata about a voice

        Args:
            voice_name: Name of the voice

        Returns:
            Dictionary with voice metadata, or None if not found
        """
        voice_path = self.get_voice_path(voice_name)

        if voice_path is None:
            return None

        stat = voice_path.stat()

        return {
            "id": voice_name.lower(),
            "name": voice_name.capitalize(),
            "filename": voice_path.name,
            "size_bytes": stat.st_size,
            "size_kb": round(stat.st_size / 1024, 1),
            "path": str(voice_path.absolute()),
        }

    def list_all_voices_info(self) -> List[Dict[str, any]]:
        """
        Get metadata for all available voices

        Returns:
            List of dictionaries with voice metadata
        """
        voices_info = []

        for voice_name in self.list_voice_names():
            info = self.get_voice_info(voice_name)
            if info:
                voices_info.append(info)

        return voices_info


# Global voice mapper instance
_voice_mapper: Optional[VoiceMapper] = None


def get_voice_mapper() -> VoiceMapper:
    """Get global voice mapper instance"""
    global _voice_mapper
    if _voice_mapper is None:
        _voice_mapper = VoiceMapper()
    return _voice_mapper
