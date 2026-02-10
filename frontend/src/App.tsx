import { useState, useEffect } from 'react';
import axios from 'axios';
import { MapContainer, TileLayer, Polygon, Popup, useMap } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import L from 'leaflet';
import './App.css';

// Fix para iconos de Leaflet en React
import icon from 'leaflet/dist/images/marker-icon.png';
import iconShadow from 'leaflet/dist/images/marker-shadow.png';

let DefaultIcon = L.icon({
    iconUrl: icon,
    shadowUrl: iconShadow,
    iconSize: [25, 41],
    iconAnchor: [12, 41]
});
L.Marker.prototype.options.icon = DefaultIcon;

// Usamos ruta relativa siempre. El proxy (dev) o Nginx (prod) se encargan del resto.
const API_URL = '/api';


interface ProcesoStatus {
    proceso_id: string;
    estado: 'procesando' | 'completado' | 'error';
    progreso: number;
    mensaje: string;
    carpeta_resultado?: string;
    geometrias?: { refcat: string; coords: [number, number][] }[];
    error?: string;
}

// Componente para auto-ajustar el zoom del mapa a las parcelas
function FitBounds({ geometrias }: { geometrias: NonNullable<ProcesoStatus['geometrias']> }) {
    const map = useMap();
    useEffect(() => {
        if (geometrias && geometrias.length > 0) {
            const points = geometrias.flatMap(g => g.coords);
            if (points.length > 0) {
                const bounds = L.latLngBounds(points);
                map.fitBounds(bounds, { padding: [50, 50] });
            }
        }
    }, [geometrias, map]);
    return null;
}

