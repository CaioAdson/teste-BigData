#!/usr/bin/env bash
set -euo pipefail
echo "[1/4] Validando o Compose"
docker compose config --quiet
echo "[2/4] Conferindo serviços"
docker compose ps
echo "[3/4] Eventos do gerador"
docker compose logs --tail=3 generator
echo "[4/4] Eventos capturados pelo Flume"
docker compose logs --tail=30 flume | grep -E "Event:|Body:" | tail -5
echo "Checkpoint básico da Semana 1 verificado."
