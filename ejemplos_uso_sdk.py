"""
Script simplificado para extraer información específica de archivos .raw de MassLynx

Ejemplos de uso común para análisis rápidos
"""

import sys
import os

# Agregar el path del SDK
sdk_path = r"c:\Damico\Laboratorio\Software\Prueba\MassLynxSDKDownload_v5.0.0\python_wheel\extracted"
sys.path.insert(0, sdk_path)

from masslynxsdk import (
    MassLynxRawInfoReader,
    MassLynxRawChromatogramReader,
    MassLynxRawScanReader,
    MassLynxHeaderItem,
    MassLynxScanItem
)

# Cargar licencia
def cargar_licencia():
    """Carga el archivo de licencia"""
    import os
    dir_script = os.path.dirname(os.path.abspath(__file__))
    ruta_licencia = os.path.join(dir_script, "license.key")
    
    if not os.path.exists(ruta_licencia):
        sdk_base = os.path.join(dir_script, "MassLynxSDKDownload_v5.0.0")
        ruta_licencia = os.path.join(sdk_base, "license.key")
    
    if os.path.exists(ruta_licencia):
        with open(ruta_licencia, 'r') as f:
            return f.read().strip()
    return ""

LICENCIA = cargar_licencia()


def extraer_info_basica(ruta_raw):
    """
    Extrae información básica del archivo .raw
    
    Returns:
        dict con información básica
    """
    info = MassLynxRawInfoReader(ruta_raw, LICENCIA)
    
    datos = {
        'nombre': info.GetHeaderItemValue([MassLynxHeaderItem.ACQUIRED_NAME]).Get(MassLynxHeaderItem.ACQUIRED_NAME),
        'fecha': info.GetHeaderItemValue([MassLynxHeaderItem.ACQUIRED_DATE]).Get(MassLynxHeaderItem.ACQUIRED_DATE),
        'hora': info.GetHeaderItemValue([MassLynxHeaderItem.ACQUIRED_TIME]).Get(MassLynxHeaderItem.ACQUIRED_TIME),
        'muestra_id': info.GetHeaderItemValue([MassLynxHeaderItem.SAMPLE_ID]).Get(MassLynxHeaderItem.SAMPLE_ID),
        'instrumento': info.GetHeaderItemValue([MassLynxHeaderItem.INSTRUMENT]).Get(MassLynxHeaderItem.INSTRUMENT),
        'vial': info.GetHeaderItemValue([MassLynxHeaderItem.BOTTLE_NUMBER]).Get(MassLynxHeaderItem.BOTTLE_NUMBER),
        'num_funciones': info.GetNumberofFunctions()
    }
    
    return datos


def listar_transiciones_mrm(ruta_raw, funcion=0):
    """
    Lista todas las transiciones MRM de una función
    
    Args:
        ruta_raw: ruta al archivo .raw
        funcion: índice de la función (0-based)
    
    Returns:
        list de dicts con info de cada transición
    """
    info = MassLynxRawInfoReader(ruta_raw, LICENCIA)
    
    # Verificar que es MRM
    tipo = info.GetFunctionTypeString(info.GetFunctionType(funcion))
    if 'MRM' not in tipo.upper():
        print(f"Advertencia: La función {funcion} no es MRM, es {tipo}")
    
    num_mrm = info.GetMRMCount(funcion)
    
    transiciones = []
    for i in range(num_mrm):
        try:
            trans = {
                'numero': i + 1,
                'indice': i
            }
            
            # Intentar obtener parámetros comunes
            try:
                trans['q1'] = float(info.GetScanItemValue(funcion, i, [MassLynxScanItem.SET_MASS]).Get(MassLynxScanItem.SET_MASS))
            except:
                trans['q1'] = None
            
            try:
                trans['energia_colision'] = float(info.GetScanItemValue(funcion, i, [MassLynxScanItem.COLLISION_ENERGY]).Get(MassLynxScanItem.COLLISION_ENERGY))
            except:
                trans['energia_colision'] = None
            
            try:
                trans['voltaje_cono'] = float(info.GetScanItemValue(funcion, i, [MassLynxScanItem.SAMPLING_CONE_VOLTAGE]).Get(MassLynxScanItem.SAMPLING_CONE_VOLTAGE))
            except:
                trans['voltaje_cono'] = None
            
            transiciones.append(trans)
        except Exception as e:
            print(f"Error en transición {i}: {e}")
    
    return transiciones


def extraer_cromatograma_tic(ruta_raw, funcion=0):
    """
    Extrae el cromatograma TIC de una función
    
    Returns:
        tuple (tiempos, intensidades)
    """
    chrom = MassLynxRawChromatogramReader(ruta_raw, LICENCIA)
    tiempos, intensidades = chrom.ReadTIC(funcion)
    return tiempos, intensidades


