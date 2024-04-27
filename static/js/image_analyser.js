document.getElementById('fileInput').addEventListener('change', function(event) {
    const file = event.target.files[0];
    if (file) {
        showModal('loadingModal');
        displayImage(event);
        analyseImage(file);
    }
});

async function analyseImage(file) {
    const formData = new FormData();
    formData.append("file", file);
    const requestOptions = {
        method: "POST",
        body: formData
    };
    await fetch("/image/analyse?output_format=HTML", requestOptions)
        .then((response) => {
            if (!response.ok) {
                return response.text().then(errorText => displayError(errorText));
            } else {
                return response.text().then((result) => displayMetadata(result))
            }
        })
        .catch((error) => console.error(error));

    closeModal('loadingModal');
}

function displayMetadata(results) {
    let container = document.getElementById('results-container');
    container.innerHTML = results;
}

function displayError(error) {

    closeModal('loadingModal');

    const errorObj = JSON.parse(error)
    let code = document.getElementById('code');
    let message = document.getElementById('message');
    let instruction = document.getElementById('instruction');
    code.innerHTML = errorObj['code'];
    message.innerHTML = errorObj['message'];
    instruction.innerHTML = errorObj['instruction'];

    showModal('errorModal');
}

function displayImage(event) {
    let reader = new FileReader();
    reader.onload = function(){
        let imgContent = document.getElementById('image-content');
        let imgElement = document.createElement('img');
        imgElement.src = reader.result;
        imgElement.className = 'modal-content';
        imgElement.style.maxWidth = "500px";
        imgContent.innerHTML = '';
        imgContent.appendChild(imgElement);
    }
    try {
        reader.readAsDataURL(event.target.files[0]);
    } catch {
        reader.readAsDataURL(event);
    }
}


function closeModal(modalId) {
    let modal = document.getElementById(modalId);
    modal.style.opacity = '0';
    setTimeout(() => {
        modal.style.display = 'none';
    }, 100);
}

function showModal(modalId) {
    let modal = document.getElementById(modalId);
    modal.style.display = 'block';
    setTimeout(() => {
        modal.style.opacity = '1';
    }, 100);
}
