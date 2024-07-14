document.getElementById('addCommentBtn').addEventListener('click', function() {
    const commentSection = document.getElementById('commentSection');
    const commentInput = document.getElementById('commentInput');
    const commentText = commentInput.value;

    if (commentText === '') {
        alert('Por favor, escribe un comentario.');
        return;
    }

    const commentDiv = document.createElement('div');
    commentDiv.className = 'comment';

    const commentContent = document.createElement('p');
    commentContent.textContent = commentText;

    const deleteBtn = document.createElement('button');
    deleteBtn.textContent = 'Eliminar';
    deleteBtn.addEventListener('click', function() {
        commentSection.removeChild(commentDiv);
    });

    commentDiv.appendChild(commentContent);
    commentDiv.appendChild(deleteBtn);
    commentSection.appendChild(commentDiv);

    commentInput.value = ''; // Clear the input
});
