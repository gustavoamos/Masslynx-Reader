"""
Interfaz Gráfica para Análisis de Archivos .raw de MassLynx

Interfaz simple con tkinter para facilitar el uso del SDK
"""

import sys
import os
from pathlib import Path
import tkinter as tk
from tkinter import ttk, filedialog, scrolledtext, messagebox
import threading

# Agregar el path del SDK
sdk_path = r"c:\Damico\Laboratorio\Software\Prueba\MassLynxSDKDownload_v5.0.0\python_wheel\extracted"
sys.path.insert(0, sdk_path)

from analizar_raw_masslynx import AnalizadorRawMassLynx


class InterfazAnalizadorMassLynx:
    """Interfaz gráfica para el analizador de archivos .raw"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Analizador de Archivos MassLynx .raw")
        self.root.geometry("900x700")
        
        self.archivo_raw = None
        self.analizador = None
        self.resultados = None
        
        self.crear_interfaz()
    
    def crear_interfaz(self):
        """Crea todos los elementos de la interfaz"""
        
        # Frame superior - Selección de archivo
        frame_archivo = ttk.LabelFrame(self.root, text="Archivo .raw", padding=10)
        frame_archivo.pack(fill="x", padx=10, pady=5)
        
        self.label_archivo = ttk.Label(frame_archivo, text="No hay archivo seleccionado", 
                                       foreground="gray")
        self.label_archivo.pack(side="left", fill="x", expand=True)
        
        ttk.Button(frame_archivo, text="Seleccionar Archivo...", 
                  command=self.seleccionar_archivo).pack(side="right", padx=5)
        
        # Frame medio - Opciones de análisis
        frame_opciones = ttk.LabelFrame(self.root, text="Opciones de Análisis", padding=10)
        frame_opciones.pack(fill="x", padx=10, pady=5)
        
        self.check_header = tk.BooleanVar(value=True)
        ttk.Checkbutton(frame_opciones, text="Información del Header", 
                       variable=self.check_header).pack(anchor="w")
        
        self.check_funciones = tk.BooleanVar(value=True)
        ttk.Checkbutton(frame_opciones, text="Información de Funciones", 
                       variable=self.check_funciones).pack(anchor="w")
        
        self.check_transiciones = tk.BooleanVar(value=True)
        ttk.Checkbutton(frame_opciones, text="Transiciones MRM", 
                       variable=self.check_transiciones).pack(anchor="w")
        
        self.check_parametros = tk.BooleanVar(value=True)
        ttk.Checkbutton(frame_opciones, text="Parámetros (energías, voltajes)", 
                       variable=self.check_parametros).pack(anchor="w")
        
        self.check_cromatogramas = tk.BooleanVar(value=True)
        ttk.Checkbutton(frame_opciones, text="Cromatogramas (TIC, BPI, MRM)", 
                       variable=self.check_cromatogramas).pack(anchor="w")
        
        self.check_espectros = tk.BooleanVar(value=False)
        ttk.Checkbutton(frame_opciones, text="Espectros de Masas", 
                       variable=self.check_espectros).pack(anchor="w")
        
        # Frame de botones de acción
        frame_botones = ttk.Frame(self.root)
        frame_botones.pack(fill="x", padx=10, pady=5)
        
        self.btn_analizar = ttk.Button(frame_botones, text="🔍 Analizar Archivo", 
                                       command=self.analizar_archivo, state="disabled")
        self.btn_analizar.pack(side="left", padx=5)
        
        self.btn_exportar = ttk.Button(frame_botones, text="💾 Exportar a CSV", 
                                       command=self.exportar_csv, state="disabled")
        self.btn_exportar.pack(side="left", padx=5)
        
        ttk.Button(frame_botones, text="🗑️ Limpiar", 
                  command=self.limpiar).pack(side="left", padx=5)
        
        # Frame de progreso
        self.frame_progreso = ttk.Frame(self.root)
        self.frame_progreso.pack(fill="x", padx=10, pady=5)
        
        self.progress = ttk.Progressbar(self.frame_progreso, mode='indeterminate')
        self.label_estado = ttk.Label(self.frame_progreso, text="")
        
        # Frame de resultados
        frame_resultados = ttk.LabelFrame(self.root, text="Resultados", padding=10)
        frame_resultados.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Área de texto con scroll
        self.texto_resultados = scrolledtext.ScrolledText(frame_resultados, 
                                                          wrap=tk.WORD, 
                                                          font=('Courier New', 9))
        self.texto_resultados.pack(fill="both", expand=True)
    
    def seleccionar_archivo(self):
        """Abre diálogo para seleccionar archivo .raw"""
        archivo = filedialog.askdirectory(
            title="Seleccionar carpeta .raw de MassLynx",
            initialdir=r"c:\Damico\Laboratorio\Software\Prueba"
        )
        
        if archivo:
            # Verificar que sea un archivo .raw válido
            if not archivo.lower().endswith('.raw'):
                messagebox.showwarning("Advertencia", 
                                      "El archivo seleccionado no tiene extensión .raw")
            
            self.archivo_raw = archivo
            self.label_archivo.config(text=os.path.basename(archivo), foreground="black")
            self.btn_analizar.config(state="normal")
            self.escribir_log(f"✓ Archivo seleccionado: {os.path.basename(archivo)}\n")
    
    def escribir_log(self, texto):
        """Escribe texto en el área de resultados"""
        self.texto_resultados.insert(tk.END, texto)
        self.texto_resultados.see(tk.END)
        self.root.update()
    
    def limpiar(self):
        """Limpia el área de resultados"""
        self.texto_resultados.delete(1.0, tk.END)
        self.label_estado.config(text="")
    
    def mostrar_progreso(self, mensaje):
        """Muestra barra de progreso"""
        self.label_estado.config(text=mensaje)
        self.label_estado.pack(side="left", padx=5)
        self.progress.pack(side="left", fill="x", expand=True, padx=5)
        self.progress.start(10)
        self.root.update()
    
    def ocultar_progreso(self):
        """Oculta barra de progreso"""
        self.progress.stop()
        self.progress.pack_forget()
        self.label_estado.pack_forget()
        self.root.update()
    
    def analizar_archivo(self):
        """Ejecuta el análisis del archivo"""
        if not self.archivo_raw:
            messagebox.showerror("Error", "Debe seleccionar un archivo .raw primero")
            return
        
        # Limpiar resultados anteriores
        self.limpiar()
        
        # Deshabilitar botones durante análisis
        self.btn_analizar.config(state="disabled")
        self.btn_exportar.config(state="disabled")
        
        # Ejecutar análisis en thread separado
        thread = threading.Thread(target=self._ejecutar_analisis)
        thread.daemon = True
        thread.start()
    
    def _ejecutar_analisis(self):
        """Ejecuta el análisis (en thread separado)"""
        try:
            self.mostrar_progreso("Inicializando analizador...")
            
            # Redirigir salida a la interfaz
            import io
            from contextlib import redirect_stdout
            
            output = io.StringIO()
            
            with redirect_stdout(output):
                # Crear analizador
                self.analizador = AnalizadorRawMassLynx(self.archivo_raw)
                
                # Ejecutar análisis
                self.resultados = self.analizador.analisis_completo(
                    extraer_espectros=self.check_espectros.get()
                )
            
            # Obtener texto capturado
            texto_salida = output.getvalue()
            
            # Mostrar en interfaz
            self.root.after(0, lambda: self.escribir_log(texto_salida))
            self.root.after(0, lambda: self.escribir_log(
                "\n" + "="*80 + "\n✓ ANÁLISIS COMPLETADO EXITOSAMENTE\n" + "="*80 + "\n"
            ))
            
            # Habilitar exportación
            self.root.after(0, lambda: self.btn_exportar.config(state="normal"))
            
        except Exception as e:
            error_msg = f"\n❌ ERROR durante el análisis:\n{str(e)}\n"
            self.root.after(0, lambda: self.escribir_log(error_msg))
            import traceback
            self.root.after(0, lambda: self.escribir_log(traceback.format_exc()))
        
        finally:
            self.root.after(0, self.ocultar_progreso)
            self.root.after(0, lambda: self.btn_analizar.config(state="normal"))
    
    def exportar_csv(self):
        """Exporta los cromatogramas a CSV"""
        if not self.resultados:
            messagebox.showerror("Error", "Debe analizar un archivo primero")
            return
        
        # Seleccionar carpeta de salida
        carpeta = filedialog.askdirectory(
            title="Seleccionar carpeta para exportar archivos CSV",
            initialdir=os.path.dirname(self.archivo_raw)
        )
        
        if not carpeta:
            return
        
        try:
            self.mostrar_progreso("Exportando a CSV...")
            self.escribir_log(f"\nExportando cromatogramas a: {carpeta}\n")
            
            # Exportar
            self.analizador.exportar_cromatogramas_csv(self.resultados, carpeta)
            
            self.escribir_log("\n✓ Exportación completada!\n")
            messagebox.showinfo("Éxito", f"Archivos exportados a:\n{carpeta}")
            
        except Exception as e:
            error_msg = f"\n❌ ERROR durante la exportación:\n{str(e)}\n"
            self.escribir_log(error_msg)
            messagebox.showerror("Error", str(e))
        
        finally:
            self.ocultar_progreso()


def main():
    """Inicia la interfaz gráfica"""
    root = tk.Tk()
    app = InterfazAnalizadorMassLynx(root)
    root.mainloop()


if __name__ == "__main__":
    main()
