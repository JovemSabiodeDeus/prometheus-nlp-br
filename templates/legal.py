"""
Gerador de dataset NER (Named Entity Recognition) jurídico-empresarial.
Formato BIO (Begin-Inside-Outside) compatível com spaCy, HuggingFace Transformers.
"""

import random
from typing import List, Dict, Tuple

# ── Entidades ────────────────────────────────────────────────────────────────

NOMES_MASCULINOS = [
    "João Silva", "Carlos Eduardo Mendes", "Roberto Alves", "Fernando Costa",
    "Antônio Pereira", "Marcos Souza", "Rafael Lima", "Lucas Oliveira",
    "André Santos", "Paulo Ferreira", "Ricardo Rodrigues", "Gustavo Martins",
    "Eduardo Carvalho", "Felipe Barbosa", "Thiago Ribeiro", "Daniel Gomes",
    "Pedro Henrique Nascimento", "Leonardo Cavalcante", "Rodrigo Azevedo",
]

NOMES_FEMININOS = [
    "Maria Aparecida Costa", "Ana Paula Ferreira", "Carla Rodrigues",
    "Fernanda Lima", "Patricia Santos", "Juliana Oliveira", "Camila Alves",
    "Beatriz Mendes", "Larissa Pereira", "Vanessa Souza", "Daniela Martins",
    "Adriana Costa", "Renata Barbosa", "Cristiane Ribeiro", "Sandra Gomes",
    "Luciana Carvalho", "Simone Nascimento", "Mariana Cavalcante",
]

NOMES = NOMES_MASCULINOS + NOMES_FEMININOS

ORGANIZACOES = [
    "Petrobras S.A.", "Vale S.A.", "Itaú Unibanco Holding S.A.",
    "Bradesco S.A.", "Banco do Brasil S.A.", "Ambev S.A.",
    "Magazine Luiza S.A.", "Ministério da Fazenda", "Receita Federal do Brasil",
    "Tribunal de Justiça de São Paulo", "Superior Tribunal de Justiça",
    "Supremo Tribunal Federal", "BNDES", "Banco Central do Brasil",
    "Comissão de Valores Mobiliários", "Anatel", "CADE",
    "Escritório Jurídico Mendes & Associados", "Construtora ABC Ltda.",
    "Farmacêutica Brasileira S.A.", "Tech Solutions Brasil Ltda.",
    "Distribuidora Nacional de Alimentos Ltda.", "Transportadora Silva & Cia.",
]

CIDADES = [
    "São Paulo", "Rio de Janeiro", "Brasília", "Salvador", "Belo Horizonte",
    "Fortaleza", "Curitiba", "Manaus", "Recife", "Porto Alegre",
    "Belém", "Goiânia", "Campinas", "São Luís", "Maceió",
    "Natal", "Teresina", "Campo Grande", "João Pessoa", "Aracaju",
]

ESTADOS = [
    "São Paulo", "Rio de Janeiro", "Minas Gerais", "Bahia", "Paraná",
    "Rio Grande do Sul", "Pernambuco", "Ceará", "Pará", "Goiás",
]

VALORES = [
    "R$ 12.500,00", "R$ 45.000,00", "R$ 1.200.000,00", "R$ 350.000,00",
    "R$ 78.500,00", "R$ 2.500.000,00", "R$ 150.000,00", "R$ 890.000,00",
    "R$ 5.000.000,00", "R$ 23.000,00", "R$ 430.000,00",
]

DATAS = [
    "15 de março de 2023", "3 de julho de 2024", "22 de janeiro de 2023",
    "10 de setembro de 2024", "1º de abril de 2023", "28 de fevereiro de 2024",
    "5 de novembro de 2023", "17 de junho de 2024", "30 de outubro de 2023",
    "12 de agosto de 2024",
]


def _anotar_entidades(texto: str, entidades: List[Tuple[str, str]]) -> List[Dict]:
    """
    Converte texto e lista de (entidade, tipo) em tokens anotados no formato BIO.
    Retorna lista de {token, tag}.
    """
    tokens = texto.split()
    tags = ["O"] * len(tokens)

    for entidade, tipo in entidades:
        partes = entidade.split()
        for i in range(len(tokens)):
            if tokens[i : i + len(partes)] == partes:
                tags[i] = f"B-{tipo}"
                for j in range(1, len(partes)):
                    if i + j < len(tokens):
                        tags[i + j] = f"I-{tipo}"

    return [{"token": t, "tag": g} for t, g in zip(tokens, tags)]


