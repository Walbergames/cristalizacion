#version 430
out vec4 fragColor;
void main() {
    // Obtener la posición del pixel en coordenadas normalizadas (0.0 a 1.0)
    vec2 uv = gl_FragCoord.xy / vec2(1600.0, 900.0);  // Usando el tamaño de la ventana
    
    // Crear el gradiente: rojo (1.0, 0.0, 0.0) a azul (0.0, 0.0, 1.0)
    vec3 col = vec3(1.0 - uv.x, 0.0, uv.x);
    
    fragColor = vec4(col, 1.0);
}