import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import simpy
import random
import numpy as np
import matplotlib
matplotlib.use('TkAgg')  # Configuración importante para matplotlib
import matplotlib.pyplot as plt
from collections import defaultdict
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class HardwareMaintenanceApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Simulador de Mantenimiento de Hardware")
        self.root.geometry("1000x700")
        
        # Variables para almacenar datos
        self.tecnicos = []
        self.herramientas = []
        self.servicios = {}
        
        # Crear pestañas
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill='both', expand=True)
        
        # Pestaña de Configuración
        self.config_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.config_frame, text='Configuración')
        self.setup_config_tab()
        
        # Pestaña de Simulación
        self.sim_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.sim_frame, text='Simulación')
        self.setup_sim_tab()
        
        # Pestaña de Resultados
        self.results_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.results_frame, text='Resultados')
        self.setup_results_tab()
        
        # Deshabilitar pestañas hasta que se complete la configuración
        self.notebook.tab(1, state='disabled')
        self.notebook.tab(2, state='disabled')
    
    def setup_config_tab(self):
        # Sección de técnicos
        ttk.Label(self.config_frame, text="👨‍💼 Configuración de Técnicos", 
                font=('Arial', 12, 'bold')).grid(row=0, column=0, padx=10, pady=10, sticky='w')
        
        ttk.Label(self.config_frame, text="Cantidad de técnicos:").grid(row=1, column=0, padx=10, sticky='e')
        self.num_tecnicos = tk.IntVar(value=1)
        ttk.Entry(self.config_frame, textvariable=self.num_tecnicos, width=10).grid(row=1, column=1, sticky='w')
        
        ttk.Label(self.config_frame, text="Horas base por semana:").grid(row=2, column=0, padx=10, sticky='e')
        self.horas_semana = tk.DoubleVar(value=40)
        ttk.Entry(self.config_frame, textvariable=self.horas_semana, width=10).grid(row=2, column=1, sticky='w')
        
        ttk.Label(self.config_frame, text="Horas extras máximas por semana:").grid(row=3, column=0, padx=10, sticky='e')
        self.horas_extras = tk.DoubleVar(value=15)
        ttk.Entry(self.config_frame, textvariable=self.horas_extras, width=10).grid(row=3, column=1, sticky='w')
        
        ttk.Label(self.config_frame, text="Salario por hora normal ($):").grid(row=4, column=0, padx=10, sticky='e')
        self.salario_hora = tk.DoubleVar(value=15)
        ttk.Entry(self.config_frame, textvariable=self.salario_hora, width=10).grid(row=4, column=1, sticky='w')
        
        ttk.Label(self.config_frame, text="Salario por hora extra ($):").grid(row=5, column=0, padx=10, sticky='e')
        self.salario_extra = tk.DoubleVar(value=22)
        ttk.Entry(self.config_frame, textvariable=self.salario_extra, width=10).grid(row=5, column=1, sticky='w')
        
        # Sección de herramientas
        ttk.Label(self.config_frame, text="🧰 Registro de Herramientas", 
                font=('Arial', 12, 'bold')).grid(row=6, column=0, padx=10, pady=(20, 5), sticky='w')
        
        self.herramientas_frame = ttk.Frame(self.config_frame)
        self.herramientas_frame.grid(row=7, column=0, columnspan=3, padx=10, sticky='w')
        
        # Encabezados de herramientas
        ttk.Label(self.herramientas_frame, text="Nombre:").grid(row=0, column=0)
        ttk.Label(self.herramientas_frame, text="Precio ($):").grid(row=0, column=1)
        ttk.Label(self.herramientas_frame, text="Vida útil (usos):").grid(row=0, column=2)
        
        self.herramienta_entries = []
        self.add_herramienta_row()
        
        ttk.Button(self.herramientas_frame, text="+ Añadir herramienta", 
                command=self.add_herramienta_row).grid(row=100, column=0, pady=5)
        
        # Sección de servicios
        ttk.Label(self.config_frame, text="🔩 Servicios Disponibles", 
                font=('Arial', 12, 'bold')).grid(row=8, column=0, padx=10, pady=(20, 5), sticky='w')
        
        self.servicios_frame = ttk.Frame(self.config_frame)
        self.servicios_frame.grid(row=9, column=0, columnspan=3, padx=10, sticky='w')
        
        # Encabezados de servicios
        ttk.Label(self.servicios_frame, text="Nombre del servicio:").grid(row=0, column=0)
        ttk.Label(self.servicios_frame, text="Costo ($):").grid(row=0, column=1)
        
        self.servicio_entries = []
        self.add_servicio_row()
        
        ttk.Button(self.servicios_frame, text="+ Añadir servicio", 
                command=self.add_servicio_row).grid(row=100, column=0, pady=5)
        
        # Botón de guardar configuración
        ttk.Button(self.config_frame, text="Guardar Configuración", 
                command=self.guardar_configuracion).grid(row=10, column=0, pady=20, columnspan=2)
    
    def add_herramienta_row(self):
        row = len(self.herramienta_entries)
        
        nombre = tk.StringVar()
        precio = tk.DoubleVar()
        vida_util = tk.IntVar(value=10)
        
        ttk.Entry(self.herramientas_frame, textvariable=nombre, width=20).grid(row=row+1, column=0, padx=5, pady=2)
        ttk.Entry(self.herramientas_frame, textvariable=precio, width=10).grid(row=row+1, column=1, padx=5, pady=2)
        ttk.Entry(self.herramientas_frame, textvariable=vida_util, width=10).grid(row=row+1, column=2, padx=5, pady=2)
        
        self.herramienta_entries.append((nombre, precio, vida_util))
    
    def add_servicio_row(self):
        row = len(self.servicio_entries)
        
        nombre = tk.StringVar()
        costo = tk.DoubleVar()
        
        ttk.Entry(self.servicios_frame, textvariable=nombre, width=30).grid(row=row+1, column=0, padx=5, pady=2)
        ttk.Entry(self.servicios_frame, textvariable=costo, width=10).grid(row=row+1, column=1, padx=5, pady=2)
        
        self.servicio_entries.append((nombre, costo))
    
    def guardar_configuracion(self):
        try:
            # Validación básica
            if self.num_tecnicos.get() <= 0:
                raise ValueError("Debe haber al menos 1 técnico")
            
            # Guardar técnicos
            self.tecnicos = [{
                "horas_normales": self.horas_semana.get(),
                "horas_extras": self.horas_extras.get(),
                "costo_hora": self.salario_hora.get(),
                "costo_extra": self.salario_extra.get(),
                "horas_trabajadas": 0,
                "horas_extras_trabajadas": 0
            } for _ in range(self.num_tecnicos.get())]
            
            # Guardar herramientas
            self.herramientas = []
            for nombre, precio, vida_util in self.herramienta_entries:
                if nombre.get().strip():  # Ignorar campos vacíos
                    self.herramientas.append({
                        "nombre": nombre.get(),
                        "precio": precio.get(),
                        "vida_util": vida_util.get(),
                        "usos": 0
                    })
            
            if not self.herramientas:
                raise ValueError("Debes registrar al menos 1 herramienta")
            
            # Guardar servicios
            self.servicios = {}
            for nombre, costo in self.servicio_entries:
                if nombre.get().strip():  # Ignorar campos vacíos
                    self.servicios[nombre.get()] = costo.get()
            
            # Habilitar pestaña de simulación
            self.notebook.tab(1, state='normal')
            messagebox.showinfo("Éxito", "Configuración guardada correctamente")
            
        except ValueError as ve:
            messagebox.showerror("Error de validación", str(ve))
        except Exception as e:
            messagebox.showerror("Error", f"Error al guardar configuración: {str(e)}")
    
    def setup_sim_tab(self):
        ttk.Label(self.sim_frame, text="📆 Configuración de la Simulación", 
                font=('Arial', 12, 'bold')).pack(pady=10)
        
        ttk.Label(self.sim_frame, text="Días a simular:").pack()
        self.dias_simulacion = tk.IntVar(value=7)
        ttk.Entry(self.sim_frame, textvariable=self.dias_simulacion, width=10).pack()
        
        # Consola de salida
        self.console = scrolledtext.ScrolledText(self.sim_frame, width=100, height=20, state='disabled')
        self.console.pack(pady=10, padx=10, fill='both', expand=True)
        
        ttk.Button(self.sim_frame, text="Iniciar Simulación", 
                command=self.iniciar_simulacion).pack(pady=10)
    
    def log_to_console(self, message):
        self.console.config(state='normal')
        self.console.insert('end', message + '\n')
        self.console.see('end')
        self.console.config(state='disabled')
    
    def iniciar_simulacion(self):
        try:
            dias = self.dias_simulacion.get()
            if dias <= 0:
                raise ValueError("Los días de simulación deben ser mayores a 0")
            if not self.tecnicos:
                raise ValueError("Primero debes guardar la configuración de técnicos")
            if not self.herramientas:
                raise ValueError("No hay herramientas registradas")
            
            self.console.config(state='normal')
            self.console.delete(1.0, 'end')
            self.console.config(state='disabled')
            
            self.log_to_console("⚙️ INICIANDO SIMULACIÓN...")
            
            # Reiniciar estadísticas de horas trabajadas
            for tecnico in self.tecnicos:
                tecnico["horas_trabajadas"] = 0
                tecnico["horas_extras_trabajadas"] = 0
            
            # Ejecutar simulación en segundo plano
            self.root.after(100, lambda: self.run_simulation(dias))
            
        except ValueError as ve:
            messagebox.showerror("Error de validación", str(ve))
        except Exception as e:
            messagebox.showerror("Error", f"Error al iniciar simulación: {str(e)}")
    
    def run_simulation(self, dias):
        self.stats = {
            "costos": [],
            "servicios": defaultdict(int),
            "herramientas": defaultdict(int),
            "horas_normales": 0,
            "horas_extras": 0
        }
        
        env = simpy.Environment()
        
        def realizar_reparacion(env, tecnico):
            # Selección de servicio
            servicio, costo = (random.choice(list(self.servicios.items())) 
                            if self.servicios 
                            else ("Reparación genérica", random.uniform(50, 200)))
            
            self.stats["servicios"][servicio] += 1
            
            # Tiempo de reparación (0.5 a 3 horas)
            tiempo = random.uniform(0.5, 3)
            yield env.timeout(tiempo)
            
            # Costos
            hora_actual = env.now % 24
            dia_actual = int(env.now // 24)
            
            # Calcular costo de mano de obra
            es_hora_extra = False
            
            # Verificar si es horario nocturno o si ya completó las horas normales
            if (hora_actual < 8 or hora_actual > 18 or 
                tecnico["horas_trabajadas"] >= tecnico["horas_normales"]):
                
                # Verificar que no exceda el máximo de horas extras
                if tecnico["horas_extras_trabajadas"] < tecnico["horas_extras"]:
                    es_hora_extra = True
                    tecnico["horas_extras_trabajadas"] += tiempo
                    self.stats["horas_extras"] += tiempo
                else:
                    # Si ya no puede hacer más horas extras, se cuenta como hora normal
                    tecnico["horas_trabajadas"] += tiempo
                    self.stats["horas_normales"] += tiempo
            else:
                tecnico["horas_trabajadas"] += tiempo
                self.stats["horas_normales"] += tiempo
            
            costo_mano_obra = tiempo * (tecnico["costo_extra"] if es_hora_extra else tecnico["costo_hora"])
            
            # Desgaste de herramientas
            herramienta = random.choice(self.herramientas)
            self.stats["herramientas"][herramienta["nombre"]] += 1
            herramienta["usos"] += 1
            costo_herramienta = 0
            if herramienta["usos"] >= herramienta["vida_util"]:
                costo_herramienta = herramienta["precio"]
                herramienta["usos"] = 0
            
            # Registrar costos
            if not self.stats["costos"] or self.stats["costos"][-1]["dia"] != dia_actual:
                self.stats["costos"].append({
                    "dia": dia_actual,
                    "servicios": 0,
                    "mano_obra": 0,
                    "herramientas": 0
                })
            
            self.stats["costos"][-1]["servicios"] += costo
            self.stats["costos"][-1]["mano_obra"] += costo_mano_obra
            self.stats["costos"][-1]["herramientas"] += costo_herramienta

            # Mostrar progreso en la consola
            tipo_hora = "EXTRA" if es_hora_extra else "NORMAL"
            self.root.after(0, self.log_to_console, 
                        f"\n🔧 Día {dia_actual+1} - {hora_actual:02.0f}:00 ({tipo_hora})\n" +
                        f"• Servicio: {servicio} (${costo:.2f})\n" +
                        f"• Técnico: {tiempo:.1f} horas trabajadas\n" +
                        f"• Herramienta usada: {herramienta['nombre']}\n" +
                        f"• Horas normales acumuladas: {tecnico['horas_trabajadas']:.1f}/{tecnico['horas_normales']}\n" +
                        f"• Horas extras acumuladas: {tecnico['horas_extras_trabajadas']:.1f}/{tecnico['horas_extras']}")

        def generar_trabajos(env):
            while True:
                yield env.timeout(random.expovariate(1/2))  # 1 trabajo cada 2 horas en promedio
                env.process(realizar_reparacion(env, random.choice(self.tecnicos)))

        env.process(generar_trabajos(env))
        env.run(until=dias*24)
        
        self.root.after(0, self.log_to_console, "\n✅ SIMULACIÓN COMPLETADA")
        self.root.after(0, lambda: self.notebook.tab(2, state='normal'))
        self.root.after(0, self.notebook.select, 2)
    
    def setup_results_tab(self):
        self.results_canvas_frame = ttk.Frame(self.results_frame)
        self.results_canvas_frame.pack(fill='both', expand=True)
        
        self.results_text = scrolledtext.ScrolledText(self.results_frame, width=100, height=10, state='disabled')
        self.results_text.pack(fill='x', padx=10, pady=10)
        
        ttk.Button(self.results_frame, text="Mostrar Resultados", 
                command=self.mostrar_resultados).pack(pady=10)
    
    def mostrar_resultados(self):
        if not hasattr(self, 'stats'):
            messagebox.showerror("Error", "Primero debes ejecutar una simulación")
            return
        
        dias = self.dias_simulacion.get()
        
        # Limpiar frame de gráficos
        for widget in self.results_canvas_frame.winfo_children():
            widget.destroy()
        
        try:
            # Procesar datos
            dias_sim = [d["dia"]+1 for d in self.stats["costos"]]
            acum_servicios = np.cumsum([d["servicios"] for d in self.stats["costos"]])
            acum_mano_obra = np.cumsum([d["mano_obra"] for d in self.stats["costos"]])
            acum_herramientas = np.cumsum([d["herramientas"] for d in self.stats["costos"]])
            total = acum_servicios + acum_mano_obra + acum_herramientas
            
            # Gráfico 1: Evolución de costos
            fig1, ax1 = plt.subplots(figsize=(10, 4))
            ax1.plot(dias_sim, acum_servicios, label="Servicios", marker='o')
            ax1.plot(dias_sim, acum_mano_obra, label="Mano de obra", marker='s')
            ax1.plot(dias_sim, acum_herramientas, label="Herramientas", marker='^')
            ax1.plot(dias_sim, total, label="TOTAL", linestyle='--', linewidth=2, color='red')
            
            ax1.set_title(f"📈 COSTOS ACUMULADOS ({dias} DÍAS)", pad=20)
            ax1.set_xlabel("Día de operación")
            ax1.set_ylabel("Costos ($)")
            ax1.legend()
            ax1.grid(True, alpha=0.3)
            
            canvas1 = FigureCanvasTkAgg(fig1, self.results_canvas_frame)
            canvas1.draw()
            canvas1.get_tk_widget().pack(fill='both', expand=True)
            
            # Gráfico 2: Frecuencia de servicios
            fig2, ax2 = plt.subplots(figsize=(10, 4))
            servicios = list(self.stats["servicios"].keys())
            frecuencias = list(self.stats["servicios"].values())
            ax2.bar(servicios, frecuencias, color='skyblue')
            ax2.set_title("📊 FRECUENCIA DE SERVICIOS")
            plt.setp(ax2.get_xticklabels(), rotation=45, ha='right')
            ax2.grid(True, axis='y', alpha=0.3)
            
            canvas2 = FigureCanvasTkAgg(fig2, self.results_canvas_frame)
            canvas2.draw()
            canvas2.get_tk_widget().pack(fill='both', expand=True)
            
            # Gráfico 3: Distribución de horas trabajadas
            fig3, ax3 = plt.subplots(figsize=(10, 4))
            labels = ['Horas Normales', 'Horas Extras']
            valores = [self.stats["horas_normales"], self.stats["horas_extras"]]
            ax3.bar(labels, valores, color=['green', 'orange'])
            ax3.set_title("⏱ DISTRIBUCIÓN DE HORAS TRABAJADAS")
            ax3.set_ylabel("Horas")
            ax3.grid(True, axis='y', alpha=0.3)
            
            canvas3 = FigureCanvasTkAgg(fig3, self.results_canvas_frame)
            canvas3.draw()
            canvas3.get_tk_widget().pack(fill='both', expand=True)
            
            # Reporte final en texto
            self.results_text.config(state='normal')
            self.results_text.delete(1.0, 'end')
            
            reporte = "="*50 + "\n"
            reporte += f"📑 INFORME FINAL - {dias} DÍAS".center(50) + "\n"
            reporte += "="*50 + "\n\n"
            reporte += f"🔧 Servicios realizados: {sum(self.stats['servicios'].values())}\n"
            reporte += f"⏱ Horas normales trabajadas: {self.stats['horas_normales']:.1f}\n"
            reporte += f"⏱ Horas extras trabajadas: {self.stats['horas_extras']:.1f}\n"
            reporte += f"💰 Costo total: ${total[-1]:,.2f}\n\n"
            reporte += "🛠️ Herramientas más usadas:\n"
            
            for herramienta, usos in sorted(self.stats["herramientas"].items(), key=lambda x: x[1], reverse=True):
                reporte += f"• {herramienta}: {usos} usos\n"
            
            self.results_text.insert('end', reporte)
            self.results_text.config(state='disabled')
            
        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron generar los resultados: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = HardwareMaintenanceApp(root)
    root.mainloop()