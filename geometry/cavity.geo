lc = 0.025;
Point(1) = {0, 0, 0, lc};
Point(2) = {1, 0, 0, lc};
Point(3) = {1, 1, 0, lc};
Point(4) = {0, 1, 0, lc};
Line(1) = {1, 2};
Line(2) = {2, 3};
Line(3) = {3, 4};
Line(4) = {4, 1};
Transfinite Curve {1, 2, 3, 4} = 41;
Curve Loop(1) = {1, 2, 3, 4};
Plane Surface(1) = {1};
Transfinite Surface {1};
Recombine Surface {1};

// Extrusión 3D (1 capa para OpenFOAM)
out[] = Extrude {0, 0, 0.1} {
  Surface{1}; Layers{1}; Recombine;
};

Physical Surface("frontAndBack") = {1, out[0]};
Physical Surface("fixedWalls") = {out[2], out[3], out[5]};
Physical Surface("movingWall") = {out[4]};
Physical Volume("internalField") = {out[1]};