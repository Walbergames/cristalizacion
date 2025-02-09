#version 430
uniform sampler2D stateTexture;
out vec4 fragColor;

void main() {
    // Obtener coordenadas UV correctamente normalizadas
    vec2 uv = gl_FragCoord.xy / textureSize(stateTexture, 0);
    
    // Leer textura y ajustar contraste
    float state = texture(stateTexture, uv).r;
    fragColor = vec4(vec3(step(0.5, state)), 1.0); // Blanco si > 0.5
}