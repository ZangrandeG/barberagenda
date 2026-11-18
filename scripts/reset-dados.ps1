# Restaura a massa de dados fictícios (somente perfis dev e test; exige administrador).
# Uso: powershell -ExecutionPolicy Bypass -File scripts\reset-dados.ps1 [-Url http://localhost:8080]
# Credencial: variáveis ADMIN_LOGIN e ADMIN_SENHA (padrão fictício admin/admin123).
param([string]$Url = 'http://localhost:8080')

$login = if ($env:ADMIN_LOGIN) { $env:ADMIN_LOGIN } else { 'admin' }
$senha = if ($env:ADMIN_SENHA) { $env:ADMIN_SENHA } else { 'admin123' }
$basic = [Convert]::ToBase64String([Text.Encoding]::UTF8.GetBytes("${login}:${senha}"))

$resposta = Invoke-RestMethod -Method Post -Uri "$Url/api/dev/reset" -Headers @{ Authorization = "Basic $basic" }
Write-Output "Dados restaurados: $($resposta.barbeiros) barbeiros, $($resposta.servicos) serviços, $($resposta.clientes) clientes, $($resposta.agendamentos) agendamentos."
