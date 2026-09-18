// geometry/cavity.geo
lc = 0.025; // Tamaño base

// 1. Puntos del cuadrado
Point(1) = {0, 0, 0, lc};
Point(2) = {1, 0, 0, lc};
Point(3) = {1, 1, 0, lc};
Point(4) = {0, 1, 0, lc};

// 2. Líneas
Line(1) = {1, 2}; // Abajo
Line(2) = {2, 3}; // Derecha
Line(3) = {3, 4}; // Arriba (Tapa móvil)
Line(4) = {4, 1}; // Izquierda

// 3. Malla estructurada 41x41
Transfinite Curve {1, 2, 3, 4} = 41;
Curve Loop(1) = {1, 2, 3, 4};
Plane Surface(1) = {1};
Transfinite Surface {1};
Recombine Surface {1}; // Cuadriláteros en vez de triángulos

// 4. Extrusión 3D (1 sola capa para OpenFOAM)
out[] = Extrude {0, 0, 0.1} {
  Surface{1}; Layers{1}; Recombine;
};

// 5. Nombres de las fronteras físicas
// out[0] es la cara frontal, out[2..5] son las caras laterales extruidas
Physical Surface("frontAndBack") = {1, out[0]};
Physical Surface("fixedWalls") = {out[2], out[3], out[5]};
Physical Surface("movingWall") = {out[4]};
Physical Volume("internalField") = {out[1]};