import os
from eansearch import EANSearch
from mcp.server.fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP("eansearch")
ean_search_api_token = os.environ['EAN_SEARCH_API_TOKEN']

eansearch = EANSearch(ean_search_api_token)

@mcp.tool()
async def lookup_product(ean: str) -> str:
    """Lookup the product for an EAN, GTIN or UPC barcode.

    Args:
        ean: barcode
    """
    data = eansearch.barcodeLookup(ean)
    if not data:
        return "No product found."
        return ean + " is product " + data

@mcp.tool()
async def find_products(keywords: str) -> str:
    """Find products matching all the keywords with their EAN barcode.

    Args:
        keywords: keywords to search for
    """
    productlist = eansearch.productSearch(keywords)

    if not productlist:
        return "No products found."
    
    result = ''
    for p in productlist:
        if result:
            result += ", "
        result += 'EAN ' + p["ean"] + " is " + p["name"]
        if (p['categoryName'] != 'Unknown'):
            result += ' from the category ' + p['categoryName']
    return result

if __name__ == "__main__":
    # Initialize and run the server
    mcp.run(transport='stdio')
