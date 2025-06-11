function imageOverview(){
    let files = Array.from(document.querySelectorAll('.choose-image'));

    files.forEach(element => {
        element.addEventListener('change', event=> {
            console.log('event listener triggered')
            const files = element.files[0];

            console.log(element.files)
            console.log(files.type)
            if(files && files.type.startsWith("image/"))
            {
                console.log('file uploaded');
                console.log(element.previousElementSibling)
                const reader = new FileReader();

                reader.onload = e=>{
                    element.previousElementSibling.src = e.target.result;
                }

                reader.readAsDataURL(files);
            }
        })
    })
}


imageOverview()