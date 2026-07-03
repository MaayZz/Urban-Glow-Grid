import sys

filename = '/Users/Abir/Desktop/innovation project/simulation/Urban_GlowGrid_Simulator.html'
with open(filename, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Change lawn to asphalt
content = content.replace(
    'const lawnMat = new THREE.MeshStandardMaterial({ color: 0x2e5c32, roughness: 0.9 });',
    'const lawnMat = new THREE.MeshStandardMaterial({ color: 0x2b2b2c, roughness: 0.9, metalness: 0.1 });'
)

# 2. Add tri-planar UV mapping to fix texture stretch
uv_fix_code = """
                    // Fix UVs (Tri-planar)
                    geom.computeVertexNormals();
                    if (geom.attributes.uv && geom.attributes.normal) {
                        const pos = geom.attributes.position;
                        const uv = geom.attributes.uv;
                        const norm = geom.attributes.normal;
                        for (let i = 0; i < uv.count; i++) {
                            const nx = Math.abs(norm.getX(i)), ny = Math.abs(norm.getY(i)), nz = Math.abs(norm.getZ(i));
                            const x = pos.getX(i), y = pos.getY(i), z = pos.getZ(i);
                            if (ny > nx && ny > nz) uv.setXY(i, x * 0.05, z * 0.05);
                            else if (nx > ny && nx > nz) uv.setXY(i, z * 0.05, y * 0.05);
                            else uv.setXY(i, x * 0.05, y * 0.05);
                        }
                        uv.needsUpdate = true;
                    }
"""
content = content.replace(
    'const geom = new THREE.ExtrudeGeometry(shape, extrudeSettings);',
    'const geom = new THREE.ExtrudeGeometry(shape, extrudeSettings);' + uv_fix_code
)
content = content.replace(
    'const geom = createMeshGeometry(ent);',
    'const geom = createMeshGeometry(ent);' + uv_fix_code
)

# 3. Thin out buildings and add plazas/fountains
plaza_code = """
            // Thin out Haussmann buildings by 45% randomly
            const isDefense = cx < -150 && cz < -150;
            if (!isDefense && Math.random() < 0.45) {
                // Build a plaza instead!
                const pad = new THREE.Mesh(new THREE.CylinderGeometry(4, 4, 0.5, 16), new THREE.MeshStandardMaterial({ color: 0x9ca3af, roughness: 0.9 }));
                pad.position.set(cx, 0.4, cz);
                pad.receiveShadow = true;
                scene.add(pad);

                const fountain = new THREE.Group();
                fountain.position.set(cx, 0.6, cz);
                const base = new THREE.Mesh(new THREE.CylinderGeometry(1.5, 1.5, 0.5, 8), goldMat);
                base.position.y = 0.25; base.castShadow = true;
                const stem = new THREE.Mesh(new THREE.CylinderGeometry(0.3, 0.3, 1.5, 8), goldMat);
                stem.position.y = 1; stem.castShadow = true;
                const basin = new THREE.Mesh(new THREE.CylinderGeometry(1.2, 1.5, 0.3, 8), goldMat);
                basin.position.y = 1.65; basin.castShadow = true;
                const water = new THREE.Mesh(new THREE.CylinderGeometry(1.3, 1.3, 0.1, 8), new THREE.MeshStandardMaterial({ color: 0x38bdf8, roughness: 0.1, metalness: 0.8 }));
                water.position.y = 1.7;
                fountain.add(base, stem, basin, water);
                scene.add(fountain);
                return;
            }
"""
content = content.replace(
    'const materials = getBuildingMaterials(cx, cz);',
    plaza_code + '\n            const materials = getBuildingMaterials(cx, cz);'
)

# 4. Add the Etoile Avenues
etoile_code = """
    function buildEtoileAvenues() {
        const cx = -373.45;
        const cz = 209.27;
        const starRoadMat = new THREE.MeshStandardMaterial({ color: 0x1e293b, roughness: 0.8, polygonOffset: true, polygonOffsetFactor: -1 });
        
        for (let i = 0; i < 12; i++) {
            const angle = (i / 12) * Math.PI * 2;
            const length = 150;
            const width = 8;
            
            const roadGeom = new THREE.PlaneGeometry(width, length);
            const road = new THREE.Mesh(roadGeom, starRoadMat);
            
            const dx = Math.cos(angle) * (length / 2 + 15);
            const dz = Math.sin(angle) * (length / 2 + 15);
            
            road.position.set(cx + dx, 0.3, cz + dz);
            road.rotation.x = -Math.PI / 2;
            road.rotation.z = -angle + Math.PI / 2;
            road.receiveShadow = true;
            scene.add(road);
        }
    }
"""
content = content.replace('function buildBuildings() {', etoile_code + '\n    function buildBuildings() {')
content = content.replace('buildBuildings();', 'buildBuildings(); buildEtoileAvenues();')

# 5. Fix Camera Clipping (The "Fog" effect at a distance)
content = content.replace('1, 2000);', '1, 10000);')
content = content.replace('controls.maxDistance = 1000;', 'controls.maxDistance = 4000;')
content = content.replace('sun.shadow.camera.far = 1500;', 'sun.shadow.camera.far = 10000;')

# 6. Stylize Background
content = content.replace(
    'scene.background = new THREE.Color(0x090d16);',
    'scene.background = new THREE.Color(0x050510); scene.fog = null;'
)
content = content.replace(
    'const targetSky = isNight ? new THREE.Color(0x05070c) : new THREE.Color(0x0f172a);',
    'const targetSky = isNight ? new THREE.Color(0x020205) : new THREE.Color(0x0a0a1a); scene.fog = null;'
)
content = content.replace(
    'const gridHelper = new THREE.GridHelper(1200, 48, 0x1e3a8a, 0x0f172a);',
    'const gridHelper = new THREE.GridHelper(10000, 200, 0x38bdf8, 0x0f172a);\n        const ringGeom = new THREE.TorusGeometry(BOARD_RADIUS + 2, 2, 16, 100);\n        const ringMat = new THREE.MeshBasicMaterial({ color: 0x38bdf8 });\n        const ring = new THREE.Mesh(ringGeom, ringMat);\n        ring.position.y = -6;\n        ring.rotation.x = Math.PI / 2;\n        scene.add(ring);'
)

# 7. Make stats button more robust
content = content.replace('z-index: 100;', 'z-index: 1000;')
content = content.replace('pointer-events: none;', 'pointer-events: none;') # no-op just to be sure it's there

with open(filename, 'w', encoding='utf-8') as f:
    f.write(content)
print("Patch applied successfully.")
