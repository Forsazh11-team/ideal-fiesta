 let profileMenu = document.getElementById("profileMenu");
    function toggleMenu(){
        profileMenu.classList.toggle("open-menu");
    }


    // Функция для открытия/закрытия меню профиля
    function toggleMenu() {
        var menu = document.getElementById("profileMenu");
        menu.classList.toggle("open-menu");
    }

    // Закрываем меню при клике вне его
    document.addEventListener("click", function(event) {
    var menu = document.getElementById("profileMenu");
    var profileImage = document.querySelector(".nav-profile-img");
    // Проверяем, если клик был за пределами меню и изображения профиля
    if (!menu.contains(event.target) && !profileImage.contains(event.target)) {
        menu.classList.remove("open-menu"); // Закрываем меню
    }
    });


    function autoResize(textarea) {
        textarea.style.height = 'auto'; // Сбрасываем высоту
        textarea.style.height = textarea.scrollHeight + 'px'; // Устанавливаем новую высоту
    }

     $(document).ready(function () {
        $('#submit_button').click(function (e) {
            e.preventDefault(); // Отменяем стандартное поведение формы

            var tweetContent = $('#tweet_content').val();  // Получаем содержимое твита
            var csrfToken = $('input[name="csrfmiddlewaretoken"]').val();  // Получаем CSRF-токен

            if (tweetContent.trim() === "") {
                return;
            }

            // Отправляем данные через AJAX
            $.ajax({
                url: $('#post_form').attr('action'),  // URL формы
                type: 'POST',
                data: {
                    content: tweetContent,
                    csrfmiddlewaretoken: csrfToken
                },
                success: function (response) {
                    // Добавляем новый твит в начало списка
                    // Создаем контейнер для нового твита
                    var newPost = document.createElement('div');
                    newPost.className = 'post';
                    newPost.setAttribute('data-post-id', response.id);

                    // Создаем блок автора поста
                    var postAuthor = document.createElement('div');
                    postAuthor.className = 'post-author';

                    var authorImage = document.createElement('img');
                    authorImage.src = response.author_image;
                    authorImage.alt = '';

                    var authorInfo = document.createElement('div');

                    var authorLink = document.createElement('a');
                    authorLink.href = `/${response.author_username}`;
                    var authorName = document.createElement('h1');
                    authorName.textContent = response.author_username;
                    authorLink.appendChild(authorName);

                    var postDate = document.createElement('small');
                    postDate.textContent = response.date_posted;

                    // Собираем блок автора
                    authorInfo.appendChild(authorLink);
                    authorInfo.appendChild(postDate);
                    postAuthor.appendChild(authorImage);
                    postAuthor.appendChild(authorInfo);

                    // Создаем блок контента поста
                    var postContent = document.createElement('div');
                    postContent.className = 'post-content';
                    postContent.innerHTML = response.content; // Используем innerHTML для вставки HTML-контента

                    // Создаем блок активности поста
                    var postActivity = document.createElement('div');
                    postActivity.className = 'post-activity';

                    var postActivityLink = document.createElement('div');
                    postActivityLink.className = 'post-activity-link';

                    var likeBtn = document.createElement('button');
                    likeBtn.id = `likeBtn-${response.id}`;
                    likeBtn.className = 'like-btn';
                    likeBtn.setAttribute('data-liked', 'false');
                    likeBtn.onclick = function(event) { likeClick(event, response.id); };

                    var likeIcon = document.createElement('i');
                    likeIcon.className = 'far fa-heart';
                    likeBtn.appendChild(likeIcon);

                    var likeCount = document.createElement('span');
                    likeCount.textContent = response.likes; // Используем likes от response

                    postActivityLink.appendChild(likeBtn);
                    postActivityLink.appendChild(likeCount);
                    postActivity.appendChild(postActivityLink);

                    // Создаем элемент ul
                    const tagContainer = document.createElement('ul');
                    tagContainer.className = 'tag-container';

                    // Итерация по тегам и создание элементов li
                    response.hashtags.forEach(tag => {
                        const li = document.createElement('li');

                        const link = document.createElement('a');
                        link.href = `/search/?tag=${encodeURIComponent(tag)}`; // Используем encodeURIComponent для безопасного URL
                        link.style.color = 'white';
                        link.style.textDecoration = 'none'

                        const span = document.createElement('span');
                        span.className = 'tag-label';

                        // Создаем элемент иконки
                        const icon = document.createElement('i');
                        icon.className = 'fas fa-circle';
                        icon.style.marginLeft = '-5px'; // Добавляем отступ

                        // Добавляем иконку и текст тега в span
                        span.appendChild(icon);
                        span.appendChild(document.createTextNode(tag.text));
                        link.appen(span)

                        // Добавляем span в li
                        li.appendChild(link);

                        // Добавляем li в ul
                        tagContainer.appendChild(li);
                    });


                    // Создаем блок комментариев
                    var commentSection = document.createElement('div');
                    commentSection.className = 'comment-section';
                    commentSection.onclick = childClick; // Назначаем обработчик события

                    // Список комментариев
                    var commentList = document.createElement('div');
                    commentList.id = `comment-list-${response.id}`;

                    // Секция для добавления нового комментария
                    var commentItem = document.createElement('div');
                    commentItem.className = 'comment-item';

                    var commentImage = document.createElement('img');
                    commentImage.src = response.author_image;

                    var commentInput = document.createElement('textarea');
                    commentInput.rows = 1;
                    commentInput.className = 'comment-input';
                    commentInput.id = `comment-${response.id}`;
                    commentInput.placeholder = "Напишите ваш комментарий...";
                    commentInput.oninput = function() { autoResize(this); };
                    commentInput.required = true;

                    var submitCommentBtn = document.createElement('button');
                    submitCommentBtn.className = 'submit-comment';
                    submitCommentBtn.onclick = function() { addComment(response.id); };
                    submitCommentBtn.textContent = 'Отправить';

                    // Собираем блок комментариев
                    commentItem.appendChild(commentImage);
                    commentItem.appendChild(commentInput);
                    commentItem.appendChild(submitCommentBtn);
                    commentSection.appendChild(commentList);
                    commentSection.appendChild(commentItem);

                    // Собираем весь пост
                    newPost.appendChild(postAuthor);
                    newPost.appendChild(postContent);
                    newPost.appendChild(postActivity);
                    newPost.appendChild(tagContainer);
                    newPost.appendChild(commentSection);


                    // Добавляем новый твит в начало списка
                    $('#new_tweets').prepend(newPost);

                    // Очищаем поле ввода
                    $('#tweet_content').val('');
                },
                error: function (xhr, status, error) {
                    alert("Error: Unable to post tweet. Please try again.");
                }
            });
        });
    });

    function openModal(tweetId) {
       $.ajax({
        url: `/tweet/${tweetId}/`,
        type: 'GET',
        success: function(data) {
            document.body.classList.add('modal-open');

            // Заполнение модального окна данными твита
            document.getElementById('modal-author').textContent = data.author;
            document.getElementById('modal-content').textContent = data.content;
            document.getElementById('modal-date').textContent = data.date_posted;
            var link = document.getElementById('author-link');
            link.setAttribute("href", `/profile/${data.author}`)
            var imglink = document.getElementById('img-author-link');
            link.setAttribute("href", `/profile/${data.author}`)
            document.getElementById('modal-img').src = data.img;
            document.getElementById('modal-likes-count').textContent = data.likes;
            var button = document.getElementById('modal-likeBtn');
            button.onclick = function(event) {
                ModallikeClick(event, data.id);
            };
            var id = data.id;
            if (data.liked) {
                button.innerHTML='<i class="fas fa-heart" style="color: #704c9e;"></i>'
                button.setAttribute("data-liked", 'true')
            }
            else {
                button.innerHTML='<i class="far fa-heart"></i>'
                button.setAttribute("data-liked", 'false')
            }

            // Создаем элемент ul
            const tagContainer = document.getElementById('modal-tag-container');
            $('#modal-tag-container').empty();

            data.tags.forEach(tag => {
                const li = document.createElement('li');

                const link = document.createElement('a');
                link.href = `/search/?tag=${encodeURIComponent(tag)}`; // Используем encodeURIComponent для безопасного URL
                link.style.color = 'white';
                link.style.textDecoration = 'none'

                const span = document.createElement('span');
                span.className = 'tag-label';

                // Создаем элемент иконки
                const icon = document.createElement('i');
                icon.className = 'fas fa-circle';
                icon.style.marginLeft = '-5px'; // Добавляем отступ

                // Добавляем иконку и текст тега в span
                span.appendChild(icon);
                span.appendChild(document.createTextNode(tag));
                link.appendChild(span);

                // Добавляем span в li
                li.appendChild(link);

                // Добавляем li в ul
                tagContainer.appendChild(li);
            });

            $('#modal-comments').empty();
            data.comments.forEach(comment => {
                // Создание элементов комментария
                var commentItem = $('<div>').addClass('comment-item');
                var commentImg = $('<img>').attr('src', comment.img);
                var commentContent = $('<div>').addClass('comment-content');
                var commentAuthor = $('<strong>').text(comment.author); // текстовое содержимое
                var commentText = $('<p>').text(comment.content); // текстовое содержимое
                var commentDate = $('<span>').addClass('comment-date').text(comment.date_posted);

                // Сборка комментария
                commentContent.append(commentAuthor, commentText, commentDate);
                commentItem.append(commentImg, commentContent);

                // Добавление в модальное окно
                $('#modal-comments').append('<hr class="comment-line">', commentItem);
            });;

            document.getElementById('tweetModal').style.display = 'block';
        },
        error: function(xhr, status, error) {
            console.error('AJAX Error:', error);
        }
    });
    }
    function closeModal() {
        document.body.classList.remove('modal-open');
        const modal = document.getElementById("tweetModal");
        modal.style.display = "none";  // Скрываем модальное окно
    }

    // Закрытие модального окна при клике вне его содержимого
    window.onclick = function(event) {
        const modal = document.getElementById("tweetModal");
        const followings = document.getElementById("followingsModal");
        if (event.target === modal) {
            closeModal();
        }
        if (event.target === followings) {
            closeFollowingsModal();
        }
    }

    
    $(document).ready(function() {
    // Устанавливаем обработчик события клика на все твиты
    $('#new_tweets').on('click', '.post', function() {
        var tweetId = $(this).attr('data-post-id');
        openModal(tweetId)
    });
});


    function addComment(tweetId) {
        const commentInput = document.getElementById(`comment-${tweetId}`).value;
        if (commentInput.trim() === "") {
            alert("Комментарий не может быть пустым");
            return;
        }

        fetch(`/comment/${tweetId}/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken'), // Получаем CSRF-токен
            },
            body: JSON.stringify({ content: commentInput }) // Отправляем коммент
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            location.reload();
        })
    }

    function addModalComment(tweetId) {
        const commentInput = document.getElementById(`comment-modal-${tweetId}`).value;
         fetch(`/comment/${tweetId}/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken'), // Получаем CSRF-токен
            },
            body: JSON.stringify({ content: commentInput }) // Отправляем коммент
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            location.reload();
        })

        // Создание элементов комментария
        var commentItem = $('<div>').addClass('comment-item');
        //var commentImg = $('<img>').attr('src', comment.img);
        var commentContent = $('<div>').addClass('comment-content');
        var commentAuthor = $('<strong>').text("xd"); // текстовое содержимое
        var commentText = $('<p>').text(commentInput); // текстовое содержимое
        var commentDate = $('<span>').addClass('comment-date').text("1111");

        // Сборка комментария
        commentContent.append(commentAuthor, commentText, commentDate);
        commentItem.append(commentImg, commentContent);

        // Добавление в модальное окно
        $('#modal-comments').append('<hr class="comment-line">', commentItem);


    }

    function childClick(event) {
        event.stopPropagation(); // Останавливает всплытие события
    }

    function likeClick(event, tweetId) {
        event.stopPropagation(); // Останавливает всплытие события
        const likeBtn = document.getElementById(`likeBtn-${tweetId}`);
        const likeCountSpan = document.getElementById(`likeCount-${tweetId}`);
        const isLiked = likeBtn.getAttribute('data-liked') === 'true';
        // AJAX-запрос для обновления лайка в базе данных
        fetch(`/like/${tweetId}/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken'), // Получаем CSRF-токен
            },
            body: JSON.stringify({ liked: !isLiked }) // Отправляем статус лайка
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            if (data.liked) {
                likeBtn.setAttribute('data-liked', 'true');
                likeBtn.innerHTML = '<i class="fas fa-heart" style="color: #704c9e;"></i>'; // Закрашенное сердце
                likeCountSpan.textContent = parseInt(likeCountSpan.textContent) + 1;
            } else {
                likeBtn.setAttribute('data-liked', 'false');
                likeBtn.innerHTML = '<i class="far fa-heart"></i>'; // Обведённое сердце
                likeCountSpan.textContent = parseInt(likeCountSpan.textContent) - 1; // Уменьшаем счётчик
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
    }

    function followingClick(event, username) {
        event.stopPropagation(); // Останавливает всплытие события
        const followBtn = document.getElementById(`flwBtn`);
        const follow = followBtn.getAttribute('follow') === 'true';
        console.log("follow = ", follow)
        fetch(`/follow/${username}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken'), // Получаем CSRF-токен
            },
            body: JSON.stringify({'follow': follow})
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            if(data.follow == 1){
                followBtn.setAttribute('follow', 'true');
                followBtn.style.background='#421954';
                followBtn.textContent = "Отписаться"
                console.log("Follow")
            }
            else{
                followBtn.setAttribute('follow', 'false')
                followBtn.style.background='#704c9e';
                followBtn.textContent = "Подписаться"
                console.log("Unfollow")
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
    }

    function ModallikeClick(event, tweetId) {
        const likeBtn = document.getElementById(`modal-likeBtn`);
        const likeCountSpan = document.getElementById(`modal-likes-count`);
        const isLiked = likeBtn.getAttribute('data-liked') === 'true';
        // AJAX-запрос для обновления лайка в базе данных
        fetch(`/like/${tweetId}/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken'), // Получаем CSRF-токен
            },
            body: JSON.stringify({ liked: !isLiked }) // Отправляем статус лайка
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            if (data.liked) {
                likeBtn.setAttribute('data-liked', 'true');
                likeBtn.innerHTML = '<i class="fas fa-heart" style="color: #704c9e;"></i>'; // Закрашенное сердце
                likeCountSpan.textContent = parseInt(likeCountSpan.textContent) + 1;
            } else {
                likeBtn.setAttribute('data-liked', 'false');
                likeBtn.innerHTML = '<i class="far fa-heart"></i>'; // Обведённое сердце
                likeCountSpan.textContent = parseInt(likeCountSpan.textContent) - 1; // Уменьшаем счётчик
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
        likeClick(event,tweetId)
    }

    function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

    // Получаем все кнопки с классом 'edit-delete-btn'
    const buttons = document.querySelectorAll('.edit-delete-btn');

    buttons.forEach((button, index) => {
        const popupMenu = button.nextElementSibling; // Получаем соседний элемент (всплывающее меню)

        // Обработка наведения на кнопку
        button.addEventListener('mouseenter', function() {
            popupMenu.style.display = 'block'; // Показываем всплывающее окно
        });

        // Обработка наведения на всплывающее окно
        popupMenu.addEventListener('mouseenter', function() {
            popupMenu.style.display = 'block'; // Оставляем всплывающее окно открытым
        });

        // Обработка ухода мыши с кнопки
        button.addEventListener('mouseleave', function() {
            if (!popupMenu.matches(':hover')) { // Проверяем, что курсор не на всплывающем окне
                popupMenu.style.display = 'none'; // Скрываем всплывающее окно
            }
        });

        // Обработка ухода мыши со всплывающего окна
        popupMenu.addEventListener('mouseleave', function() {
            popupMenu.style.display = 'none'; // Скрываем всплывающее окно
        });
    });


    // Пример функции редактирования поста
    function editPost(id) {
        var edit_area = document.getElementById(`content-${id}`);
        var content = edit_area.innerText;;
         // Создаем элемент textarea
        const textArea = document.createElement('textarea');

        // Устанавливаем атрибуты
        textArea.setAttribute('rows', '2');
        textArea.setAttribute('class', 'edit-area');
        textArea.setAttribute('id', `edit-${id}`);
        textArea.setAttribute('required', '');
        textArea.setAttribute('onclick', 'childClick(event);');
        textArea.value = content
        // Добавляем событие oninput для автоизменения размера
        textArea.setAttribute('oninput', 'autoResize(this)');
        textArea.addEventListener('keydown', function(event) {
                if (event.key === 'Enter' && !event.shiftKey) { // Check if Enter is pressed without Shift
                    event.preventDefault(); // Prevents adding a new line
                    // Создаем новый элемент для замены textarea
                    const textDisplay = document.createElement('div'); // Можно использовать 'span' или 'div'
                    textDisplay.setAttribute('id', `content-${id}`);
                    textDisplay.setAttribute('class', 'post-content'); // Класс для стилей текста
                    textDisplay.textContent = this.value; // Текст для отображения
                    this.replaceWith(textDisplay);
                    // Дальше нужно изменить пост в бд
                    fetch(`/tweet/${id}/`, {
                        method: 'PUT',
                        headers: {
                            'Content-Type': 'application/json',
                            'X-CSRFToken': getCookie('csrftoken'), // Получаем CSRF-токен
                        },
                        body: JSON.stringify({data: this.value}) // Отправляем статус лайка
                    })
                }
        });
        edit_area.replaceWith(textArea);

    }

    // Пример функции удаления поста
    function deletePost(id) {
        fetch(`/tweet/${id}/`, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken'), // Получаем CSRF-токен
            },
            body: JSON.stringify({}) // Отправляем статус лайка
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            if (data.Success == 1) {
                let element = document.getElementById(`post-${id}`);
                if (element) {
                    element.remove();
                }
            } else {
                throw new Error('error delete');
            }
        })
    }

    // Функция для открытия модального окна
    function openFollowingsModal() {
        document.body.classList.add('modal-open');
        document.getElementById("followingsModal").style.display = "block";
    }

    // Функция для закрытия модального окна
    function closeFollowingsModal() {
        document.body.classList.remove('modal-open');
        document.getElementById("followingsModal").style.display = "none";
    }


     // Функция для открытия модального окна
    function openFollowersModal() {
        document.body.classList.add('modal-open');
        document.getElementById("followersModal").style.display = "block";
    }

    // Функция для закрытия модального окна
    function closeFollowersModal() {
        document.body.classList.remove('modal-open');
        document.getElementById("followersModal").style.display = "none";
    }