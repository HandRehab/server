
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from fastapi.responses import HTMLResponse
from fastapi import FastAPI, Request
from routes import register,auth,box,balloon,snake,ball,punch,list


app = FastAPI(title="HandRehab backend",
              description="This is the docs for the api's used in handrehab",
              version="0.9.12",
              contact={
                  "name": "Athul Saji",
                  "email": "athulsaji1317@gmail.com",
              },
              

              )

# CORS middleware to allow requests from the React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000","*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    html_content = """
    <html>
        <head>
            <title>Official backend docs of HandRehab</title>
            <script>location.replace("/docs");</script>
        </head>
    </html>
    """

    return HTMLResponse(content=html_content, status_code=200)

app.include_router(register.app)
app.include_router(auth.app)
app.include_router(box.app)
app.include_router(balloon.app)
app.include_router(snake.app)
app.include_router(ball.app)
app.include_router(punch.app)
app.include_router(list.app)

@app.exception_handler(StarletteHTTPException)
async def custom_http_exception_handler(request, exc):
    return RedirectResponse("/notFound")


@app.get("/notFound")
@app.post("/notFound")
@app.post("/notFound")
@app.patch("/notFound")
@app.delete("/notFound")
def notFound():
    return {
    "success": 'false',
    "message": 'Page not found',
    "error": {
      "statusCode": 404,
      "message": 'You reached a route that is not defined on this server',
    },
  }