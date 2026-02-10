import { useEffect } from 'react';
import { MapContainer, TileLayer, Polyline, CircleMarker, Popup, useMap } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import './MapViewer.css';

interface Coordinate {
    lat: number;
    lng: number;
}

interface MapViewerProps {
    coordinates?: Coordinate[];
    center?: [number, number];
    zoom?: number;
}

// Componente para ajustar el mapa cuando cambian las coordenadas
function MapBounds({ coordinates }: { coordinates?: Coordinate[] }) {
    const map = useMap();

    useEffect(() => {
        if (coordinates && coordinates.length > 0) {
            const bounds = coordinates.map(coord => [coord.lat, coord.lng] as [number, number]);
            map.fitBounds(bounds, { padding: [50, 50] });
        }
    }, [coordinates, map]);

    return null;
}

export default function MapViewer({ 
    coordinates = [], 
    center = [36.8381, -2.4597], // Almería, España
    zoom = 13 
}: MapViewerProps) {
    
    const hasCoordinates = coordinates && coordinates.length > 0;

    return (
        <div className="map-viewer-container">
            <div className="map-header">
                <h3 className="map-title">🗺️ Visor de Parcelas</h3>
                {hasCoordinates && (
                    <div className="map-stats">
                        <span className="stat-badge">
                            📍 {coordinates.length} punto{coordinates.length !== 1 ? 's' : ''}
                        </span>
                    </div>
                )}
            </div>

            <MapContainer
                center={center}
                zoom={zoom}
                className="map-container"
                scrollWheelZoom={true}
            >
                <TileLayer
                    attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
                    url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
                />

                {hasCoordinates && (
                    <>
                        <MapBounds coordinates={coordinates} />
                        
                        {/* Líneas conectando las parcelas */}
                        <Polyline 
                            positions={coordinates.map(c => [c.lat, c.lng])}
                            pathOptions={{ 
                                color: '#667eea', 
                                weight: 3,
                                opacity: 0.8 
                            }}
                        />

                        {/* Marcadores para cada parcela */}
                        {coordinates.map((coord, index) => (
                            <CircleMarker
                                key={index}
                                center={[coord.lat, coord.lng]}
                                radius={8}
                                pathOptions={{
                                    fillColor: '#667eea',
                                    fillOpacity: 1,
                                    color: 'white',
                                    weight: 3
                                }}
                            >
                                <Popup>
                                    <div className="map-popup">
                                        <strong>Parcela {index + 1}</strong>
                                        <br />
                                        <small>
                                            Lat: {coord.lat.toFixed(6)}<br />
                                            Lng: {coord.lng.toFixed(6)}
                                        </small>
                                    </div>
                                </Popup>
                            </CircleMarker>
                        ))}
                    </>
                )}
            </MapContainer>

            {!hasCoordinates && (
                <div className="map-empty-state">
                    <div className="empty-icon">📍</div>
                    <p>No hay parcelas para mostrar</p>
                    <small>Las parcelas procesadas aparecerán aquí</small>
                </div>
            )}
        </div>
    );
}
