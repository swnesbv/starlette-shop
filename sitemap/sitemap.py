import subprocess, math
from starlette.templating import Jinja2Templates
from starlette.responses import RedirectResponse


templates = Jinja2Templates(directory="templates")


async def all_sitemap(request):
    # ..
    if request.method == "GET":
        # ..
        subprocess.Popen(["./ENV/Scripts/python", "generate_sitemap.py"])
        # ..
        return RedirectResponse(
            "/messages?msg=the request is being processed..", status_code=302
        )
