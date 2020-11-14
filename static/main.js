const uploadForm = document.getElementById('upload-form')
const input = document.getElementById('id_upload')

const alertBox = document.getElementById('alert-box')
const fileBox = document.getElementById('file-box')
const infoBox = document.getElementById('info-box')
const progressBox = document.getElementById('progress-box')
const cancelBox = document.getElementById('cancel-box')
const resultBox = document.getElementById('result-box')
const cancelBtn = document.getElementById('cancel-btn')

const csrf = document.getElementsByName('csrfmiddlewaretoken')

input.addEventListener('change', ()=>{
    progressBox.classList.remove('not-visible')
    cancelBox.classList.remove('not-visible')

    const file_data = input.files[0]
    const file_type = input.files[0].type
    const file_size = input.files[0].size
    const url = URL.createObjectURL(file_data)

    const fd = new FormData()
    fd.append('csrfmiddlewaretoken', csrf[0].value)
    fd.append('upload', file_data)

    $.ajax({
        type: 'POST',
        url: uploadForm.action,
        enctype: 'multipart/form-data',
        data: fd,
        beforeSend: function(){
            alertBox.innerHTML = ""
            fileBox.innerHTML = ""
            infoBox.innerHTML = ""
            resultBox.innerHTML = ""
        },
        xhr: function(){
            const xhr = new window.XMLHttpRequest();
            xhr.upload.addEventListener('progress', e => {
                if(e.lengthComputable){
                    const percent = e.loaded / e.total * 100;
                    progressBox.innerHTML = `<div class="progress">
                    <div class="progress-bar" role="progressbar" role="progressbar" style="width: ${percent}%" aria-valuenow="${percent}" aria-valuemin="0" aria-valuemax="100"></div>
                    </div>
                    <p>${percent.toFixed(1)}%</p>`
                }
            })
            cancelBtn.addEventListener('click', () => {
                xhr.abort()
                setTimeout(() => {
                    uploadForm.reset()
                    progressBox.innerHTML = ""
                    alertBox.innerHTML = ""
                    cancelBox.classList.add('not-visible')
                }, 2000)
            })
            return xhr;
        },
        success: function(response){
            let need_type = 'warning'
            let human_type = 'Is not sheet'
            if (file_type.substring(file_type.length - 5) == 'sheet'){
                need_type = 'success'
                human_type = 'OK - sheet'
            }
            fileBox.innerHTML = `<img src="${url}" width="300px">`
            alertBox.innerHTML = `<div class="alert alert-${need_type}" role="alert">
                                    Successfully uploaded!</div>`
            infoBox.innerHTML = `<div class="text text-${need_type}">Type: ${human_type}</div>
            <div class="text text-${need_type}">Size file: ${Math.round(file_size / 8192)} KB</div>`
            cancelBox.classList.add('not-visible')
            resultBox.innerHTML = `<div class="text text-${need_type}">Answer: ${response.result.added}</div>`;
        },
        error: function(error){
            alertBox.innerHTML = `<div class="alert alert-danger" role="alert">Something wrong...</div>`
        },
        cache: false,
        contentType: false,
        processData:false,
    })
})