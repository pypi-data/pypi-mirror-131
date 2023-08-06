"""Generic HTTP and URL utilities."""

from typing import Optional
from urllib.parse import parse_qsl, urlencode, urljoin, urlparse, urlunparse

import validators
from starlette.datastructures import QueryParams

from fast_redirect.exceptions import HTTPHostHeaderDomainInvalid


def parse_host_header(value: str) -> str:
    """Parse HTTP host header."""
    domain = value.split(":")[0]

    if not validators.domain(domain):
        raise HTTPHostHeaderDomainInvalid

    return domain


def build_url(
    *,
    destination_url: str,
    path: Optional[str] = None,
    query_parameters: Optional[QueryParams] = None,
) -> str:
    """Build URL."""

    # Construct URL by joining path

    url = urljoin(destination_url, path)

    # If query parameters are not set, we're done

    if not query_parameters:
        return url

    # If we get here, query parameters are set. Return URL with merged query
    # parameters

    return merge_query_parameters(url, query_parameters)


def merge_query_parameters(url: str, query_parameters: QueryParams) -> str:
    """Merge query parameters with URL that may already contain query parameters."""

    # Parse current URL

    parsed_url = urlparse(url)

    # Convert query parameters in current URL from string to dict, so that we can
    # append our query parameters dict to it.
    #
    # Uses 'dict(parse_qsl(...))', instead of 'parse_qs' which returns a dict. We do
    # this because our .update() will add a string as the value, while the value of
    # the dict that 'parse_qs' would return is a list. By casting the tuples from
    # 'parse_qsl' to a dict, the dict is the same as QueryParams (no list of value).

    new_query_parameters = dict(parse_qsl(parsed_url.query))

    # Add query parameters to current query parameters

    new_query_parameters.update(query_parameters)

    # Convert query parameters dict, which now contains our new query parameters,
    # back to string

    url_new_query = urlencode(new_query_parameters)

    # Replace the old query parameters with our new query parameters in the URL

    parsed_url = parsed_url._replace(query=url_new_query)

    # Convert the parsed URL back into an actual URL, which now contains our new
    # query parameters

    unparsed_url = urlunparse(parsed_url)

    return unparsed_url
