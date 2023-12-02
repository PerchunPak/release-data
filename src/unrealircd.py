import mwparserfromhell
import re
from common import http
from common import endoflife

URL = "https://www.unrealircd.org/docwiki/index.php?title=History_of_UnrealIRCd_releases&action=raw"

print("::group::unrealircd")
response = http.fetch_url(URL)
wikicode = mwparserfromhell.parse(response.text)

versions = {}
for tr in wikicode.ifilter_tags(matches=lambda node: node.tag == "tr"):
    items = tr.contents.filter_tags(matches=lambda node: node.tag == "td")
    if len(items) >= 2:
        maybe_version = items[0].__strip__()
        if re.match(endoflife.DEFAULT_VERSION_REGEX, maybe_version):
            maybe_date = items[1].__strip__()
            if re.match(r"\d{4}-\d{2}-\d{2}", maybe_date):
                versions[maybe_version] = maybe_date
                print(f"{maybe_version}: {maybe_date}")

endoflife.write_releases('unrealircd', versions)
print("::endgroup::")
