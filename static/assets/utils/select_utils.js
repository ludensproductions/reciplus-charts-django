
const getSelected = (selectId) => {
    return $(`#${selectId}`).select2('data').map(data => data.id)
}

const clearSelect = (select) => {
    let def_val = select.querySelector("option[value='']")
    select.innerHTML = ''
    if (def_val)
        select.appendChild(def_val)
}

const fillWithList = (select, keyValList) => {
    let selected = getSelected(select.id);
    clearSelect(select);
    if(keyValList.length === 0) {
        select.disabled = true;
    } else {
        select.disabled = false;
        keyValList.forEach(keyValArr => {
            let opt = document.createElement('option');
            opt.value = keyValArr[0];
            opt.innerHTML = keyValArr[1];
            if (selected.indexOf(`${keyValArr[0]}`) > -1)
                opt.setAttribute('selected', 'selected');
            select.appendChild(opt)
        })
    }
}