def extraer_cromatogramas_mrm(ruta_raw, funcion=0):
    """
    Extrae todos los cromatogramas MRM de una función
    
    Returns:
        dict con transiciones como keys y (tiempos, intensidades) como values
    """
    info = MassLynxRawInfoReader(ruta_raw, LICENCIA)
    chrom = MassLynxRawChromatogramReader(ruta_raw, LICENCIA)
    
    num_mrm = info.GetMRMCount(funcion)
    
    cromatogramas = {}
    for i in range(num_mrm):
        tiempos, intensidades = chrom.ReadMRMChromatogram(funcion, i)
        cromatogramas[f'Transicion_{i+1}'] = (tiempos, intensidades)
    
    return cromatogramas


def extraer_espectro_scan(ruta_raw, funcion=0, scan=0):
    """
    Extrae el espectro de un scan específico
    
    Returns:
        tuple (masas, intensidades)
    """
    scan_reader = MassLynxRawScanReader(ruta_raw, LICENCIA)
    masas, intensidades = scan_reader.ReadScan(funcion, scan)
    return masas, intensidades


def obtener_parametros_funcion(ruta_raw, funcion=0):
    """
    Obtiene parámetros de una función
    
    Returns:
        dict con parámetros
    """
    info = MassLynxRawInfoReader(ruta_raw, LICENCIA)
    
    params = {}
    
    # Información básica de la función
    params['tipo'] = info.GetFunctionTypeString(info.GetFunctionType(funcion))
    params['modo_ion'] = info.GetIonModeString(info.GetIonMode(funcion))
    params['num_scans'] = info.GetScansInFunction(funcion)
    
    # Rangos
    low_mass, high_mass = info.GetAcquisitionMassRange(funcion)
    params['rango_masas'] = (low_mass, high_mass)
    
    start_time, end_time = info.GetAcquisitionTimeRange(funcion)
    params['rango_tiempo'] = (start_time, end_time)
    
    params['continuum'] = info.IsContinuum(funcion)
    
    # Si es MRM
    try:
        params['num_transiciones_mrm'] = info.GetMRMCount(funcion)
    except:
        params['num_transiciones_mrm'] = 0
    
    return params


def exportar_mrm_a_csv(ruta_raw, funcion, archivo_salida):
    """
    Exporta todos los cromatogramas MRM de una función a un archivo CSV
    con columnas separadas para cada transición
    
    Args:
        ruta_raw: ruta al archivo .raw
        funcion: índice de la función
        archivo_salida: ruta del archivo CSV de salida
    """
    import csv
    
    info = MassLynxRawInfoReader(ruta_raw, LICENCIA)
    chrom = MassLynxRawChromatogramReader(ruta_raw, LICENCIA)
    
    num_mrm = info.GetMRMCount(funcion)
    
    # Extraer todos los cromatogramas
    datos = {}
    tiempos = None
    
    for i in range(num_mrm):
        t, intensidades = chrom.ReadMRMChromatogram(funcion, i)
        if tiempos is None:
            tiempos = t
        datos[f'Transicion_{i+1}'] = intensidades
    
    # Escribir CSV
    with open(archivo_salida, 'w', newline='') as f:
        writer = csv.writer(f)
        
        # Header
        header = ['Tiempo_min'] + [f'Trans_{i+1}' for i in range(num_mrm)]
        writer.writerow(header)
        
        # Datos
        for i, t in enumerate(tiempos):
            fila = [t] + [datos[f'Transicion_{j+1}'][i] for j in range(num_mrm)]
            writer.writerow(fila)
    
    print(f"Exportado a: {archivo_salida}")


