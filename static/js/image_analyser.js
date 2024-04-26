let isImageSet = false;

function previewImage(event) {
    let reader = new FileReader();
    reader.onload = function(){
        let modal = document.getElementById('previewModal');
        let modalContent = document.getElementById('modal-content');
        let imgElement = document.createElement('img');
        imgElement.src = reader.result;
        imgElement.className = 'modal-content';
        imgElement.style.maxWidth = "80%";
        imgElement.style.maxHeight = "80%";
        modalContent.innerHTML = '';
        modalContent.appendChild(imgElement);
        modal.style.display = 'block';
        setTimeout(() => { // Delay to ensure the transition is applied
            modal.style.opacity = '1';
        }, 10);
         isImageSet = true; // Set flag to true
        document.getElementById('showModalBtn').disabled = false;
        document.getElementById('analyseBtn').disabled = false;
    }
    try {
        reader.readAsDataURL(event.target.files[0]);
    } catch {
        reader.readAsDataURL(event);
    }
}

document.getElementById('fileInput').addEventListener('change', function(event) {
    const file = event.target.files[0];
    if (file) {
        const fileSize = file.size; // File size in bytes
        const fileType = file.type; // File type (MIME type)
        const fileName = file.name; // File name
        const img = new Image();
        img.onload = function() {
            const resolution = this.width + 'x' + this.height; // Image resolution
            let elementFileName = document.getElementById('imgFileName')
            let elementFileSize = document.getElementById('imgFileSize')
            let elementFileType = document.getElementById('imgFileType')
            let elementResolution = document.getElementById('imgResolution')
            elementFileName.innerHTML = 'File Name: ' + fileName;
            elementFileSize.innerHTML = 'File Size: ' + fileSize + ' bytes';
            elementFileType.innerHTML = 'File Type: ' + fileType;
            elementResolution.innerHTML = 'Resolution: ' + resolution;
        };
        img.src = URL.createObjectURL(file);
    }
});

// Preview Modal Close
document.getElementsByClassName('close')[0].addEventListener('click', function() {
    let modal = document.getElementById('previewModal');
    modal.style.opacity = '0';
    setTimeout(() => { // Delay to ensure the transition is applied
        modal.style.display = 'none';
    }, 500);
});

function showModal() {
    if (isImageSet) {
        let modal = document.getElementById('previewModal');
        modal.style.display = 'block';
        setTimeout(() => { // Delay to ensure the transition is applied
            modal.style.opacity = '1';
        }, 10);
    }
}

// Preview Modal Set
document.getElementById('fileInput').addEventListener('change', previewImage);

// Showing Error Modal
$(document).ready(function(){$('#errorModal').modal('show');});
