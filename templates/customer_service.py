"""
Gerador de diálogos de atendimento ao cliente em português brasileiro.
Cobre: banco, telecom, e-commerce, saúde, seguros, energia.
"""

import random
from typing import List, Dict

# ── Dados base ───────────────────────────────────────────────────────────────

NOMES_CLIENTES = [
    "João", "Maria", "Carlos", "Ana", "Ricardo", "Fernanda",
    "Pedro", "Juliana", "Rafael", "Camila", "Marcos", "Beatriz",
    "Lucas", "Larissa", "Gabriel", "Patricia", "Rodrigo", "Vanessa",
]

NUMEROS_PROTOCOLO = lambda: f"{random.randint(100000,999999)}"
VALORES_FATURA = lambda: f"R$ {random.randint(50,2500)},{random.randint(10,99):02d}"
DATAS_VENC = lambda: f"{random.randint(1,28):02d}/{random.randint(1,12):02d}/2024"
PLANOS = ["básico", "intermediário", "premium", "empresarial", "família"]
OPERADORAS = ["Vivo", "Claro", "TIM", "Oi", "NET"]
BANCOS = ["Itaú", "Bradesco", "Nubank", "Banco do Brasil", "Santander", "Caixa"]
ECOMMERCES = ["Mercado Livre", "Amazon", "Shopee", "Americanas", "Magazine Luiza"]
SEGURADORAS = ["Porto Seguro", "Bradesco Seguros", "SulAmérica", "Allianz"]


def _dialogo_bancario() -> Dict:
    nome = random.choice(NOMES_CLIENTES)
    banco = random.choice(BANCOS)
    valor = VALORES_FATURA()
    protocolo = NUMEROS_PROTOCOLO()

    categorias = [
        {
            "categoria": "contestacao_cobranca",
            "intencao": "contestar_cobranca",
            "user": f"Olá, meu nome é {nome}. Apareceu uma cobrança de {valor} na minha fatura que eu não reconheço. Preciso cancelar isso.",
            "agent": f"Olá, {nome}! Entendo sua preocupação. Vou verificar essa cobrança agora mesmo. Pode me informar o mês de referência da fatura em que apareceu? Vou registrar sua contestação com o protocolo {protocolo} e o estorno será processado em até 5 dias úteis após análise.",
            "resolucao": "contestacao_registrada"
        },
        {
            "categoria": "bloqueio_cartao",
            "intencao": "bloquear_cartao",
            "user": f"Preciso bloquear meu cartão urgente! Acho que perdi na rua.",
            "agent": f"Sem problema, {nome}! Vou bloquear agora preventivamente. Já está feito. Protocolo: {protocolo}. Deseja solicitar um novo cartão? A entrega é em até 10 dias úteis no endereço cadastrado.",
            "resolucao": "cartao_bloqueado"
        },
        {
            "categoria": "transferencia_pix",
            "intencao": "suporte_pix",
            "user": f"Fiz um PIX de {valor} e o dinheiro saiu da minha conta mas não chegou no destinatário. Já faz 30 minutos.",
            "agent": f"Oi {nome}! O PIX pode levar até 60 segundos normalmente, mas em casos de suspeita de fraude, o banco destinatário pode reter por até 30 minutos. Abri o protocolo {protocolo}. Se não resolver em 1 hora, o valor retorna à sua conta automaticamente.",
            "resolucao": "monitoramento_ativo"
        },
        {
            "categoria": "limite_credito",
            "intencao": "solicitar_aumento_limite",
            "user": f"Quero aumentar o limite do meu cartão. Estou há 3 anos com o {banco} sem inadimplência.",
            "agent": f"Que ótimo, {nome}! Seu histórico é excelente. Posso solicitar uma análise de crédito agora. O processo leva até 3 dias úteis e você receberá a resposta por SMS e email. Protocolo {protocolo}. Posso prosseguir?",
            "resolucao": "analise_solicitada"
        },
    ]

    dialogo = random.choice(categorias)
    return {
        "dialogo": [
            {"role": "user", "content": dialogo["user"]},
            {"role": "agent", "content": dialogo["agent"]},
        ],
        "categoria": dialogo["categoria"],
        "intencao": dialogo["intencao"],
        "resolucao": dialogo["resolucao"],
        "setor": "bancario",
        "idioma": "pt-BR"
    }


