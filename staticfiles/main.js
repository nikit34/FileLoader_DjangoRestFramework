const uploadForm = document.getElementById('upload-form')
const input = document.getElementById('id_upload')

const alertBox = document.getElementById('alert-box')
const imageBox = document.getElementById('image-box')
const progressBox = document.getElementById('progress-box')
const cancelBox = document.getElementById('cancel-box')
const cancelBtn = document.getElementById('cancel-btn')

const csrf = document.getElementsByName('csrfmiddlewaretoken')

input.addEventListener('change', ()=>{
    progressBox.classList.remove('not-visible')
    cancelBox.classList.remove('not-visible')

    const img_data = input.files[0]
    const fd = new FormData()
    fd.append('csrfmiddlewaretoken', csrf[0].value)
    fd.append('image', img_data)

    $.ajax({
        type:'POST',
        url: uploadForm.action,
        enctype: 'multipart/form-data',
        data: fd,
        beforeSend: function(){

        },
        xhr: function(){
            const xhr = new window.XMLHttpRequest();
            xhr.upload.addEventListener('progress', e => {
                if(e.lengthComputable){
                    const percent = e.loaded / e.total * 100
                }
            })
            return xhr;
        },
        success: function(response){
            console.log(1, response);
        },
        error: function(error){
            console.log(2, error);
        },
        cache: false,
        contentType: false,
        processData:false,
    })
})