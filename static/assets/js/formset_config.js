export function getFormsetConfig() {
    const configElement = document.getElementById("formset-config");
    if (!configElement) return { formId: "form-fixed-id", formsets: {} };

    const rawConfig = JSON.parse(configElement.textContent);
    const processedFormsets = {};

    (rawConfig.formsets || []).forEach(function (formset) {
        processedFormsets[`list_${formset.prefix}`] = {
            total_forms_id: `id_${formset.prefix}-TOTAL_FORMS`,
            initial_forms_id: `id_${formset.prefix}-INITIAL_FORMS`,
            oneToNFormsets: formset.oneToNFormsets,
        };
    });

    return {
        formId: rawConfig.formId || "form-fixed-id",
        formsets: processedFormsets,
    };
}
