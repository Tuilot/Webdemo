var isLoad = false;
function checkRegisterInfo() {
    if (isLoad == false) {
        isLoad = true;
        return false;
    }
    var canSubmit = true;
    canSubmit = checkEmail() && canSubmit;
    canSubmit = checkUsername() && canSubmit;
    canSubmit = checkPassword() && canSubmit;
    canSubmit = checkPasswordConfirm() && canSubmit;
    return canSubmit;
}

function checkEmail() {
    var email = document.getElementById('email');
    var hint = document.getElementById('email_hint');
    var reg = /^[0-9a-zA-Z_.-]+[@][0-9a-zA-Z_.-]+([.][a-zA-Z]+){1,2}$/;
    if (email.value === '') {
        hint.hidden = false;
        hint.innerText = "邮箱不能为空"
        return false;
    } else if (!reg.test(email.value)) {
        hint.hidden = false;
        hint.innerText = "邮箱格式错误，请确认邮箱地址是否正确"
        return false;
    } else {
        hint.hidden = true;
        return true;
    }
}

function checkUsername() {
    var username = document.getElementById('username');
    var hint = document.getElementById('username_hint');
    if (username.value === '') {
        hint.hidden = false;
        hint.innerText = "用户名不能为空";
        return false;
    } else {
        hint.hidden = true;
        return true;
    }
}

function checkPassword() {
    var password = document.getElementById('password');
    var hint = document.getElementById('password_hint');
    if (password.value === '') {
        hint.hidden = false;
        hint.innerText = "密码长度应在8-16位";
        return false;
    } else if (password.value) {

    } else {
        hint.hidden = true;
        return true;
    }
    return false;
}

function checkPasswordConfirm() {
    var password = document.getElementById('password');
    var confirm = document.getElementById('password_confirm');
    var hint = document.getElementById('confirm_hint');
    if (confirm.value === '') {
        hint.hidden = false;
        hint.innerText = "密码不能为空";
        return false;
    } else if (confirm.value !== password.value) {
        hint.hidden = false;
        hint.innerText = "密码不一致";
        return false;
    } else {
        hint.hidden = true;
        return true;
    }
    return false;
}