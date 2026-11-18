# Registra as versões do ambiente de execução e testes (manual, seção 9.1, item 4).
# Uso (na raiz do projeto):  powershell -ExecutionPolicy Bypass -File scripts\registrar-ambiente.ps1
# Gera: entrega\01_SISTEMA_ALVO\ambiente.md

$ErrorActionPreference = 'Continue'
$raiz = Split-Path -Parent $PSScriptRoot
$destino = Join-Path $raiz 'entrega\01_SISTEMA_ALVO\ambiente.md'

# Executa o comando e devolve a primeira linha de saída (stdout ou stderr, como "java -version").
function Get-PrimeiraLinha([scriptblock]$comando) {
    try {
        $saida = & $comando 2>&1 | ForEach-Object { "$_" } | Where-Object { $_.Trim() } | Select-Object -First 1
        if ($saida) { return $saida.Trim() }
    } catch { }
    return 'não encontrado'
}

$so = Get-CimInstance Win32_OperatingSystem
$sistema = "$($so.Caption) $($so.Version) ($($so.OSArchitecture))"

$javaHome = $env:JAVA_HOME
$javaExe = if ($javaHome) { Join-Path $javaHome 'bin\java.exe' } else { 'java' }
$java = Get-PrimeiraLinha { & $javaExe -version }

Push-Location $raiz
$maven = Get-PrimeiraLinha { & .\mvnw.cmd -v -q }
Pop-Location

$chromeExe = 'C:\Program Files\Google\Chrome\Application\chrome.exe'
$chrome = if (Test-Path $chromeExe) { (Get-Item $chromeExe).VersionInfo.ProductVersion } else { 'não instalado' }
$firefoxExe = 'C:\Program Files\Mozilla Firefox\firefox.exe'
$firefox = if (Test-Path $firefoxExe) { (Get-Item $firefoxExe).VersionInfo.ProductVersion } else { 'não instalado' }

$git = Get-PrimeiraLinha { git --version }
$node = Get-PrimeiraLinha { node -v }
$npm = Get-PrimeiraLinha { npm -v }
$python = Get-PrimeiraLinha { python --version }
$newman = Get-PrimeiraLinha { newman -v }
$docker = Get-PrimeiraLinha { docker --version }

$data = Get-Date -Format 'yyyy-MM-dd HH:mm'

$conteudo = @"
# Ambiente de execução e testes

Gerado por ``scripts/registrar-ambiente.ps1`` em $data.

| Item | Versão |
|---|---|
| Sistema operacional | $sistema |
| Java (JAVA_HOME) | $java |
| Maven (via Maven Wrapper) | $maven |
| Spring Boot | 3.5.16 (definido no pom.xml) |
| Banco de dados | H2 2.3.232 (embutido; arquivo no perfil dev, memória no perfil test) |
| Git | $git |
| Node.js / npm | $node / $npm |
| Python | $python |
| Google Chrome | $chrome |
| Mozilla Firefox | $firefox |
| ChromeDriver | Resolvido automaticamente pelo Selenium Manager na Fase 7 (registrar a versão usada no log dos testes) |
| Newman | $newman |
| Docker | $docker |
"@

$conteudo | Out-File -FilePath $destino -Encoding utf8
Write-Output "Ambiente registrado em $destino"
