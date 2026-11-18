# Restaura a massa de dados fictícios (somente perfis dev e test).
# Uso: powershell -ExecutionPolicy Bypass -File scripts\reset-dados.ps1 [-Url http://localhost:8080]
param([string]$Url = 'http://localhost:8080')

$resposta = Invoke-RestMethod -Method Post -Uri "$Url/api/dev/reset"
Write-Output "Dados restaurados: $($resposta.barbeiros) barbeiros, $($resposta.servicos) serviços, $($resposta.clientes) clientes, $($resposta.agendamentos) agendamentos."
