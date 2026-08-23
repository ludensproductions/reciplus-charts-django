# What is Summernote

Summernote is a WYSIWYG editor, this is easy to implement and with a lot of functionalities, but has some problems with latex formulas, there is a plugin called summernote-math, this library is a little bit outdated, so that files has some modifications to work.

## First step
* Get the lastest version of the code in the [link](https://summernote.org/getting-started/)

## Initial setup in html

### Html head
In the html head import cdn for summernote and katex css
```html
<head>

    <!-- Pre-import bootstrap css    -->

    <!-- Summetnote lite css (without bootstrap) -->
    <link href="https://cdn.jsdelivr.net/npm/summernote@0.8.18/dist/summernote-lite.min.css" rel="stylesheet">
    <!-- Katex css -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/KaTeX/0.9.0/katex.min.css">
</head>
```

### Script codes
At the end of the file import cdn for summernote and katex
```html

<!-- Pre-import jquery and bootstrap things    -->

<!-- Summernote lite js (without bootstrap) -->
<script src="https://cdn.jsdelivr.net/npm/summernote@0.8.18/dist/summernote-lite.min.js"></script>
<!-- Summenote pack for spanish (spain) -->
<script src="https://cdn.jsdelivr.net/npm/summernote@0.8.18/dist/lang/summernote-es-ES.min.js"></script>
<!-- Katex js -->
<script src="https://cdnjs.cloudflare.com/ajax/libs/KaTeX/0.9.0/katex.min.js"></script>
<!-- Summernote math library with mods -->
<script src="{% static 'assets/summernote/summernote-math.js' %}"></script>

<script>

    $(document).ready(() => {
        $(`#editor`).summernote({
            lang: 'es-ES',
            placeholder: 'Ingrese un texto',
            tabsize: 4,
            height: 200,
            toolbar: [
                ['style', ['style']],
                ['font', ['bold', 'underline', 'clear']],
                ['color', ['color']],
                ['para', ['ul', 'ol', 'paragraph']],
                ['table', ['table']],
                ['insert', ['link', 'picture', 'math']],
                ['view', ['help']]
            ]
        });
    });

    // Add form-control to summernote file input
    $(document).on('summernote.init', function () {
        $('.note-image-input').addClass('form-control');
    });
</script>
```

### Render katex in normal html

To render katex in normal html it is necessary to import css and js for katex, and write the following code

```html
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.6/dist/katex.min.css"                    integrity="sha384-mXD7x5S50Ko38scHSnD4egvoExgMPbrseZorkbE49evAfv9nNcbrXJ8LLNsDgh9d" crossorigin="anonymous">

    <script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.6/dist/katex.min.js" integrity="sha384-j/ZricySXBnNMJy9meJCtyXTKMhIJ42heyr7oAdxTDBy/CYA9hzpMo+YTNV5C+1X" crossorigin="anonymous"></script>

    <!-- This code turns every katex text into formulas -->
    <script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.6/dist/contrib/auto-render.min.js" integrity="sha384-+VBxd3r6XgURycqtZ117nYw44OOcIax56Z4dCRWbxyPt0Koah1uHoK0o4+/RRE05" crossorigin="anonymous"
        onload="renderMathInElement(document.body);"></script>
```
