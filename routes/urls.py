from starlette.routing import Mount

from item.urls import routes as item_routes
from account.urls import routes as account_routes
from auth_privileged.urls import routes as privileged_routes
from comment.urls import routes as comment_routes
# ..
from sitemap.urls import routes as sitemap_routes


routes = [
    # ..
    Mount("/item", routes=item_routes),
    Mount("/account", routes=account_routes),
    Mount("/privileged", routes=privileged_routes),
    Mount("/comment", routes=comment_routes),
    # ..
    Mount("/sitemap", routes=sitemap_routes),

]
