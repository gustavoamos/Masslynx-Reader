# MassLynx Raw Data Reader 📊

Herramienta completa para extraer y analizar datos de archivos `.raw` de **Waters MassLynx**, incluyendo transiciones MRM con toda su información asociada.

![Python](https://img.shields.io/badge/python-3.7+-blue.svg)
![License](https://img.shields.io/badge/license-SDK-green.svg)
![Status](https://img.shields.io/badge/status-production-brightgreen.svg)

---

## 🎯 Características Principales

### ✅ Extracción Completa de Datos MRM
- **Q1 (Masa Precursora)** y **Q3 (Masa Producto)** por transición
- **Nombres de compuestos** (ej: "TTP1-P (LINCL)", "NAGLU-P (MPS III B)")
- **Cone Voltage (CV)** por transición
- **Collision Energy (CE)** por transición
- **Cromatogramas individuales** para cada transición MRM
- **TIC** (Total Ion Chromatogram) y **BPI** (Base Peak Intensity)

### 📊 Información de Header
- Nombre de adquisición
- Fecha y hora
- ID de muestra
- Instrumento
- Código de trabajo
- Usuario

### 🔬 Información de Funciones
- Tipo de función (MRM, MS, MS/MS, etc.)
- Modo de ionización (ES+, ES-, APCI, etc.)
- Número de scans
- Rangos de masa y tiempo
- Modo de datos (Centroide/Continuo)

---

## 🚀 Instalación

### Prerrequisitos
- Python 3.7 o superior
- tkinter (incluido en instalaciones estándar de Python)

### Instalación del SDK de MassLynx
El SDK de MassLynx está incluido en el repositorio. Solo necesitas:

1. Clonar el repositorio:
```bash
git clone https://github.com/gustavoamos/Masslynx-Reader.git
cd Masslynx-Reader
```

2. Asegurarte de tener el archivo `license.key` válido

¡Listo! No se requieren dependencias adicionales.

---

## 💻 Uso

### Opción 1: Interfaz Gráfica (Recomendada)

```bash
python interfaz_masslynx.py
```

1. Click en **"Seleccionar Archivo..."** → Elegir carpeta `.raw`
2. Click en **"🔍 Analizar Archivo"**
3. Click en **"💾 Exportar a CSV"** (opcional)

![GUI Screenshot](docs/screenshot_gui.png)

---

### Opción 2: Desde Python

```python
from analizar_raw_masslynx import AnalizadorRawMassLynx

# Crear analizador
analizador = AnalizadorRawMassLynx("ruta/al/archivo.raw")

# Análisis completo (muestra en consola)
analizador.analisis_completo()

# Exportar a CSV
analizador.exportar_cromatogramas_csv("salida.csv")
```

---

### Opción 3: Funciones de Utilidad

```python
from ejemplos_uso_sdk import (
    extraer_info_basica,
    listar_transiciones_mrm,
    extraer_cromatogramas_mrm,
    exportar_mrm_a_csv
)

# Extraer información básica
info = extraer_info_basica("archivo.raw")
print(f"Nombre: {info['nombre']}")
print(f"Fecha: {info['fecha']}")

# Listar transiciones MRM
transiciones = listar_transiciones_mrm("archivo.raw", funcion=0)
for t in transiciones:
    print(f"{t['transicion']}: {t['nombre']}")

# Extraer cromatogramas
cromatogramas = extraer_cromatogramas_mrm("archivo.raw", funcion=0)

# Exportar todo a CSV
exportar_mrm_a_csv("archivo.raw", funcion=0, archivo_salida="datos.csv")
```

---

## 📊 Ejemplo de Salida

### Transiciones MRM Extraídas

```
MRM   Q1         Q3         Transición      CV     CE     Nombre/Compuesto                
==========================================================================================
1     350.2000   250.2000   350.20>250.20   20     12     TTP1-P (LINCL)                  
2     359.3000   251.2000   359.30>251.20   20     12     TPP1-IS                         
3     420.2000   311.2000   420.20>311.20   25     13     NAGLU-P (MPS III B)             
4     423.2000   314.2000   423.20>314.20   25     13     NAGLU-IS                        
5     434.3000   325.3000   434.30>325.30   25     15     GUSB-P (MPS VII)                
...
```

### Archivo CSV Generado

```csv
Tiempo_min,Trans_1,Trans_2,Trans_3,Trans_4,...
0.0000,12450,8920,15600,22100,...
0.0043,13200,9150,16200,23500,...
0.0086,14100,9800,17100,24800,...
...
```

---

## 🔧 Solución Técnica

### Problema Original
Los métodos estándar del SDK de MassLynx no proporcionaban información individual por transición MRM:
- Todas las transiciones mostraban la misma Q1>Q3
- CE y CV retornaban valores vacíos
- No había acceso a nombres de compuestos

### Solución Implementada

1. **Masas Q1>Q3**: Llamada directa a la DLL con parámetro `whichMRM`
   ```python
   getAcquisitionMassRange = MassLynxProvider.MassLynxDll.getAcquisitionMassRange
   code = getAcquisitionMassRange(reader_ptr, funcion, mrm_idx, lowMass, highMass)
   ```

2. **Nombres de Compuestos**: Lectura del archivo binario `_FUNC001.CMP`
   ```python
   strings_ascii = re.findall(b'([ -~]{4,})', content)
   nombres = [s.decode('ascii').strip() for s in strings_ascii]
   ```

3. **CE y CV**: Decodificación del archivo binario `_FUNC001.EE`
   ```python
   # Formato: pares de uint16 (CV1, CE1, CV2, CE2, ...)
   energias = struct.unpack('<H', datos[i:i+2])
   ```

---

## 📁 Estructura del Proyecto

```
Masslynx-Reader/
├── analizar_raw_masslynx.py       # Clase principal del analizador
├── interfaz_masslynx.py            # Interfaz gráfica (GUI)
├── ejemplos_uso_sdk.py             # Funciones de utilidad
├── license.key                     # Licencia del SDK
├── LEER_PRIMERO.md                 # Guía rápida en español
├── README.md                       # Este archivo
└── MassLynxSDKDownload_v5.0.0/     # SDK de MassLynx
    └── python_wheel/
        └── extracted/
            └── masslynxsdk/        # Módulo Python del SDK
```

---

## 📖 Documentación

- **[LEER_PRIMERO.md](LEER_PRIMERO.md)** - Guía rápida de inicio
- **[README_SDK_MassLynx.md](README_SDK_MassLynx.md)** - Documentación técnica del SDK
- **[PROYECTO_LIMPIO.md](PROYECTO_LIMPIO.md)** - Detalles de optimización del proyecto

---

## 🧪 Validado Con

**Archivo de prueba**: MRM con 18 transiciones
- Funciones: 1
- Tipo: MRM (Multiple Reaction Monitoring)
- Modo: ES+ (Electrospray Positivo)
- Transiciones: 18
- Scans: 467
- Tiempo: 0.00 - 1.99 min
- Instrumento: XEVO-TQSmicro

**Resultados**: ✅ 100% de datos extraídos correctamente

---

## 🛠️ Tecnologías

- **Python 3.7+**
- **MassLynx SDK v5.0.0** (Waters Corporation)
- **tkinter** (GUI)
- **ctypes** (Acceso directo a DLL)
- **struct** (Decodificación binaria)
- **re** (Expresiones regulares)

---

## 📝 Notas Importantes

1. Un archivo `.raw` de MassLynx es en realidad una **carpeta** que contiene múltiples archivos binarios
2. La información de transiciones MRM está distribuida en varios archivos:
   - `_FUNC001.CMP` - Nombres de compuestos
   - `_FUNC001.EE` - Energías (CE/CV)
   - Archivos `.DAT` - Datos espectrales
3. Se requiere un archivo `license.key` válido del SDK de MassLynx

---

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor:

1. Fork el repositorio
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

---

## 📄 Licencia

Este proyecto utiliza el SDK de MassLynx de Waters Corporation. Consulta el archivo de licencia del SDK para más detalles.

---

## 👤 Autor

**Gustavo Amos**
- GitHub: [@gustavoamos](https://github.com/gustavoamos)

---

## 🙏 Agradecimientos

- Waters Corporation por el SDK de MassLynx
- Comunidad de Python científico

---

## 📞 Soporte

Si encuentras algún problema o tienes preguntas:
1. Abre un [Issue](https://github.com/gustavoamos/Masslynx-Reader/issues)
2. Consulta la [documentación](LEER_PRIMERO.md)

---

**⭐ Si este proyecto te fue útil, considera darle una estrella en GitHub!**
