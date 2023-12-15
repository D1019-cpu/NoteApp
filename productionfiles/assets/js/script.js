// console.log("Hello World!");
const notesElem = document.getElementById('notes');
const addNoteBtn = document.getElementById('add-note');

$.ajax({
    type: 'GET',
    url: `/note-list/`,
    success: function(response) {
        // console.log(response.notes);
        const notes = response.notes;
        notes.map(note => {
            // console.log(note);
            const noteElem = document.createElement('div');
            noteElem.classList.add('note');
            noteElem.setAttribute('data-id', note.id);

            noteElem.innerHTML = `
                    <div class="tools">
                        
                        <div>
                            <div></div>
                            <button class="save hidden">
                                <i class="fa-solid fa-floppy-disk"></i>
                            </button>
                        </div>
                        
                        <div>
                            <button class="edit">
                                <i class="fa-solid fa-pen-to-square"></i>
                            </button>
                            <button class="delete">
                                <i class="fa-solid fa-trash-can"></i>
                            </button>
                        </div>
                    </div>
                    <div class="main">${note.content}</div>
                    <textarea class="hidden"></textarea>
            `;

            const saveBtn = noteElem.querySelector('.save');
            const editBtn = noteElem.querySelector('.edit');
            const deleteBtn = noteElem.querySelector('.delete');

            const main = noteElem.querySelector('.main');
            const textArea = noteElem.querySelector('textarea');

            const noteContent = note.content;
            main.innerHTML = marked.parse(noteContent);

            const csrfToken = document.getElementsByName("csrfmiddlewaretoken")[0].value;
            let noteId = noteElem.getAttribute('data-id');
            
            saveBtn.addEventListener('click', () => {
                let content = textArea.value;
                // console.log(csrfToken);
                // console.log(content);
                // console.log(noteId);

                const requestData = {
                    csrfmiddlewaretoken: csrfToken,
                    content: content
                }

                $.ajax({
                    type: 'POST',
                    url: `/note/save/${noteId}/`,
                    data: requestData,
                    success: function(response) {
                        console.log(response);
                    },
                    error: function(error) {
                        console.log(error);
                    }
                });

                editBtn.classList.toggle('hidden');
                saveBtn.classList.toggle('hidden');
                main.classList.toggle('hidden');
                textArea.classList.toggle('hidden');
            });

            editBtn.addEventListener('click', () => {
                main.classList.toggle('hidden');
                textArea.classList.toggle('hidden');
                editBtn.classList.toggle('hidden');
                saveBtn.classList.toggle('hidden');

                textArea.innerHTML = noteContent;
            });

            deleteBtn.addEventListener('click', () => {
                const deleteData = {
                    csrfmiddlewaretoken: csrfToken
                }
                $.ajax({
                    type: 'POST',
                    url: `/note/delete/${noteId}/`,
                    data: deleteData,
                    success: function(response) {
                        console.log(response);
                    },
                    error: function(error) {
                        console.log(error);
                    }
                });

                noteElem.remove()
            });

            textArea.addEventListener('input', (e) => {
                const {value} = e.target;
                main.innerHTML = marked.parse(value);
            });

            notesElem.appendChild(noteElem);
        });
    },
    error: function(error) {
        console.log(error);
    }
});


addNoteBtn.addEventListener('click', () => {
    const csrfToken = document.getElementsByName("csrfmiddlewaretoken")[0].value;
    const createData = {
        csrfmiddlewaretoken: csrfToken
    }
    $.ajax({
        type: 'POST',
        url: '/note/create/',
        data: createData,
        success: function(response) {
            console.log(response);
            location.reload(true);
        },
        error: function(error) {
            console.log(error);
        }
    });
    
});

