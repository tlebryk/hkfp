import json
import pandas

with open("test.jl", "r") as json_file:
    json_list = list(json_file)

for json_str in json_list:
    result = json.loads(json_str)
    # print(f"result: {result}")
    # print(isinstance(result, dict))

dropkeys = [
    "images",
    "thumbnails",
    "mediaStream",
    "resources",
    "content",
    "created",
    "highlightContent",
    "highlightTitle",
    "highlight",
    "type",
    "channelName",
    "channelId",
    "attIds",
    "system",  # ismp
    "author_low",
    "dubTitle",
    "dupFlag",
    "originSpecialId",
    # "columnId",
    "specialId",
    "expired",
    "originUri",
    "originUrl",
    "comment",
    "language",
    "properties",
    "jsonUrl",
    "shareUrl",
    "leadinLine",
    "canComment",
    "contentType",
    "thumbnailStyle",
    "categories",
    "dupFlag",
    "dupTitle",
    "extInfo",
    "img",
    "attIds",
    "originalId",  # empty
    "created",  # None
    "content",  # empty
]

remaining = {k: v for k, v in art.items() if k not in dropkeys}

keepkeys = [
    "id",
    "inner_id",
    "title",
    "subtitle",
    "keywords",
    "tags",  # nont for now but keeping; keywords is better
    "columnDirname",
    "source",  # hk edition, china daily etc.
    "url",
    "plainText",
    "updated",
    "summary",
    "authors",
    "columnName",
    "reviewEditor",
    "editor",
    "pubDateStr",  # 2021-12-29 22:32
    "publishTime",  # 1640823764000
    "lastModified",  # 1640823764000
    "imageCount",
    "wordCount",
    "columnName",
    "columnId",
    "storyType",  # should be COMPO but videos slip in
    # TODO: edit search query?
]
ermain = []
editorRecommends = ["editorRecommends"]

content = dct["content"]
# for art in content:
art = content[0]
er = art["editorRecommends"]
id_ = art["id"]
ermain += [dict(d, **{"anchor_id": id_}) for d in er]

key = "tags"
[d[key] for d in content]
