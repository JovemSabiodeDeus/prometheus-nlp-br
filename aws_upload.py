"""
Upload automático para AWS S3.
Os dados publicados aqui alimentam o AWS Data Exchange.
Roda como parte do pipeline do GitHub Actions.

SETUP (uma única vez):
  pip install boto3
  aws configure  (insira suas credenciais)
"""

import os
import json
import datetime
from pathlib import Path

try:
    import boto3
    from botocore.exceptions import ClientError, NoCredentialsError
    BOTO_DISPONIVEL = True
except ImportError:
    BOTO_DISPONIVEL = False

BUCKET_NAME = os.environ.get("AWS_S3_BUCKET", "prometheus-datasets-br")
REGION = os.environ.get("AWS_REGION", "us-east-1")


def _criar_bucket_se_necessario(s3_client, bucket: str, region: str):
    """Cria o bucket S3 caso não exista (operação idempotente)."""
    try:
        s3_client.head_bucket(Bucket=bucket)
    except ClientError as e:
        if e.response["Error"]["Code"] == "404":
            if region == "us-east-1":
                s3_client.create_bucket(Bucket=bucket)
            else:
                s3_client.create_bucket(
                    Bucket=bucket,
                    CreateBucketConfiguration={"LocationConstraint": region},
                )
            # Habilita versionamento
            s3_client.put_bucket_versioning(
                Bucket=bucket,
                VersioningConfiguration={"Status": "Enabled"},
            )
            print(f"✅ Bucket criado: s3://{bucket}")
        else:
            raise


def upload_datasets(datasets_dir: Path = Path("datasets")):
    """
    Faz upload de todos os arquivos JSONL do dia para o S3.
    Retorna lista de URLs dos arquivos enviados.
    """
    if not BOTO_DISPONIVEL:
        print("⚠️  boto3 não instalado. Pulando upload AWS.")
        print("   Para instalar: pip install boto3")
        return []

    try:
        s3 = boto3.client("s3", region_name=REGION)
        _criar_bucket_se_necessario(s3, BUCKET_NAME, REGION)
    except NoCredentialsError:
        print("⚠️  Credenciais AWS não configuradas. Pulando upload.")
        print("   Configure via: aws configure OU variáveis AWS_ACCESS_KEY_ID + AWS_SECRET_ACCESS_KEY")
        return []

    date_str = datetime.date.today().isoformat()
    uploaded = []

    jsonl_files = list(datasets_dir.glob(f"*{date_str}*.jsonl"))
    if not jsonl_files:
        print("⚠️  Nenhum arquivo JSONL encontrado para upload.")
        return []

    for filepath in jsonl_files:
        s3_key = f"datasets/{date_str}/{filepath.name}"
        try:
            s3.upload_file(
                str(filepath),
                BUCKET_NAME,
                s3_key,
                ExtraArgs={
                    "ContentType": "application/json",
                    "Metadata": {
                        "generated-by": "prometheus-autonomous",
                        "date": date_str,
                        "project": "portuguese-nlp-datasets"
                    }
                }
            )
            url = f"s3://{BUCKET_NAME}/{s3_key}"
            uploaded.append(url)
            size_kb = filepath.stat().st_size // 1024
            print(f"   ✅ Enviado: {filepath.name} ({size_kb} KB) → {url}")
        except Exception as e:
            print(f"   ❌ Erro ao enviar {filepath.name}: {e}")

    # Atualiza index.json no S3 com todos os datasets disponíveis
    if uploaded:
        _atualizar_index(s3, date_str, uploaded)

    return uploaded


def _atualizar_index(s3_client, date_str: str, new_files: list):
    """Mantém um index.json público com todos os datasets disponíveis."""
    index_key = "index.json"
    try:
        response = s3_client.get_object(Bucket=BUCKET_NAME, Key=index_key)
        index = json.loads(response["Body"].read())
    except Exception:
        index = {"datasets": [], "updated_at": ""}

    index["datasets"].append({
        "date": date_str,
        "files": new_files,
        "count": len(new_files)
    })
    index["datasets"] = index["datasets"][-90:]  # mantém últimos 90 dias
    index["updated_at"] = datetime.datetime.utcnow().isoformat()

    s3_client.put_object(
        Bucket=BUCKET_NAME,
        Key=index_key,
        Body=json.dumps(index, ensure_ascii=False, indent=2),
        ContentType="application/json"
    )
    print(f"   📋 Index atualizado: s3://{BUCKET_NAME}/{index_key}")


if __name__ == "__main__":
    urls = upload_datasets()
    if urls:
        print(f"\n✅ {len(urls)} arquivos enviados para AWS S3")
    else:
        print("\n⚠️  Nenhum arquivo enviado (verifique configuração AWS)")
