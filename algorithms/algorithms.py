import math
from typing import List
from entities.line import Line
from entities.pixel import Pixel
from tkinter import Canvas

class Algorithms:
    def __init__(self) -> None:
        pass
    
    def line_dda_algorithm(self, initial_pixel: Pixel, final_pixel: Pixel, canvas: Canvas) -> None:
        dx = final_pixel.x - initial_pixel.x
        dy = final_pixel.y - initial_pixel.y
        
        passos = 0
        x_incr = y_incr = x = y = 0
        
        if abs(dx) > abs(dy):
            passos = abs(dx)
        else:
            passos = abs(dy)
            
        x_incr = dx / passos
        y_incr = dy / passos
        
        x = initial_pixel.x
        y = initial_pixel.y 
        canvas.create_rectangle(round(x), round(y), round(x+1), round(y+1)) # Desenha um pixel na posição (x,y)
        
        for k in range(passos):
            x = x + x_incr
            y = y + y_incr
            canvas.create_rectangle(round(x), round(y), round(x+1), round(y+1)) # Desenha um pixel na posição (x,y)   
    
    def line_bresenham_algorithm(self, initial_pixel: Pixel, final_pixel: Pixel, canvas: Canvas) -> None:
        dx = final_pixel.x - initial_pixel.x
        dy = final_pixel.y - initial_pixel.y
        
        if (dx >= 0):
            x_incr = 1
        else:
            x_incr = -1
            dx = -dx
            
        if(dy >= 0):
            y_incr = 1
        else:
            y_incr = -1
            dy = -dy
        
        x = initial_pixel.x
        y = initial_pixel.y
        
        canvas.create_rectangle(x, y, x+1, y+1) # Desenha um pixel na posição (x,y)
        
        if dy < dx:
            p = 2 * dy - dx
            const1 = 2 * dy
            const2 = 2 * (dy-dx)
            
            for _ in range(int(dx)):
                x += x_incr
                if p < 0:
                    p += const1
                else:
                    y += y_incr
                    p += const2
                canvas.create_rectangle(x, y, x+1, y+1) # Desenha um pixel na posição (x,y)
        else:
            p = 2 * dx - dy
            const1 = 2 * dx
            const2 = 2 * (dx-dy)
            
            for _ in range(int(dy)):
                y += y_incr
                if p < 0:
                    p += const1
                else:
                    x += x_incr
                    p += const2
                canvas.create_rectangle(x, y, x+1, y+1) # Desenha um pixel na posição (x,y)
                
    def circle_bresenham_algorithm(self, center_pixel: Pixel, radious: int, canvas: Canvas) -> None:
        
        # Procedimento responsável por desenhar os equivalentes em outros quadrantes
        def draw_circle_pixels() -> None: 
            xc = center_pixel.x
            yc = center_pixel.y
            canvas.create_rectangle(xc+x, yc+y, xc+x+1, yc+y+1)
            canvas.create_rectangle(xc-x, yc+y, xc-x+1, yc+y+1)
            canvas.create_rectangle(xc+x, yc-y, xc+x+1, yc-y+1)
            canvas.create_rectangle(xc-x, yc-y, xc-x+1, yc-y+1)
            
            canvas.create_rectangle(xc+y, yc+x, xc+y+1, yc+x+1)
            canvas.create_rectangle(xc-y, yc+x, xc-y+1, yc+x+1)
            canvas.create_rectangle(xc+y, yc-x, xc+y+1, yc-x+1)
            canvas.create_rectangle(xc-y, yc-x, xc-y+1, yc-x+1)
        
        radious = int(radious)
        
        x = 0
        y = radious
        p = 3 - 2 * radious
        draw_circle_pixels()
         
        while x < y:
            if p < 0:
                p += 4*x + 6
            else:
                p += 4*(x-y) + 10
                y -= 1
            
            x += 1
            draw_circle_pixels()

    def clip_cohen_sutherland(self, lines: List[Line], window_min: Pixel, window_max: Pixel, canvas: Canvas) -> List[Line]:
        new_lines: List[Line] = []
        xmin = window_min.x
        ymin = window_min.y
        xmax = window_max.x
        ymax = window_max.y
        
        for line in lines:
            x1 = line.initial_pixel.x
            y1 = line.initial_pixel.y
            x2 = line.final_pixel.x
            y2 = line.final_pixel.y
               
            # Procedimento responsável por determinar o código do pixel
            def region_code(x: int, y: int):
                code = 0
                
                if x < xmin:
                    code += 1
                if x > xmax:
                    code += 2
                if y < ymin:
                    code += 4
                if y > ymax:
                    code += 8

                return code
            
            accept = False
            done = False
            
            while not done:
                c1 = region_code(x1,y1)
                c2 = region_code(x2,y2)
                
                # Teste do cóidigo para otimização
                if c1 == 0 and c2 == 0:
                    accept = True
                    done = True
                elif c1 & c2 != 0:
                    done = True
                else:
                    if c1 != 0:
                        cfora = c1
                    else:
                        cfora = c2
                        
                    # Bloco responsável por executar o AND bitwise do código
                    if cfora & 1:
                        xint = xmin
                        yint = y1+(y2-y1)*(xmin-x1)/(x2-x1)
                    elif cfora & 2:
                        xint = xmax
                        yint = y1+(y2-y1)*(xmax-x1)/(x2-x1)
                    elif cfora & 4:
                        yint = ymin
                        xint = x1+(x2-x1)*(ymin-y1)/(y2-y1)
                    elif cfora & 8:
                        yint = ymax
                        xint = x1+(x2-x1)*(ymax-y1)/(y2-y1)
                        
                    if(c1 == cfora):
                        x1 = xint
                        y1 = yint
                    else:
                        x2=xint
                        y2=yint
                        
            if accept:
                initial_pixel = Pixel(round(x1), round(y1))
                final_pixel = Pixel(round(x2), round(y2))
                new_lines.append(Line(initial_pixel=initial_pixel, final_pixel=final_pixel))

        canvas.delete("all") # Apaga as linhas existentes
        for new_line in new_lines:
            # Desenha todas as linhas presentes na janela
            self.line_bresenham_algorithm(new_line.initial_pixel, new_line.final_pixel, canvas)
        
        return new_lines
    
    def clip_liang_barsky(self, lines: List[Line], window_min: Pixel, window_max: Pixel, canvas: Canvas) -> List[Line]:
        new_lines: List[Line] = []
        xmin = window_min.x
        ymin = window_min.y
        xmax = window_max.x
        ymax = window_max.y
        
        for line in lines:  
            x1 = line.initial_pixel.x
            y1 = line.initial_pixel.y
            x2 = line.final_pixel.x
            y2 = line.final_pixel.y
            
            u1 = 0.0
            u2 = 1.0
            
            dx = x2 - x1
            dy = y2 - y1
            
            def clip_test(p, q):
                nonlocal u1, u2
                result = True
                if p < 0.0:
                    r = q / p
                    if r > u2:
                        result = False
                    elif r > u1:
                        u1 = r
                elif p > 0.0:
                    r = q / p
                    if r < u1:
                        result = False
                    elif r < u2:
                        u2 = r
                elif q < 0.0:
                    result = False
                    
                return result
            
            if clip_test(-dx, x1-xmin):
                if clip_test(dx, xmax - x1):
                    if clip_test(-dy, y1-ymin):
                        if clip_test(dy, ymax - y1):
                            if u2 < 1.0:
                                x2 = x1 + u2 * dx
                                y2 = y1 + u2 * dy
                            if u1 > 0.0:
                                x1 = x1 + u1 * dx
                                y1 = y1 + u1 * dy 
                            initial_pixel = Pixel(round(x1), round(y1))
                            final_pixel = Pixel(round(x2), round(y2))
                            new_lines.append(Line(initial_pixel=initial_pixel, final_pixel=final_pixel))

        canvas.delete("all") # Apaga as linhas existentes
        for new_line in new_lines:
            # Desenha todas as linhas presentes na janela
            self.line_bresenham_algorithm(new_line.initial_pixel, new_line.final_pixel, canvas)
        
        return new_lines
    
    def translation(self, lines: List[Line], translation_vector: List[int], canvas: Canvas) -> List[Line]:
        # translaction_vector é um array [int, int] em que vector[0] é valor de tx e 
        # vector[1] é o valor de ty
        new_lines: List[Line] = []
        for line in lines:
            line.initial_pixel.x += translation_vector[0]
            line.initial_pixel.y += translation_vector[1]
            
            line.final_pixel.x += translation_vector[0]
            line.final_pixel.y += translation_vector[1]
            
            new_lines.append(line)
        
        canvas.delete("all") # Apaga as linhas existentes
        for new_line in new_lines:
            # Desenha todas as linhas com transformação aplicada
            self.line_bresenham_algorithm(new_line.initial_pixel, new_line.final_pixel, canvas)
            
        return new_lines
            
    def scale(self, lines: List[Line], scale_vector: List[int], canvas: Canvas) -> List[Line]:
        new_lines: List[Line] = []
        
        for line in lines:
            line.initial_pixel.x = (line.initial_pixel.x) * scale_vector[0]
            line.initial_pixel.y = (line.initial_pixel.y) * scale_vector[1]
               
            line.final_pixel.x = (line.final_pixel.x) * scale_vector[0]
            line.final_pixel.y = (line.final_pixel.y) * scale_vector[1]
            
            new_lines.append(line)
        
        canvas.delete("all") # Apaga as linhas existentes
        for new_line in new_lines:
            # Desenha todas as linhas com transformação aplicada
            self.line_bresenham_algorithm(new_line.initial_pixel, new_line.final_pixel, canvas)
            
        return new_lines
    
    def rotate(self, lines: List[Line], theta: int, canvas: Canvas) -> List[Line]:
        new_lines: List[Line] = []
        # Define a origem como (0,0), utilizado para não
        # distorcer a reta original
        origin = Pixel(0,0)
        origin_x = origin.x
        origin_y = origin.y
        theta = math.radians(theta)
        
        for line in lines:
            tx = line.initial_pixel.x
            ty = line.initial_pixel.y
            
            line.initial_pixel.x = origin_x
            line.initial_pixel.y = origin_y
            line.final_pixel.x -= tx
            line.final_pixel.y -= ty
            
            initial_rotated_x = line.initial_pixel.x
            initial_rotated_y = line.initial_pixel.y
                
            final_rotated_x = line.final_pixel.x * math.cos(theta) - line.final_pixel.y * math.sin(theta)
            final_rotated_y = line.final_pixel.x * math.sin(theta) + line.final_pixel.y * math.cos(theta)
            
            initial_rotated_x += tx
            initial_rotated_y += ty
            final_rotated_x += tx
            final_rotated_y += ty
            
            rotated_line = Line(Pixel(initial_rotated_x, initial_rotated_y), Pixel(final_rotated_x, final_rotated_y))
            
            new_lines.append(rotated_line)
        
        canvas.delete("all") # Apaga as linhas existentes
        for new_line in new_lines:
            # Desenha todas as linhas com transformação aplicada
            self.line_bresenham_algorithm(new_line.initial_pixel, new_line.final_pixel, canvas)
            
        return new_lines
    
    def reflection(self, lines: List[Line], axisOption, canvas: Canvas) -> List[Line]:
        new_lines: List[Line] = []
        origin = Pixel(round(canvas.winfo_width() / 2), round(canvas.winfo_height() / 2))
        origin_x, origin_y = origin.x, origin.y
        for line in lines:
            if axisOption == 'x':
                new_lines.append(Line(
                    Pixel(line.initial_pixel.x, line.initial_pixel.y - 2 * (line.initial_pixel.y - origin_y)), 
                    Pixel(line.final_pixel.x, line.final_pixel.y - 2 * (line.final_pixel.y - origin_y)))
                )
            elif axisOption == 'y':
                new_lines.append(Line(
                    Pixel(line.initial_pixel.x - 2 * (line.initial_pixel.x - origin_x), line.initial_pixel.y),
                    Pixel(line.final_pixel.x - 2 * (line.final_pixel.x - origin_x), line.final_pixel.y))
                ) 
            else:
                new_lines.append(Line(
                    Pixel(line.initial_pixel.x - 2 * (line.initial_pixel.x - origin_x), line.initial_pixel.y - 2 * (line.initial_pixel.y - origin_y)),
                    Pixel(line.final_pixel.x - 2 * (line.final_pixel.x - origin_x), line.final_pixel.y - 2 * (line.final_pixel.y - origin_y)))
                ) 

        canvas.delete("all") # Apaga as linhas existentes
        for new_line in new_lines:
            # Desenha todas as linhas com transformação aplicada
            self.line_bresenham_algorithm(new_line.initial_pixel, new_line.final_pixel, canvas)
            
        return new_lines