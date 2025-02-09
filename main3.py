import pygame
from pygame.locals import *
import moderngl
import numpy as np

pygame.init()
window_size = (800, 600)
pygame.display.set_mode(window_size, DOUBLEBUF | OPENGL)
ctx = moderngl.create_context()

# Framebuffers
texture1 = ctx.texture(window_size, 4)
texture2 = ctx.texture(window_size, 4)
framebuffer1 = ctx.framebuffer(texture1)
framebuffer2 = ctx.framebuffer(texture2)

# Shaders corregidos
vertex_shader = '''
#version 330 core
in vec2 in_vert;
out vec2 uv;

void main() {
    gl_Position = vec4(in_vert, 0.0, 1.0);
    uv = in_vert * 0.5 + 0.5;
}
'''

fragment_shader_diamond = '''
#version 330 core
in vec2 uv;
out vec4 color;

void main() {
    vec2 center = vec2(0.5, 0.5);
    vec2 pos = abs(uv - center);
    float diamond = step(pos.x + pos.y, 0.3);
    color = vec4(diamond, diamond * 0.5, 0.0, 1.0);
}
'''

fragment_shader_blur = '''
#version 330 core
uniform sampler2D texture_input;
in vec2 uv;
out vec4 color;

void main() {
    vec2 texel_size = 1.0 / textureSize(texture_input, 0);
    vec3 sum = vec3(0.0);
    
    for(int x = -5; x <= 5; ++x) {
        for(int y = -5; y <= 5; ++y) {
            sum += texture(texture_input, uv + vec2(x, y) * texel_size).rgb;
        }
    }
    
    color = vec4(sum / 100.0, 1.0);
}
'''

# Programas
prog_diamond = ctx.program(
    vertex_shader=vertex_shader,
    fragment_shader=fragment_shader_diamond
)

prog_blur = ctx.program(
    vertex_shader=vertex_shader,
    fragment_shader=fragment_shader_blur
)

# Geometría
vertices = np.array([-1, -1, 1, -1, -1, 1, 1, 1], dtype='f4')
vbo = ctx.buffer(vertices)
vao_diamond = ctx.simple_vertex_array(prog_diamond, vbo, 'in_vert')
vao_blur = ctx.simple_vertex_array(prog_blur, vbo, 'in_vert')

# Bucle principal
clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

    # Dibujar rombo en framebuffer1
    framebuffer1.use()
    ctx.clear()
    vao_diamond.render(mode=moderngl.TRIANGLE_STRIP)

    # Aplicar blur a framebuffer2
    framebuffer2.use()
    texture1.use(0)
    prog_blur['texture_input'] = 0
    vao_blur.render(mode=moderngl.TRIANGLE_STRIP)

    # Mostrar resultado final
    ctx.screen.use()
    ctx.clear()
    texture1.use(0)
    vao_blur.render(mode=moderngl.TRIANGLE_STRIP)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()