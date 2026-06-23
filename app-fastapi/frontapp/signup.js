const apiUrl = "http://localhost:8001/user/signup"

function displayMessage(message){
    alert(message);
}

function resetForm(){
    document.getElementById('name').value = '';
    document.getElementById('password').value = '';
    document.getElementById('password_confirm').value = '';
}

document.getElementById('createUserForm').addEventListener('submit', async (e) => {
    e.preventDefault();

    const username = document.getElementById('name').value;
    const password = document.getElementById('password').value;
    const passwordConfirm = document.getElementById('password_confirm').value;

    if (password != passwordConfirm){
        displayMessage('パスワードと確認用パスワードが一致しません');
        return;
    }
     const userData = {
        user_name: username,
        password: password,
        password_confirm: passwordConfirm
     }
     await createUser(userData);
})

async function createUser(user){
    try{
        const response = await fetch(apiUrl, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(user)
        });
        const data = await response.json();
        if (response.ok){
            displayMessage(data.message);
            resetForm();
        }else{
            if (response.status === 422){
                displayMessage('入力内容に誤りがあります。');
            }else{
                displayMessage(data.detail);
            }
        }
    }catch(error){
        console.error('サインアップ中にエラーが発生しました。', error);
    }
}

