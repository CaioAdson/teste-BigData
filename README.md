# Grupo 4 — Pipeline Big Data para e-commerce

Base do trabalho usando Python no streaming e no batch. O checkpoint completo
da Semana 1 está em [`docs/semana-01.md`](docs/semana-01.md).

`gerador Python → Flume → HDFS → PySpark → Hive`

`dados em streaming → PyFlink → alertas → HBase`

## Ambiente

- Windows 10/11
- WSL 2 com Ubuntu
- Docker Desktop integrado ao WSL
- Recomendado: 12 GB de RAM disponíveis para os contêineres docker compose build flume


## Semana 1 — início rápido

No terminal Ubuntu/WSL:

```bash
docker compose pull
docker compose build flume
docker compose up -d
docker compose ps
```

Valide o checkpoint:

```bash
bash scripts/check-week1.sh
```

Interfaces: Flink em `localhost:8081`, Spark em `localhost:8080` e HDFS em
`localhost:9870`.

## Componentes já preparados

- `generator/gerador.py`: cria cliques, carrinhos, compras e atualizações de entrega.
- `flume/flume-test.conf`: captura com `TAILDIR` e envia ao logger na Semana 1.
- `flume/flume.conf`: configuração planejada para envio ao HDFS posteriormente.
- `flink/job.py`: usa tempo de evento, watermark de 10 segundos e janela deslizante de 1 minuto/20 segundos.
- `spark/etl.py`: calcula vendas por categoria e região; o `groupBy` demonstra wide dependency.
- `hive/schema.sql`: esquema inicial do Data Warehouse.

## Estratégia de integração

O primeiro checkpoint prova `Python → Flume → sink logger`, com HDFS, Flink e
Spark ativos. Depois conectem o Flume ao HDFS, executem o PyFlink e, nas etapas
seguintes, integrem HBase e Hive.

## Divisão sugerida

1. Gerador e modelo JSON
2. Flume e HDFS
3. PyFlink e HBase
4. PySpark e Hive
5. Docker, integração, GitHub e roteiro do vídeo

## Próximos critérios de pronto

- Eventos aparecem continuamente em `data/events.jsonl`.
- Flume registra ingestão sem erro e cria arquivos no HDFS.
- PyFlink imprime alertas de produto em alta.
- HBase contém os alertas.
- PySpark cria `ecommerce.daily_sales` no Hive.
- README final contém comandos reproduzíveis e evidências de teste.

> Esta é uma base inicial. O Docker Compose e o sink HBase ainda dependem da
> combinação de versões aceita no laboratório/aula.
