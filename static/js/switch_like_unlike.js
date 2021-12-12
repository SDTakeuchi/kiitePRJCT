$(function() {
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    const csrftoken = getCookie('csrftoken');

    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

    $(document).on('click', '#show_spinner', function () {
        reverseLikeStatus($(this), flipBtnColor);
    });
    const reverseLikeStatus = (likeBtn, callback) => {
        likeBtn.preventDefault();
        const ajaxUrl = likeBtn.attr('href');
        $.ajax({
            url: ajaxUrl,
            method: 'GET',
            timeout: 10000,
            dataType: 'json',
        });
        callback(likeBtn);
    }
    const flipBtnColor = (likeBtn) => {
        const buttonTag = likeBtn.find('button');
        if (buttonTag.attr('class') === 'btn btn-primary') {
            likeBtn.append(defaultLikeBtn).append(defaultSvg).append(defaultPath.after(inBtnText));
        } else {
            likeBtn.append(enabledLikeBtn).append(enabledSvg).append(enabledPath.after(inBtnText));
        }
        buttonTag.remove();
    }

    const defaultLikeBtn = $("<button>", {
        className: 'btn btn-default',
    });

    const defaultSvg = $("<svg>", {
        xmls: "http://www.w3.org/2000/svg",
        width: 16,
        height: 16,
        fill: "#337ab7",
        className: "bi bi-hand-thumbs-up-fill",
        viewBox: "0 0 16 16"
    });

    const defaultPath = $("<path>", {
        d: "M6.956 1.745C7.021.81 7.908.087 8.864.325l.261.066c.463.116.874.456 1.012.965.22.816.533 2.511.062 4.51a9.84 9.84 0 0 1 .443-.051c.713-.065 1.669-.072 2.516.21.518.173.994.681 1.2 1.273.184.532.16 1.162-.234 1.733.058.119.103.242.138.363.077.27.113.567.113.856 0 .289-.036.586-.113.856-.039.135-.09.273-.16.404.169.387.107.819-.003 1.148a3.163 3.163 0 0 1-.488.901c.054.152.076.312.076.465 0 .305-.089.625-.253.912C13.1 15.522 12.437 16 11.5 16H8c-.605 0-1.07-.081-1.466-.218a4.82 4.82 0 0 1-.97-.484l-.048-.03c-.504-.307-.999-.609-2.068-.722C2.682 14.464 2 13.846 2 13V9c0-.85.685-1.432 1.357-1.615.849-.232 1.574-.787 2.132-1.41.56-.627.914-1.28 1.039-1.639.199-.575.356-1.539.428-2.59z"
    });

    const enabledLikeBtn = $("<button>", {
        className: 'btn btn-primary',
    });

    const enabledSvg = $("<svg>", {
        xmls: "http://www.w3.org/2000/svg",
        width: 16,
        height: 16,
        fill: "currentColor",
        className: "bi bi-hand-thumbs-up-fill",
        viewBox: "0 0 16 16"
    });

    const enabledPath = $("<path>", {
        d: "M6.956 1.745C7.021.81 7.908.087 8.864.325l.261.066c.463.116.874.456 1.012.965.22.816.533 2.511.062 4.51a9.84 9.84 0 0 1 .443-.051c.713-.065 1.669-.072 2.516.21.518.173.994.681 1.2 1.273.184.532.16 1.162-.234 1.733.058.119.103.242.138.363.077.27.113.567.113.856 0 .289-.036.586-.113.856-.039.135-.09.273-.16.404.169.387.107.819-.003 1.148a3.163 3.163 0 0 1-.488.901c.054.152.076.312.076.465 0 .305-.089.625-.253.912C13.1 15.522 12.437 16 11.5 16H8c-.605 0-1.07-.081-1.466-.218a4.82 4.82 0 0 1-.97-.484l-.048-.03c-.504-.307-.999-.609-2.068-.722C2.682 14.464 2 13.846 2 13V9c0-.85.685-1.432 1.357-1.615.849-.232 1.574-.787 2.132-1.41.56-.627.914-1.28 1.039-1.639.199-.575.356-1.539.428-2.59z"
    });

    const inBtnText = $('<div>', {
        display: 'inline',
        text: ' いいね !',
    });

});