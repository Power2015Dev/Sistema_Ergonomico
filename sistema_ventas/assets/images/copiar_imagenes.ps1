# Script para copiar imágenes generadas al proyecto
$src = "C:\Users\EQUIPO DELL\.gemini\antigravity\brain\348f824d-9030-47a2-9c4b-788d81266083"
$dst = "C:\Users\EQUIPO DELL\OneDrive\Documents\GitHub\Sistema_Ergonomico\sistema_ventas\assets\images"

Copy-Item "$src\silla_ergonomica_pro_1783097659670.png"  "$dst\silla-pro.png"  -Force
Copy-Item "$src\escritorio_motorizado_1783097668677.png" "$dst\escritorio.png" -Force
Copy-Item "$src\soporte_monitor_1783097678607.png"       "$dst\soporte.png"    -Force
Copy-Item "$src\hero_workspace_1783097694475.png"        "$dst\hero.png"       -Force
Copy-Item "$src\accesorios_ergo_1783097703874.png"       "$dst\accesorios.png" -Force
Copy-Item "$src\reposapies_ergo_1783097711714.png"       "$dst\reposapies.png" -Force

Write-Host "Imágenes copiadas correctamente."
