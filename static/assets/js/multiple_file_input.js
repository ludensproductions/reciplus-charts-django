import { create, registerPlugin, setOptions  } from 'https://esm.sh/filepond';

import FilePondPluginImagePreview from 'https://esm.sh/filepond-plugin-image-preview';

import es_ES from 'https://esm.sh/filepond/locale/es-es.js';

setOptions(es_ES)
setOptions({
    credits: null, // Disable credits link
    imagePreviewHeight: 'fixed',
    server: {
        load: (source, load, error, progress, abort, headers) => {

            // Fetch the picture
            fetch(source)
                .then(response => {
                    if (!response.ok) throw new Error('Network response was not ok');
                    return response.blob();
                })
                .then(blob => {
                    // derive filename from source URL (handles queries and relative URLs)
                    let filename;
                    try {
                        const url = new URL(source, window.location.href);
                        filename = decodeURIComponent(url.pathname.split('/').pop() || 'file');
                    } catch (e) {
                        // fallback for non-URL sources
                        filename = decodeURIComponent(String(source).split('?')[0].split('/').pop() || 'file');
                    }
                    const file = new File([blob], filename, { type: blob.type });
                    load(file);
                })
                .catch(err => {
                    console.error('Error fetching image:', err);
                    error(err);
                });

        },
    }
})

registerPlugin(FilePondPluginImagePreview);



const fileInput = document.getElementById('id_files');

// Hidden input to communicate kept existing file IDs to backend
let keptInput = document.getElementById('id_kept_files');
if (!keptInput) {
    keptInput = document.createElement('input');
    keptInput.type = 'hidden';
    keptInput.name = 'kept_files';
    keptInput.id = 'id_kept_files';
    // insert right after file input
    fileInput.parentNode.insertBefore(keptInput, fileInput.nextSibling);
}

const fileInputPond = create(fileInput, {
    allowMultiple: true,
    storeAsFile: true,
});


// Convert server files into FilePond file objects
const preloaded = Array.isArray(fileUrls)
    ? fileUrls.map(f => {
            // Support legacy string array
            if (typeof f === 'string') {
                const name = f.split('/').pop();
                return {
                    source: name,
                    options: {
                        type: 'local',
                        // supply a dummy local file to avoid network loading
                        file: { name, size: 0, type: 'application/octet-stream' },
                        metadata: { id: null, url: f, name }
                    }
                };
            }
            return {
                source: String(f.url),
                options: {
                    type: 'local',
                    metadata: { id: f.id, url: f.url, name: f.name }
                }
            };
        })
    : [];

// Load preloaded files
if (preloaded.length) {
    fileInputPond.addFiles(preloaded);
}

// Initialize kept ids with all preloaded ids (only those with numeric id)
let keptIds = preloaded
    .map(p => p.options?.metadata?.id)
    .filter(id => id !== null && id !== undefined)
    .map(id => String(id));
keptInput.value = JSON.stringify(keptIds.map(Number));

// Track removal of preloaded files: when a 'local' file is removed, drop its id from keptIds
fileInputPond.on('removefile', (error, file) => {
    if (!file) return;
    const metaId = file.getMetadata('id');
    // Only adjust keptIds for preloaded files (identified by having a numeric id)
    if (metaId !== null && metaId !== undefined) {
        const id = String(metaId);
        keptIds = keptIds.filter(x => x !== id);
        keptInput.value = JSON.stringify(keptIds.map(Number));
    }
});

// If user re-adds a preloaded file (unlikely), treat as kept
fileInputPond.on('addfile', (error, file) => {
    if (!file) return;

    requestAnimationFrame(() => {
        const files = fileInputPond.getFiles();
        const images = files.filter(f => f.file?.type?.startsWith('image/'));
        const nonImages = files.filter(f => !f.file?.type?.startsWith('image/'));
        const sorted = [...images, ...nonImages];

        sorted.forEach((f, index) => {
            fileInputPond.moveFile(f.id, index);
        });
    });

    const metaId = file.getMetadata && file.getMetadata('id');
    if (metaId !== null && metaId !== undefined) {
        const id = String(metaId);
        if (!keptIds.includes(id)) {
            keptIds.push(id);
            keptInput.value = JSON.stringify(keptIds.map(Number));
        }
    }
});

// Ensure kept files are synced before submit
const form = fileInput.closest('form');
if (form) {
    form.addEventListener('submit', () => {
        // In case files were manipulated without events, resync from pond state
        const currentPreloaded = fileInputPond.getFiles()
            .map(f => f.getMetadata('id'))
            .filter(id => id !== null && id !== undefined)
            .map(id => Number(id));
        keptInput.value = JSON.stringify(currentPreloaded);
    });
}
