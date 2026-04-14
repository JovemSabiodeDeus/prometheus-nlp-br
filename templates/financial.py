"""
Gerador de dataset de sentimento financeiro em português brasileiro.
Template-based: sem LLM, sem custo, escala infinita.
"""

import random
from typing import List, Dict

# ── Entidades brasileiras reais ───────────────────────────────────────────────

EMPRESAS = [
    "Petrobras", "Vale", "Itaú Unibanco", "Bradesco", "Ambev",
    "Magazine Luiza", "Localiza", "WEG", "Embraer", "JBS",
    "Natura &Co", "Rede D'Or", "Grupo Pão de Açúcar", "Suzano",
    "Rumo", "Gerdau", "Azul", "GOLL4", "CVC Brasil", "Totvs",
    "Banco do Brasil", "Santander Brasil", "Porto Seguro", "B3",
    "Fleury", "Hapvida", "Intermédica", "BNDES", "Vivo", "Claro",
    "Americanas", "Casas Bahia", "Raia Drogasil", "Arezzo",
    "Hypera Pharma", "3R Petroleum", "PetroRio", "CSAN3", "Brava Energia",
]

SETORES = [
    "o setor financeiro", "o varejo", "o setor de commodities",
    "a indústria petroquímica", "o setor de saúde", "o agronegócio",
    "o mercado de tecnologia", "o setor aéreo", "o mercado imobiliário",
]

PERIODOS = [
    "no terceiro trimestre", "no segundo trimestre", "no primeiro trimestre",
    "no quarto trimestre", "no primeiro semestre", "no segundo semestre",
    "em 2023", "em 2024", "no último exercício fiscal",
]

METRICAS_POSITIVAS = [
    ("receita líquida", ["cresceu {pct}% em relação ao ano anterior",
                          "superou as expectativas do mercado em R$ {val} bilhões",
                          "atingiu R$ {val} bilhões, recorde histórico"]),
    ("EBITDA", ["expandiu {pct}% na comparação anual",
                 "alcançou R$ {val} bilhões, acima do guidance",
                 "registrou margem de {pct}%, superando projeções"]),
    ("lucro líquido", ["cresceu {pct}% frente ao mesmo período do ano passado",
                        "atingiu R$ {val} bilhões, surpreendendo analistas",
                        "foi {pct}% superior às expectativas do consenso"]),
    ("margem bruta", ["se expandiu em {pct} pontos percentuais",
                       "atingiu {pct}%, o maior nível em cinco anos",
                       "cresceu para {pct}% com melhora operacional"]),
]

METRICAS_NEGATIVAS = [
    ("receita líquida", ["caiu {pct}% na comparação anual",
                          "ficou abaixo das projeções em R$ {val} bilhões",
                          "recuou {pct}% impactada pela queda de demanda"]),
    ("EBITDA", ["contraiu {pct}% ano a ano",
                 "decepcionou ao registrar R$ {val} bilhões abaixo do guidance",
                 "foi pressionado pela alta dos custos operacionais"]),
    ("prejuízo", ["totalizou R$ {val} bilhões {periodo}",
                   "atingiu R$ {val} bilhões, o maior em {anos} anos",
                   "surpreendeu negativamente analistas com R$ {val} bilhões"]),
    ("dívida líquida", ["aumentou {pct}% em relação ao trimestre anterior",
                         "pressionou a alavancagem para {pct}x o EBITDA",
                         "cresceu R$ {val} bilhões com novas captações"]),
]

CONTEXTOS_POSITIVOS = [
    "impulsionada pela demanda aquecida",
    "beneficiada pela alta do dólar",
    "com ganhos de eficiência operacional",
    "após reestruturação bem-sucedida",
    "com forte desempenho de vendas",
    "apoiada pela expansão de margens",
    "refletindo a melhora do cenário macroeconômico",
]

CONTEXTOS_NEGATIVOS = [
    "pressionada pela alta da Selic",
    "impactada pela desaceleração do consumo",
    "afetada pela valorização do real",
    "com aumento de custos de insumos",
    "em meio à retração do mercado",
    "impactada pelo cenário fiscal adverso",
    "refletindo a crise de crédito no setor",
]

ANALISTAS = [
    "Analistas do BTG Pactual", "O mercado", "Especialistas do XP Investimentos",
    "Gestores de fundos", "O consenso de mercado", "Analistas da Genial Investimentos",
    "Investidores institucionais", "O sell-side",
]


