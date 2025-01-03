document.addEventListener('DOMContentLoaded', function() {
    // Constantes
    const API_URL = 'http://localhost:5000';
    const uploadArea = document.getElementById('upload-area');
    const fileInput = document.getElementById('csv-file');
    const fileInfo = document.getElementById('file-info');
    const querySection = document.querySelector('.query-section');
    const queryInput = document.getElementById('query-input');
    const resultsSection = document.getElementById('query-results');
    const viewLogsBtn = document.getElementById('view-logs');
    const logsContent = document.getElementById('logs-content');
    const downloadResultsBtn = document.getElementById('download-results');

    let currentQueryType = null; // Tipo de query actual
    let lastQueryResults = []; // Últimos resultados del query SELECT

    // Agregar soporte para Drag and Drop
    uploadArea.addEventListener('dragover', (e) => {
        e.preventDefault();
        e.stopPropagation();
        uploadArea.classList.add('dragging');
    });

    uploadArea.addEventListener('dragleave', (e) => {
        e.preventDefault();
        e.stopPropagation();
        uploadArea.classList.remove('dragging');
    });

    uploadArea.addEventListener('drop', (e) => {
        e.preventDefault();
        e.stopPropagation();
        uploadArea.classList.remove('dragging');

        const files = e.dataTransfer.files;
        if (files.length > 0) {
            handleFileUpload({ target: { files: [files[0]] } });
        }
    });

    // Manejar selección manual de archivo
    fileInput.addEventListener('change', handleFileUpload);

    const executeBtn = document.getElementById('execute-query');
    executeBtn.addEventListener('click', async () => {
        const query = queryInput.value.trim();
        if (!query) {
            alert('Please enter a query');
            return;
        }

        try {
            const response = await fetch(`${API_URL}/query`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ query: query })
            });

            const data = await response.json();
            console.log('Query response:', data);  // Debug

            if (data.success) {
                currentQueryType = data.operation; // Guardar el tipo de operación actual
                displayResults(data.data, data.operation);
            } else {
                alert(data.message);
            }
        } catch (error) {
            console.error('Error executing query:', error);
            alert('Error executing query');
        }
    });

    viewLogsBtn.addEventListener('click', async () => {
        try {
            const response = await fetch(`${API_URL}/logs`);
            const data = await response.json();
            console.log('Logs response:', data); // Debug

            if (data.success) {
                // Mostrar los logs en una tabla
                logsContent.innerHTML = `
                    <table class="logs-table">
                        <thead>
                            <tr>
                                <th>Timestamp</th>
                                <th>Query</th>
                                <th>Browser</th>
                                <th>OS</th>
                                <th>Method</th>
                            </tr>
                        </thead>
                        <tbody>
                            ${data.data.map(log => `
                                <tr>
                                    <td>${log.timestamp || 'N/A'}</td>
                                    <td>${log.query || 'N/A'}</td>
                                    <td>${log.browser} ${log.browser_version}</td>
                                    <td>${log.os} ${log.os_version}</td>
                                    <td>${log.method}</td>
                                </tr>
                            `).join('')}
                        </tbody>
                    </table>
                `;
                logsContent.classList.remove('hidden');
            } else {
                alert(data.message);
            }
        } catch (error) {
            console.error('Error fetching logs:', error);
            alert('Error fetching logs');
        }
    });

    // Manejador de carga de archivo
    async function handleFileUpload(e) {
        const file = e.target.files[0];
        if (!file) return;
    
        const formData = new FormData();
        formData.append('file', file);
    
        try {
            const response = await fetch(`${API_URL}/csv/upload`, {
                method: 'POST',
                body: formData
            });
    
            const data = await response.json();
            console.log('Respuesta del servidor:', data);  // Debug
    
            if (data.success) {
                fileInfo.innerHTML = `
                    <p>File loaded: ${file.name}</p>
                    <p>Total rows: ${data.metadata.total_rows}</p>
                    <p>Columns: ${data.metadata.columns.join(', ')}</p>
                `;
                fileInfo.classList.remove('hidden');
                querySection.style.display = 'block';
                console.log('Mostrando sección de queries');
            } else {
                console.log('Error en la carga:', data.message);  // Debug
                alert(data.message || 'Error uploading file');
            }
        } catch (error) {
            console.error('Error uploading file:', error);
            alert('Error uploading file');
        }
    }
    

    function displayResults(data, queryType) {
        resultsSection.classList.remove('hidden');
        const resultsTable = resultsSection.querySelector('.results-table');

        if (queryType === "SELECT") {
            if (data.length === 0) {
                // Mostrar mensaje de resultados vacíos
                resultsTable.innerHTML = '<p>No se encontraron resultados para este query.</p>';
                downloadResultsBtn.classList.add('hidden');
            } else {
                // Renderizar resultados en tabla
                lastQueryResults = data; // Guardar los últimos resultados para descargar
                const table = createTable(data);
                resultsTable.innerHTML = '';
                resultsTable.appendChild(table);
                downloadResultsBtn.classList.remove('hidden');
                downloadResultsBtn.textContent = "Download Results as CSV";
            }
        } else {
            resultsTable.innerHTML = `<p>${data}</p>`;
            downloadResultsBtn.textContent = "Download Updated CSV";
            downloadResultsBtn.classList.remove('hidden');
        }
    }

    downloadResultsBtn.addEventListener('click', async () => {
        if (currentQueryType === "SELECT") {
            downloadAsCSV(lastQueryResults);
        } else {
            await downloadFullCSV();
        }
    });

    function downloadAsCSV(data) {
        if (!data || !data.length) return;

        // Obtener headers de las columnas
        const headers = Object.keys(data[0]);

        // Crear contenido CSV
        const csvContent = [
            headers.join(','), // Header row
            ...data.map(row => headers.map(header => {
                let value = row[header] ?? '';
                if (value.toString().includes(',')) {
                    value = `"${value}"`;
                }
                return value;
            }).join(','))
        ].join('\n');

        // Crear blob y descargar
        const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
        const url = URL.createObjectURL(blob);
        const link = document.createElement('a');
        link.href = url;
        link.download = 'query_results.csv';
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        URL.revokeObjectURL(url);
    }

    async function downloadFullCSV() {
        try {
            const response = await fetch(`${API_URL}/csv/download`);
            if (!response.ok) throw new Error('Download failed');

            const blob = await response.blob();
            const url = URL.createObjectURL(blob);
            const link = document.createElement('a');
            link.href = url;
            link.download = 'updated_data.csv';
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
            URL.revokeObjectURL(url);
        } catch (error) {
            console.error('Error downloading CSV:', error);
            alert('Error downloading CSV');
        }
    }

    function createTable(data) {
        const table = document.createElement('table');
        table.classList.add('results-table');

        // Crear encabezados
        const thead = document.createElement('thead');
        const headerRow = document.createElement('tr');
        Object.keys(data[0] || {}).forEach(key => {
            const th = document.createElement('th');
            th.textContent = key;
            headerRow.appendChild(th);
        });
        thead.appendChild(headerRow);
        table.appendChild(thead);

        // Crear filas de datos
        const tbody = document.createElement('tbody');
        data.forEach(row => {
            const tr = document.createElement('tr');
            Object.values(row).forEach(value => {
                const td = document.createElement('td');
                td.textContent = value;
                tr.appendChild(td);
            });
            tbody.appendChild(tr);
        });
        table.appendChild(tbody);

        return table;
    }
});
