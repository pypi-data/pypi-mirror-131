"""
pages API endpoint
"""
from django.conf import settings
from django.http import JsonResponse, Http404
from django.shortcuts import get_object_or_404

from ...cms.models import Region, Page
from ..decorators import json_response


def transform_page(page_translation):
    """
    Function to create a dict from a single page_translation Object.

    :param page_translation: single page translation object
    :type page_translation: ~integreat_cms.cms.models.pages.page_translation.PageTranslation

    :return: data necessary for API
    :rtype: dict
    """
    if page_translation.page.icon:
        thumbnail = settings.BASE_URL + page_translation.page.icon.url
    else:
        thumbnail = None
    if page_translation.page.parent:
        parent = {
            "id": page_translation.page.parent.id,
            "url": page_translation.page.parent.get_translation(
                page_translation.language.slug
            ).backend_base_link,
            "path": "/"
            + page_translation.page.parent.get_translation(
                page_translation.language.slug
            ).permalink
            + "/",
        }
    else:
        parent = {
            "id": 0,
            "url": None,
            "path": None,
        }
    return {
        "id": page_translation.id,
        "url": page_translation.backend_base_link,
        "path": "/" + page_translation.permalink + "/",
        "title": page_translation.title,
        "modified_gmt": page_translation.combined_last_updated,
        "excerpt": page_translation.text,
        "content": page_translation.combined_text,
        "parent": parent,
        "order": page_translation.page.lft,  # use left edge indicator of mptt model for order
        "available_languages": page_translation.available_languages,
        "thumbnail": thumbnail,
        "hash": None,
    }


@json_response
# pylint: disable=unused-argument
def pages(request, region_slug, language_slug):
    """
    Function to iterate through all non-archived pages of a region and return them as JSON.

    :param request: Django request
    :type request: ~django.http.HttpRequest
    :param region_slug: slug of a region
    :type region_slug: str
    :param language_slug: language slug
    :type language_slug: str

    :return: JSON object according to APIv3 pages endpoint definition
    :rtype: ~django.http.JsonResponse
    """
    region = Region.get_current_region(request)
    result = []
    for page in region.get_pages():
        page_translation = page.get_public_translation(language_slug)
        if page_translation:
            result.append(transform_page(page_translation))
    return JsonResponse(
        result, safe=False
    )  # Turn off Safe-Mode to allow serializing arrays


def get_single_page(request, language_slug):
    """
    Helper function returning the desired page or a 404 if the
    requested page does not exist.

    :param request: The request that has been sent to the Django server
    :type request: ~django.http.HttpRequest

    :param language_slug: Code to identify the desired language
    :type language_slug: str

    :raises ~django.http.Http404: HTTP status 404 if the request is malformed or no page with the given id or url exists.

    :raises RuntimeError: If neither the id nor the url parameter is given

    :return: the requested page
    :rtype: ~integreat_cms.cms.models.pages.page.Page
    """
    region = Region.get_current_region(request)

    if request.GET.get("id"):
        page = get_object_or_404(region.pages, id=request.GET.get("id"))

    elif request.GET.get("url"):
        # Strip leading and trailing slashes to avoid ambiguous urls
        url = request.GET.get("url").strip("/")
        # The last path component of the url is the page translation slug
        page_translation_slug = url.split("/")[-1]
        # Get page by filtering for translation slug and translation language slug
        page = get_object_or_404(
            region.pages,
            translations__slug=page_translation_slug,
            translations__language__slug=language_slug,
        )

    else:
        raise RuntimeError("Either the id or the url parameter is required.")

    return page


@json_response
# pylint: disable=unused-argument
def single_page(request, region_slug, language_slug):
    """
    View function returning the desired page as a JSON or a 404 if the
    requested page does not exist.

    :param request: The request that has been sent to the Django server
    :type request: ~django.http.HttpRequest

    :param region_slug: Slug defining the region
    :type region_slug: str

    :param language_slug: Code to identify the desired language
    :type language_slug: str

    :raises ~django.http.Http404: HTTP status 404 if the request is malformed or no page with the given id or url exists.

    :return: JSON with the requested page and a HTTP status 200.
    :rtype: ~django.http.JsonResponse
    """
    try:
        page = get_single_page(request, language_slug)
    except RuntimeError as e:
        return JsonResponse({"error": str(e)}, status=400)
    # Get most recent public revision of the page
    page_translation = page.get_public_translation(language_slug)
    if page_translation:
        return JsonResponse(transform_page(page_translation), safe=False)

    raise Http404("No Page matches the given url or id.")


@json_response
# pylint: disable=unused-argument
def children(request, region_slug, language_slug):
    """
    Retrieves all children for a single page

    :param request: The request that has been sent to the Django server
    :type request: ~django.http.HttpRequest

    :param region_slug: Slug defining the region
    :type region_slug: str

    :param language_slug: Code to identify the desired language
    :type language_slug: str

    :raises ~django.http.Http404: HTTP status 404 if the request is malformed or no page with the given id or url exists.

    :return: JSON with the requested page descendants
    :rtype: ~django.http.JsonResponse
    """
    depth = int(request.GET.get("depth", 1))
    try:
        # try to get a single ancestor page based on the requests query string
        root_pages = [get_single_page(request, language_slug)]
    except RuntimeError:
        # if neither id nor url is set then get all root pages
        root_pages = Page.get_root_pages(region_slug)
        # simulate a virtual root node for WP compatibility
        # so that depth = 1 returns only those pages without parents (immediate children of this virtual root page)
        # like in wordpress depth = 0 will return no results in this case
        depth = depth - 1
    result = []
    for root in root_pages:
        descendants = root.get_descendants_max_depth(True, depth)
        for descendant in descendants:
            public_translation = descendant.get_public_translation(language_slug)
            if public_translation:
                result.append(transform_page(public_translation))
    return JsonResponse(result, safe=False)
