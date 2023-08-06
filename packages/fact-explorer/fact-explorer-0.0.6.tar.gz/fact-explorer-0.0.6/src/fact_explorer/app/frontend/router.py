from datetime import datetime
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pathlib import Path

from fact_explorer.app.business import search as fact_search
from json import loads, dumps

router = APIRouter(
    prefix="/fe",
    responses={404: {"description": "Not Found!"}},
    include_in_schema=False,
)

templates = Jinja2Templates(
    directory=str(Path(__file__).resolve().parent.joinpath("templates"))
)


@router.get("/", response_class=HTMLResponse)
async def home(request: Request):
    context = {"title": "Home", "request": request}
    response = templates.TemplateResponse(
        "home.jinja2",
        context=context,
    )
    return response


@router.get("/search", response_class=HTMLResponse)
async def search(request: Request):
    context = {"title": "Search", "request": request}
    response = templates.TemplateResponse(
        "search.jinja2",
        context=context,
    )
    return response


@router.get("/last", response_class=HTMLResponse)
async def get_last_result(request: Request, minutes: int = 15, decrypt: bool = False):
    res = await fact_search.time_interval(
        db=request.app.state.db,
        key_backend=request.app.state.key_backend,
        minutes=minutes,
        decrypt=decrypt,
    )

    parsed = await _advanced_parsing(res)

    data = dumps(parsed, indent=2, sort_keys=True)
    context = {"title": "Last X Minutes", "request": request, "data": data}
    response = templates.TemplateResponse(
        "fragments/server_rendered_code_display.jinja2",
        context=context,
    )
    return response


@router.get("/search/result", response_class=HTMLResponse)
async def search_result(
    request: Request,
    skip: int = 0,
    limit: int = 20,
    hq: str = "{}",
    pq: str = "{}",
    decrypt: bool = False,
):
    res = await fact_search.strict(
        db=request.app.state.db,
        key_backend=request.app.state.key_backend,
        skip=skip,
        limit=limit,
        hq=loads(hq),
        pq=loads(pq),
        decrypt=decrypt,
    )

    if not res:
        return HTMLResponse(content="Noting found")  # TODO: Return proper 404 here

    parsed = await _advanced_parsing(res)

    data = dumps(parsed, indent=2, sort_keys=True)
    context = {"title": "Search", "request": request, "data": data}
    response = templates.TemplateResponse(
        "fragments/server_rendered_code_display.jinja2",
        context=context,
    )
    return response


async def _advanced_parsing(res):
    parsed = []
    for item in res:
        repres = {"header": loads(item["header"]), "payload": loads(item["payload"])}
        try:
            repres["header"]["meta"]["_ts"] = datetime.fromtimestamp(
                repres["header"]["meta"]["_ts"] / 1000.0
            ).strftime(
                "%Y-%m-%dT%H:%M:%S"
            )  # TODO figure out timezone
        except Exception:  # noqa: E722 - date parsing inability should not stop us
            pass

        parsed.append(repres)
    return parsed
