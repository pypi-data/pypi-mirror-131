"""Main file for converting RedBrick format to coco format."""
import asyncio
from typing import Dict, List, Optional, Tuple

import aiohttp
from yarl import URL

from redbrick.utils.async_utils import gather_with_concurrency
from redbrick.utils import aioimgspy
from redbrick.utils.logging import print_error
from .polygon import rb2coco_polygon
from .bbox import rb2coco_bbox
from .categories import rb_get_class_id, rb2coco_categories_format


async def _get_image_dimension_map(
    datapoints: List[Dict],
) -> Dict[str, Tuple[int, int]]:
    """Get a map from dpId to [width, height] of the images."""

    async def _get_size(
        session: aiohttp.ClientSession, datapoint: Dict
    ) -> Tuple[int, int, str]:
        async with session.get(
            # encode with yarl so that aiohttp doesn't encode again.
            URL(datapoint["itemsPresigned"][0], encoded=True)
        ) as response:
            temp = await aioimgspy.probe(response.content)  # type: ignore
            return (temp["width"], temp["height"], datapoint["dpId"])

    # limit to 30, default is 100, cleanup is done by session
    conn = aiohttp.TCPConnector(limit=30)
    async with aiohttp.ClientSession(connector=conn) as session:
        coros = [_get_size(session, dpoint) for dpoint in datapoints]
        all_sizes = await gather_with_concurrency(10, coros, "Getting image dimensions")

    await asyncio.sleep(0.250)  # give time to close ssl connections
    return {temp[2]: (temp[0], temp[1]) for temp in all_sizes}


# pylint: disable=too-many-locals
def coco_converter(
    datapoints: List[Dict],
    taxonomy: Dict,
    image_dims_map: Optional[Dict[str, Tuple[int, int]]] = None,
) -> Dict:
    """Convert redbrick labels to standard coco format."""
    coco_categories = rb2coco_categories_format(taxonomy)

    if image_dims_map is None:
        image_dims_map = asyncio.run(_get_image_dimension_map(datapoints))

    images: List[Dict] = []
    annotations: List[Dict] = []
    for data in datapoints:
        file_name = data["name"]
        dp_id = data["dpId"]
        labels = data["labels"]

        width, height = image_dims_map[dp_id]

        current_image_id = len(images)
        image_entry = {
            "id": current_image_id,
            "file_name": file_name,
            "raw_url": data["items"][0],
            "dp_id": data["dpId"],
            "height": height,
            "width": width,
        }
        if "itemsPresigned" in data:
            image_entry["signed_url"] = data["itemsPresigned"][0]

        for label in labels:
            annotation_index = len(annotations)
            if label.get("bbox2d"):
                class_id = rb_get_class_id(label["category"][0], taxonomy)
                coco_label = rb2coco_bbox(
                    label, annotation_index, current_image_id, class_id, width, height
                )
                annotations.append(coco_label)
            elif label.get("polygon"):
                class_id = rb_get_class_id(label["category"][0], taxonomy)
                coco_label = rb2coco_polygon(
                    label, annotation_index, current_image_id, class_id, width, height
                )
                annotations.append(coco_label)
            else:
                print_error(
                    "Label not converted, Coco format only supports bbox and polygon labels."
                )
        images.append(image_entry)

    return {
        "images": images,
        "annotations": annotations,
        "categories": coco_categories,
        "info": {},
        "licenses": [],
    }
