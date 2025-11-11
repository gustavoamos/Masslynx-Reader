# Documentación del SDK de MassLynx para análisis de archivos .raw

## Descripción General

Este documento describe cómo usar el SDK de MassLynx v5.0.0 para extraer información de archivos `.raw` generados por instrumentos Waters MassLynx.

## Estructura del SDK

El SDK de MassLynx proporciona las siguientes clases principales:

### Clases de Lectura (Readers)

1. **MassLynxRawInfoReader** - Información general del archivo
   - Número de funciones
   - Tipo de función (MS, MRM, SIR, etc.)
   - Rangos de masa y tiempo
   - Modo de ionización
   - Parámetros de adquisición

2. **MassLynxRawChromatogramReader** - Lectura de cromatogramas
   - TIC (Total Ion Chromatogram)
   - BPI (Base Peak Intensity)
   - Cromatogramas de masa específica
   - Cromatogramas MRM

3. **MassLynxRawScanReader** - Lectura de espectros
   - Espectros de masa completos
   - Espectros con drift time
   - Espectros de productos

4. **MassLynxRawAnalogReader** - Lectura de canales analógicos
   - Trazas de detectores analógicos (UV, ELSD, etc.)

### Clases de Procesamiento

1. **MassLynxDDAProcessor** - Procesamiento de datos DDA
2. **MassLynxLockMassProcessor** - Corrección de lock mass
3. **MassLynxScanProcessor** - Procesamiento de scans
4. **MassLynxParameters** - Gestión de parámetros
5. **MassLynxLicense** - Gestión de licencias

## Información que se puede extraer

### 1. Información del Header (Encabezado)

```python
from masslynxsdk import MassLynxRawInfoReader, MassLynxHeaderItem

info_reader = MassLynxRawInfoReader("ruta/al/archivo.raw")

# Información básica
nombre_adquisicion = info_reader.GetHeaderItemValue(MassLynxHeaderItem.ACQUIRED_NAME)
fecha = info_reader.GetHeaderItemValue(MassLynxHeaderItem.ACQUIRED_DATE)
hora = info_reader.GetHeaderItemValue(MassLynxHeaderItem.ACQUIRED_TIME)
sample_id = info_reader.GetHeaderItemValue(MassLynxHeaderItem.SAMPLE_ID)
instrumento = info_reader.GetHeaderItemValue(MassLynxHeaderItem.INSTRUMENT)
```

**Items disponibles del header:**
- `ACQUIRED_NAME` - Nombre de la adquisición
- `ACQUIRED_DATE` - Fecha
- `ACQUIRED_TIME` - Hora
- `SAMPLE_ID` - ID de muestra
- `SAMPLE_DESCRIPTION` - Descripción
- `INSTRUMENT` - Nombre del instrumento
- `JOB_CODE` - Código de trabajo
- `USER_NAME` - Usuario
- `BOTTLE_NUMBER` - Número de vial
- `INLET_METHOD` - Método de inlet
- Y muchos más...

### 2. Información de Funciones

```python
# Obtener número de funciones
num_funciones = info_reader.GetNumberofFunctions()

# Para cada función
for func in range(num_funciones):
    # Tipo de función
    tipo = info_reader.GetFunctionType(func)
    tipo_str = info_reader.GetFunctionTypeString(tipo)
    
    # Modo de ionización
    ion_mode = info_reader.GetIonMode(func)
    ion_mode_str = info_reader.GetIonModeString(ion_mode)
    
    # Número de scans
    num_scans = info_reader.GetScansInFunction(func)
    
    # Rango de masas
    low_mass, high_mass = info_reader.GetAcquisitionMassRange(func)
    
    # Rango de tiempo
    start_time, end_time = info_reader.GetAcquisitionTimeRange(func)
    
    # Continuum o centroide
    is_continuum = info_reader.IsContinuum(func)
```

**Tipos de función disponibles:**
- `MS` - Full scan
- `MRM` - Multiple Reaction Monitoring
- `SIR` - Selected Ion Recording
- `TOF` - Time of Flight
- `DAUGHTER` - MS/MS
- Y muchos más...

**Modos de ionización:**
- `ES_POS` - Electrospray positivo
- `ES_NEG` - Electrospray negativo
- `CI_POS` - Chemical Ionization positivo
- `CI_NEG` - Chemical Ionization negativo
- Etc.

### 3. Parámetros de Scans (Energías y Voltajes)

