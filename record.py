"""
#main.py 6-18아래 문법은 이미 사용 안함. 
app = FastAPI()
prisma = Prisma()

@app.on_event("startup")
async def startup():
    await prisma.connect()
    print("Start Server")

@app.on_event("shutdown")
async def shutdown():
    await prisma.disconnect()
    print("Shutdown Server")
"""

"""
@asynccontextmanager
async def lifespan(app: FastAPI):
    await prisma.connect()
    print("Start Server")
    yield
    await prisma.disconnect()
    print("Shutdown Server")


app = FastAPI(lifespan=lifespan)


@app.get("/")
async def root():
    return {"message": "Hello World"}
"""
