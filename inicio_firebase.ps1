# 🚀 INICIO RÁPIDO - Despliegue Firebase

Write-Host ""
Write-Host "╔════════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║                                                            ║" -ForegroundColor Cyan
Write-Host "║        🔥 LIBRERÍA JODA - DESPLIEGUE FIREBASE 🔥          ║" -ForegroundColor Cyan
Write-Host "║                                                            ║" -ForegroundColor Cyan
Write-Host "╚════════════════════════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""

$opcion = Read-Host @"

¿Qué deseas hacer?

1. 📋 Verificar requisitos pre-despliegue
2. 💾 Exportar datos actuales (BACKUP)
3. 🚀 Desplegar aplicación en Firebase
4. 📥 Importar datos después de despliegue
5. 📚 Ver guías de ayuda
6. ❌ Salir

Selecciona una opción (1-6)
"@

switch ($opcion) {
    "1" {
        Write-Host ""
        Write-Host "🔍 Ejecutando verificación..." -ForegroundColor Cyan
        .\verificar_despliegue.ps1
    }
    "2" {
        Write-Host ""
        Write-Host "💾 Exportando datos..." -ForegroundColor Cyan
        python exportar_datos.py
        Write-Host ""
        Write-Host "✅ Backup completado" -ForegroundColor Green
        Write-Host "📁 Archivo guardado en el directorio actual" -ForegroundColor Gray
    }
    "3" {
        Write-Host ""
        Write-Host "⚠️  IMPORTANTE: ¿Ya hiciste backup de tus datos? (S/N)" -ForegroundColor Yellow
        $backup = Read-Host
        
        if ($backup -eq "S" -or $backup -eq "s") {
            Write-Host ""
            Write-Host "🚀 Iniciando despliegue..." -ForegroundColor Cyan
            .\deploy.ps1
        } else {
            Write-Host ""
            Write-Host "⚠️  Por favor, primero haz backup con la opción 2" -ForegroundColor Yellow
        }
    }
    "4" {
        Write-Host ""
        $archivos = Get-ChildItem -Filter "datos_backup_*.json" | Sort-Object LastWriteTime -Descending
        
        if ($archivos.Count -eq 0) {
            Write-Host "❌ No se encontraron archivos de backup" -ForegroundColor Red
            Write-Host "   Primero exporta tus datos con la opción 2" -ForegroundColor Yellow
        } else {
            Write-Host "📁 Archivos de backup encontrados:" -ForegroundColor Cyan
            Write-Host ""
            
            for ($i = 0; $i -lt $archivos.Count; $i++) {
                Write-Host "   $($i+1). $($archivos[$i].Name) - $($archivos[$i].LastWriteTime)" -ForegroundColor Gray
            }
            
            Write-Host ""
            $seleccion = Read-Host "Selecciona el archivo a importar (1-$($archivos.Count))"
            
            if ($seleccion -match '^\d+$' -and [int]$seleccion -ge 1 -and [int]$seleccion -le $archivos.Count) {
                $archivoSeleccionado = $archivos[[int]$seleccion - 1].Name
                Write-Host ""
                Write-Host "📥 Importando datos desde: $archivoSeleccionado" -ForegroundColor Cyan
                python importar_datos.py $archivoSeleccionado
            } else {
                Write-Host "❌ Selección inválida" -ForegroundColor Red
            }
        }
    }
    "5" {
        Write-Host ""
        Write-Host "📚 GUÍAS DISPONIBLES:" -ForegroundColor Cyan
        Write-Host ""
        Write-Host "1. README_FIREBASE.md - Arquitectura y conceptos" -ForegroundColor Gray
        Write-Host "2. INICIO_RAPIDO_DESPLIEGUE.md - Pasos rápidos" -ForegroundColor Gray
        Write-Host "3. GUIA_DESPLIEGUE_FIREBASE.md - Guía completa detallada" -ForegroundColor Gray
        Write-Host ""
        
        $guia = Read-Host "¿Qué guía deseas abrir? (1-3, Enter para ninguna)"
        
        switch ($guia) {
            "1" { Start-Process "README_FIREBASE.md" }
            "2" { Start-Process "INICIO_RAPIDO_DESPLIEGUE.md" }
            "3" { Start-Process "GUIA_DESPLIEGUE_FIREBASE.md" }
        }
    }
    "6" {
        Write-Host ""
        Write-Host "👋 ¡Hasta pronto!" -ForegroundColor Green
        Write-Host ""
        exit
    }
    default {
        Write-Host ""
        Write-Host "❌ Opción inválida" -ForegroundColor Red
    }
}

Write-Host ""
Write-Host "Presiona Enter para continuar..."
Read-Host
.\inicio_firebase.ps1
