const apiUrl = "http://localhost:8001/favorite"

function displayMessage(message){
    alert(message)
}

async function searchArticles(keyword) {
    try {
        const response = await fetch(`${apiUrl}/search?key_word=${keyword}`);
        const articles = await response.json();
        
        const articlesList = document.getElementById('articlesList');
        articlesList.innerHTML = '<h3>検索結果（最新記事5件）</h3>'; 

        articles.forEach(article => {
            const div = document.createElement('div');
            div.style.margin = "10px 0";
            div.className = 'card mb-2 p-2 shadow-sm bg-white';
            div.innerHTML = `
                <div class="d-flex justify-content-between align-items-center">
                    <div style="font-size: 13px;">
                        <strong>${article.title}</strong> - 
                        <a href="${article.url}" target="_blank" class="text-decoration-none">記事を読む 🔗</a>
                    </div>
                    <button class="add-btn btn btn-outline-primary btn-sm" style="font-size: 11px;">⭐ お気に入り</button>
                </div>
            `;
            div.querySelector('.add-btn').addEventListener('click', async () => {
                const favoriteData = {
                    title: article.title,
                    url: article.url,
                    regist_date: new Date().toISOString().split('T')[0],
                    category: "技術"
                };
                await addFavorite(favoriteData);
            });

            articlesList.appendChild(div);
        });
    } catch(error) {
        console.error('記事検索中にエラーが発生しました:', error);
    }
}

async function addFavorite(favorite){
    try{
        const response = await fetch(apiUrl, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(favorite)
        });
        const data = await response.json();
        if(response.ok){
            displayMessage(data.message);
            await fetchAndDisplayFavorites();
        }
    }catch(error){
        console.error('お気に入り追加中にエラーが発生しました:', error);
    }
}

async function deleteFavorite(favoriteId) {
    try{
        const response = await fetch(`${apiUrl}/${favoriteId}`, {
            method: 'DELETE'
        });
        const data = await response.json();
        if(response.ok){
            displayMessage(data.message);
            await fetchAndDisplayFavorites();
        }else{
            displayMessage(data.detail);
        }
    }catch(error){
        console.error('お気に入り削除中にエラーが発生しました:', error);
    }
}

async function fetchAndDisplayFavorites() {
    try{
        const response = await fetch(apiUrl);
        if (!response.ok){
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const favorites = await response.json();
        const favoritesList = document.getElementById('favoritesList');
        favoritesList.innerHTML = '';
        favorites.forEach(favorite => {
        const card = document.createElement('div');
        card.className = 'card mb-2 shadow-sm';            
        card.innerHTML = `
            <div class="card-header fw-bold text-dark bg-light" style="font-size: 14px; padding: 8px 12px;">
                ${favorite.title}
            </div>
            <div class="card-body d-flex justify-content-between align-items-center" style="padding: 10px 12px;">
                <div style="font-size: 13px;">
                    <span class="text-muted">カテゴリー : ${favorite.category}</span>
                    <span class="mx-1">-</span>
                    <a href="${favorite.url}" target="_blank" class="text-decoration-none">URL 🔗</a>
                </div>
                <button class="delete btn btn-sm btn-outline-danger" style="font-size: 11px; padding: 2px 8px;" data-id="${favorite.id}">削除</button>
            </div>
        `;
        favoritesList.appendChild(card);
        });
    }catch(error){
        console.error('お気に入り一覧取得中にエラーが発生しました:', error);
    }
}

document.addEventListener('DOMContentLoaded', ()=> {
    const currentUser = localStorage.getItem('currentUser');
    if (!currentUser) {
        alert('ログインが必要です。');
        window.location.href = 'login.html';
        return; // 未ログインならここで処理をストップ
    } else {
        const userSpan = document.getElementById('loginUser');
        if (userSpan) {
            userSpan.textContent = currentUser;
        }
    }
    const searchForm = document.getElementById('searchForm');
    if (searchForm) {
        searchForm.onsubmit = async (event) => {
            event.preventDefault(); 
            const keyword = document.getElementById('keyword').value;
            await searchArticles(keyword);
        };
    }

    const favoritesList = document.getElementById('favoritesList');
    if (favoritesList) {
        favoritesList.addEventListener('click', async (event) => {
            if (event.target.classList.contains('delete')) {
                const favoriteId = event.target.dataset.id;
                await deleteFavorite(favoriteId);
            }
        });
    }
});