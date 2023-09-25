function closeDiv(el) {
    el.parentElement.style.display = 'none';
}

try {
    flashMsgCloseBtnDivs = document.querySelectorAll('.alert');
    flashMsgCloseBtnDivs.forEach(div => {
        button = div.querySelector('.btn-close');
        button.addEventListener('click', () => {closeDiv(button)});
    });
} catch (error) {
    console.error(error)
}