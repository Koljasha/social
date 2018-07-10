import Vue from 'vue';
import axios from 'axios/dist/axios.min';

import 'bootstrap/dist/css/bootstrap.min.css';
import './style.css';

import './widgets.jss';
import './twitter.png';
import './vk.png';
import './favicon.png';
import './og.jpg';

// функция подключения к api
let axiget = url => {
    // основной запрос
    axios.get(url)
        .then(response => {
            if (response.data["error"] !== undefined) {
                alert(response.data["error"])
            } else {
                // встроенные Твиты
                for (let i of response.data) {
                    if (i.embedded == " ") {
                        axios.get('/api/embedded/', {
                                params: {
                                    link: i.link,
                                }
                            })
                            .then(response => {
                                i.embedded = response.data.html;
                                // для внутреннего loader
                                app.idTw = i.id
                            })
                            .catch(error => console.log(error))
                    }
                }
                app.items = app.items.concat(response.data);
            }
        })
        .catch(error => console.log(error))
}

// Loader во время запроса
axios.interceptors.request.use(function (config) {
    app.mainloader = true;
    return config;
}, function (error) {
    return Promise.reject(error);
});
axios.interceptors.response.use(function (response) {
    app.mainloader = false;
    return response;
}, function (error) {
    return Promise.reject(error);
});


var app = new Vue({
    el: '#app',
    data: {
        items: [],
        buttonShow: false,
        menuShow: false,
        idTw: null,
        mainloader: false
    },
    created() {
        axiget('/api/');
    },
    updated() {
        let elem = document.getElementById(app.idTw)
        twttr.widgets.load(elem)
            .then(() => {
                // адаптивная ширина
                let windowWidth = window.innerWidth;
                let width = 500;
                if (576 >= windowWidth && windowWidth > 375) width = 350;
                else if (375 >= windowWidth) width = 300;
                
                if (elem !== null) {
                    elem.firstChild.style.width = width + 'px';

                    // shadowRoot или iframe
                    let node;
                    try {
                        node = elem.firstChild.shadowRoot.querySelector('.EmbeddedTweet');
                    } catch (err){
                        node = elem.firstChild.contentWindow.document.querySelector('.EmbeddedTweet');
                    }

                    // цвета
                    node.style.backgroundColor = 'rgb(35, 53, 70)';
                    node.style.color = 'white';
                    // лоадер
                    elem.nextElementSibling.hidden = true;
                    elem.hidden = false;
                }
            })
            .catch(error => console.log(error));

    },
    methods: {
        onScroll: e => {
            let listItem = e.target;
            app.buttonShow = listItem.scrollTop != 0 ? true : false;
            if (listItem.scrollTop + listItem.clientHeight >= listItem.scrollHeight) {
                axiget('/api/next/');
            }
        },
        onClick: link => window.open(link, "_blank"),
        toTop: () => app.$refs.listGroup.scrollTop = 0,
        reloadPage: () => location.reload(),
        isEmbedded: (data) => data !== null ? true : false,
        exitPage: () => location.href = '/logout/'
    }
})