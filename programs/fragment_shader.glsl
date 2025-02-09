#version 430

out vec4 fragColor;

uniform vec2 resolution;
uniform float time;

void main() {
    vec2 uv = gl_FragCoord.xy / resolution;
    
    // Crear una línea vertical centrada que se mueve
    float linePos = fract(time * 0.5); // Movimiento cíclico cada 2 segundos
    float lineWidth = 0.002;
    
    // Detectar si estamos en la línea móvil
    float line = smoothstep(lineWidth, 0.0, abs(uv.x - linePos));
    
    // Desplazamiento de color (toma el color de la derecha)
    vec3 col = vec3(
        fract(uv.x * 2.0 + time),  // Patrón de color que se desplaza
        mod(uv.y + time * 0.2, 1.0),
        0.5
    );
    
    // Mezclar el color base con el de la línea
    col = mix(col, vec3(1.0, 1.0, 1.0), line);
    
    fragColor = vec4(col, 1.0);
}