def _dialogo_telecom() -> Dict:
    nome = random.choice(NOMES_CLIENTES)
    operadora = random.choice(OPERADORAS)
    plano = random.choice(PLANOS)
    valor = VALORES_FATURA()
    protocolo = NUMEROS_PROTOCOLO()

    categorias = [
        {
            "categoria": "internet_lenta",
            "intencao": "reclamacao_servico",
            "user": f"A internet da {operadora} está muito lenta desde ontem. Não consigo nem abrir um site direito.",
            "agent": f"Oi {nome}! Lamento o inconveniente. Estou verificando a sua linha agora. Identificamos uma instabilidade na sua região que já está sendo corrigida pela equipe técnica. Prazo de normalização: 4 horas. Protocolo: {protocolo}. Caso persista, podemos agendar visita técnica sem custo.",
            "resolucao": "incidente_registrado"
        },
        {
            "categoria": "troca_plano",
            "intencao": "upgrade_plano",
            "user": f"Quero mudar para o plano {plano}. Quanto custa?",
            "agent": f"Olá {nome}! O plano {plano} da {operadora} custa {valor} por mês e inclui internet ilimitada, ligações gratuitas e mais benefícios. A migração é sem custo e entra em vigor no próximo ciclo. Posso realizar a mudança agora?",
            "resolucao": "troca_realizada"
        },
        {
            "categoria": "fatura_contestada",
            "intencao": "contestar_fatura",
            "user": f"Minha fatura veio {valor} mais cara que o normal e não entendo o motivo.",
            "agent": f"Vou verificar, {nome}! Analisando... Identifiquei que houve cobrança de serviço adicional ativado. Vou cancelar e solicitar crédito na próxima fatura. Protocolo {protocolo}. O crédito aparecerá em até 2 ciclos de cobrança.",
            "resolucao": "credito_solicitado"
        },
    ]

    dialogo = random.choice(categorias)
    return {
        "dialogo": [
            {"role": "user", "content": dialogo["user"]},
            {"role": "agent", "content": dialogo["agent"]},
        ],
        "categoria": dialogo["categoria"],
        "intencao": dialogo["intencao"],
        "resolucao": dialogo["resolucao"],
        "setor": "telecom",
        "idioma": "pt-BR"
    }


def _dialogo_ecommerce() -> Dict:
    nome = random.choice(NOMES_CLIENTES)
    loja = random.choice(ECOMMERCES)
    protocolo = NUMEROS_PROTOCOLO()
    valor = VALORES_FATURA()
    data = DATAS_VENC()

    categorias = [
        {
            "categoria": "rastreamento_pedido",
            "intencao": "rastrear_pedido",
            "user": f"Fiz uma compra no {loja} e está constando 'em trânsito' há 8 dias. O prazo era de 5 dias úteis.",
            "agent": f"Oi {nome}! Verificando seu pedido agora. O pacote está na transportadora desde {data} aguardando rota de entrega. Abri reclamação com protocolo {protocolo}. A transportadora tem 48h para resolver. Se não entregar, processamos reenvio ou reembolso integral de {valor}.",
            "resolucao": "reclamacao_transportadora"
        },
        {
            "categoria": "troca_produto",
            "intencao": "solicitar_troca",
            "user": f"Recebi o produto errado. Pedi tamanho M e vieram dois tamanhos G.",
            "agent": f"Que situação desagradável, {nome}! Já estou abrindo o processo de troca. Protocolo: {protocolo}. A coleta do produto errado será agendada para os próximos 2 dias úteis, sem custo algum. O correto chegará em até 7 dias após a coleta.",
            "resolucao": "troca_aprovada"
        },
        {
            "categoria": "cancelamento",
            "intencao": "cancelar_pedido",
            "user": f"Quero cancelar meu pedido e receber meu dinheiro de volta. Paguei {valor} e não recebi nada ainda.",
            "agent": f"Cancelado agora mesmo, {nome}! Protocolo {protocolo}. O reembolso de {valor} será processado em até 5 dias úteis no mesmo método de pagamento utilizado. Receberá confirmação por email.",
            "resolucao": "cancelamento_realizado"
        },
    ]

    dialogo = random.choice(categorias)
    return {
        "dialogo": [
            {"role": "user", "content": dialogo["user"]},
            {"role": "agent", "content": dialogo["agent"]},
        ],
        "categoria": dialogo["categoria"],
        "intencao": dialogo["intencao"],
        "resolucao": dialogo["resolucao"],
        "setor": "ecommerce",
        "idioma": "pt-BR"
    }


def generate_customer_service_batch(n: int = 8000) -> List[Dict]:
    """Gera n diálogos de atendimento ao cliente em múltiplos setores."""
    generators = [_dialogo_bancario, _dialogo_telecom, _dialogo_ecommerce]
    batch = [random.choice(generators)() for _ in range(n)]
    random.shuffle(batch)
    return batch
