import Sortable from 'https://cdn.jsdelivr.net/npm/@shopify/draggable/build/esm/Sortable/Sortable.mjs';
import * as Plugins from 'https://cdn.jsdelivr.net/npm/@shopify/draggable/build/esm/Plugins/index.mjs';

function SetupPermission() {
    const containers = document.querySelectorAll('#permission-section .StackedList');

    const sortable = new Sortable(containers, {
        draggable: '.draggable-item',
        mirror: {
            constrainDimensions: true,
        },
        plugins: [Plugins.ResizeMirror],
    });

    let initialContainer;

    // --- Draggable events --- //
    sortable.on('drag:start', (evt) => {
        evt.originalSource.classList.toggle('item-selected');
        initialContainer = evt.sourceContainer.parentElement.parentElement.id;
    });

    sortable.on('drag:stopped', (evt) => {
        const container = evt.originalSource.parentElement.parentElement.parentElement.id;
        if (initialContainer !== container) {
            evt.originalSource.classList.remove('item-selected');
        }
    });

    return sortable;
}

SetupPermission();