```python
from masslynxsdk import MassLynxScanItem

# Para un scan específico en una función
funcion = 0
scan = 0

# Energía de colisión
energia_colision = info_reader.GetScanItemValue(funcion, scan, MassLynxScanItem.COLLISION_ENERGY)

# Voltaje de cono (sampling cone)
voltaje_cono = info_reader.GetScanItemValue(funcion, scan, MassLynxScanItem.SAMPLING_CONE_VOLTAGE)

# Temperatura de fuente
temp_fuente = info_reader.GetScanItemValue(funcion, scan, MassLynxScanItem.SOURCE_TEMPERATURE)

# Voltaje RF
rf_voltage = info_reader.GetScanItemValue(funcion, scan, MassLynxScanItem.RF_VOLTAGE)

# Multiplicadores
mult1 = info_reader.GetScanItemValue(funcion, scan, MassLynxScanItem.MULTIPLIER1)
mult2 = info_reader.GetScanItemValue(funcion, scan, MassLynxScanItem.MULTIPLIER2)

# Para MRM: masa configurada (precursor)
set_mass = info_reader.GetScanItemValue(funcion, scan, MassLynxScanItem.SET_MASS)

# TIC del scan
tic = info_reader.GetScanItemValue(funcion, scan, MassLynxScanItem.TOTAL_ION_CURRENT)

# Pico base
base_peak_mass = info_reader.GetScanItemValue(funcion, scan, MassLynxScanItem.BASE_PEAK_MASS)
base_peak_int = info_reader.GetScanItemValue(funcion, scan, MassLynxScanItem.BASE_PEAK_INTENSITY)
```

**Parámetros importantes disponibles:**
- `COLLISION_ENERGY` - Energía de colisión (eV)
- `COLLISION_ENERGY2` - Energía de colisión 2
- `SAMPLING_CONE_VOLTAGE` - Voltaje de cono (V)
- `SOURCE_TEMPERATURE` - Temperatura de fuente
- `PROBE_TEMPERATURE` - Temperatura de sonda
- `RF_VOLTAGE` - Voltaje RF
- `MULTIPLIER1` / `MULTIPLIER2` - Multiplicadores
- `SET_MASS` - Masa configurada (Q1 en MRM)
- `ION_ENERGY` - Energía de iones
- `TOTAL_ION_CURRENT` - TIC
- `BASE_PEAK_MASS` - Masa del pico base
- `BASE_PEAK_INTENSITY` - Intensidad del pico base
- Y muchos más (ver MassLynxScanItem en MassLynxRawDefs.py)

### 4. Transiciones MRM

```python
# Obtener número de transiciones MRM
num_mrm = info_reader.GetMRMCount(funcion)

# Para cada transición MRM, los parámetros están en los scans
# Generalmente cada scan corresponde a una transición en orden
for mrm_idx in range(num_mrm):
    # Masa precursora (Q1)
    q1_mass = info_reader.GetScanItemValue(funcion, mrm_idx, MassLynxScanItem.SET_MASS)
    
    # Energía de colisión para esta transición
    ce = info_reader.GetScanItemValue(funcion, mrm_idx, MassLynxScanItem.COLLISION_ENERGY)
    
    # Voltaje de cono
    cone = info_reader.GetScanItemValue(funcion, mrm_idx, MassLynxScanItem.SAMPLING_CONE_VOLTAGE)
```

### 5. Cromatogramas

```python
from masslynxsdk import MassLynxRawChromatogramReader

chrom_reader = MassLynxRawChromatogramReader("ruta/al/archivo.raw")

# TIC (Total Ion Chromatogram)
tiempos_tic, intensidades_tic = chrom_reader.ReadTIC(funcion)

# BPI (Base Peak Intensity)
tiempos_bpi, intensidades_bpi = chrom_reader.ReadBPI(funcion)

# Cromatograma de una masa específica
masa = 500.0
ventana = 0.5  # Da
productos = False  # True para iones producto
tiempos, intensidades = chrom_reader.ReadMassChromatogram(funcion, masa, ventana, productos)

# Cromatogramas de múltiples masas
masas = [100.0, 200.0, 300.0]
ventana = 0.5
tiempos, lista_intensidades = chrom_reader.ReadMassChromatograms(funcion, masas, ventana, productos)

# Cromatograma MRM individual
transicion = 0  # índice de la transición
tiempos_mrm, intensidades_mrm = chrom_reader.ReadMRMChromatogram(funcion, transicion)

# Múltiples cromatogramas MRM
transiciones = [0, 1, 2]  # índices
tiempos, lista_int_mrm = chrom_reader.ReadMRMChromatograms(funcion, transiciones)
```

### 6. Espectros de Masas

```python
from masslynxsdk import MassLynxRawScanReader

scan_reader = MassLynxRawScanReader("ruta/al/archivo.raw")

# Leer un espectro completo
funcion = 0
scan = 100
masas, intensidades = scan_reader.ReadScan(funcion, scan)

# Leer espectro con flags
masas, intensidades, flags = scan_reader.ReadScanFlags(funcion, scan)

# Para datos con drift time (IMS)
drift = 0
masas, intensidades = scan_reader.ReadDriftScan(funcion, scan, drift)

# Espectro de productos
masas, intensidades, masas_producto = scan_reader.ReadProductScan(funcion, scan)
```

### 7. Tiempo de Retención

