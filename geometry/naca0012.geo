Mesh.MshFileVersion = 2.2; // Forza la compatibilidad automática
lc = 1.0;
lc_wing = 0.01; // Malla muy fina cerca del ala para capturar turbulencia

// Dominio del Túnel de Viento
Point(1) = {-5, -5, 0, lc};
Point(2) = {15, -5, 0, lc};
Point(3) = {15,  5, 0, lc};
Point(4) = {-5,  5, 0, lc};
Line(1) = {1, 2}; Line(2) = {2, 3}; Line(3) = {3, 4}; Line(4) = {4, 1};

// Puntos matemáticos del Perfil NACA 0012
Point(5) = {1.0, 0.0, 0, lc_wing};        // Borde de fuga
Point(6) = {0.7, 0.045, 0, lc_wing};
Point(7) = {0.3, 0.06, 0, lc_wing};
Point(8) = {0.0, 0.0, 0, lc_wing};        // Borde de ataque
Point(9) = {0.3, -0.06, 0, lc_wing};
Point(10)= {0.7, -0.045, 0, lc_wing};

Spline(5) = {5, 6, 7, 8}; // Extradós (Arriba)
Spline(6) = {8, 9, 10, 5}; // Intradós (Abajo)

Curve Loop(1) = {1, 2, 3, 4};
Curve Loop(2) = {5, 6};
Plane Surface(1) = {1, 2}; // Superficie con el ala como "agujero"

out[] = Extrude {0, 0, 0.1} { Surface{1}; Layers{1}; Recombine; };

// Etiquetas físicas compatibles con el tutorial airFoil2D
Physical Surface("frontAndBack") = {1, out[0]};
Physical Surface("upperAndLower") = {out[2], out[4]}; 
Physical Surface("outlet") = {out[3]};                
Physical Surface("inlet") = {out[5]};                 
Physical Surface("airfoil") = {out[6], out[7]};       
Physical Volume("internalField") = {out[1]};