function App() {
    const [archivo, setArchivo] = useState<File | null>(null);
    const [procesoId, setProcesoId] = useState<string | null>(null);
    const [status, setStatus] = useState<ProcesoStatus | null>(null);
    const [logs, setLogs] = useState<string[]>([]);
    const [cargando, setCargando] = useState(false);
    const [arrastrando, setArrastrando] = useState(false);

    // Polling para obtener estado del proceso
    useEffect(() => {
        if (!procesoId) return;

        const interval = setInterval(async () => {
            try {
                const response = await axios.get<ProcesoStatus>(`${API_URL}/status/${procesoId}`);
                setStatus(response.data);

                // Obtener logs
                const logsResponse = await axios.get<{ logs: string[] }>(`${API_URL}/logs/${procesoId}`);
                setLogs(logsResponse.data.logs);

                // Detener polling si completó o hubo error
                if (response.data.estado === 'completado' || response.data.estado === 'error') {
                    clearInterval(interval);
                }
            } catch (error) {
                console.error('Error obteniendo estado:', error);
            }
        }, 2000); // Cada 2 segundos

        return () => clearInterval(interval);
    }, [procesoId]);

    const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        if (e.target.files && e.target.files[0]) {
            setArchivo(e.target.files[0]);
        }
    };

    const handleDragOver = (e: React.DragEvent) => {
        e.preventDefault();
        setArrastrando(true);
    };

    const handleDragLeave = () => {
        setArrastrando(false);
    };

    const handleDrop = (e: React.DragEvent) => {
        e.preventDefault();
        setArrastrando(false);

        if (e.dataTransfer.files && e.dataTransfer.files[0]) {
            const droppedFile = e.dataTransfer.files[0];
            if (droppedFile.name.endsWith('.txt')) {
                setArchivo(droppedFile);
            } else {
                alert('Por favor, sube un archivo .txt');
            }
        }
    };

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();

        if (!archivo) {
            alert('Por favor, selecciona un archivo .txt');
            return;
        }

        setCargando(true);
        setStatus(null);
        setLogs([]);

        const formData = new FormData();
        formData.append('file', archivo);

        console.log(`Enviando petición a: ${API_URL}/upload`);
        try {
            const response = await axios.post(`${API_URL}/upload`, formData, {
                headers: { 'Content-Type': 'multipart/form-data' }
            });

            setProcesoId(response.data.proceso_id);
        } catch (error: any) {
            alert('Error al subir el archivo: ' + (error.response?.data?.detail || error.message));
            setCargando(false);
        }
    };

    const handleDescargar = async () => {
        if (!procesoId) return;

        try {
            const response = await axios.get(`${API_URL}/download/${procesoId}`, {
                responseType: 'blob'
            });

            const url = window.URL.createObjectURL(new Blob([response.data]));
            const link = document.createElement('a');
            link.href = url;
            link.setAttribute('download', `resultados-${procesoId}.zip`);
            document.body.appendChild(link);
            link.click();
            link.remove();
        } catch (error: any) {
            alert('Error al descargar: ' + (error.response?.data?.detail || error.message));
        }
    };

    const handleNuevoProceso = () => {
        setArchivo(null);
        setProcesoId(null);
        setStatus(null);
        setLogs([]);
        setCargando(false);
    };

    return (
        <div className="app">
            {/* Header */}
            <header className="header">
                <div className="header-content">
                    <div className="logo-section">
                        <div className="logo-icon">🗺️</div>
                        <div>
                            <h1 className="title">Mi Visor Catastral</h1>
                            <p className="subtitle">Gestión Inteligente de Parcelas</p>
                        </div>
                    </div>
                </div>
            </header>

            <main className="main-content">
                <div className="container">
                    {/* Paso 1: Subir Archivo */}
                    {!procesoId && (
                        <div className="upload-section">
                            {/* Columna Izquierda: Formulario */}
                            <div className="left-column">
                                <div className="card">
                                    <h2 className="section-title">📤 Subir Archivo</h2>
                                    <p className="section-description">
                                        Sube un archivo .txt con referencias catastrales (una por línea)
                                    </p>

                                    <form onSubmit={handleSubmit}>
                                        <div
                                            className={`dropzone ${arrastrando ? 'dragging' : ''} ${archivo ? 'has-file' : ''}`}
                                            onDragOver={handleDragOver}
                                            onDragLeave={handleDragLeave}
                                            onDrop={handleDrop}
                                        >
                                            {!archivo ? (
                                                <>
                                                    <div className="dropzone-icon">📁</div>
                                                    <p className="dropzone-text">
                                                        Arrastra un archivo .txt aquí<br />o haz clic para seleccionar
                                                    </p>
                                                    <input
                                                        type="file"
                                                        accept=".txt"
                                                        onChange={handleFileChange}
                                                        className="file-input"
                                                        id="file-input"
                                                    />
                                                    <label htmlFor="file-input" className="file-label">
                                                        Seleccionar archivo
                                                    </label>
                                                </>
                                            ) : (
                                                <>
                                                    <div className="file-selected">
                                                        <div className="file-icon">📄</div>
                                                        <div className="file-info">
                                                            <p className="file-name">{archivo.name}</p>
                                                            <p className="file-size">{(archivo.size / 1024).toFixed(2)} KB</p>
                                                        </div>
                                                        <button
                                                            type="button"
                                                            onClick={() => setArchivo(null)}
                                                            className="remove-file"
                                                        >
                                                            ✕
                                                        </button>
                                                    </div>
                                                </>
                                            )}
                                        </div>

                                        <button
                                            type="submit"
                                            disabled={!archivo || cargando}
                                            className="btn btn-primary"
                                        >
                                            {cargando ? '⏳ Iniciando procesamiento...' : '▶️ Procesar Referencias'}
                                        </button>
                                    </form>
                                </div>
                            </div>

                            {/* Columna Derecha: Mapa e Info */}
                            <div className="right-column">
                                {/* Mapa */}
                                <div className="map-card">
                                    <MapContainer center={[40.416775, -3.703790]} zoom={6} scrollWheelZoom={true}>
                                        <TileLayer
                                            attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
                                            url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
                                        />
                                        {/* Renderizar geometrías si existen (incluso de procesos anteriores si se guardaran) */}
                                    </MapContainer>
                                </div>
                            </div>
                        </div>
                    )}

                    {/* Paso 2: Progreso y Logs */}
                    {procesoId && status && (
                        <div className="processing-section">
                            <div className="upload-section">
                                {/* Columna Izquierda: Estado y Logs */}
                                <div className="left-column">
                                    <div className="card">
                                        <h2 className="section-title">
                                            {status.estado === 'procesando' && '⏳ Procesando...'}
                                            {status.estado === 'completado' && '✅ Completado'}
                                            {status.estado === 'error' && '❌ Error'}
                                        </h2>

                                        {/* Barra de Progreso */}
                                        <div className="progress-container">
                                            <div className="progress-info">
                                                <span className="progress-label">{status.mensaje}</span>
                                                <span className="progress-percentage">{status.progreso}%</span>
                                            </div>
                                            <div className="progress-bar">
                                                <div
                                                    className={`progress-fill ${status.estado === 'error' ? 'error' : ''}`}
                                                    style={{ width: `${status.progreso}%` }}
                                                />
                                            </div>
                                        </div>

                                        {/* Logs */}
                                        <div className="logs-section">
                                            <h3 className="logs-title">📋 Registro de Actividad</h3>
                                            <div className="logs-container">
                                                {logs.length === 0 ? (
                                                    <p className="logs-empty">Esperando logs...</p>
                                                ) : (
                                                    logs.map((log, index) => (
                                                        <div key={index} className="log-entry">
                                                            {log}
                                                        </div>
                                                    ))
                                                )}
                                            </div>
                                        </div>

                                        {/* Botones de Acción */}
                                        <div className="action-buttons">
                                            {status.estado === 'completado' && (
                                                <>
                                                    <button onClick={handleDescargar} className="btn btn-success">
                                                        📦 Descargar Resultados (ZIP)
                                                    </button>
                                                    <button onClick={handleNuevoProceso} className="btn btn-secondary">
                                                        🔄 Nuevo Proceso
                                                    </button>
                                                </>
                                            )}

                                            {status.estado === 'error' && (
                                                <>
                                                    <div className="error-message">
                                                        ⚠️ {status.error || 'Ocurrió un error durante el procesamiento'}
                                                    </div>
                                                    <button onClick={handleNuevoProceso} className="btn btn-secondary">
                                                        🔄 Intentar de Nuevo
                                                    </button>
                                                </>
                                            )}
                                        </div>
                                    </div>
                                </div>

                                {/* Columna Derecha: Mapa en tiempo real */}
                                <div className="right-column">
                                    <div className="map-card" style={{ height: '100%', minHeight: '500px' }}>
                                        <MapContainer center={[40.416775, -3.703790]} zoom={6} scrollWheelZoom={true}>
                                            <TileLayer
                                                attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
                                                url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
                                            />
                                            {status.geometrias && status.geometrias.map((geo) => (
                                                <Polygon key={geo.refcat} positions={geo.coords} color="blue">
                                                    <Popup>{geo.refcat}</Popup>
                                                </Polygon>
                                            ))}
                                            {status.geometrias && <FitBounds geometrias={status.geometrias} />}
                                        </MapContainer>
                                    </div>
                                </div>
                            </div>
                        </div>
                    )}
                </div>
            </main>

            {/* Footer */}
            <footer className="footer">
                <p>Pipeline GIS Catastral v1.0 | Procesamiento automatizado de datos catastrales</p>
            </footer>
        </div>
    );
}

export default App;