```python
# Obtener tiempo de retención de un scan específico
funcion = 0
scan = 100
tiempo_retencion = info_reader.GetRetentionTime(funcion, scan)

# Obtener rango de scans para un rango de tiempo
start_time = 5.0  # minutos
end_time = 10.0
start_scan, end_scan = info_reader.GetScanRange(funcion, start_time, end_time)
```

## Ejemplo Completo: Análisis de archivo MRM

```python
from masslynxsdk import (
    MassLynxRawInfoReader,
    MassLynxRawChromatogramReader,
    MassLynxHeaderItem,
    MassLynxScanItem
)

# Inicializar lectores
ruta_raw = "C:/datos/muestra.raw"
info_reader = MassLynxRawInfoReader(ruta_raw)
chrom_reader = MassLynxRawChromatogramReader(ruta_raw)

# Información básica
nombre = info_reader.GetHeaderItemValue(MassLynxHeaderItem.ACQUIRED_NAME)
sample_id = info_reader.GetHeaderItemValue(MassLynxHeaderItem.SAMPLE_ID)

print(f"Analizando: {nombre} (ID: {sample_id})")

# Obtener funciones
num_funciones = info_reader.GetNumberofFunctions()

for func in range(num_funciones):
    tipo = info_reader.GetFunctionTypeString(info_reader.GetFunctionType(func))
    print(f"\nFunción {func+1}: {tipo}")
    
    # Si es MRM, analizar transiciones
    num_mrm = info_reader.GetMRMCount(func)
    if num_mrm > 0:
        print(f"  Transiciones MRM: {num_mrm}")
        
        for mrm_idx in range(num_mrm):
            # Extraer parámetros
            q1 = info_reader.GetScanItemValue(func, mrm_idx, MassLynxScanItem.SET_MASS)
            ce = info_reader.GetScanItemValue(func, mrm_idx, MassLynxScanItem.COLLISION_ENERGY)
            cone = info_reader.GetScanItemValue(func, mrm_idx, MassLynxScanItem.SAMPLING_CONE_VOLTAGE)
            
            print(f"    Transición {mrm_idx+1}: Q1={q1:.2f}, CE={ce}V, Cono={cone}V")
            
            # Extraer cromatograma
            tiempos, intensidades = chrom_reader.ReadMRMChromatogram(func, mrm_idx)
            max_int = max(intensidades) if len(intensidades) > 0 else 0
            print(f"      Puntos: {len(tiempos)}, Imax: {max_int:.2e}")
```

## Manejo de Errores

```python
from masslynxsdk import MassLynxException

try:
    info_reader = MassLynxRawInfoReader("archivo.raw")
    num_funciones = info_reader.GetNumberofFunctions()
except MassLynxException as e:
    print(f"Error del SDK: {e}")
except Exception as e:
    print(f"Error general: {e}")
```

## Notas Importantes

1. **Rutas de archivos**: Los archivos `.raw` de MassLynx son en realidad carpetas que contienen múltiples archivos binarios.

2. **Índices**: Los índices de funciones y scans comienzan en 0.

3. **Unidades**:
   - Tiempos: minutos
   - Masas: Da (Daltons)
   - Energías: eV (electronvoltios)
   - Voltajes: V (voltios)
   - Temperaturas: °C

4. **Disponibilidad de datos**: No todos los parámetros están disponibles en todos los tipos de funciones. Usar try/except para manejar parámetros no disponibles.

5. **Licencia**: Algunos usuarios pueden requerir un archivo de licencia válido.

## Estructura de un archivo .raw

Un archivo `.raw` de MassLynx es una carpeta que contiene:
- `_HEADER.TXT` - Información del header en texto
- `_FUNCTNS.INF` - Información de funciones (binario)
- `_FUNC001.DAT`, `_FUNC002.DAT`, etc. - Datos de cada función
- `_FUNC001.IDX` - Índices de scans
- `_INLET.INF` - Información del inlet
- Y otros archivos de metadatos

## Scripts de Ejemplo

El script `analizar_raw_masslynx.py` proporciona:
- Clase `AnalizadorRawMassLynx` para análisis completo
- Extracción de toda la información disponible
- Exportación a CSV de cromatogramas
- Informes detallados

### Uso básico:

```python
from analizar_raw_masslynx import AnalizadorRawMassLynx

# Crear analizador
analizador = AnalizadorRawMassLynx("ruta/al/archivo.raw")

# Análisis completo
resultados = analizador.analisis_completo(extraer_espectros=True)

# Exportar a CSV
analizador.exportar_cromatogramas_csv(resultados, "carpeta_salida")
```

## Referencias

- SDK Version: 5.0.0
- Documentación HTML incluida en: `MasslynxSDK help zip/extracted_help/python_help/`
- Headers C++: `cpp_headers/`

## Soporte

Para más información sobre el SDK de MassLynx, consultar:
- Documentación oficial de Waters
- Headers C++ en `cpp_headers/` para detalles de implementación
- Archivos de ayuda HTML incluidos en el SDK
