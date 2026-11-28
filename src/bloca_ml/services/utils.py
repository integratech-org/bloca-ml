from pathlib import Path
from typing import Any

import joblib
from ai_edge_litert.interpreter import Interpreter
from huggingface_hub import hf_hub_download
from loguru import logger


class HFFileDownloader:
    def __init__(
        self,
        repo_id: str,
        repo_revision: str,
        model_directory: Path,
    ) -> None:
        self.repo_id = repo_id
        self.repo_revision = repo_revision
        self.target_dir = Path(model_directory) / repo_revision

    def ensure(self, filename: str) -> Path:
        path = self.target_dir / filename
        if path.exists():
            logger.debug(f"[+] {path} already exists, skipping download")
            return path

        logger.info(
            f"[+] Downloading {filename} from {self.repo_id}@{self.repo_revision}"
        )
        self.target_dir.mkdir(parents=True, exist_ok=True)
        try:
            hf_hub_download(
                repo_id=self.repo_id,
                filename=filename,
                revision=self.repo_revision,
                local_dir=str(self.target_dir),
            )
        except Exception as exc:
            raise RuntimeError(
                f"Failed to download {filename} from {self.repo_id}@{self.repo_revision}"
            ) from exc

        if not path.exists():
            raise RuntimeError(
                f"Download of {filename} from {self.repo_id}@{self.repo_revision} finished but {path} was not found"
            )

        logger.info(f"[+] Downloaded {filename} to {path}")
        return path


class JoblibModelLoader:
    def __init__(self, downloader: HFFileDownloader, filename: str) -> None:
        self.downloader = downloader
        self.filename = filename

    def load(self) -> Any:
        path = self.downloader.ensure(self.filename)
        model = joblib.load(path)
        logger.info(f"[+] Loaded joblib model from {path}")
        return model


class TFLiteModelLoader:
    def __init__(self, downloader: HFFileDownloader, filename: str) -> None:
        self.downloader = downloader
        self.filename = filename

    def load(self) -> Interpreter:
        path = self.downloader.ensure(self.filename)
        interpreter = Interpreter(model_path=str(path))
        interpreter.allocate_tensors()
        logger.info(f"[+] Loaded TFLite model from {path}")
        return interpreter
