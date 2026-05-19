import os
from pathlib import Path
from ml import SGM
from ml import InferenceEngine, load_deployment_vocabularies

ML_DIR = Path(os.environ.get("ML_DIR", "/app/ml"))

word2id, slot_unmap, intent_unmap = load_deployment_vocabularies(str(ML_DIR))
_model = SGM(len(word2id), 300, 128, len(slot_unmap), len(intent_unmap))

engine = InferenceEngine(
    model_path=str(ML_DIR / "weights/best_sgm_model.pth"),
    model_class=_model,
    word2id=word2id,
    intent_unmapping=intent_unmap,
    slot_unmapping=slot_unmap,
    device="cpu",
)