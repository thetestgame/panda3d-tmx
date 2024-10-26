"""
MIT License

Copyright (c) 2024 Jordan Maxwell

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

from panda3d.core import Shader

tmx_layer_frag_shader = """
#version 130
#extension GL_EXT_texture_array : enable

uniform sampler2DArray p3d_Texture0; // Tile Sheets used by this layer

// Input from vertex shader
in vec2 texcoord;
in vec2 tilePosition;
in vec2 tileCount;
in float tileSheet;

// Output from the fragment shader
out vec4 p3d_FragColor;

void main() {
  
  // Calculate our base tile image/frame
  vec2 tileScale = vec2(1.0) / tileCount;
  vec3 tilecoord = vec3(
      (texcoord.x + tilePosition.x) * tileScale.x,
      (texcoord.y * tileScale.y) + tilePosition.y * tileScale.y,
      tileSheet);

  vec4 tileColor = texture2DArray(p3d_Texture0, tilecoord);
  p3d_FragColor = tileColor.rgba;
}
"""

tmx_layer_vert_shader = """
#version 130

// Uniform inputs
uniform mat4 p3d_ModelViewProjectionMatrix;

// Vertex inputs
in vec4 p3d_Vertex;
in vec2 p3d_MultiTexCoord0;

in vec2 frct_tilePosition;
in vec2 frct_tileCount;
in float frct_tileSheet;

// Output to fragment shader
out vec2 texcoord;
out vec2 tilePosition;
out vec2 tileCount;
out float tileSheet;

void main() {
  gl_Position = p3d_ModelViewProjectionMatrix * p3d_Vertex;

  texcoord = p3d_MultiTexCoord0;
  tilePosition = frct_tilePosition;
  tileCount = frct_tileCount;
  tileSheet = frct_tileSheet;
}
"""

tmx_layer_shader = Shader.make(Shader.SL_GLSL, tmx_layer_vert_shader, tmx_layer_frag_shader)