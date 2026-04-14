"""
PROMETHEUS — Autonomous Portuguese AI Data Forge
Gerador principal de datasets. Roda via GitHub Actions diariamente.
Sem LLM externo. Sem custo. Sem intervenção humana.
"""

import json
import random
import datetime
import os
import sys
import hashlib
from pathlib import Path

# Fix encoding para Windows (cp1252 não suporta emoji)
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

from templates.financial import generate_financial_batch
from templates.legal import generate_legal_batch
from templates.customer_service import generate_customer_service_batch
from quality_check import validate_and_deduplicate

OUTPUT_DIR = Path("datasets")
OUTPUT_DIR.mkdir(exist_ok=True)

MANIFEST_FILE = Path("MANIFEST.json")


def save_jsonl(data: list, filepath: Path) -> int:
    """Salva lista de exemplos em formato JSONL."""
    with open(filepath, "w", encoding="utf-8") as f:
        for item in data:
            f.write(json.dumps(item, ensure_ascii=False) + "\n")
    return len(data)


def compute_hash(filepath: Path) -> str:
    """Hash SHA256 do arquivo para verificação de integridade."""
    h = hashlib.sha256()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def update_manifest(entries: list):
    """Atualiza o manifesto com metadados de cada release."""
    manifest = []
    if MANIFEST_FILE.exists():
        with open(MANIFEST_FILE, "r", encoding="utf-8") as f:
            manifest = json.load(f)

    manifest.extend(entries)
    # Mantém apenas os últimos 90 dias
    manifest = manifest[-90:]

    with open(MANIFEST_FILE, "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)


def generate_all():
    date_str = datetime.date.today().isoformat()
    run_id = f"{date_str}-{random.randint(1000,9999)}"
    entries = []

    print(f"\n{'='*60}")
    print(f"  PROMETHEUS — Run {run_id}")
    print(f"{'='*60}\n")

    # ── 1. Financial Sentiment ────────────────────────────────
    print("[FINANCIAL] Gerando dataset de sentimento financeiro...")
    financial_raw = generate_financial_batch(n=12000)
    financial_clean = validate_and_deduplicate(financial_raw)
    fp = OUTPUT_DIR / f"financial_sentiment_{date_str}.jsonl"
    save_jsonl(financial_clean, fp)
    h = compute_hash(fp)
    size_kb = fp.stat().st_size // 1024
    print(f"   OK: {len(financial_clean):,} exemplos | {size_kb} KB | SHA256: {h[:12]}...")
    entries.append({
        "date": date_str, "type": "financial_sentiment",
        "count": len(financial_clean), "file": fp.name,
        "sha256": h, "size_kb": size_kb
    })

    # ── 2. Named Entity Recognition ──────────────────────────
    print("[LEGAL NER] Gerando dataset NER juridico-empresarial...")
    legal_raw = generate_legal_batch(n=8000)
    legal_clean = validate_and_deduplicate(legal_raw)
    fp = OUTPUT_DIR / f"legal_ner_{date_str}.jsonl"
    save_jsonl(legal_clean, fp)
    h = compute_hash(fp)
    size_kb = fp.stat().st_size // 1024
    print(f"   OK: {len(legal_clean):,} exemplos | {size_kb} KB | SHA256: {h[:12]}...")
    entries.append({
        "date": date_str, "type": "legal_ner",
        "count": len(legal_clean), "file": fp.name,
        "sha256": h, "size_kb": size_kb
    })

    # ── 3. Customer Service Dialogues ────────────────────────
    print("[CUSTOMER SERVICE] Gerando dataset de atendimento ao cliente...")
    cs_raw = generate_customer_service_batch(n=8000)
    cs_clean = validate_and_deduplicate(cs_raw)
    fp = OUTPUT_DIR / f"customer_service_{date_str}.jsonl"
    save_jsonl(cs_clean, fp)
    h = compute_hash(fp)
    size_kb = fp.stat().st_size // 1024
    print(f"   OK: {len(cs_clean):,} exemplos | {size_kb} KB | SHA256: {h[:12]}...")
    entries.append({
        "date": date_str, "type": "customer_service",
        "count": len(cs_clean), "file": fp.name,
        "sha256": h, "size_kb": size_kb
    })

    update_manifest(entries)

    total = sum(e["count"] for e in entries)
    total_kb = sum(e["size_kb"] for e in entries)

    print(f"\n{'='*60}")
    print(f"  GERACAO CONCLUIDA")
    print(f"  Total: {total:,} exemplos | {total_kb:,} KB")
    print(f"  Manifesto atualizado: {MANIFEST_FILE}")
    print(f"{'='*60}\n")

    return total


if __name__ == "__main__":
    generate_all()