def resumen_completo(ruta_raw):
    """
    Imprime un resumen completo del archivo .raw
    """
    info = MassLynxRawInfoReader(ruta_raw, LICENCIA)
    
    print("=" * 70)
    print("RESUMEN DEL ARCHIVO .RAW")
    print("=" * 70)
    
    # Info básica
    print(f"\nArchivo: {os.path.basename(ruta_raw)}")
    print(f"Nombre: {info.GetHeaderItemValue([MassLynxHeaderItem.ACQUIRED_NAME]).Get(MassLynxHeaderItem.ACQUIRED_NAME)}")
    print(f"Fecha: {info.GetHeaderItemValue([MassLynxHeaderItem.ACQUIRED_DATE]).Get(MassLynxHeaderItem.ACQUIRED_DATE)}")
    print(f"Hora: {info.GetHeaderItemValue([MassLynxHeaderItem.ACQUIRED_TIME]).Get(MassLynxHeaderItem.ACQUIRED_TIME)}")
    print(f"Muestra ID: {info.GetHeaderItemValue([MassLynxHeaderItem.SAMPLE_ID]).Get(MassLynxHeaderItem.SAMPLE_ID)}")
    print(f"Instrumento: {info.GetHeaderItemValue([MassLynxHeaderItem.INSTRUMENT]).Get(MassLynxHeaderItem.INSTRUMENT)}")
    
    # Funciones
    num_func = info.GetNumberofFunctions()
    print(f"\nNúmero de funciones: {num_func}")
    
    for func in range(num_func):
        print(f"\n--- Función {func + 1} ---")
        
        tipo = info.GetFunctionTypeString(info.GetFunctionType(func))
        modo = info.GetIonModeString(info.GetIonMode(func))
        num_scans = info.GetScansInFunction(func)
        
        print(f"  Tipo: {tipo}")
        print(f"  Modo: {modo}")
        print(f"  Scans: {num_scans}")
        
        low_mass, high_mass = info.GetAcquisitionMassRange(func)
        print(f"  Rango de masas: {low_mass:.1f} - {high_mass:.1f} Da")
        
        start_time, end_time = info.GetAcquisitionTimeRange(func)
        print(f"  Rango de tiempo: {start_time:.2f} - {end_time:.2f} min")
        
        # Si es MRM
        try:
            num_mrm = info.GetMRMCount(func)
            if num_mrm > 0:
                print(f"  *** MRM: {num_mrm} transiciones ***")
                
                # Mostrar primeras 5 transiciones
                for i in range(min(5, num_mrm)):
                    try:
                        q1 = float(info.GetScanItemValue(func, i, [MassLynxScanItem.SET_MASS]).Get(MassLynxScanItem.SET_MASS))
                        ce = float(info.GetScanItemValue(func, i, [MassLynxScanItem.COLLISION_ENERGY]).Get(MassLynxScanItem.COLLISION_ENERGY))
                        cone = float(info.GetScanItemValue(func, i, [MassLynxScanItem.SAMPLING_CONE_VOLTAGE]).Get(MassLynxScanItem.SAMPLING_CONE_VOLTAGE))
                        print(f"    Trans {i+1}: Q1={q1:.2f}, CE={ce}V, Cono={cone}V")
                    except:
                        print(f"    Trans {i+1}: parámetros no disponibles")
                
                if num_mrm > 5:
                    print(f"    ... y {num_mrm - 5} transiciones más")
        except:
            pass
    
    print("\n" + "=" * 70)


# ============================================================================
# EJEMPLOS DE USO
# ============================================================================

if __name__ == "__main__":
    # Archivo de ejemplo
    ruta_raw = r"c:\Damico\Laboratorio\Software\Prueba\20251002_20250825 QC3.raw"
    
    # Ejemplo 1: Resumen completo
    print("\n### EJEMPLO 1: Resumen completo ###\n")
    resumen_completo(ruta_raw)
    
    # Ejemplo 2: Info básica
    print("\n\n### EJEMPLO 2: Información básica ###\n")
    info_basica = extraer_info_basica(ruta_raw)
    for key, value in info_basica.items():
        print(f"{key}: {value}")
    
    # Ejemplo 3: Parámetros de función
    print("\n\n### EJEMPLO 3: Parámetros de función 1 ###\n")
    params = obtener_parametros_funcion(ruta_raw, funcion=0)
    for key, value in params.items():
        print(f"{key}: {value}")
    
    # Ejemplo 4: Listar transiciones MRM
    print("\n\n### EJEMPLO 4: Transiciones MRM ###\n")
    transiciones = listar_transiciones_mrm(ruta_raw, funcion=0)
    print(f"Total de transiciones: {len(transiciones)}")
    for trans in transiciones[:5]:  # Mostrar primeras 5
        print(f"  Trans {trans['numero']}: Q1={trans.get('q1', 'N/A')}, "
              f"CE={trans.get('energia_colision', 'N/A')}V, "
              f"Cono={trans.get('voltaje_cono', 'N/A')}V")
    
    # Ejemplo 5: Extraer TIC
    print("\n\n### EJEMPLO 5: Extraer TIC ###\n")
    tiempos_tic, int_tic = extraer_cromatograma_tic(ruta_raw, funcion=0)
    print(f"TIC extraído: {len(tiempos_tic)} puntos")
    print(f"Tiempo: {tiempos_tic[0]:.2f} - {tiempos_tic[-1]:.2f} min")
    print(f"Intensidad máxima: {max(int_tic):.2e}")
    
    # Ejemplo 6: Extraer cromatogramas MRM
    print("\n\n### EJEMPLO 6: Extraer cromatogramas MRM ###\n")
    croms_mrm = extraer_cromatogramas_mrm(ruta_raw, funcion=0)
    print(f"Cromatogramas MRM extraídos: {len(croms_mrm)}")
    for nombre, (tiempos, intensidades) in list(croms_mrm.items())[:3]:
        print(f"  {nombre}: {len(tiempos)} puntos, Imax={max(intensidades):.2e}")
    
    # Ejemplo 7: Exportar MRM a CSV
    print("\n\n### EJEMPLO 7: Exportar MRM a CSV ###\n")
    archivo_csv = r"c:\Damico\Laboratorio\Software\Prueba\cromatogramas_mrm.csv"
    try:
        exportar_mrm_a_csv(ruta_raw, funcion=0, archivo_salida=archivo_csv)
    except Exception as e:
        print(f"Error al exportar: {e}")
    
    print("\n\n✓ Ejemplos completados!")
