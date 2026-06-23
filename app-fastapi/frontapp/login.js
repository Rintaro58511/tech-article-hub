const apiUrl = "http://localhost:8001/user/login"

function displayMessage(message){
    alert(message);
}

function resetForm(){
    document.getElementById('name').value = '';
    document.getElementById('password').value = '';
}

document.getElementById('loginUserForm').addEventListener('submit', async (e) => {
    e.preventDefault();

    const username = document.getElementById('name').value;
    const password = document.getElementById('password').value;

    const userData = {
        user_name: username,
        password: password,
    }
    const isSuccess = await loginUser(userData);

    if (isSuccess){
        localStorage.setItem('currentUser', username); 
        window.location.href = 'favorite.html';
    }
})

async function loginUser(user){
    try{
        const response = await fetch(apiUrl, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(user)
        });
        const data = await response.json();
        if (response.ok){
            displayMessage(data.message || 'ログインに成功しました！');
            resetForm();
            return true;
        }else{
            if (response.status === 422){
                displayMessage('入力内容に誤りがあります。');
            }else{
                displayMessage(data.detail);
            }
        }
    }catch(error){
        console.error('ログイン中にエラーが発生しました。', error);
        return false;
    }
}

