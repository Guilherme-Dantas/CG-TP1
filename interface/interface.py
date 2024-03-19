
import tkinter as tk
from tkinter import ttk
import math

from entities.pixel import Pixel
from entities.line import Line
from algorithms.algorithms import Algorithms

class CanvasApp:
    def __init__(self, root):
        self.initial_pixel = {}
        self.final_pixel = {}
        
        self.window_initial_pixel = {}
        self.window_final_pixel = {}
        
        self.lines = []
        
        self.root = root
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)
        
        self.root.title("Trabalho Prático 1 - Computação Gráfica")

        # Cria o Canvas
        self.canvas = tk.Canvas(root, width=500, height=500, bg="white")
        self.canvas.grid(row=5,column=0)        
        
        # Cria as Labels
        self.label1 = tk.Label(root, text="Valor do Primeiro Ponto:")
        self.label1.grid(row=6,column=0)

        self.label2 = tk.Label(root, text="Valor do Segundo Ponto:")
        self.label2.grid(row=7,column=0)

        # Vinculando botões as ações
        self.canvas.bind("<Button-1>", self.handle_click)
        self.canvas.bind("<Button-3>", self.handle_window_click)
        
        self.menu_bar = tk.Menu(root)
        self.root.config(menu=self.menu_bar)
        
        self.transform_menu = tk.Menu(self.menu_bar)
        self.menu_bar.add_cascade(label="Transformations", menu=self.transform_menu)
        self.transform_menu.add_command(label="Translation", command=self.translation)
        self.transform_menu.add_command(label="Scale", command=self.scale)
        self.transform_menu.add_command(label="Rotate", command=self.rotate)
        self.transform_menu.add_command(label="Reflection X Axis", command=self.reflection_x)
        self.transform_menu.add_command(label="Reflection Y Axis", command=self.reflection_y)
        self.transform_menu.add_command(label="Reflection XY Axis", command=self.reflection_xy)
        
        
        self.rasterization_menu = tk.Menu(self.menu_bar)
        self.menu_bar.add_cascade(label="Rasterization", menu=self.rasterization_menu)
        self.rasterization_menu.add_command(label="Bresenham", command=self.line_bresenham)
        self.rasterization_menu.add_command(label="DDA", command=self.line_dda)
        self.rasterization_menu.add_command(label="Círculo", command=self.circle_bresenham)
        
        self.clip_menu = tk.Menu(self.menu_bar)
        self.menu_bar.add_cascade(label="Clip", menu=self.clip_menu)
        self.clip_menu.add_command(label="Cohen-Sutherland", command=self.clip_image_cohen_sutherland)
        self.clip_menu.add_command(label="Liang-Barsky", command=self.clip_image_liang_barksy)
        
        # Adicionando inputs de apoio
        frame = ttk.Frame(root, padding="30")
        frame.grid(column=0, row=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        x_label = ttk.Label(frame, text="Valor de X:")
        x_label.grid(column=0, row=0, sticky=tk.W)

        self.x_entry = ttk.Entry(frame, width=10)
        self.x_entry.grid(column=1, row=0)

        y_label = ttk.Label(frame, text="Valor de Y:")
        y_label.grid(column=0, row=1, sticky=tk.W)

        self.y_entry = ttk.Entry(frame, width=10)
        self.y_entry.grid(column=1, row=1)
        
        self.degree_label = ttk.Label(frame, text="Valor da rotação:")
        self.degree_label.grid(column=0, row=2, sticky=tk.W)
        
        self.degree = ttk.Entry(frame, width=10)
        self.degree.grid(column=1, row=2)
        
        self.degree_label = ttk.Label(frame, text="Valor da rotação:")
        self.degree_label.grid(column=0, row=2, sticky=tk.W)
        
        self.degree = ttk.Entry(frame, width=10)
        self.degree.grid(column=1, row=2)
        
        button6 = tk.Button(root, text="Limpar Quadro", command=self.clear_canvas)
        button6.grid(row=4,column=0,padx=(5, 5))
        
        # Controle para alternar entre as Labels
        self.is_first_label = True
        self.is_window_first_pixel = True
        
    def is_number(self, value: str):
        try:
            float(value)
            return True
        except:
            return False
        
    # Funções para invocar os métodos responsáveis pelos algoritmos
    def reflection_x(self):
        self.lines = Algorithms().reflection(self.lines, "x", self.canvas)
     
    def reflection_y(self):
        self.lines = Algorithms().reflection(self.lines, 'y', self.canvas)
        
    def reflection_xy(self):
        self.lines = Algorithms().reflection(self.lines, "xy", self.canvas)
        
    def rotate(self):
        degree = int(self.degree.get()) if self.is_number(self.degree.get()) else 0
        self.lines = Algorithms().rotate(self.lines, degree, self.canvas)    
    
    def translation(self):
        x = int(self.x_entry.get()) if self.is_number(self.x_entry.get()) else 0
        y = int(self.y_entry.get()) if self.is_number(self.y_entry.get()) else 0
        self.lines = Algorithms().translation(self.lines, [x, y], self.canvas)
        
    def scale(self):
        x = float(self.x_entry.get()) if self.is_number(self.x_entry.get()) else 1
        y = float(self.y_entry.get()) if self.is_number(self.y_entry.get()) else 1
        self.lines = Algorithms().scale(self.lines, [x, y], self.canvas)

    def line_bresenham(self):
        self.canvas.delete("first_pixel")
        self.canvas.delete("final_pixel")
        self.lines.append(Line(self.initial_pixel, self.final_pixel))      
        Algorithms().line_bresenham_algorithm(self.initial_pixel, self.final_pixel, self.canvas)

    def line_dda(self):
        self.canvas.delete("first_pixel")
        self.canvas.delete("final_pixel")
        self.lines.append(Line(self.initial_pixel, self.final_pixel))
        Algorithms().line_dda_algorithm(self.initial_pixel, self.final_pixel, self.canvas)
        
    def circle_bresenham(self):
        self.canvas.delete("first_pixel")
        self.canvas.delete("final_pixel")
        center_pixel = self.initial_pixel
        radious = abs(math.sqrt(
                (self.final_pixel.x - self.initial_pixel.x)**2 + (self.final_pixel.y - self.initial_pixel.y)**2))
        Algorithms().circle_bresenham_algorithm(center_pixel, radious, self.canvas)

    def format_window(self):
        """
        Ajusta o offset dos pontos selecionados na janela, tornando sempre o pixel com menor (x,y) o inicial
        e o com maior (x,y) o final
        
        Returns:
            (Pixel, Pixel): Pixels inicial e final da janelas formatados
        """
        formatted_initial_pixel = self.window_initial_pixel
        formatted_final_pixel = self.window_final_pixel
        if formatted_initial_pixel.x > formatted_final_pixel.x:
            formatted_initial_pixel.x, formatted_final_pixel.x = formatted_final_pixel.x, formatted_initial_pixel.x
        if formatted_initial_pixel.y > formatted_final_pixel.y:
            formatted_initial_pixel.y, formatted_final_pixel.y = formatted_final_pixel.y, formatted_initial_pixel.y
            
        return formatted_initial_pixel, formatted_final_pixel
    
    def clip_image_cohen_sutherland(self):
        formatted_initial_pixel, formatted_final_pixel = self.format_window()
        self.lines = Algorithms().clip_cohen_sutherland(self.lines, formatted_initial_pixel, formatted_final_pixel, self.canvas)
        
    def clip_image_liang_barksy(self):
        formatted_initial_pixel, formatted_final_pixel = self.format_window()
        self.lines = Algorithms().clip_liang_barsky(self.lines, formatted_initial_pixel, formatted_final_pixel, self.canvas)
    
    def clear_canvas(self):
        self.canvas.delete("all")
        self.lines = []

    def handle_click(self, event):
        """
        Gerencia o clique com o botáo esquerdo, definindo as variáveis de pixel inicial e final
        a partir dos pontos clicados na tela
        
        Args:
            event: Evento de clique com o botão esquerdo
        """
        x, y = event.x, event.y

        if self.is_first_label:
            self.canvas.delete("first_pixel")
            self.initial_pixel = Pixel(x,y)
            self.label1.config(text=f"Valor do Primeiro Ponto: x={x}, y={y}")
            self.canvas.create_rectangle(x,y,x+1,y-1, fill="black", tags="first_pixel")
        else:
            self.canvas.delete("final_pixel")
            self.final_pixel = Pixel(x,y)
            self.label2.config(text=f"Valor do Segundo Ponto: x={x}, y={y}")
            self.canvas.create_rectangle(x,y,x+1,y-1, fill="black", tags="final_pixel")

            
        self.is_first_label = not self.is_first_label

    def handle_window_click(self, event):
        """
        Gerencia o clique com o botão direito, definindo as variáveis de pixel inicial e final
        a partir dos pontos clicados na tela
        
        Args:
            event: Evento de clique com o botão direito
        """
        x, y = event.x, event.y
        if self.is_window_first_pixel:
            self.canvas.delete("window_initial_pixel")
            self.window_initial_pixel = Pixel(x,y)
            self.canvas.create_rectangle(x,y,x+1,y-1, fill="blue", tags="window_initial_pixel")
        else:
            self.canvas.delete("window_final_pixel")
            self.window_final_pixel = Pixel(x,y)
            self.canvas.create_rectangle(x,y,x+1,y-1, fill="blue", tags="window_final_pixel")
            self.canvas.create_rectangle(self.window_initial_pixel.x, self.window_initial_pixel.y,self.window_final_pixel.x, self.window_final_pixel.y, outline="blue", tags="window_final_pixel")

            
        self.is_window_first_pixel = not self.is_window_first_pixel


 