import { useState, useEffect } from 'react';
import axios from 'axios';
import './App.css';

const API_URL = import.meta.env.VITE_API_URL || '/api';

interface ProcesoStatus {
    proceso_id: string;
    estado: 'procesando' | 'completado' | 'error';
    progreso: number;
    mensaje: string;
    carpeta_resultado?: string;
    error?: string;
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
                            <h1 className="title">Pipeline GIS Catastral</h1>
                            <p className="subtitle">Procesamiento Automatizado de Referencias Catastrales</p>
                        </div>
                    </div>
                </div>
            </header>

            <main className="main-content">
                <div className="container">
                    {/* Paso 1: Subir Archivo */}
                    {!procesoId && (
                        <div className="upload-section">
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
                                        {cargando ? '⏳ Iniciando procesamiento...' : '🚀 Procesar Referencias'}
                                    </button>
                                </form>
                            </div>

                            {/* Información */}
                            <div className="info-card">
                                <h3 className="info-title">ℹ️ Información del Pipeline</h3>
                                <div className="info-content">
                                    <div className="info-item">
                                        <span className="info-number">19</span>
                                        <span className="info-label">Pasos Automatizados</span>
                                    </div>
                                    <div className="info-item">
                                        <span className="info-number">12</span>
                                        <span className="info-label">Planos Cartográficos</span>
                                    </div>
                                    <div className="info-item">
                                        <span className="info-number">20+</span>
                                        <span className="info-label">Archivos Generados</span>
                                    </div>
                                </div>

                                <div className="phases">
                                    <h4>Fases del Proceso:</h4>
                                    <ul>
                                        <li>🔍 Fase 1: Adquisición de datos (XML, PDF)</li>
                                        <li>🗺️ Fase 2: Generación vectorial (KML, PNG)</li>
                                        <li>📊 Fase 3: Exportación tabular (Excel, CSV)</li>
                                        <li>📝 Fase 4: Documentación (Logs)</li>
                                        <li>🌍 Fase 5: Análisis espacial (Afecciones)</li>
                                        <li>📍 Fases 6-12: Planos cartográficos</li>
                                    </ul>
                                </div>
                            </div>
                        </div>
                    )}

                    {/* Paso 2: Progreso y Logs */}
                    {procesoId && status && (
                        <div className="processing-section">
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
