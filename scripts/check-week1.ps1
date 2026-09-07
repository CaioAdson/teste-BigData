$ErrorActionPreference = "Stop"
Write-Host "[1/4] Validando o Compose"
docker compose config --quiet
Write-Host "[2/4] Conferindo serviços"
docker compose ps
Write-Host "[3/4] Eventos do gerador"
docker compose logs --tail=3 generator
Write-Host "[4/4] Logs do Flume (procure Event ou Body)"
docker compose logs --tail=30 flume
