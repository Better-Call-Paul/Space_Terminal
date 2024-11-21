"use client";
"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
var react_1 = require("react");
var fiber_1 = require("@react-three/fiber");
var drei_1 = require("@react-three/drei");
var THREE = require("three");
var Grid = function () {
    var gridRef = (0, react_1.useRef)(null);
    var grid = (0, react_1.useMemo)(function () {
        var gridObject = new THREE.Object3D();
        var material = new THREE.LineBasicMaterial({ color: 0xcccccc, transparent: true, opacity: 0.3 });
        var radius = 1.02; // Slightly larger than the Earth
        var segments = 36;
        // Horizontal lines (latitudes)
        for (var i = 0; i < segments; i++) {
            var lat = (i / segments) * Math.PI - Math.PI / 2;
            var latRadius = Math.cos(lat) * radius;
            var positions = [];
            for (var j = 0; j <= segments; j++) {
                var lon = (j / segments) * Math.PI * 2;
                positions.push(latRadius * Math.sin(lon), radius * Math.sin(lat), latRadius * Math.cos(lon));
            }
            var geometry = new THREE.BufferGeometry();
            geometry.setAttribute('position', new THREE.Float32BufferAttribute(positions, 3));
            var line = new THREE.Line(geometry, material);
            gridObject.add(line);
        }
        // Vertical lines (longitudes)
        for (var i = 0; i < segments; i++) {
            var lon = (i / segments) * Math.PI * 2;
            var positions = [];
            for (var j = 0; j <= segments; j++) {
                var lat = (j / segments) * Math.PI - Math.PI / 2;
                var latRadius = Math.cos(lat) * radius;
                positions.push(latRadius * Math.sin(lon), radius * Math.sin(lat), latRadius * Math.cos(lon));
            }
            var geometry = new THREE.BufferGeometry();
            geometry.setAttribute('position', new THREE.Float32BufferAttribute(positions, 3));
            var line = new THREE.Line(geometry, material);
            gridObject.add(line);
        }
        return gridObject;
    }, []);
    (0, fiber_1.useFrame)(function () {
        if (gridRef.current) {
            gridRef.current.rotation.y += 0.001;
        }
    });
    return <primitive object={grid} ref={gridRef}/>;
};
var Particles = function (_a) {
    var onSelectParticle = _a.onSelectParticle;
    var particlesRef = (0, react_1.useRef)(null);
    var _b = (0, fiber_1.useThree)(), raycaster = _b.raycaster, camera = _b.camera, mouse = _b.mouse;
    var particlesCount = 2000;
    var _c = (0, react_1.useMemo)(function () {
        var positions = new Float32Array(particlesCount * 3);
        var speeds = new Float32Array(particlesCount);
        var orbits = [];
        for (var i = 0; i < particlesCount; i++) {
            var theta = Math.random() * Math.PI * 2;
            var phi = Math.acos((Math.random() * 2) - 1);
            var r = 1.01; // Slightly above the Earth's surface
            positions[i * 3] = r * Math.sin(phi) * Math.cos(theta);
            positions[i * 3 + 1] = r * Math.sin(phi) * Math.sin(theta);
            positions[i * 3 + 2] = r * Math.cos(phi);
            speeds[i] = 0.0002 + Math.random() * 0.0008; // Slower speeds
            // Generate orbit points
            var orbitPoints = [];
            for (var j = 0; j < 100; j++) {
                var angle = (j / 100) * Math.PI * 2;
                orbitPoints.push(r * Math.sin(phi) * Math.cos(theta + angle), r * Math.sin(phi) * Math.sin(theta + angle), r * Math.cos(phi));
            }
            orbits.push(orbitPoints);
        }
        return [positions, speeds, orbits];
    }, []), positions = _c[0], speeds = _c[1], orbits = _c[2];
    (0, fiber_1.useFrame)(function () {
        if (particlesRef.current) {
            var positionsArray = particlesRef.current.geometry.attributes.position.array;
            for (var i = 0; i < particlesCount; i++) {
                var i3 = i * 3;
                var x = positionsArray[i3];
                //const y = positionsArray[i3 + 1]
                var z = positionsArray[i3 + 2];
                // Rotate around the y-axis
                var angle = speeds[i];
                var newX = x * Math.cos(angle) - z * Math.sin(angle);
                var newZ = x * Math.sin(angle) + z * Math.cos(angle);
                positionsArray[i3] = newX;
                positionsArray[i3 + 2] = newZ;
            }
            particlesRef.current.geometry.attributes.position.needsUpdate = true;
        }
    });
    var handleClick = function (event) {
        raycaster.setFromCamera(mouse, camera);
        var intersects = raycaster.intersectObject(particlesRef.current);
        if (intersects.length > 0) {
            var index = intersects[0].index;
            if (index !== undefined) {
                onSelectParticle(orbits[index]);
            }
        }
    };
    return (<points ref={particlesRef} onClick={handleClick}>
      <bufferGeometry>
        <bufferAttribute attachObject={['attributes', 'position']} count={positions.length / 3} array={positions} itemSize={3}/>
      </bufferGeometry>
      <pointsMaterial size={0.01} color="red"/>
    </points>);
};
var Earth = function () {
    var earthRef = (0, react_1.useRef)(null);
    var texture = (0, fiber_1.useLoader)(THREE.TextureLoader, '/assets/3d/texture_earth.jpg');
    // Create a grey and black version of the texture
    var greyAndBlackTexture = (0, react_1.useMemo)(function () {
        var canvas = document.createElement('canvas');
        var context = canvas.getContext('2d');
        if (!context) {
            console.error('Failed to get 2D context');
            return texture;
        }
        var image = texture.image;
        canvas.width = image.width;
        canvas.height = image.height;
        context.drawImage(image, 0, 0);
        var imageData = context.getImageData(0, 0, canvas.width, canvas.height);
        var data = imageData.data;
        for (var i = 0; i < data.length; i += 4) {
            var avg = (data[i] + data[i + 1] + data[i + 2]) / 3;
            if (avg > 128) {
                // Land: grey
                data[i] = data[i + 1] = data[i + 2] = 150;
            }
            else {
                // Ocean: black
                data[i] = data[i + 1] = data[i + 2] = 0;
            }
        }
        context.putImageData(imageData, 0, 0);
        return new THREE.CanvasTexture(canvas);
    }, [texture]);
    (0, fiber_1.useFrame)(function () {
        if (earthRef.current) {
            earthRef.current.rotation.y += 0.001;
        }
    });
    return (<drei_1.Sphere ref={earthRef} args={[1, 64, 64]}>
      <meshStandardMaterial map={greyAndBlackTexture}/>
    </drei_1.Sphere>);
};
var Scene = function () {
    var _a = (0, react_1.useState)(null), selectedOrbit = _a[0], setSelectedOrbit = _a[1];
    return (<>
      <ambientLight intensity={0.5}/>
      <pointLight position={[10, 10, 10]}/>
      <Earth />
      <Grid />
      <Particles onSelectParticle={setSelectedOrbit}/>
      {selectedOrbit && (<drei_1.Line points={selectedOrbit} color="yellow" lineWidth={4}/>)}
      <drei_1.OrbitControls enableZoom={true} enablePan={true} enableRotate={true}/>
    </>);
};
function Component() {
    return (<div className="w-full h-screen bg-black">
      <fiber_1.Canvas camera={{ position: [0, 0, 2.5] }}>
        <Scene />
      </fiber_1.Canvas>
      <div className="absolute top-4 right-4 text-white bg-black bg-opacity-50 p-2 rounded">
        <p>Name: STARLINK-5414</p>
        <p>NORAD ID: 54809</p>
        <p>COSPAR: 2022-175BD</p>
        <p>Orbit: 539 x 541, 53.22°</p>
      </div>
      <div className="absolute bottom-4 left-4 text-white">
        <button className="bg-yellow-500 text-black px-2 py-1 rounded mr-2">-16x</button>
        <button className="bg-yellow-500 text-black px-2 py-1 rounded mr-2">-4x</button>
        <button className="bg-yellow-500 text-black px-2 py-1 rounded mr-2">Live</button>
        <button className="bg-yellow-500 text-black px-2 py-1 rounded mr-2">+4x</button>
        <button className="bg-yellow-500 text-black px-2 py-1 rounded">+16x</button>
      </div>
    </div>);
}
exports.default = Component;
