var clipboard = new ClipboardJS('.clipboard');


clipboard.on('success', function(e) {
    console.info('Action:', e.action);
    console.info('Text:', e.text);
    console.info('Trigger:', e.trigger);

    e.clearSelection();
});

clipboard.on('error', function(e) {
    console.error('Action:', e.action);
    console.error('Trigger:', e.trigger);
});

function showLink() {
    var link = document.getElementById('clip');
    var note_io = document.getElementById('foo');
    console.log(note_io.value);
    if (note_io.value != "")
    {
        link.style.display = 'block';
    }
}

showLink();