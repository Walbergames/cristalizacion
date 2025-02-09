import moderngl_window as mglw
import numpy as np

class GameOfLife(mglw.WindowConfig):
    window_size = 800, 800
    resource_dir = 'programs'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # Configuración de texturas
        self.textures = [
            self.ctx.texture(self.window_size, 1, dtype='f1'),
            self.ctx.texture(self.window_size, 1, dtype='f1')
        ]
        # Asegurar formato correcto:
        for tex in self.textures:
            tex.filter = (self.ctx.NEAREST, self.ctx.NEAREST)  # Sin interpolación
            tex.repeat_x = False  # Desactivar repetición
            tex.repeat_y = False

        # Patrón inicial aleatorio
        random_data = np.random.randint(0, 256, self.window_size, dtype=np.uint8)  # Valores 0-255
        self.textures[0].write(random_data.tobytes())
        
        self.fbo = self.ctx.framebuffer(self.textures[1])
        self.quad = mglw.geometry.quad_fs()
        
        # Shaders
        self.render_prog = self.load_program(
            vertex_shader='vertex_shader.glsl',
            fragment_shader='render_shader.glsl'
        )
        self.update_prog = self.load_program(
            vertex_shader='vertex_shader.glsl',
            fragment_shader='update_shader.glsl'
        )
        
        self.texture_index = 0

        self.last_update = 0.0

    def on_render(self, time: float, frametime: float):
        # Actualizar cada 0.1 segundos
        if time - self.last_update > 0.1:
            # Paso 1: Actualizar estado
            self.textures[self.texture_index].use(0)
            self.fbo.use()
            self.quad.render(self.update_prog)
            
            # Intercambiar buffers
            self.texture_index = 1 - self.texture_index
            self.last_update = time
        
        # Paso 2: Renderizar siempre
        self.ctx.screen.use()
        self.textures[self.texture_index].use(0)
        self.quad.render(self.render_prog)
        
        # Intercambiar buffers
        self.texture_index = 1 - self.texture_index

if __name__ == '__main__':
    mglw.run_window_config(GameOfLife)