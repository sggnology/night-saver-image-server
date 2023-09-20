from fastapi import FastAPI, UploadFile
from starlette.responses import HTMLResponse, JSONResponse
import text_extract_car_plate as tecp

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


@app.get("/test")
async def file_test():
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Document</title>
        </head>
        <body>
            <input id="imageFile" type="file" accept="image/*">
            <button id="sendBtn" onclick="">파일 전송</button>
        </body>
        <script>
            let file;
        
            const $imageFile = document.querySelector("#imageFile");
            const $sendBtn = document.querySelector("#sendBtn");
        
            $imageFile.addEventListener("change", (e) => {
                file = e.target.files[0];
                console.log(file);
            });
        
            $sendBtn.addEventListener("click", () => {
        
                let fd = new FormData();
                fd.append("image", file);
        
                fetch("/image/car-number", {
                    method: "POST",
                    body: fd
                }).then((res) => {
                    return res.json();
                }).then((res) => {
                    console.log(res);
                }).catch(()=> {
                    alert("실패");
                })
            });
        
        </script>
    </html>
    """
    return HTMLResponse(content=html_content)


@app.post("/image/car-number")
async def extract_car_number_from_image(image: UploadFile):
    extracted_car_plates = await tecp.extract_car_plates_from_image(image)

    result = {
        "carPlateCandidates": extracted_car_plates
    }

    return JSONResponse(
        content=result,
        status_code=200
    )
