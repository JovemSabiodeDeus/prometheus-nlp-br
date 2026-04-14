# 🔥 PROMETHEUS — Autonomous Portuguese NLP Dataset Factory

> **Fábrica autônoma de datasets de NLP em português brasileiro.**
> Zero custo. Zero intervenção humana. Geração diária automática.

---

## 📊 Datasets Disponíveis

| Dataset | Exemplos/dia | Formato | Domínio |
|---|---|---|---|
| **Financial Sentiment** | ~12.000 | JSONL | Análise de sentimento financeiro |
| **Legal NER** | ~8.000 | JSONL (BIO) | Named Entity Recognition jurídico |
| **Customer Service Dialogues** | ~8.000 | JSONL | Diálogos de atendimento ao cliente |

**Total diário: ~28.000 exemplos únicos em português brasileiro (pt-BR)**

---

## 🚀 Como Funciona

```
GitHub Actions (cron diário — 03:00 UTC)
├── Executa generate.py (Python puro, sem API externa)
│   ├── templates/financial.py    → sentimento financeiro
│   ├── templates/legal.py        → NER jurídico (formato BIO)
│   └── templates/customer_service.py → diálogos de atendimento
├── quality_check.py → validação + deduplicação automática
├── Publica como GitHub Release (download público)
├── [Opcional] Upload para AWS S3
└── Atualiza MANIFEST.json com histórico
```

---

## 📦 Formato dos Dados

### Financial Sentiment
```json
{
  "text": "A Petrobras reportou que a receita líquida cresceu 23.5% ...",
  "label": "POSITIVO",
  "label_id": 2,
  "empresa": "Petrobras",
  "dominio": "financeiro",
  "idioma": "pt-BR"
}
```

### Legal NER (formato BIO)
```json
{
  "text": "O contrato celebrado entre João Silva e Vale S.A. ...",
  "tokens_bio": [{"token": "O", "tag": "O"}, {"token": "João", "tag": "B-PER"}, ...],
  "entities": [{"text": "João Silva", "label": "PER"}, {"text": "Vale S.A.", "label": "ORG"}],
  "dominio": "juridico",
  "idioma": "pt-BR"
}
```

### Customer Service Dialogues
```json
{
  "dialogo": [
    {"role": "user", "content": "Olá, preciso bloquear meu cartão urgente!"},
    {"role": "agent", "content": "Sem problema! Vou bloquear agora preventivamente..."}
  ],
  "categoria": "bloqueio_cartao",
  "intencao": "bloquear_cartao",
  "resolucao": "cartao_bloqueado",
  "setor": "bancario",
  "idioma": "pt-BR"
}
```

---

## 🛠️ Executar Localmente

```bash
# Instalar dependências
pip install -r requirements.txt

# Gerar datasets
python generate.py

# Resultado: pasta datasets/ com 3 arquivos JSONL
```

---

## 📈 Características

- ✅ **100% autônomo** — roda via GitHub Actions sem intervenção
- ✅ **Zero custo** — sem LLM, sem API paga, sem servidor
- ✅ **Português brasileiro nativo** — textos realistas com entidades brasileiras
- ✅ **Validação automática** — deduplicação + controle de qualidade
- ✅ **Formato padrão** — compatível com HuggingFace, spaCy, PyTorch
- ✅ **Rastreável** — MANIFEST.json com hash SHA256 de cada release
- ✅ **Escala infinita** — templates expansíveis, sem limite de geração

---

## 📋 Licença

Consultar termos de uso para dados comerciais.

---

*PROMETHEUS — O sistema que acorda antes de você, trabalha enquanto você dorme, e deposita enquanto você não olha.*
