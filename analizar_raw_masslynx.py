"""
Script para extraer información completa de archivos .raw de MassLynx
Extrae: nombres de cromatogramas, transiciones MRM, energías de cono/colisión,
datos de cromatogramas, y toda la información relevante del análisis.

Autor: Análisis del SDK de MassLynx v5.0.0
"""

import sys
import os
import struct
import re
from pathlib import Path
from ctypes import *

# Agregar el path del SDK de MassLynx
sdk_path = r"c:\Damico\Laboratorio\Software\Prueba\MassLynxSDKDownload_v5.0.0\python_wheel\extracted"
sys.path.insert(0, sdk_path)

# Importar las clases necesarias del SDK
from masslynxsdk import (
    MassLynxRawInfoReader,
    MassLynxRawInfoReaderEx,
    MassLynxRawChromatogramReader,
    MassLynxRawScanReader,
    MassLynxHeaderItem,
    MassLynxScanItem,
    MassLynxException
)
from masslynxsdk.Providers.MassLynxProvider import MassLynxProvider


class AnalizadorRawMassLynx:
    """Clase para analizar archivos .raw de MassLynx y extraer toda la información"""
    
    def __init__(self, ruta_raw, ruta_licencia=None):
        """
        Inicializa el analizador con la ruta del archivo .raw
        
        Args:
            ruta_raw: Ruta completa al archivo .raw (carpeta)
            ruta_licencia: Ruta al archivo license.key (opcional, busca automáticamente)
        """
        self.ruta_raw = ruta_raw
        self.info_reader = None
        self.chrom_reader = None
        self.scan_reader = None
        
        # Validar que existe el archivo
        if not os.path.exists(ruta_raw):
            raise FileNotFoundError(f"No se encontró el archivo: {ruta_raw}")
        
        # Buscar archivo de licencia
        if ruta_licencia is None:
            # Buscar en directorio del script
            dir_script = os.path.dirname(os.path.abspath(__file__))
            ruta_licencia = os.path.join(dir_script, "license.key")
            
            # Si no existe, buscar en el directorio del SDK
            if not os.path.exists(ruta_licencia):
                sdk_base = os.path.join(dir_script, "MassLynxSDKDownload_v5.0.0")
                ruta_licencia = os.path.join(sdk_base, "license.key")
        
        # Leer licencia
        licencia = ""
        if os.path.exists(ruta_licencia):
            try:
                with open(ruta_licencia, 'r') as f:
                    licencia = f.read().strip()
                print(f"✓ Licencia cargada desde: {ruta_licencia}")
            except Exception as e:
                print(f"Advertencia: No se pudo leer licencia: {e}")
        else:
            print(f"Advertencia: No se encontró archivo de licencia en: {ruta_licencia}")
        
        # Inicializar los lectores con licencia (usar versión extendida para MRM)
        try:
            self.info_reader = MassLynxRawInfoReaderEx(ruta_raw, licencia)
            self.chrom_reader = MassLynxRawChromatogramReader(ruta_raw, licencia)
            self.scan_reader = MassLynxRawScanReader(ruta_raw, licencia)
            print("✓ Lectores inicializados correctamente")
        except Exception as e:
            print(f"Error al inicializar lectores: {e}")
            raise
    
    def extraer_informacion_header(self):
        """Extrae información del encabezado del archivo"""
        print("=" * 80)
        print("INFORMACIÓN DEL ENCABEZADO")
        print("=" * 80)
        
        headers_importantes = {
            MassLynxHeaderItem.ACQUIRED_NAME: "Nombre de adquisición",
            MassLynxHeaderItem.ACQUIRED_DATE: "Fecha de adquisición",
            MassLynxHeaderItem.ACQUIRED_TIME: "Hora de adquisición",
            MassLynxHeaderItem.SAMPLE_ID: "ID de muestra",
            MassLynxHeaderItem.INSTRUMENT: "Instrumento",
            MassLynxHeaderItem.JOB_CODE: "Código de trabajo",
            MassLynxHeaderItem.USER_NAME: "Usuario",
            MassLynxHeaderItem.SAMPLE_DESCRIPTION: "Descripción de muestra",
            MassLynxHeaderItem.BOTTLE_NUMBER: "Número de vial"
        }
        
        info_header = {}
        for header_item, descripcion in headers_importantes.items():
            try:
                params = self.info_reader.GetHeaderItemValue([header_item])
                valor = params.Get(header_item)
                info_header[descripcion] = valor
                print(f"{descripcion}: {valor}")
            except Exception as e:
                print(f"{descripcion}: No disponible ({e})")
        
        print()
        return info_header
    
    def extraer_informacion_funciones(self):
        """Extrae información de todas las funciones"""
        print("=" * 80)
        print("INFORMACIÓN DE FUNCIONES")
        print("=" * 80)
        
        try:
            num_funciones = self.info_reader.GetNumberofFunctions()
            print(f"Número total de funciones: {num_funciones}\n")
            
            info_funciones = []
            
            for func in range(num_funciones):
                print(f"\n--- FUNCIÓN {func + 1} ---")
                
                info_func = {
                    'numero': func + 1,
                    'indice': func
                }
                
                # Tipo de función
                try:
                    tipo_func = self.info_reader.GetFunctionType(func)
                    tipo_func_str = self.info_reader.GetFunctionTypeString(tipo_func)
                    info_func['tipo'] = tipo_func_str
                    print(f"Tipo de función: {tipo_func_str}")
                except Exception as e:
                    print(f"Tipo de función: No disponible ({e})")
                
                # Modo de ionización
                try:
                    ion_mode = self.info_reader.GetIonMode(func)
                    ion_mode_str = self.info_reader.GetIonModeString(ion_mode)
                    info_func['modo_ion'] = ion_mode_str
                    print(f"Modo de ionización: {ion_mode_str}")
                except Exception as e:
                    print(f"Modo de ionización: No disponible ({e})")
                
                # Número de scans
                try:
                    num_scans = self.info_reader.GetScansInFunction(func)
                    info_func['num_scans'] = num_scans
                    print(f"Número de scans: {num_scans}")
                except Exception as e:
                    print(f"Número de scans: No disponible ({e})")
                
                # Rango de masas
                try:
                    low_mass, high_mass = self.info_reader.GetAcquisitionMassRange(func)
                    info_func['rango_masas'] = (low_mass, high_mass)
                    print(f"Rango de masas: {low_mass:.2f} - {high_mass:.2f} Da")
                except Exception as e:
                    print(f"Rango de masas: No disponible ({e})")
                
                # Rango de tiempo
                try:
                    start_time, end_time = self.info_reader.GetAcquisitionTimeRange(func)
                    info_func['rango_tiempo'] = (start_time, end_time)
                    print(f"Rango de tiempo: {start_time:.2f} - {end_time:.2f} min")
                except Exception as e:
                    print(f"Rango de tiempo: No disponible ({e})")
                
                # Continuum o centroide
                try:
                    is_continuum = self.info_reader.IsContinuum(func)
                    info_func['continuum'] = is_continuum
                    print(f"Modo: {'Continuum' if is_continuum else 'Centroide'}")
                except Exception as e:
                    print(f"Modo: No disponible ({e})")
                
                # Información específica de MRM
                try:
                    num_mrm = self.info_reader.GetMRMCount(func)
                    if num_mrm > 0:
                        info_func['num_transiciones'] = num_mrm
                        print(f"\n*** Función MRM con {num_mrm} transiciones ***")
                        info_func['transiciones'] = self.extraer_transiciones_mrm(func, num_mrm)
                except Exception as e:
                    print(f"MRM: No aplicable ({e})")
                
                info_funciones.append(info_func)
            
            return info_funciones
            
        except Exception as e:
            print(f"Error al extraer información de funciones: {e}")
            return []
    
    def _extraer_masas_mrm_dll(self, funcion, num_transiciones):
        """
        Extrae las masas Q1>Q3 de cada transición MRM usando la DLL directamente
        
        Args:
            funcion: Índice de la función (0-based)
            num_transiciones: Número de transiciones MRM
        
        Returns:
            Lista de tuplas (Q1, Q3) para cada transición
        """
        # Obtener el puntero interno del reader
        reader_ptr = self.info_reader._provider._getReader()
        
        # Obtener la función getAcquisitionMassRange de la DLL
        getAcquisitionMassRange = MassLynxProvider.MassLynxDll.getAcquisitionMassRange
        getAcquisitionMassRange.argtypes = [c_void_p, c_int, c_int, POINTER(c_float), POINTER(c_float)]
        getAcquisitionMassRange.restype = c_int
        
        masas = []
        for mrm_idx in range(num_transiciones):
            lowMass = c_float(0)
            highMass = c_float(0)
            
            # Llamar a la DLL con whichMRM específico
            code = getAcquisitionMassRange(reader_ptr, funcion, mrm_idx, lowMass, highMass)
            
            if code == 0:  # 0 = éxito
                q1 = lowMass.value
                q3 = highMass.value
                masas.append((q1, q3))
            else:
                masas.append((0.0, 0.0))
        
        return masas
    
    def _extraer_nombres_mrm_archivo(self, num_transiciones):
        """
        Extrae los nombres de las transiciones MRM desde el archivo _FUNC001.CMP
        
        Args:
            num_transiciones: Número de transiciones MRM esperadas
        
        Returns:
            Lista de nombres de transiciones
        """
        archivo_cmp = os.path.join(self.ruta_raw, "_FUNC001.CMP")
        
        if not os.path.exists(archivo_cmp):
            return [f"MRM_{i+1}" for i in range(num_transiciones)]
        
        try:
            with open(archivo_cmp, 'rb') as f:
                content = f.read()
            
            # Buscar strings imprimibles (ASCII) de al menos 4 caracteres
            strings_ascii = re.findall(b'([ -~]{4,})', content)
            nombres = [s.decode('ascii').strip() for s in strings_ascii]
            
            # Asegurar que tengamos el número correcto
            if len(nombres) < num_transiciones:
                nombres.extend([f"MRM_{i+1}" for i in range(len(nombres), num_transiciones)])
            
            return nombres[:num_transiciones]
        except:
            return [f"MRM_{i+1}" for i in range(num_transiciones)]
    
    def _extraer_energias_mrm_archivo(self, num_transiciones):
        """
        Extrae CE y CV de cada transición MRM desde el archivo _FUNC001.EE
        
        Args:
            num_transiciones: Número de transiciones MRM esperadas
        
        Returns:
            Lista de tuplas (CV, CE) para cada transición
        """
        archivo_ee = os.path.join(self.ruta_raw, "_FUNC001.EE")
        
        if not os.path.exists(archivo_ee):
            return [(None, None)] * num_transiciones
        
        try:
            with open(archivo_ee, 'rb') as f:
                content = f.read()
            
            # Los datos de energía están al final del archivo (offset 128)
            datos_offset = 128
            datos = content[datos_offset:]
            
            # Leer como enteros de 2 bytes (uint16, little-endian)
            # Formato: CV1, CE1, CV2, CE2, ..., CVn, CEn
            energias = []
            for i in range(0, len(datos) - 1, 2):
                val = struct.unpack('<H', datos[i:i+2])[0]
                energias.append(val)
            
            # Agrupar en pares (CV, CE)
            pares_energias = []
            for i in range(0, len(energias), 2):
                if i+1 < len(energias):
                    cv = energias[i]
                    ce = energias[i+1]
                    pares_energias.append((cv, ce))
            
            # Asegurar que tengamos el número correcto
            if len(pares_energias) < num_transiciones:
                pares_energias.extend([(None, None)] * (num_transiciones - len(pares_energias)))
            
            return pares_energias[:num_transiciones]
        except:
            return [(None, None)] * num_transiciones
    
    def extraer_transiciones_mrm(self, funcion, num_transiciones):
        """Extrae información COMPLETA de transiciones MRM incluyendo Q1, Q3, nombres, CE y CV"""
        print(f"\nTRANSICIONES MRM (Función {funcion + 1}):")
        print("-" * 80)
        
        # Extraer toda la información
        masas = self._extraer_masas_mrm_dll(funcion, num_transiciones)
        nombres = self._extraer_nombres_mrm_archivo(num_transiciones)
        energias = self._extraer_energias_mrm_archivo(num_transiciones)
        
        transiciones = []
        
        for mrm_idx in range(num_transiciones):
            q1, q3 = masas[mrm_idx] if mrm_idx < len(masas) else (0.0, 0.0)
            nombre = nombres[mrm_idx] if mrm_idx < len(nombres) else f"MRM_{mrm_idx+1}"
            cv, ce = energias[mrm_idx] if mrm_idx < len(energias) else (None, None)
            
            trans_info = {
                'indice': mrm_idx,
                'numero': mrm_idx + 1,
                'q1_precursor': q1,
                'q3_producto': q3,
                'transicion': f"{q1:.2f} > {q3:.2f}",
                'nombre': nombre,
                'voltaje_cono': cv,
                'energia_colision': ce
            }
            
            transiciones.append(trans_info)
            
            # Imprimir info
            print(f"\nTransición {trans_info['numero']}: {trans_info['transicion']}")
            print(f"  Nombre: {nombre}")
            print(f"  Q1 (precursor): {q1:.4f} Da")
            print(f"  Q3 (producto): {q3:.4f} Da")
            if cv is not None:
                print(f"  Voltaje de cono (CV): {cv} V")
            if ce is not None:
                print(f"  Energía de colisión (CE): {ce} V")
        
        return transiciones
    
    def extraer_parametros_scan(self, funcion, scan=0):
        """Extrae parámetros específicos de un scan"""
        print(f"\n--- PARÁMETROS DEL SCAN {scan} (Función {funcion + 1}) ---")
        
        parametros = {}
        
        # Lista de parámetros importantes
        items_importantes = {
            MassLynxScanItem.COLLISION_ENERGY: "Energía de colisión (eV)",
            MassLynxScanItem.SAMPLING_CONE_VOLTAGE: "Voltaje de cono (V)",
            MassLynxScanItem.SOURCE_TEMPERATURE: "Temperatura de fuente (°C)",
            MassLynxScanItem.PROBE_TEMPERATURE: "Temperatura de sonda (°C)",
            MassLynxScanItem.RF_VOLTAGE: "Voltaje RF",
            MassLynxScanItem.MULTIPLIER1: "Multiplicador 1",
            MassLynxScanItem.MULTIPLIER2: "Multiplicador 2",
            MassLynxScanItem.SET_MASS: "Masa configurada",
            MassLynxScanItem.ION_ENERGY: "Energía de iones",
            MassLynxScanItem.BASE_PEAK_MASS: "Masa del pico base",
            MassLynxScanItem.BASE_PEAK_INTENSITY: "Intensidad del pico base",
            MassLynxScanItem.TOTAL_ION_CURRENT: "Corriente iónica total (TIC)"
        }
        
        for item, descripcion in items_importantes.items():
            try:
                params = self.info_reader.GetScanItemValue(funcion, scan, [item])
                valor = params.Get(item)
                parametros[descripcion] = valor
                print(f"{descripcion}: {valor}")
            except Exception as e:
                pass  # Algunos parámetros pueden no estar disponibles
        
        return parametros
    
    def extraer_cromatogramas(self, funcion):
        """Extrae cromatogramas TIC, BPI y MRM de una función"""
        print(f"\n--- CROMATOGRAMAS (Función {funcion + 1}) ---")
        
        cromatogramas = {}
        
        # Extraer TIC (Total Ion Chromatogram)
        try:
            tiempos_tic, intensidades_tic = self.chrom_reader.ReadTIC(funcion)
            cromatogramas['TIC'] = {
                'tiempos': tiempos_tic,
                'intensidades': intensidades_tic,
                'puntos': len(tiempos_tic)
            }
            print(f"TIC extraído: {len(tiempos_tic)} puntos")
            print(f"  Tiempo: {tiempos_tic[0]:.2f} - {tiempos_tic[-1]:.2f} min")
            print(f"  Intensidad máxima: {max(intensidades_tic):.2e}")
        except Exception as e:
            print(f"No se pudo extraer TIC: {e}")
        
        # Extraer BPI (Base Peak Intensity)
        try:
            tiempos_bpi, intensidades_bpi = self.chrom_reader.ReadBPI(funcion)
            cromatogramas['BPI'] = {
                'tiempos': tiempos_bpi,
                'intensidades': intensidades_bpi,
                'puntos': len(tiempos_bpi)
            }
            print(f"BPI extraído: {len(tiempos_bpi)} puntos")
            print(f"  Intensidad máxima: {max(intensidades_bpi):.2e}")
        except Exception as e:
            print(f"No se pudo extraer BPI: {e}")
        
        # Extraer MRM cromatogramas si es una función MRM
        try:
            num_mrm = self.info_reader.GetMRMCount(funcion)
            if num_mrm > 0:
                print(f"\nExtrayendo {num_mrm} cromatogramas MRM...")
                cromatogramas['MRM'] = []
                
                for mrm_idx in range(num_mrm):
                    try:
                        tiempos_mrm, intensidades_mrm = self.chrom_reader.ReadMRMChromatogram(funcion, mrm_idx)
                        cromatogramas['MRM'].append({
                            'transicion': mrm_idx + 1,
                            'tiempos': tiempos_mrm,
                            'intensidades': intensidades_mrm,
                            'puntos': len(tiempos_mrm),
                            'intensidad_maxima': max(intensidades_mrm) if len(intensidades_mrm) > 0 else 0
                        })
                        print(f"  Transición {mrm_idx + 1}: {len(tiempos_mrm)} puntos, Imax = {max(intensidades_mrm):.2e}")
                    except Exception as e:
                        print(f"  Error en transición {mrm_idx + 1}: {e}")
        except Exception as e:
            print(f"No se pudieron extraer cromatogramas MRM: {e}")
        
        return cromatogramas
    
    def extraer_espectro(self, funcion, scan):
        """Extrae un espectro de masas de un scan específico"""
        print(f"\n--- ESPECTRO DE MASAS (Función {funcion + 1}, Scan {scan}) ---")
        
        try:
            masas, intensidades = self.scan_reader.ReadScan(funcion, scan)
            
            espectro = {
                'masas': masas,
                'intensidades': intensidades,
                'num_picos': len(masas)
            }
            
            print(f"Espectro extraído: {len(masas)} picos")
            if len(masas) > 0:
                print(f"  Rango de masas: {min(masas):.2f} - {max(masas):.2f} Da")
                print(f"  Intensidad máxima: {max(intensidades):.2e}")
                
                # Mostrar los 5 picos más intensos
                picos_ordenados = sorted(zip(masas, intensidades), key=lambda x: x[1], reverse=True)
                print(f"\n  Top 5 picos más intensos:")
                for i, (masa, intensidad) in enumerate(picos_ordenados[:5]):
                    print(f"    {i+1}. m/z {masa:.4f}: {intensidad:.2e}")
            
            return espectro
        except Exception as e:
            print(f"Error al extraer espectro: {e}")
            return None
    
    def analisis_completo(self, extraer_espectros=False):
        """Realiza un análisis completo del archivo .raw"""
        print("\n")
        print("╔" + "═" * 78 + "╗")
        print("║" + " " * 20 + "ANÁLISIS COMPLETO DE ARCHIVO RAW" + " " * 26 + "║")
        print("║" + " " * 78 + "║")
        print("║  " + f"Archivo: {os.path.basename(self.ruta_raw)}".ljust(76) + "║")
        print("╚" + "═" * 78 + "╝")
        print("\n")
        
        resultados = {}
        
        # 1. Información del header
        resultados['header'] = self.extraer_informacion_header()
        
        # 2. Información de funciones
        resultados['funciones'] = self.extraer_informacion_funciones()
        
        # 3. Para cada función, extraer cromatogramas
        print("\n" + "=" * 80)
        print("EXTRACCIÓN DE CROMATOGRAMAS")
        print("=" * 80)
        
        resultados['cromatogramas'] = []
        for func_info in resultados['funciones']:
            func_idx = func_info['indice']
            
            # Extraer parámetros del scan
            parametros = self.extraer_parametros_scan(func_idx, 0)
            
            # Extraer cromatogramas
            croms = self.extraer_cromatogramas(func_idx)
            resultados['cromatogramas'].append({
                'funcion': func_idx + 1,
                'parametros': parametros,
                'cromatogramas': croms
            })
            
            # Opcionalmente extraer espectros
            if extraer_espectros and func_info.get('num_scans', 0) > 0:
                # Extraer un espectro de ejemplo (scan del medio)
                scan_medio = func_info['num_scans'] // 2
                espectro = self.extraer_espectro(func_idx, scan_medio)
        
        print("\n" + "=" * 80)
        print("ANÁLISIS COMPLETADO")
        print("=" * 80)
        
        return resultados
    
    def exportar_cromatogramas_csv(self, resultados, carpeta_salida):
        """Exporta los cromatogramas a archivos CSV"""
        import csv
        
        os.makedirs(carpeta_salida, exist_ok=True)
        
        for func_data in resultados['cromatogramas']:
            func_num = func_data['funcion']
            croms = func_data['cromatogramas']
            
            # Exportar TIC
            if 'TIC' in croms:
                archivo_tic = os.path.join(carpeta_salida, f"TIC_Funcion_{func_num}.csv")
                with open(archivo_tic, 'w', newline='') as f:
                    writer = csv.writer(f)
                    writer.writerow(['Tiempo (min)', 'Intensidad'])
                    for t, i in zip(croms['TIC']['tiempos'], croms['TIC']['intensidades']):
                        writer.writerow([t, i])
                print(f"Exportado: {archivo_tic}")
            
            # Exportar BPI
            if 'BPI' in croms:
                archivo_bpi = os.path.join(carpeta_salida, f"BPI_Funcion_{func_num}.csv")
                with open(archivo_bpi, 'w', newline='') as f:
                    writer = csv.writer(f)
                    writer.writerow(['Tiempo (min)', 'Intensidad'])
                    for t, i in zip(croms['BPI']['tiempos'], croms['BPI']['intensidades']):
                        writer.writerow([t, i])
                print(f"Exportado: {archivo_bpi}")
            
            # Exportar MRM
            if 'MRM' in croms:
                for mrm_data in croms['MRM']:
                    trans_num = mrm_data['transicion']
                    archivo_mrm = os.path.join(carpeta_salida, f"MRM_Funcion_{func_num}_Transicion_{trans_num}.csv")
                    with open(archivo_mrm, 'w', newline='') as f:
                        writer = csv.writer(f)
                        writer.writerow(['Tiempo (min)', 'Intensidad'])
                        for t, i in zip(mrm_data['tiempos'], mrm_data['intensidades']):
                            writer.writerow([t, i])
                    print(f"Exportado: {archivo_mrm}")


def main():
    """Función principal para ejecutar el análisis"""
    
    # Ruta al archivo .raw de ejemplo
    ruta_raw = r"c:\Damico\Laboratorio\Software\Prueba\20251002_20250825 QC3.raw"
    
    # Verificar que existe
    if not os.path.exists(ruta_raw):
        print(f"ERROR: No se encuentra el archivo {ruta_raw}")
        return
    
    try:
        # Crear el analizador
        analizador = AnalizadorRawMassLynx(ruta_raw)
        
        # Realizar análisis completo
        resultados = analizador.analisis_completo(extraer_espectros=True)
        
        # Exportar cromatogramas a CSV
        carpeta_salida = r"c:\Damico\Laboratorio\Software\Prueba\resultados_analisis"
        print(f"\n\nExportando cromatogramas a: {carpeta_salida}")
        analizador.exportar_cromatogramas_csv(resultados, carpeta_salida)
        
        print("\n\n✓ Análisis completado exitosamente!")
        
    except Exception as e:
        print(f"\n\nERROR durante el análisis: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