def _r(template: str) -> str:
    """Preenche template com valores aleatórios."""
    return template.format(
        pct=round(random.uniform(3.0, 45.0), 1),
        val=round(random.uniform(0.5, 12.0), 1),
        anos=random.randint(3, 10),
        periodo=random.choice(PERIODOS),
    )


def _gerar_positivo() -> Dict:
    empresa = random.choice(EMPRESAS)
    metrica, templates = random.choice(METRICAS_POSITIVAS)
    template = random.choice(templates)
    periodo = random.choice(PERIODOS)
    contexto = random.choice(CONTEXTOS_POSITIVOS)

    patterns = [
        f"A {empresa} reportou que a {metrica} {_r(template)} {periodo}, {contexto}.",
        f"{random.choice(ANALISTAS)} avaliam positivamente os resultados da {empresa}: a {metrica} {_r(template)}.",
        f"Resultado sólido da {empresa} {periodo}: {metrica} {_r(template)}, {contexto}.",
        f"A {empresa} divulgou resultados acima do esperado {periodo}. A {metrica} {_r(template)}.",
        f"Ações da {empresa} sobem após divulgação: {metrica} {_r(template)} {contexto}.",
    ]

    return {
        "text": random.choice(patterns),
        "label": "POSITIVO",
        "label_id": 2,
        "empresa": empresa,
        "dominio": "financeiro",
        "idioma": "pt-BR"
    }


def _gerar_negativo() -> Dict:
    empresa = random.choice(EMPRESAS)
    metrica, templates = random.choice(METRICAS_NEGATIVAS)
    template = random.choice(templates)
    periodo = random.choice(PERIODOS)
    contexto = random.choice(CONTEXTOS_NEGATIVOS)

    patterns = [
        f"A {empresa} reportou {metrica} de R$ {round(random.uniform(0.5,8.0),1)} bilhões {periodo}, {contexto}.",
        f"{random.choice(ANALISTAS)} revisam para baixo as estimativas da {empresa}: {metrica} {_r(template)}.",
        f"Resultado abaixo das projeções da {empresa} {periodo}: {metrica} {_r(template)}, {contexto}.",
        f"A {empresa} decepcionou {periodo}. {metrica.capitalize()} {_r(template)} {contexto}.",
        f"Ações da {empresa} recuam após balanço: {metrica} {_r(template)}.",
    ]

    return {
        "text": random.choice(patterns),
        "label": "NEGATIVO",
        "label_id": 0,
        "empresa": empresa,
        "dominio": "financeiro",
        "idioma": "pt-BR"
    }


def _gerar_neutro() -> Dict:
    empresa = random.choice(EMPRESAS)
    periodo = random.choice(PERIODOS)
    setor = random.choice(SETORES)
    val = round(random.uniform(1.0, 20.0), 1)
    pct = round(random.uniform(-2.0, 2.0), 1)

    patterns = [
        f"A {empresa} reportou receita de R$ {val} bilhões {periodo}, em linha com as projeções.",
        f"Resultados da {empresa} vieram dentro do esperado {periodo}, sem grandes surpresas.",
        f"A {empresa} manteve sua participação de mercado em {setor} {periodo}.",
        f"O conselho da {empresa} aprovou a distribuição de dividendos conforme o guidance.",
        f"A {empresa} informou variação de {pct}% no resultado operacional {periodo}, alinhado ao consenso.",
        f"Analistas mantêm recomendação neutra para {empresa} após balanço do {periodo}.",
    ]

    return {
        "text": random.choice(patterns),
        "label": "NEUTRO",
        "label_id": 1,
        "empresa": empresa,
        "dominio": "financeiro",
        "idioma": "pt-BR"
    }


def generate_financial_batch(n: int = 10000) -> List[Dict]:
    """
    Gera n exemplos de sentimento financeiro, balanceados entre
    positivo, negativo e neutro.
    """
    batch = []
    per_class = n // 3

    for _ in range(per_class):
        batch.append(_gerar_positivo())
    for _ in range(per_class):
        batch.append(_gerar_negativo())
    for _ in range(n - 2 * per_class):
        batch.append(_gerar_neutro())

    random.shuffle(batch)
    return batch
