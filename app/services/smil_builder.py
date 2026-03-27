from lxml import etree

class SMILBuilder:
    def __init__(self):
        self.root = etree.Element("smil", xmlns="http://www.w3.org/2001/SMIL20/Language")
        self.head = etree.SubElement(self.root, "head")
        self.layout = etree.SubElement(self.head, "layout")
        self.body = etree.SubElement(self.root, "body")

    def add_region(self, id, top=0, left=0, width="100%", height="100%", z_index=1):
        region = etree.SubElement(self.layout, "region", id=id)
        region.set("top", str(top))
        region.set("left", str(left))
        region.set("width", str(width))
        region.set("height", str(height))
        region.set("z-index", str(z_index))
        return region

    def add_video(self, src, region_id, dur=None):
        video = etree.SubElement(self.body, "video", src=src, region=region_id)
        if dur:
            video.set("dur", str(dur))
        return video

    def add_image(self, src, region_id, dur="10s"):
        image = etree.SubElement(self.body, "img", src=src, region=region_id)
        image.set("dur", str(dur))
        return image

    def get_smil_string(self):
        return etree.tostring(self.root, pretty_print=True, xml_declaration=True, encoding='UTF-8').decode('UTF-8')
