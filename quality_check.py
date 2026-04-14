"""
Validação e deduplicação automática de datasets.
Garante qualidade sem intervenção humana.
"""

import re
import hashlib
from typing import List, Dict


def _hash_texto(texto: str) -> str:
    """Hash para detecção de duplicatas."""
    return hashlib.md5(texto.lower().strip().encode("utf-8")).hexdigest()


def _extrair_texto(item: Dict) -> str:
    """Extrai o campo textual principal de qualquer tipo de item."""
    if "text" in item:
        return item["text"]
    if "dialogo" in item:
        return " ".join(m["content"] for m in item["dialogo"])
    return ""


def _validar_item(item: Dict) -> tuple:
    """
    Valida um único item. Retorna (valido: bool, motivo: str).
    """
    texto = _extrair_texto(item)

    # Comprimento mínimo e máximo
    if len(texto) < 40:
        return False, "texto_curto"
    if len(texto) > 1500:
        return False, "texto_longo"

    # Deve conter caracteres portugueses básicos
    if not re.search(r"[a-záéíóúàâêîôãõç]", texto.lower()):
        return False, "sem_portugues"

    # Não pode ser só números
    if re.fullmatch(r"[\d\s\.,R$%/-]+", texto):
        return False, "so_numeros"

    # Deve ter pelo menos 5 palavras
    if len(texto.split()) < 5:
        return False, "poucas_palavras"

    # Verificações por tipo de dataset
    if "label" in item:
        if item["label"] not in ("POSITIVO", "NEGATIVO", "NEUTRO"):
            return False, "label_invalido"

    if "tokens_bio" in item:
        bio = item["tokens_bio"]
        if not isinstance(bio, list) or len(bio) == 0:
            return False, "bio_vazio"

    if "dialogo" in item:
        d = item["dialogo"]
        if not isinstance(d, list) or len(d) < 2:
            return False, "dialogo_incompleto"
        for msg in d:
            if "role" not in msg or "content" not in msg:
                return False, "dialogo_formato_invalido"
            if len(msg["content"]) < 10:
                return False, "mensagem_curta"

    return True, "ok"


def validate_and_deduplicate(batch: List[Dict]) -> List[Dict]:
    """
    Valida e deduplica um batch de exemplos.
    Retorna apenas exemplos válidos e únicos.
    """
    seen_hashes = set()
    clean = []
    stats = {"total": len(batch), "invalidos": 0, "duplicatas": 0, "aceitos": 0}

    for item in batch:
        # Validação
        valido, motivo = _validar_item(item)
        if not valido:
            stats["invalidos"] += 1
            continue

        # Deduplicação
        texto = _extrair_texto(item)
        h = _hash_texto(texto)
        if h in seen_hashes:
            stats["duplicatas"] += 1
            continue

        seen_hashes.add(h)
        clean.append(item)
        stats["aceitos"] += 1

    taxa = stats["aceitos"] / stats["total"] * 100 if stats["total"] > 0 else 0
    print(f"   QC: {stats['aceitos']:,}/{stats['total']:,} aceitos ({taxa:.1f}%) | "
          f"{stats['invalidos']} inválidos | {stats['duplicatas']} duplicatas")

    return clean
