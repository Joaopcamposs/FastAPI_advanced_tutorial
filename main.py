from enum import Enum

from fastapi import FastAPI


class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"


app = FastAPI()

fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]


# Quando você declara outros parâmetros na função que não fazem parte dos parâmetros da rota, esses parâmetros são
# automaticamente interpretados como parâmetros de "consulta".
@app.get("/items/")
async def read_item(skip: int = 0, limit: int = 10):
    return fake_items_db[skip : skip + limit]


# FastAPI é esperto o suficiente para perceber que o parâmetro da rota item_id é um parâmetro da rota, e q não é,
# portanto, q é o parâmetro de consulta.
@app.get("/items/{item_id}")
async def read_item(item_id: str, q: str | None = None, short: bool = False):
    item = {"item_id": item_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update(
            {"description": "This is an amazing item that has a long description"}
        )
    return item


# Você pode declarar múltiplos parâmetros de rota e parâmetros de consulta ao mesmo tempo, o FastAPI vai saber o quê
# é o quê. E você não precisa declarar eles em nenhuma ordem específica. Eles serão detectados pelo nome.
@app.get("/users/{user_id}/items/{item_id}")
async def read_user_item(
    user_id: int, item_id: str, q: str | None = None, short: bool = False
):
    item = {"item_id": item_id, "owner_id": user_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update(
            {"description": "This is an amazing item that has a long description"}
        )
    return item


# Quando você quiser fazer com que o parâmetro de consulta seja obrigatório, você pode simplesmente não declarar
# nenhum valor como padrão.
@app.get("/item/{item_id}")
async def read_user_item(
    item_id: str, needy: str, skip: int = 0, limit: int | None = None
):
    item = {"item_id": item_id, "needy": needy, "skip": skip, "limit": limit}
    return item


# As operações de rota são avaliadas em ordem, você precisa ter certeza que a rota para /users/me está sendo declarado
# antes da rota /users/{user_id}
@app.get("/users/me")
async def read_user_me():
    return {"user_id": "the current user"}


@app.get("/users/{user_id}")
async def read_user(user_id: str):
    return {"user_id": user_id}


@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    if model_name is ModelName.alexnet:
        return {"model_name": model_name, "message": "Deep Learning FTW!"}

    if model_name.value == "lenet":
        return {"model_name": model_name, "message": "LeCNN all the images"}

    return {"model_name": model_name, "message": "Have some residuals"}


@app.get("/files/{file_path:path}")
async def read_file(file_path: str):
    return {"file_path": file_path}
