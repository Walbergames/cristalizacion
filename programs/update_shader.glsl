#version 430
uniform sampler2D stateTexture;
uniform vec2 resolution;
out vec4 fragColor;

int getCell(vec2 offset) {
    vec2 coord = gl_FragCoord.xy + offset;
    // Manejo de bordes: clamp para evitar coordenadas fuera de la textura
    coord = clamp(coord, vec2(0.5), resolution - vec2(1.5));
    vec2 uv = coord / resolution;
    return int(texture(stateTexture, uv).r > 127.0/255.0); // Umbral 0.5
}

void main() {
    int neighbors = 
        getCell(vec2(-1, -1)) + getCell(vec2(-1, 0)) + getCell(vec2(-1, 1)) +
        getCell(vec2(0, -1))  +                     getCell(vec2(0, 1)) +
        getCell(vec2(1, -1))  + getCell(vec2(1, 0)) + getCell(vec2(1, 1));

    int current = getCell(vec2(0, 0));
    int newState = 0;
    
    // Reglas precisas
    if (current == 1) {
        newState = (neighbors == 2 || neighbors == 3) ? 1 : 0;
    } else {
        newState = (neighbors == 3) ? 1 : 0;
    }
    
    fragColor = vec4(newState * 255.0/255.0); // 0 o 255
}