def _gerar_contrato() -> Dict:
    parte1 = random.choice(NOMES)
    parte2 = random.choice(ORGANIZACOES)
    cidade = random.choice(CIDADES)
    valor = random.choice(VALORES)
    data = random.choice(DATAS)

    templates = [
        f"O contrato celebrado entre {parte1} e {parte2} em {cidade} prevê o pagamento de {valor} até {data}.",
        f"Fica estabelecido que {parte2}, com sede em {cidade}, deverá indenizar {parte1} no valor de {valor} até {data}.",
        f"Em {data}, {parte1} firmou acordo com {parte2} no valor de {valor}, a ser executado em {cidade}.",
        f"A cláusula 5ª determina que {parte2} pagará a {parte1} o montante de {valor} até {data}.",
    ]

    texto = random.choice(templates)
    entidades = [(parte1, "PER"), (parte2, "ORG"), (cidade, "LOC"),
                 (valor, "MON"), (data, "DAT")]

    return {
        "text": texto,
        "tokens_bio": _anotar_entidades(texto, entidades),
        "entities": [{"text": e, "label": t} for e, t in entidades if e in texto],
        "dominio": "juridico",
        "idioma": "pt-BR"
    }


def _gerar_sentenca_judicial() -> Dict:
    juiz = random.choice(NOMES)
    parte_a = random.choice(NOMES)
    parte_b = random.choice(ORGANIZACOES)
    cidade = random.choice(CIDADES)
    valor = random.choice(VALORES)
    data = random.choice(DATAS)
    estado = random.choice(ESTADOS)

    templates = [
        f"O juiz {juiz}, da {random.choice(['1ª', '2ª', '3ª', '5ª'])} Vara Cível de {cidade}, {estado}, condenou {parte_b} a pagar {valor} a {parte_a}.",
        f"Em {data}, o magistrado {juiz} julgou procedente a ação movida por {parte_a} contra {parte_b}, arbitrando indenização de {valor}.",
        f"A sentença proferida pelo Dr. {juiz} em {cidade} determinou que {parte_b} ressarça {parte_a} em {valor}.",
        f"O Tribunal de Justiça de {estado}, sob relatoria do Dr. {juiz}, manteve a condenação de {parte_b} ao pagamento de {valor} a {parte_a}.",
    ]

    texto = random.choice(templates)
    entidades = [(juiz, "PER"), (parte_a, "PER"), (parte_b, "ORG"),
                 (cidade, "LOC"), (valor, "MON"), (data, "DAT"), (estado, "LOC")]

    return {
        "text": texto,
        "tokens_bio": _anotar_entidades(texto, entidades),
        "entities": [{"text": e, "label": t} for e, t in entidades if e in texto],
        "dominio": "juridico",
        "idioma": "pt-BR"
    }


def _gerar_nota_fiscal() -> Dict:
    empresa = random.choice(ORGANIZACOES)
    cidade = random.choice(CIDADES)
    valor = random.choice(VALORES)
    data = random.choice(DATAS)

    templates = [
        f"A nota fiscal emitida por {empresa}, em {data}, no valor de {valor}, foi registrada em {cidade}.",
        f"Conforme NF-e emitida em {data} por {empresa} ({cidade}), o valor total da operação é de {valor}.",
        f"O documento fiscal de {empresa} com data de {data} refere-se a prestação de serviços no valor de {valor} em {cidade}.",
    ]

    texto = random.choice(templates)
    entidades = [(empresa, "ORG"), (cidade, "LOC"), (valor, "MON"), (data, "DAT")]

    return {
        "text": texto,
        "tokens_bio": _anotar_entidades(texto, entidades),
        "entities": [{"text": e, "label": t} for e, t in entidades if e in texto],
        "dominio": "fiscal",
        "idioma": "pt-BR"
    }


def generate_legal_batch(n: int = 8000) -> List[Dict]:
    """Gera n exemplos NER de domínio jurídico-fiscal."""
    generators = [_gerar_contrato, _gerar_sentenca_judicial, _gerar_nota_fiscal]
    batch = []
    for _ in range(n):
        fn = random.choice(generators)
        batch.append(fn())
    random.shuffle(batch)
    return batch
