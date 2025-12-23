$ErrorActionPreference = "Stop"

$VERSION = (Get-Content pyproject.toml | Select-String 'version').ToString().Split('"')[1]
$OUT = "dist"
$ZIP = "mercury-framework-lite-$VERSION.zip"

Remove-Item $OUT -Recurse -Force -ErrorAction SilentlyContinue
New-Item -ItemType Directory $OUT | Out-Null

$include = @(
    "mercury",
    "mercury_plugins",
    "run.py",
    "cli.py",
    "requirements.txt",
    "README.md",
    "LICENSE",
    "RESPONSIBLE_USE.md",
    "PLUGIN_AUTHOR_GUIDE.md",
    "samples"
)

foreach ($item in $include) {
    Copy-Item $item $OUT -Recurse -Force
}

Compress-Archive -Path "$OUT\*" -DestinationPath $ZIP -Force

Write-Host "Built $ZIP"
